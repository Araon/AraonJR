"""
Moderation commands cog for AraonJR bot
"""
import discord
from discord import app_commands
from discord.ext import commands

from configs.config import EMBED_COLOR


class Moderation(commands.Cog):
    """Moderation commands for server management."""

    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.describe(
        member="The member to kick",
        reason="Reason for kicking the member"
    )
    @app_commands.default_permissions(kick_members=True)
    @app_commands.guild_only()
    async def kick(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member, 
        reason: str = None
    ):
        """Kick a member from the server."""
        # Check if the bot can kick members
        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message(
                "I don't have permission to kick members.", 
                ephemeral=True
            )
            return
            
        # Check if the target is higher than the bot in hierarchy
        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "I can't kick this member because they have a higher or equal role to me.", 
                ephemeral=True
            )
            return
            
        # Check if the user is trying to kick themselves
        if member.id == interaction.user.id:
            await interaction.response.send_message(
                "You can't kick yourself!", 
                ephemeral=True
            )
            return
            
        # Check if the user is trying to kick the bot
        if member.id == self.bot.user.id:
            await interaction.response.send_message(
                "I can't kick myself!", 
                ephemeral=True
            )
            return

        # Format reason
        reason = reason or f"Kicked by {interaction.user}"
        full_reason = f"{reason} | Kicked by {interaction.user}"
        
        # Kick the member
        try:
            await member.kick(reason=full_reason)
            
            # Create embed for confirmation
            embed = discord.Embed(
                title="✅ Member Kicked",
                description=f"{member.mention} has been kicked from the server.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"Kicked by {interaction.user}")
            
            await interaction.response.send_message(embed=embed)
            
            # Try to DM the kicked member
            try:
                dm_embed = discord.Embed(
                    title=f"You've been kicked from {interaction.guild.name}",
                    description=f"Reason: {reason}",
                    color=discord.Color.orange()
                )
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                # Unable to DM the user
                pass
                
        except discord.Forbidden:
            await interaction.response.send_message(
                "I couldn't kick that member. Check my permissions.", 
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"An error occurred: {e}", 
                ephemeral=True
            )
    
    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.describe(
        member="The member to ban",
        reason="Reason for banning the member",
        delete_days="Number of days of messages to delete (0-7)"
    )
    @app_commands.default_permissions(ban_members=True)
    @app_commands.guild_only()
    async def ban(
        self, 
        interaction: discord.Interaction, 
        member: discord.Member, 
        reason: str = None,
        delete_days: int = 1
    ):
        """Ban a member from the server."""
        # Check if the bot can ban members
        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                "I don't have permission to ban members.", 
                ephemeral=True
            )
            return
            
        # Check if the target is higher than the bot in hierarchy
        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "I can't ban this member because they have a higher or equal role to me.", 
                ephemeral=True
            )
            return
            
        # Check if the user is trying to ban themselves
        if member.id == interaction.user.id:
            await interaction.response.send_message(
                "You can't ban yourself!", 
                ephemeral=True
            )
            return
            
        # Check if the user is trying to ban the bot
        if member.id == self.bot.user.id:
            await interaction.response.send_message(
                "I can't ban myself!", 
                ephemeral=True
            )
            return

        # Validate delete_days
        delete_days = max(0, min(delete_days, 7))  # Clamp between 0-7
        
        # Format reason
        reason = reason or f"Banned by {interaction.user}"
        full_reason = f"{reason} | Banned by {interaction.user}"
        
        # Ban the member
        try:
            await member.ban(
                reason=full_reason,
                delete_message_days=delete_days
            )
            
            # Create embed for confirmation
            embed = discord.Embed(
                title="🔨 Member Banned",
                description=f"{member.mention} has been banned from the server.",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Message History Deleted", value=f"{delete_days} day(s)")
            embed.set_footer(text=f"Banned by {interaction.user}")
            
            await interaction.response.send_message(embed=embed)
            
            # Try to DM the banned member
            try:
                dm_embed = discord.Embed(
                    title=f"You've been banned from {interaction.guild.name}",
                    description=f"Reason: {reason}",
                    color=discord.Color.red()
                )
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                # Unable to DM the user
                pass
                
        except discord.Forbidden:
            await interaction.response.send_message(
                "I couldn't ban that member. Check my permissions.", 
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"An error occurred: {e}", 
                ephemeral=True
            )
    
    @app_commands.command(name="unban", description="Unban a member from the server")
    @app_commands.describe(
        user_id="The ID of the user to unban",
        reason="Reason for unbanning the user"
    )
    @app_commands.default_permissions(ban_members=True)
    @app_commands.guild_only()
    async def unban(
        self, 
        interaction: discord.Interaction, 
        user_id: str, 
        reason: str = None
    ):
        """Unban a user from the server."""
        # Check if the bot can ban members
        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                "I don't have permission to unban members.", 
                ephemeral=True
            )
            return
        
        # Validate user_id
        try:
            user_id = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                "Please provide a valid user ID.", 
                ephemeral=True
            )
            return
        
        # Format reason
        reason = reason or f"Unbanned by {interaction.user}"
        full_reason = f"{reason} | Unbanned by {interaction.user}"
        
        # Unban the user
        try:
            # Defer response since fetching bans might take time
            await interaction.response.defer(ephemeral=False)
            
            # Try to get the ban entry
            bans = [ban async for ban in interaction.guild.bans()]
            banned_user = discord.utils.find(lambda ban: ban.user.id == user_id, bans)
            
            if not banned_user:
                await interaction.followup.send(
                    "That user is not banned from this server.", 
                    ephemeral=True
                )
                return
                
            # Unban the user
            await interaction.guild.unban(banned_user.user, reason=full_reason)
            
            # Create embed for confirmation
            embed = discord.Embed(
                title="✅ User Unbanned",
                description=f"{banned_user.user.mention} ({banned_user.user}) has been unbanned from the server.",
                color=discord.Color.green()
            )
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"Unbanned by {interaction.user}")
            
            await interaction.followup.send(embed=embed)
                
        except discord.Forbidden:
            await interaction.followup.send(
                "I couldn't unban that user. Check my permissions.", 
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"An error occurred: {e}", 
                ephemeral=True
            )
    
    @app_commands.command(name="clear", description="Clear messages from the channel")
    @app_commands.describe(
        amount="Number of messages to delete (1-100)",
        user="Only delete messages from this user (optional)"
    )
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    async def clear(
        self, 
        interaction: discord.Interaction, 
        amount: int,
        user: discord.User = None
    ):
        """Clear messages from the channel."""
        # Check if the bot can manage messages
        if not interaction.channel.permissions_for(interaction.guild.me).manage_messages:
            await interaction.response.send_message(
                "I don't have permission to delete messages.", 
                ephemeral=True
            )
            return
        
        # Validate amount
        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "Please provide a number between 1 and 100.", 
                ephemeral=True
            )
            return
        
        # Defer response since deletion might take time
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Define a check if user is specified
            def check(message):
                return user is None or message.author.id == user.id
            
            # Delete messages
            if user:
                # When filtering by user, we need to fetch more messages
                # because not all will match our filter
                messages = []
                async for message in interaction.channel.history(limit=min(amount * 5, 500)):
                    if check(message):
                        messages.append(message)
                        if len(messages) >= amount:
                            break
                
                # Delete the messages
                if messages:
                    await interaction.channel.delete_messages(messages[:amount])
                    
                deleted = len(messages[:amount])
            else:
                # Simple case, delete the specified number
                deleted = len(await interaction.channel.purge(limit=amount))
            
            # Send confirmation
            await interaction.followup.send(
                f"✅ Successfully deleted {deleted} message(s)." +
                (f" from {user.mention}" if user else ""),
                ephemeral=True
            )
                
        except discord.Forbidden:
            await interaction.followup.send(
                "I couldn't delete those messages. Check my permissions.", 
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"An error occurred: {e}", 
                ephemeral=True
            )


async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(Moderation(bot))
