from openai import OpenAI
from bson import ObjectId
from app.models import Conversation

class OpenAIService:

    def __init__(self):
        self.client = OpenAI()

    async def find_conversation_by_id(self, conversation_id: str) -> Conversation:
        conversation = await Conversation.get(ObjectId(conversation_id))
        if conversation:
            return conversation
        return Conversation()

    async def send(self, conversation_id: str, prompt: str):
        conversation = await self.find_conversation_by_id(conversation_id)
        conversation.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        response = self.client.chat.completions.create(
            messages=conversation.messages,
            model="gpt-3.5-turbo"
        )
        system_message = response.choices[0].message
        conversation.messages.append(
            {
                "role": "system",
                "content": system_message
            }
        )
        await conversation.save()
        return system_message
