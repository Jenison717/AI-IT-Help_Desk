"""
Current Time Tool for LangChain.
Returns the current system date, time, and timezone in human-readable format.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class TimeInput(BaseModel):
    timezone_prompt: str = Field(
        default="local",
        description="Optional timezone format specifier or 'local'"
    )


@tool("current_time", args_schema=TimeInput)
def get_current_time(timezone_prompt: str = "local") -> str:
    """
    Returns the current local system date, time, and day of the week.
    Useful when users ask what time or day it is.
    """
    now = datetime.now()
    return now.strftime("Current Date and Time: %A, %B %d, %Y at %I:%M:%S %p (%Z)")
