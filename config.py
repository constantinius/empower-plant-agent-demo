"""Configuration management for the AI Agent application."""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")

    # FastAPI Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_reload: bool = os.getenv("API_RELOAD", "true").lower() == "true"

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")

    # Agent Configuration
    agent_name: str = os.getenv("AGENT_NAME", "EmpowerPlantAgent")
    agent_description: str = os.getenv(
        "AGENT_DESCRIPTION", "An AI agent for plant empowerment tasks"
    )
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1000"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

    # MCP Configuration
    mcp_server_url: str = os.getenv(
        "MCP_SERVER_URL",
        "https://p01--empower-mcp--wc4d2bfkjcxy.kr842zyvg5.code.run/mcp",
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
