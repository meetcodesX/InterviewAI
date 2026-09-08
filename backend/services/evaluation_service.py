"""Evaluation service for grading interview answers and adaptive difficulty management."""

from typing import List, Optional, Dict, Any
from schemas.schemas import EvaluationResponse, InterviewReport
from services.granite_service import granite_service


class EvaluationService:
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        category: str = "technical",
        difficulty: str = "medium",
        job_role: str = "Software Engineer",
        candidate_profile: Optional[dict] = None,
        experience_level: str = "fresher",
        rag_context: str = ""
    ) -> EvaluationResponse:
        """Evaluate candidate answer with complete context passed to Granite."""
        context = {
            "category": category,
            "difficulty": difficulty,
            "job_role": job_role,
            "candidate_profile": candidate_profile or {},
            "experience_level": experience_level,
            "rag_context": rag_context
        }
        return granite_service.evaluate_answer(question, answer, context)

    def determine_next_difficulty(self, evaluations: List[dict], current_difficulty: str) -> str:
        """Adapts difficulty level based on candidate performance score."""
        if not evaluations:
            return current_difficulty

        recent_evals = evaluations[-3:] if len(evaluations) >= 3 else evaluations
        avg_score = sum(e.get("overall_score", 5) for e in recent_evals) / len(recent_evals)

        levels = ["easy", "medium", "hard"]
        try:
            curr_idx = levels.index(current_difficulty.lower())
        except ValueError:
            curr_idx = 1

        # Strict specification:
        # score >= 8: increase difficulty
        # score 5-7: maintain current difficulty
        # score < 5: decrease difficulty
        if avg_score >= 8:
            curr_idx = min(len(levels) - 1, curr_idx + 1)
        elif avg_score < 5:
            curr_idx = max(0, curr_idx - 1)

        return levels[curr_idx]

    def generate_final_report(self, interview_data: dict) -> InterviewReport:
        """Compile final report via Granite service."""
        return granite_service.generate_report(interview_data)


evaluation_service = EvaluationService()
