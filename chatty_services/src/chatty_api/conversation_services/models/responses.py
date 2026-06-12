from __future__ import annotations

from pydantic import BaseModel


class ConversationIDs(BaseModel):
    conversation_id_list: list[str]
