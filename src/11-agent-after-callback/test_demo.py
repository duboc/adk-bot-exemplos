"""
Test script for the Restaurant Reviewer Agent with After Agent Callback

This script demonstrates how to run the after agent callback example and see the different behaviors
based on session state and auditor intervention.
"""

import asyncio
import os
from agent import main

async def run_demo():
    """
    Run the Restaurant Reviewer callback demonstration
    """
    print("🍽️✨ Starting Restaurant Reviewer Agent with After Agent Callback Demo ✨🍽️")
    print("\nThis demo shows two scenarios:")
    print("1. Normal review session - Auditor approves original review")
    print("2. Poor review session - Auditor improves review quality")
    print("\nNote: Make sure your GOOGLE_API_KEY environment variable is set!")
    
    # Check if API key is set
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\n⚠️  WARNING: GOOGLE_API_KEY environment variable not found!")
        print("Please set your API key before running this demo.")
        print("Example: export GOOGLE_API_KEY='your-api-key-here'")
        return
    
    try:
        await main()
        print("\n🎉 Demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print("Make sure you have the google-adk package installed and your API key is valid.")

if __name__ == "__main__":
    asyncio.run(run_demo())
