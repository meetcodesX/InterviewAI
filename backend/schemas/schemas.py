"""Pydantic schemas for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# ================================================================
# Enums
# ================================================================

class ExperienceLevel(str, Enum):
    FRESHER = "fresher"
    JUNIOR = "0-2 years"
    MID = "2-5 years"
    SENIOR = "5+ years"


class InterviewType(str, Enum):
    TECHNICAL = "technical"
    HR = "hr"
    BEHAVIORAL = "behavioral"
    MIXED = "mixed"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    ADAPTIVE = "adaptive"


# ================================================================
# Candidate Profile
# ================================================================

class CandidateProfile(BaseModel):
    name: str = ""
    education: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    experience: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    target_role: str = ""
    experience_level: str = ""
    years_of_experience: int = 0


# ================================================================
# Interview Configuration
# ================================================================

class InterviewConfig(BaseModel):
    job_role: str
    experience_level: str = "fresher"
    interview_type: str = "mixed"
    difficulty: str = "adaptive"
    num_questions: int = 10


# ================================================================
# Request Schemas
# ================================================================

class InterviewCreateRequest(BaseModel):
    profile: CandidateProfile
    config: InterviewConfig


class AnswerSubmitRequest(BaseModel):
    interview_id: str
    question_id: str
    answer: str


class ProfileExtractRequest(BaseModel):
    resume_text: str


class ManualProfileRequest(BaseModel):
    name: str
    target_role: str
    experience_level: str
    skills: str
    years_of_experience: int = 0


class NextQuestionRequest(BaseModel):
    interview_id: str


class FinishInterviewRequest(BaseModel):
    interview_id: str


# ================================================================
# Response Schemas
# ================================================================

class QuestionResponse(BaseModel):
    question_id: str
    question_number: int
    total_questions: int
    category: str
    difficulty: str
    question: str
    interview_id: str


class EvaluationResponse(BaseModel):
    overall_score: int = Field(ge=0, le=10, default=5)
    technical_accuracy: int = Field(ge=0, le=10, default=5)
    relevance: int = Field(ge=0, le=10, default=5)
    clarity: int = Field(ge=0, le=10, default=5)
    completeness: int = Field(ge=0, le=10, default=5)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    feedback: str = ""
    recommended_difficulty: str = "medium"


class AnswerEvaluationResponse(BaseModel):
    question_id: str
    question: str
    answer: str
    evaluation: EvaluationResponse


class InterviewReport(BaseModel):
    interview_id: str
    candidate_name: str = ""
    target_role: str = ""
    overall_score: int = 0
    technical_score: int = 0
    communication_score: int = 0
    problem_solving_score: int = 0
    role_readiness_score: int = 0
    questions_answered: int = 0
    total_questions: int = 0
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    difficulty_progression: List[str] = Field(default_factory=list)
    question_evaluations: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: str = ""


class HealthResponse(BaseModel):
    status: str
    ai_provider: str
    rag_status: str
    version: str


class ResumeUploadResponse(BaseModel):
    resume_text: str
    profile: CandidateProfile


class InterviewStatusResponse(BaseModel):
    interview_id: str
    status: str
    current_question: int
    total_questions: int
    profile: Optional[CandidateProfile] = None
    config: Optional[InterviewConfig] = None


class DashboardStats(BaseModel):
    total_interviews: int = 0
    average_score: int = 0
    strongest_skill: str = ""
    weakest_skill: str = ""
    recent_interviews: List[Dict[str, Any]] = Field(default_factory=list)
    score_history: List[Dict[str, Any]] = Field(default_factory=list)
