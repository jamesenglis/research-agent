#!/usr/bin/env python3
"""
Main entry point for the Research Agent.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent.research_agent import create_research_agent

def main():
    """
    Main function to demonstrate the Research Agent capabilities.
    """
    try:
        # Initialize the research agent
        print("🚀 Initializing Research Agent...")
        agent = create_research_agent()
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
        print("Please check your API keys and internet connection.")

if __name__ == "__main__":
    main()
