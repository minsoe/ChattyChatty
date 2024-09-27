from fastapi import APIRouter, FastAPI

from app.api_services.request_models.prompt import Prompt
from app.database.conversation_manager import ConversationManager
from app.open_ai.openai_service import OpenAIService


def init_conversation_router(api: FastAPI, manager: ConversationManager,
                             ai_service: OpenAIService):
    router = APIRouter()

    @router.post("/conversation")
    async def send(prompt: Prompt):
        """
        Send a message to start or continue the conversation with AI
        """
        await ai_service.send(prompt.message)

    @router.delete("/conversation")
    async def delete_conversation():
        """
        Delete the current conversation history to initiate a new conversation
        """
        await manager.delete_conversation()

    @router.get("/conversation")
    async def get_conversations():
        """
        Retrieve the current conversation's messages
        """
        conversation = await manager.get_conversation()
        return conversation.messages

    api.include_router(router)
