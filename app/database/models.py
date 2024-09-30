from datetime import datetime
from typing import List

from beanie import Document
from pydantic import Field, BaseModel
from enum import Enum

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: Role
    content: str

    class Config:
        use_enum_values = True


class Conversation(Document):
    created_at: datetime = Field(default_factory=datetime.now)
    messages: List[Message] = Field(default_factory=lambda: [])

    def openAiMessages(self):
        return [vars(message) for message in self.messages]
