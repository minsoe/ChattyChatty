from abc import abstractmethod
from typing import Protocol

from chattychatty.database.models import Conversation, Message


class AIService(Protocol):
    @abstractmethod
    async def send(self, prompt: str, conversation: Conversation) -> Message:
        pass
