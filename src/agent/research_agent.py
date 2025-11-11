"""
Main Research Agent implementation using LangChain.
Uses absolute imports to avoid relative import issues.
"""

import os
import sys

# Add the necessary paths for imports
current_dir = os.path.dirname(__file__)
tools_dir = os.path.join(current_dir, '..', 'tools')
utils_dir = os.path.join(current_dir, '..', 'utils')

sys.path.insert(0, tools_dir)
sys.path.insert(0, utils_dir)

from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits import Tool
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any

try:
    from web_search import web_search_tool
    from web_scraper import web_scraper_tool
    from config import config
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback: try direct import
    import importlib.util
    def import_from_path(module_path, module_name):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    web_search_module = import_from_path(os.path.join(tools_dir, 'web_search.py'), 'web_search')
    web_scraper_module = import_from_path(os.path.join(tools_dir, 'web_scraper.py'), 'web_scraper')
    config_module = import_from_path(os.path.join(utils_dir, 'config.py'), 'config')
    
    web_search_tool = web_search_module.web_search_tool
    web_scraper_tool = web_scraper_module.web_scraper_tool
    config = config_module.config

class ResearchAgent:
    """
    An AI agent that performs automated research on given topics.
    """
    
    def __init__(self):
        """Initialize the Research Agent with tools and configuration."""
        self.llm = self._setup_llm()
        self.memory = self._setup_memory()
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()
    
    def _setup_llm(self) -> ChatOpenAI:
        """Configure and initialize the language model."""
        return ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            openai_api_key=config.openai_api_key
        )
    
    def _setup_memory(self) -> ConversationBufferMemory:
        """Initialize conversation memory for context retention."""
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    
    def _setup_tools(self) -> list:
        """Create and configure tools for the agent to use."""
        return [
            Tool(
                name="WebSearch",
                func=web_search_tool.get_search_results,
                description=(
                    "Useful for searching the web for recent information on any topic. "
                    "Input should be a clear search query. "
                    "Returns search results with titles, URLs, and snippets."
                )
            ),
            Tool(
                name="WebScraper", 
                func=web_scraper_tool.scrape_website,
                description=(
                    "Useful for reading the full content of a specific web page. "
                    "Input should be a valid URL. "
                    "Returns the main article content from the webpage."
                )
            )
        ]
    
    def _setup_agent(self):
        """Initialize the LangChain agent with tools and configuration."""
        system_message = SystemMessage(content=(
            "You are a professional research assistant. Your role is to:"
            "\n1. Use WebSearch to find relevant, recent information"
            "\n2. Use WebScraper to read important articles in detail" 
            "\n3. Synthesize information from multiple sources"
            "\n4. Provide comprehensive, well-structured reports"
            "\n5. Always cite your sources with URLs"
            "\n6. Be objective and factual in your analysis"
            "\n\nFormat your final answer with clear sections and citations."
        ))
        
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            memory=self.memory,
            verbose=True,
            agent_kwargs={
                'system_message': system_message,
            },
            handle_parsing_errors=True
        )
    
    def research(self, topic: str) -> Dict[str, Any]:
        """
        Perform comprehensive research on a given topic.
        """
        try:
            research_prompt = (
                f"Please research the following topic and provide a comprehensive report: {topic}\n"
                "Use web search to find recent information and read important articles. "
                "Provide a well-structured report with key findings and citations."
            )
            
            report = self.agent.run(research_prompt)
            
            return {
                'topic': topic,
                'report': report,
                'sources': self._extract_sources(report),
                'timestamp': self._get_current_timestamp()
            }
            
        except Exception as e:
            error_msg = f"Research failed: {str(e)}"
            return {
                'topic': topic,
                'report': error_msg,
                'sources': [],
                'timestamp': self._get_current_timestamp(),
                'error': True
            }
    
    def _extract_sources(self, report: str) -> list:
        """Extract source URLs from the research report."""
        import re
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, report)
        return list(set(urls))
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()

def create_research_agent() -> ResearchAgent:
    """Factory function to create a new ResearchAgent instance."""
    return ResearchAgent()
