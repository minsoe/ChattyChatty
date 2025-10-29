from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from chattychatty.database.models import BeanieConversation


async def init_mock_database():
    client = AsyncMongoMockClient()
    await init_beanie(client.mocked_db, document_models=[BeanieConversation])
    return client
