"""
LangGraph Agent State Definition for AI IT Helpdesk.
Defines the typed dictionary that flows through all graph nodes.
"""

from typing import TypedDict, List, Dict, Any, Optional


class HelpdeskState(TypedDict, total=False):
    """Represents the shared mutable state across all LangGraph nodes."""

    # User & Session Identifiers
    user_id: str
    session_id: str

    # User Query & Classification
    query: str
    intent: str  # 'it_troubleshooting', 'tool_request', 'general_chat', 'unclear'

    # Tool Execution State
    tool_name: Optional[str]
    tool_input: Optional[str]
    tool_result: Optional[str]

    # RAG Knowledge Retrieval State
    retrieved_docs: Optional[str]
    sources: List[Dict[str, Any]]

    # Response & Status
    response: Optional[str]
    status_message: str

    # Conversation History & Context
    chat_history: List[Dict[str, Any]]
    cross_session_context: Optional[str]

    # Error handling
    error: Optional[str]
