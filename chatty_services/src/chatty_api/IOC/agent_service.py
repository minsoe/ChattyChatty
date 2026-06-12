from __future__ import annotations

from chatty_agent import AgentService, LangChainAgentService

__all__ = ["get_agent_service"]


def get_agent_service() -> AgentService:
    return LangChainAgentService()
