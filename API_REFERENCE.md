# API Reference

## ResearchAgent Class

### `ResearchAgent()`
Main agent class for automated research.

**Methods:**

#### `research(topic: str) -> Dict[str, Any]`
Perform comprehensive research on a topic.

**Parameters:**
- `topic` (str): Research topic or question

**Returns:**
\`\`\`python
{
    'topic': str,           # Original research topic
    'report': str,          # Comprehensive research report
    'sources': List[str],   # List of source URLs
    'timestamp': str,       # ISO format timestamp
    'error': bool           # True if research failed (optional)
}
\`\`\`

**Example:**
\`\`\`python
from src.agent.research_agent import create_research_agent

agent = create_research_agent()
results = agent.research("quantum computing advances 2024")
print(results['report'])
\`\`\`

## Tools

### WebSearchTool
- `search(query: str, num_results: int = 5) -> Dict`
- `get_search_results(query: str) -> str`

### WebScraperTool
- `scrape_website(url: str) -> Optional[str]`

## Configuration

### Config Class
Manages environment variables and settings.

**Attributes:**
- `openai_api_key` (str)
- `serper_api_key` (str) 
- `model_name` (str)
- `temperature` (float)

## Helper Functions

### `create_research_agent() -> ResearchAgent`
Factory function to create a new ResearchAgent instance.

**Example:**
\`\`\`python
from src.agent.research_agent import create_research_agent

# Recommended way to create an agent
agent = create_research_agent()
results = agent.research("your research topic")
\`\`\`
