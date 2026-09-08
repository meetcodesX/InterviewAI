@echo off
title InterviewAI - Agentic Interview Trainer
echo ========================================================
echo   InterviewAI - Agentic Interview Trainer (AICTE 2026)
echo   Powered by IBM Granite, LangGraph, RAG & ChromaDB
echo ========================================================
echo.

:: 1. Check .env
if not exist .env (
    echo [INFO] Creating .env from .env.example ...
    copy .env.example .env
)

:: 2. Launch FastAPI Backend
echo [INFO] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "InterviewAI Backend (Port 8000)" cmd /k "cd /d %~dp0backend && uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

:: 3. Launch Next.js Frontend
echo [INFO] Starting Next.js Frontend on http://localhost:3000 ...
start "InterviewAI Frontend (Port 3000)" cmd /k "cd /d %~dp0frontend && npm run dev"

:: 4. Open browser
echo [INFO] Waiting for servers to initialize ...
timeout /t 4 /nobreak >nul
echo [INFO] Opening InterviewAI in default browser ...
start http://localhost:3000

echo.
echo ========================================================
echo   InterviewAI is running!
echo   Frontend: http://localhost:3000
echo   Backend:  http://127.0.0.1:8000
echo   API Docs: http://127.0.0.1:8000/docs
echo ========================================================
echo Press any key to exit this launcher window (servers remain active).
pause >nul
