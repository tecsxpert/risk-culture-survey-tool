import time
import logging
from collections import deque
from datetime import datetime, timezone
from flask import Blueprint, jsonify
from services.chroma_client import chroma_client

logger = logging.getLogger("health")

health_bp = Blueprint("health", __name__)

# Service start time (for uptime calculation) 
SERVICE_START_TIME = time.time()

# Response time tracker (last 10 calls) 
response_times = deque(maxlen=10)

# Helper functions 

def record_response_time(ms: int):
    """
    Called by other routes after every Groq API call.
    Keeps track of last 10 response times.
    """
    response_times.append(ms)

def record_cache_hit():
    """Call this when a cached response is returned."""
    pass  # tracking now handled by cache_service

def record_cache_miss():
    """Call this when a fresh Groq call is made."""
    pass  # tracking now handled by cache_service

def get_avg_response_time() -> float:
    """Calculate average of last 10 response times."""
    if not response_times:
        return 0.0
    return round(sum(response_times) / len(response_times), 2)

def get_uptime() -> dict:
    """Calculate how long the service has been running."""
    elapsed_seconds = int(time.time() - SERVICE_START_TIME)

    hours   = elapsed_seconds // 3600
    minutes = (elapsed_seconds % 3600) // 60
    seconds = elapsed_seconds % 60

    return {
        "seconds": elapsed_seconds,
        "human":   f"{hours}h {minutes}m {seconds}s"
    }

def check_chroma_status() -> dict:
    """Check ChromaDB connection and document count."""
    try:
        doc_count = chroma_client.count()
        return {
            "status":    "connected",
            "doc_count": doc_count
        }
    except Exception as e:
        logger.error(f"ChromaDB health check failed: {e}")
        return {
            "status":    "disconnected",
            "doc_count": 0,
            "error":     str(e)
        }

def check_groq_status() -> dict:
    """Check if Groq API key is configured."""
    from services.groq_client import GROQ_API_KEY, MODEL
    return {
        "model":      MODEL,
        "key_loaded": bool(GROQ_API_KEY)
    }

# Health endpoint

@health_bp.route("/health", methods=["GET"])
def health():
    """
    GET /health
    No authentication required.

    Returns:
    {
        "status":    "healthy" | "degraded",
        "timestamp": str (ISO),
        "uptime":    { seconds: int, human: str },
        "groq": {
            "model":                  str,
            "key_loaded":             bool,
            "avg_response_time_ms":   float,
            "response_times_tracked": int
        },
        "chromadb": {
            "status":    "connected" | "disconnected",
            "doc_count": int
        },
        "cache": {
            "hits":            int,
            "misses":          int,
            "total":           int,
            "hit_rate_pct":    float,
            "redis_connected": bool,
            "ttl_seconds":     int
        }
    }
    """

    # Import cache_service here to avoid circular imports
    from services.cache_service import cache_service

    # Gather all health data 
    groq_info        = check_groq_status()
    chroma_info      = check_chroma_status()
    uptime_info      = get_uptime()
    avg_rt           = get_avg_response_time()
    cache_stats_data = cache_service.get_stats()

    # Determine overall status 
    is_healthy = (
        groq_info["key_loaded"] and
        chroma_info["status"] == "connected"
    )
    overall_status = "healthy" if is_healthy else "degraded"

    # Build response
    response = {
        "status":    overall_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime":    uptime_info,
        "groq": {
            "model":                   groq_info["model"],
            "key_loaded":              groq_info["key_loaded"],
            "avg_response_time_ms":    avg_rt,
            "response_times_tracked":  len(response_times)
        },
        "chromadb": {
            "status":    chroma_info["status"],
            "doc_count": chroma_info["doc_count"]
        },
        "cache": cache_stats_data
    }

    http_status = 200 if is_healthy else 503
    return jsonify(response), http_status