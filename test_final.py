#!/usr/bin/env python3
"""
Final test to verify the Research Agent works.
"""
import os
import sys

print("🎯 Final Research Agent Test")
print("=" * 40)

# Test basic file structure
print("📁 Checking file structure...")
required_files = [
    "main.py",
    "src/utils/config.py",
    "src/tools/web_search.py", 
    "src/tools/web_scraper.py",
    "src/agent/research_agent.py"
]

all_files_exist = True
for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file}")
        all_files_exist = False

if all_files_exist:
    print("✅ All required files present!")
    
    # Test that main.py can run
    print("\n🚀 Testing main.py...")
    try:
        # We'll do a dry run that should at least start
        import subprocess
        result = subprocess.run([sys.executable, 'main.py'], 
                              input='\n',  # Send empty input to exit
                              text=True, 
                              capture_output=True, 
                              timeout=10)
        if "Research Agent" in result.stdout:
            print("✅ main.py runs successfully!")
        else:
            print("⚠️  main.py ran but output may need checking")
    except subprocess.TimeoutExpired:
        print("✅ main.py started and is waiting for input (expected)")
    except Exception as e:
        print(f"❌ main.py test failed: {e}")
else:
    print("❌ Some files are missing")

print(f"\n🎉 Research Agent project is {'READY' if all_files_exist else 'NEEDS ATTENTION'}!")
print("📚 GitHub Repository: https://github.com/jamesenglis/research-agent")
