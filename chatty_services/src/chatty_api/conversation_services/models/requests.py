from __future__ import annotations

from chatty_core.models.models import ChattyBaseModel


class Prompt(ChattyBaseModel):
    message: str
    agent_id: str | None = None
