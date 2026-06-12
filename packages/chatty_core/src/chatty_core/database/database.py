from __future__ import annotations

import os

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from chatty_core.models import Agent, Conversation

__all__ = ["init_mongodb", "BeanieConversation", "BeanieAgent"]


async def init_mongodb():
    motor_client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    await init_beanie(
        database=motor_client.chatty,
        document_models=[BeanieConversation, BeanieAgent],
    )


class BeanieConversation(Conversation, Document):
    pass


class BeanieAgent(Agent, Document):
    pass
