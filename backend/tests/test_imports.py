"""Check and verify all required python dependencies for serverless production and local dev."""

import sys

required = [
    'fastapi',
    'uvicorn',
    'sqlalchemy',
    'pydantic',
    'dotenv',
    'fitz',
    'langgraph',
    'ibm_watsonx_ai',
    'httpx',
]

optional = [
    'chromadb',
    'sentence_transformers',
]

all_passed = True
print("=== Required Production Dependencies ===")
for mod in required:
    try:
        __import__(mod)
        print(f"PASS (required): {mod}")
    except Exception as e:
        print(f"FAIL (required): {mod} -> {e}")
        all_passed = False

print("\n=== Optional Local Dev Dependencies ===")
for mod in optional:
    try:
        __import__(mod)
        print(f"AVAILABLE (optional): {mod}")
    except Exception as e:
        print(f"INFO (not required on serverless): {mod} -> {e}")

if not all_passed:
    sys.exit(1)
print("\nAll required production dependencies verified successfully!")
