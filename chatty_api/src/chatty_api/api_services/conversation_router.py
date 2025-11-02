from chatty_core.conversations.conversation_manager import (
    ConversationManager,
    ConversationNotFoundException,
)
from chatty_core.models import Conversation, Message
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv

from chatty_ai import AIService
from chatty_api.api_services.models.requests import Prompt
from chatty_api.api_services.models.responses import ConversationIDs
from chatty_api.IOC.conversation_manager import (
    get_conversation_manager,
)

__all__ = ["router"]

router = APIRouter(prefix="/conversations")


@cbv(router)
class ConversationsRouter:
    manager: ConversationManager = Depends(get_conversation_manager)
    ai_service: AIService = Depends(AIService)

    @router.post("/{conversation_id}")
    async def send(self, conversation_id: str, prompt: Prompt) -> Message:
        """
        Send a message to existing conversation
        """
        conversation = await self.get_conversation(conversation_id)

        if conversation is None:
            raise HTTPException(404, detail="Conversation not found")

        message = await self.ai_service.send(
            prompt=prompt.message, conversation=conversation
        )
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
    async def create_conversation(self, prompt: Prompt):
        """
        Create a new conversation with a starting message
        """
        conversation = await self.manager.create_conversation()
        received = await self.ai_service.send(prompt.message, conversation)
        await self.manager.save(received)
        return conversation
