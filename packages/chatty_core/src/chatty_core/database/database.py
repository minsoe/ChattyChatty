import os

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from chatty_core.models import Conversation

__all__ = ["init_mongodb", "BeanieConversation"]


async def init_mongodb():
    motor_client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    await init_beanie(
        database=motor_client.chatty,
        document_models=[BeanieConversation],
    )


class BeanieConversation(Conversation, Document):
    pass
