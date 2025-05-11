"""
Utility commands cog for AraonJR bot
"""
import discord
from discord import app_commands
from discord.ext import commands

from configs.config import EMBED_COLOR
from utils.sentiment_utils import analyze_sentiment, get_sentiment_emoji
from utils.wiki_utils import get_wiki_summary


class Utility(commands.Cog):
    """Utility commands for various helpful functions."""

    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="wiki", description="Get a summary from Wikipedia")
    @app_commands.describe(topic="The topic to search for on Wikipedia")
    async def wiki(self, interaction: discord.Interaction, topic: str):
        """Get a brief summary from Wikipedia."""
        await interaction.response.defer()
        
        success, result = await get_wiki_summary(topic, sentences=3)
        
        if success:
            summary, url = result
            embed = discord.Embed(
                title=f"Wikipedia: {topic}",
                description=summary,
                color=EMBED_COLOR,
                url=url
            )
            embed.set_footer(text="Source: Wikipedia | Limited to 3 sentences")
            await interaction.followup.send(embed=embed)
        else:
            # Error occurred
            embed = discord.Embed(
                title="Wikipedia Error",
                description=result,
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="sentiment", description="Analyze the sentiment of a message")
    @app_commands.describe(text="The text to analyze")
    async def sentiment(self, interaction: discord.Interaction, text: str):
        """Analyze the sentiment of the given text."""
        await interaction.response.defer()
        
        # Analyze sentiment
        result = await analyze_sentiment(text)
        
        # Get appropriate emoji
        emoji = get_sentiment_emoji(result["result"])
        
        # Create result embed
        embed = discord.Embed(
            title="Sentiment Analysis",
            description=f"Text: {text}",
            color=EMBED_COLOR
        )
        
        # Add sentiment results
        sentiment_text = f"{emoji} "
        if result["result"].name == "POSITIVE":
            sentiment_text += "Positive"
            embed.color = discord.Color.green()
        elif result["result"].name == "NEGATIVE":
            sentiment_text += "Negative"
            embed.color = discord.Color.red()
        else:
            sentiment_text += "Neutral"
            embed.color = discord.Color.light_gray()
            
        embed.add_field(name="Sentiment", value=sentiment_text, inline=False)
        embed.add_field(name="Polarity", value=f"{result['polarity']:.2f} (-1.0 to 1.0)", inline=True)
        embed.add_field(name="Subjectivity", value=f"{result['subjectivity']:.2f} (0.0 to 1.0)", inline=True)
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="avatar", description="Show a user's avatar")
    @app_commands.describe(user="The user whose avatar to show")
    async def avatar(self, interaction: discord.Interaction, user: discord.User = None):
        """Display a user's avatar."""
        # Default to the command user if no user specified
        target_user = user or interaction.user
        
        # Create embed
        embed = discord.Embed(
            title=f"{target_user.display_name}'s Avatar",
            color=EMBED_COLOR
        )
        
        # Add avatar image
        embed.set_image(url=target_user.display_avatar.url)
        
        # Add links to different formats
        formats = []
        if target_user.display_avatar.is_animated():
            formats.append(f"[GIF]({target_user.display_avatar.with_format('gif').url})")
        formats.append(f"[PNG]({target_user.display_avatar.with_format('png').url})")
        formats.append(f"[JPG]({target_user.display_avatar.with_format('jpg').url})")
        formats.append(f"[WEBP]({target_user.display_avatar.with_format('webp').url})")
        
        embed.add_field(name="Links", value=" | ".join(formats))
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo", description="Show information about a user")
    @app_commands.describe(user="The user to get information about")
    @app_commands.guild_only()
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        """Display information about a user."""
        # Default to the command user if no user specified
        target_user = user or interaction.user
        
        # Create embed
        embed = discord.Embed(
            title=f"User Information: {target_user.display_name}",
            color=target_user.color if hasattr(target_user, "color") else EMBED_COLOR
        )
        
        # Add user avatar
        embed.set_thumbnail(url=target_user.display_avatar.url)
        
        # Basic information
        embed.add_field(name="Username", value=str(target_user), inline=True)
        embed.add_field(name="User ID", value=target_user.id, inline=True)
        embed.add_field(name="Bot", value="Yes" if target_user.bot else "No", inline=True)
        
        # Dates
        created_at = target_user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        embed.add_field(name="Account Created", value=created_at, inline=True)
        
        if hasattr(target_user, "joined_at") and target_user.joined_at:
            joined_at = target_user.joined_at.strftime("%Y-%m-%d %H:%M:%S")
            embed.add_field(name="Joined Server", value=joined_at, inline=True)
        
        # Roles (if in guild)
        if hasattr(target_user, "roles"):
            role_list = [role.mention for role in reversed(target_user.roles) if role.name != "@everyone"]
            if role_list:
                embed.add_field(name=f"Roles ({len(role_list)})", value=" ".join(role_list[:10]), inline=False)
                if len(role_list) > 10:
                    embed.add_field(name="", value="...and more", inline=False)
        
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(Utility(bot))
