"""LangGraph-based interview agent for InterviewAI.

Implements an adaptive interview workflow:
  load_profile -> retrieve_context -> generate_question -> evaluate_answer -> update_state -> generate_report
"""

from typing import TypedDict, Dict, Any, List, Optional, Tuple
import uuid
import logging
from langgraph.graph import StateGraph, END
from services.rag_service import rag_service
from services.granite_service import granite_service
from services.evaluation_service import evaluation_service

logger = logging.getLogger(__name__)


class InterviewState(TypedDict):
    candidate_profile: dict
    config: dict
    interview_id: str
    current_question_index: int
    total_questions: int
    questions: list
    answers: list
    evaluations: list
    difficulty_progression: list
    current_difficulty: str
    skills_tested: list
    current_question: Optional[dict]
    rag_context: str
    is_complete: bool
    report: Optional[dict]


# =====================================================================
# LangGraph Workflow Nodes
# =====================================================================

def load_profile(state: InterviewState) -> InterviewState:
    """Initialize difficulty from configuration or default to medium."""
    if "current_difficulty" not in state or not state["current_difficulty"]:
        diff = state.get("config", {}).get("difficulty", "medium")
        if diff == "adaptive":
            diff = "medium"
        state["current_difficulty"] = diff
    return state


def retrieve_context(state: InterviewState) -> InterviewState:
    """Use RAG service to fetch role-specific questions and rubrics."""
    profile = state.get("candidate_profile", {})
    config = state.get("config", {})
    skills = profile.get("skills", [])
    tested = state.get("skills_tested", [])

    # Select the next skill to test
    remaining_skills = [s for s in skills if s not in tested]
    skill = remaining_skills[0] if remaining_skills else (skills[0] if skills else "General Software Development")

    context = rag_service.get_interview_context(
        job_role=config.get("job_role", "Software Engineer"),
        skills=[skill],
        category=config.get("interview_type", "technical"),
        difficulty=state.get("current_difficulty", "medium")
    )

    state["rag_context"] = context
    if "skills_tested" not in state or state["skills_tested"] is None:
        state["skills_tested"] = []
    state["skills_tested"].append(skill)
    return state


def generate_question(state: InterviewState) -> InterviewState:
    """Generate interview question using IBM Granite and RAG context with persistent deduplication."""
    from services.question_dedup_service import question_dedup_service, normalize_question
    from database.db import get_db

    # Get DB session for deduplication check
    db = next(get_db())
    try:
        # Collect questions already asked in current session
        current_session_questions = [
            q.get("question") for q in state.get("questions", []) if isinstance(q, dict) and q.get("question")
        ]
        
        # Also fetch recent questions from history to pass into Granite context so it avoids them
        recent_history = question_dedup_service.get_recent_questions(db, limit=15)
        avoid_questions = list(set(current_session_questions + recent_history))

        context = {
            "candidate_profile": state.get("candidate_profile", {}),
            "rag_context": state.get("rag_context", ""),
            "difficulty": state.get("current_difficulty", "medium"),
            "previous_questions": avoid_questions
        }

        # Attempt up to 4 times to generate a unique question
        selected_question = None
        for attempt in range(4):
            question_data = granite_service.generate_question(context)
            cand_q = question_data.get("question", "").strip()
            
            is_dup, sim_score, reason = question_dedup_service.is_duplicate(
                db, cand_q, current_interview_questions=current_session_questions
            )
            
            if not is_dup:
                selected_question = question_data
                break
            else:
                logger.info(f"Regenerating question (attempt {attempt + 1}/4) due to duplicate: {reason}")

        # Fallback to local markdown knowledge base if LLM repeatedly generated duplicate
        if not selected_question:
            asked_norms = {normalize_question(q) for q in (current_session_questions + recent_history)}
            cat = state.get("config", {}).get("interview_type", "technical")
            diff = state.get("current_difficulty", "medium")
            kb_q = rag_service.get_unasked_knowledge_question(cat, diff, asked_norms)
            if kb_q:
                selected_question = kb_q
                logger.info(f"Selected unasked question from knowledge base: {kb_q['question']}")
            else:
                selected_question = {
                    "question": question_data.get("question", "Could you describe a challenging technical problem you solved recently?"),
                    "category": cat,
                    "difficulty": diff
                }

        q_number = len(state.get("questions", [])) + 1
        q_dict = {
            "question_id": str(uuid.uuid4()),
            "question": selected_question.get("question", "Could you tell me about your background and technical experience?"),
            "category": selected_question.get("category", state.get("config", {}).get("interview_type", "technical")),
            "difficulty": state.get("current_difficulty", "medium"),
            "question_number": q_number,
            "interview_id": str(state.get("interview_id", ""))
        }

        state["current_question"] = q_dict
        if "questions" not in state or state["questions"] is None:
            state["questions"] = []
        state["questions"].append(q_dict)

        if "difficulty_progression" not in state or state["difficulty_progression"] is None:
            state["difficulty_progression"] = []
        state["difficulty_progression"].append(state.get("current_difficulty", "medium"))

        return state
    finally:
        db.close()


def evaluate_answer(state: InterviewState) -> InterviewState:
    """Evaluate candidate answer using IBM Granite and update difficulty adaptively."""
    answers = state.get("answers", [])
    questions = state.get("questions", [])

    if not answers or len(answers) == 0:
        return state

    latest_answer = answers[-1]
    # Current question corresponds to the answer being evaluated
    q_index = len(answers) - 1
    current_q = questions[q_index] if q_index < len(questions) else questions[-1]

    # Retrieve targeted RAG context specifically for this question to evaluate against
    q_text = current_q.get("question", "")
    rag_ctx = rag_service.get_relevant_context(
        query=q_text,
        category=current_q.get("category", "technical"),
        top_k=3
    )

    eval_resp = evaluation_service.evaluate_answer(
        question=q_text,
        answer=latest_answer,
        category=current_q.get("category", "technical"),
        difficulty=current_q.get("difficulty", "medium"),
        job_role=state.get("config", {}).get("job_role", "Software Engineer"),
        candidate_profile=state.get("candidate_profile", {}),
        experience_level=state.get("config", {}).get("experience_level", "fresher"),
        rag_context=rag_ctx
    )

    eval_dict = eval_resp.model_dump() if hasattr(eval_resp, "model_dump") else dict(eval_resp)

    if "evaluations" not in state or state["evaluations"] is None:
        state["evaluations"] = []
    state["evaluations"].append(eval_dict)

    # Adaptive difficulty progression based on performance
    if state.get("config", {}).get("difficulty") == "adaptive":
        next_diff = evaluation_service.determine_next_difficulty(
            state["evaluations"],
            state.get("current_difficulty", "medium")
        )
        state["current_difficulty"] = next_diff

    state["current_question_index"] = len(state["answers"])

    # Check termination condition
    if state["current_question_index"] >= state.get("total_questions", 10):
        state["is_complete"] = True

    return state


def update_state(state: InterviewState) -> InterviewState:
    """Clear transient state before next question cycle."""
    state["current_question"] = None
    state["rag_context"] = ""
    return state


def generate_report_node(state: InterviewState) -> InterviewState:
    """Compile comprehensive final evaluation report using IBM Granite."""
    report = evaluation_service.generate_final_report(state)
    report_dict = report.model_dump() if hasattr(report, "model_dump") else dict(report)
    state["report"] = report_dict
    state["is_complete"] = True
    return state


def check_complete(state: InterviewState) -> str:
    if state.get("is_complete", False):
        return "generate_report"
    return "retrieve_context"


# =====================================================================
# Compile LangGraph StateGraph
# =====================================================================

def create_interview_graph() -> StateGraph:
    workflow = StateGraph(InterviewState)

    workflow.add_node("load_profile", load_profile)
    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("generate_question", generate_question)
    workflow.add_node("evaluate_answer", evaluate_answer)
    workflow.add_node("update_state", update_state)
    workflow.add_node("generate_report", generate_report_node)

    workflow.set_entry_point("load_profile")
    workflow.add_edge("load_profile", "retrieve_context")
    workflow.add_edge("retrieve_context", "generate_question")
    workflow.add_edge("generate_question", END)

    workflow.add_conditional_edges("evaluate_answer", check_complete, {
        "generate_report": "generate_report",
        "retrieve_context": "update_state"
    })
    workflow.add_edge("update_state", "retrieve_context")
    workflow.add_edge("generate_report", END)

    return workflow.compile()


graph = create_interview_graph()


# =====================================================================
# Database Rehydration & Stateless Workflow Functions
# =====================================================================

def state_from_interview(db_interview) -> InterviewState:
    """Reconstruct an InterviewState from a SQLAlchemy Interview record.

    Ensures the database is the authoritative single source of truth.
    """
    questions = list(db_interview.questions or [])
    answers = list(db_interview.answers or [])
    evaluations = list(db_interview.evaluations or [])
    config = dict(db_interview.config or {})
    profile = dict(db_interview.candidate_profile or {})
    diff_prog = list(db_interview.difficulty_progression or [])

    current_diff = diff_prog[-1] if diff_prog else config.get("difficulty", "medium")
    if current_diff == "adaptive":
        current_diff = "medium"

    current_q = questions[-1] if questions else None

    # Track skills tested from questions
    skills_tested = []
    for q in questions:
        if isinstance(q, dict) and q.get("category"):
            skills_tested.append(q.get("category"))

    total_q = int(config.get("num_questions", 10))
    is_done = (
        db_interview.status == "completed"
        or (len(answers) >= total_q and total_q > 0)
    )

    return {
        "candidate_profile": profile,
        "config": config,
        "interview_id": str(db_interview.id),
        "current_question_index": db_interview.current_question_index or len(answers),
        "total_questions": total_q,
        "questions": questions,
        "answers": answers,
        "evaluations": evaluations,
        "difficulty_progression": diff_prog,
        "current_difficulty": current_diff,
        "skills_tested": skills_tested,
        "current_question": current_q,
        "rag_context": "",
        "is_complete": is_done,
        "report": db_interview.report if db_interview.report else None,
    }


def initialize_interview(profile: dict, config: dict, interview_id: str) -> Tuple[InterviewState, dict]:
    """Execute LangGraph initial cycle: load_profile -> retrieve_context -> generate_question."""
    initial_diff = config.get("difficulty", "medium")
    if initial_diff == "adaptive":
        initial_diff = "medium"

    state: InterviewState = {
        "candidate_profile": profile,
        "config": config,
        "interview_id": str(interview_id),
        "current_question_index": 0,
        "total_questions": int(config.get("num_questions", 10)),
        "questions": [],
        "answers": [],
        "evaluations": [],
        "difficulty_progression": [],
        "current_difficulty": initial_diff,
        "skills_tested": [],
        "current_question": None,
        "rag_context": "",
        "is_complete": False,
        "report": None,
    }

    result = graph.invoke(state)
    first_q = result.get("current_question")
    return result, first_q


def process_answer(state: InterviewState, answer: str) -> Tuple[InterviewState, dict, Optional[dict]]:
    """Evaluate submitted answer and determine next question or final report."""
    if "answers" not in state or state["answers"] is None:
        state["answers"] = []
    state["answers"].append(answer)

    # 1. Evaluate answer node
    state = evaluate_answer(state)
    eval_result = state["evaluations"][-1] if state.get("evaluations") else {}

    next_q = None
    # 2. Check if finished or generate next question
    if state.get("is_complete"):
        state = generate_report_node(state)
    else:
        state = update_state(state)
        state = retrieve_context(state)
        state = generate_question(state)
        next_q = state.get("current_question")

    return state, eval_result, next_q


# =====================================================================
# Compatibility Helpers (for test scripts)
# =====================================================================

def start_interview(profile: dict, config: dict, interview_id: str) -> dict:
    _, first_q = initialize_interview(profile, config, interview_id)
    return first_q
