"""Configuration management for the AI Agent application."""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # API settings
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_reload: bool = os.getenv("API_RELOAD", "true").lower() == "true"

    # API tester settings
    api_tester_enabled: bool = True
    api_tester_base_interval_ms: int = (
        20 * 60 * 1000
    )  # 20 minutes base interval, every ~10 mins in peak times
    api_tester_jitter_percent: int = 10

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    agent_model: str = "gpt-5-mini"
    light_model: str = "gpt-5-nano"

    # MCP settings
    mcp_server_url: str = (
        "https://p01--empower-mcp--wc4d2bfkjcxy.kr842zyvg5.code.run/mcp"
    )

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")

    # Agent Configuration
    agent_name: str = os.getenv("AGENT_NAME", "EmpowerPlantAgent")
    agent_description: str = os.getenv(
        "AGENT_DESCRIPTION", "An AI agent for plant empowerment tasks"
    )
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1000"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Sentry Configuration
    sentry_dsn: str = os.getenv("SENTRY_DSN", "")
    sentry_environment: str = os.getenv("SENTRY_ENVIRONMENT", "development")
    sentry_traces_sample_rate: float = float(
        os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")
    )
    sentry_profiles_sample_rate: float = float(
        os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "1.0")
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


# Instantiate settings
settings = Settings()
