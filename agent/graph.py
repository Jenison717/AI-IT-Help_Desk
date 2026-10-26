"""
LangGraph Agent Workflow Definition for AI IT Helpdesk.
Builds the routing graph connecting Intent Classification, RAG, Tools, Generation, and Memory.
"""

from typing import Dict, Any, Callable, Optional, List
from langgraph.graph import StateGraph, START, END

from agent.state import HelpdeskState
from agent.nodes import (
    classify_intent_node,
    retrieve_knowledge_node,
    decide_tool_node,
    execute_tool_node,
    generate_response_node,
    save_memory_node,
)


def route_intent(state: HelpdeskState) -> str:
    """Conditional routing edge function based on classified user intent."""
    intent = state.get("intent", "general_chat")

    if intent == "it_troubleshooting":
        return "retrieve_knowledge"
    elif intent == "tool_request":
        return "decide_tool"
    else:  # general_chat or unclear
        return "generate_response"


def build_helpdesk_graph():
    """Constructs and compiles the complete LangGraph agent workflow."""
    workflow = StateGraph(HelpdeskState)

    # Add Nodes
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("retrieve_knowledge", retrieve_knowledge_node)
    workflow.add_node("decide_tool", decide_tool_node)
    workflow.add_node("execute_tool", execute_tool_node)
    workflow.add_node("generate_response", generate_response_node)
    workflow.add_node("save_memory", save_memory_node)

    # Connect Edges
    workflow.add_edge(START, "classify_intent")

    # Conditional Branching from intent classification
    workflow.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "retrieve_knowledge": "retrieve_knowledge",
            "decide_tool": "decide_tool",
            "generate_response": "generate_response",
        },
    )

    # RAG Branch
    workflow.add_edge("retrieve_knowledge", "generate_response")

    # Tool Execution Branch
    workflow.add_edge("decide_tool", "execute_tool")
    workflow.add_edge("execute_tool", "generate_response")

    # Response & Memory Persistence
    workflow.add_edge("generate_response", "save_memory")
    workflow.add_edge("save_memory", END)

    return workflow.compile()


# Compile reusable agent graph
helpdesk_app = build_helpdesk_graph()


def run_agent(
    query: str,
    user_id: str = "student001",
    session_id: str = "default_session",
    chat_history: Optional[List[Dict[str, Any]]] = None,
    status_callback: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    """
    Executes the helpdesk agent graph step-by-step for a given user query.
    Supports a real-time status callback to update UI status banners.
    """
    initial_state: HelpdeskState = {
        "user_id": user_id,
        "session_id": session_id,
        "query": query,
        "intent": "it_troubleshooting",
        "chat_history": chat_history or [],
        "sources": [],
        "status_message": "Understanding query...",
    }

    current_state = dict(initial_state)

    # Stream through nodes to trigger live UI status updates
    for output in helpdesk_app.stream(current_state):
        for node_name, node_state in output.items():
            current_state.update(node_state)
            status_msg = node_state.get("status_message")
            if status_msg and status_callback:
                status_callback(status_msg)

    return current_state
