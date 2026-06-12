from __future__ import annotations

from typing import List

from beanie import Document, View, init_beanie
from mongomock_motor import AsyncMongoMockClient

__all__ = ["init_mock_database"]


async def init_mock_database(document_models: List[type[Document] | type[View] | str]):
    client = AsyncMongoMockClient()
    await init_beanie(client.mocked_db, document_models=document_models)
    return client
