"""Check and verify all required python dependencies."""

import sys

required = [
    'fastapi',
    'uvicorn',
    'sqlalchemy',
    'pydantic',
    'dotenv',
    'fitz',
    'langchain',
    'langgraph',
    'chromadb',
    'ibm_watsonx_ai',
    'sentence_transformers'
]

for mod in required:
    try:
        __import__(mod)
        print(f"PASS: {mod}")
    except Exception as e:
        print(f"FAIL: {mod} -> {e}")
