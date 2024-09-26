import unittest

from unittest.mock import patch, AsyncMock

from app.database.conversation_manager import ConversationManager
from app.open_ai.openai_service import OpenAIService
from app.database.models import Conversation

class OpenAIServieTests(unittest.IsolatedAsyncioTestCase):

    @patch('app.openai_service.OpenAI')
    async def test_send_message(self, mock_ai):
        mocked_manager = AsyncMock(ConversationManager)
        mocked_conversation = AsyncMock(Conversation)
        mocked_conversation.messages = [
            {
                "role": "system",
                "content": "Welcome"
            }
        ]
        mocked_manager.get_conversation.return_value = mocked_conversation

        mocked_message = "Mocked response"
        mock_response = AsyncMock()
        mock_response.choices[0].message.content = mocked_message

        mocked_client = mock_ai.return_value
        mocked_client.chat.completions.create.return_value = mock_response

        service = OpenAIService()
        conversation = await service.send(prompt="Test", manager=mocked_manager)

        self.assertEqual(3, len(conversation.messages))
        mocked_manager.get_conversation.assert_called_once()
        mocked_manager.save.assert_called_once()

if __name__ == '__main__':
    unittest.main()
