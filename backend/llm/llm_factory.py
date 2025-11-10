"""Factory for creating LLM clients"""

from typing import Protocol
from ..core.config import get_settings


class LLMClient(Protocol):
    """Protocol for LLM clients"""

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        ...


class OllamaClient:
    """Local LLM using Ollama"""

    def __init__(self, host: str, model: str):
        self.host = host
        self.model = model

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.host}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"{system_prompt}\n\n{prompt}",
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens,
                        },
                    },
                ) as response:
                    result = await response.json()
                    return result.get("response", "")
        except Exception as e:
            return f"Error: {str(e)}"


class OpenAIClient:
    """Cloud LLM using OpenAI"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self._client = None

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        try:
            from openai import AsyncOpenAI

            if not self._client:
                self._client = AsyncOpenAI(api_key=self.api_key)

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = await self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


def create_llm_client() -> LLMClient:
    """Create LLM client based on configuration"""
    settings = get_settings()

    if settings.use_local_llm:
        return OllamaClient(
            host=settings.ollama_host,
            model=settings.ollama_model,
        )
    else:
        if settings.cloud_llm_provider == "openai":
            return OpenAIClient(
                api_key=settings.openai_api_key,
                model=settings.cloud_llm_model,
            )
        else:
            # Fallback to Ollama
            return OllamaClient(
                host=settings.ollama_host,
                model=settings.ollama_model,
            )
