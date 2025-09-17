"""Example usage of the Plant Agent API with openai-agents."""

import asyncio
import json

import httpx


async def test_plant_agent():
    """Test the plant agent API endpoints."""

    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:

        # Test health endpoint
        print("🔍 Testing health endpoint...")
        health_response = await client.get(f"{base_url}/api/v1/health")
        print(f"Health: {health_response.json()}")
        print()

        # Test agent info endpoint
        print("🤖 Getting agent info...")
        info_response = await client.get(f"{base_url}/api/v1/agent/info")
        print(f"Agent Info: {info_response.json()}")
        print()

        # Test chat endpoint with various plant questions
        test_cases = [
            {
                "message": "My plant's leaves are turning yellow. What should I do?",
                "context": {
                    "plant_type": "pothos",
                    "location": "indoor",
                    "light_conditions": "medium",
                },
            },
            {
                "message": "How often should I water my snake plant?",
                "context": {
                    "plant_type": "snake plant",
                    "pot_size": "medium",
                    "location": "living room",
                },
            },
            {
                "message": "What's the best fertilizer for tomatoes?",
                "context": {
                    "plant_type": "tomato",
                    "location": "outdoor garden",
                    "season": "summer",
                },
            },
            {
                "message": "Help me identify this plant with small white flowers and heart-shaped leaves."
            },
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(f"🌱 Test Case {i}: {test_case['message'][:50]}...")

            try:
                chat_response = await client.post(
                    f"{base_url}/api/v1/chat", json=test_case
                )

                if chat_response.status_code == 200:
                    response_data = chat_response.json()
                    print(f"✅ Response from {response_data['agent_name']}:")
                    print(f"   {response_data['response'][:200]}...")
                else:
                    print(
                        f"❌ Error: {chat_response.status_code} - {chat_response.text}"
                    )

            except Exception as e:
                print(f"❌ Exception: {e}")

            print()


if __name__ == "__main__":
    print("🚀 Starting Plant Agent API Tests")
    print("Make sure the API server is running on http://localhost:8000")
    print("Using openai-agents directly with module-level agent")
    print("=" * 60)

    asyncio.run(test_plant_agent())
