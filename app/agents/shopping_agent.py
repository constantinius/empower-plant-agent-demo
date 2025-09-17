"""Shopping AI agent for product retrieval and checkout using MCP tools."""

import logging
import os
from typing import Any, Dict, Optional

from agents import Agent, HostedMCPTool, Runner
from agents.tool import Mcp

from config import settings

logger = logging.getLogger(__name__)

# Agent metadata
AGENT_NAME = "ShoppingAgent"
AGENT_DESCRIPTION = (
    "a specialized AI assistant for product discovery and checkout processes"
)

# Agent instructions
AGENT_INSTRUCTIONS = """You are ShoppingAgent, a specialized AI assistant focused on helping users find and purchase products.

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

Be helpful, accurate, and guide users through the entire shopping experience from product discovery to successful checkout completion."""

# Create MCP tool configuration for shopping
mcp_config = Mcp(
    type="mcp",
    server_label="shoppingMcpServer",
    server_description="MCP server providing shopping and checkout tools",
    server_url=settings.mcp_server_url,
    headers={},
    # Filter to only use shopping-related tools
    allowed_tools={"allowed_tool_names": ["get-products", "checkout"]},
)

# Create MCP tool
mcp_tool = HostedMCPTool(tool_config=mcp_config)

# Create the shopping agent with MCP tools
shopping_agent = Agent(
    name=AGENT_NAME,
    instructions=AGENT_INSTRUCTIONS,
    model=settings.openai_model_cheap,
    tools=[mcp_tool],
)


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
