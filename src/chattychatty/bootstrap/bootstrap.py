from dotenv import load_dotenv
from fastapi import FastAPI

from chattychatty.api_services import conversation_router
from chattychatty.database.database import init_mongodb

__all__ = ["bootstrap"]


async def bootstrap(api: FastAPI):
    load_dotenv()
    await init_mongodb()

    api.include_router(conversation_router.router)
