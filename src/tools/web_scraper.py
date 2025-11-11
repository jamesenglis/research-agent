"""
Web scraping functionality for extracting content from web pages.
Uses requests and BeautifulSoup for robust content extraction.
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Optional
from urllib.parse import urlparse

class WebScraperTool:
    """
    A tool for scraping and cleaning content from web pages.
    
    This tool extracts main article content while removing navigation,
    ads, and other non-essential elements.
    """
    
    def __init__(self):
        """Initialize the WebScraperTool with default settings."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Research-Agent/1.0 (+https://github.com/jamesenglis/research-agent)'
        })
    
    def scrape_website(self, url: str) -> Optional[str]:
        """
        Scrape and clean main content from a web page.
        
        Args:
            url (str): The URL of the web page to scrape
            
        Returns:
            Optional[str]: Cleaned text content of the page, or None if scraping fails
        """
        try:
            # Validate URL format
            if not self._is_valid_url(url):
                return f"Invalid URL: {url}"
            
            # Fetch web page content
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            self._remove_unwanted_elements(soup)
            
            # Extract main content
            content = self._extract_main_content(soup)
            
            if not content:
                return "No main content found on the page."
            
            # Clean and format the text
            cleaned_content = self._clean_text(content)
            
            return cleaned_content[:8000]  # Limit content length
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching URL {url}: {str(e)}"
        except Exception as e:
            return f"Error processing URL {url}: {str(e)}"
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate URL format and scheme.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False
    
    def _remove_unwanted_elements(self, soup: BeautifulSoup) -> None:
        """
        Remove non-content elements from BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): Parsed HTML document
        """
        # Elements to remove (scripts, styles, nav, ads, etc.)
        elements_to_remove = soup.find_all([
            'script', 'style', 'nav', 'header', 'footer', 
            'aside', 'iframe', 'noscript'
        ])
        
        for element in elements_to_remove:
            element.decompose()
    
    def _extract_main_content(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract main content using common semantic HTML tags.
        
        Args:
            soup (BeautifulSoup): Parsed HTML document
            
        Returns:
            Optional[str]: Main content as text
        """
        # Priority order for content extraction
        selectors = [
            'article',
            'main',
            '[role="main"]',
            '.content', '.main-content', '.article-content',
            '#content', '#main-content', '#article-content'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text()
        
        # Fallback: use body if no specific content containers found
        return soup.find('body').get_text() if soup.find('body') else None
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            str: Cleaned and normalized text
        """
        # Remove extra whitespace and normalize
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple newlines to double
        text = re.sub(r'[ \t]+', ' ', text)      # Multiple spaces to single
        text = text.strip()
        
        return text

# Create a singleton instance for tool usage
web_scraper_tool = WebScraperTool()
