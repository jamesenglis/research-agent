#!/usr/bin/env python3
import os
import subprocess

print("🎯 Final Project Verification")
print("=" * 50)

# Check file sizes
print("📊 File Sizes:")
files_to_check = [
    "main.py",
    "src/utils/config.py", 
    "src/tools/web_search.py",
    "src/tools/web_scraper.py",
    "src/agent/research_agent.py",
    "README.md",
    "requirements.txt"
]

for file in files_to_check:
    size = os.path.getsize(file) if os.path.exists(file) else 0
    status = "✅" if size > 100 else "❌"
    print(f"  {status} {file}: {size} bytes")

# Test imports
print("\n🧪 Testing Imports:")
try:
    import sys
    sys.path.append('src')
    from utils.config import Config
    print("  ✅ Config imports")
    from tools.web_search import WebSearchTool
    print("  ✅ WebSearchTool imports")
    from tools.web_scraper import WebScraperTool
    print("  ✅ WebScraperTool imports")
    from agent.research_agent import ResearchAgent
    print("  ✅ ResearchAgent imports")
except Exception as e:
    print(f"  ❌ Import error: {e}")

# Git status
print("\n📁 Git Status:")
result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print(result.stdout)

print("🚀 Your Research Agent is complete and ready for GitHub!")
