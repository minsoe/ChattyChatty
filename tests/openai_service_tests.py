import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from chattychatty.database.conversation_manager import ConversationManager
from chattychatty.database.models import BeanieConversation, Conversation, Message, Role
from chattychatty.open_ai.openai_service import OpenAIService
from tests.mocks.mock_ai import mock_ai
from tests.mocks.mock_database import init_mock_database


class OpenAIServieTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await init_mock_database()

    async def asyncTearDown(self):
        await BeanieConversation.get_motor_collection().drop()

    async def test_send_message(self):
        mocked_response = "mocked ai response"
        expected = Message(role=Role.ASSISTANT, content=mocked_response)
        mocked_manager = AsyncMock(ConversationManager)
        conversation = Conversation()
        service = OpenAIService(mocked_manager, ai=mock_ai())

        message = await service.send(prompt="Test", conversation=conversation)

        assert message == expected
        assert conversation.messages == [
            (Message(role=Role.USER, content="Test")),
            (Message(role=Role.ASSISTANT, content=mocked_response)),
        ]
        assert mocked_manager.save.called_once


if __name__ == "__main__":
    unittest.main()
