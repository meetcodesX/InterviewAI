import os
import re
import math
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from collections import Counter
from config import settings

logger = logging.getLogger(__name__)

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}


def _tokenize(text: str) -> List[str]:
    """Tokenize and filter common stopwords and trivial characters."""
    words = re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())
    return [w for w in words if w not in STOPWORDS]


def _fallback_split_text(text: str, chunk_size: int = 800, chunk_overlap: int = 150) -> List[str]:
    """Lightweight pure-python fallback text splitter preserving markdown headers."""
    sections = re.split(r"(?=\n### |\n## |\n# )", text)
    chunks = []
    current = ""
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        if len(current) + len(sec) < chunk_size:
            current = f"{current}\n\n{sec}".strip()
        else:
            if current:
                chunks.append(current)
            if len(sec) <= chunk_size:
                current = sec
            else:
                # Split large section by paragraphs
                paragraphs = sec.split("\n\n")
                sub = ""
                for p in paragraphs:
                    if len(sub) + len(p) < chunk_size:
                        sub = f"{sub}\n\n{p}".strip()
                    else:
                        if sub:
                            chunks.append(sub)
                        sub = p
                current = sub
    if current:
        chunks.append(current)
    return chunks


class KnowledgeChunk:
    """Represents an indexed chunk from the local markdown knowledge base."""
    def __init__(self, chunk_id: str, text: str, category: str, source: str, chunk_index: int):
        self.chunk_id = chunk_id
        self.text = text
        self.category = category.lower().strip()
        self.source = source
        self.chunk_index = chunk_index
        tokens = _tokenize(text)
        self.token_counts = Counter(tokens)
        self.token_set = set(self.token_counts.keys())
        first_line = text.strip().split("\n")[0]
        self.header_tokens = set(_tokenize(first_line))


class RAGService:
    """Hybrid RAG Service for InterviewAI.
    
    Supports ChromaDB + SentenceTransformer when available, while providing
    a zero-dependency, ultra-fast BM25/TF-IDF Markdown Knowledge Retriever for
    production serverless environments (e.g. Vercel) under the 500MB limit.
    """
    def __init__(self):
        self.collection_name = 'interview_knowledge'
        self.initialized = False
        self.client = None
        self.collection = None
        self.model = None
        self.docs_cache: List[KnowledgeChunk] = []
        self.doc_freq: Dict[str, int] = {}
        self.num_docs: int = 0
        self._ingested = False

    def _ensure_initialized(self) -> None:
        """Lazily index the markdown knowledge base on first retrieval request."""
        if not self._ingested:
            # In serverless environments (e.g. Vercel), do not attempt to load local transformers
            if not os.getenv("VERCEL") and not os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
                try:
                    import chromadb
                    from sentence_transformers import SentenceTransformer

                    persist_dir = os.path.abspath(settings.CHROMA_PERSIST_DIR)
                    os.makedirs(persist_dir, exist_ok=True)

                    self.client = chromadb.PersistentClient(path=persist_dir)
                    self.model = SentenceTransformer("all-MiniLM-L6-v2")
                    self.collection = self.client.get_or_create_collection(
                        name=self.collection_name,
                        metadata={"hnsw:space": "cosine"}
                    )
                    logger.info(f"RAGService initialized with ChromaDB at {persist_dir}")
                except Exception as e:
                    logger.info(f"Heavy ML packages not loaded ({e}). Using lightweight built-in knowledge retriever.")
                    self.client = None
                    self.collection = None
                    self.model = None

            try:
                self.ingest_documents()
            except Exception as ingest_err:
                logger.error(f"Failed to ingest knowledge markdown: {ingest_err}")
            self._ingested = True
            self.initialized = len(self.docs_cache) > 0 or (self.collection is not None and self.collection.count() > 0)

    def ingest_documents(self, data_dir: Optional[str] = None) -> int:
        """Loads all markdown files from data_dir, chunks them, and indexes them in cache and ChromaDB (if active)."""
        if data_dir is None:
            data_dir = settings.DATA_DIR

        data_path = Path(data_dir)
        if not data_path.exists():
            logger.warning(f"Data directory {data_dir} does not exist.")
            return 0

        # Attempt to use langchain splitter if installed, else fallback
        splitter_func = _fallback_split_text
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            r_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=150,
                separators=["\n### ", "\n## ", "\n\n", "\n", " "]
            )
            splitter_func = r_splitter.split_text
        except Exception:
            pass

        md_files = list(data_path.rglob("*.md"))
        if not md_files:
            logger.info(f"No markdown files found in {data_dir}.")
            return 0

        new_docs: List[KnowledgeChunk] = []
        chroma_ids = []
        chroma_texts = []
        chroma_metas = []

        for file_path in md_files:
            try:
                category = file_path.parent.name
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                if not text.strip():
                    continue

                chunks = splitter_func(text)
                for idx, chunk_text in enumerate(chunks):
                    chunk_id = f"{category}_{file_path.stem}_{idx}"
                    chunk_obj = KnowledgeChunk(
                        chunk_id=chunk_id,
                        text=chunk_text,
                        category=category,
                        source=str(file_path.relative_to(data_path)),
                        chunk_index=idx
                    )
                    new_docs.append(chunk_obj)
                    if self.collection is not None and self.model is not None:
                        chroma_ids.append(chunk_id)
                        chroma_texts.append(chunk_text)
                        chroma_metas.append({
                            "source": str(file_path.relative_to(data_path)),
                            "category": category,
                            "chunk_index": idx
                        })
            except Exception as file_err:
                logger.error(f"Error ingesting file {file_path}: {file_err}")

        self.docs_cache = new_docs
        self.num_docs = len(new_docs)

        # Compute document frequencies for TF-IDF / BM25
        self.doc_freq = Counter()
        for doc in self.docs_cache:
            for term in doc.token_set:
                self.doc_freq[term] += 1

        # Optionally upsert to ChromaDB if active
        if self.collection is not None and self.model is not None and chroma_texts:
            try:
                embeddings = self.model.encode(chroma_texts).tolist()
                self.collection.upsert(
                    ids=chroma_ids,
                    documents=chroma_texts,
                    embeddings=embeddings,
                    metadatas=chroma_metas
                )
            except Exception as chroma_err:
                logger.error(f"ChromaDB upsert error: {chroma_err}")

        self.initialized = len(self.docs_cache) > 0
        logger.info(f"RAG Ingestion complete. Total knowledge chunks indexed: {len(self.docs_cache)}")
        return len(self.docs_cache)

    def retrieve_context(self, query: str, filters: Optional[dict] = None, k: int = 3) -> List[str]:
        """Retrieves top-k relevant chunks from ChromaDB (if available) or built-in BM25/TF-IDF ranker."""
        self._ensure_initialized()
        # 1. Try ChromaDB if fully loaded and populated
        if self.collection is not None and self.model is not None:
            try:
                count = self.collection.count()
                if count > 0:
                    query_embedding = self.model.encode([query]).tolist()
                    query_args = {
                        "query_embeddings": query_embedding,
                        "n_results": min(k, count)
                    }
                    if filters:
                        query_args["where"] = filters
                    results = self.collection.query(**query_args)
                    if results and 'documents' in results and results['documents'] and results['documents'][0]:
                        docs = results['documents'][0]
                        distances = results.get("distances", [[]])[0]
                        scores = [round(max(0.0, 1.0 - d), 4) for d in distances] if distances else []
                        self._log_debug(query, docs, scores)
                        return docs
            except Exception as chroma_err:
                logger.warning(f"ChromaDB retrieval error ({chroma_err}). Using built-in retriever.")

        # 2. Built-in fast BM25/TF-IDF knowledge retriever
        if not self.docs_cache:
            return ["Standard industry interview expectations and fundamental technical principles."]

        q_tokens = _tokenize(query)
        cat_filter = (filters.get("category", "").lower().strip()) if filters else ""

        scored_candidates = []
        for doc in self.docs_cache:
            # Check category filter if specified
            if cat_filter and doc.category != cat_filter:
                continue

            score = 0.0
            for term in q_tokens:
                if term in doc.token_counts:
                    tf = doc.token_counts[term]
                    df = self.doc_freq.get(term, 1)
                    idf = math.log((self.num_docs + 1.0) / (df + 0.5)) + 1.0
                    header_boost = 2.0 if term in doc.header_tokens else 1.0
                    score += tf * idf * header_boost

            # Category boost if category matches query keywords
            if doc.category in query.lower():
                score *= 1.5

            if score > 0.0:
                # Length normalization
                norm_score = score / (math.sqrt(len(doc.token_counts)) + 5.0)
                scored_candidates.append((norm_score, doc))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        docs = []
        scores = []
        for s, doc in scored_candidates[:k]:
            docs.append(doc.text)
            scores.append(round(float(s), 4))

        # Fallback if no matching terms found
        if not docs:
            # Pick first available from the category, or any category
            fallback_docs = [d for d in self.docs_cache if (not cat_filter or d.category == cat_filter)]
            for d in fallback_docs[:k]:
                docs.append(d.text)
                scores.append(0.5)

        if not docs:
            docs = ["Standard industry interview expectations and fundamental technical principles."]
            scores = [0.5]

        self._log_debug(query, docs, scores)
        return docs

    def _log_debug(self, query: str, docs: List[str], similarity_scores: List[float]) -> None:
        """Prints development-mode debug output for RAG retrieval."""
        print(f"\n================== RAG RETRIEVAL DEBUG ==================")
        print(f"QUERY:\n{query}")
        print(f"\nRETRIEVED DOCUMENTS ({len(docs)} found):")
        for idx, d in enumerate(docs):
            score_str = f" [score: {similarity_scores[idx]}]" if idx < len(similarity_scores) else ""
            print(f"  Doc {idx+1}{score_str}:\n  {d[:160]}...")
        print(f"\nSIMILARITY SCORES:\n{similarity_scores}")
        print(f"=========================================================\n")

    def get_interview_context(self, job_role: str, skills: List[str], category: str, difficulty: str) -> str:
        """Constructs a targeted query and returns relevant interview context."""
        skills_str = ", ".join(skills) if skills else "general technical skills"
        query = f"Interview questions and assessment criteria for {job_role} covering {skills_str}, category: {category}, difficulty: {difficulty}"

        cat_filter = None
        clean_category = category.lower().strip()
        known_cats = [
            "hr", "behavioral", "python", "sql", "dsa", "oop", "rag",
            "machine_learning", "data_science", "deep_learning", "nlp",
            "generative_ai", "system_design", "devops", "software_engineering"
        ]
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
        self._ensure_initialized()
        data_path = Path(settings.DATA_DIR)
        clean_cat = category.lower().strip()

        target_dirs = [data_path / clean_cat] if (data_path / clean_cat).exists() else list(data_path.glob("*"))

        for cat_dir in target_dirs:
            q_file = cat_dir / "questions.md"
            if not q_file.exists():
                continue

            try:
                content = q_file.read_text(encoding="utf-8")
                q_matches = re.findall(r"###\s*(?:Q\d+:\s*)?([^\n\r]+)", content)
                for q_text in q_matches:
                    q_cleaned = q_text.strip()
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
