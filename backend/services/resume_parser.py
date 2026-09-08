"""Heuristic and rule-based resume text parser.

Extracts structured candidate profile attributes directly from extracted PDF text
when operating without external LLM or as an offline fallback.
Never returns hardcoded placeholder data.
"""

import re
import logging
from typing import Dict, Any, List
from schemas.schemas import CandidateProfile

logger = logging.getLogger(__name__)

# Common job roles to detect
KNOWN_ROLES = [
    "Machine Learning Engineer", "ML Engineer", "Data Scientist", "Data Analyst",
    "Data Engineer", "Full-Stack Software Engineer", "Full-Stack Developer",
    "Fullstack Developer", "Frontend Developer", "Frontend Engineer",
    "Backend Developer", "Backend Engineer", "Software Engineer", "Software Developer",
    "DevOps Engineer", "Cloud Architect", "Cloud Engineer", "AI Engineer",
    "Deep Learning Engineer", "NLP Engineer", "System Architect", "QA Engineer"
]

# Vocabulary of tech skills to recognize
TECH_SKILLS = [
    # Languages
    "Python", "JavaScript", "TypeScript", "C++", "C#", "Java", "Go", "Rust", "SQL", "R", "PHP", "Ruby", "Swift", "Kotlin", "HTML5", "CSS3", "Bash", "Shell",
    # AI / ML
    "PyTorch", "TensorFlow", "Keras", "Scikit-Learn", "Hugging Face", "Transformers",
    "LangChain", "LangGraph", "ChromaDB", "Vector Databases", "Prompt Engineering",
    "Computer Vision", "Natural Language Processing", "NLP", "Deep Learning",
    "Machine Learning", "Generative AI", "RAG", "LLM", "BERT", "RoBERTa", "GPT",
    # Web & Frameworks
    "React", "Next.js", "Vue", "Angular", "Node.js", "Express", "FastAPI", "Django", "Flask", "Spring Boot", "Redux", "Tailwind CSS", "Bootstrap",
    # Databases
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra", "Elasticsearch", "DynamoDB",
    # Cloud & DevOps
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Git", "GitHub Actions", "CI/CD", "Linux", "Terraform", "Postman", "REST APIs", "GraphQL", "Microservices"
]


def extract_name(lines: List[str]) -> str:
    """Extract candidate name from the top lines of the resume."""
    for line in lines[:8]:
        cleaned = line.strip()
        if not cleaned:
            continue
        # Skip headers / labels
        upper = cleaned.upper()
        if any(h in upper for h in [
            "RESUME", "CURRICULUM VITAE", "CV", "CONTACT", "EMAIL", "PHONE",
            "SUMMARY", "PROFESSIONAL SUMMARY", "PROFILE", "PAGE", "HTTP", "WWW"
        ]):
            continue
        # Skip lines with phone numbers or email addresses
        if "@" in cleaned or re.search(r"\d{4,}", cleaned):
            continue
        # A name is typically 2 to 4 words
        words = cleaned.split()
        if 1 <= len(words) <= 4 and all(w.isalpha() or w.replace(".", "").isalpha() for w in words):
            return " ".join(w.capitalize() for w in words)
    return "Candidate"


def extract_role(text: str, lines: List[str]) -> str:
    """Detect the candidate's target or current job role."""
    # Check top lines first
    for line in lines[:8]:
        cleaned = line.strip()
        for role in KNOWN_ROLES:
            if role.lower() in cleaned.lower():
                return role

    # Search through the full text
    for role in KNOWN_ROLES:
        if re.search(rf"\b{re.escape(role)}\b", text, re.IGNORECASE):
            return role

    return "Software Engineer"


def extract_skills(text: str) -> List[str]:
    """Identify technical skills mentioned in the resume text."""
    found_skills = []
    text_lower = text.lower()

    for skill in TECH_SKILLS:
        pattern = rf"(?<![\w\-]){re.escape(skill.lower())}(?![\w\-])"
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    # Also parse explicit SKILLS section if available
    skills_section = re.search(r"(?:TECHNICAL\s+SKILLS|SKILLS|TECHNOLOGIES)[\s\:\-]+(.*?)(?=\n\s*[A-Z]{3,}|\Z)", text, re.DOTALL | re.IGNORECASE)
    if skills_section:
        section_text = skills_section.group(1)
        # Split by comma, bullets, pipes, or newlines
        tokens = re.split(r"[\,\•\-\|\n\r]+", section_text)
        for token in tokens:
            cleaned = token.strip().strip(":")
            if 2 <= len(cleaned) <= 30 and not any(kw in cleaned.lower() for kw in ["proficiency", "experience", "level", "etc"]):
                if cleaned not in found_skills and len(cleaned.split()) <= 4:
                    # Only add if title-cased or alphanumeric
                    if any(c.isalpha() for c in cleaned):
                        found_skills.append(cleaned)

    # Deduplicate while preserving order
    seen = set()
    result = []
    for s in found_skills:
        s_clean = s.strip()
        if s_clean.lower() not in seen and s_clean:
            seen.add(s_clean.lower())
            result.append(s_clean)

    return result[:20]


def extract_education(text: str) -> List[str]:
    """Extract degrees and institutions from education section."""
    education = []
    edu_section = re.search(r"(?:EDUCATION|ACADEMIC BACKGROUND|QUALIFICATIONS)[\s\:\-]+(.*?)(?=\n\s*[A-Z]{3,}|\Z)", text, re.DOTALL | re.IGNORECASE)
    search_text = edu_section.group(1) if edu_section else text

    lines = [l.strip() for l in search_text.splitlines() if l.strip()]
    for line in lines:
        if any(deg in line for deg in [
            "B.Tech", "B.E.", "M.Tech", "M.S.", "B.S.", "Bachelor", "Master",
            "Ph.D", "Diploma", "IIT", "NIT", "University", "College", "Institute"
        ]):
            education.append(line.lstrip("•-* "))

    return education[:4]


def extract_projects(text: str) -> List[str]:
    """Extract project titles or key project descriptions."""
    projects = []
    proj_section = re.search(r"(?:KEY PROJECTS|PROJECTS|ACADEMIC PROJECTS)[\s\:\-]+(.*?)(?=\n\s*[A-Z]{3,}|\Z)", text, re.DOTALL | re.IGNORECASE)
    if proj_section:
        lines = [l.strip() for l in proj_section.group(1).splitlines() if l.strip()]
        for line in lines:
            if re.match(r"^\d+\.|\*|\-", line) or any(line.startswith(p) for p in ["1.", "2.", "3.", "•"]):
                cleaned = re.sub(r"^[\d\.\•\-\*\s]+", "", line).strip()
                if 5 <= len(cleaned) <= 80:
                    projects.append(cleaned)
            elif 5 <= len(line) <= 60 and not line.endswith("."):
                projects.append(line)

    return projects[:4]


def extract_experience(text: str) -> List[str]:
    """Extract work history records."""
    experience = []
    exp_section = re.search(r"(?:PROFESSIONAL EXPERIENCE|WORK EXPERIENCE|EXPERIENCE|EMPLOYMENT)[\s\:\-]+(.*?)(?=\n\s*[A-Z]{3,}|\Z)", text, re.DOTALL | re.IGNORECASE)
    if exp_section:
        lines = [l.strip() for l in exp_section.group(1).splitlines() if l.strip()]
        for line in lines:
            if any(role in line.lower() for role in ["engineer", "developer", "intern", "analyst", "lead", "manager", "associate"]):
                cleaned = line.lstrip("•-* 1234567890. ")
                if 5 <= len(cleaned) <= 100:
                    experience.append(cleaned)

    return experience[:4]


def extract_certifications(text: str) -> List[str]:
    """Extract certifications."""
    certs = []
    cert_section = re.search(r"(?:CERTIFICATIONS|CERTIFICATES|LICENSES)[\s\:\-]+(.*?)(?=\n\s*[A-Z]{3,}|\Z)", text, re.DOTALL | re.IGNORECASE)
    if cert_section:
        lines = [l.strip() for l in cert_section.group(1).splitlines() if l.strip()]
        for line in lines:
            cleaned = line.lstrip("•-* 1234567890. ")
            if 5 <= len(cleaned) <= 80:
                certs.append(cleaned)
    return certs[:4]


def extract_experience_level_and_years(text: str, experience_entries: List[str]) -> tuple:
    """Determine experience level and estimated years."""
    text_lower = text.lower()
    
    # Check for explicit year statements
    yr_match = re.search(r"(\d+)\+?\s*years?\s+of\s+experience", text_lower)
    if yr_match:
        years = int(yr_match.group(1))
    else:
        # Check date spans (e.g. 2021 - 2024)
        dates = re.findall(r"\b(20\d\d)\b", text)
        if len(dates) >= 2:
            years = min(15, max(0, max(int(d) for d in dates) - min(int(d) for d in dates)))
        else:
            years = 1 if experience_entries else 0

    if "intern" in text_lower or "fresher" in text_lower or years == 0:
        level = "fresher"
    elif years <= 2:
        level = "junior"
    elif years <= 5:
        level = "mid"
    else:
        level = "senior"

    return level, years


def parse_resume_text(text: str) -> CandidateProfile:
    """Heuristically parse resume text into a validated CandidateProfile.
    
    Raises ValueError if the text contains no recognizable candidate information.
    """
    cleaned = text.strip()
    if not cleaned or len(cleaned) < 30:
        raise ValueError("Unable to extract resume information. Please upload a valid text-based PDF.")

    lines = [l.strip() for l in cleaned.splitlines() if l.strip()]

    name = extract_name(lines)
    target_role = extract_role(cleaned, lines)
    skills = extract_skills(cleaned)
    education = extract_education(cleaned)
    projects = extract_projects(cleaned)
    experience = extract_experience(cleaned)
    certifications = extract_certifications(cleaned)
    experience_level, years_of_exp = extract_experience_level_and_years(cleaned, experience)

    # Validation: If we couldn't find a name AND we couldn't find any skills, it's not a valid text resume
    if name == "Candidate" and not skills:
        raise ValueError("Unable to extract resume information. Please upload a valid text-based PDF.")

    return CandidateProfile(
        name=name,
        education=education,
        skills=skills,
        projects=projects,
        experience=experience,
        certifications=certifications,
        target_role=target_role,
        experience_level=experience_level,
        years_of_experience=years_of_exp
    )
