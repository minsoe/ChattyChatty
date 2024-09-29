from openai import OpenAI
import json

from openai.types.chat import ChatCompletionAssistantMessageParam

from app.database.conversation_manager import ConversationManager
from app.database.models import Conversation, Message


class OpenAIService:

    def __init__(self, client: OpenAI, manager: ConversationManager):
        self.client = client
        self.manager = manager

    async def send(self, prompt: str) -> Message:
        conversation = await self.manager.get_conversation()

        conversation.messages.append(Message(role="user", content=prompt))

        response = self.client.chat.completions.create(
            messages=[vars(message) for message in conversation.messages],
            model="gpt-3.5-turbo"
        )
        assistant_content = response.choices[0].message.content
        assistant_message = Message(role="assistant", content=assistant_content)
        conversation.messages.append(assistant_message)

        await self.manager.save(conversation)
        return assistant_message
