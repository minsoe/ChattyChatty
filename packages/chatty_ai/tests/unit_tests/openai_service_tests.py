from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from chatty_core.models import Conversation, Message, Role

from chatty_ai import OpenAIService


class OpenAIServieTests(IsolatedAsyncioTestCase):
    @patch("chatty_ai.openai_service.OpenAI")
    async def test_send_message(self, mocked_openai):
        mocked_content = "mocked ai response"
        choice = MagicMock()
        choice.message = MagicMock()
        choice.message.content = mocked_content

        mocked_response = MagicMock()
        mocked_response.choices = [choice]

        mocked_openai.return_value.chat.completions.create.return_value = (
            mocked_response
        )

        conversation = Conversation()

        service = OpenAIService()
        message = await service.send(prompt="Test", conversation=conversation)

        assert message == Message(role=Role.ASSISTANT, content=mocked_content)
        assert conversation.messages == [
            (Message(role=Role.USER, content="Test")),
            (Message(role=Role.ASSISTANT, content=mocked_content)),
        ]
