"""
LangGraph Workflow Nodes for AI IT Helpdesk Agent.
Implements modular graph processing steps: classification, retrieval, tool execution, generation, and memory.
"""

import json
import re
from typing import Dict, Any, Optional

from config.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from agent.state import HelpdeskState
from agent.prompts import (
    INTENT_CLASSIFICATION_PROMPT,
    TOOL_SELECTION_PROMPT,
    TROUBLESHOOTING_SYSTEM_PROMPT,
    TOOL_RESPONSE_PROMPT,
    GENERAL_CHAT_PROMPT,
    CLARIFICATION_PROMPT,
)
from rag.retriever import retrieve_relevant_knowledge
from tools import TOOL_MAP
from memory.database import db


def get_llm():
    """Initializes and returns the ChatOllama client."""
    try:
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.1,
        )
    except Exception:
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.1,
        )


def _safe_call_llm(prompt: str) -> str:
    """Calls the Ollama LLM safely, returning error explanation if service is unavailable."""
    try:
        llm = get_llm()
        res = llm.invoke(prompt)
        return res.content if hasattr(res, "content") else str(res)
    except Exception as e:
        err_msg = str(e).lower()
        if "connection refused" in err_msg or "connect" in err_msg:
            return (
                "⚠️ **Ollama Service Unavailable**: Unable to connect to Ollama at `"
                f"{OLLAMA_BASE_URL}`. Please verify that the Ollama service is running locally (`ollama serve`) "
                f"and that model `{OLLAMA_MODEL}` is installed (`ollama pull {OLLAMA_MODEL}`)."
            )
        return f"⚠️ **LLM Error**: {str(e)}"


# ==========================================
# NODE 1: Classify Intent
# ==========================================
def classify_intent_node(state: HelpdeskState) -> Dict[str, Any]:
    """Classifies user query into troubleshooting, tool request, general chat, or unclear."""
    query = state.get("query", "").strip()

    if not query:
        return {
            "intent": "unclear",
            "status_message": "Empty query received",
            "response": "Please describe your IT issue or question so I can assist you.",
        }

    # Fast heuristic check for obvious basic tools to guarantee zero latency on simple commands
    lower_query = query.lower()
    if re.search(r"\b(time|what time is it|current time|date today)\b", lower_query):
        return {
            "intent": "tool_request",
            "tool_name": "current_time",
            "tool_input": "local",
            "status_message": "Classified intent: Tool Execution (current_time)",
        }
    if re.search(r"\b(internet connected|check internet|network status|check connection|ping check)\b", lower_query):
        return {
            "intent": "tool_request",
            "tool_name": "network_check",
            "tool_input": "8.8.8.8",
            "status_message": "Classified intent: Tool Execution (network_check)",
        }
    if re.search(r"\b(system info|os version|specs|ram info|cpu info|system specs)\b", lower_query):
        return {
            "intent": "tool_request",
            "tool_name": "system_info",
            "tool_input": "general",
            "status_message": "Classified intent: Tool Execution (system_info)",
        }
    if re.search(r"\b(calculate|multiplied by|divided by|\d+\s*[\+\-\*\/]\s*\d+)\b", lower_query):
        # Extract expression
        expr = re.sub(r"(calculate|what is|compute)", "", lower_query).strip()
        expr = expr.replace("multiplied by", "*").replace("times", "*").replace("divided by", "/").replace("plus", "+").replace("minus", "-")
        return {
            "intent": "tool_request",
            "tool_name": "calculator",
            "tool_input": expr or query,
            "status_message": "Classified intent: Tool Execution (calculator)",
        }
    if re.search(r"\b(count words|word count|how many words)\b", lower_query):
        text_match = re.sub(r"(count words in|count words|word count of|word count for)", "", query, flags=re.IGNORECASE).strip()
        return {
            "intent": "tool_request",
            "tool_name": "word_count",
            "tool_input": text_match or query,
            "status_message": "Classified intent: Tool Execution (word_count)",
        }

    # LLM-assisted classification for nuanced questions
    prompt = INTENT_CLASSIFICATION_PROMPT.format(query=query)
    raw_res = _safe_call_llm(prompt)

    intent = "it_troubleshooting"  # safe default for an IT helpdesk
    try:
        json_match = re.search(r"\{.*\}", raw_res, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            intent = data.get("intent", "it_troubleshooting")
    except Exception:
        # Fallback to keyword matching if json parsing fails
        if any(w in lower_query for w in ["hello", "hi", "hey", "who are you", "thanks", "thank you"]):
            intent = "general_chat"
        elif len(lower_query.split()) <= 1 and lower_query not in ["wifi", "printer", "network"]:
            intent = "unclear"
        else:
            intent = "it_troubleshooting"

    return {
        "intent": intent,
        "status_message": f"Classified intent: {intent.replace('_', ' ').title()}",
    }


# ==========================================
# NODE 2: Retrieve Knowledge (RAG)
# ==========================================
def retrieve_knowledge_node(state: HelpdeskState) -> Dict[str, Any]:
    """Retrieves relevant troubleshooting documents from local ChromaDB."""
    query = state.get("query", "")
    context_text, sources = retrieve_relevant_knowledge(query, top_k=4)

    return {
        "retrieved_docs": context_text,
        "sources": sources,
        "status_message": f"Retrieved {len(sources)} troubleshooting document(s) from knowledge base",
    }


# ==========================================
# NODE 3: Decide Tool
# ==========================================
def decide_tool_node(state: HelpdeskState) -> Dict[str, Any]:
    """Selects which diagnostic tool to invoke and prepares parameters."""
    tool_name = state.get("tool_name")
    tool_input = state.get("tool_input")

    # If already identified in heuristic classification, keep it
    if tool_name and tool_name in TOOL_MAP:
        return {
            "tool_name": tool_name,
            "tool_input": tool_input or "general",
            "status_message": f"Selected diagnostic tool: {tool_name}",
        }

    query = state.get("query", "")
    prompt = TOOL_SELECTION_PROMPT.format(query=query)
    raw_res = _safe_call_llm(prompt)

    selected_tool = "system_info"
    selected_arg = "general"

    try:
        json_match = re.search(r"\{.*\}", raw_res, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            selected_tool = data.get("tool_name", "system_info")
            selected_arg = data.get("tool_input", "general")
    except Exception:
        pass

    return {
        "tool_name": selected_tool,
        "tool_input": selected_arg,
        "status_message": f"Selected tool: {selected_tool}",
    }


# ==========================================
# NODE 4: Execute Tool
# ==========================================
def execute_tool_node(state: HelpdeskState) -> Dict[str, Any]:
    """Executes the selected safe diagnostic tool and captures output."""
    tool_name = state.get("tool_name")
    tool_input = state.get("tool_input", "")

    if not tool_name or tool_name not in TOOL_MAP:
        return {
            "tool_result": f"Error: Tool '{tool_name}' is not recognized or permitted.",
            "status_message": "Tool execution failed: unrecognized tool",
        }

    tool_fn = TOOL_MAP[tool_name]
    try:
        # LangChain tool invocation
        result = tool_fn.invoke(tool_input)
        result_str = str(result)
    except Exception as e:
        result_str = f"Diagnostic tool execution failed safely: {str(e)}"

    return {
        "tool_result": result_str,
        "status_message": f"Executed tool: {tool_name}",
    }


# ==========================================
# NODE 5: Generate Response
# ==========================================
def generate_response_node(state: HelpdeskState) -> Dict[str, Any]:
    """Synthesizes final answer according to the classified intent and retrieved data."""
    intent = state.get("intent", "general_chat")
    query = state.get("query", "")

    # Format recent history for context
    raw_history = state.get("chat_history", [])
    history_str = ""
    for msg in raw_history[-4:]:
        role = msg.get("role", "user").capitalize()
        content = msg.get("message", "")
        history_str += f"{role}: {content}\n"

    if intent == "it_troubleshooting":
        kb_docs = state.get("retrieved_docs", "No knowledge base documents found.")
        prompt = TROUBLESHOOTING_SYSTEM_PROMPT.format(
            knowledge_context=kb_docs,
            conversation_history=history_str or "No previous messages in current session.",
            query=query,
        )
        response = _safe_call_llm(prompt)

        # Ensure citation notice is included
        if "knowledge base" not in response.lower():
            response = (
                "ℹ️ *Troubleshooting guidance based on the IT Knowledge Base:*\n\n"
                + response
            )

    elif intent == "tool_request":
        tool_name = state.get("tool_name", "diagnostic_tool")
        tool_result = state.get("tool_result", "No output.")
        prompt = TOOL_RESPONSE_PROMPT.format(
            query=query,
            tool_name=tool_name,
            tool_result=tool_result,
        )
        response = _safe_call_llm(prompt)
        # If LLM failed, fallback to raw tool result directly
        if "⚠️" in response:
            response = f"Diagnostic Tool Result (`{tool_name}`):\n\n{tool_result}"

    elif intent == "unclear":
        prompt = CLARIFICATION_PROMPT.format(query=query)
        response = _safe_call_llm(prompt)
        if "⚠️" in response:
            response = (
                "I couldn't clearly identify the IT issue you are experiencing. "
                "Could you please specify: Are you experiencing a hardware problem (e.g., keyboard, mouse, printer, laptop overheating), "
                "a network issue (e.g., Wi-Fi, slow internet), or a software/login problem?"
            )

    else:  # general_chat
        prompt = GENERAL_CHAT_PROMPT.format(query=query)
        response = _safe_call_llm(prompt)
        if "⚠️" in response:
            response = (
                "Hello! I am your AI IT Helpdesk Support Agent. I can help troubleshoot hardware, "
                "software, network, and login issues using our local knowledge base, or run diagnostic tools."
            )

    return {
        "response": response,
        "status_message": "Response generated successfully",
    }


# ==========================================
# NODE 6: Save Memory
# ==========================================
def save_memory_node(state: HelpdeskState) -> Dict[str, Any]:
    """Persists user query and agent response into SQLite database."""
    user_id = state.get("user_id", "guest_user")
    session_id = state.get("session_id", "default_session")
    query = state.get("query", "")
    response = state.get("response", "")
    intent = state.get("intent")
    tool_used = state.get("tool_name")

    try:
        # Save user message
        db.save_message(
            user_id=user_id,
            session_id=session_id,
            role="user",
            message=query,
            intent=intent,
        )

        # Save assistant response
        meta = {
            "sources": state.get("sources", []),
            "tool_result": state.get("tool_result"),
        }
        db.save_message(
            user_id=user_id,
            session_id=session_id,
            role="assistant",
            message=response,
            intent=intent,
            tool_used=tool_used,
            metadata=meta,
        )
        status = "Conversation saved to SQLite database"
    except Exception as e:
        status = f"Memory save warning: {str(e)}"

    return {"status_message": status}
