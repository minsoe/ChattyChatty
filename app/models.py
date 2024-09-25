from beanie import Document
from pydantic import Field, UUID1
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

class Conversation(Document):
    created_at: datetime = Field(default_factory=datetime.now)
    messages: List = []

