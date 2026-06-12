from __future__ import annotations

from typing import Protocol, abstractmethod

from chatty_core.models import Agent, Conversation, Message

__all__ = ["AgentService"]


class AgentService(Protocol):
    @abstractmethod
    async def run_agent(
        self, agent_config: Agent, conversation: Conversation, prompt: str
    ) -> Message:
        pass
