from typing import Optional
from openai import OpenAI
from app.models import Conversation


class OpenAIService:

    def __init__(self):
        self.client = OpenAI()

    async def send(self, prompt: str, conversation: Optional[Conversation] = None):
        create = 0
        if conversation is None:
            create = 1
            conversation = Conversation()

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
        if create == 1:
            await conversation.insert()
        else:
            await conversation.save()
        return conversation

