"""
Persistent SQLite Memory Storage for AI IT Helpdesk Agent.
Manages user conversations, sessions, message history, and agent state.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from config.config import DATABASE_PATH


class HelpdeskDatabase:
    """Manages SQLite persistent memory operations for the helpdesk agent."""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a connection to the SQLite database with row factory enabled."""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Initializes database tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Conversations/Messages table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    intent TEXT,
                    tool_used TEXT,
                    metadata TEXT,
                    timestamp TEXT NOT NULL
                )
                """
            )

            # Sessions table for metadata and tracking
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

            # Indexes for high performance
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_user_id ON conversation_history(user_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_session_id ON conversation_history(session_id)"
            )
            conn.commit()

    def save_message(
        self,
        user_id: str,
        session_id: str,
        role: str,
        message: str,
        intent: Optional[str] = None,
        tool_used: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Saves a single chat message with associated state metadata into SQLite.
        Ensures sessions table is also updated.
        """
        now_str = datetime.now().isoformat()
        meta_json = json.dumps(metadata) if metadata else None

        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Insert message
            cursor.execute(
                """
                INSERT INTO conversation_history 
                (user_id, session_id, role, message, intent, tool_used, metadata, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, session_id, role, message, intent, tool_used, meta_json, now_str),
            )
            msg_id = cursor.lastrowid

            # Upsert session record
            cursor.execute(
                """
                INSERT INTO user_sessions (session_id, user_id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET 
                    updated_at = excluded.updated_at
                """,
                (
                    session_id,
                    user_id,
                    message[:40] + ("..." if len(message) > 40 else ""),
                    now_str,
                    now_str,
                ),
            )
            conn.commit()
            return msg_id or 0

    def get_session_history(self, session_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves messages for a given session sorted chronologically."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, user_id, session_id, role, message, intent, tool_used, metadata, timestamp
                FROM conversation_history
                WHERE session_id = ?
                ORDER BY id ASC
                LIMIT ?
                """,
                (session_id, limit),
            )
            rows = cursor.fetchall()
            results = []
            for row in rows:
                meta = json.loads(row["metadata"]) if row["metadata"] else {}
                results.append(
                    {
                        "id": row["id"],
                        "user_id": row["user_id"],
                        "session_id": row["session_id"],
                        "role": row["role"],
                        "message": row["message"],
                        "intent": row["intent"],
                        "tool_used": row["tool_used"],
                        "metadata": meta,
                        "timestamp": row["timestamp"],
                    }
                )
            return results

    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves all sessions belonging to a user."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT session_id, user_id, title, created_at, updated_at
                FROM user_sessions
                WHERE user_id = ?
                ORDER BY updated_at DESC
                """,
                (user_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_user_recent_context(
        self, user_id: str, exclude_session: Optional[str] = None, limit: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Retrieves recent interactions across prior sessions for cross-session context memory.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if exclude_session:
                cursor.execute(
                    """
                    SELECT role, message, intent, timestamp
                    FROM conversation_history
                    WHERE user_id = ? AND session_id != ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (user_id, exclude_session, limit),
                )
            else:
                cursor.execute(
                    """
                    SELECT role, message, intent, timestamp
                    FROM conversation_history
                    WHERE user_id = ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (user_id, limit),
                )
            rows = cursor.fetchall()
            return [dict(row) for row in reversed(rows)]

    def clear_session(self, session_id: str) -> None:
        """Deletes all messages for a specific session."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversation_history WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM user_sessions WHERE session_id = ?", (session_id,))
            conn.commit()


# Singleton instance
db = HelpdeskDatabase()
