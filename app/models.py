from beanie import Document
from pydantic import Field, UUID1, BaseModel
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

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



