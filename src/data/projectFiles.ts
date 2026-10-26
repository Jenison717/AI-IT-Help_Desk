export interface ProjectFile {
  path: string;
  category: "app" | "agent" | "tools" | "rag" | "memory" | "config" | "docs";
  description: string;
}

export const PROJECT_FILES: ProjectFile[] = [
  { path: "app.py", category: "app", description: "Streamlit Web UI with chat, sessions, and live agent status" },
  { path: "agent/graph.py", category: "agent", description: "LangGraph StateGraph workflow, routing edges, and execution runner" },
  { path: "agent/nodes.py", category: "agent", description: "All 6 LangGraph nodes: classify, retrieve, decide, execute, generate, save" },
  { path: "agent/state.py", category: "agent", description: "TypedDict state schema carrying query, intent, tools, RAG docs, and memory" },
  { path: "agent/prompts.py", category: "agent", description: "System prompts for intent classification, tool dispatch, and structured RAG" },
  { path: "tools/calculator.py", category: "tools", description: "Safe AST arithmetic evaluator without eval() to prevent code injection" },
  { path: "tools/time_tool.py", category: "tools", description: "System date and time diagnostic tool" },
  { path: "tools/network_tool.py", category: "tools", description: "Non-invasive socket handshake to test internet connectivity and DNS" },
  { path: "tools/system_info.py", category: "tools", description: "Diagnostic specs inspector (OS, Python, CPU cores, RAM metrics)" },
  { path: "tools/word_count.py", category: "tools", description: "Text analysis counter for words, characters, and sentences" },
  { path: "rag/vector_store.py", category: "rag", description: "ChromaDB vector collection initialization, persistence, and querying" },
  { path: "rag/retriever.py", category: "rag", description: "Semantic vector retrieval and knowledge context citation formatter" },
  { path: "rag/document_loader.py", category: "rag", description: "Markdown reader and recursive text splitter for knowledge runbooks" },
  { path: "rag/embeddings.py", category: "rag", description: "Embeddings provider (HuggingFace / Ollama fallback)" },
  { path: "memory/database.py", category: "memory", description: "SQLite database manager for sessions, conversation history, and state" },
  { path: "config/config.py", category: "config", description: "Centralized environment loader (Ollama URL, model name, DB paths)" },
  { path: "scripts/build_vector_db.py", category: "rag", description: "Standalone vector database indexing CLI script" },
  { path: "requirements.txt", category: "config", description: "Python dependencies with modern non-deprecated LangChain & LangGraph" },
  { path: "README.md", category: "docs", description: "Complete documentation, architecture diagram, installation, and commands" }
];
