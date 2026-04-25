import re
from flask import request, jsonify

# Patterns for prompt injection / malicious intent
BLOCKED_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"reveal .* (data|info)",
    r"bypass security",
    r"act as .*",
    r"<script.*?>.*?</script>"
]

def sanitize_input(text: str) -> str:
    """Remove HTML tags and trim spaces"""
    text = re.sub(r"<.*?>", "", text)
    return text.strip()

def is_malicious(text: str) -> bool:
    """Detect prompt injection or malicious patterns"""
    text = text.lower()
    return any(re.search(pattern, text) for pattern in BLOCKED_PATTERNS)

def validate_request():
    data = request.get_json(silent=True)

    # ✅ FIX 1: Ensure data is valid JSON object
    if not data or not isinstance(data, dict):
        return jsonify({
            "error": "Invalid input",
            "message": "JSON object expected"
        }), 400

    # ✅ FIX 2: Safe iteration
    for key, value in data.items():

        if isinstance(value, str):
            cleaned = sanitize_input(value)

            # ✅ Detect malicious input
            if is_malicious(cleaned):
                return jsonify({
                    "error": "Malicious input detected",
                    "field": key
                }), 400

            # ✅ Replace with cleaned value
            data[key] = cleaned

    return None