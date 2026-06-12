import unittest
from unittest import IsolatedAsyncioTestCase

from chatty_core.conversations.beanie_conversation_manager import (
    BeanieConversationManager,
)
from chatty_core.database import BeanieConversation
from chatty_core.models import Message, Role
from chatty_test_services.mocks.mock_database import init_mock_database


class TestConversationManager(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = await init_mock_database([BeanieConversation])

    async def asyncTearDown(self):
        await BeanieConversation.get_motor_collection().drop()

    async def test_get_conversations_ids(self):
        c1 = await BeanieConversation().create()
        c2 = await BeanieConversation().create()

        manager = BeanieConversationManager()
        conversations_ids = await manager.get_conversations_ids()

        assert conversations_ids is not None
        assert len(conversations_ids) == 2
        assert str(c1.id) in conversations_ids
        assert str(c2.id) in conversations_ids

    async def test_get_conversation_by_id(self):
        new_conversation = BeanieConversation()
        await new_conversation.create()

        manager = BeanieConversationManager()
        conversation = await manager.get_conversation(str(new_conversation.id))

        assert conversation is not None
        assert conversation.id == new_conversation.id

    async def test_delete_conversation(self):
        new_conversation = BeanieConversation()
        await new_conversation.create()

        manager = BeanieConversationManager()
        await manager.delete_conversation(str(new_conversation.id))

        conversation = await manager.get_conversation(str(new_conversation.id))
        assert conversation is None

    async def test_save_conversation(self):
        new_conversation = BeanieConversation()
        message = Message(role=Role.USER, content="testing")
        new_conversation.messages = [message]
        manager = BeanieConversationManager()
        await manager.save(new_conversation)

        conversation = await manager.get_conversation(str(new_conversation.id))
        assert conversation is not None
        assert len(conversation.messages) == 1
        assert conversation.messages[0] == message
        assert conversation.id == new_conversation.id

    async def test_create_conversation(self):
        manager = BeanieConversationManager()
        conversation = await manager.create_conversation()

        assert conversation is not None
