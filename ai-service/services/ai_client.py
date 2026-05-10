import json

def categorize_text(text):
    """
    Mock AI categorization function.
    This simulates an AI response and is safe (no PII storage or logging).
    """

    # ✅ Ensure input is string (extra safety)
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # ✅ Trim input (no unnecessary data handling)
    clean_text = text.strip()

    # ✅ Mock response (structured)
    mock_response = {
        "category": "High Risk",
        "confidence": 0.85,
        "reasoning": "Mock response for development"
    }

    # ✅ Return JSON string (to match your existing flow)
    return json.dumps(mock_response)