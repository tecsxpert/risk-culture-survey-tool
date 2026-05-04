import json
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.groq_client import groq_client
from services.cache_service import cache_service
from services.fallback_service import fallback_service
from services.tracker import record_response_time

logger = logging.getLogger("categorise")
categorise_bp = Blueprint("categorise", __name__)

VALID_CATEGORIES = [
    "Leadership & Governance",
    "Risk Awareness",
    "Communication & Reporting",
    "Accountability",
    "Training & Competency",
    "Policies & Procedures",
    "Incident & Near Miss",
    "Culture & Behaviour"
]

def load_prompt() -> str:
    try:
        with open("prompts/categorise_prompt.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("categorise_prompt.txt not found")
        raise

def parse_ai_response(content: str) -> dict:
    """
    Safely parse AI JSON response.
    Handles long reasoning, special characters, markdown wrapping.
    """
    cleaned = content.strip()

    if cleaned.startswith("```"):
        lines   = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()

    try:
        parsed = json.loads(cleaned)

    except json.JSONDecodeError:
        logger.warning("Direct JSON parse failed — trying manual extraction")

        category = ""
        if '"category"' in cleaned:
            start    = cleaned.find('"category"') + len('"category"')
            start    = cleaned.find('"', start) + 1
            end      = cleaned.find('"', start)
            category = cleaned[start:end].strip()

        confidence = 0.7
        if '"confidence"' in cleaned:
            start = cleaned.find('"confidence"') + len('"confidence"')
            start = cleaned.find(':', start) + 1
            end   = cleaned.find(',', start)
            if end == -1:
                end = cleaned.find('}', start)
            try:
                confidence = float(cleaned[start:end].strip())
            except ValueError:
                confidence = 0.7

        reasoning = "Classified based on survey response content."
        if '"reasoning"' in cleaned:
            start = cleaned.find('"reasoning"') + len('"reasoning"')
            start = cleaned.find('"', start) + 1
            pos   = start
            while pos < len(cleaned):
                if cleaned[pos] == '"' and cleaned[pos-1] != '\\':
                    break
                pos += 1
            reasoning = cleaned[start:pos].strip()
            words     = reasoning.split()
            if len(words) > 100:
                reasoning = " ".join(words[:100])

        parsed = {
            "category":   category,
            "confidence": confidence,
            "reasoning":  reasoning
        }

    if not parsed.get("category"):
        raise ValueError("Missing or empty 'category'")
    if "confidence" not in parsed:
        raise ValueError("Missing 'confidence'")
    if "reasoning" not in parsed:
        raise ValueError("Missing 'reasoning'")

    confidence = float(parsed["confidence"])
    if not (0.0 <= confidence <= 1.0):
        confidence = 0.7

    if parsed["category"] not in VALID_CATEGORIES:
        logger.warning(f"Unknown category: {parsed['category']}")

    reasoning = parsed["reasoning"].strip()
    words     = reasoning.split()
    if len(words) > 150:
        reasoning = " ".join(words[:150])

    return {
        "category":   parsed["category"],
        "confidence": round(confidence, 2),
        "reasoning":  reasoning
    }

@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    # 1. Validate input 
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "Request body must be JSON",
            "code":  "INVALID_JSON"
        }), 400

    text       = data.get("text", "").strip()
    skip_cache = data.get("skip_cache", False)

    if not text:
        return jsonify({
            "error": "Field 'text' is required",
            "code":  "MISSING_TEXT"
        }), 400
    if len(text) < 10:
        return jsonify({
            "error": "Field 'text' must be at least 10 characters",
            "code":  "TEXT_TOO_SHORT"
        }), 400
    if len(text) > 5000:
        return jsonify({
            "error": "Field 'text' must not exceed 5000 characters",
            "code":  "TEXT_TOO_LONG"
        }), 400

    # 2. Check cache 
    cache_key = cache_service.make_key("categorise", text)

    if not skip_cache:
        cached = cache_service.get(cache_key)
        if cached:
            logger.info("Returning cached categorise response")
            cached["from_cache"]     = True
            cached["meta"]["cached"] = True
            return jsonify(cached), 200

    # 3. Load prompt 
    try:
        system_prompt = load_prompt()
    except FileNotFoundError:
        return jsonify({
            "error": "Prompt template not found.",
            "code":  "PROMPT_NOT_FOUND"
        }), 500

    logger.info(f"Categorising text of length {len(text)}")

    # 4. Call Groq 
    ai_result = groq_client.chat(
        system_prompt=system_prompt,
        user_message=(
            f"Classify this risk culture survey response:\n\n{text}"
        ),
        temperature=0.1,
        max_tokens=200
    )

    record_response_time(ai_result["response_time_ms"])

    # 5. Handle fallback 
    if ai_result["is_fallback"]:
        fallback = fallback_service.get_categorise_fallback(
            error=ai_result.get("error")
        )
        return jsonify(fallback), 200

    # 6. Parse response 
    try:
        parsed = parse_ai_response(ai_result["content"])
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.error(f"Failed to parse AI response: {e}")
        fallback = fallback_service.get_categorise_fallback(
            error=f"Parse error: {e}"
        )
        return jsonify(fallback), 200

    # 7. Build result with meta 
    result = {
        "category":     parsed["category"],
        "confidence":   parsed["confidence"],
        "reasoning":    parsed["reasoning"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "from_cache":   False,
        "meta": {
            "confidence":       parsed["confidence"],
            "model_used":       ai_result["model_used"],
            "tokens_used":      ai_result["tokens_used"],
            "response_time_ms": ai_result["response_time_ms"],
            "cached":           False,
            "is_fallback":      False
        }
    }

    cache_service.set(cache_key, result)
    return jsonify(result), 200