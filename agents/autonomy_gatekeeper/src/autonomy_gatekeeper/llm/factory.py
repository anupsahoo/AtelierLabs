"""LLM factory — creates configured language model instances."""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from autonomy_gatekeeper.config import Settings


def create_llm(settings: Settings) -> ChatOpenAI:
    """Create a ChatOpenAI instance from application settings."""
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.0,
    )
