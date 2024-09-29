from datetime import datetime
from typing import List, Union

from beanie import Document
from openai.types.chat import ChatCompletionAssistantMessageParam, ChatCompletionSystemMessageParam, \
    ChatCompletionUserMessageParam
from pydantic import Field, BaseModel

class Message(BaseModel):
    role: str
    content: str


class Conversation(Document):
    created_at: datetime = Field(default_factory=datetime.now)
    messages: List[Message] = Field(default_factory=lambda: [])
