"""
Configuration management for the Research Agent.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Central configuration class for managing API keys and settings.
    
    Attributes:
        openai_api_key (str): API key for OpenAI services
        serper_api_key (str): API key for Serper search API
        model_name (str): Name of the LLM model to use
        temperature (float): Creativity setting for LLM (0.0 to 1.0)
    """
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        self.openai_api_key = self._get_env_var('OPENAI_API_KEY')
        self.serper_api_key = self._get_env_var('SERPER_API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'gpt-4')
        self.temperature = float(os.getenv('TEMPERATURE', '0.1'))
    
    def _get_env_var(self, var_name: str) -> str:
        """
        Retrieve environment variable or raise informative error.
        
        Args:
            var_name (str): Name of the environment variable to retrieve
            
        Returns:
            str: Value of the environment variable
            
        Raises:
            ValueError: If the environment variable is not set
        """
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Missing required environment variable: {var_name}")
        return value

# Create global config instance
config = Config()
