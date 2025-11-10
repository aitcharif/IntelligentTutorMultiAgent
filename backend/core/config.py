"""Configuration management"""

import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # LLM Configuration
    use_local_llm: bool = True
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "mistral"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    cloud_llm_provider: str = "openai"
    cloud_llm_model: str = "gpt-4"

    # RAG Configuration
    chroma_db_path: str = "./data/chroma_db"
    chroma_collection: str = "moroccan_cs_knowledge"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    rag_top_k: int = 5
    rag_score_threshold: float = 0.7

    # Audio Configuration
    stt_service: str = "whisper"
    whisper_model: str = "base"
    tts_service: str = "gtts"
    tts_language: str = "fr"
    audio_sample_rate: int = 16000
    audio_chunk_duration: int = 5

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    api_workers: int = 4
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    cors_allow_credentials: bool = True

    # Language Settings
    default_language: str = "fr"
    supported_languages: List[str] = ["fr", "ar", "en"]

    # Session Configuration
    session_timeout: int = 3600
    max_history_messages: int = 50

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    # Database
    database_url: str = "sqlite:///./data/app.db"

    # Agent Configuration
    coordinator_temperature: float = 0.7
    coordinator_max_tokens: int = 2000
    tutor_temperature: float = 0.8
    tutor_max_tokens: int = 3000
    evaluator_temperature: float = 0.3
    evaluator_max_tokens: int = 2000
    generator_temperature: float = 0.9
    generator_max_tokens: int = 4000

    # Moroccan Context
    curriculum_level: str = "all"
    education_system: str = "moroccan"

    # Development
    debug: bool = True
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
