from __future__ import annotations

from chatty_core.models.models import ChattyBaseModel

__all__ = ["CreateAgentRequest"]


class CreateAgentRequest(ChattyBaseModel):
    model: str
    system_prompt: str
