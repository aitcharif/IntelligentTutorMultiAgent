"""Embedding generation for RAG"""

from typing import List
from loguru import logger


class EmbeddingGenerator:
    """Generate embeddings for text"""

    def __init__(self, model_name: str = "paraphrase-multilingual-mpnet-base-v2"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        """Lazy load embedding model"""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
                logger.info(f"Embedding model loaded: {self.model_name}")
            except ImportError:
                logger.error("sentence-transformers not installed")
                raise

    async def generate(self, text: str) -> List[float]:
        """Generate embedding for text"""
        try:
            self._load_model()
            embedding = self._model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []

    async def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            self._load_model()
            embeddings = self._model.encode(texts)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return []
