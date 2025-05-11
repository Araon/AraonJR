"""
Pytest configuration for Discord bot tests.
"""
import asyncio
from unittest.mock import MagicMock, patch

import discord
import pytest
import pytest_asyncio
from discord.ext import commands

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch("os.getenv") as mock_getenv:
        # Setup default mock values for environment variables
        mock_getenv.return_value = "mock_token"
        yield mock_getenv


# Create a pytest fixture for an async event loop
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Create a mock bot instance for testing
@pytest_asyncio.fixture
async def mock_bot():
    # Create instance of the bot with mocked values
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix=";", intents=intents)
    
    # Mock bot attributes
    bot.user = MagicMock()
    bot.user.id = 123456789
    bot.user.name = "MockBot"
    
    # Return the bot
    yield bot
    
    # Cleanup
    await bot.close()


# Mock Discord Interaction for testing slash commands
@pytest.fixture
def mock_interaction():
    mock = MagicMock(spec=discord.Interaction)
    mock.response = MagicMock()
    mock.response.send_message = MagicMock()
    mock.followup = MagicMock()
    mock.followup.send = MagicMock()
    mock.user = MagicMock(spec=discord.User)
    mock.user.id = 987654321
    mock.user.name = "TestUser"
    mock.user.display_name = "Test User"
    mock.user.mention = "<@987654321>"
    mock.user.display_avatar = MagicMock()
    mock.user.display_avatar.url = "https://example.com/avatar.png"
    
    # Setup guild properties
    mock.guild = MagicMock(spec=discord.Guild)
    mock.guild.id = 123123123
    mock.guild.name = "Test Guild"
    mock.guild.me = MagicMock(spec=discord.Member)
    
    # Setup channel properties
    mock.channel = MagicMock(spec=discord.TextChannel)
    mock.channel.send = MagicMock()
    mock.channel.permissions_for.return_value = discord.Permissions(
        send_messages=True,
        embed_links=True,
        attach_files=True
    )
    
    return mock
