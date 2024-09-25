import os
from typing import Type
from beanie import init_beanie

from app.models import Conversation
from motor.motor_asyncio import AsyncIOMotorClient

async def init_mongodb():
    motor_client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    db = motor_client['chatty_chatty']
    await init_beanie(db, document_models=[Type[Conversation]])