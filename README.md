# Research Agent 🤖

An intelligent AI research assistant that can search the web, read articles, and compile comprehensive research reports automatically.

## Features

- 🔍 **Web Search**: Uses Serper API to find relevant, recent information
- 📄 **Content Extraction**: Scrapes and cleans web page content
- 🧠 **AI-Powered Analysis**: Uses OpenAI GPT-4 to synthesize information
- 📊 **Structured Reports**: Generates well-formatted reports with citations
- 💾 **Conversation Memory**: Remains context-aware during research sessions

## Quick Start

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/jamesenglis/research-agent.git
   cd research-agent
   \`\`\`

2. **Set up environment**
   \`\`\`bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   \`\`\`

3. **Configure API keys**
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your API keys
   \`\`\`

4. **Run the agent**
   \`\`\`bash
   python main.py
   \`\`\`

## API Keys Required

- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Serper API Key**: Get from [Serper.dev](https://serper.dev/api-key) (free tier available)

## Project Structure

\`\`\`
research_agent/
├── src/
│   ├── agent/           # Core agent logic
│   ├── tools/           # Web search and scraping tools
│   └── utils/           # Configuration and utilities
├── tests/               # Test suite
├── main.py              # Entry point
└── requirements.txt     # Dependencies
\`\`\`

## Usage Example

\`\`\`python
from src.agent.research_agent import create_research_agent

# Initialize the agent
agent = create_research_agent()

# Research a topic
results = agent.research("latest developments in quantum computing 2024")
print(results['report'])
\`\`\`

## Technologies Used

- **LangChain**: Agent framework and tool management
- **OpenAI GPT-4**: Language model for reasoning and synthesis
- **Serper API**: Google search functionality
- **BeautifulSoup4**: Web scraping and content extraction
- **Python-dotenv**: Environment management

## Contributing

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes (\`git commit -m 'Add amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
