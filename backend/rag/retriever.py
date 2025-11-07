"""Document retriever for RAG system"""

from typing import List, Dict, Any, Optional
from loguru import logger


class DocumentRetriever:
    """Retrieve relevant documents from knowledge base"""

    def __init__(self, vector_store=None, embedding_generator=None):
        """
        Initialize retriever

        Args:
            vector_store: Vector database instance
            embedding_generator: Embedding generator instance
        """
        self.vector_store = vector_store
        self.embedding_generator = embedding_generator

    async def search(
        self, query: str, top_k: int = 5, threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents

        Args:
            query: Search query
            top_k: Number of results
            threshold: Minimum similarity score

        Returns:
            List of relevant documents
        """
        try:
            if not self.vector_store or not self.embedding_generator:
                logger.warning("RAG system not fully configured")
                return self._fallback_search(query, top_k)

            # Generate query embedding
            query_embedding = await self.embedding_generator.generate(query)

            # Search in vector store
            results = await self.vector_store.search(
                embedding=query_embedding,
                top_k=top_k,
                threshold=threshold,
            )

            return results

        except Exception as e:
            logger.error(f"Error in document retrieval: {str(e)}")
            return self._fallback_search(query, top_k)

    def _fallback_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Fallback search using simple keyword matching"""
        # Simple fallback - return example documents
        examples = [
            {
                "content": "Les variables en Python sont des conteneurs pour stocker des données. "
                          "Exemple: x = 5, nom = 'Ahmed'",
                "metadata": {"topic": "variables", "language": "fr"},
                "score": 0.8,
            },
            {
                "content": "Les boucles permettent de répéter des instructions. "
                          "Python a deux types: for et while.",
                "metadata": {"topic": "loops", "language": "fr"},
                "score": 0.7,
            },
            {
                "content": "Les fonctions en Python se définissent avec def. "
                          "Exemple: def saluer(nom): return f'Bonjour {nom}'",
                "metadata": {"topic": "functions", "language": "fr"},
                "score": 0.6,
            },
        ]

        # Simple keyword filtering
        query_lower = query.lower()
        filtered = [
            doc for doc in examples
            if any(word in doc["content"].lower() for word in query_lower.split())
        ]

        return filtered[:top_k] if filtered else examples[:top_k]
