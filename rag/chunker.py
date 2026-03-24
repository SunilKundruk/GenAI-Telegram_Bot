"""
Document chunker — splits Markdown files into overlapping text chunks.
"""
import os
import re
from dataclasses import dataclass

@dataclass
class Chunk:
    """A single text chunk from a document."""
    doc_name: str
    chunk_index: int
    text: str


def _clean_text(text: str) -> str:
    """Remove excessive whitespace while preserving paragraph breaks."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def chunk_text(
    text: str,
    doc_name: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[Chunk]:
    """
    Split text into overlapping chunks.

    Args:
        text: The full document text.
        doc_name: Name of the source document.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Overlap between consecutive chunks.

    Returns:
        List of Chunk objects.
    """
    text = _clean_text(text)

    if len(text) <= chunk_size:
        return [Chunk(doc_name=doc_name, chunk_index=0, text=text)]

    chunks = []
    start = 0
    index = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at a sentence or paragraph boundary
        if end < len(text):
            # Look for the last newline or period within the chunk
            last_break = text.rfind('\n', start + chunk_size // 2, end)
            if last_break == -1:
                last_break = text.rfind('. ', start + chunk_size // 2, end)
            if last_break != -1:
                end = last_break + 1

        chunk_text_content = text[start:end].strip()
        if chunk_text_content:
            chunks.append(Chunk(
                doc_name=doc_name,
                chunk_index=index,
                text=chunk_text_content,
            ))
            index += 1

        start = end - chunk_overlap
        if start >= len(text):
            break

    return chunks


def load_and_chunk_documents(
    directory: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[Chunk]:
    """
    Load all .md and .txt files from a directory and chunk them.

    Args:
        directory: Path to the knowledge base directory.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Overlap between consecutive chunks.

    Returns:
        List of all Chunk objects across all documents.
    """
    all_chunks = []

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Knowledge base directory not found: {directory}")

    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(('.md', '.txt')):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        doc_name = os.path.splitext(filename)[0]
        chunks = chunk_text(content, doc_name, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)

    return all_chunks
