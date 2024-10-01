import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from app.database.conversation_manager import ConversationManager
from app.database.models import Conversation
from tests.mocks.mock_database import init_mock_database


class ConversationManagerTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await init_mock_database()

    @patch('app.database.models.Conversation.find_all')
    async def test_get_conversations_ids(self, mock_find_all):
        mock_conversations = [AsyncMock(id='123'), AsyncMock(id='456')]
        mock_find_all.return_value.to_list = AsyncMock(return_value=mock_conversations)

        manager = ConversationManager()
        conversations_ids = await manager.get_conversations_ids()
        assert conversations_ids is not None
        assert len(conversations_ids) == 2

    async def test_get_conversation_by_id(self):
        Conversation.get = AsyncMock()
        Conversation.get.return_value = AsyncMock(id='123')

        manager = ConversationManager()
        conversation = await manager.get_conversation("123")

        assert conversation is not None
        assert conversation.id == '123'


    async def test_delete_conversation(self):
        conversation = MagicMock(Conversation)

        manager = ConversationManager()
        await manager.delete_conversation(conversation)

        assert conversation.delete.called_once

    async def test_save_conversation(self):
        conversation = MagicMock(Conversation)

        manager = ConversationManager()
        await manager.save(conversation)

        assert conversation.save.called_once

    async def test_create_conversation(self):
        Conversation.insert_one = AsyncMock()

        create = AsyncMock()
        create.return_value = MagicMock(Conversation)
        Conversation.create = create

        manager = ConversationManager()
        manager._converstaion = MagicMock()
        conversation = await manager.create_conversation()

        assert conversation is not None

if __name__ == '__main__':
    unittest.main()
