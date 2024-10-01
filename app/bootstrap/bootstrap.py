from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI

from app.api_services.conversation_router import init_conversation_router
from app.database.conversation_manager import ConversationManager
from app.database.database import init_mongodb
from app.open_ai.openai_service import OpenAIService


async def bootstrap(api: FastAPI):
    load_dotenv()
    await init_mongodb()

    manager = ConversationManager()
    ai_service = OpenAIService(OpenAI(), manager)
    init_conversation_router(api, manager, ai_service)
