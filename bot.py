"""
AraonJR Discord Bot - Modernized Version
A multipurpose Discord bot with various commands and features.
"""
import asyncio
import logging
import os
import platform
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from configs.config import BOT_TOKEN, OWNER_ID, PREFIX, VERSION

# Configure logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content
intents.members = True  # Needed for welcome messages

class AraonJR(commands.Bot):
    """Main bot class with extended functionality."""
    
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),
            intents=intents,
            help_command=None,  # We'll implement our own help command
            activity=discord.Game(name="and doing her best"),
            status=discord.Status.online
        )
        self.start_time = None
        self.owner_id = OWNER_ID
        self.version = VERSION
        
    async def setup_hook(self):
        """Called when the bot is setting up, before login."""
        self.start_time = datetime.now()
        
        # Load cogs
        await self.load_cogs()
        
        # Sync app commands
        logger.info("Syncing application commands...")
        
    async def load_cogs(self):
        """Load all cog extensions."""
        logger.info("Loading cogs...")
        cog_count = 0
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('_'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f"Loaded cog: {filename}")
                    cog_count += 1
                except Exception as e:
                    logger.error(f"Failed to load cog {filename}: {str(e)}")
        
        logger.info(f"Loaded {cog_count} cogs.")
    
    async def on_ready(self):
        """Event triggered when the bot is ready and connected."""
        logger.info(f"Logged in as {self.user.name} | {self.user.id}")
        logger.info(f"Discord.py Version: {discord.__version__}")
        logger.info(f"Python Version: {platform.python_version()}")
        logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        
        # Log to file
        with open('botlog.txt', 'a', encoding='utf-8') as f:
            f.write(f'\nBot Online from {self.start_time.strftime("%c")}')
            
        print(f"AraonJR v{self.version} is ready!")
        print(f"Started at: {self.start_time.strftime('%c')}")
        
        # Sync commands only to test guild in development
        # await self.tree.sync()  # Uncomment for global sync when ready

    async def on_guild_join(self, guild):
        """Event triggered when the bot joins a new guild."""
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        
        # Try to send welcome message
        general = discord.utils.find(lambda x: x.name.lower() == 'general', guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send(f"Hey it's me, AraonJR! {guild.name} sure looks cozy!")
    
    async def on_member_join(self, member):
        """Event triggered when a new member joins a guild."""
        guild = member.guild
        if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
            welcome_embed = discord.Embed(
                title="New Member!",
                description=f"Hey {member.mention}, welcome to {guild.name}!",
                color=discord.Color.green()
            )
            welcome_embed.set_thumbnail(url=member.display_avatar.url)
            welcome_embed.set_footer(text=f"Member #{len(guild.members)}")
            
            await guild.system_channel.send(embed=welcome_embed)
            
        # Log join
        with open('botlog.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{member} has joined {guild.name} on {datetime.now().strftime("%c")}')
    
    async def on_member_remove(self, member):
        """Event triggered when a member leaves a guild."""
        # Log leave
        with open('botlog.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{member} has left {member.guild.name} on {datetime.now().strftime("%c")}')

    async def on_error(self, event_method: str, *args, **kwargs):
        """Global error handler for all events."""
        logger.error(f'Error in {event_method}:', exc_info=True)
        
        # Log to file
        with open('error.log', 'a', encoding='utf-8') as f:
            f.write(f'\nError in {event_method} at {datetime.now().strftime("%c")}\n')
            import traceback
            traceback.print_exc(file=f)

    async def on_command_error(self, ctx, error):
        """Global error handler for command errors."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
            
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"❌ You don't have permission to use this command.")
            return
            
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"❌ I don't have the required permissions to do that.")
            return
            
        # Log the error
        logger.error(f'Command error in {ctx.command}:', exc_info=error)
        
        # Notify the user
        error_msg = f"❌ An error occurred: {str(error)}"
        try:
            await ctx.send(error_msg)
        except discord.HTTPException:
            # If we can't send to the channel, try to DM the user
            try:
                await ctx.author.send(error_msg)
            except discord.HTTPException:
                pass  # Can't send messages to the user

    async def on_application_command_error(self, interaction: discord.Interaction, error):
        """Global error handler for application command errors."""
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"⏳ This command is on cooldown. Try again in {error.retry_after:.2f}s.",
                ephemeral=True
            )
            return
            
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        # Log the error
        logger.error(f'Application command error:', exc_info=error)
        
        # Notify the user
        try:
            if interaction.response.is_done():
                await interaction.followup.send(
                    f"❌ An error occurred: {str(error)}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"❌ An error occurred: {str(error)}",
                    ephemeral=True
                )

# Command group for owner-only commands
@app_commands.guild_only()
class OwnerCog(commands.GroupCog, name="owner"):
    def __init__(self, bot: AraonJR):
        self.bot = bot
        super().__init__()
    
    async def cog_check(self, ctx):
        """Check if the user is the bot owner."""
        return await self.bot.is_owner(ctx.author)
    
    @app_commands.command(name="sync", description="Sync application commands")
    @app_commands.describe(scope="The scope to sync commands to (global/guild)")
    async def sync(self, interaction: discord.Interaction, scope: str = "guild"):
        """Sync application commands to the current guild or globally."""
        if scope.lower() == "global":
            await self.bot.tree.sync()
            await interaction.response.send_message("Synced commands globally.")
        elif scope.lower() == "guild":
            self.bot.tree.copy_global_to(guild=interaction.guild)
            await self.bot.tree.sync(guild=interaction.guild)
            await interaction.response.send_message(f"Synced commands to {interaction.guild.name}.")
        else:
            await interaction.response.send_message("Invalid scope. Use 'global' or 'guild'.")

async def main():
    """Main entry point for the bot."""
    bot = AraonJR()
    await bot.add_cog(OwnerCog(bot))
    
    async with bot:
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
