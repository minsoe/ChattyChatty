from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI

from app.api_services.conversation_router import init_conversation_router
from app.database.conversation_manager import ConversationManager
from app.database.database import init_mongodb
from app.open_ai.openai_service import OpenAIService



@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    await init_mongodb()

    manager = ConversationManager()
    ai_service = OpenAIService(OpenAI(), manager)
    init_conversation_router(app, manager, ai_service)
    yield


app = FastAPI(lifespan=lifespan)
