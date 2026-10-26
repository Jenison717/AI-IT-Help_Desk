"""
Vector Store Management Module for RAG.
Initializes, saves, and queries the local ChromaDB vector database.
"""

import os
from typing import Optional, List
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from config.config import VECTOR_DB_PATH, KNOWLEDGE_BASE_DIR
from rag.document_loader import load_knowledge_documents, split_documents
from rag.embeddings import get_embedding_function

COLLECTION_NAME = "it_helpdesk_knowledge"


def is_vector_store_ready(db_path: str = VECTOR_DB_PATH) -> bool:
    """Checks if the Chroma vector store directory exists and contains data."""
    p = Path(db_path)
    if not p.exists():
        return False
    # Check for sqlite3 or parquet files inside the Chroma directory
    files = list(p.glob("*"))
    return len(files) > 0


def get_vector_store(
    db_path: str = VECTOR_DB_PATH,
    collection_name: str = COLLECTION_NAME,
) -> Optional[Chroma]:
    """Loads an existing Chroma vector store instance."""
    if not is_vector_store_ready(db_path):
        return None

    try:
        embeddings = get_embedding_function()
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=db_path,
        )
        return vector_store
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None


def build_vector_store(
    kb_dir: str = KNOWLEDGE_BASE_DIR,
    db_path: str = VECTOR_DB_PATH,
    collection_name: str = COLLECTION_NAME,
) -> int:
    """
    Loads knowledge documents, chunks them, computes embeddings,
    and builds/persists the Chroma vector database. Returns total chunk count.
    """
    print(f"-> Loading knowledge documents from: {kb_dir}")
    raw_docs = load_knowledge_documents(kb_dir)
    if not raw_docs:
        raise ValueError(f"No valid markdown or text documents found in '{kb_dir}'")

    print(f"-> Loaded {len(raw_docs)} documents. Splitting into semantic chunks...")
    chunks: List[Document] = split_documents(raw_docs)
    print(f"-> Created {len(chunks)} chunks.")

    print(f"-> Initializing embeddings and generating vectors...")
    embeddings = get_embedding_function()

    os.makedirs(db_path, exist_ok=True)
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=db_path,
    )
    # Chroma >= 0.4 automatically persists, but explicit call for older versions
    if hasattr(vector_store, "persist"):
        vector_store.persist()

    print(f"-> Successfully indexed {len(chunks)} chunks into ChromaDB at: {db_path}")
    return len(chunks)
