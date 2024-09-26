import os

from beanie import init_beanie
from app.models import Conversation
from motor.motor_asyncio import AsyncIOMotorClient

async def init_mongodb():
    motor_client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    await init_beanie(motor_client.chatty, document_models=[Conversation])
