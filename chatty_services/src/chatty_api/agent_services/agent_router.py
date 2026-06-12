from __future__ import annotations

from chatty_api.agent_services.models.requests import CreateAgentRequest
from chatty_api.IOC.agent_manager import get_agent_manager
from chatty_core.agents import AgentManager, AgentNotFoundException
from chatty_core.models import Agent
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv

__all__ = ["router"]

router = APIRouter(prefix="/agents")

SUPPORTED_MODELS = ["openai:gpt-4o", "openai:gpt-3.5-turbo"]


@cbv(router)
class AgentsRouter:
    manager: AgentManager = Depends(get_agent_manager)

    @router.post("/")
    async def create_agent(self, request: CreateAgentRequest) -> Agent:
        """
        Create a new agent configurations
        """
        if request.model not in SUPPORTED_MODELS:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{request.model}' is not supported. Supported models are: {SUPPORTED_MODELS}",
            )
        agent = Agent(
            model=request.model,
            system_prompt=request.system_prompt,
        )
        return await self.manager.create_agent(agent)

    @router.get("/")
    async def get_agents(self) -> list[Agent]:
        """
        Retrieve all registered agents
        """
        return await self.manager.get_agents()

    @router.get("/models")
    async def get_supported_models(self) -> list[str]:
        """
        Retrieve all supported models for agents
        """
        return SUPPORTED_MODELS

    @router.get("/{agent_id}")
    async def get_agent(self, agent_id: str) -> Agent:
        """
        Retrieve the configuration of a specific agent
        """
        agent = await self.manager.get_agent(agent_id)
        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent

    @router.delete("/{agent_id}")
    async def delete_agent(self, agent_id: str):
        """
        Delete an agent by ID
        """
        try:
            await self.manager.delete_agent(agent_id)
        except AgentNotFoundException:
            raise HTTPException(status_code=404, detail="Agent not found")
