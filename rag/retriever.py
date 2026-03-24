"""
RAG retriever — orchestrates retrieval + LLM answer generation.
"""
from google import genai

import config
from rag.vector_store import VectorStore, SearchResult
from utils.cache import query_cache


def _build_rag_prompt(
    query: str,
    context_chunks: list[SearchResult],
    history: list[dict] | None = None,
) -> str:
    """
    Build the prompt for the LLM with retrieved context and conversation history.
    """
    # Format context chunks with source info
    context_parts = []
    for i, result in enumerate(context_chunks, 1):
        context_parts.append(
            f"[Source: {result.doc_name}.md | Relevance: {result.score:.2f}]\n"
            f"{result.text}"
        )
    context_text = "\n\n---\n\n".join(context_parts)

    # Format conversation history
    history_text = ""
    if history:
        history_lines = []
        for msg in history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_lines.append(f"{role.capitalize()}: {content}")
        history_text = "\n\nRecent conversation:\n" + "\n".join(history_lines)

    prompt = f"""You are a helpful assistant that answers questions based on the provided knowledge base context. 

INSTRUCTIONS:
- Answer the question using ONLY the information from the context below.
- If the context doesn't contain enough information, say so honestly.
- Keep your answer concise and well-structured.
- At the end, mention which source document(s) you used.

CONTEXT:
{context_text}
{history_text}

QUESTION: {query}

ANSWER:"""

    return prompt


class Retriever:
    """Orchestrates the full RAG pipeline: retrieve → generate → respond."""

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self._configure_llm()

    def _configure_llm(self):
        """Configure the Gemini API client."""
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)

    def retrieve_answer(
        self,
        query: str,
        history: list[dict] | None = None,
    ) -> dict:
        """
        Full RAG pipeline: embed query → retrieve chunks → generate answer.

        Args:
            query: The user's question.
            history: Optional list of recent conversation messages.

        Returns:
            Dict with 'answer' (str) and 'sources' (list of dicts with doc, snippet).
        """
        # Check cache first
        cached = query_cache.get(query)
        if cached is not None:
            cached["from_cache"] = True
            return cached

        # 1. Retrieve relevant chunks
        results = self.vector_store.search(query, top_k=config.TOP_K)

        if not results:
            return {
                "answer": "I couldn't find any relevant information in my knowledge base. "
                          "Please try rephrasing your question.",
                "sources": [],
                "from_cache": False,
            }

        # 2. Build prompt with context
        prompt = _build_rag_prompt(query, results, history)

        # 3. Generate answer using Gemini
        try:
            response = self.client.models.generate_content(
                model=config.LLM_MODEL,
                contents=prompt,
            )
            answer = response.text.strip()
        except Exception as e:
            answer = f"⚠️ Error generating answer: {str(e)}"

        # 4. Prepare source information
        sources = [
            {
                "doc": r.doc_name,
                "snippet": r.text[:150] + "..." if len(r.text) > 150 else r.text,
                "score": round(r.score, 3),
            }
            for r in results
        ]

        result = {
            "answer": answer,
            "sources": sources,
            "from_cache": False,
        }

        # Cache the result
        query_cache.put(query, result)

        return result
