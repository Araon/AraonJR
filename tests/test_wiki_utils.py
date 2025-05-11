"""
Tests for the wiki_utils module.
"""
import unittest.mock
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import wikipedia

from utils.wiki_utils import get_wiki_summary


class TestWikiUtils:
    """Test the wiki utilities."""

    @pytest.mark.asyncio
    async def test_get_wiki_summary_success(self):
        """Test successful wiki summary retrieval."""
        # Mock the Wikipedia API calls
        with patch('wikipedia.search') as mock_search, \
             patch('wikipedia.summary') as mock_summary, \
             patch('wikipedia.page') as mock_page:
             
            # Setup mocks
            mock_search.return_value = ["Python (programming language)"]
            mock_summary.return_value = "Python is a programming language."
            mock_page_instance = MagicMock()
            mock_page_instance.url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
            mock_page.return_value = mock_page_instance
            
            # Call the function
            success, result = await get_wiki_summary("Python programming")
            
            # Verify the result
            assert success is True
            summary, url = result
            assert summary == "Python is a programming language."
            assert url == "https://en.wikipedia.org/wiki/Python_(programming_language)"
            
            # Verify the function called Wikipedia API correctly
            mock_search.assert_called_once()
            mock_summary.assert_called_once()
            mock_page.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_wiki_summary_no_results(self):
        """Test wiki summary with no search results."""
        # Mock the Wikipedia API calls
        with patch('wikipedia.search') as mock_search:
            # Setup mock to return empty results
            mock_search.return_value = []
            
            # Call the function
            success, message = await get_wiki_summary("nonexistentpage12345")
            
            # Verify the result
            assert success is False
            assert "No Wikipedia article found" in message
            
            # Verify the function called Wikipedia API correctly
            mock_search.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_wiki_summary_disambiguation(self):
        """Test wiki summary with disambiguation error."""
        # Mock the Wikipedia API calls
        with patch('wikipedia.search') as mock_search, \
             patch('wikipedia.summary') as mock_summary:
             
            # Setup mocks
            mock_search.return_value = ["Python"]
            mock_summary.side_effect = wikipedia.DisambiguationError(
                "Python", ["Python (programming language)", "Python (snake)", "Monty Python"]
            )
            
            # Call the function
            success, message = await get_wiki_summary("Python")
            
            # Verify the result
            assert success is False
            assert "Topic is ambiguous" in message
            assert "Python (programming language)" in message
            assert "Python (snake)" in message
            assert "Monty Python" in message
            
            # Verify the function called Wikipedia API correctly
            mock_search.assert_called_once()
            mock_summary.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_wiki_summary_page_error(self):
        """Test wiki summary with page error."""
        # Mock the Wikipedia API calls
        with patch('wikipedia.search') as mock_search, \
             patch('wikipedia.summary') as mock_summary:
             
            # Setup mocks
            mock_search.return_value = ["SomePage"]
            mock_summary.side_effect = wikipedia.PageError("SomePage")
            
            # Call the function
            success, message = await get_wiki_summary("SomePage")
            
            # Verify the result
            assert success is False
            assert "page doesn't exist" in message
            
            # Verify the function called Wikipedia API correctly
            mock_search.assert_called_once()
            mock_summary.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_wiki_summary_general_exception(self):
        """Test wiki summary with general exception."""
        # Mock the Wikipedia API calls
        with patch('wikipedia.search') as mock_search:
            # Setup mock to raise an exception
            mock_search.side_effect = Exception("Some error")
            
            # Call the function
            success, message = await get_wiki_summary("Python")
            
            # Verify the result
            assert success is False
            assert "An error occurred" in message
            assert "Some error" in message
            
            # Verify the function called Wikipedia API correctly
            mock_search.assert_called_once()
