from __future__ import annotations

from chatty_core.agents import AgentManager, BeanieAgentManager

__all__ = ["get_agent_manager"]


def get_agent_manager() -> AgentManager:
    return BeanieAgentManager()
