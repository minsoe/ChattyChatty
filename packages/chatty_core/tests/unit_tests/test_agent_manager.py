from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

from chatty_test_services.mocks.mock_database import init_mock_database

from chatty_core.agents.beanie_agent_manager import BeanieAgentManager
from chatty_core.database import BeanieAgent
from chatty_core.models import Agent


class TestAgentManager(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = await init_mock_database([BeanieAgent])

    async def asyncTearDown(self):
        await BeanieAgent.get_motor_collection().drop()

    async def test_create_and_get_agent(self):
        manager = BeanieAgentManager()
        agent_in = Agent(
            model="openai:gpt-4o",
            system_prompt="Test agent",
            tools=["calculator"],
        )
        created = await manager.create_agent(agent_in)
        assert created.id is not None

        retrieved = await manager.get_agent(str(created.id))
        assert retrieved is not None
        assert retrieved.model == "openai:gpt-4o"
        assert retrieved.system_prompt == "Test agent"
        assert retrieved.tools == ["calculator"]

    async def test_get_agents(self):
        manager = BeanieAgentManager()
        a1 = Agent(model="openai:gpt-4o", system_prompt="Agent 1")
        a2 = Agent(model="openai:gpt-3.5-turbo", system_prompt="Agent 2")
        await manager.create_agent(a1)
        await manager.create_agent(a2)

        agents = await manager.get_agents()
        assert len(agents) == 2

    async def test_delete_agent(self):
        manager = BeanieAgentManager()
        a = Agent(model="openai:gpt-4o", system_prompt="Delete me")
        created = await manager.create_agent(a)

        await manager.delete_agent(str(created.id))

        retrieved = await manager.get_agent(str(created.id))
        assert retrieved is None
