import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.database.models import Conversation


async def init_mongodb():
    motor_client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    await init_beanie(motor_client.chatty, document_models=[Conversation])
