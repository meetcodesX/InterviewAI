from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db
from api.resume import router as resume_router
from api.interview import router as interview_router
from api.report import router as report_router
from config import settings
from schemas.schemas import HealthResponse
from services.rag_service import rag_service

app = FastAPI(title="InterviewAI", description="Agentic Interview Trainer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(report_router)

@app.on_event("startup")
async def startup():
    init_db()
    if not rag_service.initialized:
        print("Warning: RAG Service is not fully initialized. Running in mock/degraded mode.")

@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        ai_provider=settings.AI_PROVIDER,
        rag_status="initialized" if rag_service.initialized else "not_initialized",
        version="1.0.0"
    )
