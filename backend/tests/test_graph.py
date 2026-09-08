"""Test LangGraph compilation and workflow execution."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from agents.interview_agent import graph, start_interview, submit_answer, get_next_question, finish_interview
    print("LangGraph graph compiled successfully!")

    # Test starting interview
    test_profile = {
        "name": "Alex Sharma",
        "skills": ["Python", "Machine Learning", "RAG"],
        "target_role": "ML Engineer",
        "experience_level": "fresher"
    }
    test_config = {
        "job_role": "ML Engineer",
        "experience_level": "fresher",
        "interview_type": "technical",
        "difficulty": "adaptive",
        "num_questions": 3
    }
    first_q = start_interview(test_profile, test_config, "test-session-123")
    print("start_interview output:", first_q)

    # Test submitting answer
    ans_result = submit_answer("test-session-123", "Supervised learning uses labeled training datasets, whereas unsupervised learning finds hidden patterns in unlabeled data.")
    print("submit_answer evaluation output:", ans_result)

    # Test getting next question
    next_q = get_next_question("test-session-123")
    print("get_next_question output:", next_q)

    # Test finish interview
    report = finish_interview("test-session-123")
    print("finish_interview report score:", report.get("overall_score"))
    print("ALL AGENT TESTS PASSED!")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"FAILED: {e}")
