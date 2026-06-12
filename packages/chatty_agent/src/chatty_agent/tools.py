from __future__ import annotations

import datetime

from langchain_core.tools import tool

__all__ = ["get_current_datetime", "TOOL_MAPPING"]


@tool
def get_current_datetime() -> str:
    """Get the current date and time."""
    return str(datetime.datetime.now())


TOOL_MAPPING = {
    "datetime": get_current_datetime,
}
