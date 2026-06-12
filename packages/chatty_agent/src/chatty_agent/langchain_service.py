from __future__ import annotations

from typing import Any

from chatty_core.models import Agent as CoreAgent
from chatty_core.models import Conversation, Message, Role
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage

from chatty_agent.agent_service import AgentService
from chatty_agent.tools import TOOL_MAPPING

__all__ = ["LangChainAgentService"]


class LangChainAgentService(AgentService):
    async def run_agent(
        self, agent_config: CoreAgent, conversation: Conversation, prompt: str
    ) -> Message:
        # Convert existing messages to langchain message classes
        langchain_messages: list[Any] = []
        for msg in conversation.messages:
            if msg.role == Role.USER:
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == Role.ASSISTANT:
                langchain_messages.append(AIMessage(content=msg.content))

        # Append the current user prompt
        langchain_messages.append(HumanMessage(content=prompt))

        # Resolve tools by checking name in mapping
        tools = [
            TOOL_MAPPING[name] for name in agent_config.tools if name in TOOL_MAPPING
        ]

        # Parse model name (e.g. "openai:gpt-4o")
        provider, _, model = agent_config.model.partition(":")
        if not model:
            # Fallback if provider was not specified
            model = provider
            provider = "openai"

        # Initialize langchain chat model
        chat_model = init_chat_model(
            model=model,
            model_provider=provider,
            temperature=0.0,
        )

        # Create the deep agent
        agent = create_deep_agent(
            model=chat_model,
            tools=tools,
            system_prompt=agent_config.system_prompt,
        )

        # Invoke the agent asynchronously
        response = await agent.ainvoke({"messages": langchain_messages})

        # Retrieve output messages from the agent execution state
        output_messages = response.get("messages", [])
        if not output_messages:
            raise ValueError("No response messages returned by the agent")

        # The last message is the final assistant response
        final_msg = output_messages[-1]
        final_content = final_msg.content

        # Update conversation history with user message and assistant message
        conversation.messages.append(Message(role=Role.USER, content=prompt))
        assistant_message = Message(role=Role.ASSISTANT, content=final_content)
        conversation.messages.append(assistant_message)

        return assistant_message
