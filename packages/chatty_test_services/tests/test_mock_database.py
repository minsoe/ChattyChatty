from __future__ import annotations

from beanie import Document

from chatty_test_services.mocks import init_mock_database


class SampleDocument(Document):
    name: str


class TestMockDatabase:
    async def test_mock_database(self):
        client = await init_mock_database(document_models=[SampleDocument])
        assert client is not None
