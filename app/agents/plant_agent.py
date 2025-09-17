"""Plant empowerment AI agent using openai-agents directly as a module variable."""

import logging
import os
from typing import Any, Dict, Optional

from agents import Agent, HostedMCPTool, Runner
from agents.tool import Mcp

from config import settings

logger = logging.getLogger(__name__)

# Set OpenAI API key for openai-agents
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

# Agent metadata
AGENT_NAME = "EmpowerPlantAgent"
AGENT_DESCRIPTION = "a specialized AI assistant focused on plant care, gardening advice, and helping plants thrive"

# Agent instructions
AGENT_INSTRUCTIONS = """You are EmpowerPlantAgent, a specialized AI assistant focused on plant care and empowerment. 

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

You have access to MCP tools that can help you provide better assistance. Use them when appropriate to help users with their plant care needs."""

# Create MCP tool configuration
mcp_config = Mcp(
    type="mcp",
    server_label="plantEmpowermentMcpServer",
    server_description="MCP server providing plant care tools and resources",
    server_url=settings.mcp_server_url,
    headers={},  # Add any required headers here
)

# Create MCP tool
mcp_tool = HostedMCPTool(tool_config=mcp_config)

# Create the plant agent with MCP tools
plant_agent = Agent(
    name=AGENT_NAME,
    instructions=AGENT_INSTRUCTIONS,
    model=settings.openai_model,
    tools=[mcp_tool],
)


async def process_message(
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
        logger.error(f"Agent processing failed: {e}")
        raise Exception(f"Agent processing failed: {str(e)}")


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
