"""Application configuration loaded from environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of backend
BASE_DIR = Path(__file__).resolve().parent

# Load .env from project root or backend
_root_env = BASE_DIR.parent / ".env"
_backend_env = BASE_DIR / ".env"

if _root_env.exists():
    load_dotenv(dotenv_path=_root_env)
elif _backend_env.exists():
    load_dotenv(dotenv_path=_backend_env)
else:
    load_dotenv()


def _resolve_database_url() -> str:
    """Ensure consistent absolute path for SQLite regardless of execution directory."""
    raw_url = os.getenv("DATABASE_URL", "").strip()
    if not raw_url or raw_url.startswith("sqlite:///./") or raw_url == "sqlite:///interview_ai.db":
        db_file = (BASE_DIR / "interview_ai.db").resolve()
        return f"sqlite:///{db_file.as_posix()}"
    return raw_url


def _resolve_chroma_dir() -> str:
    """Ensure consistent absolute path for ChromaDB."""
    raw_dir = os.getenv("CHROMA_PERSIST_DIR", "").strip()
    if not raw_dir or raw_dir.startswith("./") or raw_dir == "chroma_db":
        return str((BASE_DIR / "chroma_db").resolve())
    return raw_dir


class Settings:
    """Central configuration for the InterviewAI backend."""

    # AI Provider - "ibm_granite" or "mock"
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock")

    # IBM watsonx.ai
    IBM_API_KEY: str = os.getenv("IBM_API_KEY", "")
    IBM_PROJECT_ID: str = os.getenv("IBM_PROJECT_ID", "")
    IBM_URL: str = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
    IBM_GRANITE_MODEL: str = os.getenv("IBM_GRANITE_MODEL", "ibm/granite-3-8b-instruct")

    # Consistent absolute database URL
    DATABASE_URL: str = _resolve_database_url()

    # Consistent absolute ChromaDB directory
    CHROMA_PERSIST_DIR: str = _resolve_chroma_dir()

    # Application URLs
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".pdf"}

    # Data directory for RAG knowledge base
    DATA_DIR: str = str((BASE_DIR / "data").resolve())

    # Question Deduplication Threshold
    QUESTION_SIMILARITY_THRESHOLD: float = float(os.getenv("QUESTION_SIMILARITY_THRESHOLD", "0.85"))

    @property
    def is_mock(self) -> bool:
        return self.AI_PROVIDER.lower() == "mock"

    @property
    def is_ibm(self) -> bool:
        return self.AI_PROVIDER.lower() == "ibm_granite"


settings = Settings()
