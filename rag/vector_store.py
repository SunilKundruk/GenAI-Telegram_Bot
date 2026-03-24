"""
SQLite-based vector store for chunk embeddings with cosine similarity search.
"""
import sqlite3
import numpy as np
from dataclasses import dataclass

import config
from rag.chunker import Chunk, load_and_chunk_documents
from rag.embedder import Embedder


@dataclass
class SearchResult:
    """A single search result with score and metadata."""
    doc_name: str
    chunk_index: int
    text: str
    score: float


class VectorStore:
    """Stores chunk embeddings in SQLite and performs cosine similarity search."""

    def __init__(self, embedder: Embedder, db_path: str | None = None):
        self.embedder = embedder
        self.db_path = db_path or config.SQLITE_DB_PATH
        self._init_db()

    def _init_db(self):
        """Create the chunks table if it doesn't exist."""
        conn = self._get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_name TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                text TEXT NOT NULL,
                embedding BLOB NOT NULL,
                UNIQUE(doc_name, chunk_index)
            )
        """)
        conn.commit()
        conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a new SQLite connection."""
        return sqlite3.connect(self.db_path)

    def _embedding_to_blob(self, embedding: np.ndarray) -> bytes:
        """Convert numpy array to bytes for SQLite storage."""
        return embedding.astype(np.float32).tobytes()

    def _blob_to_embedding(self, blob: bytes) -> np.ndarray:
        """Convert bytes back to numpy array."""
        return np.frombuffer(blob, dtype=np.float32)

    def get_indexed_docs(self) -> set[str]:
        """Return the set of doc_names already indexed."""
        conn = self._get_connection()
        cursor = conn.execute("SELECT DISTINCT doc_name FROM chunks")
        docs = {row[0] for row in cursor.fetchall()}
        conn.close()
        return docs

    def add_chunks(self, chunks: list[Chunk]):
        """
        Embed and store a list of chunks in the database.

        Args:
            chunks: List of Chunk objects to embed and store.
        """
        if not chunks:
            return

        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed_batch(texts)

        conn = self._get_connection()
        for chunk, embedding in zip(chunks, embeddings):
            conn.execute(
                """
                INSERT OR REPLACE INTO chunks (doc_name, chunk_index, text, embedding)
                VALUES (?, ?, ?, ?)
                """,
                (chunk.doc_name, chunk.chunk_index, chunk.text,
                 self._embedding_to_blob(embedding)),
            )
        conn.commit()
        conn.close()
        print(f"   📥 Stored {len(chunks)} chunks in vector store.")

    def search(self, query: str, top_k: int | None = None) -> list[SearchResult]:
        """
        Search for the most relevant chunks using cosine similarity.

        Args:
            query: The search query text.
            top_k: Number of top results to return.

        Returns:
            List of SearchResult objects sorted by relevance (highest first).
        """
        top_k = top_k or config.TOP_K
        query_embedding = self.embedder.embed(query)

        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT doc_name, chunk_index, text, embedding FROM chunks"
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return []

        # Compute cosine similarity for all chunks
        results = []
        for doc_name, chunk_index, text, emb_blob in rows:
            stored_embedding = self._blob_to_embedding(emb_blob)
            # Since embeddings are normalized, cosine similarity = dot product
            score = float(np.dot(query_embedding, stored_embedding))
            results.append(SearchResult(
                doc_name=doc_name,
                chunk_index=chunk_index,
                text=text,
                score=score,
            ))

        # Sort by score descending and return top_k
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def index_documents(self, directory: str | None = None):
        """
        Index all documents from the knowledge base directory.
        Skips documents that are already indexed.

        Args:
            directory: Path to knowledge base directory.
        """
        directory = directory or config.KNOWLEDGE_BASE_DIR
        already_indexed = self.get_indexed_docs()

        all_chunks = load_and_chunk_documents(
            directory,
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
        )

        # Filter out already-indexed docs
        new_chunks = [c for c in all_chunks if c.doc_name not in already_indexed]

        if not new_chunks:
            print("✅ All documents already indexed.")
            return

        new_docs = set(c.doc_name for c in new_chunks)
        print(f"📄 Indexing {len(new_chunks)} chunks from {len(new_docs)} new document(s)...")

        self.add_chunks(new_chunks)
        print("✅ Indexing complete.")

    def get_total_chunks(self) -> int:
        """Return the total number of chunks in the store."""
        conn = self._get_connection()
        cursor = conn.execute("SELECT COUNT(*) FROM chunks")
        count = cursor.fetchone()[0]
        conn.close()
        return count
