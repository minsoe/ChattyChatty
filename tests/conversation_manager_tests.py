import unittest

from app.database.conversation_manager import ConversationManager
from app.database.models import Conversation
from tests.mocks.mock_database import init_mock_database


class ConversationManagerTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.client = await init_mock_database()

    async def asyncTearDown(self):
        await Conversation.get_motor_collection().drop()

    async def test_get_conversations_ids(self):
        await Conversation().create()
        await Conversation().create()

        manager = ConversationManager()
        conversations_ids = await manager.get_conversations_ids()

        assert conversations_ids is not None
        assert len(conversations_ids) == 2

    async def test_get_conversation_by_id(self):
        new_conversation = Conversation()
        await new_conversation.create()

        manager = ConversationManager()
        conversation = await manager.get_conversation(str(new_conversation.id))

        assert conversation is not None
        assert conversation.id == new_conversation.id

    async def test_delete_conversation(self):
        new_conversation = Conversation()
        await new_conversation.create()

        manager = ConversationManager()
        await manager.delete_conversation(new_conversation)

        conversation = await manager.get_conversation(str(new_conversation.id))
        assert conversation is None

    async def test_save_conversation(self):
        new_conversation = Conversation()

        manager = ConversationManager()
        await manager.save(new_conversation)

        conversation = await manager.get_conversation(str(new_conversation.id))
        assert conversation is not None
        assert conversation.id == new_conversation.id

    async def test_create_conversation(self):
        manager = ConversationManager()
        conversation = await manager.create_conversation()

        assert conversation is not None


if __name__ == '__main__':
    unittest.main()
