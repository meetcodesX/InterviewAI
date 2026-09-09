import os
import sys
from pathlib import Path

# Ensure backend root is always in sys.path for serverless function environments (e.g. Vercel)
_backend_dir = str(Path(__file__).resolve().parent)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.resume import router as resume_router
from api.interview import router as interview_router
from api.report import router as report_router
from config import settings
from schemas.schemas import HealthResponse

app = FastAPI(title="InterviewAI", description="Agentic Interview Trainer", version="1.0.0")

# Collect allowed origins safely
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
if settings.FRONTEND_URL and settings.FRONTEND_URL not in allowed_origins:
    allowed_origins.append(settings.FRONTEND_URL.rstrip("/"))
if os.getenv("VERCEL_URL"):
    allowed_origins.append(f"https://{os.getenv('VERCEL_URL')}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(report_router)

@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Ultra-fast, non-blocking health check.
    
    Returns immediately without initializing databases, vector stores,
    or external AI model connections.
    """
    return HealthResponse(
        status="ok",
        ai_provider=getattr(settings, "AI_PROVIDER", "mock"),
        rag_status="initialized",
        version="1.0.0"
    )
