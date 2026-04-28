import re
from flask import request, jsonify

# ✅ Pre-compile patterns (better performance)
BLOCKED_PATTERNS = [
    re.compile(r"ignore previous instructions", re.IGNORECASE),
    re.compile(r"system prompt", re.IGNORECASE),
    re.compile(r"reveal .* (data|info)", re.IGNORECASE),
    re.compile(r"bypass security", re.IGNORECASE),
    re.compile(r"act as .*", re.IGNORECASE),
    re.compile(r"<script.*?>.*?</script>", re.IGNORECASE)
]

def sanitize_input(text: str) -> str:
    """Remove HTML tags and trim spaces"""
    if not isinstance(text, str):
        return text

    # Remove HTML tags
    cleaned = re.sub(r"<.*?>", "", text)

    return cleaned.strip()

def is_malicious(text: str) -> bool:
    """Detect prompt injection or malicious patterns"""
    if not isinstance(text, str):
        return False

    return any(pattern.search(text) for pattern in BLOCKED_PATTERNS)

def validate_request():
    data = request.get_json(silent=True)

    # ❌ Invalid JSON
    if not data or not isinstance(data, dict):
        return jsonify({
            "error": "Invalid input",
            "message": "JSON object expected"
        }), 400

    # ✅ Validate each field safely
    for key, value in data.items():

        if isinstance(value, str):
            cleaned = sanitize_input(value)

            # ❌ Malicious content detected
            if is_malicious(cleaned):
                return jsonify({
                    "error": "Malicious input detected",
                    "field": key
                }), 400

            # ❌ Optional: length protection (extra safety)
            if len(cleaned) > 1000:
                return jsonify({
                    "error": "Input too long",
                    "field": key
                }), 400

            # ✅ Replace with cleaned value
            data[key] = cleaned

    return None