import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.groq_client import groq_client
from services.chroma_client import chroma_client
from services.cache_service import cache_service
from services.fallback_service import fallback_service
from services.tracker import record_response_time

logger   = logging.getLogger("query")
query_bp = Blueprint("query", __name__)
TOP_K    = 3

def load_prompt() -> str:
    try:
        with open("prompts/query_prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("query_prompt.txt not found")
        raise

def build_context(chunks):
    if not chunks:
        return "No relevant documents found."
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[Document {i}]\n{chunk['text']}\n"
            f"(Source: {chunk['metadata'].get('source', 'knowledge base')}, "
            f"Category: {chunk['metadata'].get('category', 'General')})"
        )
    return "\n\n".join(parts)

def format_sources(chunks):
    return [{
        "id":       c["id"],
        "category": c["metadata"].get("category", "General"),
        "source":   c["metadata"].get("source", "knowledge base"),
        "score":    c["score"],
        "preview":  c["text"][:150] + "..."
                    if len(c["text"]) > 150 else c["text"]
    } for c in chunks]

@query_bp.route("/query", methods=["POST"])
def query():
    # 1. Validate input 
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "Request body must be JSON",
            "code":  "INVALID_JSON"
        }), 400

    question   = data.get("question", "").strip()
    skip_cache = data.get("skip_cache", False)

    if not question:
        return jsonify({
            "error": "Field 'question' is required",
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

    # 2. Check cache 
    cache_key = cache_service.make_key("query", question)

    if not skip_cache:
        cached = cache_service.get(cache_key)
        if cached:
            logger.info("Returning cached query response")
            cached["from_cache"]     = True
            cached["meta"]["cached"] = True
            return jsonify(cached), 200

    # 3. Retrieve chunks from ChromaDB 
    try:
        chunks = chroma_client.query(question, n_results=TOP_K)
    except Exception as e:
        logger.error(f"ChromaDB query failed: {e}")
        fallback = fallback_service.get_query_fallback(
            error=f"ChromaDB error: {e}"
        )
        return jsonify(fallback), 200

    # 4. Build context and load prompt 
    context = build_context(chunks)
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

    record_response_time(ai_result["response_time_ms"])

    # 6. Handle fallback 
    if ai_result["is_fallback"]:
        fallback = fallback_service.get_query_fallback(
            error=ai_result.get("error")
        )
        return jsonify(fallback), 200

    # 7. Build result with meta 
    result = {
        "answer":       ai_result["content"],
        "sources":      format_sources(chunks),
        "chunks_used":  len(chunks),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "from_cache":   False,
        "meta": {
            "confidence":       1.0,
            "model_used":       ai_result["model_used"],
            "tokens_used":      ai_result["tokens_used"],
            "response_time_ms": ai_result["response_time_ms"],
            "cached":           False,
            "is_fallback":      False
        }
    }

    cache_service.set(cache_key, result)
    return jsonify(result), 200