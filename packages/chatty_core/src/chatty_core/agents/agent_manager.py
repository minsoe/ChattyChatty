from __future__ import annotations

from abc import abstractmethod
from typing import Protocol

from chatty_core.models import Agent

__all__ = ["AgentNotFoundException", "AgentManager"]


class AgentNotFoundException(Exception):
    pass


class AgentManager(Protocol):
    @abstractmethod
    async def get_agent(self, agent_id: str) -> Agent | None:
        pass

    @abstractmethod
    async def get_agents(self) -> list[Agent]:
        pass

    @abstractmethod
    async def create_agent(self, agent: Agent) -> Agent:
        pass

    @abstractmethod
    async def delete_agent(self, agent_id: str):
        pass
