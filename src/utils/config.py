"""Configuration management"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Application settings"""

    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    llm_provider: str = "openai"
    default_model: str = "gpt-4"
    evaluator_model: str = "gpt-4"
    exercise_generator_model: str = "gpt-4"

    # Agent Configuration
    default_temperature: float = 0.7
    max_tokens: int = 2000

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/tutor.log"

    # Application
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False


def load_config(env_file: str = ".env") -> Settings:
    """
    Load configuration from environment variables

    Args:
        env_file: Path to .env file

    Returns:
        Settings object
    """
    # Load .env file if it exists
    if os.path.exists(env_file):
        load_dotenv(env_file)

    return Settings()
