"""SQLAlchemy ORM models for interview data persistence."""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.sql import func
from database.db import Base


class Interview(Base):
    """Stores interview sessions with their full state."""
    __tablename__ = "interviews"

    id = Column(String, primary_key=True)
    candidate_name = Column(String, nullable=False, default="")
    candidate_profile = Column(JSON, default=dict)
    config = Column(JSON, default=dict)
    status = Column(String, default="in_progress")  # in_progress, completed
    current_question_index = Column(Integer, default=0)
    questions = Column(JSON, default=list)
    answers = Column(JSON, default=list)
    evaluations = Column(JSON, default=list)
    difficulty_progression = Column(JSON, default=list)
    report = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class InterviewQuestion(Base):
    """Individual question records within an interview."""
    __tablename__ = "interview_questions"

    id = Column(String, primary_key=True)
    interview_id = Column(String, nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    evaluation = Column(JSON, nullable=True)
    category = Column(String, default="")
    difficulty = Column(String, default="medium")
    question_number = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


class QuestionHistory(Base):
    """Persistent store of previously asked questions across all interviews.
    
    Used for semantic deduplication to prevent question repetition.
    """
    __tablename__ = "question_history"

    id = Column(String, primary_key=True)
    interview_id = Column(String, nullable=True, index=True)
    question_text = Column(Text, nullable=False)
    normalized_question = Column(Text, nullable=False, index=True)
    category = Column(String, default="")
    job_role = Column(String, default="")
    difficulty = Column(String, default="medium")
    interview_type = Column(String, default="technical")
    created_at = Column(DateTime, server_default=func.now())
