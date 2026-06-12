from __future__ import annotations

from chatty_core.database.database import init_mongodb
from dotenv import load_dotenv
from fastapi import FastAPI

from chatty_api.agent_services import agent_router
from chatty_api.conversation_services import conversation_router

__all__ = ["bootstrap"]


async def bootstrap(api: FastAPI):
    load_dotenv()
    await init_mongodb()
    api.include_router(conversation_router.router)
    api.include_router(agent_router.router)
