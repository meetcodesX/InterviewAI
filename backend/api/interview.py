"""FastAPI routes for interview lifecycle management.

Fully persisted with SQLite + SQLAlchemy as the single source of truth.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
import logging

from database.db import get_db, init_db
from models.models import Interview, InterviewQuestion
from schemas.schemas import (
    InterviewCreateRequest, AnswerSubmitRequest, NextQuestionRequest,
    FinishInterviewRequest, QuestionResponse, AnswerEvaluationResponse,
    InterviewReport, InterviewStatusResponse, DashboardStats
)
from agents.interview_agent import (
    initialize_interview, process_answer, state_from_interview,
    generate_report_node, retrieve_context, generate_question
)
from services.question_dedup_service import question_dedup_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Interview"])


@router.post("/interview/create", response_model=QuestionResponse)
async def create_interview(req: InterviewCreateRequest, db: Session = Depends(get_db)):
    """Create a new interview session, persist to database, and return the first question."""
    init_db()  # Ensure tables exist
    interview_id = str(uuid.uuid4()).strip()

    try:
        # 1. Run LangGraph initial step to generate the first question
        _, first_q = initialize_interview(
            profile=req.profile.model_dump(),
            config=req.config.model_dump(),
            interview_id=interview_id
        )

        if not first_q or not isinstance(first_q, dict):
            raise ValueError("Failed to generate initial question from agent")

        first_qid = str(first_q["question_id"]).strip()
        first_diff = str(first_q.get("difficulty", "medium")).strip()

        # 2. Persist the Interview record to SQLite
        db_interview = Interview(
            id=interview_id,
            candidate_name=req.profile.name or "Candidate",
            candidate_profile=req.profile.model_dump(),
            config=req.config.model_dump(),
            status="in_progress",
            current_question_index=0,
            questions=[first_q],
            answers=[],
            evaluations=[],
            difficulty_progression=[first_diff],
            report=None
        )
        db.add(db_interview)

        # 3. Persist the first InterviewQuestion record to SQLite
        q_record = InterviewQuestion(
            id=first_qid,
            interview_id=interview_id,
            question_text=first_q.get("question", "Tell me about yourself."),
            category=first_q.get("category", "technical"),
            difficulty=first_diff,
            question_number=1,
            answer_text=None,
            evaluation=None
        )
        db.add(q_record)

        # 4. Record to persistent QuestionHistory for cross-interview deduplication
        question_dedup_service.record_question(
            db=db,
            question_dict=first_q,
            interview_id=interview_id,
            job_role=req.config.job_role or "",
            interview_type=req.config.interview_type or "technical"
        )

        # 5. Commit and refresh to ensure data is written to disk
        db.commit()
        db.refresh(db_interview)
        db.refresh(q_record)

        total_q = req.config.num_questions if (req.config and req.config.num_questions) else 10

        logger.info(f"Created interview record in DB: ID={interview_id}, Q1={first_qid}")

        return QuestionResponse(
            question_id=first_qid,
            question_number=1,
            total_questions=total_q,
            category=first_q.get("category", "technical"),
            difficulty=first_diff,
            question=first_q["question"],
            interview_id=interview_id,
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create interview: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")


@router.post("/interview/answer")
async def answer_question(req: AnswerSubmitRequest, db: Session = Depends(get_db)):
    """Submit an answer, evaluate with IBM Granite, adapt difficulty, and persist state."""
    clean_id = str(req.interview_id).strip()
    clean_qid = str(req.question_id).strip()

    # 1. Retrieve the interview from the database
    db_interview = db.query(Interview).filter(Interview.id == clean_id).first()
    if not db_interview:
        logger.warning(f"Interview {clean_id} not found in DB")
        raise HTTPException(status_code=404, detail=f"Interview {clean_id} not found")

    try:
        # 2. Reconstruct LangGraph state from database record
        state = state_from_interview(db_interview)

        # 3. Process answer: evaluation + adaptive difficulty + next question generation
        state, eval_data, next_q = process_answer(state, req.answer)

        # 4. Synchronize state back into DB record
        db_interview.answers = list(state.get("answers", []))
        db_interview.evaluations = list(state.get("evaluations", []))
        db_interview.difficulty_progression = list(state.get("difficulty_progression", []))
        db_interview.questions = list(state.get("questions", []))
        db_interview.current_question_index = int(state.get("current_question_index", 0))

        if state.get("is_complete"):
            db_interview.status = "completed"
            if state.get("report"):
                db_interview.report = state["report"]

        # 5. Update the specific InterviewQuestion record
        q_record = db.query(InterviewQuestion).filter(
            InterviewQuestion.interview_id == clean_id,
            InterviewQuestion.id == clean_qid
        ).first()
        if q_record:
            q_record.answer_text = req.answer
            q_record.evaluation = eval_data

        # 6. If next question was generated, ensure an InterviewQuestion record exists
        if next_q and isinstance(next_q, dict) and next_q.get("question_id"):
            next_qid = str(next_q["question_id"]).strip()
            existing_q = db.query(InterviewQuestion).filter(
                 InterviewQuestion.id == next_qid
            ).first()
            if not existing_q:
                new_q_rec = InterviewQuestion(
                    id=next_qid,
                    interview_id=clean_id,
                    question_text=next_q.get("question", ""),
                    category=next_q.get("category", "technical"),
                    difficulty=next_q.get("difficulty", "medium"),
                    question_number=next_q.get("question_number", len(state.get("questions", []))),
                    answer_text=None,
                    evaluation=None
                )
                db.add(new_q_rec)
                
                # Record to persistent QuestionHistory
                question_dedup_service.record_question(
                    db=db,
                    question_dict=next_q,
                    interview_id=clean_id,
                    job_role=state.get("config", {}).get("job_role", ""),
                    interview_type=state.get("config", {}).get("interview_type", "technical")
                )

        # 7. Commit changes and refresh
        db.commit()
        db.refresh(db_interview)

        # Find question text for response
        q_text = ""
        for q in (db_interview.questions or []):
            if isinstance(q, dict) and str(q.get("question_id")).strip() == clean_qid:
                q_text = q.get("question", "")
                break

        return {
            "question_id": clean_qid,
            "question": q_text,
            "answer": req.answer,
            "evaluation": eval_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to evaluate answer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to evaluate answer: {str(e)}")


@router.post("/interview/next")
async def next_question(req: NextQuestionRequest, db: Session = Depends(get_db)):
    """Retrieve the next question for the interview session."""
    clean_id = str(req.interview_id).strip()

    # 1. Retrieve the interview from the database
    db_interview = db.query(Interview).filter(Interview.id == clean_id).first()
    if not db_interview:
        logger.warning(f"Interview {clean_id} not found in DB")
        raise HTTPException(status_code=404, detail=f"Interview {clean_id} not found")

    try:
        config = db_interview.config or {}
        total_q = int(config.get("num_questions", 10))
        answers = db_interview.answers or []
        questions = db_interview.questions or []

        # Check if interview is completed
        if db_interview.status == "completed" or (len(answers) >= total_q and total_q > 0):
            return {"status": "complete"}

        # 2. Get next question from existing list or generate dynamically
        next_q = None
        if len(questions) > len(answers):
            next_q = questions[len(answers)]
        else:
            # Generate next question via LangGraph
            state = state_from_interview(db_interview)
            state = retrieve_context(state)
            state = generate_question(state)
            next_q = state.get("current_question")

            questions_list = list(questions)
            questions_list.append(next_q)
            db_interview.questions = questions_list
            db_interview.current_question_index = len(questions_list) - 1

            diff_prog = list(db_interview.difficulty_progression or [])
            diff_prog.append(next_q.get("difficulty", "medium"))
            db_interview.difficulty_progression = diff_prog

            next_qid = str(next_q["question_id"]).strip()
            new_q_rec = InterviewQuestion(
                id=next_qid,
                interview_id=clean_id,
                question_text=next_q.get("question", ""),
                category=next_q.get("category", "technical"),
                difficulty=next_q.get("difficulty", "medium"),
                question_number=next_q.get("question_number", len(questions_list)),
                answer_text=None,
                evaluation=None
            )
            db.add(new_q_rec)

            # Record to persistent QuestionHistory
            question_dedup_service.record_question(
                db=db,
                question_dict=next_q,
                interview_id=clean_id,
                job_role=config.get("job_role", ""),
                interview_type=config.get("interview_type", "technical")
            )

            db.commit()
            db.refresh(db_interview)

        q_number = len(answers) + 1
        return QuestionResponse(
            question_id=str(next_q["question_id"]),
            question_number=next_q.get("question_number", q_number),
            total_questions=total_q,
            category=next_q.get("category", "technical"),
            difficulty=next_q.get("difficulty", "medium"),
            question=next_q["question"],
            interview_id=clean_id,
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to get next question: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get next question: {str(e)}")


@router.post("/interview/finish")
async def complete_interview(req: FinishInterviewRequest, db: Session = Depends(get_db)):
    """Finish the interview and compile the final report."""
    clean_id = str(req.interview_id).strip()

    db_interview = db.query(Interview).filter(Interview.id == clean_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail=f"Interview {clean_id} not found")

    try:
        if db_interview.status == "completed" and db_interview.report:
            return db_interview.report

        # Reconstruct LangGraph state and generate report
        state = state_from_interview(db_interview)
        state = generate_report_node(state)
        report_data = state["report"]

        db_interview.status = "completed"
        db_interview.report = report_data
        db.commit()
        db.refresh(db_interview)

        return report_data
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to finish interview: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@router.get("/interview/{interview_id}", response_model=InterviewStatusResponse)
async def get_interview_status(interview_id: str, db: Session = Depends(get_db)):
    """Get the current status of an interview session."""
    clean_id = str(interview_id).strip()
    db_interview = db.query(Interview).filter(Interview.id == clean_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail=f"Interview {clean_id} not found")

    config = db_interview.config or {}
    return InterviewStatusResponse(
        interview_id=clean_id,
        status=db_interview.status,
        current_question=db_interview.current_question_index or 0,
        total_questions=int(config.get("num_questions", 10)),
        profile=db_interview.candidate_profile,
        config=db_interview.config,
    )


@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics across all completed interviews."""
    interviews = db.query(Interview).all()

    if not interviews:
        return DashboardStats()

    completed_interviews = [i for i in interviews if i.status == "completed" and i.report]
    total = len(completed_interviews)
    scores = []
    all_strengths = {}
    all_weaknesses = {}
    recent = []

    for interview in (completed_interviews if completed_interviews else interviews):
        report = interview.report or {}
        score = int(report.get("overall_score", 0))
        if score > 0:
            scores.append(score)

        for s in report.get("strengths", []):
            all_strengths[s] = all_strengths.get(s, 0) + 1
        for w in report.get("weaknesses", []):
            all_weaknesses[w] = all_weaknesses.get(w, 0) + 1

        recent.append({
            "id": str(interview.id),
            "candidate_name": interview.candidate_name,
            "role": (interview.config or {}).get("job_role", "Software Engineer"),
            "score": score,
            "date": interview.created_at.isoformat() if interview.created_at else "",
            "status": interview.status,
        })

    avg_score = int(sum(scores) / len(scores)) if scores else 0
    strongest = max(all_strengths, key=all_strengths.get) if all_strengths else "N/A"
    weakest = max(all_weaknesses, key=all_weaknesses.get) if all_weaknesses else "N/A"

    recent.sort(key=lambda x: x.get("date", ""), reverse=True)

    score_history = [
        {"interview": i + 1, "score": s} for i, s in enumerate(scores[-20:])
    ]

    return DashboardStats(
        total_interviews=total if total > 0 else len(interviews),
        average_score=avg_score,
        strongest_skill=strongest,
        weakest_skill=weakest,
        recent_interviews=recent[:10],
        score_history=score_history,
    )
