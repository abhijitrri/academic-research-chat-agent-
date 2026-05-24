"""Retrieval-Augmented Generation (RAG) system for research documents."""
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer


class RAGSystem:
    """Retrieval system for document search and synthesis."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize RAG system with embedding model.

        Args:
            model_name: Sentence transformer model to use for embeddings
        """
        self.embedder = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = None

    def add_documents(self, documents: List[str]):
        """Add documents to the retrieval system.

        Args:
            documents: List of document texts to index
        """
        self.documents.extend(documents)
        self.embeddings = self.embedder.encode(self.documents, convert_to_tensor=True)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Search for relevant documents.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of (document, similarity_score) tuples
        """
        if not self.documents:
            return []

        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        similarities = query_embedding @ self.embeddings.T

        top_indices = np.argsort(similarities.cpu().numpy())[-top_k:][::-1]
        return [(self.documents[i], float(similarities[i])) for i in top_indices]

    def clear(self):
        """Clear all documents."""
        self.documents = []
        self.embeddings = None
