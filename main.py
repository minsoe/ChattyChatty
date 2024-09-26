from dotenv import load_dotenv
from app.api_services.conversation_router import conversation_routher
from app.database.database import init_mongodb
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    await init_mongodb()
    app.include_router(conversation_routher())
    yield

app = FastAPI(lifespan=lifespan)