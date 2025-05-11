"""
Utility module for sentiment analysis functionality
"""
import asyncio
from enum import Enum
from typing import Dict, Union

from textblob import TextBlob


class SentimentResult(Enum):
    """Enum representing sentiment analysis results."""
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


async def analyze_sentiment(text: str) -> Dict[str, Union[SentimentResult, float, float]]:
    """
    Analyze the sentiment of the given text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing sentiment analysis results:
            - result: The sentiment classification (NEGATIVE, NEUTRAL, POSITIVE)
            - polarity: The polarity score (-1.0 to 1.0)
            - subjectivity: The subjectivity score (0.0 to 1.0)
    """
    # TextBlob is CPU-intensive, so run it in a thread pool
    loop = asyncio.get_event_loop()
    analysis = await loop.run_in_executor(None, lambda: TextBlob(text))
    
    # Determine sentiment result
    if analysis.sentiment.polarity > 0.1:
        result = SentimentResult.POSITIVE
    elif analysis.sentiment.polarity < -0.1:
        result = SentimentResult.NEGATIVE
    else:
        result = SentimentResult.NEUTRAL
    
    return {
        "result": result,
        "polarity": analysis.sentiment.polarity,
        "subjectivity": analysis.sentiment.subjectivity
    }


def get_sentiment_emoji(sentiment_result: SentimentResult) -> str:
    """
    Get an appropriate emoji for a sentiment result.
    
    Args:
        sentiment_result: The sentiment classification
        
    Returns:
        An emoji string representing the sentiment
    """
    if sentiment_result == SentimentResult.POSITIVE:
        return "😊"
    elif sentiment_result == SentimentResult.NEGATIVE:
        return "😔"
    else:
        return "😐"
