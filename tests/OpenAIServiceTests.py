import unittest
from unittest.mock import patch, MagicMock
from app.openai_service import OpenAIService
from app.models import Conversation

class OpenAIServieTests(unittest.TestCase):

    @patch('app.openai_service.MongoClient')
    @patch('app.openai_service.OpenAI')
    def test_send_message(self, mock_ai, mock_mongo):
        mocked_message = "Mocked response"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=mocked_message)]

        ai_instance = mock_ai.return_value
        ai_instance.chat.completions.create.return_value = mock_response

        mongo_instance = mock_mongo.return_value
        mock_db = mongo_instance['chat_history']
        mock_collection = mock_db['chatty_chatty']

        service = OpenAIService()
        self.assertEqual(service.send("Test"), mocked_message)
        conversation = Conversation(user="Test", system=mocked_message)
        mock_collection.insert_one.assert_called_once_with(conversation.model_dump())


if __name__ == '__main__':
    unittest.main()
