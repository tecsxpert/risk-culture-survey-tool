import logging
from datetime import datetime, timezone

logger = logging.getLogger("FallbackService")

class FallbackService:
    """
    Manages pre-written fallback responses for all AI endpoints.

    Used when:
      - Groq API is unavailable
      - Rate limit exceeded (429)
      - Request timeout
      - Any other Groq error

    Every fallback response includes:
      - is_fallback: True in meta
      - generated_at timestamp
      - Human-readable message explaining the situation
    """

    # Fallback templates 
    CATEGORISE_FALLBACK = {
        "category":   "Uncategorised",
        "confidence": 0.0,
        "reasoning":  (
            "The AI classification service is temporarily unavailable. "
            "This response has been automatically categorised as "
            "Uncategorised. Please try again in a few moments or "
            "manually review and categorise this survey response."
        ),
        "from_cache": False,
    }

    QUERY_FALLBACK = {
        "answer": (
            "The AI assistant is temporarily unavailable due to high "
            "demand or a service interruption. Your question has been "
            "received but cannot be answered at this time. Please try "
            "again in a few moments. If the issue persists, contact "
            "your system administrator."
        ),
        "sources":     [],
        "chunks_used": 0,
        "from_cache":  False,
    }

    GENERATE_REPORT_FALLBACK = {
        "report": {
            "title": "Risk Culture Assessment Report — Service Unavailable",
            "executive_summary": (
                "The AI report generation service is temporarily "
                "unavailable. This is a placeholder report. Please "
                "retry report generation when the service is restored."
            ),
            "overview": (
                "Due to a temporary service interruption, the AI-powered "
                "risk culture analysis could not be completed at this time. "
                "The survey data has been received and stored. Once the "
                "service is restored, a full analysis will be available. "
                "We apologise for any inconvenience caused."
            ),
            "top_items": [
                {
                    "rank":        1,
                    "title":       "Service Temporarily Unavailable",
                    "description": (
                        "The AI analysis service is currently experiencing "
                        "high demand. Please retry in a few minutes."
                    )
                }
            ],
            "recommendations": [
                {
                    "title":       "Retry Report Generation",
                    "description": (
                        "Please attempt to regenerate this report in "
                        "5-10 minutes when the AI service has recovered."
                    ),
                    "priority": "High"
                }
            ]
        }
    }

    # Public methods 
    def get_categorise_fallback(self, error: str = None) -> dict:
        """
        Return fallback response for /categorise endpoint.
        Always includes is_fallback: True in meta.
        """
        logger.warning(
            f"Returning categorise fallback. "
            f"Error: {error or 'unknown'}"
        )
        response = dict(self.CATEGORISE_FALLBACK)
        response["generated_at"] = datetime.now(timezone.utc).isoformat()
        response["meta"]          = self._build_meta(error)
        return response

    def get_query_fallback(self, error: str = None) -> dict:
        """
        Return fallback response for /query endpoint.
        Always includes is_fallback: True in meta.
        """
        logger.warning(
            f"Returning query fallback. "
            f"Error: {error or 'unknown'}"
        )
        response = dict(self.QUERY_FALLBACK)
        response["generated_at"] = datetime.now(timezone.utc).isoformat()
        response["meta"]          = self._build_meta(error)
        return response

    def get_generate_report_fallback(self, error: str = None) -> dict:
        """
        Return fallback response for /generate-report endpoint.
        Always includes is_fallback: True in meta.
        """
        logger.warning(
            f"Returning generate-report fallback. "
            f"Error: {error or 'unknown'}"
        )
        response = {
            "report":       self.GENERATE_REPORT_FALLBACK["report"],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "meta":         self._build_meta(error)
        }
        return response

    # Private helpers 
    def _build_meta(self, error: str = None) -> dict:
        """
        Build standard meta object for fallback responses.
        is_fallback is always True here.
        """
        return {
            "confidence":       0.0,
            "model_used":       "fallback",
            "tokens_used":      0,
            "response_time_ms": 0,
            "cached":           False,
            "is_fallback":      True,
            "error":            error or "AI service temporarily unavailable"
        }

    def is_rate_limit_error(self, error: str) -> bool:
        """Check if error is a Groq rate limit (429)."""
        error_lower = str(error).lower()
        return "429" in error_lower or "rate_limit" in error_lower

    def is_timeout_error(self, error: str) -> bool:
        """Check if error is a timeout."""
        error_lower = str(error).lower()
        return "timeout" in error_lower or "timed out" in error_lower

    def get_retry_message(self, error: str) -> str:
        """
        Return human-readable retry message based on error type.
        Shown to users in the frontend.
        """
        if self.is_rate_limit_error(error):
            return (
                "The AI service has reached its request limit. "
                "Please try again in a few minutes."
            )
        if self.is_timeout_error(error):
            return (
                "The AI service took too long to respond. "
                "Please try again."
            )
        return (
            "The AI service is temporarily unavailable. "
            "Please try again in a few moments."
        )

# Singleton instance 
fallback_service = FallbackService()