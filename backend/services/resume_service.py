"""Resume processing service: text extraction via PyMuPDF and profile parsing."""

import io
import json
import logging
from fastapi import HTTPException

from config import settings
from schemas.schemas import CandidateProfile
from services.granite_service import granite_service
from services.resume_parser import parse_resume_text

logger = logging.getLogger(__name__)


class ResumeService:
    def __init__(self):
        self.pdf_engine = None
        try:
            import pymupdf
            self.pdf_engine = "pymupdf"
        except ImportError:
            try:
                import fitz
                self.pdf_engine = "fitz"
            except ImportError:
                try:
                    import pypdf
                    self.pdf_engine = "pypdf"
                except ImportError:
                    self.pdf_engine = None

    def extract_text_from_pdf(self, file_bytes: bytes, filename: str = "uploaded_file.pdf") -> str:
        """Extracts plain text from PDF bytes using PyMuPDF (with fallback to pypdf)."""
        if len(file_bytes) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds limit (10MB)")

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Unable to extract resume information. Please upload a valid text-based PDF."
            )

        text = ""

        # Primary: PyMuPDF
        try:
            import pymupdf as fitz
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as fitz_err:
            logger.warning(f"PyMuPDF extraction failed ({fitz_err}), trying pypdf fallback...")
            try:
                from pypdf import PdfReader
                reader = PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            except Exception as pypdf_err:
                logger.error(f"Both PDF extractors failed for {filename}: {pypdf_err}")
                raise HTTPException(
                    status_code=400,
                    detail="Unable to extract resume information. Please upload a valid text-based PDF."
                )

        cleaned_text = text.strip()
        if not cleaned_text or len(cleaned_text) < 20:
            logger.warning(f"Extracted text too short ({len(cleaned_text)} chars) for {filename}")
            raise HTTPException(
                status_code=400,
                detail="Unable to extract resume information. Please upload a valid text-based PDF."
            )

        return cleaned_text

    def parse_resume(self, text: str, filename: str = "uploaded_file.pdf") -> CandidateProfile:
        """Extracts a structured CandidateProfile from resume text.
        
        Attempts LLM extraction if Granite is connected, otherwise uses intelligent
        heuristic parsing. Never falls back to hardcoded demo data.
        """
        profile: CandidateProfile = None

        # 1. Try IBM Granite if connected
        if settings.is_ibm and granite_service.is_connected:
            try:
                profile = granite_service.extract_profile(text)
            except Exception as e:
                logger.warning(f"Granite profile extraction failed ({e}), using heuristic parser.")

        # 2. Heuristic parsing directly from the resume text
        if profile is None or not profile.name or profile.name == "Candidate":
            try:
                profile = parse_resume_text(text)
            except ValueError as ve:
                logger.error(f"Resume text parsing error: {ve}")
                raise HTTPException(
                    status_code=400,
                    detail="Unable to extract resume information. Please upload a valid text-based PDF."
                )
            except Exception as e:
                logger.error(f"Unexpected error in resume parser: {e}")
                raise HTTPException(
                    status_code=400,
                    detail="Unable to extract resume information. Please upload a valid text-based PDF."
                )

        # 3. Development logging as required by specification
        profile_json = json.dumps(profile.model_dump(), indent=2)
        print(f"\n================ RESUME UPLOAD DEBUG ================")
        print(f"RESUME FILE:\n{filename}")
        print(f"\nEXTRACTED TEXT LENGTH:\n{len(text)}")
        print(f"\nEXTRACTED PROFILE:\n{profile_json}")
        print(f"=====================================================\n")

        logger.info(
            f"\nRESUME FILE: {filename}\n"
            f"EXTRACTED TEXT LENGTH: {len(text)}\n"
            f"EXTRACTED PROFILE: {profile_json}"
        )

        return profile


resume_service = ResumeService()
