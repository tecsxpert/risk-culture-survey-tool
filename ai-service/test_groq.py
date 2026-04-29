import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

def test_groq_connection():
    print("Testing Groq API connection...")
    print(f"Model: {MODEL}")
    print(f".env path: {env_path} ({'found' if env_path.exists() else 'NOT FOUND'})")
    print(f"API Key loaded: {GROQ_API_KEY[:10]}..." if GROQ_API_KEY else "API Key: NOT FOUND")
    print("-" * 50)

    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not found in environment.")
        return False

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant for a Risk Culture Survey Tool."
            },
            {
                "role": "user",
                "content": (
                    "In one sentence, describe what a Risk Culture Survey Tool does "
                    "in an organisation."
                )
            }
        ],
        "temperature": 0.3,
        "max_tokens": 100
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        reply = data["choices"][0]["message"]["content"].strip()
        tokens_used = data["usage"]["total_tokens"]
        model_used = data["model"]

        print("SUCCESS! Groq API is working.")
        print(f"Model used   : {model_used}")
        print(f"Tokens used  : {tokens_used}")
        print(f"Response     : {reply}")
        return True

    except requests.exceptions.Timeout:
        print("ERROR: Request timed out.")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP {e.response.status_code} — {e.response.text}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error — {e}")
        return False


if __name__ == "__main__":
    success = test_groq_connection()
    print("-" * 50)
    print("Day 1 status:", "COMPLETE ✓" if success else "FAILED — fix errors above")