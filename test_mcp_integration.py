"""Test script for MCP integration with the plant agent."""

import asyncio
import logging

from app.agents.plant_agent import process_message
from config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_agent_with_mcp():
    """Test the plant agent with MCP integration."""
    print("🌱 Testing Plant Agent with MCP Tools...")
    print(f"   MCP Server URL: {settings.mcp_server_url}")

    test_messages = [
        "Hello, can you help me with my plant?",
        "My plant's leaves are turning yellow. What should I do?",
        "What tools do you have available to help me?",
        "Can you use any tools to diagnose my plant's problem?",
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"\n   Test {i}: {message}")
        try:
            response = await process_message(message)
            print(
                f"   Response: {response[:200]}{'...' if len(response) > 200 else ''}"
            )
            print("   ✅ Success")
        except Exception as e:
            print(f"   ❌ Error: {e}")


async def main():
    """Run MCP integration tests."""
    print("🚀 Starting MCP Integration Tests")
    print("=" * 50)

    await test_agent_with_mcp()

    print("\n" + "=" * 50)
    print("🏁 MCP Integration Tests Complete")


if __name__ == "__main__":
    asyncio.run(main())
