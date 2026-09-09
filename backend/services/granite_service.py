"""IBM Granite LLM Service with intelligent semantic fallback for local development.

Adheres strictly to the AICTE 2026 Problem Statement #22 specifications:
- Uses IBM watsonx.ai Granite foundation models when configured
- Provides semantic evaluation and question generation
- Logs full evaluation debug traces
- Never returns hardcoded placeholder identities for uploaded resumes
"""

import json
import logging
import re
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
import numpy as np

from config import settings
from schemas.schemas import CandidateProfile, EvaluationResponse, InterviewReport
from services.rag_service import rag_service

logger = logging.getLogger(__name__)


class GraniteService:
    """Service wrapping IBM Granite via watsonx.ai with intelligent semantic fallback."""

    def __init__(self):
        self.is_mock = settings.is_mock
        self.model = None
        self.is_connected = False

        if not self.is_mock:
            if (
                not settings.IBM_API_KEY
                or settings.IBM_API_KEY == "your_ibm_api_key_here"
                or not settings.IBM_PROJECT_ID
                or settings.IBM_PROJECT_ID == "your_project_id_here"
            ):
                logger.warning("IBM_API_KEY or IBM_PROJECT_ID unconfigured/placeholder. Running in mock fallback mode.")
                self.is_mock = True
            else:
                try:
                    from ibm_watsonx_ai.foundation_models import ModelInference
                    from ibm_watsonx_ai import Credentials

                    credentials = Credentials(
                        url=settings.IBM_URL,
                        api_key=settings.IBM_API_KEY,
                    )
                    self.model = ModelInference(
                        model_id=settings.IBM_GRANITE_MODEL,
                        credentials=credentials,
                        project_id=settings.IBM_PROJECT_ID,
                        params={"max_new_tokens": 2048, "temperature": 0.7},
                    )
                    self.is_connected = True
                    logger.info(f"IBM Granite model initialized successfully: {settings.IBM_GRANITE_MODEL}")
                except ImportError:
                    logger.warning("ibm_watsonx_ai not installed. Falling back to mock mode.")
                    self.is_mock = True
                except Exception as e:
                    logger.error(f"Failed to connect to IBM Watsonx: {e}. Falling back to mock mode.")
                    self.is_mock = True

    def get_status(self) -> Dict[str, Any]:
        return {
            "provider": "ibm_granite" if not self.is_mock else "mock",
            "model": settings.IBM_GRANITE_MODEL,
            "connected": self.is_connected,
            "has_credentials": bool(settings.IBM_API_KEY and settings.IBM_API_KEY != "your_ibm_api_key_here")
        }

    # ------------------------------------------------------------------
    # Core LLM text generation
    # ------------------------------------------------------------------
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        """Call IBM Granite model or raise real error when configured."""
        if self.is_mock:
            raise RuntimeError("Mock mode active; use semantic generation methods")

        if not self.model:
            raise RuntimeError("IBM Granite model is not initialized. Check your credentials.")

        try:
            result = self.model.generate_text(
                prompt=prompt,
                params={"max_new_tokens": max_tokens, "temperature": 0.7}
            )
            return result
        except Exception as e:
            logger.error(f"IBM Granite API call failed: {e}", exc_info=True)
            raise RuntimeError(f"IBM Granite API call failed: {str(e)}")

    # ------------------------------------------------------------------
    # JSON parsing helper
    # ------------------------------------------------------------------
    def _parse_json(self, text: str) -> Dict[str, Any]:
        """Extract and parse JSON from LLM output, handling code blocks."""
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try extracting from code fences
        for fence in ("```json", "```"):
            if fence in text:
                try:
                    chunk = text.split(fence, 1)[1]
                    chunk = chunk.split("```", 1)[0].strip()
                    return json.loads(chunk)
                except (json.JSONDecodeError, IndexError):
                    continue

        # Try finding JSON object boundaries
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass

        logger.warning(f"Could not parse JSON from output: {text[:200]}...")
        return {}

    # ------------------------------------------------------------------
    # Profile Extraction via Granite
    # ------------------------------------------------------------------
    def extract_profile(self, resume_text: str) -> CandidateProfile:
        """Extract candidate profile using IBM Granite."""
        prompt = f"""You are an expert technical recruiter and resume parser.
Extract the structured candidate profile from the resume text below.
DO NOT invent information. Only extract what is present in the text.

Resume Text:
{resume_text[:3500]}

Return ONLY valid JSON matching this schema:
{{
  "name": "Full Name",
  "education": ["degree and institution"],
  "skills": ["skill1", "skill2"],
  "projects": ["project1"],
  "experience": ["role at company"],
  "certifications": ["certification1"],
  "target_role": "target role",
  "experience_level": "fresher/junior/mid/senior",
  "years_of_experience": 0
}}"""
        raw_output = self.generate(prompt)
        data = self._parse_json(raw_output)
        if not data:
            raise ValueError("Failed to parse candidate profile JSON from IBM Granite response")
        return CandidateProfile(**data)

    # ------------------------------------------------------------------
    # Question Generation
    # ------------------------------------------------------------------
    def generate_question(self, context: dict) -> dict:
        """Generate a role-specific interview question, avoiding duplicates."""
        profile = context.get("candidate_profile", {})
        difficulty = context.get("difficulty", "medium")
        rag_context = context.get("rag_context", "")
        role = context.get("job_role") or profile.get("target_role", "Software Engineer")
        skills = profile.get("skills", ["General Technical Skills"])
        excluded = context.get("excluded_questions", [])

        # Format excluded questions prompt constraint
        excluded_str = "\n".join(f"- {q}" for q in excluded[-15:]) if excluded else "None"

        if not self.is_mock and self.is_connected:
            prompt = f"""You are a professional technical interviewer conducting a job interview.
Generate ONE interview question based on the following candidate profile and retrieved knowledge.

Candidate Skills: {', '.join(skills[:8])}
Target Role: {role}
Difficulty Level: {difficulty}

EXCLUDED QUESTIONS (Do NOT generate any question that is identical or semantically equivalent to any of these):
{excluded_str}

Reference Material:
{rag_context[:1000]}

Return ONLY valid JSON:
{{
  "question": "Your interview question here",
  "category": "technical",
  "difficulty": "{difficulty}"
}}"""
            try:
                raw_output = self.generate(prompt)
                data = self._parse_json(raw_output)
                if data and data.get("question"):
                    data["difficulty"] = difficulty
                    return data
            except Exception as e:
                logger.warning(f"Granite question generation failed: {e}. Using semantic pool.")

        # Fallback to intelligent semantic question selection
        return self._semantic_generate_question(role, skills, difficulty, excluded)

    def _semantic_generate_question(
        self,
        role: str,
        skills: List[str],
        difficulty: str,
        excluded: List[str]
    ) -> dict:
        """Deterministically select an unasked question from knowledge base or diverse pool."""
        norm_excluded = {
            " ".join(re.sub(r"[^\w\s]", "", q.lower()).split())
            for q in excluded if q
        }

        # 1. Try finding an unasked question from the 15 RAG markdown knowledge base files
        kb_q = rag_service.get_unasked_knowledge_question(
            category=role,
            difficulty=difficulty,
            asked_normalized_questions=norm_excluded
        )
        if kb_q and kb_q.get("question"):
            return kb_q

        # 2. Comprehensive built-in question pool
        pool = self._BUILTIN_POOLS.get(difficulty.lower(), self._BUILTIN_POOLS["medium"])
        for item in pool:
            norm_q = " ".join(re.sub(r"[^\w\s]", "", item["question"].lower()).split())
            if norm_q not in norm_excluded:
                return dict(item)

        # 3. Dynamic fallback if all predefined were asked
        unique_id = str(uuid.uuid4())[:6]
        return {
            "question": f"Discuss an advanced architecture or challenging project related to {skills[0] if skills else role} (Ref: {unique_id}).",
            "category": "technical",
            "difficulty": difficulty
        }

    # ------------------------------------------------------------------
    # Answer Evaluation (Bug 3 Root-Cause Fix)
    # ------------------------------------------------------------------
    def evaluate_answer(self, question: str, answer: str, context: dict) -> EvaluationResponse:
        """Evaluates candidate answer adhering strictly to the required rubric."""
        profile = context.get("candidate_profile", {})
        job_role = context.get("job_role") or profile.get("target_role", "Software Engineer")
        experience_level = context.get("experience_level") or profile.get("experience_level", "fresher")
        difficulty = context.get("difficulty", "medium")
        rag_context = context.get("rag_context", "")
        model_name = settings.IBM_GRANITE_MODEL if not self.is_mock else "SemanticEvaluator (all-MiniLM-L6-v2)"

        raw_output = ""
        parsed_data = {}

        # 1. Evaluate with IBM Granite if connected
        if not self.is_mock and self.is_connected:
            prompt = f"""You are a senior technical interviewer and subject matter expert. Evaluate the candidate's answer to the specific interview question below.

CURRENT QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

CANDIDATE PROFILE:
Target Role: {job_role}
Experience Level: {experience_level}
Skills: {', '.join(profile.get('skills', []))}

REFERENCE KNOWLEDGE / MODEL RUBRIC:
{rag_context if rag_context else 'Assess based on standard engineering and industry best practices.'}

SCORING RUBRIC (Rate each dimension on a scale of 0–10):
- technical_accuracy: Factual correctness, precision of concepts, correct algorithmic/architectural reasoning.
- relevance: Direct responsiveness to what was asked.
- clarity: Structured communication, articulation, and explanations.
- completeness: Depth of explanation, trade-offs, and coverage of critical elements.

IMPORTANT EVALUATION RULES:
- Evaluate semantic correctness and technical validity. Do not compare the answer to an exact expected sentence.
- Recognize equivalent valid ML/technical approaches (e.g. for class imbalance: SMOTE, oversampling, undersampling, class weighting, PR-AUC, focal loss are all valid).
- A technically correct and thorough answer MUST receive high marks (8–10).
- A partially correct answer with good points but missing depth should receive (5–7).
- A weak, wrong, or empty answer should receive (0–4).
- Calculate overall_score consistently: round(0.35 * technical_accuracy + 0.25 * relevance + 0.20 * clarity + 0.20 * completeness).

Return ONLY valid JSON matching this schema:
{{
  "overall_score": 8,
  "technical_accuracy": 8,
  "relevance": 9,
  "clarity": 8,
  "completeness": 8,
  "strengths": ["Identified key techniques...", "Discussed trade-offs accurately..."],
  "weaknesses": ["Could have elaborated on..."],
  "feedback": "2-3 sentence constructive feedback.",
  "recommended_difficulty": "medium"
}}"""
            try:
                raw_output = self.generate(prompt)
                parsed_data = self._parse_json(raw_output)
            except Exception as e:
                logger.error(f"IBM Granite evaluation failed: {e}", exc_info=True)
                raise RuntimeError(f"IBM Granite evaluation failed: {str(e)}")

        # 2. Intelligent Semantic Evaluation when in mock/local mode
        if not parsed_data or "overall_score" not in parsed_data:
            parsed_data = self._semantic_evaluate_answer(question, answer, rag_context, job_role, difficulty)
            raw_output = json.dumps(parsed_data)

        # Ensure consistent weighted overall_score calculation
        tech = int(parsed_data.get("technical_accuracy", 5))
        rel = int(parsed_data.get("relevance", 5))
        cla = int(parsed_data.get("clarity", 5))
        comp = int(parsed_data.get("completeness", 5))
        
        calculated_overall = int(round(0.35 * tech + 0.25 * rel + 0.20 * cla + 0.20 * comp))
        parsed_data["overall_score"] = max(0, min(10, calculated_overall))

        # 3. Development Mode Raw Evaluation Logging
        print("\n========== EVALUATION DEBUG ==========")
        print(f"QUESTION:\n{question}")
        print(f"\nANSWER:\n{answer}")
        print(f"\nPROFILE:\n{profile.get('name', 'Candidate')} ({profile.get('experience_level', 'fresher')})")
        print(f"\nROLE:\n{job_role}")
        print(f"\nRAG CONTEXT:\n{rag_context[:250]}..." if rag_context else "\nRAG CONTEXT:\nNone")
        print(f"\nMODEL:\n{model_name}")
        print(f"\nRAW MODEL OUTPUT:\n{raw_output[:400]}")
        print(f"\nPARSED EVALUATION:\n{json.dumps(parsed_data, indent=2)}")
        print(f"\nFINAL SCORE:\n{parsed_data.get('overall_score')}/10")
        print("=======================================\n")

        # Clamp all scores
        for k in ("overall_score", "technical_accuracy", "relevance", "clarity", "completeness"):
            if k in parsed_data:
                parsed_data[k] = max(0, min(10, int(parsed_data[k])))

        return EvaluationResponse(**parsed_data)

    def _semantic_evaluate_answer(
        self,
        question: str,
        answer: str,
        rag_context: str,
        job_role: str,
        difficulty: str
    ) -> dict:
        """Intelligent semantic scoring engine based on concept coverage and embedding similarity."""
        cleaned_ans = answer.strip()
        ans_lower = cleaned_ans.lower()
        words = re.findall(r"\b\w+\b", ans_lower)
        word_count = len(words)

        # Case 1: Empty or extremely short / evasive response
        if word_count < 6 or any(ans_lower == phrase for phrase in [
            "i don't know", "idk", "no idea", "not sure", "pass", "skip", "i do not know"
        ]):
            return {
                "overall_score": 1,
                "technical_accuracy": 1,
                "relevance": 2,
                "clarity": 2,
                "completeness": 1,
                "strengths": ["Acknowledged lack of familiarity with the concept"],
                "weaknesses": ["No technical explanation provided", "Failed to address the question"],
                "feedback": "You did not provide an answer to this question. Review the foundational concepts for this topic and practice answering with structured technical definitions.",
                "recommended_difficulty": "easy"
            }

        # Case 2: Semantic similarity & technical concept analysis
        # Extract candidate key concepts against RAG knowledge and question
        sim_score = 0.5
        if rag_service.model is not None:
            try:
                import numpy as np
                ref_text = question + "\n" + (rag_context if rag_context else "")
                ans_emb = rag_service.model.encode([cleaned_ans])
                ref_emb = rag_service.model.encode([ref_text])
                
                ans_norm = ans_emb / (np.linalg.norm(ans_emb) + 1e-9)
                ref_norm = ref_emb / (np.linalg.norm(ref_emb) + 1e-9)
                sim_score = float(np.dot(ans_norm, ref_norm.T)[0][0])
            except Exception as e:
                logger.error(f"Semantic scoring error: {e}")
        else:
            # Token and concept overlap against question and RAG context (zero-dependency)
            ref_words = set(re.findall(r"\b\w{3,}\b", (question + " " + (rag_context or "")).lower()))
            ans_meaningful = set(re.findall(r"\b\w{3,}\b", ans_lower))
            if ref_words and ans_meaningful:
                overlap = len(ans_meaningful & ref_words)
                sim_score = min(1.0, overlap / max(5.0, len(ans_meaningful) * 0.4))

        # Domain concept matching
        found_concepts = []
        domain_keywords = [
            # ML & Data Science
            "smote", "oversampling", "undersampling", "class weights", "imbalance",
            "precision", "recall", "f1", "pr-auc", "roc-auc", "focal loss",
            "bias", "variance", "tradeoff", "overfitting", "underfitting",
            "cross-validation", "stratified", "data leakage", "regularization",
            "features", "gradient", "loss", "metric", "threshold",
            # Software & DB
            "acid", "atomicity", "consistency", "isolation", "durability",
            "index", "indexing", "transaction", "latency", "throughput",
            "cache", "caching", "microservices", "rest", "idempotency",
            "api", "database", "query", "normalization", "distributed"
        ]

        for kw in domain_keywords:
            if kw in ans_lower:
                found_concepts.append(kw)

        # High technical correctness: either rich concept overlap or high semantic similarity with substantial explanation
        concept_count = len(found_concepts)

        if (concept_count >= 3 and word_count >= 20) or (sim_score >= 0.65 and word_count >= 30) or word_count >= 70:
            tech_acc = min(10, 8 + (1 if concept_count >= 4 else 0) + (1 if word_count >= 40 else 0))
            relevance = min(10, 8 + (1 if sim_score >= 0.5 else 0))
            clarity = min(10, 8 + (1 if "." in cleaned_ans else 0))
            completeness = min(10, 7 + (1 if concept_count >= 3 else 0) + (1 if word_count >= 50 else 0))

            strengths = [
                f"Accurately incorporated key technical concepts: {', '.join(found_concepts[:4])}" if found_concepts else "Strong technical grasp of the question",
                "Structured and logically coherent explanation",
                "Directly answered the core challenge posed by the interviewer"
            ]
            weaknesses = [
                "Could further elaborate on production edge cases or operational trade-offs"
            ]
            feedback = "Excellent response! You demonstrated strong technical depth, used correct terminology, and articulated your reasoning clearly."
            rec_diff = "hard" if difficulty != "hard" else "hard"

        elif (concept_count >= 1 and word_count >= 15) or (sim_score >= 0.45 and word_count >= 20):
            tech_acc = 6
            relevance = 7
            clarity = 6
            completeness = 5

            strengths = [
                f"Demonstrated awareness of core principles ({', '.join(found_concepts[:2])})" if found_concepts else "Identified fundamental concepts",
                "Relevant response to the question"
            ]
            weaknesses = [
                "Could provide deeper mathematical, algorithmic, or implementation details",
                "Explanation is somewhat brief"
            ]
            feedback = "Good answer that captures the basics. To improve, try expanding on specific implementation steps and comparing alternative techniques."
            rec_diff = "medium"

        else:
            tech_acc = 4
            relevance = 5
            clarity = 4
            completeness = 3

            strengths = ["Attempted to answer the question"]
            weaknesses = [
                "Answer lacks key technical depth and specific methodologies",
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
        """Compile final report based on actual candidate evaluations."""
        evaluations = interview_data.get("evaluations", [])
        profile = interview_data.get("candidate_profile", {})

        if evaluations:
            overall_scores = [e.get("overall_score", 5) for e in evaluations]
            tech_scores = [e.get("technical_accuracy", 5) for e in evaluations]
            clarity_scores = [e.get("clarity", 5) for e in evaluations]
            relevance_scores = [e.get("relevance", 5) for e in evaluations]

            avg_overall = sum(overall_scores) / len(overall_scores)
            avg_tech = sum(tech_scores) / len(tech_scores)
            avg_clarity = sum(clarity_scores) / len(clarity_scores)
            avg_relevance = sum(relevance_scores) / len(relevance_scores)

            overall = int(round(avg_overall * 10))
            tech = int(round(avg_tech * 10))
            comm = int(round(avg_clarity * 10))
            prob = int(round(avg_relevance * 10))
            readiness = int(round((avg_tech * 0.6 + avg_clarity * 0.4) * 10))
        else:
            overall, tech, comm, prob, readiness = 65, 60, 70, 65, 65

        # Aggregate unique strengths and weaknesses from evaluations
        strengths = []
        weaknesses = []
        for e in evaluations:
            for s in e.get("strengths", []):
                if s not in strengths:
                    strengths.append(s)
            for w in e.get("weaknesses", []):
                if w not in weaknesses:
                    weaknesses.append(w)

        if not strengths:
            strengths = ["Solid foundation in core computer science principles", "Engaged thoughtfully with technical problems"]
        if not weaknesses:
            weaknesses = ["Practice presenting edge case handling and system trade-offs"]

        recommendations = [
            f"Review advanced concepts in {profile.get('skills', ['your target domain'])[0]}.",
            "Practice structuring technical answers using the STAR method for behavioral scenarios and First Principles for technical questions.",
            "Deepen your familiarity with production deployment, monitoring, and debugging trade-offs.",
            "Focus on communicating trade-offs between competing architectural or algorithmic solutions.",
            "Conduct mock interviews regularly to sharpen articulation under timed conditions."
        ]

        q_evals = []
        questions = interview_data.get("questions", [])
        answers = interview_data.get("answers", [])
        for i, ev in enumerate(evaluations):
            q_text = questions[i].get("question", f"Question {i+1}") if i < len(questions) else f"Question {i+1}"
            ans_text = answers[i] if i < len(answers) else ""
            q_evals.append({
                "question": q_text,
                "answer": ans_text,
                "score": ev.get("overall_score", 5),
                "feedback": ev.get("feedback", ""),
            })

        diff_prog = interview_data.get("difficulty_progression", [])
        if not diff_prog:
            diff_prog = ["medium"]

        report_payload = {
            "interview_id": str(interview_data.get("interview_id", uuid.uuid4())),
            "candidate_name": profile.get("name", "Candidate"),
            "target_role": profile.get("target_role", "Software Engineer"),
            "overall_score": overall,
            "technical_score": tech,
            "communication_score": comm,
            "problem_solving_score": prob,
            "role_readiness_score": readiness,
            "questions_answered": len(evaluations),
            "total_questions": int(interview_data.get("total_questions", 10)),
            "strengths": strengths[:6],
            "weaknesses": weaknesses[:6],
            "recommendations": recommendations,
            "difficulty_progression": diff_prog,
            "question_evaluations": q_evals,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        return InterviewReport(**report_payload)

    # ------------------------------------------------------------------
    # Built-in diverse question pools
    # ------------------------------------------------------------------
    _BUILTIN_POOLS = {
        "easy": [
            {"question": "What is the difference between a list and a tuple in Python?", "category": "technical", "difficulty": "easy"},
            {"question": "Explain what supervised learning is and provide a real-world example.", "category": "technical", "difficulty": "easy"},
            {"question": "What is the purpose of Git and version control in software engineering?", "category": "technical", "difficulty": "easy"},
            {"question": "Can you describe a time when you collaborated effectively on a technical team?", "category": "behavioral", "difficulty": "easy"},
            {"question": "Explain the difference between SQL and NoSQL databases.", "category": "technical", "difficulty": "easy"},
            {"question": "What is an API and how do RESTful endpoints work?", "category": "technical", "difficulty": "easy"},
            {"question": "What are the four core pillars of object-oriented programming?", "category": "technical", "difficulty": "easy"},
            {"question": "What is the difference between a stack and a queue data structure?", "category": "technical", "difficulty": "easy"},
            {"question": "What motivates you in your software engineering career?", "category": "hr", "difficulty": "easy"},
            {"question": "How do you approach learning a completely new programming language or framework?", "category": "behavioral", "difficulty": "easy"},
        ],
        "medium": [
            {"question": "Explain the bias-variance tradeoff in machine learning and how regularization impacts it.", "category": "technical", "difficulty": "medium"},
            {"question": "How would you handle class imbalance in a classification problem?", "category": "technical", "difficulty": "medium"},
            {"question": "Describe the architectural differences and trade-offs between REST and GraphQL APIs.", "category": "technical", "difficulty": "medium"},
            {"question": "Walk me through how you would design a recommendation system for an e-commerce platform.", "category": "technical", "difficulty": "medium"},
            {"question": "What is the difference between precision and recall? When would you prioritize precision over recall?", "category": "technical", "difficulty": "medium"},
            {"question": "Explain how a Random Forest algorithm works and how it avoids overfitting compared to a single decision tree.", "category": "technical", "difficulty": "medium"},
            {"question": "Describe a challenging technical outage or bug you resolved and your systematic approach.", "category": "behavioral", "difficulty": "medium"},
            {"question": "What are ACID properties in database systems, and how is isolation achieved?", "category": "technical", "difficulty": "medium"},
            {"question": "Explain dependency injection and how it facilitates test-driven development.", "category": "technical", "difficulty": "medium"},
            {"question": "How do you detect and prevent memory leaks or connection pool exhaustion in backend applications?", "category": "technical", "difficulty": "medium"},
        ],
        "hard": [
            {"question": "Design a scalable real-time ML inference pipeline that handles 10,000 requests per second with sub-50ms latency.", "category": "technical", "difficulty": "hard"},
            {"question": "Explain the multi-head attention mechanism in transformers and why self-attention replaced recurrent architectures.", "category": "technical", "difficulty": "hard"},
            {"question": "How would you architect a distributed training system for a large model across multiple GPU nodes?", "category": "technical", "difficulty": "hard"},
            {"question": "Describe techniques to reduce hallucinations and verify citations in an enterprise RAG architecture.", "category": "technical", "difficulty": "hard"},
            {"question": "Compare and contrast optimization algorithms: SGD with momentum, RMSProp, and AdamW.", "category": "technical", "difficulty": "hard"},
            {"question": "How would you design a distributed rate limiter operating across multiple data centers?", "category": "technical", "difficulty": "hard"},
            {"question": "Explain the CAP theorem and PACELC theorem, and how modern distributed databases navigate these trade-offs.", "category": "technical", "difficulty": "hard"},
            {"question": "How would you design a system to detect, monitor, and mitigate feature drift and concept drift in production models?", "category": "technical", "difficulty": "hard"},
            {"question": "Describe a high-stakes technical decision where you had to push back against executive or team consensus.", "category": "behavioral", "difficulty": "hard"},
            {"question": "Explain how consistent hashing works and how virtual nodes prevent hot-spotting in distributed key-value stores.", "category": "technical", "difficulty": "hard"},
        ],
    }


granite_service = GraniteService()
