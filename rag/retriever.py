"""
Retriever Module for RAG Pipeline.
Performs semantic similarity search against the ChromaDB vector store and formats context.
"""

from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from rag.vector_store import get_vector_store


def retrieve_relevant_knowledge(
    query: str, top_k: int = 4
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Retrieves the most relevant troubleshooting documents for a given query.
    Returns:
        - formatted_context (str): Ready to inject into LLM prompt
        - sources (List[dict]): List of metadata sources for citation
    """
    vector_store = get_vector_store()
    if vector_store is None:
        return (
            "Knowledge base vector store has not been initialized. "
            "Please run 'python scripts/build_vector_db.py'.",
            [],
        )

    try:
        # Retrieve top documents with similarity search
        docs_with_scores = vector_store.similarity_search_with_relevance_scores(query, k=top_k)
    except Exception:
        # Fallback to standard similarity search if relevance scoring isn't supported by embedding
        docs = vector_store.similarity_search(query, k=top_k)
        docs_with_scores = [(d, 1.0) for d in docs]

    if not docs_with_scores:
        return "No relevant troubleshooting procedures found in knowledge base.", []

    formatted_chunks = []
    sources = []

    for idx, (doc, score) in enumerate(docs_with_scores, 1):
        src = doc.metadata.get("source", "knowledge_base.md")
        title = doc.metadata.get("title", "IT Troubleshooting Procedure")
        category = doc.metadata.get("category", "General")

        formatted_chunks.append(
            f"--- KNOWLEDGE DOC #{idx} [{title} | Category: {category} | File: {src}] ---\n"
            f"{doc.page_content.strip()}\n"
        )
        sources.append(
            {
                "title": title,
                "source": src,
                "category": category,
                "score": round(score, 3) if isinstance(score, (int, float)) else None,
            }
        )

    formatted_context = "\n".join(formatted_chunks)
    return formatted_context, sources
