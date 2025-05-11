"""
Tests for the sentiment_utils module.
"""
import unittest.mock
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from textblob import TextBlob

from utils.sentiment_utils import SentimentResult, analyze_sentiment, get_sentiment_emoji


class TestSentimentUtils:
    """Test the sentiment analysis utilities."""

    @pytest.mark.asyncio
    async def test_analyze_sentiment_positive(self):
        """Test analyzing positive sentiment."""
        # Mock TextBlob to return positive sentiment
        with patch('textblob.TextBlob') as mock_textblob:
            # Setup mock
            mock_blob = MagicMock()
            mock_blob.sentiment.polarity = 0.8
            mock_blob.sentiment.subjectivity = 0.6
            mock_textblob.return_value = mock_blob
            
            # Call the function
            result = await analyze_sentiment("This is great!")
            
            # Verify the result
            assert result["result"] == SentimentResult.POSITIVE
            assert result["polarity"] == 0.8
            assert result["subjectivity"] == 0.6
            
            # Verify TextBlob was called correctly
            mock_textblob.assert_called_once_with("This is great!")
    
    @pytest.mark.asyncio
    async def test_analyze_sentiment_negative(self):
        """Test analyzing negative sentiment."""
        # Mock TextBlob to return negative sentiment
        with patch('textblob.TextBlob') as mock_textblob:
            # Setup mock
            mock_blob = MagicMock()
            mock_blob.sentiment.polarity = -0.7
            mock_blob.sentiment.subjectivity = 0.8
            mock_textblob.return_value = mock_blob
            
            # Call the function
            result = await analyze_sentiment("This is terrible!")
            
            # Verify the result
            assert result["result"] == SentimentResult.NEGATIVE
            assert result["polarity"] == -0.7
            assert result["subjectivity"] == 0.8
            
            # Verify TextBlob was called correctly
            mock_textblob.assert_called_once_with("This is terrible!")
    
    @pytest.mark.asyncio
    async def test_analyze_sentiment_neutral(self):
        """Test analyzing neutral sentiment."""
        # Mock TextBlob to return neutral sentiment
        with patch('textblob.TextBlob') as mock_textblob:
            # Setup mock
            mock_blob = MagicMock()
            mock_blob.sentiment.polarity = 0.0
            mock_blob.sentiment.subjectivity = 0.2
            mock_textblob.return_value = mock_blob
            
            # Call the function
            result = await analyze_sentiment("This is a fact.")
            
            # Verify the result
            assert result["result"] == SentimentResult.NEUTRAL
            assert result["polarity"] == 0.0
            assert result["subjectivity"] == 0.2
            
            # Verify TextBlob was called correctly
            mock_textblob.assert_called_once_with("This is a fact.")
    
    def test_get_sentiment_emoji(self):
        """Test getting sentiment emoji."""
        # Test positive sentiment
        assert get_sentiment_emoji(SentimentResult.POSITIVE) == "😊"
        
        # Test negative sentiment
        assert get_sentiment_emoji(SentimentResult.NEGATIVE) == "😔"
        
        # Test neutral sentiment
        assert get_sentiment_emoji(SentimentResult.NEUTRAL) == "😐"
