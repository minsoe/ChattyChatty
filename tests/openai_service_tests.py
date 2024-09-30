import unittest
from typing import List
from unittest.mock import AsyncMock, MagicMock, call

from app.database.models import Conversation, Message, Role
from app.open_ai.openai_service import OpenAIService


class OpenAIServieTests(unittest.IsolatedAsyncioTestCase):
    mocked_response = "Mocked response"

    def mock_manager(self):
        mocked_manager = AsyncMock()
        mocked_conversation = AsyncMock(Conversation)
        mocked_conversation.messages = []
        mocked_manager.get_conversation.return_value = mocked_conversation
        return mocked_manager

    def mock_client(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = self.mocked_response

        mocked_client = MagicMock()
        mocked_client.chat.completions.create.return_value = mock_response
        return mocked_client

    def mock_conversation(self):
        mocked_conversation = MagicMock(Conversation)
        mocked_conversation.messages = MagicMock(List[Message])
        append = MagicMock()
        mocked_conversation.messages.append = append
        return mocked_conversation

    async def test_send_message(self):
        expected = Message(role=Role.ASSISTANT, content=self.mocked_response)
        mocked_manager = self.mock_manager()
        mocked_conversation = self.mock_conversation()
        mocked_client = self.mock_client()

        service = OpenAIService(mocked_client, mocked_manager)
        message = await service.send(prompt="Test", conversation=mocked_conversation)

        assert message == expected
        assert mocked_conversation.messages.append.has_calls([
            call(Message(role=Role.USER, content="Test")),
            call(Message(role=Role.ASSISTANT, content=self.mocked_response)),
        ])
        assert mocked_manager.save.called_once


if __name__ == '__main__':
    unittest.main()
