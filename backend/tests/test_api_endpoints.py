"""Comprehensive API endpoint testing for InterviewAI."""
import sys
import io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from main import app
from database.db import init_db
import pymupdf as fitz

# Ensure tables are initialized
init_db()
client = TestClient(app)

print("--- 1. Testing Health Endpoint ---")
res = client.get("/api/health")
assert res.status_code == 200, f"Health check failed: {res.text}"
health_data = res.json()
print("Health status:", health_data)
assert health_data["status"] == "ok"
assert health_data["rag_status"] == "initialized"

print("\n--- 2. Testing Manual Profile Endpoint ---")
manual_payload = {
    "name": "Alex Sharma",
    "target_role": "ML Engineer",
    "experience_level": "Fresher",
    "skills": "Python, Machine Learning, Deep Learning, RAG, NLP",
    "years_of_experience": 0
}
res = client.post("/api/profile/manual", json=manual_payload)
assert res.status_code == 200, f"Manual profile failed: {res.text}"
profile = res.json()
print("Profile created:", profile["name"], profile["target_role"], profile["skills"])

print("\n--- 3. Testing PDF Resume Upload Endpoint ---")
doc = fitz.open()
page = doc.new_page()
rect = fitz.Rect(50, 50, 500, 700)
page.insert_textbox(rect, "Alex Sharma\nML Engineer\nSkills: Python, Machine Learning, PyTorch, LangGraph, RAG\nEducation: B.Tech CS", fontsize=12)
pdf_data = doc.tobytes()
doc.close()

files = {"file": ("resume.pdf", pdf_data, "application/pdf")}
res = client.post("/api/resume/upload", files=files)
assert res.status_code == 200, f"Resume upload failed: {res.text}"
upload_data = res.json()
print("Resume uploaded & parsed text length:", len(upload_data["resume_text"]))
assert "Alex Sharma" in upload_data["resume_text"]

print("\n--- 4. Testing Interview Creation (Question 1) ---")
create_payload = {
    "profile": profile,
    "config": {
        "job_role": "ML Engineer",
        "experience_level": "Fresher",
        "interview_type": "technical",
        "difficulty": "adaptive",
        "num_questions": 3
    }
}
res = client.post("/api/interview/create", json=create_payload)
assert res.status_code == 200, f"Interview creation failed: {res.text}"
q1 = res.json()
interview_id = q1["interview_id"]
q1_id = q1["question_id"]
print(f"Created Interview ID: {interview_id}")
print(f"Question 1 ({q1['difficulty']}): {q1['question']}")

print("\n--- 5. Testing Answer Submission for Q1 ---")
answer_payload = {
    "interview_id": interview_id,
    "question_id": q1_id,
    "answer": "Supervised learning algorithms are trained using labeled datasets where the input corresponds to a known ground truth output. Unsupervised learning models explore unlabeled data to identify latent patterns, clustering structures, or dimensionality reduction without external guidance."
}
res = client.post("/api/interview/answer", json=answer_payload)
assert res.status_code == 200, f"Answer submission failed: {res.text}"
ans_eval = res.json()
evaluation = ans_eval["evaluation"]
print("Q1 Evaluation Score:", evaluation["overall_score"], "/ 10")
print("Technical Accuracy:", evaluation["technical_accuracy"], "/ 10")
print("Strengths:", evaluation["strengths"])
print("Recommended Next Difficulty:", evaluation["recommended_difficulty"])

print("\n--- 6. Testing Next Question (Q2) ---")
res = client.post("/api/interview/next", json={"interview_id": interview_id})
assert res.status_code == 200, f"Next question failed: {res.text}"
q2 = res.json()
q2_id = q2["question_id"]
print(f"Question 2 ({q2['difficulty']}): {q2['question']}")

print("\n--- 7. Testing Weak Answer Submission for Q2 ---")
weak_answer_payload = {
    "interview_id": interview_id,
    "question_id": q2_id,
    "answer": "I don't know much about this."
}
res = client.post("/api/interview/answer", json=weak_answer_payload)
assert res.status_code == 200, f"Answer 2 submission failed: {res.text}"
ans2_eval = res.json()["evaluation"]
print("Q2 Evaluation Score:", ans2_eval["overall_score"], "/ 10")
print("Weaknesses identified:", ans2_eval["weaknesses"])

print("\n--- 8. Testing Interview Status Endpoint ---")
res = client.get(f"/api/interview/{interview_id}")
assert res.status_code == 200, f"Status fetch failed: {res.text}"
status_data = res.json()
print("Interview Status:", status_data["status"], "| Questions completed:", status_data["current_question"])

print("\n--- 9. Testing Interview Finish and Final Report ---")
res = client.post("/api/interview/finish", json={"interview_id": interview_id})
assert res.status_code == 200, f"Finish interview failed: {res.text}"
report = res.json()
print("Report Overall Score:", report["overall_score"], "/ 100")
print("Difficulty progression:", report.get("difficulty_progression"))
print("Recommendations count:", len(report.get("recommendations", [])))

print("\n--- 10. Testing Report Retrieval Endpoint ---")
res = client.get(f"/api/report/{interview_id}")
assert res.status_code == 200, f"Get report failed: {res.text}"
fetched_report = res.json()
assert fetched_report["overall_score"] == report["overall_score"]
print("Report retrieved successfully via GET /api/report/{id}")

print("\n--- 11. Testing Dashboard Stats ---")
res = client.get("/api/dashboard/stats")
assert res.status_code == 200, f"Dashboard stats failed: {res.text}"
stats = res.json()
print("Total completed interviews in stats:", stats["total_interviews"])
print("Average score:", stats["average_score"])
print("Recent interviews:", len(stats["recent_interviews"]))

print("\n================================================")
print("ALL BACKEND INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
print("================================================")
