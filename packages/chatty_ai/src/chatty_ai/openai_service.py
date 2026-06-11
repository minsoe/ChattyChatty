from enum import StrEnum

from chatty_core.models import Conversation, Message, Role
from openai import OpenAI, OpenAIError

from chatty_ai.ai_service import AIService

__all__ = ["OpenAIModel", "OpenAIService"]


class OpenAIModel(StrEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4O = "gpt-4o"


class OpenAiConversation(Conversation):
    def openAiMessages(self):
        return [vars(message) for message in self.messages]


class OpenAIService(AIService):
    def __init__(self, model: OpenAIModel = OpenAIModel.GPT_4O):
        self.model = model
        self.ai = OpenAI()

    async def send(self, prompt: str, conversation: Conversation) -> Message:
        conversation.messages.append(Message(role=Role.USER, content=prompt))

        response = self.ai.chat.completions.create(
            messages=self._in_open_ai_messages(conversation.messages),  # type: ignore
            model=self.model,
        )
        assistant_content = response.choices[0].message.content

        if assistant_content is not None:
            assistant_message = Message(role=Role.ASSISTANT, content=assistant_content)
            conversation.messages.append(assistant_message)
            return assistant_message

        raise OpenAIError("no content")

    def _in_open_ai_messages(self, messages: list[Message]):
        return [vars(message) for message in messages]
