from __future__ import annotations

from unittest.mock import MagicMock

__all__ = ["mock_ai"]


def mock_ai():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "mocked ai response"

    mocked_client = MagicMock()
    mocked_client.chat.completions.create.return_value = mock_response
    return mocked_client
