from chatty_core.conversations.beanie_conversation_manager import (
    BeanieConversationManager,
)
from chatty_core.conversations.conversation_manager import ConversationManager

__all__ = ["get_conversation_manager"]


def get_conversation_manager() -> ConversationManager:
    return BeanieConversationManager()
