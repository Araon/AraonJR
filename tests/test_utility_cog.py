"""
Tests for the Utility cog.
"""
import unittest.mock
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
import pytest_asyncio

from cogs.utility import Utility
from utils.sentiment_utils import SentimentResult


class TestUtilityCog:
    """Test the utility commands cog."""

    @pytest_asyncio.fixture
    async def utility_cog(self, mock_bot):
        """Create an instance of the Utility cog for testing."""
        cog = Utility(mock_bot)
        return cog

    @pytest.mark.asyncio
    @patch("cogs.utility.get_wiki_summary")
    async def test_wiki_command_success(self, mock_wiki_summary, utility_cog, mock_interaction):
        """Test the wiki command with successful result."""
        # Set up the mocks
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.followup.send = AsyncMock()
        
        # Mock the wiki summary function to return success
        mock_wiki_summary.return_value = (
            True, 
            ("Python is a programming language.", "https://en.wikipedia.org/wiki/Python_(programming_language)")
        )
        
        # Call the command
        await utility_cog.wiki(mock_interaction, "Python")
        
        # Verify the response was deferred
        mock_interaction.response.defer.assert_called_once()
        
        # Verify wiki summary was called with the right parameters
        mock_wiki_summary.assert_called_once_with("Python", sentences=3)
        
        # Verify the response
        mock_interaction.followup.send.assert_called_once()
        args, kwargs = mock_interaction.followup.send.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Wikipedia: Python" in embed.title
        assert "Python is a programming language." in embed.description
    
    @pytest.mark.asyncio
    @patch("cogs.utility.get_wiki_summary")
    async def test_wiki_command_failure(self, mock_wiki_summary, utility_cog, mock_interaction):
        """Test the wiki command with failure result."""
        # Set up the mocks
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.followup.send = AsyncMock()
        
        # Mock the wiki summary function to return an error
        mock_wiki_summary.return_value = (
            False, 
            "No Wikipedia article found for that topic."
        )
        
        # Call the command
        await utility_cog.wiki(mock_interaction, "NonexistentTopic")
        
        # Verify the response was deferred
        mock_interaction.response.defer.assert_called_once()
        
        # Verify wiki summary was called with the right parameters
        mock_wiki_summary.assert_called_once_with("NonexistentTopic", sentences=3)
        
        # Verify the response
        mock_interaction.followup.send.assert_called_once()
        args, kwargs = mock_interaction.followup.send.call_args
        
        # Verify embed was sent with error message
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Error" in embed.title
        assert "No Wikipedia article found" in embed.description
        assert embed.color == discord.Color.red()
    
    @pytest.mark.asyncio
    @patch("cogs.utility.analyze_sentiment")
    @patch("cogs.utility.get_sentiment_emoji")
    async def test_sentiment_command_positive(self, mock_get_emoji, mock_analyze_sentiment, utility_cog, mock_interaction):
        """Test the sentiment command with positive result."""
        # Set up the mocks
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.followup.send = AsyncMock()
        
        # Mock the sentiment analysis function
        mock_analyze_sentiment.return_value = {
            "result": SentimentResult.POSITIVE,
            "polarity": 0.8,
            "subjectivity": 0.6
        }
        mock_get_emoji.return_value = "😊"
        
        # Call the command
        await utility_cog.sentiment(mock_interaction, "This is amazing!")
        
        # Verify the response was deferred
        mock_interaction.response.defer.assert_called_once()
        
        # Verify sentiment analysis was called with the right text
        mock_analyze_sentiment.assert_called_once_with("This is amazing!")
        
        # Verify emoji getter was called with the right sentiment
        mock_get_emoji.assert_called_once_with(SentimentResult.POSITIVE)
        
        # Verify the response
        mock_interaction.followup.send.assert_called_once()
        args, kwargs = mock_interaction.followup.send.call_args
        
        # Verify embed was sent with right content
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "Sentiment Analysis" in embed.title
        assert "This is amazing!" in embed.description
        assert embed.color == discord.Color.green()
    
    @pytest.mark.asyncio
    async def test_avatar_command(self, utility_cog, mock_interaction):
        """Test the avatar command."""
        # Set up the mock
        mock_interaction.response.send_message = AsyncMock()
        
        # Setup avatar mock
        mock_user = MagicMock()
        mock_user.display_name = "TestUser"
        mock_user.display_avatar = MagicMock()
        mock_user.display_avatar.url = "https://example.com/avatar.png"
        mock_user.display_avatar.is_animated.return_value = False
        mock_user.display_avatar.with_format = MagicMock(return_value=mock_user.display_avatar)
        
        # Call the command
        await utility_cog.avatar(mock_interaction, mock_user)
        
        # Verify the response
        mock_interaction.response.send_message.assert_called_once()
        args, kwargs = mock_interaction.response.send_message.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "TestUser's Avatar" in embed.title
        assert embed.image.url == "https://example.com/avatar.png"
    
    @pytest.mark.asyncio
    async def test_userinfo_command(self, utility_cog, mock_interaction):
        """Test the userinfo command."""
        # Set up the mock
        mock_interaction.response.send_message = AsyncMock()
        
        # Setup mock member
        mock_member = MagicMock(spec=discord.Member)
        mock_member.display_name = "TestUser"
        mock_member.id = 12345
        mock_member.bot = False
        mock_member.created_at.strftime.return_value = "2020-01-01 00:00:00"
        mock_member.joined_at.strftime.return_value = "2021-01-01 00:00:00"
        mock_member.roles = []  # Empty roles list
        mock_member.color = discord.Color.blue()
        mock_member.display_avatar.url = "https://example.com/avatar.png"
        
        # Call the command
        await utility_cog.userinfo(mock_interaction, mock_member)
        
        # Verify the response
        mock_interaction.response.send_message.assert_called_once()
        args, kwargs = mock_interaction.response.send_message.call_args
        
        # Verify embed was sent
        assert "embed" in kwargs
        embed = kwargs["embed"]
        assert isinstance(embed, discord.Embed)
        assert "User Information: TestUser" in embed.title
        assert embed.thumbnail.url == "https://example.com/avatar.png"
