from app.database.models import Conversation

class ConversationManager:

    async def get_conversation(self) -> Conversation:
        conversation = await Conversation.find_one()
        if conversation is None:
            conversation = self.create_conversation()
            await Conversation.insert_one(conversation)
        return conversation

    async def delete_conversation(self):
        await Conversation.delete_all()

    async def save(self, conversation: Conversation):
        await  conversation.save()

    def create_conversation(self) -> Conversation:
        return Conversation()