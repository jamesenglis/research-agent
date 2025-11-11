"""
Web search functionality using Serper API.
Provides Google search capabilities for the research agent.
"""

import requests
import json
from typing import Dict, List, Optional
from ..utils.config import config

class WebSearchTool:
    """
    A tool for performing web searches using the Serper API.
    
    This tool allows the AI agent to search the web for current information
    and retrieve relevant URLs and snippets.
    """
    
    def __init__(self):
        """Initialize the WebSearchTool with API configuration."""
        self.api_key = config.serper_api_key
        self.base_url = "https://google.serper.dev/search"
        self.headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def search(self, query: str, num_results: int = 5) -> Dict[str, List[Dict]]:
        """
        Perform a web search and return structured results.
        
        Args:
            query (str): The search query string
            num_results (int): Number of results to return (default: 5)
            
        Returns:
            Dict: Structured search results containing organic results, 
                  answer box, and related questions
        """
        try:
            # Prepare search payload
            payload = json.dumps({
                "q": query,
                "num": num_results
            })
            
            # Execute API request
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                data=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Search API error: {e}")
            return {'organic': [], 'answerBox': {}, 'relatedSearches': []}
    
    def get_search_results(self, query: str) -> str:
        """
        Get formatted search results as a string for the AI agent.
        
        Args:
            query (str): The search query string
            
        Returns:
            str: Formatted string containing search results
        """
        results = self.search(query)
        formatted_results = []
        
        # Process organic results
        if 'organic' in results and results['organic']:
            for i, result in enumerate(results['organic'][:5], 1):
                title = result.get('title', 'No title')
                link = result.get('link', 'No URL')
                snippet = result.get('snippet', 'No description')
                
                formatted_results.append(
                    f"Result {i}:\nTitle: {title}\nURL: {link}\nSnippet: {snippet}\n"
                )
        
        # Include answer box if available
        if 'answerBox' in results and results['answerBox']:
            answer = results['answerBox']
            formatted_results.append(
                f"Quick Answer:\n{answer.get('snippet', 'No answer available')}"
            )
        
        return "\n".join(formatted_results) if formatted_results else "No results found."

# Create a singleton instance
web_search_tool = WebSearchTool()
