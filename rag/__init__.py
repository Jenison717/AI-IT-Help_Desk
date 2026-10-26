"""
RAG package initialization.
Exports loader, vector store, embeddings, and retrieval utilities.
"""

from rag.document_loader import load_knowledge_documents, split_documents
from rag.vector_store import build_vector_store, get_vector_store, is_vector_store_ready
from rag.retriever import retrieve_relevant_knowledge

__all__ = [
    "load_knowledge_documents",
    "split_documents",
    "build_vector_store",
    "get_vector_store",
    "is_vector_store_ready",
    "retrieve_relevant_knowledge",
]
