#!/usr/bin/env python3
"""
Manual trigger for the WhatPeopleWant graph.
This script allows you to manually trigger the ScrapeYC graph execution.
"""

import asyncio
import sys
from exospherehost import StateManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def trigger_graph():
    """Manually trigger the ScrapeYC graph execution."""
    try:
        print("🚀 Triggering WhatPeopleWant graph execution...")
        
        # Initialize the state manager
        state_manager = StateManager(namespace="WhatPeopleWant")
        
        # Trigger the graph execution
        result = await state_manager.trigger(
            graph_name="ScrapeYC",
            inputs={},
            store={},
            start_delay=0
           
        )
        
        print(f"✅ Graph triggered successfully!")
        print(f"📊 Execution ID: {result.get('id', 'N/A')}")
        print(f"🔗 Check the Exosphere dashboard for execution details")
        
        return result
        
    except Exception as e:
        print(f"❌ Error triggering graph: {str(e)}")
        print(f"🔍 Make sure the graph is registered and the state manager is running")
        return None

async def check_graph_status():
    """Check the status of the ScrapeYC graph."""
    try:
        print("🔍 Checking graph status...")
        
        state_manager = StateManager(namespace="WhatPeopleWant")
        
        # Get graph information
        graph_info = await state_manager.get_graph("ScrapeYC")
        
        if graph_info:
            print(f"✅ Graph 'ScrapeYC' found")
            print(f"📋 Graph ID: {graph_info.get('id', 'N/A')}")
            print(f"🔄 Status: {graph_info.get('status', 'N/A')}")
            print(f"⏰ Last run: {graph_info.get('last_run', 'N/A')}")
        else:
            print("❌ Graph 'ScrapeYC' not found")
            print("💡 Make sure to run register.py first to register the graph")
            
    except Exception as e:
        print(f"❌ Error checking graph status: {str(e)}")

async def list_recent_executions():
    """List recent graph executions."""
    try:
        print("📋 Fetching recent executions...")
        
        state_manager = StateManager(namespace="WhatPeopleWant")
        
        # Get recent executions (this might need to be adjusted based on the actual API)
        executions = await state_manager.get_executions("ScrapeYC", limit=5)
        
        if executions:
            print(f"📊 Recent executions:")
            for i, execution in enumerate(executions, 1):
                print(f"  {i}. ID: {execution.get('id', 'N/A')}")
                print(f"     Status: {execution.get('status', 'N/A')}")
                print(f"     Started: {execution.get('started_at', 'N/A')}")
                print(f"     Duration: {execution.get('duration', 'N/A')}")
                print()
        else:
            print("📭 No recent executions found")
            
    except Exception as e:
        print(f"❌ Error fetching executions: {str(e)}")

def print_usage():
    """Print usage information."""
    print("""
🎯 WhatPeopleWant Graph Trigger

Usage:
    python trigger.py [command]

Commands:
    trigger    - Manually trigger the ScrapeYC graph execution (default)
    status     - Check the status of the ScrapeYC graph
    executions - List recent graph executions
    help       - Show this help message

Examples:
    python trigger.py              # Trigger the graph
    python trigger.py trigger      # Trigger the graph
    python trigger.py status       # Check graph status
    python trigger.py executions   # List recent executions
    python trigger.py help         # Show help

Environment:
    Make sure you have a .env file with the required environment variables:
    - EXOSPHERE_STATE_MANAGER_URI
    - EXOSPHERE_API_KEY
    - And other required variables (see README.md)
""")

async def main():
    """Main function to handle command line arguments."""
    command = sys.argv[1] if len(sys.argv) > 1 else "trigger"
    
    if command == "help":
        print_usage()
        return
    
    print("🎯 WhatPeopleWant Graph Trigger")
    print("=" * 40)
    
    if command == "trigger":
        await trigger_graph()
    elif command == "status":
        await check_graph_status()
    elif command == "executions":
        await list_recent_executions()
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)
