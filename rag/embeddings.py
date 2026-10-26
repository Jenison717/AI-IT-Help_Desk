"""
Embeddings Provider Module for RAG.
Provides vector embeddings using Ollama or HuggingFace with robust fallback.
"""

from typing import Any
from config.config import OLLAMA_MODEL, OLLAMA_BASE_URL, EMBEDDING_MODEL_NAME


def get_embedding_function() -> Any:
    """
    Returns an embeddings model instance.
    First attempts HuggingFace sentence-transformers (fast, local, deterministic, offline),
    then falls back to OllamaEmbeddings if HuggingFace is not installed.
    """
    try:
        from langchain_huggingface import HuggingFaceEmbeddings

        # Uses standard lightweight CPU-friendly embedding model
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    except Exception:
        pass

    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    except Exception:
        pass

    # Fallback to OllamaEmbeddings
    try:
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
        )
    except Exception:
        from langchain_community.embeddings import OllamaEmbeddings

        return OllamaEmbeddings(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
        )
