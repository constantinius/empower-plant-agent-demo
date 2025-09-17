"""Agent initialization with handoffs."""

import logging
import os
from typing import Any, Dict, Optional

from agents import Agent, FunctionTool, Handoff, HostedMCPTool, Runner
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


# Local function tool for plant care
def calculate_watering_schedule(
    plant_type: str, pot_size: str, season: str, location: str = "indoor"
) -> str:
    """Calculate optimal watering schedule for a plant.

    Args:
        plant_type: Type of plant (e.g., 'succulent', 'tropical', 'herb', 'flowering', 'foliage', 'cactus')
        pot_size: Size of pot ('small', 'medium', 'large')
        season: Current season ('spring', 'summer', 'fall', 'winter')
        location: Plant location ('indoor', 'outdoor')

    Returns:
        Personalized watering schedule recommendation with frequency and tips
    """
    # Base watering frequencies (days between watering)
    base_schedule = {
        "succulent": 7,
        "tropical": 3,
        "herb": 2,
        "flowering": 2,
        "foliage": 4,
        "cactus": 10,
        "fern": 3,
        "orchid": 5,
        "snake plant": 7,
        "pothos": 4,
        "monstera": 4,
        "fiddle leaf fig": 5,
        "peace lily": 3,
        "rubber plant": 5,
    }

    # Pot size modifiers
    pot_modifiers = {
        "small": 0.7,  # More frequent watering (smaller volume)
        "medium": 1.0,
        "large": 1.3,  # Less frequent watering (larger volume)
        "extra large": 1.5,
    }

    # Season modifiers
    season_modifiers = {
        "spring": 1.0,  # Active growing season
        "summer": 0.8,  # More frequent in summer (heat/growth)
        "fall": 1.2,  # Slowing down
        "winter": 1.5,  # Dormant period, less water needed
    }

    # Location modifiers
    location_modifiers = {
        "indoor": 1.0,
        "outdoor": 0.8,  # More frequent due to wind/sun
        "greenhouse": 0.9,
        "balcony": 0.8,
    }

    # Get base frequency or default to 4 days
    plant_key = plant_type.lower().strip()
    base_days = base_schedule.get(plant_key, 4)

    # Apply modifiers
    pot_modifier = pot_modifiers.get(pot_size.lower().strip(), 1.0)
    season_modifier = season_modifiers.get(season.lower().strip(), 1.0)
    location_modifier = location_modifiers.get(location.lower().strip(), 1.0)

    # Calculate final frequency
    final_days = int(base_days * pot_modifier * season_modifier * location_modifier)
    final_days = max(1, min(final_days, 21))  # Between 1-21 days

    # Generate personalized advice
    frequency_text = f"every {final_days} day{'s' if final_days != 1 else ''}"

    # Add seasonal advice
    seasonal_tips = {
        "spring": "Growth season - watch for increased water needs as plant becomes more active.",
        "summer": "Hot weather increases water needs. Check soil more frequently and ensure good drainage.",
        "fall": "Growth slows down - reduce watering frequency and watch for overwatering.",
        "winter": "Dormant period - water sparingly and allow soil to dry between waterings.",
    }

    # Add plant-specific tips
    plant_tips = {
        "succulent": "Let soil dry completely between waterings. Water deeply but infrequently.",
        "tropical": "Maintain consistent moisture but avoid waterlogging. Loves humidity.",
        "cactus": "Water thoroughly then let soil dry completely. Less is more!",
        "fern": "Likes consistently moist (not wet) soil. High humidity helps.",
        "orchid": "Water with ice cubes or small amounts. Good drainage is essential.",
    }

    response = f"""🌱 **Watering Schedule for your {plant_type.title()}**

**Frequency**: Water {frequency_text} during {season}
**Pot Size Factor**: {pot_size.title()} pot - {'more frequent' if pot_modifier < 1 else 'standard' if pot_modifier == 1 else 'less frequent'} watering
**Location**: {location.title()} conditions considered

**{season.title()} Tip**: {seasonal_tips.get(season.lower(), 'Monitor soil moisture regularly.')}

**Plant-Specific Advice**: {plant_tips.get(plant_key, 'Check soil moisture by inserting finger 1-2 inches deep. Water when top inch is dry.')}

**General Tips**:
• Always check soil moisture before watering
• Ensure proper drainage to prevent root rot  
• Water in the morning when possible
• Adjust frequency based on humidity and temperature changes"""

    return response


# Create the watering calculator function tool
async def invoke_watering_calculator(context, input_json: str) -> str:
    """Invoke the watering calculator tool."""
    import json

    try:
        params = json.loads(input_json)
        return calculate_watering_schedule(
            plant_type=params.get("plant_type", ""),
            pot_size=params.get("pot_size", "medium"),
            season=params.get("season", "spring"),
            location=params.get("location", "indoor"),
        )
    except Exception as e:
        return f"Error calculating watering schedule: {str(e)}"


# Define the JSON schema for the watering calculator
watering_calculator_schema = {
    "type": "object",
    "properties": {
        "plant_type": {
            "type": "string",
            "description": "Type of plant (e.g., succulent, tropical, herb, flowering, cactus)",
        },
        "pot_size": {
            "type": "string",
            "enum": ["small", "medium", "large", "extra large"],
            "description": "Size of the pot",
        },
        "season": {
            "type": "string",
            "enum": ["spring", "summer", "fall", "winter"],
            "description": "Current season",
        },
        "location": {
            "type": "string",
            "enum": ["indoor", "outdoor", "greenhouse", "balcony"],
            "description": "Where the plant is located",
            "default": "indoor",
        },
    },
    "required": ["plant_type", "pot_size", "season"],
}

# Create the function tool
watering_tool = FunctionTool(
    name="calculate_watering_schedule",
    description="Calculate optimal watering frequency and provide personalized care advice based on plant type, pot size, season, and location",
    params_json_schema=watering_calculator_schema,
    on_invoke_tool=invoke_watering_calculator,
)

# Create agents first without handoffs
plant_agent = Agent(
    name=PLANT_AGENT_NAME,
    instructions=PLANT_AGENT_INSTRUCTIONS,
    model=settings.openai_model_expansive,
    tools=[plant_mcp_tool, watering_tool],
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
