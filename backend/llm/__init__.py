"""LLM integration - supports cloud and local models"""

from .llm_factory import create_llm_client, LLMClient

__all__ = ["create_llm_client", "LLMClient"]
