import unittest
from unittest.mock import AsyncMock

from app.database.conversation_manager import ConversationManager
from app.database.models import Conversation, Message, Role
from app.open_ai.openai_service import OpenAIService
from tests.mocks.mock_ai import mock_ai
from tests.mocks.mock_database import init_mock_database


class OpenAIServieTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await init_mock_database()

    async def test_send_message(self):
        mocked_response = "mocked ai response"
        expected = Message(role=Role.ASSISTANT, content=mocked_response)
        mocked_manager = AsyncMock(ConversationManager)
        conversation = Conversation()

        service = OpenAIService(mock_ai(), mocked_manager)
        message = await service.send(prompt="Test", conversation=conversation)

        assert message == expected
        assert conversation.messages == [
            (Message(role=Role.USER, content="Test")),
            (Message(role=Role.ASSISTANT, content=mocked_response)),
        ]
        assert mocked_manager.save.called_once


if __name__ == '__main__':
    unittest.main()
