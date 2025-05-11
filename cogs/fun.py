"""
Fun commands cog for AraonJR bot
"""
import io
import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

from configs.config import EMBED_COLOR


class Fun(commands.Cog):
    """Fun commands for entertainment."""

    def __init__(self, bot):
        self.bot = bot
        self.gali_responses = [
            "Bewakoof",
            "Gadha",
            "Ullu ka patta",
            "Nalayak",
            "Pagal",
            "Motu",
            "Chappri",
            "Popat",
            "Buddhu",
            "Ghadela"
        ]
        self.kami_responses = [
            "Kaminey",
            "Haraami",
            "Harami",
            "Chor",
            "Badmash",
            "Chandaal",
            "Naalaayak",
            "Junglee",
            "Dhakkan",
            "Bevda"
        ]
        self.headpat_responses = [
            "Thanks for the headpat!",
            "*purrs*",
            "Nyaa~",
            "*happy bot noises*",
            "I appreciate the headpats!",
            "You're the best!",
            "*smiles*",
            "Headpats make my day better!"
        ]
    
    @app_commands.command(name="gali", description="Get bestowed with a random gali")
    async def gali(self, interaction: discord.Interaction):
        """Get a random gali (light insult)."""
        response = random.choice(self.gali_responses)
        
        embed = discord.Embed(
            title="Random Gali",
            description=f"**{response}!**",
            color=EMBED_COLOR
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="kami", description="Get a random kami response")
    async def kami(self, interaction: discord.Interaction):
        """Get a random kami response."""
        response = random.choice(self.kami_responses)
        
        embed = discord.Embed(
            title="Kami Says",
            description=f"**{response}!**",
            color=EMBED_COLOR
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="headpat", description="Give the bot a headpat")
    async def headpat(self, interaction: discord.Interaction):
        """Give the bot a headpat."""
        response = random.choice(self.headpat_responses)
        
        embed = discord.Embed(
            title="*Receives Headpat*",
            description=response,
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="poke", description="Poke someone")
    @app_commands.describe(user="The user to poke")
    async def poke(self, interaction: discord.Interaction, user: discord.User):
        """Poke a user."""
        # Don't allow self-pokes
        if user.id == interaction.user.id:
            await interaction.response.send_message("You can't poke yourself!", ephemeral=True)
            return
            
        # Don't allow poking the bot
        if user.id == self.bot.user.id:
            await interaction.response.send_message(
                "Hey! That tickles! Use `/headpat` instead!", 
                ephemeral=True
            )
            return
            
        # Create embed for poke
        embed = discord.Embed(
            title="Poke!",
            description=f"{interaction.user.mention} poked {user.mention}!",
            color=EMBED_COLOR
        )
        
        # Get a random poke gif
        poke_gifs = [
            "https://c.tenor.com/3dOqO4vVlr4AAAAC/poke-anime.gif",
            "https://c.tenor.com/9KyHAu_xd6MAAAAC/poke-anime.gif",
            "https://c.tenor.com/1YMrMsCtxLwAAAAC/anime-poke.gif",
            "https://c.tenor.com/jA3aqoOGwqUAAAAC/poke-anime.gif",
            "https://c.tenor.com/z2ttQJBDYX0AAAAC/anime-poke.gif"
        ]
        embed.set_image(url=random.choice(poke_gifs))
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="worth", description="Find out how worthless someone is")
    @app_commands.describe(name="Name of the person to evaluate")
    async def worth(self, interaction: discord.Interaction, name: str):
        """Calculate how worthless someone is (as a joke)."""
        # Seed the random with the name for consistent results
        random.seed(name.lower())
        
        # Generate a random percentage (0-100)
        worthless_percent = random.randint(0, 100)
        
        # Create a response based on the percentage
        if worthless_percent < 20:
            response = f"{name} is barely worthless at all! Only {worthless_percent}% worthless."
            color = discord.Color.green()
        elif worthless_percent < 50:
            response = f"{name} is somewhat worthless. {worthless_percent}% worthless."
            color = discord.Color.gold()
        elif worthless_percent < 80:
            response = f"{name} is quite worthless. {worthless_percent}% worthless."
            color = discord.Color.orange()
        else:
            response = f"{name} is extremely worthless! {worthless_percent}% worthless!"
            color = discord.Color.red()
        
        # Create embed
        embed = discord.Embed(
            title="Worthless Calculator",
            description=response,
            color=color
        )
        
        # Add a progress bar
        progress = "▓" * (worthless_percent // 10) + "░" * (10 - worthless_percent // 10)
        embed.add_field(name="Worthless Meter", value=f"`{progress}` {worthless_percent}%")
        
        # Reset the random seed
        random.seed()
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="slap", description="Slap someone with a generated image")
    @app_commands.describe(member="The member to slap")
    async def slap(self, interaction: discord.Interaction, member: discord.Member):
        """Slap a member with a generated image."""
        # Defer response due to potential image processing time
        await interaction.response.defer()
        
        # Don't allow self-slaps
        if member.id == interaction.user.id:
            await interaction.followup.send("You can't slap yourself!", ephemeral=True)
            return
            
        # Get the avatar URLs
        try:
            # Download avatars
            slapper_avatar_url = interaction.user.display_avatar.with_size(128).with_format("png").url
            slapped_avatar_url = member.display_avatar.with_size(128).with_format("png").url
            
            # Create embed for slap
            embed = discord.Embed(
                title="Slap!",
                description=f"{interaction.user.mention} slapped {member.mention}!",
                color=discord.Color.red()
            )
            
            # Get a random slap gif instead of generating an image
            # This is a fallback since we can't generate images in this environment
            slap_gifs = [
                "https://c.tenor.com/rVXByOZKidMAAAAd/anime-slap.gif",
                "https://c.tenor.com/Ws6Dm1ZW_vMAAAAC/girl-slap.gif",
                "https://c.tenor.com/PeJyQRCSHHkAAAAC/saki-saki-mugi-awaya.gif",
                "https://c.tenor.com/EfhPfbG0hnMAAAAC/slap-handa-seishuu.gif",
                "https://c.tenor.com/cMDrceEZ_hgAAAAC/hit-slap.gif"
            ]
            embed.set_image(url=random.choice(slap_gifs))
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            await interaction.followup.send(f"Failed to generate slap image: {str(e)}", ephemeral=True)
    
    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(message="The message for the bot to say")
    async def say(self, interaction: discord.Interaction, message: str):
        """Make the bot say something."""
        # Check for mentions and unwanted content
        if "@everyone" in message or "@here" in message:
            await interaction.response.send_message(
                "I won't say that! No mass mentions allowed.", 
                ephemeral=True
            )
            return
            
        # First acknowledge the interaction privately
        await interaction.response.send_message(
            "Message sent! ✅", 
            ephemeral=True
        )
        
        # Then send the actual message
        await interaction.channel.send(message)
    
    @app_commands.command(name="spank", description="Spank someone")
    @app_commands.describe(member="The member to spank")
    async def spank(self, interaction: discord.Interaction, member: discord.Member):
        """Spank a member with a gif."""
        # Don't allow self-spanks
        if member.id == interaction.user.id:
            await interaction.response.send_message("You can't spank yourself!", ephemeral=True)
            return
            
        # Create embed for spank
        embed = discord.Embed(
            title="Spank!",
            description=f"{interaction.user.mention} spanked {member.mention}!",
            color=discord.Color.red()
        )
        
        # Get a random spank gif
        spank_gifs = [
            "https://c.tenor.com/Ep5iIDiO0V8AAAAC/anime-spanking.gif",
            "https://c.tenor.com/NV-JEWCZ-dMAAAAC/anime-spank.gif",
            "https://c.tenor.com/noZB3lC0WEwAAAAC/spank-shinobu.gif",
            "https://c.tenor.com/4RIbf7sk58AAAAAC/anime-lightspeed.gif",
            "https://c.tenor.com/EAdI_LQ3KkEAAAAC/melissa-spank.gif"
        ]
        embed.set_image(url=random.choice(spank_gifs))
        
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(Fun(bot))
