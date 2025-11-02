from abc import abstractmethod
from typing import Protocol

from chatty_core.models import Conversation, Message

__all__ = ["AIService"]


class AIService(Protocol):
    @abstractmethod
    async def send(self, prompt: str, conversation: Conversation) -> Message:
        pass
