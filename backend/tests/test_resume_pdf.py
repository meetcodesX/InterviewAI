"""Test PDF creation and PyMuPDF text extraction with resume_service."""
import sys
import io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pymupdf as fitz
    from services.resume_service import resume_service

    # Create a real PDF document in-memory using pymupdf
    doc = fitz.open()
    page = doc.new_page()
    text = """Alex Sharma
Machine Learning Engineer
Email: alex.sharma@example.com | Phone: +1-555-0199 | Location: San Francisco, CA

SUMMARY
Passionate Machine Learning Engineer specializing in Python, RAG pipelines, and LLM fine-tuning.

EDUCATION
B.Tech in Computer Science - IIT Delhi (2020 - 2024)

SKILLS
- Programming: Python, SQL, C++
- AI/ML: PyTorch, Transformers, LangChain, LangGraph, ChromaDB
- Domains: Generative AI, Natural Language Processing, Retrieval-Augmented Generation

PROJECTS
- Autonomous RAG Interview Assistant: Built end-to-end agentic workflow with ChromaDB and Granite.
- Sentiment Classifier: Fine-tuned BERT model achieving 94% F1-score on imbalanced datasets.
"""
    rect = fitz.Rect(50, 50, 550, 750)
    page.insert_textbox(rect, text, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()

    print(f"Generated test PDF: {len(pdf_bytes)} bytes")

    # Extract text using resume_service
    extracted_text = resume_service.extract_text_from_pdf(pdf_bytes)
    print(f"Extracted {len(extracted_text)} characters.")
    assert "Alex Sharma" in extracted_text, "Alex Sharma not found in extracted text!"
    assert "Machine Learning" in extracted_text, "Machine Learning not found!"
    print("PDF Text Extraction: SUCCESS")

    # Extract candidate profile
    profile = resume_service.parse_resume(extracted_text)
    print("Parsed Candidate Profile:")
    print(f"  Name: {profile.name}")
    print(f"  Role: {profile.target_role}")
    print(f"  Skills: {profile.skills}")
    assert profile.name != "", "Profile name should not be empty!"
    print("Resume Parsing: SUCCESS")
    print("ALL RESUME TESTS PASSED!")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"FAILED: {e}")
