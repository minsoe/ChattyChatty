from fastapi import Depends
from openai import OpenAI

from chattychatty.IOC.conversation_manager import get_conversation_manager
from chattychatty.open_ai.ai_service import AIService
from chattychatty.open_ai.openai_service import OpenAIService

__all__ = ["get_ai_service"]


def get_ai_service() -> AIService:
    return OpenAIService(Depends(get_conversation_manager), OpenAI())
