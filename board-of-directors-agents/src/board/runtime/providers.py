"""AI provider implementations for Ollama and OpenAI."""

import os
from typing import Optional, Protocol

import ollama
import openai
from openai import OpenAI


class AIProvider(Protocol):
    """Protocol for AI providers."""
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text from prompt."""
        ...


class OllamaProvider:
    """Ollama local model provider."""
    
    def __init__(self, model: str = "llama2", base_url: Optional[str] = None):
        self.model = model
        self.base_url = base_url or "http://localhost:11434"
        
        # Test connection
        try:
            ollama.list()
        except Exception as e:
            raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}: {e}")
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text using Ollama."""
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': max_tokens,
                    'temperature': 0.7,
                }
            )
            return response['response']
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {e}")


class OpenAIProvider:
    """OpenAI API provider."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise RuntimeError(f"OpenAI generation failed: {e}")


def get_provider() -> AIProvider:
    """Get the appropriate AI provider based on environment."""
    
    # Check for OpenAI API key first
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        model = os.getenv("BOARD_MODEL", "gpt-3.5-turbo")
        return OpenAIProvider(openai_key, model)
    
    # Fall back to Ollama
    model = os.getenv("BOARD_MODEL", "llama2")
    base_url = os.getenv("OLLAMA_BASE_URL")
    return OllamaProvider(model, base_url)
