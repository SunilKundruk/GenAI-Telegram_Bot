"""
Configuration module — loads settings from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# ── Embedding Model ──────────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ── LLM Model ────────────────────────────────────────────────────────────────
# Using Flash Latest which is often the most compatible
LLM_MODEL = "gemini-flash-latest"

# ── RAG Settings ──────────────────────────────────────────────────────────────
CHUNK_SIZE = 500          # characters per chunk
CHUNK_OVERLAP = 100       # overlap between consecutive chunks
TOP_K = 3                 # number of chunks to retrieve

# ── Paths ─────────────────────────────────────────────────────────────────────
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "vector_store.db")

# ── Cache ─────────────────────────────────────────────────────────────────────
CACHE_MAX_SIZE = 128      # max cached query results
