"""
Main Research Agent implementation using LangChain.
Orchestrates web search and content analysis to produce research reports.
"""

from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits import Tool
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any, Optional

from ..tools.web_search import web_search_tool
from ..tools.web_scraper import web_scraper_tool
from ..utils.config import config

class ResearchAgent:
    """
    An AI agent that performs automated research on given topics.
    
    The agent can search the web, read articles, and compile comprehensive
    reports with citations. It uses a reasoning loop to decide when to
    search, when to read, and when to synthesize information.
    
    Attributes:
        llm (ChatOpenAI): The language model powering the agent
        memory (ConversationBufferMemory): Conversation memory
        tools (list): List of available tools
        agent: The LangChain agent instance
    """
    
    def __init__(self):
        """Initialize the Research Agent with tools and configuration."""
        self.llm = self._setup_llm()
        self.memory = self._setup_memory()
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()
    
    def _setup_llm(self) -> ChatOpenAI:
        """
        Configure and initialize the language model.
        
        Returns:
            ChatOpenAI: Configured ChatOpenAI instance
        """
        return ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            openai_api_key=config.openai_api_key
        )
    
    def _setup_memory(self) -> ConversationBufferMemory:
        """
        Initialize conversation memory for context retention.
        
        Returns:
            ConversationBufferMemory: Conversation memory instance
        """
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    
    def _setup_tools(self) -> list:
        """
        Create and configure tools for the agent to use.
        
        Returns:
            list: List of Tool objects available to the agent
        """
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
        """
        Initialize the LangChain agent with tools and configuration.
        
        Returns:
            AgentExecutor: Configured agent instance
        """
        # System prompt to guide agent behavior
        system_message = SystemMessage(content=(
            "You are a professional research assistant. Your role is to:"
            "\n1. Use WebSearch to find relevant, recent information"
            "\n2. Use WebScraper to read important articles in detail" 
            "\n3. Synthesize information from multiple sources"
            "\n4. Provide comprehensive, well-structured reports"
            "\n5. Always cite your sources with URLs"
            "\n6. Be objective and factual in your analysis"
            "\n7. Acknowledge limitations or conflicting information"
            "\n\nFormat your final answer with clear sections, bullet points, and citations."
        ))
        
        # Initialize the agent with tools and memory
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            memory=self.memory,
            verbose=True,  # Show reasoning process
            agent_kwargs={
                'system_message': system_message,
            },
            handle_parsing_errors=True
        )
    
    def research(self, topic: str) -> Dict[str, Any]:
        """
        Perform comprehensive research on a given topic.
        
        Args:
            topic (str): The research topic or question
            
        Returns:
            Dict[str, Any]: Research results containing:
                - topic: Original research topic
                - report: Comprehensive research report
                - sources: List of sources used
                - timestamp: When research was conducted
        """
        try:
            # Construct research prompt
            research_prompt = (
                f"Please research the following topic and provide a comprehensive report: {topic}\n"
                "Use web search to find recent information and read important articles. "
                "Provide a well-structured report with key findings and citations."
            )
            
            # Execute the research
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
        """
        Extract source URLs from the research report.
        
        Args:
            report (str): The research report text
            
        Returns:
            list: List of unique URLs found in the report
        """
        import re
        # Simple URL extraction - can be enhanced with more sophisticated parsing
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, report)
        return list(set(urls))  # Return unique URLs
    
    def _get_current_timestamp(self) -> str:
        """
        Get current timestamp in ISO format.
        
        Returns:
            str: Current timestamp string
        """
        from datetime import datetime
        return datetime.now().isoformat()

# Convenience function for easy usage
def create_research_agent() -> ResearchAgent:
    """
    Factory function to create a new ResearchAgent instance.
    
    Returns:
        ResearchAgent: New ResearchAgent instance
    """
    return ResearchAgent()
