from typing import Optional

from openai import OpenAI

from app.database import find_conversation_by_id


class OpenAIService:

    def __init__(self):
        self.client = OpenAI()

    async def send(self, prompt: str, conversation_id: Optional[str] = None):
        conversation = await find_conversation_by_id(conversation_id)
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
