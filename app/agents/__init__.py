"""Agent initialization with handoffs."""

import logging
import os
from typing import Any, Dict, Optional

from agents import Agent, Handoff, HostedMCPTool, Runner
from agents.tool import Mcp

from config import settings

logger = logging.getLogger(__name__)

# Set OpenAI API key for openai-agents
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

# Plant Agent Configuration
PLANT_AGENT_NAME = "EmpowerPlantAgent"
PLANT_AGENT_DESCRIPTION = "a specialized AI assistant focused on plant care, gardening advice, and helping plants thrive"

PLANT_AGENT_INSTRUCTIONS = """You are EmpowerPlantAgent, a specialized AI assistant focused on plant care and empowerment. 

Your expertise includes:
- Plant identification and care requirements
- Troubleshooting plant health issues (yellowing leaves, pests, diseases)
- Optimal growing conditions (light, water, soil, humidity)
- Seasonal care recommendations
- Indoor and outdoor gardening advice
- Plant propagation techniques
- Sustainable gardening practices
- Companion planting suggestions

Always provide:
- Clear, actionable advice
- Safety considerations when relevant
- Multiple solutions when possible
- Encouragement for plant parents
- Scientific backing when appropriate

Be friendly, encouraging, and remember that every plant parent is on a learning journey. When users provide context about their specific plant, location, or growing conditions, use that information to give more targeted advice.

If someone asks about purchasing products, tools, or wants to buy something, transfer them to the ShoppingAgent who can help them find and purchase what they need.

You have access to MCP tools that can help you provide better assistance. Use them when appropriate to help users with their plant care needs."""

# Shopping Agent Configuration
SHOPPING_AGENT_NAME = "ShoppingAgent"
SHOPPING_AGENT_DESCRIPTION = (
    "a specialized AI assistant for product discovery and checkout processes"
)

SHOPPING_AGENT_INSTRUCTIONS = """You are ShoppingAgent, a specialized AI assistant focused on helping users find and purchase products.

Your expertise includes:
- Product discovery and search
- Product recommendations based on user needs
- Checkout process assistance
- Order management and tracking
- Price comparisons and deals
- Product specifications and details

Your available tools:
- get-products: Retrieve available products based on search criteria
- checkout: Process orders and handle payment flow

Always provide:
- Clear product information and specifications
- Helpful recommendations based on user preferences
- Step-by-step checkout guidance
- Order confirmation and tracking details
- Professional and friendly customer service

If someone asks about plant care, gardening advice, plant health issues, or how to care for plants, transfer them to the EmpowerPlantAgent who is the expert in plant care and gardening.

Be helpful, accurate, and guide users through the entire shopping experience from product discovery to successful checkout completion."""

# Create MCP configurations
plant_mcp_config = Mcp(
    type="mcp",
    server_label="plantEmpowermentMcpServer",
    server_description="MCP server providing plant care tools and resources",
    server_url=settings.mcp_server_url,
    headers={},
    allowed_tools={"allowed_tool_names": ["get-plant-care-guide"]},
)

shopping_mcp_config = Mcp(
    type="mcp",
    server_label="shoppingMcpServer",
    server_description="MCP server providing shopping and checkout tools",
    server_url=settings.mcp_server_url,
    headers={},
    allowed_tools={"allowed_tool_names": ["get-products", "checkout"]},
)

# Create MCP tools
plant_mcp_tool = HostedMCPTool(tool_config=plant_mcp_config)
shopping_mcp_tool = HostedMCPTool(tool_config=shopping_mcp_config)

# Create agents first without handoffs
plant_agent = Agent(
    name=PLANT_AGENT_NAME,
    instructions=PLANT_AGENT_INSTRUCTIONS,
    model=settings.openai_model_expansive,
    tools=[plant_mcp_tool],
)

shopping_agent = Agent(
    name=SHOPPING_AGENT_NAME,
    instructions=SHOPPING_AGENT_INSTRUCTIONS,
    model=settings.openai_model_cheap,
    tools=[shopping_mcp_tool],
)

# Set up handoffs after both agents are created
plant_agent.handoffs = [shopping_agent]  # Plant agent can handoff to shopping agent
shopping_agent.handoffs = [plant_agent]  # Shopping agent can handoff to plant agent


async def process_plant_message(
    message: str, context: Optional[Dict[str, Any]] = None
) -> str:
    """Process a message and return a response using the plant agent."""
    try:
        # Format message with context if provided
        formatted_message = _format_message_with_context(message, context)

        # Run the agent with the message
        result = await Runner.run(plant_agent, formatted_message)

        return result.final_output

    except Exception as e:
        logger.error(f"Plant agent processing failed: {e}")
        raise Exception(f"Plant agent processing failed: {str(e)}")


async def process_shopping_message(
    message: str, context: Optional[Dict[str, Any]] = None
) -> str:
    """Process a shopping message and return a response using the shopping agent."""
    try:
        # Format message with context if provided
        formatted_message = _format_message_with_context(message, context)

        # Run the agent with the message
        result = await Runner.run(shopping_agent, formatted_message)

        return result.final_output

    except Exception as e:
        logger.error(f"Shopping agent processing failed: {e}")
        raise Exception(f"Shopping agent processing failed: {str(e)}")


def _format_message_with_context(
    message: str, context: Optional[Dict[str, Any]] = None
) -> str:
    """Format message with context information.

    Args:
        message: Original message
        context: Optional context information

    Returns:
        Formatted message with context
    """
    if not context:
        return message

    context_str = _format_context(context)
    return f"Context: {context_str}\n\nUser message: {message}"


def _format_context(context: Dict[str, Any]) -> str:
    """Format context dictionary into a readable string.

    Args:
        context: Context information

    Returns:
        Formatted context string
    """
    context_parts = []
    for key, value in context.items():
        if value:
            context_parts.append(f"{key}: {value}")
    return ", ".join(context_parts)


# Export everything needed
__all__ = [
    "plant_agent",
    "shopping_agent",
    "process_plant_message",
    "process_shopping_message",
    "PLANT_AGENT_NAME",
    "PLANT_AGENT_DESCRIPTION",
    "SHOPPING_AGENT_NAME",
    "SHOPPING_AGENT_DESCRIPTION",
]
