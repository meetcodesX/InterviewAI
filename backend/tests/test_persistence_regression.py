"""Regression test for interview persistence and state management.

Verifies:
1. create interview -> get returned interview_id
2. retrieve same interview directly from database using SQLAlchemy session
3. submit answer using that ID -> assert HTTP 200 & evaluation returned
4. verify answer and evaluation persisted to database
5. call next question using same ID -> assert HTTP 200 & Q2 returned
6. submit answer to Q2
7. call finish using same ID -> assert HTTP 200 & report returned
8. verify report and status="completed" in database
9. retrieve report via GET /api/report/{id}
10. Runs multiple times with a fresh SQLite database to guarantee determinism.
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

# Configure an explicit test SQLite database
test_db_path = backend_dir / "regression_test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{test_db_path.as_posix()}"

from config import settings
# Force settings.DATABASE_URL to our test database
settings.DATABASE_URL = f"sqlite:///{test_db_path.as_posix()}"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database.db import Base
from models.models import Interview, InterviewQuestion
from main import app


def run_single_regression_cycle(cycle_num: int):
    print(f"\n=======================================================")
    print(f"  RUNNING REGRESSION CYCLE #{cycle_num} (Fresh SQLite DB)")
    print(f"=======================================================")

    # 1. Clean up any existing test DB file
    if test_db_path.exists():
        try:
            test_db_path.unlink()
            print(f"Removed previous test database: {test_db_path.name}")
        except Exception as e:
            print(f"Could not remove db: {e}")

    # 2. Re-create engine and tables
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    client = TestClient(app)

    # 3. Create interview
    create_payload = {
        "profile": {
            "name": f"Candidate Cycle {cycle_num}",
            "target_role": "ML Engineer",
            "experience_level": "Fresher",
            "skills": ["Python", "Machine Learning", "Deep Learning", "RAG"],
            "years_of_experience": 0,
            "education": ["B.Tech"],
            "projects": ["RAG Project"],
            "experience": [],
            "certifications": []
        },
        "config": {
            "job_role": "ML Engineer",
            "experience_level": "Fresher",
            "interview_type": "technical",
            "difficulty": "adaptive",
            "num_questions": 3
        }
    }

    res_create = client.post("/api/interview/create", json=create_payload)
    assert res_create.status_code == 200, f"Cycle {cycle_num}: /create failed: {res_create.text}"
    q1 = res_create.json()
    interview_id = q1["interview_id"]
    q1_id = q1["question_id"]
    print(f"[{cycle_num}] 1. /create -> HTTP 200 | Returned interview_id: {interview_id}")
    print(f"[{cycle_num}]    Initial question: {q1['question']}")

    # 4. Directly verify record in SQLite database via SQLAlchemy
    with TestingSessionLocal() as db:
        db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
        assert db_interview is not None, f"Cycle {cycle_num}: Interview {interview_id} NOT found in DB!"
        assert db_interview.id == interview_id
        assert db_interview.status == "in_progress"
        assert len(db_interview.questions) >= 1
        print(f"[{cycle_num}] 2. Verified record in SQLite database: candidate='{db_interview.candidate_name}', status='{db_interview.status}'")

        q1_record = db.query(InterviewQuestion).filter(
            InterviewQuestion.interview_id == interview_id,
            InterviewQuestion.id == q1_id
        ).first()
        assert q1_record is not None, f"Cycle {cycle_num}: InterviewQuestion {q1_id} not found in DB!"
        print(f"[{cycle_num}]    Verified initial InterviewQuestion in DB.")

    # 5. Submit answer for Question 1
    answer_payload = {
        "interview_id": interview_id,
        "question_id": q1_id,
        "answer": "Supervised learning uses labeled ground truth data for training, while unsupervised learning discovers intrinsic patterns without labels."
    }
    res_ans = client.post("/api/interview/answer", json=answer_payload)
    assert res_ans.status_code == 200, f"Cycle {cycle_num}: /answer failed: {res_ans.text}"
    eval_resp = res_ans.json()
    print(f"[{cycle_num}] 3. /answer -> HTTP 200 | Evaluation score: {eval_resp['evaluation']['overall_score']}/10")

    # 6. Verify answer and evaluation were persisted in DB
    with TestingSessionLocal() as db:
        db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
        assert len(db_interview.answers) == 1, f"Expected 1 answer in DB, found {len(db_interview.answers)}"
        assert len(db_interview.evaluations) == 1, f"Expected 1 evaluation in DB, found {len(db_interview.evaluations)}"
        print(f"[{cycle_num}] 4. Verified answer and evaluation persisted to DB.")

    # 7. Call /next
    res_next = client.post("/api/interview/next", json={"interview_id": interview_id})
    assert res_next.status_code == 200, f"Cycle {cycle_num}: /next failed: {res_next.text}"
    q2 = res_next.json()
    q2_id = q2["question_id"]
    print(f"[{cycle_num}] 5. /next -> HTTP 200 | Q2: {q2['question']} (difficulty: {q2['difficulty']})")
    assert q2_id != q1_id, "Q2 should have a distinct ID from Q1"

    # 8. Submit answer for Question 2
    res_ans2 = client.post("/api/interview/answer", json={
        "interview_id": interview_id,
        "question_id": q2_id,
        "answer": "We can address class imbalance using SMOTE oversampling, undersampling the majority class, focal loss, or adjusting classification thresholds."
    })
    assert res_ans2.status_code == 200, f"Cycle {cycle_num}: /answer 2 failed: {res_ans2.text}"
    print(f"[{cycle_num}] 6. /answer for Q2 -> HTTP 200 | Score: {res_ans2.json()['evaluation']['overall_score']}/10")

    # 9. Call /finish
    res_finish = client.post("/api/interview/finish", json={"interview_id": interview_id})
    assert res_finish.status_code == 200, f"Cycle {cycle_num}: /finish failed: {res_finish.text}"
    report = res_finish.json()
    print(f"[{cycle_num}] 7. /finish -> HTTP 200 | Overall Score: {report['overall_score']}/100")
    assert "overall_score" in report

    # 10. Verify DB status is now completed with report
    with TestingSessionLocal() as db:
        db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
        assert db_interview.status == "completed"
        assert db_interview.report is not None
        print(f"[{cycle_num}] 8. Verified status='completed' and report stored in DB.")

    # 11. Fetch report via GET /api/report/{id}
    res_get_report = client.get(f"/api/report/{interview_id}")
    assert res_get_report.status_code == 200, f"Cycle {cycle_num}: /report/{interview_id} failed: {res_get_report.text}"
    assert res_get_report.json()["overall_score"] == report["overall_score"]
    print(f"[{cycle_num}] 9. GET /api/report/{interview_id} -> HTTP 200 | Report retrieved successfully.")

    print(f"[{cycle_num}] ALL STEPS IN CYCLE #{cycle_num} COMPLETED WITH 100% SUCCESS!")


def main():
    # Run 3 consecutive cycles with a completely fresh database each time
    for i in range(1, 4):
        run_single_regression_cycle(i)

    print("\n=======================================================")
    print("  ALL 3 REGRESSION CYCLES PASSED WITH ZERO ERRORS!")
    print("=======================================================")

    # Clean up test DB at the end
    if test_db_path.exists():
        try:
            test_db_path.unlink()
        except:
            pass


if __name__ == "__main__":
    main()
