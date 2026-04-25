from flask import Blueprint, request, jsonify
from datetime import datetime

from services.ai_client import categorize_text
import json
import re

categorise_bp = Blueprint('categorise', __name__)

@categorise_bp.route('/categorise', methods=['POST'])
def categorise():
    data = request.get_json(silent=True)

    # ❌ No JSON provided
    if not data:
        return jsonify({
            "error": "Invalid input",
            "message": "Request body must be JSON"
        }), 400

    text = data.get("text", "")

    # ❌ Not a string
    if not isinstance(text, str):
        return jsonify({
            "error": "Invalid input",
            "message": "Text must be a string"
        }), 400

    text = text.strip()

    # ❌ Empty input
    if not text:
        return jsonify({
            "error": "Invalid input",
            "message": "Text cannot be empty"
        }), 400

    # ❌ Too short
    if len(text) < 5:
        return jsonify({
            "error": "Invalid input",
            "message": "Text is too short"
        }), 400

    # ❌ Too long
    if len(text) > 500:
        return jsonify({
            "error": "Invalid input",
            "message": "Text is too long"
        }), 400

    # ✅ CALL AI
    try:
        ai_response = categorize_text(text)

        print("AI RESPONSE RECEIVED:", ai_response)  # 👈 debug

        # 🔥 Extract JSON safely
        json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)

        if json_match:
            result = json.loads(json_match.group())
        else:
            raise ValueError("Invalid AI response format")

        return jsonify({
            **result,
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": False
        })

    except Exception as e:
        print("ERROR:", str(e))  # 👈 debug

        return jsonify({
            "category": "unknown",
            "confidence": 0.5,
            "reasoning": "Fallback due to AI error",
            "generated_at": datetime.utcnow().isoformat(),
            "is_fallback": True
        }), 200