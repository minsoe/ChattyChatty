from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from bson import ObjectId
from chatty_api.conversation_services import conversation_router
from chatty_api.IOC.agent_manager import get_agent_manager
from chatty_api.IOC.agent_service import get_agent_service
from chatty_api.IOC.ai_service import get_ai_service
from chatty_api.IOC.conversation_manager import get_conversation_manager
from chatty_core.conversations.conversation_manager import ConversationNotFoundException
from chatty_core.database import BeanieConversation
from chatty_core.models import Agent, Message, Role
from chatty_test_services.mocks.mock_database import init_mock_database
from fastapi import FastAPI
from fastapi.testclient import TestClient


def get_conversation_ids_mock_manager():
    manager = MagicMock()
    manager.get_conversations_ids = AsyncMock()
    manager.get_conversations_ids.return_value = [str(ObjectId())]
    return manager


def mock_ai_service():
    return MagicMock()


def mock_agent_manager():
    manager = MagicMock()
    manager.get_agent = AsyncMock()
    manager.get_agent.return_value = Agent(
        model="openai:gpt-4o", system_prompt="System prompt", tools=[]
    )
    return manager


def mock_agent_service():
    service = MagicMock()
    service.run_agent = AsyncMock()
    service.run_agent.return_value = Message(
        role=Role.ASSISTANT, content="mocked agent reply"
    )
    return service


def apply_overrides(app, manager_override=None):
    if manager_override:
        app.dependency_overrides[get_conversation_manager] = manager_override
    app.dependency_overrides[get_ai_service] = mock_ai_service
    app.dependency_overrides[get_agent_manager] = mock_agent_manager
    app.dependency_overrides[get_agent_service] = mock_agent_service


@pytest.fixture
def get_conversation_ids_client():
    app = FastAPI()
    apply_overrides(app, get_conversation_ids_mock_manager)
    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest.fixture
def delete_conversation_client():
    app = FastAPI()

    def delete_conversation_mock_manager():
        manager = MagicMock()
        manager.delete_conversation = AsyncMock()
        return manager

    apply_overrides(app, delete_conversation_mock_manager)
    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest.fixture
def delete_conversation_not_found_client():
    app = FastAPI()

    def delete_conversation_not_found_mock_manager():
        manager = MagicMock()
        manager.delete_conversation = AsyncMock()
        manager.delete_conversation.side_effect = ConversationNotFoundException(
            "not found"
        )
        return manager

    apply_overrides(app, delete_conversation_not_found_mock_manager)
    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest.fixture
def get_converstation_client():
    app = FastAPI()

    def get_conversation_mock_manager():
        manager = MagicMock()
        manager.get_conversation = AsyncMock()
        manager.get_conversation.return_value = BeanieConversation()
        return manager

    apply_overrides(app, get_conversation_mock_manager)
    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest.fixture
def converstation_not_found_client():
    app = FastAPI()

    def get_conversation_not_found_mock_manager():
        manager = MagicMock()
        manager.get_conversation = AsyncMock()
        manager.get_conversation.return_value = None
        return manager

    apply_overrides(app, get_conversation_not_found_mock_manager)
    app.include_router(conversation_router.router)
    return TestClient(app)


def mock_ai_service_with_message():
    ai_service = MagicMock()
    ai_service.send = AsyncMock()
    ai_service.send.return_value = Message(
        role=Role.ASSISTANT, content="Mocked Message"
    )
    return ai_service


@pytest.fixture
def post_conversation_client():
    app = FastAPI()

    def mock_manager():
        manager = MagicMock()
        manager.get_conversation = AsyncMock()
        manager.get_conversation.return_value = BeanieConversation()
        manager.save = AsyncMock()
        return manager

    apply_overrides(app, mock_manager)
    app.dependency_overrides[get_ai_service] = mock_ai_service_with_message
    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest.fixture
def agent_conversation_client():
    app = FastAPI()

    def mock_manager():
        manager = MagicMock()
        manager.get_conversation = AsyncMock()
        conv = BeanieConversation(agent_id=str(ObjectId()))
        manager.get_conversation.return_value = conv
        manager.create_conversation = AsyncMock()
        manager.create_conversation.return_value = conv
        manager.save = AsyncMock()
        return manager

    apply_overrides(app, mock_manager)
    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest_asyncio.fixture(autouse=True)
async def mock_database():
    client = await init_mock_database([BeanieConversation])
    yield client
    await BeanieConversation.get_motor_collection().drop()


class TestConversationRouter:
    def test_delete_conversation(self, delete_conversation_client):
        conversation_id = str(ObjectId())

        response = delete_conversation_client.delete(
            f"/conversations/{conversation_id}"
        )

        assert response.status_code == 200

    def test_delete_conversation_when_not_found(
        self, delete_conversation_not_found_client
    ):
        response = delete_conversation_not_found_client.delete("/conversations/345")

        assert response.status_code == 404

    # @pytest.mark.asyncio
    def test_get_conversation(self, get_converstation_client):
        response = get_converstation_client.get("/conversations/567")

        assert response.status_code == 200

    def test_get_conversation_when_not_found(self, converstation_not_found_client):
        response = converstation_not_found_client.get("/conversations/456")

        assert response.status_code == 404

    def test_post_conversation(self, post_conversation_client):
        response = post_conversation_client.post(
            "/conversations/123", json={"message": "test"}
        )

        assert response.status_code == 200
        assert response.json() == {
            "role": "assistant",
            "content": "Mocked Message",
        }

    def test_post_conversation_when_not_found(self, converstation_not_found_client):
        response = converstation_not_found_client.post(
            "/conversations/7891", json={"message": "test"}
        )

        assert response.status_code == 404

    def test_get_conversations_ids(self, get_conversation_ids_client):
        response = get_conversation_ids_client.get("/conversations/ids/")

        assert response.status_code == 200
        assert len(response.json()["conversation_id_list"]) == 1

    def test_post_conversation_with_agent(self, agent_conversation_client):
        agent_id = str(ObjectId())
        response = agent_conversation_client.post(
            "/conversations/",
            json={"message": "start conversation", "agentId": agent_id},
        )
        assert response.status_code == 200
        assert response.json()["agentId"] == agent_id

    def test_send_message_with_agent(self, agent_conversation_client):
        conversation_id = str(ObjectId())
        response = agent_conversation_client.post(
            f"/conversations/{conversation_id}",
            json={"message": "hello agent"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "role": "assistant",
            "content": "mocked agent reply",
        }
