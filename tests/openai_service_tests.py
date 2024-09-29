import unittest
from unittest.mock import AsyncMock, MagicMock

from app.database.models import Conversation, Message
from app.open_ai.openai_service import OpenAIService


class OpenAIServieTests(unittest.IsolatedAsyncioTestCase):
    mocked_response = "Mocked response"

    def mock_manager(self):
        mocked_manager = AsyncMock()
        mocked_conversation = AsyncMock(Conversation)
        mocked_conversation.messages = [Message(role="system", content="Welcome")]
        mocked_manager.get_conversation.return_value = mocked_conversation
        return mocked_manager

    def mock_client(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = self.mocked_response

        mocked_client = MagicMock()
        mocked_client.chat.completions.create.return_value = mock_response
        return mocked_client

    async def test_send_message(self):
        expected = Message(role="assistant", content=self.mocked_response)
        mocked_manager = self.mock_manager()
        service = OpenAIService(self.mock_client(), mocked_manager)
        message = await service.send(prompt="Test")

        self.assertEqual(message, expected)
        mocked_manager.get_conversation.assert_called_once()
        mocked_manager.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
