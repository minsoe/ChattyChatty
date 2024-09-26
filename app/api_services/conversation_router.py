from fastapi import APIRouter, FastAPI

from app.api_services.prompt import Prompt
from app.database.conversation_manager import ConversationManager
from app.open_ai.openai_service import OpenAIService


def init_conversation_router(api: FastAPI, manager: ConversationManager,
                             ai_service: OpenAIService):
    router = APIRouter()

    @router.post("/conversation")
    async def send(prompt: Prompt):
        await ai_service.send(prompt.message)

    @router.delete("/conversation")
    async def delete_conversation():
        await manager.delete_conversation()

    @router.get("/conversation")
    async def get_conversations():
        conversation = await manager.get_conversation()
        return conversation.messages

    api.include_router(router)
