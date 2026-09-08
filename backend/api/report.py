from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import Interview
from schemas.schemas import InterviewReport
from agents.interview_agent import state_from_interview, generate_report_node

router = APIRouter(prefix="/api", tags=["Report"])


@router.get("/report/{interview_id}", response_model=InterviewReport)
async def get_report(interview_id: str, db: Session = Depends(get_db)):
    clean_id = str(interview_id).strip()
    db_interview = db.query(Interview).filter(Interview.id == clean_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail=f"Interview {clean_id} not found")

    # If report already generated, return it
    if db_interview.report and isinstance(db_interview.report, dict):
        return db_interview.report

    # If interview has been answered or finished, dynamically generate report
    try:
        state = state_from_interview(db_interview)
        state = generate_report_node(state)
        report_data = state["report"]

        db_interview.status = "completed"
        db_interview.report = report_data
        db.commit()
        db.refresh(db_interview)

        return report_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")
