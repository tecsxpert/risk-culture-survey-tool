import json
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.groq_client import groq_client
from services.cache_service import cache_service        
from routes.health import record_response_time         
from routes.health import record_cache_hit             
from routes.health import record_cache_miss             

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
        logger.error("categorise_prompt.txt not found in prompts/")
        raise

def parse_ai_response(content: str) -> dict:
    """
    Safely parse AI JSON response.
    Handles long reasoning, special characters, and markdown wrapping.
    """
    cleaned = content.strip()

    # Strip markdown code blocks if present
    if cleaned.startswith("```"):
        lines   = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()

    # Try direct JSON parse first
    try:
        parsed = json.loads(cleaned)

    except json.JSONDecodeError:
        # ── Fallback: extract fields manually using string search ─
        logger.warning("Direct JSON parse failed — trying manual extraction")

        # Extract category
        category = ""
        if '"category"' in cleaned:
            start    = cleaned.find('"category"') + len('"category"')
            start    = cleaned.find('"', start) + 1
            end      = cleaned.find('"', start)
            category = cleaned[start:end].strip()

        # Extract confidence
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

        # Extract reasoning — take first 100 words max
        reasoning = "Classified based on survey response content."
        if '"reasoning"' in cleaned:
            start = cleaned.find('"reasoning"') + len('"reasoning"')
            start = cleaned.find('"', start) + 1
            # Find closing quote — handle escaped quotes
            pos = start
            while pos < len(cleaned):
                if cleaned[pos] == '"' and cleaned[pos-1] != '\\':
                    break
                pos += 1
            reasoning = cleaned[start:pos].strip()
            # Truncate to 100 words
            words     = reasoning.split()
            if len(words) > 100:
                reasoning = " ".join(words[:100])

        parsed = {
            "category":   category,
            "confidence": confidence,
            "reasoning":  reasoning
        }

    # Validate required fields
    if not parsed.get("category"):
        raise ValueError("Missing or empty 'category' in AI response")
    if "confidence" not in parsed:
        raise ValueError("Missing 'confidence' in AI response")
    if "reasoning" not in parsed:
        raise ValueError("Missing 'reasoning' in AI response")

    # Validate confidence range
    confidence = float(parsed["confidence"])
    if not (0.0 <= confidence <= 1.0):
        confidence = 0.7  # safe default instead of crashing

    # Validate category 
    if parsed["category"] not in VALID_CATEGORIES:
        logger.warning(f"Unknown category returned: {parsed['category']}")

    # Truncate reasoning to 150 words max
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
            "error": "Field 'text' is required and cannot be empty",
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

    # 2. Check cache (skip if skip_cache=True) 
    cache_key    = cache_service.make_key("categorise", text)  
    cached_value = None                                         

    if not skip_cache:                                          
        cached_value = cache_service.get(cache_key)          
        if cached_value:                                      
            record_cache_hit()                                  
            logger.info("Returning cached categorise response") 
            cached_value["from_cache"] = True                  
            return jsonify(cached_value), 200                  

    record_cache_miss()                                         

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
        user_message=f"Classify this risk culture survey response:\n\n{text}",
        temperature=0.1,
        max_tokens=200
    )

    # Track response time in /health 
    record_response_time(ai_result["response_time_ms"])        

    # 5. Handle fallback 
    if ai_result["is_fallback"]:
        return jsonify({
            "category":     "Uncategorised",
            "confidence":   0.0,
            "reasoning":    "AI service temporarily unavailable.",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "is_fallback":  True,
            "from_cache":   False
        }), 200

    # 6. Parse response 
    try:
        parsed = parse_ai_response(ai_result["content"])
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.error(f"Failed to parse AI response: {e}")
        return jsonify({
            "error": "Failed to parse AI response.",
            "code":  "PARSE_ERROR"
        }), 500

    # 7. Build response and cache it
    result = {
        "category":     parsed["category"],
        "confidence":   parsed["confidence"],
        "reasoning":    parsed["reasoning"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "is_fallback":  False,
        "from_cache":   False                                
    }

    cache_service.set(cache_key, result)                       

    return jsonify(result), 200