"""Test specifically reproducing and verifying the fix for the user-reported bug:
POST /api/interview/create -> HTTP 200 (returns interview_id)
POST /api/interview/answer with that ID -> HTTP 200 (NOT 500)
POST /api/interview/next with that ID -> HTTP 200 (NOT 500)
POST /api/interview/finish with that ID -> HTTP 200 (NOT 500)
"""
import httpx
import uuid
import sys

BASE_URL = "http://127.0.0.1:8000"

print("--- Testing Reported Bug Reproduction & Fix on Live Backend ---")

with httpx.Client(base_url=BASE_URL, timeout=15.0) as client:
    # 1. POST /api/interview/create
    create_payload = {
        "profile": {
            "name": "Alex Sharma",
            "target_role": "ML Engineer",
            "experience_level": "Fresher",
            "skills": ["Python", "Machine Learning", "RAG"],
            "years_of_experience": 0,
            "education": [],
            "projects": [],
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
    assert res_create.status_code == 200, f"Expected 200, got {res_create.status_code}: {res_create.text}"
    q1_data = res_create.json()
    interview_id = q1_data["interview_id"]
    q1_id = q1_data["question_id"]
    print(f"STEP 1: POST /api/interview/create -> HTTP 200 (interview_id: {interview_id})")

    # 2. POST /api/interview/answer
    answer_payload = {
        "interview_id": interview_id,
        "question_id": q1_id,
        "answer": "Supervised learning algorithms are trained using labeled datasets where inputs map to known outputs, whereas unsupervised learning analyzes patterns in unlabeled data."
    }
    res_answer = client.post("/api/interview/answer", json=answer_payload)
    print(f"STEP 2: POST /api/interview/answer -> HTTP {res_answer.status_code}")
    assert res_answer.status_code == 200, f"Expected 200, got {res_answer.status_code}: {res_answer.text}"
    ans_data = res_answer.json()
    assert "evaluation" in ans_data
    print(f"        Score: {ans_data['evaluation']['overall_score']}/10")

    # 3. POST /api/interview/next
    next_payload = {"interview_id": interview_id}
    res_next = client.post("/api/interview/next", json=next_payload)
    print(f"STEP 3: POST /api/interview/next -> HTTP {res_next.status_code}")
    assert res_next.status_code == 200, f"Expected 200, got {res_next.status_code}: {res_next.text}"
    q2_data = res_next.json()
    assert "question" in q2_data
    print(f"        Next Question: {q2_data['question']}")

    # 4. POST /api/interview/finish
    finish_payload = {"interview_id": interview_id}
    res_finish = client.post("/api/interview/finish", json=finish_payload)
    print(f"STEP 4: POST /api/interview/finish -> HTTP {res_finish.status_code}")
    assert res_finish.status_code == 200, f"Expected 200, got {res_finish.status_code}: {res_finish.text}"
    rep_data = res_finish.json()
    assert "overall_score" in rep_data
    print(f"        Report Overall Score: {rep_data['overall_score']}/100")

    # 5. GET /api/interview/{id}
    res_status = client.get(f"/api/interview/{interview_id}")
    print(f"STEP 5: GET /api/interview/{interview_id} -> HTTP {res_status.status_code}")
    assert res_status.status_code == 200
    assert res_status.json()["status"] == "completed"

    print("\n=======================================================")
    print("  USER-REPORTED BUG ROOT CAUSE IS COMPLETELY RESOLVED!")
    print("=======================================================")
