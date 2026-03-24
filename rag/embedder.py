"""
Embedding module — wraps sentence-transformers for local text embeddings.
"""
import numpy as np
from sentence_transformers import SentenceTransformer

import config


class Embedder:
    """Generates text embeddings using a local sentence-transformer model."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or config.EMBEDDING_MODEL
        self._model = None

    @property
    def model(self) -> SentenceTransformer:
        """Lazy-load the model on first use."""
        if self._model is None:
            print(f"📦 Loading embedding model: {self.model_name}...")
            self._model = SentenceTransformer(self.model_name)
            print("✅ Embedding model loaded.")
        return self._model

    def embed(self, text: str) -> np.ndarray:
        """
        Embed a single text string.

        Args:
            text: Input text to embed.

        Returns:
            1-D numpy array of the embedding vector.
        """
        return self.model.encode(text, normalize_embeddings=True)

    def embed_batch(self, texts: list[str], batch_size: int = 32) -> np.ndarray:
        """
        Embed a batch of text strings.

        Args:
            texts: List of input texts.
            batch_size: Batch size for encoding.

        Returns:
            2-D numpy array of shape (len(texts), embedding_dim).
        """
        return self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > 50,
        )
