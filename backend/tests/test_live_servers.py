"""Test live running servers: Next.js (port 3000) and FastAPI (port 8000)."""
import httpx
import sys

print("Verifying live servers...")

# 1. Check Backend live health
with httpx.Client(timeout=10.0) as client:
    resp = client.get("http://127.0.0.1:8000/api/health")
    print(f"Backend GET /api/health: {resp.status_code} -> {resp.json()}")
    assert resp.status_code == 200, "Backend health failed"

    # 2. Check Next.js Frontend home page
    resp_front = client.get("http://127.0.0.1:3000/")
    print(f"Frontend GET /: {resp_front.status_code} (length: {len(resp_front.text)} bytes)")
    assert resp_front.status_code == 200, "Frontend home page failed"
    assert "InterviewAI" in resp_front.text, "Landing page text missing"

    # 3. Check Next.js API rewrite proxy to backend
    resp_proxy = client.get("http://127.0.0.1:3000/api/health")
    print(f"Frontend Next.js Rewrite Proxy /api/health: {resp_proxy.status_code} -> {resp_proxy.json()}")
    assert resp_proxy.status_code == 200, "Next.js API proxy failed"

    # 4. Perform live complete interview flow through Next.js rewrite proxy!
    print("\n--- Live E2E User Flow via Next.js Proxy ---")
    # A. Create Demo Profile
    profile = {
        "name": "Alex Sharma",
        "target_role": "ML Engineer",
        "skills": ["Python", "Machine Learning", "Deep Learning", "RAG", "NLP"],
        "experience_level": "Fresher",
        "years_of_experience": 0,
        "education": ["B.Tech CS"],
        "projects": ["RAG Assistant"],
        "experience": [],
        "certifications": []
    }
    config = {
        "job_role": "ML Engineer",
        "experience_level": "Fresher",
        "interview_type": "technical",
        "difficulty": "adaptive",
        "num_questions": 3
    }
    create_res = client.post("http://127.0.0.1:3000/api/interview/create", json={"profile": profile, "config": config})
    assert create_res.status_code == 200, f"Create interview failed: {create_res.text}"
    q1 = create_res.json()
    interview_id = q1["interview_id"]
    print(f"1. Interview created successfully: ID = {interview_id}")
    print(f"   Q1: {q1['question']} (difficulty: {q1['difficulty']})")

    # B. Submit Answer 1
    ans1_res = client.post("http://127.0.0.1:3000/api/interview/answer", json={
        "interview_id": interview_id,
        "question_id": q1["question_id"],
        "answer": "Supervised learning utilizes labeled datasets where ground truth target variables guide optimization. Unsupervised learning identifies geometric structures, clusters, or lower-dimensional representations directly from unlabeled observations."
    })
    assert ans1_res.status_code == 200, f"Submit answer failed: {ans1_res.text}"
    eval1 = ans1_res.json()["evaluation"]
    print(f"2. Answer 1 evaluated: score = {eval1['overall_score']}/10, clarity = {eval1['clarity']}/10")

    # C. Next Question
    next_res = client.post("http://127.0.0.1:3000/api/interview/next", json={"interview_id": interview_id})
    assert next_res.status_code == 200, f"Next question failed: {next_res.text}"
    q2 = next_res.json()
    print(f"3. Next question retrieved: Q2 ({q2['difficulty']}): {q2['question']}")

    # D. Complete interview and get final report
    finish_res = client.post("http://127.0.0.1:3000/api/interview/finish", json={"interview_id": interview_id})
    assert finish_res.status_code == 200, f"Finish interview failed: {finish_res.text}"
    report = finish_res.json()
    print(f"4. Interview finished: Overall Score = {report['overall_score']}/100")
    print(f"   Role Readiness = {report['role_readiness_score']}/100")
    print(f"   Key Strengths = {report.get('strengths')}")
    print(f"   Roadmap Recommendations = {len(report.get('recommendations', []))} items")

    # E. Dashboard stats check
    dash_res = client.get("http://127.0.0.1:3000/api/dashboard/stats")
    assert dash_res.status_code == 200, f"Dashboard fetch failed: {dash_res.text}"
    dash = dash_res.json()
    print(f"5. Dashboard updated: Total interviews = {dash['total_interviews']}, Avg Score = {dash['average_score']}")

print("\n=================================================================")
print("LIVE SERVERS & PROXY VERIFICATION: 100% WORKING & VERIFIED!")
print("=================================================================")
