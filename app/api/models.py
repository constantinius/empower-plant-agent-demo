"""Pydantic models for API requests and responses."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    
    message: str = Field(..., description="User message to the agent", min_length=1)
    context: Optional[Dict[str, Any]] = Field(None, description="Optional context information")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "My plant's leaves are turning yellow. What should I do?",
                "context": {
                    "plant_type": "pothos",
                    "location": "indoor",
                    "light_conditions": "medium"
                }
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    
    response: str = Field(..., description="Agent's response")
    agent_name: str = Field(..., description="Name of the responding agent")
    
    class Config:
        schema_extra = {
            "example": {
                "response": "Yellow leaves on a pothos can indicate overwatering...",
                "agent_name": "EmpowerPlantAgent"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Service status")
    agent_name: str = Field(..., description="Agent name")
    version: str = Field(..., description="API version")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "agent_name": "EmpowerPlantAgent",
                "version": "1.0.0"
            }
        }
