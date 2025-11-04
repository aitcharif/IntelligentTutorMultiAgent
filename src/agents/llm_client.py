"""LLM client wrapper for different providers"""

from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import os
from loguru import logger


class LLMClient(ABC):
    """Abstract base class for LLM clients"""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> str:
        """Generate text from LLM"""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._client = None

    def _ensure_client(self):
        """Lazy initialize OpenAI client"""
        if self._client is None:
            try:
                from openai import AsyncOpenAI

                self._client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                logger.error("OpenAI package not installed. Install with: pip install openai")
                raise

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> str:
        """Generate text using OpenAI API"""
        self._ensure_client()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating with OpenAI: {str(e)}")
            raise


class AnthropicClient(LLMClient):
    """Anthropic Claude API client"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self._client = None

    def _ensure_client(self):
        """Lazy initialize Anthropic client"""
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic

                self._client = AsyncAnthropic(api_key=self.api_key)
            except ImportError:
                logger.error(
                    "Anthropic package not installed. Install with: pip install anthropic"
                )
                raise

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> str:
        """Generate text using Anthropic API"""
        self._ensure_client()

        try:
            response = await self._client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}],
                **kwargs,
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error generating with Anthropic: {str(e)}")
            raise


def create_llm_client(provider: str = "openai", model: str = "gpt-4", **kwargs) -> LLMClient:
    """
    Factory function to create LLM client

    Args:
        provider: LLM provider ('openai' or 'anthropic')
        model: Model name
        **kwargs: Additional arguments

    Returns:
        LLM client instance
    """
    if provider.lower() == "openai":
        return OpenAIClient(model=model, **kwargs)
    elif provider.lower() == "anthropic":
        return AnthropicClient(model=model, **kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider}")
