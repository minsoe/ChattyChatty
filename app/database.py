import os
from typing import Type, Optional
from beanie import init_beanie
from bson import ObjectId

from app.models import Conversation
from motor.motor_asyncio import AsyncIOMotorClient

async def init_mongodb():
    motor_client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    await init_beanie(motor_client.db_name, document_models=[Conversation])
