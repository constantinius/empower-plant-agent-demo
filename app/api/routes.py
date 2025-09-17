"""API routes for the AI agent."""

from fastapi import APIRouter, HTTPException

from ..agents import (
    PLANT_AGENT_DESCRIPTION,
    PLANT_AGENT_NAME,
    SHOPPING_AGENT_DESCRIPTION,
    SHOPPING_AGENT_NAME,
    plant_agent,
    process_plant_message,
    process_shopping_message,
    shopping_agent,
)
from .models import ChatRequest, ChatResponse, HealthResponse

# Initialize router
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy", agent_name="Multi-Agent System", version="1.0.0"
    )


@router.post("/chat/plant", response_model=ChatResponse)
async def chat_with_plant_agent(request: ChatRequest):
    """Chat with the Plant Care AI agent.

    Args:
        request: Chat request containing message and optional context

    Returns:
        Plant agent's response

    Raises:
        HTTPException: If agent processing fails
    """
    try:
        response = await process_plant_message(
            message=request.message, context=request.context
        )

        return ChatResponse(response=response, agent_name=PLANT_AGENT_NAME)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Plant agent processing failed: {str(e)}"
        )


@router.post("/chat/shopping", response_model=ChatResponse)
async def chat_with_shopping_agent(request: ChatRequest):
    """Chat with the Shopping AI agent.

    Args:
        request: Chat request containing message and optional context

    Returns:
        Shopping agent's response

    Raises:
        HTTPException: If agent processing fails
    """
    try:
        response = await process_shopping_message(
            message=request.message, context=request.context
        )

        return ChatResponse(response=response, agent_name=SHOPPING_AGENT_NAME)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Shopping agent processing failed: {str(e)}"
        )


@router.get("/agents/info")
async def get_agents_info():
    """Get information about all available agents."""
    return {
        "agents": [
            {
                "name": PLANT_AGENT_NAME,
                "description": PLANT_AGENT_DESCRIPTION,
                "model": plant_agent.model,
                "endpoint": "/api/v1/chat/plant",
                "tools": ["get-plant-care-guide", "calculate_watering_schedule"],
                "handoffs": ["ShoppingAgent"],
            },
            {
                "name": SHOPPING_AGENT_NAME,
                "description": SHOPPING_AGENT_DESCRIPTION,
                "model": shopping_agent.model,
                "endpoint": "/api/v1/chat/shopping",
                "tools": ["get-products", "checkout"],
                "handoffs": ["EmpowerPlantAgent"],
            },
        ]
    }


@router.get("/agent/plant/info")
async def get_plant_agent_info():
    """Get information about the plant agent."""
    return {
        "name": PLANT_AGENT_NAME,
        "description": PLANT_AGENT_DESCRIPTION,
        "model": plant_agent.model,
        "tools": ["get-plant-care-guide", "calculate_watering_schedule"],
        "handoffs": ["ShoppingAgent"],
    }


@router.get("/agent/shopping/info")
async def get_shopping_agent_info():
    """Get information about the shopping agent."""
    return {
        "name": SHOPPING_AGENT_NAME,
        "description": SHOPPING_AGENT_DESCRIPTION,
        "model": shopping_agent.model,
        "tools": ["get-products", "checkout"],
        "handoffs": ["EmpowerPlantAgent"],
    }
