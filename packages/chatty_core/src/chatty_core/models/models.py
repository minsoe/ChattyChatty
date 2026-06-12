from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["Role", "Message", "Conversation", "Agent"]


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"


def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class ChattyBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        use_enum_values=True,
        populate_by_name=True,  # Allows input using either original field name or alias
    )


class Message(ChattyBaseModel):
    role: Role
    content: str


class Conversation(ChattyBaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    messages: List[Message] = Field(default_factory=lambda: [])
    agent_id: str | None = None


class Agent(ChattyBaseModel):
    model: str
    system_prompt: str
    tools: List[str] = []
