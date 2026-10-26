"""
Streamlit Frontend Application for AI IT Helpdesk Agent.
Provides an interactive web chat UI with real-time status banners, session management, and diagnostics.
"""

import os
import sys
import uuid
import urllib.request
from datetime import datetime
import streamlit as st

# Ensure base directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import OLLAMA_MODEL, OLLAMA_BASE_URL, DATABASE_PATH, VECTOR_DB_PATH
from memory.database import db
from rag.vector_store import is_vector_store_ready
from agent.graph import run_agent

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="AI IT Helpdesk Agent",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for polished look
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .status-ready { background-color: #DEF7EC; color: #03543F; }
    .status-warning { background-color: #FEF08A; color: #854D0E; }
    .status-danger { background-color: #FEE2E2; color: #991B1B; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------
# Health Check Helpers
# ----------------------------------------------------
def check_ollama_health() -> bool:
    """Checks if Ollama server responds on configured base URL."""
    try:
        url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/tags"
        req = urllib.request.Request(url, headers={"User-Agent": "HelpdeskAgent/1.0"})
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False


# ----------------------------------------------------
# Session State Initialization
# ----------------------------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = "student001"

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_status" not in st.session_state:
    st.session_state.agent_status = "Ready for inquiries"


def load_conversation_history(session_id: str):
    """Loads chat messages from SQLite for the selected session."""
    raw_history = db.get_session_history(session_id)
    formatted = []
    for row in raw_history:
        formatted.append({
            "role": row["role"],
            "content": row["message"],
            "intent": row.get("intent"),
            "tool_used": row.get("tool_used"),
            "metadata": row.get("metadata", {}),
            "timestamp": row.get("timestamp"),
        })
    st.session_state.messages = formatted


# Initialize from DB if empty
if not st.session_state.messages:
    load_conversation_history(st.session_state.session_id)


# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------
with st.sidebar:
    st.header("⚙️ Agent Controls")

    # User ID input
    new_user_id = st.text_input("User ID", value=st.session_state.user_id)
    if new_user_id != st.session_state.user_id and new_user_id.strip():
        st.session_state.user_id = new_user_id.strip()
        st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
        st.session_state.messages = []
        st.rerun()

    # New Conversation Button
    if st.button("➕ New Conversation", use_container_width=True):
        st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
        st.session_state.messages = []
        st.session_state.agent_status = "New session started"
        st.rerun()

    st.divider()

    # System Status Panel
    st.subheader("🖥️ System Diagnostics")
    ollama_ok = check_ollama_health()
    vector_ok = is_vector_store_ready(VECTOR_DB_PATH)
    db_ok = os.path.exists(DATABASE_PATH)

    if ollama_ok:
        st.markdown("🟢 **Ollama LLM**: Connected (`" + OLLAMA_MODEL + "`)")
    else:
        st.markdown("🔴 **Ollama LLM**: Disconnected")
        st.caption("Run: `ollama serve` and `ollama pull " + OLLAMA_MODEL + "`")

    if vector_ok:
        st.markdown("🟢 **Vector DB**: Ready (ChromaDB)")
    else:
        st.markdown("🟡 **Vector DB**: Not Initialized")
        st.caption("Run: `python scripts/build_vector_db.py`")

    if db_ok:
        st.markdown("🟢 **SQLite Memory**: Active")
    else:
        st.markdown("🟢 **SQLite Memory**: Initializing")

    st.divider()

    # Previous Conversations
    st.subheader("📜 Previous Conversations")
    user_sessions = db.get_user_sessions(st.session_state.user_id)

    if user_sessions:
        for s in user_sessions[:10]:
            sid = s["session_id"]
            title = s["title"] or f"Session {sid[:6]}"
            is_current = sid == st.session_state.session_id
            label = f"{'👉 ' if is_current else ''}{title}"
            if st.button(label, key=f"session_{sid}", use_container_width=True):
                st.session_state.session_id = sid
                load_conversation_history(sid)
                st.rerun()
    else:
        st.caption("No prior sessions logged for this User ID.")

    st.divider()

    # Clear Conversation Button
    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        db.clear_session(st.session_state.session_id)
        st.session_state.messages = []
        st.rerun()


# ----------------------------------------------------
# Main Chat Area
# ----------------------------------------------------
st.markdown('<div class="main-title">🛠️ AI IT Helpdesk Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Agentic AI powered technical support assistant • LangGraph • RAG • Safe Tools</div>',
    unsafe_allow_html=True,
)

# Agent Status Display (Safe high-level statuses only)
status_container = st.empty()
status_container.info(f"⚡ **Agent Status:** {st.session_state.agent_status}")

# Display Past Messages
for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role):
        st.markdown(msg["content"])

        # Display citations if available
        meta = msg.get("metadata", {})
        sources = meta.get("sources", [])
        if sources:
            with st.expander("📚 Knowledge Base Citations", expanded=False):
                for src in sources:
                    st.markdown(f"- **{src.get('title')}** (`{src.get('source')}`) — Category: *{src.get('category')}*")

        # Display tool result badge if used
        tool_used = msg.get("tool_used")
        if tool_used:
            st.caption(f"🔧 *Resolved using diagnostic tool: `{tool_used}`*")


# ----------------------------------------------------
# User Input Processing
# ----------------------------------------------------
user_prompt = st.chat_input("Describe your IT issue, or ask a question (e.g., 'My Wi-Fi is disconnected', 'What time is it?', '25 * 4')...")

if user_prompt:
    clean_prompt = user_prompt.strip()

    if not clean_prompt:
        st.warning("Please type an IT question or technical issue.")
    else:
        # Add user message to UI immediately
        st.session_state.messages.append({"role": "user", "content": clean_prompt})
        with st.chat_message("user"):
            st.markdown(clean_prompt)

        # Status update callback for LangGraph
        def update_status_callback(status: str):
            st.session_state.agent_status = status
            status_container.info(f"⚡ **Agent Status:** {status}")

        # Assistant placeholder
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_placeholder.markdown("*(Thinking and analyzing problem...)*")

            try:
                update_status_callback("Understanding query...")

                # Execute LangGraph Workflow
                final_state = run_agent(
                    query=clean_prompt,
                    user_id=st.session_state.user_id,
                    session_id=st.session_state.session_id,
                    chat_history=st.session_state.messages,
                    status_callback=update_status_callback,
                )

                response_text = final_state.get(
                    "response",
                    "I processed your request, but could not generate a response. Please try rephrasing.",
                )
                sources = final_state.get("sources", [])
                tool_used = final_state.get("tool_name")

                # Render final response
                response_placeholder.markdown(response_text)

                if sources:
                    with st.expander("📚 Knowledge Base Citations", expanded=False):
                        for src in sources:
                            st.markdown(f"- **{src.get('title')}** (`{src.get('source')}`) — Category: *{src.get('category')}*")

                if tool_used:
                    st.caption(f"🔧 *Resolved using diagnostic tool: `{tool_used}`*")

                # Update session state messages
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "intent": final_state.get("intent"),
                    "tool_used": tool_used,
                    "metadata": {"sources": sources, "tool_result": final_state.get("tool_result")},
                })

                update_status_callback("Ready for inquiries")

            except Exception as e:
                err_message = (
                    f"⚠️ **An error occurred during agent execution:** {str(e)}\n\n"
                    "Please make sure that:\n"
                    "1. Ollama is running (`ollama serve`)\n"
                    f"2. The model is pulled (`ollama pull {OLLAMA_MODEL}`)\n"
                    "3. Vector database has been indexed (`python scripts/build_vector_db.py`)"
                )
                response_placeholder.markdown(err_message)
                update_status_callback(f"Execution halted: {str(e)}")
