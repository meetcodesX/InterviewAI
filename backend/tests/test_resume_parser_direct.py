import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pymupdf as fitz
from services.resume_parser import parse_resume_text

# 1. Test Alex Sharma
doc1 = fitz.open("../sample_resumes/alex_sharma_ml_engineer.pdf")
text1 = "".join(p.get_text() for p in doc1)
p1 = parse_resume_text(text1)

print("=== RESUME 1 PARSED ===")
print("Name:", p1.name)
print("Role:", p1.target_role)
print("Skills:", p1.skills[:6])
print("Education:", p1.education)

# 2. Test Priya Patel
doc2 = fitz.open("../sample_resumes/priya_patel_fullstack_dev.pdf")
text2 = "".join(p.get_text() for p in doc2)
p2 = parse_resume_text(text2)

print("\n=== RESUME 2 PARSED ===")
print("Name:", p2.name)
print("Role:", p2.target_role)
print("Skills:", p2.skills[:6])
print("Education:", p2.education)

assert p1.name == "Alex Sharma", f"Expected 'Alex Sharma', got '{p1.name}'"
assert p2.name == "Priya Patel", f"Expected 'Priya Patel', got '{p2.name}'"
assert p1.name != p2.name, "Profiles must be different!"
assert p1.target_role != p2.target_role, "Roles must be different!"

print("\nTEST PASSED: Both resumes extracted accurately and distinctly!")
