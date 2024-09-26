from fastapi import APIRouter

from app.database.conversation_manager import ConversationManager
from app.open_ai.openai_service import OpenAIService
from app.api_services.prompt import Prompt

def conversation_routher() -> APIRouter:
    router = APIRouter()
    manager = ConversationManager()
    ai_service = OpenAIService()

    @router.post("/conversation")
    async def send(prompt: Prompt):
        await ai_service.send(prompt.value)

    @router.delete("/conversation")
    async def delete_conversation():
        await manager.delete_conversation()

    @router.get("/conversation")
    async def get_conversations():
        conversation = await manager.get_conversation()
        return conversation.messages

    return router