"""Configuration loader — reads environment variables and validates settings."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    log_level: str = "INFO"
    policy_path: str = str(
        Path(__file__).parent / "policy" / "rules.yaml"
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def load_settings() -> Settings:
    """Load and return validated application settings."""
    return Settings()
