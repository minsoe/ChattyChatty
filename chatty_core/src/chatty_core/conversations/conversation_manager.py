from abc import abstractmethod
from typing import Protocol

from chatty_core.models import Conversation

__all__ = ["ConversationNotFoundException", "ConversationManager"]


class ConversationNotFoundException(Exception):
    pass


class ConversationManager(Protocol):
    @abstractmethod
    async def get_conversations_ids(self) -> list[str]:
        pass

    @abstractmethod
    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        pass

    @abstractmethod
    async def delete_conversation(self, conversation_id: str):
        pass

    @abstractmethod
    async def save(self, conversation: Conversation):
        pass

    @abstractmethod
    async def create_conversation(self) -> Conversation:
        pass
