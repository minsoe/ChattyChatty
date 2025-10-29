from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from bson import ObjectId
from fastapi import FastAPI
from fastapi.testclient import TestClient

from chattychatty.api_services import conversation_router
from chattychatty.database.conversation_manager import ConversationNotFoundException
from chattychatty.database.models import BeanieConversation, Message, Role
from chattychatty.IOC.ai_service import get_ai_service
from chattychatty.IOC.conversation_manager import get_conversation_manager
from tests.mocks.mock_database import init_mock_database


@pytest.fixture
def get_conversation_ids_client():
    app = FastAPI()

    def get_conversation_ids_mock_manager():
        manager = MagicMock()
        manager.get_conversations_ids = AsyncMock()
        manager.get_conversations_ids.return_value = [str(ObjectId())]
        return manager

    app.dependency_overrides[get_conversation_manager] = (
        get_conversation_ids_mock_manager
    )

    def mock_ai_service():
        return MagicMock()

    app.dependency_overrides[get_ai_service] = mock_ai_service

    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest.fixture
def delete_conversation_client():
    app = FastAPI()

    def delete_conversation_mock_manager():
        manager = MagicMock()
        manager.delete_conversation = AsyncMock()
        return manager

    app.dependency_overrides[get_conversation_manager] = (
        delete_conversation_mock_manager
    )

    def mock_ai_service():
        return MagicMock()

    app.dependency_overrides[get_ai_service] = mock_ai_service

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

    app.dependency_overrides[get_conversation_manager] = (
        delete_conversation_not_found_mock_manager
    )

    def mock_ai_service():
        return MagicMock()

    app.dependency_overrides[get_ai_service] = mock_ai_service

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

    app.dependency_overrides[get_conversation_manager] = get_conversation_mock_manager

    def mock_ai_service():
        return MagicMock()

    app.dependency_overrides[get_ai_service] = mock_ai_service

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

    app.dependency_overrides[get_conversation_manager] = (
        get_conversation_not_found_mock_manager
    )

    def mock_ai_service():
        return MagicMock()

    app.dependency_overrides[get_ai_service] = mock_ai_service

    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest.fixture
def post_conversation_client():
    app = FastAPI()

    def mock_manager():
        manager = MagicMock()
        manager.get_conversation = AsyncMock()
        manager.get_conversation.return_value = BeanieConversation()
        return manager

    app.dependency_overrides[get_conversation_manager] = mock_manager

    def mock_ai_service():
        ai_service = MagicMock()
        ai_service.send = AsyncMock()
        ai_service.send.return_value = Message(
            role=Role.ASSISTANT, content="Mocked Message"
        )
        return ai_service

    app.dependency_overrides[get_ai_service] = mock_ai_service
    app.include_router(conversation_router.router)
    return TestClient(app)


@pytest_asyncio.fixture(autouse=True)
async def mock_database():
    client = await init_mock_database()
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
        # mock_manager.get_conversation.return_value = MagicMock(Conversation)
        # client.app.manager.get_conversations_ids.return_value = MagicMock(Conversation)
        response = post_conversation_client.post(
            "/conversations/123", json={"message": "test"}
        )

        assert response.status_code == 200
        assert response.json() == {
            "role": "assistant",
            "content": "Mocked Message",
        }

    def test_post_conversation_when_not_found(self, converstation_not_found_client):
        # mock_manager.get_conversation.return_value = None
        # client.app.manager.get_conversations_ids.return_value = None
        response = converstation_not_found_client.post(
            "/conversations/7891", json={"message": "test"}
        )

        assert response.status_code == 404

    def test_get_conversations_ids(self, get_conversation_ids_client):
        response = get_conversation_ids_client.get("/conversations/ids/")

        assert response.status_code == 200
        assert len(response.json()["conversation_id_list"]) == 1
