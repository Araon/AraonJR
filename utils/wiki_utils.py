"""
Utility module for wiki-related functionality
"""
import asyncio
from typing import Tuple, Union

import wikipedia


async def get_wiki_summary(topic: str, sentences: int = 3) -> Tuple[bool, str]:
    """
    Asynchronously fetch a Wikipedia summary for the given topic.
    
    Args:
        topic: The topic to search for
        sentences: Number of sentences to return in the summary
        
    Returns:
        Tuple containing (success, content)
            - success: Boolean indicating if the query was successful
            - content: The summary if successful, otherwise an error message
    """
    # Run the blocking Wikipedia API call in a thread pool
    try:
        # First try to search for the topic to verify it exists
        loop = asyncio.get_event_loop()
        search_results = await loop.run_in_executor(
            None, lambda: wikipedia.search(topic, results=1)
        )
        
        # If no results, return early with an error
        if not search_results:
            return False, "No Wikipedia article found for that topic. Try a different search term."
            
        # Get the summary with specified number of sentences
        summary = await loop.run_in_executor(
            None, lambda: wikipedia.summary(topic, sentences=sentences)
        )
        
        # Get the page URL
        page = await loop.run_in_executor(
            None, lambda: wikipedia.page(search_results[0], auto_suggest=False)
        )
        
        return True, (summary, page.url)
    
    except wikipedia.DisambiguationError as e:
        # If there are multiple matches, suggest the options
        options = e.options[:5]  # Limit to first 5 options
        message = "Topic is ambiguous. Did you mean one of these?\n- " + "\n- ".join(options)
        if len(e.options) > 5:
            message += f"\n...and {len(e.options) - 5} more options"
        return False, message
        
    except wikipedia.PageError:
        return False, "That page doesn't exist on Wikipedia. Try a different search term."
        
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
