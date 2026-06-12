from __future__ import annotations

from chatty_ai import AIService, OpenAIService

__all__ = ["get_ai_service"]


def get_ai_service() -> AIService:
    return OpenAIService()
