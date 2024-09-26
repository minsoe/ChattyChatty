from datetime import datetime
from typing import List

from beanie import Document
from pydantic import Field, BaseModel


class Message(BaseModel):
    role: str
    content: str

class Conversation(Document):
    created_at: datetime = Field(default_factory=datetime.now)
    messages: List = Field(default_factory=lambda: [
        {
            "role": "system",
            "content": "Welcome"
        }
    ])



