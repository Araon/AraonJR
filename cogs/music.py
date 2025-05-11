"""
Music commands cog for AraonJR bot using Wavelink
"""
import asyncio
import datetime
import re
from typing import Optional

import discord
import wavelink
from discord import app_commands
from discord.ext import commands

from configs.config import EMBED_COLOR


class MusicPlayerView(discord.ui.View):
    """Interactive music player view with controls."""
    
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog
    
    @discord.ui.button(label="Pause/Resume", style=discord.ButtonStyle.primary, emoji="⏯️")
    async def pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = interaction.guild.voice_client
        if not player:
            return await interaction.response.send_message("Not currently playing anything.", ephemeral=True)
        
        if player.paused:
            await player.resume()
            await interaction.response.send_message("▶️ Resumed the music!", ephemeral=True)
        else:
            await player.pause()
            await interaction.response.send_message("⏸️ Paused the music!", ephemeral=True)
    
    @discord.ui.button(label="Skip", style=discord.ButtonStyle.primary, emoji="⏭️")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = interaction.guild.voice_client
        if not player:
            return await interaction.response.send_message("Not currently playing anything.", ephemeral=True)
        
        await player.stop()
        await interaction.response.send_message("⏭️ Skipped the current track!", ephemeral=True)
    
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️")
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = interaction.guild.voice_client
        if not player:
            return await interaction.response.send_message("Not currently playing anything.", ephemeral=True)
        
        await player.disconnect()
        await interaction.response.send_message("⏹️ Stopped the music and left the voice channel!", ephemeral=True)
    
    @discord.ui.button(label="Queue", style=discord.ButtonStyle.secondary, emoji="📜")
    async def queue(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = interaction.guild.voice_client
        if not player:
            return await interaction.response.send_message("Not currently playing anything.", ephemeral=True)
        
        if not player.queue:
            return await interaction.response.send_message("The queue is empty.", ephemeral=True)
        
        # Format the queue
        queue_str = "\n".join([
            f"**{i+1}.** {track.title} ({datetime.timedelta(milliseconds=track.length)})"
            for i, track in enumerate(player.queue[:10])
        ])
        
        if len(player.queue) > 10:
            queue_str += f"\n... and {len(player.queue) - 10} more tracks"
        
        embed = discord.Embed(
            title="Music Queue",
            description=queue_str,
            color=EMBED_COLOR
        )
        
        embed.set_footer(text=f"{len(player.queue)} tracks in queue")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class Music(commands.Cog):
    """Play music in voice channels with better quality and reliability."""

    def __init__(self, bot):
        self.bot = bot
        self.player_views = {}
        bot.loop.create_task(self.setup_wavelink())
    
    async def setup_wavelink(self):
        """Set up the Wavelink node."""
        await self.bot.wait_until_ready()
        
        # Initialize wavelink node
        nodes = [
            wavelink.Node(
                uri='http://localhost:2333',  # Default Lavalink server address
                password='youshallnotpass',   # Default Lavalink password
                inactive_player_timeout=300,
            )
        ]
        await wavelink.Pool.connect(nodes=nodes, client=self.bot)
    
    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        """Event triggered when a track starts playing."""
        player = payload.player
        track = payload.track
        
        if not player.guild:
            return
            
        channel = player.text_channel
        if not channel:
            return
        
        # Create embed for now playing
        embed = discord.Embed(
            title="Now Playing",
            description=f"[{track.title}]({track.uri})",
            color=EMBED_COLOR
        )
        
        # Add track information
        embed.add_field(name="Duration", value=str(datetime.timedelta(milliseconds=track.length)))
        embed.add_field(name="Requested By", value=track.extras.get('requester', 'Unknown'))
        
        # Add thumbnail if available
        if hasattr(track, 'artwork'):
            embed.set_thumbnail(url=track.artwork)
        
        # Create or update player view
        view = MusicPlayerView(self)
        self.player_views[player.guild.id] = view
        
        await channel.send(embed=embed, view=view)
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        """Event triggered when a track ends."""
        player = payload.player
        reason = payload.reason
        
        # If the player has been stopped or disconnected, do nothing
        if reason in (wavelink.TrackEndReason.STOPPED, wavelink.TrackEndReason.REPLACED):
            return
            
        # If autoplay is enabled and the queue is empty, try to play a related track
        if not player.queue and player.autoplay:
            await player.play(await player.get_tracks())
    
    @app_commands.command(name="play", description="Play a song or add it to the queue")
    @app_commands.describe(query="The song title, URL, or search query")
    @app_commands.guild_only()
    async def play(self, interaction: discord.Interaction, *, query: str):
        """Play a song in the voice channel."""
        # Check if the user is in a voice channel
        if not interaction.user.voice:
            return await interaction.response.send_message(
                "You need to be in a voice channel to use this command.", 
                ephemeral=True
            )
            
        # Defer the response since searching might take time
        await interaction.response.defer()
        
        # Connect to the voice channel if not already connected
        voice_channel = interaction.user.voice.channel
        
        # Get or create the player
        player: wavelink.Player = interaction.guild.voice_client or await voice_channel.connect(cls=wavelink.Player)
        
        # Set the text channel for notifications
        player.text_channel = interaction.channel
        
        # Search for the track
        if re.match(r'https?://', query):
            # URL input
            tracks = await wavelink.Playable.search(query)
        else:
            # Text search
            tracks = await wavelink.Playable.search(query, source=wavelink.TrackSource.YouTube)
        
        # Handle track search results
        if not tracks:
            return await interaction.followup.send("No matching tracks found.")
            
        # Handle playlists
        if isinstance(tracks, wavelink.Playlist):
            # Add requester info to all tracks
            for track in tracks.tracks:
                track.extras['requester'] = interaction.user.name
                
            # Add all tracks to the queue
            added = await player.queue.put_wait(tracks)
            
            # Start playing if not already
            if not player.playing:
                await player.play(player.queue.get(), volume=50)
            
            await interaction.followup.send(
                f"Added playlist **{tracks.name}** with {len(tracks.tracks)} tracks to the queue!"
            )
        else:
            # Single track
            track = tracks[0]
            track.extras['requester'] = interaction.user.name
            
            # Add to queue or play immediately
            if player.playing:
                await player.queue.put_wait(track)
                await interaction.followup.send(
                    f"Added **{track.title}** to the queue!"
                )
            else:
                await player.play(track, volume=50)
                await interaction.followup.send(
                    f"Now playing **{track.title}**!"
                )
    
    @app_commands.command(name="pause", description="Pause the currently playing track")
    @app_commands.guild_only()
    async def pause(self, interaction: discord.Interaction):
        """Pause the currently playing track."""
        # Check if the bot is in a voice channel
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(
                "I'm not currently playing anything.", 
                ephemeral=True
            )
            
        player = interaction.guild.voice_client
        
        # Check if already paused
        if player.paused:
            return await interaction.response.send_message(
                "The music is already paused.", 
                ephemeral=True
            )
            
        # Pause the player
        await player.pause()
        await interaction.response.send_message("⏸️ Paused the music!")
    
    @app_commands.command(name="resume", description="Resume the paused track")
    @app_commands.guild_only()
    async def resume(self, interaction: discord.Interaction):
        """Resume the paused track."""
        # Check if the bot is in a voice channel
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(
                "I'm not currently playing anything.", 
                ephemeral=True
            )
            
        player = interaction.guild.voice_client
        
        # Check if already playing
        if not player.paused:
            return await interaction.response.send_message(
                "The music is already playing.", 
                ephemeral=True
            )
            
        # Resume the player
        await player.resume()
        await interaction.response.send_message("▶️ Resumed the music!")
    
    @app_commands.command(name="stop", description="Stop the music and clear the queue")
    @app_commands.guild_only()
    async def stop(self, interaction: discord.Interaction):
        """Stop the music and clear the queue."""
        # Check if the bot is in a voice channel
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(
                "I'm not currently playing anything.", 
                ephemeral=True
            )
            
        player = interaction.guild.voice_client
        
        # Stop and disconnect
        await player.disconnect()
        
        # Remove the player view
        self.player_views.pop(interaction.guild.id, None)
        
        await interaction.response.send_message("⏹️ Stopped the music and left the voice channel!")
    
    @app_commands.command(name="skip", description="Skip the current track")
    @app_commands.guild_only()
    async def skip(self, interaction: discord.Interaction):
        """Skip the current track."""
        # Check if the bot is in a voice channel
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(
                "I'm not currently playing anything.", 
                ephemeral=True
            )
            
        player = interaction.guild.voice_client
        
        # Check if something is playing
        if not player.playing:
            return await interaction.response.send_message(
                "Nothing is currently playing.", 
                ephemeral=True
            )
            
        # Skip the current track
        await player.stop()
        await interaction.response.send_message("⏭️ Skipped the current track!")
    
    @app_commands.command(name="queue", description="View the current music queue")
    @app_commands.guild_only()
    async def queue(self, interaction: discord.Interaction):
        """View the current music queue."""
        # Check if the bot is in a voice channel
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(
                "I'm not currently playing anything.", 
                ephemeral=True
            )
            
        player = interaction.guild.voice_client
        
        # Check if queue is empty
        if not player.queue and not player.playing:
            return await interaction.response.send_message(
                "The queue is empty.", 
                ephemeral=True
            )
        
        # Create embed for queue
        embed = discord.Embed(
            title="Music Queue",
            color=EMBED_COLOR
        )
        
        # Add current track
        if player.playing:
            current_track = player.current
            embed.add_field(
                name="Currently Playing", 
                value=f"[{current_track.title}]({current_track.uri})\n" + 
                      f"Duration: {datetime.timedelta(milliseconds=current_track.length)}\n" +
                      f"Requested by: {current_track.extras.get('requester', 'Unknown')}",
                inline=False
            )
        
        # Format the queue
        if player.queue:
            queue_str = "\n".join([
                f"**{i+1}.** {track.title} ({datetime.timedelta(milliseconds=track.length)})"
                for i, track in enumerate(player.queue[:10])
            ])
            
            if len(player.queue) > 10:
                queue_str += f"\n... and {len(player.queue) - 10} more tracks"
                
            embed.add_field(name="Up Next", value=queue_str, inline=False)
        else:
            embed.add_field(name="Up Next", value="Nothing queued", inline=False)
        
        embed.set_footer(text=f"Total tracks in queue: {len(player.queue)}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="volume", description="Change the music volume")
    @app_commands.describe(level="Volume level (0-100)")
    @app_commands.guild_only()
    async def volume(self, interaction: discord.Interaction, level: int):
        """Change the music volume."""
        # Check if the bot is in a voice channel
        if not interaction.guild.voice_client:
            return await interaction.response.send_message(
                "I'm not currently playing anything.", 
                ephemeral=True
            )
            
        player = interaction.guild.voice_client
        
        # Validate volume level
        if level < 0 or level > 100:
            return await interaction.response.send_message(
                "Volume must be between 0 and 100.", 
                ephemeral=True
            )
            
        # Set the volume
        await player.set_volume(level)
        await interaction.response.send_message(f"🔊 Volume set to **{level}%**")


async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(Music(bot))
