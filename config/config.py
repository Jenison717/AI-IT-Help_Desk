"""
Application Configuration Module
Handles environment variables and project paths for the AI IT Helpdesk Agent.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Base Project Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Ollama LLM Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Storage Paths
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "helpdesk.db"))
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(BASE_DIR / "vectorstore" / "chroma"))
KNOWLEDGE_BASE_DIR = os.getenv("KNOWLEDGE_BASE_DIR", str(BASE_DIR / "knowledge_base"))

# Embedding Model Configuration
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Ensure required directories exist
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
os.makedirs(VECTOR_DB_PATH, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
