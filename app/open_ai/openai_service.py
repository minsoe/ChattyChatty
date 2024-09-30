from openai import OpenAI

from app.database.conversation_manager import ConversationManager
from app.database.models import Conversation, Message, Role


class OpenAIService:

    def __init__(self, client: OpenAI, manager: ConversationManager):
        self.client = client
        self.manager = manager

    async def send(self, prompt: str, conversation: Conversation) -> Message:
        conversation.messages.append(Message(role=Role.USER, content=prompt))

        response = self.client.chat.completions.create(
            messages=conversation.openAiMessages(),
            model="gpt-3.5-turbo"
        )
        assistant_content = response.choices[0].message.content
        assistant_message = Message(role=Role.ASSISTANT, content=assistant_content)
        conversation.messages.append(assistant_message)

        await self.manager.save(conversation)
        return assistant_message
