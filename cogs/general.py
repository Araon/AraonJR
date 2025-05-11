"""
General commands cog for AraonJR bot
"""
import random
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from configs.config import EMBED_COLOR


class General(commands.Cog):
    """General purpose commands."""

    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {latency}ms",
            color=EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="date", description="Display the current date")
    async def date(self, interaction: discord.Interaction):
        """Display the current date."""
        embed = discord.Embed(
            title="📅 Date",
            description=f"Today's date is {datetime.now().strftime('%x')}",
            color=EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="toss", description="Flip a coin")
    async def toss(self, interaction: discord.Interaction):
        """Flip a coin."""
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(
            title="🪙 Coin Toss",
            description=f"Result: **{result}**!",
            color=EMBED_COLOR
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="invite", description="Generate an invite link for this server")
    @app_commands.guild_only()
    async def invite(self, interaction: discord.Interaction):
        """Generate an invite link for the current server."""
        # Check if the bot has permissions to create invites
        if not interaction.channel.permissions_for(interaction.guild.me).create_instant_invite:
            await interaction.response.send_message("I don't have permission to create invites in this channel.", ephemeral=True)
            return
            
        # Create invite with no expiration
        invite = await interaction.channel.create_invite(
            reason=f"Invite requested by {interaction.user}",
            max_age=0  # Never expire
        )
        
        embed = discord.Embed(
            title="🔗 Server Invite",
            description=f"Here's an invite link for **{interaction.guild.name}**:\n{invite.url}",
            color=EMBED_COLOR
        )
        embed.set_footer(text=f"Requested by {interaction.user}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="poll", description="Create a simple poll")
    @app_commands.describe(
        question="The question for your poll",
        option1="First option",
        option2="Second option"
    )
    async def poll(
        self, 
        interaction: discord.Interaction, 
        question: str,
        option1: str,
        option2: str,
        option3: str = None,
        option4: str = None
    ):
        """Create a poll with up to 4 options."""
        options = [option1, option2]
        if option3:
            options.append(option3)
        if option4:
            options.append(option4)
            
        # Create embed
        embed = discord.Embed(
            title="📊 " + question,
            description="\n".join([f"{i+1}️⃣ {option}" for i, option in enumerate(options)]),
            color=EMBED_COLOR
        )
        embed.set_footer(text=f"Poll by {interaction.user}")
        
        # Send poll message
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        # Add reactions
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        for i in range(len(options)):
            await message.add_reaction(reactions[i])
    
    @app_commands.command(name="help", description="Show help information")
    async def help_command(self, interaction: discord.Interaction):
        """Display help information about the bot."""
        embed = discord.Embed(
            title="AraonJR Help",
            description="Here are the available commands:",
            color=EMBED_COLOR
        )
        
        # Get all commands
        for command in self.bot.tree.get_commands():
            # Skip owner commands for non-owners
            if command.name == "owner" and interaction.user.id != self.bot.owner_id:
                continue
                
            if isinstance(command, app_commands.Group):
                embed.add_field(
                    name=f"/{command.name}",
                    value=command.description or "No description",
                    inline=False
                )
                for subcommand in command.commands:
                    embed.add_field(
                        name=f"/{command.name} {subcommand.name}",
                        value=subcommand.description or "No description",
                        inline=True
                    )
            else:
                embed.add_field(
                    name=f"/{command.name}",
                    value=command.description or "No description",
                    inline=True
                )
        
        embed.set_footer(text=f"AraonJR v{self.bot.version}")
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Process messages for custom responses."""
        # Ignore messages from bots to prevent loops
        if message.author.bot:
            return
            
        # Random chance to respond to mentions
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            responses = [
                "Did someone call for me?",
                "Hello there!",
                "I'm here!",
                "At your service!",
                "How can I help you today?"
            ]
            chance = random.randint(1, 100)
            if chance <= 70:  # 70% chance to respond
                await message.channel.send(random.choice(responses))


async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(General(bot))
