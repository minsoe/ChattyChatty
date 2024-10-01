from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.database.models import Conversation


async def init_mock_database():
    client = AsyncMongoMockClient()
    await init_beanie(client.mocked_db, document_models=[Conversation])