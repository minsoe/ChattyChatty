from __future__ import annotations

from chatty_agent import AgentService
from chatty_ai import AIService
from chatty_core.agents import AgentManager
from chatty_core.conversations.conversation_manager import (
    ConversationManager,
    ConversationNotFoundException,
)
from chatty_core.models import Conversation, Message
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv

from chatty_api.conversation_services.models.requests import Prompt
from chatty_api.conversation_services.models.responses import ConversationIDs
from chatty_api.IOC.agent_manager import get_agent_manager
from chatty_api.IOC.agent_service import get_agent_service
from chatty_api.IOC.ai_service import get_ai_service
from chatty_api.IOC.conversation_manager import (
    get_conversation_manager,
)

__all__ = ["router"]

router = APIRouter(prefix="/conversations")


@cbv(router)
class ConversationsRouter:
    manager: ConversationManager = Depends(get_conversation_manager)
    ai_service: AIService = Depends(get_ai_service)
    agent_manager: AgentManager = Depends(get_agent_manager)
    agent_service: AgentService = Depends(get_agent_service)

    @router.post("/{conversation_id}")
    async def send(self, conversation_id: str, prompt: Prompt) -> Message:
        """
        Send a message to existing conversation
        """
        conversation = await self.get_conversation(conversation_id)

        if conversation is None:
            raise HTTPException(404, detail="Conversation not found")

        if conversation.agent_id:
            agent_config = await self.agent_manager.get_agent(conversation.agent_id)
            if agent_config is None:
                raise HTTPException(404, detail="Agent not found")
            message = await self.agent_service.run_agent(
                agent_config=agent_config,
                conversation=conversation,
                prompt=prompt.message,
            )
        else:
            message = await self.ai_service.send(
                prompt=prompt.message, conversation=conversation
            )

        await self.manager.save(conversation)
        return message

    @router.delete("/{conversation_id}")
    async def delete_conversation(self, conversation_id: str):
        """
        Delete the current conversation history to initiate a new conversation
        """
        try:
            await self.manager.delete_conversation(conversation_id)
        except ConversationNotFoundException:
            raise HTTPException(status_code=404, detail="Converstion not found")

    @router.get("/{conversation_id}")
    async def get_conversation(self, conversation_id: str) -> Conversation:
        """
        Retrieve the current conversation's messages
        """
        conversation = await self.manager.get_conversation(conversation_id)

        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return conversation

    @router.get("/ids/")
    async def get_conversations(self) -> ConversationIDs:
        """
        Retrieve all the conversations
        """
        conversations = await self.manager.get_conversations_ids()
        if conversations is None:
            raise HTTPException(status_code=404, detail="Conversations not found")

        return ConversationIDs(conversation_id_list=conversations)

    @router.post("/")
    async def create_conversation(self, prompt: Prompt) -> Conversation:
        """
        Create a new conversation with a starting message
        """
        conversation = await self.manager.create_conversation()
        if prompt.agent_id:
            conversation.agent_id = prompt.agent_id

        if conversation.agent_id:
            agent_config = await self.agent_manager.get_agent(conversation.agent_id)
            if agent_config is None:
                raise HTTPException(404, detail="Agent not found")
            await self.agent_service.run_agent(
                agent_config=agent_config,
                conversation=conversation,
                prompt=prompt.message,
            )
        else:
            await self.ai_service.send(prompt.message, conversation)

        await self.manager.save(conversation)
        return conversation
