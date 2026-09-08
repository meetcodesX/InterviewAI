"""Generate sample PDF resumes for demo and testing purposes."""
import os
import pymupdf as fitz

os.makedirs("sample_resumes", exist_ok=True)

# 1. Alex Sharma - ML Engineer
doc1 = fitz.open()
page1 = doc1.new_page(width=612, height=792)  # Standard Letter size

content1 = """ALEX SHARMA
Machine Learning Engineer
Email: alex.sharma@example.com | Phone: +91 98765 43210 | Bengaluru, India
GitHub: github.com/alexsharma | LinkedIn: linkedin.com/in/alexsharma

PROFESSIONAL SUMMARY
Results-oriented Machine Learning Engineer with a strong foundation in Python, deep learning, retrieval-augmented generation (RAG), and NLP systems. Experienced in developing scalable predictive models and LLM agentic workflows.

EDUCATION
Bachelor of Technology in Computer Science & Engineering
Indian Institute of Technology (IIT) Delhi | 2020 - 2024
GPA: 8.9 / 10.0

TECHNICAL SKILLS
- Programming: Python, SQL, C++, TypeScript
- ML / AI Frameworks: PyTorch, TensorFlow, Scikit-Learn, Hugging Face Transformers
- LLM & Agents: LangChain, LangGraph, ChromaDB, Vector Databases, Prompt Engineering
- Tools & Cloud: Docker, Git, FastAPI, AWS, Linux

KEY PROJECTS
1. Autonomous Agentic Interview Trainer (2024)
   - Architected a multi-stage LangGraph workflow for adaptive candidate evaluation.
   - Built a ChromaDB vector index with semantic search to retrieve role-specific rubrics.
   - Integrated IBM Granite 3.0 foundation models for real-time answer scoring.

2. Enterprise RAG Question-Answering System (2023)
   - Developed a hybrid dense-sparse retrieval system combining BM25 and cross-encoders.
   - Reduced hallucinations by 42% through semantic verification and guardrails.

3. Multimodal Sentiment Analysis Engine (2023)
   - Fine-tuned RoBERTa models on customer feedback datasets achieving 93.4% F1-score.

CERTIFICATIONS
- Deep Learning Specialization (DeepLearning.AI)
- AWS Certified Machine Learning - Specialty
"""

rect1 = fitz.Rect(40, 40, 572, 752)
page1.insert_textbox(rect1, content1, fontsize=10.5, fontname="helv", lineheight=1.25)
doc1.save("sample_resumes/alex_sharma_ml_engineer.pdf")
doc1.close()
print("Created: sample_resumes/alex_sharma_ml_engineer.pdf")

# 2. Priya Patel - Full-Stack Developer
doc2 = fitz.open()
page2 = doc2.new_page(width=612, height=792)

content2 = """PRIYA PATEL
Full-Stack Software Engineer
Email: priya.patel@example.com | Phone: +91 91234 56789 | Pune, India
Portfolio: priyapatel.dev | GitHub: github.com/priyapatel

PROFESSIONAL SUMMARY
Passionate Full-Stack Developer with 2+ years of experience building modern web applications using Next.js, React, TypeScript, Python, and PostgreSQL. Focused on clean architecture and high-performance user experiences.

EXPERIENCE
Software Engineer - CloudTech Solutions (2023 - Present)
- Developed and maintained microservices using Python FastAPI and PostgreSQL.
- Built responsive client dashboards using Next.js 14, Tailwind CSS, and Zustand.
- Optimized database queries, reducing API latency by 35%.

Junior Web Developer - InnoTech Labs (2022 - 2023)
- Built interactive frontend components and integrated RESTful backend APIs.
- Collaborated in an agile scrum team with weekly continuous delivery sprints.

EDUCATION
B.E. in Information Technology - Pune University | 2018 - 2022

TECHNICAL SKILLS
- Frontend: React, Next.js, TypeScript, Tailwind CSS, HTML5, CSS3, Redux
- Backend: Python, FastAPI, Node.js, Express, REST APIs
- Databases: PostgreSQL, SQLite, Redis, MongoDB
- DevOps & Tools: Docker, Git, GitHub Actions, Linux, Postman
"""

rect2 = fitz.Rect(40, 40, 572, 752)
page2.insert_textbox(rect2, content2, fontsize=10.5, fontname="helv", lineheight=1.25)
doc2.save("sample_resumes/priya_patel_fullstack_dev.pdf")
doc2.close()
print("Created: sample_resumes/priya_patel_fullstack_dev.pdf")
