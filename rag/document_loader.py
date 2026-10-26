"""
Document Loader and Chunking Module for RAG.
Reads Markdown and text files from the knowledge_base directory and splits them into clean chunks.
"""

import os
import re
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.config import KNOWLEDGE_BASE_DIR


def extract_metadata_from_markdown(content: str, file_path: str) -> dict:
    """Extracts title, category, and keywords from markdown document headers."""
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    category_match = re.search(r"^##\s+Category:\s*(.+)$", content, re.MULTILINE)
    keywords_match = re.search(r"\*\*Keywords\*\*:\s*(.+)$", content, re.MULTILINE)

    title = title_match.group(1).strip() if title_match else Path(file_path).stem.replace("_", " ").title()
    category = category_match.group(1).strip() if category_match else "General IT Support"
    keywords = keywords_match.group(1).strip() if keywords_match else ""

    return {
        "source": os.path.basename(file_path),
        "file_path": file_path,
        "title": title,
        "category": category,
        "keywords": keywords,
    }


def load_knowledge_documents(directory_path: str = KNOWLEDGE_BASE_DIR) -> List[Document]:
    """
    Reads all .md and .txt files from the knowledge base directory
    and returns a list of Document objects with extracted metadata.
    """
    documents: List[Document] = []
    kb_path = Path(directory_path)

    if not kb_path.exists():
        os.makedirs(kb_path, exist_ok=True)
        return documents

    for file_path in kb_path.glob("**/*"):
        if file_path.suffix.lower() in [".md", ".txt"]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_text = f.read()

                meta = extract_metadata_from_markdown(raw_text, str(file_path))
                doc = Document(page_content=raw_text, metadata=meta)
                documents.append(doc)
            except Exception as e:
                print(f"Warning: Could not read file {file_path}: {e}")

    return documents


def split_documents(
    documents: List[Document], chunk_size: int = 600, chunk_overlap: int = 80
) -> List[Document]:
    """
    Splits documents into manageable, semantically coherent chunks using modern text splitters.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n### ", "\n## ", "\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)
    return chunks
