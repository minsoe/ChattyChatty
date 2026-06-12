from __future__ import annotations

from chatty_core.agents.agent_manager import AgentNotFoundException
from chatty_core.database import BeanieAgent
from chatty_core.models import Agent

__all__ = ["BeanieAgentManager"]


class BeanieAgentManager:
    async def get_agent(self, agent_id: str) -> BeanieAgent | None:
        try:
            return await BeanieAgent.get(document_id=agent_id)
        except Exception:
            # Handle invalid ObjectId / general exceptions gracefully
            return None

    async def get_agents(self) -> list[BeanieAgent]:
        return await BeanieAgent.find_all().to_list()

    async def create_agent(self, agent: Agent) -> BeanieAgent:
        # Construct BeanieAgent using the data fields of the model
        beanie_agent = BeanieAgent(
            model=agent.model,
            system_prompt=agent.system_prompt,
            tools=agent.tools,
        )
        await beanie_agent.insert()
        return beanie_agent

    async def delete_agent(self, agent_id: str):
        beanie_agent = await self.get_agent(agent_id)
        if beanie_agent is not None:
            await beanie_agent.delete()
        else:
            raise AgentNotFoundException(f"Agent with ID {agent_id} not found")
