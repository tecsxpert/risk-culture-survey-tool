import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.groq_client import groq_client
from services.chroma_client import chroma_client

logger = logging.getLogger("query")

query_bp = Blueprint("query", __name__)

# How many ChromaDB chunks to retrieve
TOP_K = 3


def load_prompt() -> str:
    """Load the query prompt template from file."""
    try:
        with open("prompts/query_prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("query_prompt.txt not found in prompts/")
        raise


def build_context(chunks: list[dict]) -> str:
    """
    Format retrieved ChromaDB chunks into a single context string
    that gets injected into the prompt.
    """
    if not chunks:
        return "No relevant documents found."

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Document {i}]\n"
            f"{chunk['text']}\n"
            f"(Source: {chunk['metadata'].get('source', 'knowledge base')}, "
            f"Category: {chunk['metadata'].get('category', 'General')})"
        )

    return "\n\n".join(context_parts)


def format_sources(chunks: list[dict]) -> list[dict]:
    """Format ChromaDB chunks into a clean sources list for the response."""
    sources = []
    for chunk in chunks:
        sources.append({
            "id":         chunk["id"],
            "category":   chunk["metadata"].get("category", "General"),
            "source":     chunk["metadata"].get("source", "knowledge base"),
            "score":      chunk["score"],
            "preview":    chunk["text"][:150] + "..."
                          if len(chunk["text"]) > 150
                          else chunk["text"]
        })
    return sources


@query_bp.route("/query", methods=["POST"])
def query():
    """
    POST /query
    Body: { "question": "your question here" }

    RAG Pipeline:
      1. Validate input
      2. Embed the question
      3. Retrieve top-3 similar chunks from ChromaDB
      4. Inject chunks as context into prompt
      5. Call Groq with context + question
      6. Return answer + sources

    Returns:
    {
        "answer":       str,
        "sources":      list of { id, category, source, score, preview },
        "chunks_used":  int,
        "generated_at": str (ISO timestamp),
        "meta": {
            "model_used":       str,
            "tokens_used":      int,
            "response_time_ms": int,
            "is_fallback":      bool
        }
    }
    """

    #1. Validate request
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must be JSON",
            "code":  "INVALID_JSON"
        }), 400

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Field 'question' is required and cannot be empty",
            "code":  "MISSING_QUESTION"
        }), 400

    if len(question) < 10:
        return jsonify({
            "error": "Field 'question' must be at least 10 characters",
            "code":  "QUESTION_TOO_SHORT"
        }), 400

    if len(question) > 2000:
        return jsonify({
            "error": "Field 'question' must not exceed 2000 characters",
            "code":  "QUESTION_TOO_LONG"
        }), 400

    logger.info(f"RAG query received: {question[:80]}...")

    #2. Retrieve top-K chunks from ChromaDB 
    try:
        chunks = chroma_client.query(question, n_results=TOP_K)
        logger.info(f"Retrieved {len(chunks)} chunks from ChromaDB")
    except Exception as e:
        logger.error(f"ChromaDB query failed: {e}")
        return jsonify({
            "error": "Failed to retrieve documents from knowledge base.",
            "code":  "CHROMA_ERROR"
        }), 500

    # 3. Build context from chunks
    context = build_context(chunks)

    # 4. Load prompt and inject context
    try:
        prompt_template = load_prompt()
    except FileNotFoundError:
        return jsonify({
            "error": "Prompt template not found.",
            "code":  "PROMPT_NOT_FOUND"
        }), 500

    system_prompt = prompt_template.replace("{context}", context)

    # 5. Call Groq
    ai_result = groq_client.chat(
        system_prompt=system_prompt,
        user_message=f"Question: {question}",
        temperature=0.3,
        max_tokens=500
    )

    # 6. Handle fallback
    if ai_result["is_fallback"]:
        logger.error("Groq unavailable — returning fallback for /query")
        return jsonify({
            "answer":       "The AI service is temporarily unavailable. Please try again.",
            "sources":      format_sources(chunks),
            "chunks_used":  len(chunks),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "meta": {
                "model_used":       "unavailable",
                "tokens_used":      0,
                "response_time_ms": 0,
                "is_fallback":      True
            }
        }), 200

    # 7. Return full response
    return jsonify({
        "answer":       ai_result["content"],
        "sources":      format_sources(chunks),
        "chunks_used":  len(chunks),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "meta": {
            "model_used":       ai_result["model_used"],
            "tokens_used":      ai_result["tokens_used"],
            "response_time_ms": ai_result["response_time_ms"],
            "is_fallback":      False
        }
    }), 200