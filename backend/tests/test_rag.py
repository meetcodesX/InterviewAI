"""Test RAG service loading and embedding directly."""
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings

print("Testing RAG components...")

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("langchain_community.embeddings imported successfully.")
except Exception as e:
    print(f"HuggingFaceEmbeddings import error: {e}")

try:
    from sentence_transformers import SentenceTransformer
    st = SentenceTransformer("all-MiniLM-L6-v2")
    vec = st.encode(["hello world"])
    print(f"SentenceTransformer working, vector shape: {vec.shape}")
except Exception as e:
    print(f"SentenceTransformer error: {e}")

try:
    import chromadb
    client = chromadb.PersistentClient(path="./test_chroma")
    col = client.get_or_create_collection(name="test_col")
    print(f"ChromaDB working, collection count: {col.count()}")
except Exception as e:
    print(f"ChromaDB error: {e}")
