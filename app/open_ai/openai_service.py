from openai import OpenAI

from app.database.conversation_manager import ConversationManager
from app.database.models import Conversation


class OpenAIService:

    def __init__(self):
        self.client = OpenAI()

    async def send(self, prompt: str, manager: ConversationManager = ConversationManager) -> Conversation:
        conversation = await manager.get_conversation()

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
        system_message = response.choices[0].message.content
        conversation.messages.append(
            {
                "role": "assistant",
                "content": system_message
            }
        )

        await manager.save(conversation)
        return conversation

