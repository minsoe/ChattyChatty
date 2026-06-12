from __future__ import annotations

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from chatty_core.models import Agent as CoreAgent
from chatty_core.models import Conversation, Message, Role
from langchain_core.messages import AIMessage

from chatty_agent.langchain_service import LangChainAgentService


class TestAgentService(IsolatedAsyncioTestCase):
    @patch("chatty_agent.langchain_service.create_deep_agent")
    @patch("chatty_agent.langchain_service.init_chat_model")
    async def test_run_agent(self, mock_init_chat_model, mock_create_deep_agent):
        # Setup mock compiled agent response
        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock()
        mock_agent.ainvoke.return_value = {
            "messages": [AIMessage(content="mocked agent response")]
        }
        mock_create_deep_agent.return_value = mock_agent

        # Setup core model objects
        conversation = Conversation()
        agent_config = CoreAgent(
            model="openai:gpt-4o",
            system_prompt="Test system prompt",
            tools=["calculator"],
        )

        service = LangChainAgentService()
        response = await service.run_agent(agent_config, conversation, "Hello agent")

        # Assertions
        assert response == Message(role=Role.ASSISTANT, content="mocked agent response")
        assert len(conversation.messages) == 2
        assert conversation.messages[0] == Message(
            role=Role.USER, content="Hello agent"
        )
        assert conversation.messages[1] == Message(
            role=Role.ASSISTANT, content="mocked agent response"
        )

        # Verify mocks were called with correct arguments
        mock_init_chat_model.assert_called_once_with(
            model="gpt-4o",
            model_provider="openai",
            temperature=0.0,
        )
        mock_create_deep_agent.assert_called_once()
