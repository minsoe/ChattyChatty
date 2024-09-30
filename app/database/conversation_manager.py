from typing import Optional

from app.database.models import Conversation


class ConversationManager:
    async def get_conversations_ids(self):
        conversations = await Conversation.find_all().to_list()
        return [str(conversation.id) for conversation in conversations]

    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return await Conversation.get(conversation_id)

    async def delete_conversation(self, conversation: Conversation):
        await conversation.delete()

    async def save(self, conversation: Conversation):
        await  conversation.save()

    async def create_conversation(self) -> Conversation:
        conversation = await self._converstaion()
        return await Conversation.insert_one(conversation)

    def _conversation(self):
        return Conversation()
