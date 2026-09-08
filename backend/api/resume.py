from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas.schemas import CandidateProfile, ProfileExtractRequest, ManualProfileRequest, ResumeUploadResponse
from services.resume_service import resume_service

router = APIRouter(prefix="/api", tags=["Resume"])

@router.post("/resume/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_resume.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    content = await file.read()
    text = resume_service.extract_text_from_pdf(content, filename=filename)
    profile = resume_service.parse_resume(text, filename=filename)
    
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
