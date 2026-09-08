import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.rag_service import rag_service

def main():
    rag_service.ingest_documents()
    print("Knowledge base ingested successfully!")

if __name__ == "__main__":
    main()
