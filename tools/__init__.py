"""
Tools module for the AI IT Helpdesk Agent.
Exports all LangChain diagnostic tools and tool registry.
"""

from tools.calculator import calculate
from tools.time_tool import get_current_time
from tools.network_tool import check_network_connectivity
from tools.word_count import count_words
from tools.system_info import get_system_information

# Registry of all available tools
AVAILABLE_TOOLS = [
    calculate,
    get_current_time,
    check_network_connectivity,
    count_words,
    get_system_information,
]

TOOL_MAP = {tool.name: tool for tool in AVAILABLE_TOOLS}

__all__ = [
    "calculate",
    "get_current_time",
    "check_network_connectivity",
    "count_words",
    "get_system_information",
    "AVAILABLE_TOOLS",
    "TOOL_MAP",
]
