"""Embedding generation using sentence-transformers."""

import numpy as np
from sentence_transformers import SentenceTransformer

from ram.models.chunk import Chunk


class EmbeddingGenerator:
    """Generates embeddings for text chunks using sentence-transformers.

    Uses the sentence-transformers/all-MiniLM-L6-v2 model which produces
    384-dimensional embeddings suitable for semantic search.

    Attributes:
        model: SentenceTransformer model instance
        model_name: Name of the embedding model
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize EmbeddingGenerator.

        Args:
            model_name: Name of sentence-transformers model to use
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def generate(
        self, chunks: list[Chunk], show_progress: bool = False
    ) -> np.ndarray:
        """Generate embeddings for a list of chunks.

        Args:
            chunks: List of Chunk objects to embed
            show_progress: Whether to show progress bar (for large batches)

        Returns:
            Numpy array of shape (n_chunks, 384) with embeddings
        """
        # Extract text from chunks
        texts = [chunk.text for chunk in chunks]

        # Generate embeddings
        embeddings = self.model.encode(texts, show_progress_bar=show_progress)

        return embeddings
