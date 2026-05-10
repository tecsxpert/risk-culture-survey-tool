import os
import json
import time
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env from ai-service/.env 
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s"
)
logger = logging.getLogger("GroqClient")

# ── Constants ────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL        = "llama-3.3-70b-versatile"

MAX_RETRIES  = 3        # retry up to 3 times
BASE_DELAY   = 2        # seconds — doubles each retry (2, 4, 8)
TIMEOUT      = 30       # seconds per request


class GroqClient:
    """
    Handles all communication with the Groq API.
    Features:
      - 3 retries with exponential backoff
      - JSON parsing with validation
      - Full error logging
      - Fallback response on total failure
    """

    def __init__(self):
        if not GROQ_API_KEY:
            logger.error("GROQ_API_KEY is missing. Check your .env file.")
        else:
            logger.info(f"GroqClient initialized. Key loaded: {GROQ_API_KEY[:10]}...")
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

    # ── Main public method ───────────────────────────────────────────────────
    def chat(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.3,
        max_tokens: int = 1000
    ) -> dict:
        """
        Send a message to Groq and return a structured response dict.

        Returns:
            {
                "content":          str,   # AI reply text
                "model_used":       str,
                "tokens_used":      int,
                "response_time_ms": int,
                "is_fallback":      bool   # True if all retries failed
            }
        """
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message}
            ],
            "temperature": temperature,
            "max_tokens":  max_tokens
        }

        attempt    = 0
        last_error = None

        while attempt < MAX_RETRIES:
            attempt += 1
            delay = BASE_DELAY ** attempt  # 2, 4, 8 seconds
            logger.info(f"Groq API call — attempt {attempt}/{MAX_RETRIES}")

            start_time = time.time()

            try:
                response = requests.post(
                    GROQ_API_URL,
                    headers=self.headers,
                    json=payload,
                    timeout=TIMEOUT
                )
                response.raise_for_status()

                elapsed_ms = int((time.time() - start_time) * 1000)
                data       = response.json()

                # ── Parse response ───────────────────────────────────────
                content     = data["choices"][0]["message"]["content"].strip()
                tokens_used = data["usage"]["total_tokens"]
                model_used  = data["model"]

                logger.info(
                    f"Groq success — tokens: {tokens_used}, "
                    f"time: {elapsed_ms}ms"
                )

                return {
                    "content":          content,
                    "model_used":       model_used,
                    "tokens_used":      tokens_used,
                    "response_time_ms": elapsed_ms,
                    "is_fallback":      False
                }

            except requests.exceptions.Timeout:
                last_error = "Request timed out"
                logger.warning(
                    f"Attempt {attempt} timed out. "
                    f"Retrying in {delay}s..." if attempt < MAX_RETRIES
                    else "All retries exhausted."
                )

            except requests.exceptions.HTTPError as e:
                last_error = f"HTTP {e.response.status_code}: {e.response.text}"
                logger.error(f"Attempt {attempt} HTTP error — {last_error}")

                # 401 = bad key, no point retrying
                if e.response.status_code == 401:
                    logger.error("Invalid API key. Stopping retries.")
                    break

            except requests.exceptions.ConnectionError:
                last_error = "Connection error — no internet or Groq is down"
                logger.error(f"Attempt {attempt} connection error.")

            except (KeyError, json.JSONDecodeError) as e:
                last_error = f"Failed to parse Groq response: {e}"
                logger.error(f"Attempt {attempt} parse error — {last_error}")

            except Exception as e:
                last_error = str(e)
                logger.error(f"Attempt {attempt} unexpected error — {last_error}")

            # Wait before next retry (skip wait on last attempt)
            if attempt < MAX_RETRIES:
                logger.info(f"Waiting {delay}s before retry...")
                time.sleep(delay)

        # ── All retries failed — return fallback ─────────────────────────
        logger.error(f"All {MAX_RETRIES} attempts failed. Last error: {last_error}")
        return self._fallback_response(last_error)

    # ── Fallback ─────────────────────────────────────────────────────────────
    def _fallback_response(self, error: str) -> dict:
        """
        Returns a safe fallback when Groq is unavailable.
        is_fallback: True signals to the frontend to show a warning.
        """
        return {
            "content": (
                "The AI service is temporarily unavailable. "
                "Please try again in a few moments."
            ),
            "model_used":       MODEL,
            "tokens_used":      0,
            "response_time_ms": 0,
            "is_fallback":      True,
            "error":            error
        }


# ── Singleton instance ────────────────────────────────────────────────────────
# Import this in your routes: from services.groq_client import groq_client
groq_client = GroqClient()