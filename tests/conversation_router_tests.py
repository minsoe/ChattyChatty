import unittest
from unittest.mock import AsyncMock, MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api_services.conversation_router import init_conversation_router
from app.database.conversation_manager import ConversationManager
from app.database.models import Conversation, Message, Role
from app.open_ai.openai_service import OpenAIService
from tests.mocks.mock_database import init_mock_database


class ConversationRouterTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await init_mock_database()

    def mock_ai_service(self):
        ai_service = MagicMock()
        ai_service.send = AsyncMock()
        ai_service.send.return_value = Message(role=Role.ASSISTANT, content="Mocked Message")
        return ai_service

    def mock_manager_with_get_conversation_return_value(self, value):
        mock_manager = MagicMock(ConversationManager)
        get_conversation = AsyncMock()
        get_conversation.return_value = value
        mock_manager.get_conversation = get_conversation
        return mock_manager

    def client(self, manager: ConversationManager, ai_service: OpenAIService):
        app = FastAPI()
        init_conversation_router(app, manager, ai_service)
        return TestClient(app)

    def test_delete_conversation(self):
        mock_manager = self.mock_manager_with_get_conversation_return_value(MagicMock(Conversation))
        mock_manager.delete_conversation = AsyncMock()

        response = self.client(mock_manager, MagicMock()).delete("/conversations/123")

        assert response.status_code == 200

    def test_delete_conversation_when_not_found(self):
        mock_manager = self.mock_manager_with_get_conversation_return_value(None)
        mock_manager.delete_conversation = AsyncMock()

        response = self.client(mock_manager, MagicMock()).delete("/conversations/345")

        assert response.status_code == 404

    def test_get_conversation(self):
        mock_manager = self.mock_manager_with_get_conversation_return_value(MagicMock(Conversation))

        response = self.client(mock_manager, MagicMock()).get("/conversations/567")

        assert response.status_code == 200

    def test_get_conversation_when_not_found(self):
        mock_manager = self.mock_manager_with_get_conversation_return_value(None)

        response = self.client(mock_manager, MagicMock()).get("/conversations/456")

        assert response.status_code == 404

    def test_post_conversation(self):
        mock_manager = self.mock_manager_with_get_conversation_return_value(MagicMock(Conversation))
        mock_ai_service = self.mock_ai_service()

        response = self.client(mock_manager, mock_ai_service).post("/conversations/123", json={"message": "test"})

        assert response.status_code == 200
        assert response.json() == {'role': 'assistant', 'content': 'Mocked Message'}

    def test_post_conversation_when_not_found(self):
        mock_manager = self.mock_manager_with_get_conversation_return_value(None)

        response = self.client(mock_manager, MagicMock()).post("/conversations/7891", json={"message": "test"})

        assert response.status_code == 404

    def test_get_conversations(self):
        mock_manager = MagicMock(ConversationManager)
        mock_manager.get_conversations_ids.return_value = ["123"]

        response = self.client(mock_manager, MagicMock()).get("/conversations")

        assert response.status_code == 200
        assert response.json() == {"conversation_id_list": ["123"]}

    def test_get_conversations_when_empty(self):
        mock_manager = MagicMock(ConversationManager)
        mock_manager.get_conversations_ids.return_value = []

        response = self.client(mock_manager, MagicMock()).get("/conversations")

        assert response.status_code == 200
        assert response.json() == {"conversation_id_list": []}

    def test_put_conversation(self):
        mock_manager = MagicMock(ConversationManager)
        mock_manager.create_conversation.return_value = Conversation()

        response = self.client(mock_manager, self.mock_ai_service()).put("/conversations", json={"message": "test"})

        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
