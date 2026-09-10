"""Google Gemini LLM Service for InterviewAI.

Powers:
- Role-specific question generation with RAG context
- Candidate answer evaluation against industry rubric
- Adaptive difficulty progression
- Final comprehensive performance report
- Resume profile extraction
"""

import os
import re
import json
import uuid
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from config import settings
from schemas.schemas import CandidateProfile, EvaluationResponse, InterviewReport
from services.rag_service import rag_service
from services.resume_parser import parse_resume_text

logger = logging.getLogger(__name__)


class GeminiService:
    """Service wrapping Google Gemini API with intelligent offline fallback for development."""

    def __init__(self):
        self.is_mock = settings.is_mock
        self.client = None
        self.is_connected = False
        self.model_name = settings.GEMINI_MODEL

        api_key = settings.GEMINI_API_KEY
        if api_key and api_key != "your_gemini_api_key_here":
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
                self.is_connected = True
                self.is_mock = False
                logger.info(f"GeminiService successfully initialized with model {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}. Falling back to offline mode.")
                self.client = None
                self.is_connected = False
                self.is_mock = True
        else:
            logger.info("GEMINI_API_KEY not configured. Running in offline/mock mode.")
            self.is_mock = True

    def _parse_json(self, raw_text: str) -> dict:
        """Robust parser that extracts valid JSON from markdown code blocks or raw strings."""
        if not raw_text:
            return {}
        text = raw_text.strip()
        # Strip ```json ... ``` or ``` ... ```
        if "```" in text:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
            if match:
                text = match.group(1).strip()

        # Direct JSON decode
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try finding outer braces
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
        return {}

    def generate(self, prompt: str) -> str:
        """Invokes Gemini API and returns raw text output."""
        if self.is_mock or not self.client:
            raise RuntimeError("Gemini is not configured or in mock mode")
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text or ""
        except Exception as e:
            logger.error(f"Gemini API invocation failed: {e}", exc_info=True)
            raise e

    # ------------------------------------------------------------------
    # Profile Extraction
    # ------------------------------------------------------------------
    def extract_profile(self, resume_text: str) -> CandidateProfile:
        """Extracts structured candidate profile from resume text using Gemini or heuristic parser."""
        if not self.is_mock and self.is_connected:
            prompt = f"""You are an expert technical recruiter. Analyze the following resume text and extract the candidate's professional profile.
Strictly adhere to the candidate's actual resume content. Do NOT invent a name or skills.

Resume Text:
{resume_text[:4000]}

Return ONLY a valid JSON object matching this schema:
{{
  "name": "Candidate Full Name",
  "target_role": "Primary Job Title or Target Role",
  "experience_level": "Fresher | Junior | Mid | Senior",
  "skills": ["Skill1", "Skill2", "Skill3"],
  "years_of_experience": 0,
  "education": ["Degree - Institution"],
  "projects": ["Project Title - Brief Description"],
  "experience": ["Role at Company"],
  "certifications": ["Certification Name"]
}}"""
            try:
                raw_output = self.generate(prompt)
                data = self._parse_json(raw_output)
                if data and data.get("name") and data["name"] != "Candidate Full Name":
                    return CandidateProfile(**data)
            except Exception as e:
                logger.warning(f"Gemini profile extraction failed: {e}. Using heuristic parser.")

        # Heuristic offline fallback
        return parse_resume_text(resume_text)

    # ------------------------------------------------------------------
    # Question Generation
    # ------------------------------------------------------------------
    def generate_question(self, context: dict) -> dict:
        """Generates role-specific interview question adhering to RAG context and avoiding duplicates."""
        profile = context.get("candidate_profile", {})
        role = context.get("job_role") or profile.get("target_role", "Software Engineer")
        skills = profile.get("skills", [])
        difficulty = context.get("difficulty", "medium")
        category = context.get("category", "technical")
        rag_context = context.get("rag_context", "")
        excluded = context.get("excluded_questions", [])

        if not self.is_mock and self.is_connected:
            skills_str = ", ".join(skills[:8]) if skills else "relevant industry skills"
            excluded_str = "\n".join(f"- {q}" for q in excluded[-10:]) if excluded else "None"

            prompt = f"""You are an experienced technical interviewer interviewing a candidate for the role of {role} (Experience: {profile.get('experience_level', 'Fresher')}).

INTERVIEW PARAMETERS:
- Target Role: {role}
- Candidate Skills: {skills_str}
- Category: {category}
- Difficulty Level: {difficulty}

CURATED DOMAIN KNOWLEDGE (RAG CONTEXT):
{rag_context if rag_context else 'Assess standard technical competencies and problem-solving principles for this role.'}

DO NOT ASK ANY QUESTION SIMILAR TO THESE PREVIOUSLY ASKED QUESTIONS:
{excluded_str}

REQUIREMENTS:
1. Generate ONE focused, realistic interview question appropriate for {difficulty} level.
2. Directly evaluate relevant skills or architectural knowledge for {role}.
3. The question must be novel and NOT repeated.

Return ONLY valid JSON matching this schema:
{{
  "question": "Your interview question here?",
  "category": "{category}",
  "difficulty": "{difficulty}"
}}"""
            try:
                raw_output = self.generate(prompt)
                data = self._parse_json(raw_output)
                if data and data.get("question"):
                    data["difficulty"] = difficulty
                    data["category"] = category
                    return data
            except Exception as e:
                logger.warning(f"Gemini question generation failed: {e}. Using knowledge base selection.")

        # Offline deterministic selection from knowledge base
        return self._offline_generate_question(role, skills, difficulty, category, excluded)

    def _offline_generate_question(
        self,
        role: str,
        skills: List[str],
        difficulty: str,
        category: str,
        excluded: List[str]
    ) -> dict:
        """Deterministically selects an unasked question from RAG markdown files or built-in pool."""
        norm_excluded = {
            " ".join(re.sub(r"[^\w\s]", "", q.lower()).split())
            for q in excluded if q
        }

        # 1. Try finding an unasked question from the RAG markdown knowledge base files
        kb_q = rag_service.get_unasked_knowledge_question(
            category=category if category != "technical" else role,
            difficulty=difficulty,
            asked_normalized_questions=norm_excluded
        )
        if kb_q and kb_q.get("question"):
            return kb_q

        # 2. Built-in diverse question pool
        pool = self._BUILTIN_POOLS.get(difficulty.lower(), self._BUILTIN_POOLS["medium"])
        for item in pool:
            norm_q = " ".join(re.sub(r"[^\w\s]", "", item["question"].lower()).split())
            if norm_q not in norm_excluded:
                return dict(item)

        # 3. Dynamic fallback if all predefined were asked
        unique_id = str(uuid.uuid4())[:6]
        skill_name = skills[0] if skills else role
        return {
            "question": f"Discuss the core design considerations, trade-offs, and operational bottlenecks when scaling {skill_name} in production (Ref: {unique_id}).",
            "category": category,
            "difficulty": difficulty
        }

    # ------------------------------------------------------------------
    # Answer Evaluation
    # ------------------------------------------------------------------
    def evaluate_answer(self, question: str, answer: str, context: dict) -> EvaluationResponse:
        """Evaluates candidate answer adhering strictly to rubric and technical accuracy."""
        profile = context.get("candidate_profile", {})
        job_role = context.get("job_role") or profile.get("target_role", "Software Engineer")
        difficulty = context.get("difficulty", "medium")
        rag_context = context.get("rag_context", "")

        parsed_data = {}
        raw_output = ""

        if not self.is_mock and self.is_connected:
            prompt = f"""You are a senior technical interviewer and subject matter expert evaluating a candidate for the role of {job_role}.

QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

REFERENCE DOMAIN KNOWLEDGE (RAG CONTEXT):
{rag_context if rag_context else 'Evaluate against standard software engineering and role-specific principles.'}

EVALUATION RUBRIC:
- Evaluate semantic correctness, problem-solving, and technical validity.
- Recognize valid alternative approaches (e.g. for class imbalance: SMOTE, class weighting, focal loss, PR-AUC).
- Thorough, technically accurate answers MUST receive high marks (8–10).
- Partially correct answers with sound reasoning but minor gaps receive (5–7).
- Incomplete, evasive, or incorrect answers receive (0–4).
- Overall score formula: round(0.35 * technical_accuracy + 0.25 * relevance + 0.20 * clarity + 0.20 * completeness).

Return ONLY valid JSON matching this schema:
{{
  "overall_score": 8,
  "technical_accuracy": 8,
  "relevance": 9,
  "clarity": 8,
  "completeness": 8,
  "strengths": ["Strengths identified in the answer"],
  "weaknesses": ["Areas for improvement"],
  "feedback": "2-3 constructive feedback sentences.",
  "recommended_difficulty": "easy | medium | hard"
}}"""
            try:
                raw_output = self.generate(prompt)
                parsed_data = self._parse_json(raw_output)
            except Exception as e:
                logger.error(f"Gemini evaluation failed: {e}. Using rubric scoring engine.")

        if not parsed_data or "overall_score" not in parsed_data:
            parsed_data = self._rubric_evaluate_answer(question, answer, rag_context, job_role, difficulty)
            raw_output = json.dumps(parsed_data)

        # Ensure consistent weighted overall_score calculation
        tech = int(parsed_data.get("technical_accuracy", 5))
        rel = int(parsed_data.get("relevance", 5))
        cla = int(parsed_data.get("clarity", 5))
        comp = int(parsed_data.get("completeness", 5))

        calculated_overall = int(round(0.35 * tech + 0.25 * rel + 0.20 * cla + 0.20 * comp))
        parsed_data["overall_score"] = max(0, min(10, calculated_overall))

        for k in ("overall_score", "technical_accuracy", "relevance", "clarity", "completeness"):
            if k in parsed_data:
                parsed_data[k] = max(0, min(10, int(parsed_data[k])))

        return EvaluationResponse(**parsed_data)

    def _rubric_evaluate_answer(
        self,
        question: str,
        answer: str,
        rag_context: str,
        job_role: str,
        difficulty: str
    ) -> dict:
        """Intelligent semantic scoring engine based on concept coverage and word count."""
        cleaned_ans = answer.strip()
        ans_lower = cleaned_ans.lower()
        words = re.findall(r"\b\w+\b", ans_lower)
        word_count = len(words)

        # Empty or evasive response
        if word_count < 6 or any(ans_lower == phrase for phrase in [
            "i don't know", "idk", "no idea", "not sure", "pass", "skip", "i do not know"
        ]):
            return {
                "overall_score": 1,
                "technical_accuracy": 1,
                "relevance": 2,
                "clarity": 2,
                "completeness": 1,
                "strengths": ["Acknowledged unfamiliarity with the topic"],
                "weaknesses": ["No technical explanation provided", "Question was not answered"],
                "feedback": "You did not provide an answer. Review foundational concepts for this topic and practice answering with structured definitions.",
                "recommended_difficulty": "easy"
            }

        domain_keywords = [
            "supervised", "unsupervised", "reinforcement", "clustering", "classification",
            "regression", "overfitting", "underfitting", "bias", "variance", "regularization",
            "precision", "recall", "f1", "roc-auc", "pr-auc", "smote", "imbalance",
            "cross-validation", "gradient", "backpropagation", "loss", "optimizer",
            "rag", "retrieval", "embeddings", "vector", "chunking", "chromadb", "langchain",
            "acid", "atomicity", "consistency", "isolation", "durability", "transaction",
            "index", "indexing", "latency", "throughput", "cache", "caching", "rest", "api"
        ]

        found_concepts = [kw for kw in domain_keywords if kw in ans_lower]
        concept_count = len(found_concepts)

        ref_words = set(re.findall(r"\b\w{3,}\b", (question + " " + (rag_context or "")).lower()))
        ans_meaningful = set(re.findall(r"\b\w{3,}\b", ans_lower))
        overlap = len(ans_meaningful & ref_words) if ref_words else 0
        sim_score = min(1.0, overlap / max(5.0, len(ans_meaningful) * 0.4)) if ans_meaningful else 0.5

        if (concept_count >= 3 and word_count >= 20) or (sim_score >= 0.6 and word_count >= 30) or word_count >= 70:
            tech_acc = min(10, 8 + (1 if concept_count >= 4 else 0) + (1 if word_count >= 40 else 0))
            relevance = min(10, 8 + (1 if sim_score >= 0.5 else 0))
            clarity = min(10, 8 + (1 if "." in cleaned_ans else 0))
            completeness = min(10, 7 + (1 if concept_count >= 3 else 0) + (1 if word_count >= 50 else 0))

            strengths = [
                f"Accurately incorporated technical concepts: {', '.join(found_concepts[:4])}" if found_concepts else "Strong technical understanding demonstrated",
                "Structured and logically coherent explanation",
                "Directly answered the core challenge posed by the question"
            ]
            weaknesses = [
                "Could further elaborate on production edge cases or operational trade-offs"
            ]
            feedback = "Excellent response! You demonstrated solid technical depth, correct terminology, and articulated your reasoning clearly."
            rec_diff = "hard" if difficulty != "hard" else "hard"

        elif (concept_count >= 1 and word_count >= 15) or (sim_score >= 0.4 and word_count >= 20):
            tech_acc = 6
            relevance = 7
            clarity = 6
            completeness = 5
            strengths = [
                f"Demonstrated awareness of core principles ({', '.join(found_concepts[:2])})" if found_concepts else "Identified fundamental concepts",
                "Relevant response to the question"
            ]
            weaknesses = [
                "Could provide deeper algorithmic or implementation details",
                "Explanation is somewhat brief"
            ]
            feedback = "Good answer that captures the basics. To improve, elaborate on specific implementation steps and compare alternative techniques."
            rec_diff = "medium"

        else:
            tech_acc = 4
            relevance = 5
            clarity = 4
            completeness = 3
            strengths = ["Attempted to answer the question"]
            weaknesses = [
                "Answer lacks technical depth and specific methodologies",
                "Missed important domain concepts and trade-offs"
            ]
            feedback = "Your response touches on the subject but lacks technical precision. Review the core mechanics and practice giving detailed examples."
            rec_diff = "easy"

        return {
            "overall_score": int(round(0.35 * tech_acc + 0.25 * relevance + 0.20 * clarity + 0.20 * completeness)),
            "technical_accuracy": tech_acc,
            "relevance": relevance,
            "clarity": clarity,
            "completeness": completeness,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "feedback": feedback,
            "recommended_difficulty": rec_diff
        }

    # ------------------------------------------------------------------
    # Final Report Generation
    # ------------------------------------------------------------------
    def generate_report(self, interview_data: dict) -> InterviewReport:
        """Generates comprehensive final evaluation report using Gemini or synthesis engine."""
        profile = interview_data.get("candidate_profile", {})
        candidate_name = profile.get("name", "Candidate")
        job_role = interview_data.get("config", {}).get("job_role", "Software Engineer")
        evaluations = interview_data.get("evaluations", [])
        questions = interview_data.get("questions", [])
        diff_progression = interview_data.get("difficulty_progression", [])

        # Compute baseline numeric averages
        if evaluations:
            avg_overall = sum(e.get("overall_score", 5) for e in evaluations) / len(evaluations)
            avg_tech = sum(e.get("technical_accuracy", 5) for e in evaluations) / len(evaluations)
            avg_rel = sum(e.get("relevance", 5) for e in evaluations) / len(evaluations)
            avg_clarity = sum(e.get("clarity", 5) for e in evaluations) / len(evaluations)
        else:
            avg_overall, avg_tech, avg_rel, avg_clarity = 5.0, 5.0, 5.0, 5.0

        # Scale scores to 0-100
        overall_100 = int(round(avg_overall * 10))
        tech_100 = int(round(avg_tech * 10))
        comm_100 = int(round(avg_clarity * 10))
        prob_100 = int(round(avg_rel * 10))

        interview_id = str(interview_data.get("interview_id", ""))
        questions_answered = len(evaluations)
        total_questions = int(interview_data.get("config", {}).get("num_questions", len(questions) or 10))

        # Reconstruct question_evaluations list for report breakdown
        question_evaluations = []
        for idx, (q, ev) in enumerate(zip(questions, evaluations)):
            q_text = q.get("question", f"Question {idx+1}") if isinstance(q, dict) else str(q)
            q_ans = ""
            if "answers" in interview_data and idx < len(interview_data["answers"]):
                a_item = interview_data["answers"][idx]
                q_ans = a_item.get("answer", "") if isinstance(a_item, dict) else str(a_item)
            question_evaluations.append({
                "question": q_text,
                "answer": q_ans,
                "score": ev.get("overall_score", 0),
                "feedback": ev.get("feedback", ""),
                "evaluation": ev
            })

        if not self.is_mock and self.is_connected and evaluations:
            eval_summary = []
            for idx, (q, ev) in enumerate(zip(questions, evaluations)):
                q_text = q.get("question", f"Question {idx+1}") if isinstance(q, dict) else str(q)
                score = ev.get("overall_score", 5)
                fb = ev.get("feedback", "")
                eval_summary.append(f"Q{idx+1} ({ev.get('difficulty', 'medium')}): {q_text}\nScore: {score}/10 | Feedback: {fb}")

            prompt = f"""You are a principal engineering hiring manager synthesizing an interview report for {candidate_name} applying for {job_role}.

INTERVIEW PERFORMANCE SUMMARY:
{chr(10).join(eval_summary)}

SCORES CALCULATED:
- Overall Score: {overall_100}/100
- Technical Accuracy: {tech_100}/100
- Communication: {comm_100}/100
- Problem Solving: {prob_100}/100

TASK:
Produce an actionable, detailed candidate assessment report.
Return ONLY valid JSON matching this schema:
{{
  "overall_score": {overall_100},
  "technical_score": {tech_100},
  "communication_score": {comm_100},
  "problem_solving_score": {prob_100},
  "role_readiness": "Ready | Needs Improvement | Exceptional",
  "strongest_skills": ["Skill 1", "Skill 2"],
  "weakest_skills": ["Skill 1", "Skill 2"],
  "recommended_learning": ["Topic 1", "Topic 2", "Topic 3"],
  "summary": "3-4 sentence comprehensive narrative summary of candidate performance.",
  "roadmap": ["Step 1", "Step 2", "Step 3"]
}}"""
            try:
                raw_output = self.generate(prompt)
                data = self._parse_json(raw_output)
                if data and "summary" in data:
                    data["interview_id"] = interview_id
                    data["candidate_name"] = candidate_name
                    data["target_role"] = job_role
                    data["overall_score"] = overall_100
                    data["technical_score"] = tech_100
                    data["communication_score"] = comm_100
                    data["problem_solving_score"] = prob_100
                    data["role_readiness_score"] = overall_100
                    data["questions_answered"] = questions_answered
                    data["total_questions"] = total_questions
                    data["strengths"] = data.get("strongest_skills", [])
                    data["weaknesses"] = data.get("weakest_skills", [])
                    data["recommendations"] = data.get("recommended_learning", [])
                    data["difficulty_progression"] = diff_progression
                    data["question_evaluations"] = question_evaluations
                    return InterviewReport(**data)
            except Exception as e:
                logger.warning(f"Gemini report generation failed: {e}. Using synthesis engine.")

        # Offline synthesis fallback
        readiness = "Ready" if overall_100 >= 75 else ("Developing" if overall_100 >= 50 else "Needs Improvement")
        all_strengths = []
        all_weaknesses = []
        for ev in evaluations:
            all_strengths.extend(ev.get("strengths", []))
            all_weaknesses.extend(ev.get("weaknesses", []))

        strongest = list(dict.fromkeys(all_strengths))[:3] or ["Demonstrated foundational technical knowledge", "Logical problem-solving approach"]
        weakest = list(dict.fromkeys(all_weaknesses))[:3] or ["Elaborating on production edge cases", "Providing deeper architectural trade-offs"]

        learning_recs = [
            f"Review advanced architectural patterns and scalability practices for {job_role}",
            "Practice structuring answers using Situation-Task-Action-Result with concrete metrics",
            "Deep-dive into performance optimization, caching strategies, and system failure modes"
        ]

        summary = (
            f"{candidate_name} completed the {job_role} technical interview with an overall score of {overall_100}/100. "
            f"The candidate demonstrated solid problem-solving ({prob_100}/100) and communication skills ({comm_100}/100). "
            f"Recommended focus area is deepening technical implementation details and production operational trade-offs."
        )

        roadmap = [
            "Week 1-2: Core concept deep-dive and code implementation practice",
            "Week 3-4: Build hands-on end-to-end projects demonstrating scalable architectures",
            "Week 5+: Mock interview sessions focusing on concise, structured technical articulation"
        ]

        return InterviewReport(
            interview_id=interview_id,
            candidate_name=candidate_name,
            target_role=job_role,
            overall_score=overall_100,
            technical_score=tech_100,
            communication_score=comm_100,
            problem_solving_score=prob_100,
            role_readiness_score=overall_100,
            questions_answered=questions_answered,
            total_questions=total_questions,
            strengths=strongest,
            weaknesses=weakest,
            recommendations=learning_recs,
            difficulty_progression=diff_progression,
            question_evaluations=question_evaluations
        )

    _BUILTIN_POOLS = {
        "easy": [
            {
                "question": "What is the STAR method, and how do you effectively structure behavioral responses using it?",
                "category": "behavioral",
                "difficulty": "easy"
            },
            {
                "question": "Explain the difference between mutable and immutable types in Python with examples.",
                "category": "python",
                "difficulty": "easy"
            },
            {
                "question": "What is the primary difference between supervised and unsupervised machine learning?",
                "category": "machine_learning",
                "difficulty": "easy"
            }
        ],
        "medium": [
            {
                "question": "How do you handle class imbalance in a classification dataset, and what evaluation metrics are appropriate?",
                "category": "machine_learning",
                "difficulty": "medium"
            },
            {
                "question": "Explain how Retrieval-Augmented Generation (RAG) works, and discuss how chunk size and chunk overlap affect retrieval quality.",
                "category": "rag",
                "difficulty": "medium"
            },
            {
                "question": "What are ACID properties in database transactions, and how does each ensure data integrity?",
                "category": "sql",
                "difficulty": "medium"
            }
        ],
        "hard": [
            {
                "question": "Describe the architecture of a high-throughput real-time streaming feature pipeline with sub-second latency and exactly-once processing guarantees.",
                "category": "system_design",
                "difficulty": "hard"
            },
            {
                "question": "How would you mitigate hallucination in production RAG systems using reranking, guardrails, and citation verification?",
                "category": "generative_ai",
                "difficulty": "hard"
            },
            {
                "question": "Explain how attention mechanisms function in Transformers, and analyze the computational complexity of standard self-attention versus FlashAttention.",
                "category": "deep_learning",
                "difficulty": "hard"
            }
        ]
    }


gemini_service = GeminiService()
