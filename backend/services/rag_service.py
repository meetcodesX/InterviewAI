import os
import glob
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.collection_name = 'interview_knowledge'
        self.initialized = False
        self.client = None
        self.collection = None
        self.model = None

        try:
            import chromadb
            from sentence_transformers import SentenceTransformer

            # Ensure persist directory exists
            persist_dir = os.path.abspath(settings.CHROMA_PERSIST_DIR)
            os.makedirs(persist_dir, exist_ok=True)

            self.client = chromadb.PersistentClient(path=persist_dir)
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            self.initialized = True
            logger.info(f"RAGService initialized with ChromaDB at {persist_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize RAG Service: {e}")
            self.initialized = False

    def ingest_documents(self, data_dir: Optional[str] = None) -> int:
        """Loads all markdown files from data_dir, chunks them, and stores them in ChromaDB."""
        if not self.initialized:
            logger.warning("RAG service not initialized. Cannot ingest documents.")
            return 0

        if data_dir is None:
            data_dir = settings.DATA_DIR

        data_path = Path(data_dir)
        if not data_path.exists():
            logger.warning(f"Data directory {data_dir} does not exist.")
            return 0

        try:
            try:
                from langchain_text_splitters import RecursiveCharacterTextSplitter
            except ImportError:
                from langchain.text_splitter import RecursiveCharacterTextSplitter

            md_files = list(data_path.rglob("*.md"))
            if not md_files:
                logger.info(f"No markdown files found in {data_dir}.")
                return 0

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=150,
                separators=["\n### ", "\n## ", "\n\n", "\n", " "]
            )

            total_chunks = 0
            for file_path in md_files:
                try:
                    category = file_path.parent.name
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()

                    if not text.strip():
                        continue

                    chunks = text_splitter.split_text(text)
                    if not chunks:
                        continue

                    # Generate distinct IDs that include directory name and chunk index
                    ids = [f"{category}_{file_path.stem}_{i}" for i in range(len(chunks))]
                    metadatas = [
                        {
                            "source": str(file_path.relative_to(data_path)),
                            "category": category,
                            "chunk_index": i
                        }
                        for i in range(len(chunks))
                    ]

                    # Embed using SentenceTransformer
                    embeddings = self.model.encode(chunks).tolist()

                    # Upsert to ChromaDB to allow safe re-ingestion
                    self.collection.upsert(
                        ids=ids,
                        documents=chunks,
                        embeddings=embeddings,
                        metadatas=metadatas
                    )
                    total_chunks += len(chunks)
                    logger.info(f"Ingested {len(chunks)} chunks from {file_path.name} (category: {category})")
                except Exception as file_err:
                    logger.error(f"Error ingesting file {file_path}: {file_err}")

            logger.info(f"RAG Ingestion complete. Total chunks indexed: {total_chunks}")
            return total_chunks
        except Exception as e:
            logger.error(f"Error during ingestion: {e}")
            return 0

    def retrieve_context(self, query: str, filters: Optional[dict] = None, k: int = 3) -> List[str]:
        """Retrieves top-k relevant chunks from ChromaDB based on semantic similarity."""
        if not self.initialized or self.collection is None or self.collection.count() == 0:
            return ["Standard industry interview expectations and fundamental technical principles."]

        try:
            query_embedding = self.model.encode([query]).tolist()
            query_args = {
                "query_embeddings": query_embedding,
                "n_results": min(k, self.collection.count())
            }
            if filters:
                query_args["where"] = filters

            results = self.collection.query(**query_args)

            docs = []
            similarity_scores = []

            if results and 'documents' in results and results['documents'] and results['documents'][0]:
                docs = results['documents'][0]
                distances = results.get("distances", [[]])[0]
                # In cosine space, similarity = 1.0 - distance
                similarity_scores = [round(max(0.0, 1.0 - d), 4) for d in distances] if distances else []

            # Development Mode Logging as required
            print(f"\n================== RAG RETRIEVAL DEBUG ==================")
            print(f"QUERY:\n{query}")
            print(f"\nRETRIEVED DOCUMENTS ({len(docs)} found):")
            for idx, d in enumerate(docs):
                score_str = f" [score: {similarity_scores[idx]}]" if idx < len(similarity_scores) else ""
                print(f"  Doc {idx+1}{score_str}:\n  {d[:160]}...")
            print(f"\nSIMILARITY SCORES:\n{similarity_scores}")
            print(f"=========================================================\n")

            return docs
        except Exception as e:
            logger.error(f"Error retrieving context from ChromaDB: {e}")
            return ["Core software engineering and role-specific interview standards."]

    def get_interview_context(self, job_role: str, skills: List[str], category: str, difficulty: str) -> str:
        """Constructs a targeted query and returns relevant interview context."""
        skills_str = ", ".join(skills) if skills else "general technical skills"
        query = f"Interview questions and assessment criteria for {job_role} covering {skills_str}, category: {category}, difficulty: {difficulty}"

        # Category mapping if available
        cat_filter = None
        clean_category = category.lower().strip()
        known_cats = ["hr", "behavioral", "python", "sql", "dsa", "oop", "rag", "machine_learning", "data_science", "deep_learning", "nlp", "generative_ai", "system_design", "devops", "software_engineering"]
        if clean_category in known_cats:
            cat_filter = {"category": clean_category}

        docs = self.retrieve_context(query, filters=cat_filter, k=3)
        return "\n\n---\n\n".join(docs)

    def get_relevant_context(self, query: str, category: Optional[str] = None, top_k: int = 3) -> str:
        """Retrieves formatted context documents for a specific query and optional category filter."""
        cat_filter = None
        if category:
            clean_category = category.lower().strip()
            known_cats = [
                "hr", "behavioral", "python", "sql", "dsa", "oop", "rag",
                "machine_learning", "data_science", "deep_learning", "nlp",
                "generative_ai", "system_design", "devops", "software_engineering"
            ]
            if clean_category in known_cats:
                cat_filter = {"category": clean_category}

        docs = self.retrieve_context(query=query, filters=cat_filter, k=top_k)
        return "\n\n---\n\n".join(docs) if docs else ""

    def get_unasked_knowledge_question(
        self,
        category: str,
        difficulty: str,
        asked_normalized_questions: set
    ) -> Optional[dict]:
        """Extracts a question from the local markdown knowledge base that has not been asked."""
        import re
        data_path = Path(settings.DATA_DIR)
        clean_cat = category.lower().strip()
        
        # Try finding a matching category folder or fallback to related folders
        target_dirs = [data_path / clean_cat] if (data_path / clean_cat).exists() else list(data_path.glob("*"))

        for cat_dir in target_dirs:
            q_file = cat_dir / "questions.md"
            if not q_file.exists():
                continue

            try:
                content = q_file.read_text(encoding="utf-8")
                # Look for questions in markdown format: ### Q\d+: (.+) or ### (.+)
                q_matches = re.findall(r"###\s*(?:Q\d+:\s*)?([^\n\r]+)", content)
                for q_text in q_matches:
                    q_cleaned = q_text.strip()
                    # Normalize to check
                    norm_q = " ".join(re.sub(r"[^\w\s]", "", q_cleaned.lower()).split())
                    if norm_q and norm_q not in asked_normalized_questions:
                        return {
                            "question": q_cleaned,
                            "category": cat_dir.name,
                            "difficulty": difficulty
                        }
            except Exception as e:
                logger.error(f"Error reading questions from {q_file}: {e}")

        return None


rag_service = RAGService()
