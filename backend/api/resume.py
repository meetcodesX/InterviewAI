import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas.schemas import CandidateProfile, ProfileExtractRequest, ManualProfileRequest, ResumeUploadResponse
from services.resume_service import resume_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Resume"])


@router.post("/resume/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_resume.pdf"
    content_type = file.content_type or "unknown"
    logger.info(f"Resume upload initiated: filename='{filename}', content_type='{content_type}'")

    if not filename.lower().endswith(".pdf"):
        logger.warning(f"Upload rejected: '{filename}' does not end with .pdf")
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        content = await file.read()
    except Exception as read_err:
        logger.error(f"Failed to read file stream for '{filename}': {read_err}")
        raise HTTPException(status_code=400, detail=f"Failed to read upload stream: {str(read_err)}")

    file_size = len(content)
    logger.info(f"Received {file_size} bytes for '{filename}'. Extracting text...")

    try:
        text = resume_service.extract_text_from_pdf(content, filename=filename)
        logger.info(f"Successfully extracted {len(text)} characters from '{filename}'.")
    except HTTPException:
        raise
    except Exception as extract_err:
        logger.error(f"Text extraction failed for '{filename}': {extract_err}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Unable to extract text from PDF: {str(extract_err)}"
        )

    try:
        profile = resume_service.parse_resume(text, filename=filename)
    except HTTPException:
        raise
    except Exception as parse_err:
        logger.error(f"Profile parsing failed for '{filename}': {parse_err}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Unable to parse candidate profile: {str(parse_err)}"
        )

    return ResumeUploadResponse(resume_text=text, profile=profile)


@router.post("/profile/extract", response_model=CandidateProfile)
async def extract_profile(req: ProfileExtractRequest):
    profile = resume_service.parse_resume(req.resume_text)
    return profile


@router.post("/profile/manual", response_model=CandidateProfile)
async def manual_profile(req: ManualProfileRequest):
    return CandidateProfile(
        name=req.name,
        target_role=req.target_role,
        experience_level=req.experience_level,
        skills=[s.strip() for s in req.skills.split(",") if s.strip()],
        years_of_experience=req.years_of_experience
    )
