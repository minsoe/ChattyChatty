from chattychatty.database.beanie_conversation_manager import BeanieConversationManager
from chattychatty.database.conversation_manager import ConversationManager

__all__ = ["get_conversation_manager"]


def get_conversation_manager() -> ConversationManager:
    return BeanieConversationManager()
