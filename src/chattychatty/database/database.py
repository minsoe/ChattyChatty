import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from chattychatty.database.models import BeanieConversation


async def init_mongodb():
    motor_client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    await init_beanie(
        database=motor_client.chatty,
        document_models=[BeanieConversation],
    )
