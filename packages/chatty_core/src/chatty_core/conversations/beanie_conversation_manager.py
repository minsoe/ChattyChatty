from chatty_core.conversations.conversation_manager import (
    ConversationNotFoundException,
)
from chatty_core.database import BeanieConversation
from chatty_core.models import Conversation

__all__ = ["BeanieConversationManager"]


class BeanieConversationManager:
    async def get_conversations_ids(self) -> list[str]:
        conversations = await BeanieConversation.find_all().to_list()
        return [str(conversation.id) for conversation in conversations]

    async def get_conversation(self, conversation_id: str) -> BeanieConversation | None:
        return await BeanieConversation.get(document_id=conversation_id)

    async def delete_conversation(self, conversation_id: str):
        converstion = await self.get_conversation(conversation_id)
        if converstion is not None:
            await converstion.delete()
        else:
            raise ConversationNotFoundException(f"{conversation_id} not found")

    async def save(self, conversation: Conversation):
        if isinstance(conversation, BeanieConversation):
            b_conversation: BeanieConversation = conversation
            await b_conversation.save()

    async def create_conversation(self) -> Conversation:
        conversation = BeanieConversation()
        return conversation
