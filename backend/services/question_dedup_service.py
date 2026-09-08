"""Persistent Question Deduplication and Semantic Duplicate Detection.

Ensures questions are not repeated within an interview or across new interviews.
"""

import re
import uuid
import logging
from typing import Tuple, List, Optional
import numpy as np
from sqlalchemy.orm import Session

from config import settings
from models.models import QuestionHistory
from services.rag_service import rag_service

logger = logging.getLogger(__name__)


def normalize_question(text: str) -> str:
    """Normalize question string for exact matching (lowercase, no punctuation, single spaces)."""
    if not text:
        return ""
    # Remove punctuation, lowercase, collapse whitespace
    cleaned = re.sub(r"[^\w\s]", "", text.lower())
    return " ".join(cleaned.split())


class QuestionDedupService:
    """Service to detect and prevent question repetition across and within interviews."""

    def __init__(self):
        self.threshold = settings.QUESTION_SIMILARITY_THRESHOLD

    def get_recent_questions(self, db: Session, limit: int = 20) -> List[str]:
        """Fetch recently asked questions from the persistent store to guide the prompt."""
        try:
            records = (
                db.query(QuestionHistory)
                .order_by(QuestionHistory.created_at.desc())
                .limit(limit)
                .all()
            )
            return [r.question_text for r in records if r.question_text]
        except Exception as e:
            logger.error(f"Error fetching recent questions: {e}")
            return []

    def is_duplicate(
        self,
        db: Session,
        candidate_question: str,
        current_interview_questions: Optional[List[str]] = None
    ) -> Tuple[bool, float, str]:
        """Check if candidate question is an exact or semantic duplicate of any previously asked question.
        
        Returns:
            (is_duplicate, max_similarity, reason)
        """
        if not candidate_question or not candidate_question.strip():
            return True, 1.0, "Empty question"

        norm_cand = normalize_question(candidate_question)

        # 1. Check against current interview questions
        if current_interview_questions:
            for q in current_interview_questions:
                if normalize_question(q) == norm_cand:
                    return True, 1.0, f"Exact duplicate of current session question: '{q}'"

        # 2. Check exact match in persistent SQLite store
        exact_match = (
            db.query(QuestionHistory)
            .filter(QuestionHistory.normalized_question == norm_cand)
            .first()
        )
        if exact_match:
            return True, 1.0, f"Exact duplicate in history: '{exact_match.question_text}'"

        # 3. Semantic similarity check using SentenceTransformer embeddings
        try:
            all_history = (
                db.query(QuestionHistory.question_text)
                .order_by(QuestionHistory.created_at.desc())
                .limit(100)
                .all()
            )
            history_texts = [r[0] for r in all_history if r[0]]
            
            # Also include current session questions if not in history
            if current_interview_questions:
                for q in current_interview_questions:
                    if q not in history_texts:
                        history_texts.append(q)

            if not history_texts or rag_service.model is None:
                return False, 0.0, ""

            # Compute embeddings
            cand_emb = rag_service.model.encode([candidate_question])
            hist_embs = rag_service.model.encode(history_texts)

            # Cosine similarity
            cand_norm = cand_emb / (np.linalg.norm(cand_emb, axis=1, keepdims=True) + 1e-9)
            hist_norm = hist_embs / (np.linalg.norm(hist_embs, axis=1, keepdims=True) + 1e-9)

            sims = np.dot(cand_norm, hist_norm.T)[0]
            max_idx = int(np.argmax(sims))
            max_sim = float(sims[max_idx])

            if max_sim >= self.threshold:
                matched = history_texts[max_idx]
                return True, max_sim, f"Semantic duplicate ({max_sim:.2f} >= {self.threshold}): '{matched}'"

            return False, max_sim, ""
        except Exception as e:
            logger.error(f"Semantic duplicate check error: {e}")
            return False, 0.0, ""

    def record_question(
        self,
        db: Session,
        question_dict: dict,
        interview_id: Optional[str] = None,
        job_role: str = "",
        interview_type: str = "technical"
    ) -> None:
        """Persist an accepted question into QuestionHistory."""
        q_text = question_dict.get("question", "").strip()
        if not q_text:
            return

        norm_q = normalize_question(q_text)

        # Avoid inserting duplicate into QuestionHistory
        existing = (
            db.query(QuestionHistory)
            .filter(QuestionHistory.normalized_question == norm_q)
            .first()
        )
        if existing:
            return

        rec = QuestionHistory(
            id=str(uuid.uuid4()),
            interview_id=interview_id,
            question_text=q_text,
            normalized_question=norm_q,
            category=question_dict.get("category", interview_type),
            job_role=job_role,
            difficulty=question_dict.get("difficulty", "medium"),
            interview_type=interview_type,
        )
        db.add(rec)
        db.commit()
        logger.info(f"Recorded new question in history: '{q_text[:60]}...'")


question_dedup_service = QuestionDedupService()
