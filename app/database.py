import os
from typing import Type, Optional
from beanie import init_beanie
from bson import ObjectId

from app.models import Conversation
from motor.motor_asyncio import AsyncIOMotorClient

async def init_mongodb():
    motor_client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
    db = motor_client['chatty_chatty']
    await init_beanie(db, document_models=[Type[Conversation]])


async def find_conversation_by_id(conversation_id: Optional[str]) -> Optional[Conversation]:
    conversation = await Conversation.get(ObjectId(conversation_id))
    if conversation:
        return conversation
    return None
