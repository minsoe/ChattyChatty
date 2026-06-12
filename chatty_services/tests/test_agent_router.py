from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from bson import ObjectId
from chatty_api.agent_services import agent_router
from chatty_api.IOC.agent_manager import get_agent_manager
from chatty_core.agents.agent_manager import AgentNotFoundException
from chatty_core.database import BeanieAgent
from chatty_test_services.mocks.mock_database import init_mock_database
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def agent_client():
    app = FastAPI()

    manager = MagicMock()
    manager.create_agent = AsyncMock()
    manager.get_agents = AsyncMock()
    manager.get_agent = AsyncMock()
    manager.delete_agent = AsyncMock()

    app.dependency_overrides[get_agent_manager] = lambda: manager
    app.include_router(agent_router.router)
    return TestClient(app)


@pytest_asyncio.fixture(autouse=True)
async def mock_database():
    client = await init_mock_database([BeanieAgent])
    yield client
    await BeanieAgent.get_motor_collection().drop()


class TestAgentRouter:
    def test_create_agent(self, agent_client):
        mock_manager = agent_client.app.dependency_overrides[get_agent_manager]()
        mock_manager.create_agent.return_value = BeanieAgent(
            model="openai:gpt-4o",
            system_prompt="System Prompt",
        )

        response = agent_client.post(
            "/agents/",
            json={
                "model": "openai:gpt-4o",
                "systemPrompt": "System Prompt",
            },
        )

        assert response.status_code == 200
        assert response.json()["model"] == "openai:gpt-4o"
        assert response.json()["systemPrompt"] == "System Prompt"

    def test_create_agent_unsupported_model(self, agent_client):
        response = agent_client.post(
            "/agents/",
            json={
                "model": "unsupported-model",
                "systemPrompt": "System Prompt",
            },
        )
        assert response.status_code == 400
        assert "is not supported" in response.json()["detail"]

    def test_get_agents(self, agent_client):
        mock_manager = agent_client.app.dependency_overrides[get_agent_manager]()
        mock_manager.get_agents.return_value = [
            BeanieAgent(model="openai:gpt-4o", system_prompt="Agent 1"),
            BeanieAgent(model="openai:gpt-3.5-turbo", system_prompt="Agent 2"),
        ]

        response = agent_client.get("/agents/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_supported_models(self, agent_client):
        response = agent_client.get("/agents/models")
        assert response.status_code == 200
        assert response.json() == ["openai:gpt-4o", "openai:gpt-3.5-turbo"]

    def test_get_agent_by_id(self, agent_client):
        mock_manager = agent_client.app.dependency_overrides[get_agent_manager]()
        mock_manager.get_agent.return_value = BeanieAgent(
            model="openai:gpt-4o",
            system_prompt="Specific Agent",
        )

        response = agent_client.get(f"/agents/{ObjectId()}")
        assert response.status_code == 200
        assert response.json()["systemPrompt"] == "Specific Agent"

    def test_get_agent_not_found(self, agent_client):
        mock_manager = agent_client.app.dependency_overrides[get_agent_manager]()
        mock_manager.get_agent.return_value = None

        response = agent_client.get(f"/agents/{ObjectId()}")
        assert response.status_code == 404

    def test_delete_agent(self, agent_client):
        response = agent_client.delete(f"/agents/{ObjectId()}")
        assert response.status_code == 200

    def test_delete_agent_not_found(self, agent_client):
        mock_manager = agent_client.app.dependency_overrides[get_agent_manager]()
        mock_manager.delete_agent.side_effect = AgentNotFoundException("not found")

        response = agent_client.delete(f"/agents/{ObjectId()}")
        assert response.status_code == 404
