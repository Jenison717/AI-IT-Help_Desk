#!/usr/bin/env python3
"""
Script to build and initialize the ChromaDB Vector Database for the AI IT Helpdesk Agent.
Usage:
    python scripts/build_vector_db.py
"""

import sys
import os
from pathlib import Path

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from rag.vector_store import build_vector_store
from config.config import KNOWLEDGE_BASE_DIR, VECTOR_DB_PATH


def main():
    print("=" * 65)
    print("  AI IT Helpdesk Agent - Vector Database Build Script")
    print("=" * 65)
    print(f"Knowledge Base Source Directory: {KNOWLEDGE_BASE_DIR}")
    print(f"Vector Database Target Path:     {VECTOR_DB_PATH}")
    print("-" * 65)

    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        print(f"Error: Knowledge base directory '{KNOWLEDGE_BASE_DIR}' does not exist.")
        sys.exit(1)

    try:
        chunk_count = build_vector_store(
            kb_dir=KNOWLEDGE_BASE_DIR,
            db_path=VECTOR_DB_PATH,
        )
        print("-" * 65)
        print(f"SUCCESS: ChromaDB vector store built successfully!")
        print(f"Total chunks indexed: {chunk_count}")
        print("You can now run the Streamlit application: streamlit run app.py")
        print("=" * 65)
    except Exception as e:
        print(f"\nBUILD FAILED: An error occurred while creating vector store:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
