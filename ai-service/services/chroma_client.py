import os
import logging
from pathlib import Path
from dotenv import load_dotenv

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Load env 
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s"
)
logger = logging.getLogger("ChromaClient")

# Constants
CHROMA_PATH       = os.getenv("CHROMA_PATH", "./chroma_data")
COLLECTION_NAME   = os.getenv("CHROMA_COLLECTION", "risk_culture_docs")
EMBEDDING_MODEL   = "all-MiniLM-L6-v2"   # fast, lightweight, good quality


class ChromaClient:
    """
    Manages the ChromaDB persistent vector store.

    Features:
      - Persistent storage in chroma_data/ folder
      - Sentence-transformer embeddings (all-MiniLM-L6-v2)
      - Add documents with metadata
      - Query top-N similar documents
      - Document count for /health endpoint
    """

    def __init__(self):
        logger.info("Initialising ChromaDB client...")
        logger.info(f"Storage path : {CHROMA_PATH}")
        logger.info(f"Collection   : {COLLECTION_NAME}")
        logger.info(f"Embedding    : {EMBEDDING_MODEL}")

        # Init persistent ChromaDB
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection 
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}  # cosine similarity
        )

        # Load embedding model 
        logger.info("Loading sentence-transformer model (first run may take a moment)...")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("ChromaDB client ready ✓")

    # Embed text 
    def embed(self, text: str) -> list:
        """Convert text to embedding vector."""
        return self.embedding_model.encode(text).tolist()

    # Add documents
    def add_documents(self, documents: list[dict]) -> int:
        """
        Add a list of documents to ChromaDB.

        Each document must have:
            {
                "id":       str,   # unique ID
                "text":     str,   # content to embed
                "metadata": dict   # optional extra info
            }

        Returns number of documents added.
        """
        if not documents:
            logger.warning("add_documents called with empty list")
            return 0

        ids        = []
        embeddings = []
        texts      = []
        metadatas  = []

        for doc in documents:
            ids.append(doc["id"])
            texts.append(doc["text"])
            embeddings.append(self.embed(doc["text"]))
            metadatas.append(doc.get("metadata", {}))

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

        logger.info(f"Added {len(documents)} documents to ChromaDB")
        return len(documents)

    # Query documents
    def query(self, query_text: str, n_results: int = 3) -> list[dict]:
        """
        Find the top-N most similar documents for a query.

        Returns list of:
            {
                "id":       str,
                "text":     str,
                "metadata": dict,
                "score":    float  # similarity score (lower = more similar in cosine)
            }
        """
        total_docs = self.count()
        if total_docs == 0:
            logger.warning("ChromaDB collection is empty — no results to return")
            return []

        # Cap n_results to available docs
        n_results = min(n_results, total_docs)

        query_embedding = self.embed(query_text)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        # Format results
        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id":       results["ids"][0][i],
                "text":     results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score":    round(results["distances"][0][i], 4)
            })

        logger.info(f"Query returned {len(output)} results")
        return output

    # Count documents
    def count(self) -> int:
        """Return total number of documents in collection."""
        return self.collection.count()

    # Delete document
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID. Returns True if successful."""
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Deleted document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete document {doc_id}: {e}")
            return False

    # Reset collection
    def reset_collection(self) -> bool:
        """
        Delete and recreate the collection.
        WARNING: This deletes ALL documents. Use only in testing.
        """
        try:
            self.client.delete_collection(COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            logger.warning("Collection reset — all documents deleted")
            return True
        except Exception as e:
            logger.error(f"Failed to reset collection: {e}")
            return False


#Singleton instance 
# Import this in your routes: from services.chroma_client import chroma_client
chroma_client = ChromaClient()