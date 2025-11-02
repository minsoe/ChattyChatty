from enum import StrEnum

from openai import OpenAI, OpenAIError

from chattychatty.database.conversation_manager import ConversationManager
from chattychatty.database.models import Conversation, Message, Role
from chattychatty.open_ai.ai_service import AIService


class OpenAIModels(StrEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"


class OpenAiConversation(Conversation):
    def openAiMessages(self):
        return [vars(message) for message in self.messages]


class OpenAIService(AIService):
    def __init__(self, manager: ConversationManager, ai: OpenAI):
        self.manager = manager
        self.ai = ai

    async def send(self, prompt: str, conversation: Conversation) -> Message:
        conversation.messages.append(Message(role=Role.USER, content=prompt))

        response = self.ai.chat.completions.create(
            messages=self._in_open_ai_messages(conversation.messages),  # type: ignore
            model=OpenAIModels.GPT_3_5_TURBO,
        )
        assistant_content = response.choices[0].message.content

        if assistant_content is not None:
            assistant_message = Message(role=Role.ASSISTANT, content=assistant_content)
            conversation.messages.append(assistant_message)

            await self.manager.save(conversation)
            return assistant_message

        raise OpenAIError("no content")

    def _in_open_ai_messages(self, messages: list[Message]):
        return [vars(message) for message in messages]
