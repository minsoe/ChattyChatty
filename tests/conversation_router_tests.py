import unittest
from unittest.mock import AsyncMock, MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api_services.conversation_router import init_conversation_router


class ConversationRouterTests(unittest.TestCase):

    def mock_manager(self):
        manager = MagicMock()
        manager.get_conversation = AsyncMock(return_value=MagicMock(
            messages=[{"role": "user", "content": "message1"}, {"role": "assistant", "content": "message2"}]))
        manager.delete_conversation = AsyncMock()
        return manager

    def mock_ai_service(self):
        ai_service = MagicMock()
        ai_service.send = AsyncMock()
        ai_service.send.return_value = {"role": "assistant", "content": "message1"}
        return ai_service

    def client(self):
        app = FastAPI()
        init_conversation_router(app, manager=self.mock_manager(), ai_service=self.mock_ai_service())
        return TestClient(app)

    def test_send_conversation(self):
        response = self.client().post("/conversation", json={"message": "test prompt"})
        assert response.status_code == 200
        assert response.json() == {"role": "assistant", "content": "message1"}

    def test_delete_conversation(self):
        response = self.client().delete("/conversation")
        assert response.status_code == 200

    def test_get_conversations(self):
        response = self.client().get("/conversation")
        assert response.status_code == 200
        assert response.json() == [{"role": "user", "content": "message1"},
                                   {"role": "assistant", "content": "message2"}]


if __name__ == '__main__':
    unittest.main()
