"""
Tests for the General cog.
"""
import unittest.mock
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
import pytest_asyncio

from cogs.general import General


class TestGeneralCog:
    """Test the general commands cog."""

    @pytest_asyncio.fixture
    async def general_cog(self, mock_bot):
        """Create an instance of the General cog for testing."""
        cog = General(mock_bot)
        return cog

    @pytest.mark.asyncio
    async def test_ping_command(self, general_cog, mock_interaction):
        """Test the ping command."""
        # Set up the mock
        mock_interaction.response.send_message = AsyncMock()
        
        # Set bot latency
        general_cog.bot.latency = 0.1  # 100ms
        
        # Call the command
        await general_cog.ping(mock_interaction)
        
        # Verify the response
        mock_interaction.response.send_message.assert_called_once()
        args, kwargs = mock_interaction.response.send_message.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Pong" in embed.title
        assert "100ms" in embed.description
    
    @pytest.mark.asyncio
    async def test_date_command(self, general_cog, mock_interaction):
        """Test the date command."""
        # Set up the mock
        mock_interaction.response.send_message = AsyncMock()
        
        # Call the command
        await general_cog.date(mock_interaction)
        
        # Verify the response
        mock_interaction.response.send_message.assert_called_once()
        args, kwargs = mock_interaction.response.send_message.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Date" in embed.title
        assert "Today's date" in embed.description
    
    @pytest.mark.asyncio
    async def test_toss_command(self, general_cog, mock_interaction):
        """Test the coin toss command."""
        # Set up the mock
        mock_interaction.response.send_message = AsyncMock()
        
        # Call the command
        await general_cog.toss(mock_interaction)
        
        # Verify the response
        mock_interaction.response.send_message.assert_called_once()
        args, kwargs = mock_interaction.response.send_message.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Coin Toss" in embed.title
        # Result should be either Heads or Tails
        assert "Heads" in embed.description or "Tails" in embed.description
    
    @pytest.mark.asyncio
    async def test_invite_command(self, general_cog, mock_interaction):
        """Test the invite command."""
        # Set up the mock
        mock_interaction.response.send_message = AsyncMock()
        mock_channel = mock_interaction.channel
        mock_invite = MagicMock()
        mock_invite.url = "https://discord.gg/invite123"
        mock_channel.create_invite.return_value = mock_invite
        
        # Call the command
        await general_cog.invite(mock_interaction)
        
        # Verify invite was created
        mock_channel.create_invite.assert_called_once()
        
        # Verify the response
        mock_interaction.response.send_message.assert_called_once()
        args, kwargs = mock_interaction.response.send_message.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Server Invite" in embed.title
        assert "https://discord.gg/invite123" in embed.description
    
    @pytest.mark.asyncio
    async def test_poll_command(self, general_cog, mock_interaction):
        """Test the poll command."""
        # Set up the mocks
        mock_interaction.response.send_message = AsyncMock()
        mock_message = MagicMock()
        mock_message.add_reaction = AsyncMock()
        mock_interaction.original_response.return_value = mock_message
        
        # Call the command with two options
        await general_cog.poll(
            mock_interaction, 
            question="Test poll?", 
            option1="Yes", 
            option2="No"
        )
        
        # Verify the response
        mock_interaction.response.send_message.assert_called_once()
        args, kwargs = mock_interaction.response.send_message.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Test poll?" in embed.title
        assert "Yes" in embed.description
        assert "No" in embed.description
        
        # Verify reactions were added
        assert mock_message.add_reaction.call_count == 2
        
    @pytest.mark.asyncio
    async def test_help_command(self, general_cog, mock_interaction):
        """Test the help command."""
        # Set up the mock
        mock_interaction.response.send_message = AsyncMock()
        
        # Mock bot commands
        command1 = MagicMock()
        command1.name = "test1"
        command1.description = "Test command 1"
        command2 = MagicMock()
        command2.name = "test2"
        command2.description = "Test command 2"
        general_cog.bot.tree.get_commands.return_value = [command1, command2]
        
        # Call the command
        await general_cog.help_command(mock_interaction)
        
        # Verify the response
        mock_interaction.response.send_message.assert_called_once()
        args, kwargs = mock_interaction.response.send_message.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Help" in embed.title
        # Both command names should be in fields
        fields_text = "".join([f.name for f in embed.fields])
        assert "test1" in fields_text
        assert "test2" in fields_text
