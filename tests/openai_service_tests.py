import unittest
from unittest.mock import patch, MagicMock, AsyncMock

from dotenv import load_dotenv

from app.database import init_mongodb
from app.openai_service import OpenAIService
from app.models import Conversation

class OpenAIServieTests(unittest.TestCase):

    def _test_actual_message(self):
        load_dotenv()
        init_mongodb()
        service = OpenAIService()
        self.assertIsNotNone(service.send(prompt="testing"))

    @patch('app.models.Conversation')
    @patch('app.openai_service.OpenAI')
    def test_send_message(self, mock_ai, mock_conversation):
        mocked_message = "Mocked response"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=mocked_message)]

        ai_instance = mock_ai.return_value
        ai_instance.chat.completions.create.return_value = mock_response

        mock_conversation_instance = mock_conversation.get.return_value
        mock_conversation_instance.save = AsyncMock()
        service = OpenAIService()
        self.assertEqual(service.send(prompt="Test"), mocked_message)
        mock_conversation_instance.save.assert_called_once()



if __name__ == '__main__':
    unittest.main()
