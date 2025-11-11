#!/usr/bin/env python3
"""
Main entry point for the Research Agent.
Fixed import version.
"""

import os
import sys
import importlib.util

def import_module(module_path, module_name):
    """Import a module from a specific path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    """
    Main function to demonstrate the Research Agent capabilities.
    """
    try:
        # Import modules using absolute paths
        config_path = os.path.join(os.path.dirname(__file__), 'src', 'utils', 'config.py')
        web_search_path = os.path.join(os.path.dirname(__file__), 'src', 'tools', 'web_search.py')
        web_scraper_path = os.path.join(os.path.dirname(__file__), 'src', 'tools', 'web_scraper.py')
        research_agent_path = os.path.join(os.path.dirname(__file__), 'src', 'agent', 'research_agent.py')
        
        print("🚀 Initializing Research Agent...")
        
        # Import the modules
        config_module = import_module(config_path, 'config')
        web_search_module = import_module(web_search_path, 'web_search')
        web_scraper_module = import_module(web_scraper_path, 'web_scraper')
        research_agent_module = import_module(research_agent_path, 'research_agent')
        
        # Create the agent
        agent = research_agent_module.create_research_agent()
        print("✅ Research Agent ready!")
        
        # Get research topic from user
        print("\n" + "="*50)
        topic = input("Enter a research topic: ").strip()
        
        if not topic:
            print("❌ No topic provided. Exiting.")
            return
        
        # Execute research
        print(f"\n🔍 Researching: {topic}")
        print("This may take a moment...\n")
        
        results = agent.research(topic)
        
        # Display results
        print("="*50)
        print("📊 RESEARCH REPORT")
        print("="*50)
        print(results['report'])
        
        print("\n" + "="*50)
        print("🔗 SOURCES")
        print("="*50)
        for i, source in enumerate(results['sources'], 1):
            print(f"{i}. {source}")
            
        print(f"\n⏰ Research completed at: {results['timestamp']}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Research cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("This might be due to:")
        print("1. Missing API keys in .env file")
        print("2. Import issues - check the file structure")
        print("3. Network connectivity issues")

if __name__ == "__main__":
    main()
