import unittest
from unittest.mock import AsyncMock, MagicMock

from beanie.odm.interfaces.find import FindInterface

from app.conversation_manager import ConversationManager
from app.models import Conversation


class MyTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_get_conversation_when_no_existing_converstation(self):
        find_one = AsyncMock()
        find_one.return_value = None
        Conversation.find_one = find_one

        manager = ConversationManager()

        create_conversation = MagicMock()
        create_conversation.return_value = MagicMock(Conversation)
        manager.create_conversation = create_conversation

        Conversation.insert_one = AsyncMock()

        await manager.get_conversation()

        Conversation.find_one.assert_called_once()
        manager.create_conversation.assert_called_once()
        Conversation.insert_one.assert_called_once()

    async def test_get_conversation_when_with_existing_converstation(self):
        find_one = AsyncMock()
        find_one.return_value = MagicMock(Conversation)
        Conversation.find_one = find_one

        manager = ConversationManager()

        manager.create_conversation = MagicMock()
        manager.insert = AsyncMock()

        await manager.get_conversation()

        Conversation.find_one.assert_called_once()
        manager.create_conversation.assert_not_called()
        manager.insert.assert_not_called()

    async def test_delete_conversation(self):
        Conversation.delete_all = AsyncMock()
        manager = ConversationManager()
        await manager.delete_conversation()

        Conversation.delete_all.assert_called_once()



if __name__ == '__main__':
    unittest.main()
