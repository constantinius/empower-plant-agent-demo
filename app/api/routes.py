"""API routes for the AI agent."""

from fastapi import APIRouter, HTTPException

from ..agents.plant_agent import (
    AGENT_DESCRIPTION,
    AGENT_NAME,
    plant_agent,
    process_message,
)
from .models import ChatRequest, ChatResponse, HealthResponse

# Initialize router
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", agent_name=AGENT_NAME, version="1.0.0")


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the AI agent.

    Args:
        request: Chat request containing message and optional context

    Returns:
        Agent's response

    Raises:
        HTTPException: If agent processing fails
    """
    try:
        response = await process_message(
            message=request.message, context=request.context
        )

        return ChatResponse(response=response, agent_name=AGENT_NAME)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Agent processing failed: {str(e)}"
        )


@router.get("/agent/info")
async def get_agent_info():
    """Get information about the agent."""
    return {
        "name": AGENT_NAME,
        "description": AGENT_DESCRIPTION,
        "model": plant_agent.model,
    }
