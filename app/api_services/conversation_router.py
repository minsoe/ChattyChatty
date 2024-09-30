from fastapi import APIRouter, FastAPI, HTTPException

from app.api_services.request_models.prompt import Prompt
from app.database.conversation_manager import ConversationManager
from app.open_ai.openai_service import OpenAIService


def init_conversation_router(api: FastAPI, manager: ConversationManager,
                             ai_service: OpenAIService):
    router = APIRouter()

    @router.post("/conversations/{conversation_id}")
    async def send(conversation_id: str, prompt: Prompt):
        """
        Send a message to existing conversation
        """
        conversation = await get_conversation(conversation_id)
        message = await ai_service.send(prompt.message, conversation)
        return message

    @router.delete("/conversations/{conversation_id}")
    async def delete_conversation(conversation_id: str):
        """
        Delete the current conversation history to initiate a new conversation
        """
        conversation = await get_conversation(conversation_id)
        await manager.delete_conversation(conversation)

    @router.get("/conversations/{conversation_id}")
    async def get_conversation(conversation_id: str):
        """
        Retrieve the current conversation's messages
        """
        conversation = await manager.get_conversation(conversation_id)

        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return conversation

    @router.get("/conversations")
    async def get_conversations():
        """
        Retrieve all the conversations
        """
        conversations = await manager.get_conversations_ids()
        if conversations is None:
            raise HTTPException(status_code=404, detail="Conversations not found")

        return { "conversation_id_list": conversations }

    @router.put("/conversations")
    async def create_conversation(prompt: Prompt):
        """
        Create a new conversation with a starting message
        """
        conversation = await manager.create_conversation()
        await ai_service.send(prompt.message, conversation)
        return conversation

    api.include_router(router)
