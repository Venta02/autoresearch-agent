"""Configuration module."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"
PUBLIC_DIR = PROJECT_ROOT / "public"

REPORTS_DIR.mkdir(exist_ok=True)
CHROMA_DB_DIR.mkdir(exist_ok=True)

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    raise ValueError(
        "GEMINI_API_KEY not found! Setup .env file from .env.example"
    )

if not TAVILY_API_KEY or TAVILY_API_KEY == "your_tavily_api_key_here":
    raise ValueError(
        "TAVILY_API_KEY not found! Get free key at https://app.tavily.com"
    )

# Models
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

# Agent settings
MAX_RESEARCH_ITERATIONS = int(os.getenv("MAX_RESEARCH_ITERATIONS", "5"))
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "5000"))

# Vector DB
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(CHROMA_DB_DIR))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "research_memory")


def print_config():
    print("=" * 50)
    print("AutoResearch Agent - Configuration")
    print("=" * 50)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"LLM Model: {GEMINI_MODEL}")
    print(f"Max iterations: {MAX_RESEARCH_ITERATIONS}")
    print(f"Gemini Key: {'Loaded' if GEMINI_API_KEY else 'Missing'}")
    print(f"Tavily Key: {'Loaded' if TAVILY_API_KEY else 'Missing'}")
    print("=" * 50)


if __name__ == "__main__":
    print_config()
