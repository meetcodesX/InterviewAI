"""Persistent Question Deduplication and Semantic Duplicate Detection.

Ensures questions are not repeated within an interview or across new interviews.
Supports both embedding-based cosine similarity (when SentenceTransformer is loaded)
and zero-dependency token/n-gram Jaccard matching for lightweight serverless deployments.
"""

import re
import uuid
import logging
from typing import Tuple, List, Optional
from sqlalchemy.orm import Session

from config import settings
from models.models import QuestionHistory
from services.rag_service import rag_service

logger = logging.getLogger(__name__)


def normalize_question(text: str) -> str:
    """Normalize question string for exact matching (lowercase, no punctuation, single spaces)."""
    if not text:
        return ""
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

        # 3. Retrieve historical questions for semantic / token comparison
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

            if not history_texts:
                return False, 0.0, ""

            # 3A. Semantic similarity check via SentenceTransformer (if available)
            if rag_service.model is not None:
                try:
                    import numpy as np
                    cand_emb = rag_service.model.encode([candidate_question])
                    hist_embs = rag_service.model.encode(history_texts)

                    cand_norm = cand_emb / (np.linalg.norm(cand_emb, axis=1, keepdims=True) + 1e-9)
                    hist_norm = hist_embs / (np.linalg.norm(hist_embs, axis=1, keepdims=True) + 1e-9)

                    sims = np.dot(cand_norm, hist_norm.T)[0]
                    max_idx = int(np.argmax(sims))
                    max_sim = float(sims[max_idx])

                    if max_sim >= self.threshold:
                        matched = history_texts[max_idx]
                        return True, max_sim, f"Semantic duplicate ({max_sim:.2f} >= {self.threshold}): '{matched}'"

                    return False, max_sim, ""
                except Exception as model_err:
                    logger.warning(f"SentenceTransformer check failed: {model_err}. Falling back to token matching.")

            # 3B. Built-in fast token & n-gram Jaccard duplicate detection (zero-dependency)
            cand_tokens = set(re.findall(r"\b\w{3,}\b", candidate_question.lower()))
            cand_words = re.findall(r"\b\w+\b", candidate_question.lower())
            cand_bigrams = set(zip(cand_words[:-1], cand_words[1:])) if len(cand_words) > 1 else set()

            best_sim = 0.0
            best_match = ""

            for hist_q in history_texts:
                hist_tokens = set(re.findall(r"\b\w{3,}\b", hist_q.lower()))
                hist_words = re.findall(r"\b\w+\b", hist_q.lower())
                hist_bigrams = set(zip(hist_words[:-1], hist_words[1:])) if len(hist_words) > 1 else set()

                token_union = cand_tokens | hist_tokens
                token_jaccard = (len(cand_tokens & hist_tokens) / len(token_union)) if token_union else 0.0

                bigram_union = cand_bigrams | hist_bigrams
                bigram_jaccard = (len(cand_bigrams & hist_bigrams) / len(bigram_union)) if bigram_union else 0.0

                sim = 0.5 * token_jaccard + 0.5 * bigram_jaccard if bigram_union else token_jaccard

                if sim > best_sim:
                    best_sim = sim
                    best_match = hist_q

            # Semantic threshold for token/bigram similarity
            sem_threshold = min(self.threshold, 0.75)
            if best_sim >= sem_threshold:
                return True, best_sim, f"Semantic duplicate ({best_sim:.2f} >= {sem_threshold}): '{best_match}'"

            return False, best_sim, ""
        except Exception as e:
            logger.error(f"Duplicate check error: {e}")
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
