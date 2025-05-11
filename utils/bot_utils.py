"""
Common utility functions for the bot
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import List, Optional, Union

import discord
from discord.ext import commands

logger = logging.getLogger("discord")


async def log_to_file(message: str, filename: str = "botlog.txt") -> None:
    """
    Asynchronously log a message to a specified file.
    
    Args:
        message: The message to log
        filename: The file to log to (default: botlog.txt)
    """
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%c")
            f.write(f'\n[{timestamp}] {message}')
    except Exception as e:
        logger.error(f"Error writing to log file: {e}")


def get_embed_color(user: Optional[discord.Member] = None) -> discord.Color:
    """
    Get an appropriate embed color based on a user or default color.
    
    Args:
        user: Optional Discord member to use color from
        
    Returns:
        Discord Color for embeds
    """
    if user and hasattr(user, "color") and user.color != discord.Color.default():
        return user.color
    
    # Default blue color
    return discord.Color.from_rgb(52, 152, 219)


def format_uptime(start_time: datetime) -> str:
    """
    Format the uptime duration into a readable string.
    
    Args:
        start_time: The datetime when the bot started
        
    Returns:
        A formatted string representing the uptime
    """
    now = datetime.now()
    delta = now - start_time
    
    # Extract time components
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format the string based on how long it's been up
    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes, {seconds} seconds"
    else:
        return f"{minutes} minutes, {seconds} seconds"


def is_nsfw_channel(channel: Union[discord.TextChannel, discord.DMChannel, discord.Thread]) -> bool:
    """
    Check if a channel is marked as NSFW.
    
    Args:
        channel: The channel to check
        
    Returns:
        True if the channel is NSFW, False otherwise
    """
    if isinstance(channel, discord.TextChannel):
        return channel.is_nsfw()
    elif isinstance(channel, discord.Thread):
        return channel.parent.is_nsfw() if channel.parent else False
    
    return False


class BotResponseButton(discord.ui.View):
    """Interactive button for bot responses."""
    
    def __init__(self, user_id: int):
        """Initialize the button view."""
        super().__init__(timeout=60)  # 60 second timeout
        self.user_id = user_id
        self.value = None
    
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle 'Yes' button press."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This button isn't for you!", ephemeral=True)
            return
            
        self.value = True
        await interaction.response.edit_message(content="Response: Yes", view=None)
        self.stop()
    
    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle 'No' button press."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This button isn't for you!", ephemeral=True)
            return
            
        self.value = False
        await interaction.response.edit_message(content="Response: No", view=None)
        self.stop()


async def confirm_action(
    ctx_or_interaction: Union[commands.Context, discord.Interaction],
    message: str
) -> Optional[bool]:
    """
    Ask for confirmation with yes/no buttons.
    
    Args:
        ctx_or_interaction: The context or interaction
        message: The confirmation message to display
        
    Returns:
        True if confirmed, False if denied, None if timed out
    """
    # Determine if we're using a context or interaction
    if isinstance(ctx_or_interaction, commands.Context):
        # Handle Context (prefix commands)
        user_id = ctx_or_interaction.author.id
        view = BotResponseButton(user_id)
        message_obj = await ctx_or_interaction.send(message, view=view)
        
        # Wait for button press
        await view.wait()
        
        # Clean up the message if we can
        try:
            await message_obj.delete()
        except discord.HTTPException:
            pass
            
        return view.value
    else:
        # Handle Interaction (slash commands)
        user_id = ctx_or_interaction.user.id
        view = BotResponseButton(user_id)
        
        await ctx_or_interaction.response.send_message(message, view=view, ephemeral=True)
        
        # Wait for button press
        await view.wait()
        
        return view.value
