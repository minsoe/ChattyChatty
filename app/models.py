from pydantic import BaseModel, Field
from datetime import datetime, timezone
from bson import ObjectId
from typing import Optional, List

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema

class Conversation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    messages: List = []

