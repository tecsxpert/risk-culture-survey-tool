import os
import json
import hashlib
import logging
import redis
from pathlib import Path
from dotenv import load_dotenv

# Load env 
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

logger = logging.getLogger("CacheService")

# Constants
REDIS_HOST  = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT  = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB    = int(os.getenv("REDIS_DB", 0))
CACHE_TTL   = 15 * 60  # 15 minutes in seconds
CACHE_PREFIX = "ai_cache:"

class CacheService:
    """
    Redis-based cache for AI responses.

    Features:
      - SHA256 cache key generated from endpoint + input text
      - 15 minute TTL on all cached responses
      - Hit/miss counters for /health endpoint
      - skip_cache flag for fresh requests
      - Graceful fallback if Redis is unavailable
    """

    def __init__(self):
        self.hits   = 0
        self.misses = 0
        self.redis  = None
        self._connect()

    def _connect(self):
        """Connect to Redis. Fails gracefully if Redis is unavailable."""
        try:
            self.redis = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=3,
                socket_timeout=3
            )
            # Test connection
            self.redis.ping()
            logger.info(
                f"Redis connected — {REDIS_HOST}:{REDIS_PORT} db={REDIS_DB}"
            )
        except redis.exceptions.ConnectionError:
            logger.warning(
                "Redis not available — caching disabled. "
                "Start Redis or set REDIS_HOST in .env"
            )
            self.redis = None
        except Exception as e:
            logger.warning(f"Redis connection failed: {e} — caching disabled")
            self.redis = None

    # Cache key generation
    def make_key(self, endpoint: str, text: str) -> str:
        """
        Generate a SHA256 cache key from endpoint name + input text.

        Example:
            endpoint = "categorise"
            text     = "Our CEO never mentions risk..."
            key      = "ai_cache:categorise:a3f9b2c1..."
        """
        raw       = f"{endpoint}:{text.strip().lower()}"
        sha256    = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        cache_key = f"{CACHE_PREFIX}{endpoint}:{sha256}"
        logger.debug(f"Cache key generated: {cache_key[:50]}...")
        return cache_key

    # Get from cache
    def get(self, key: str) -> dict | None:
        """
        Retrieve cached response.
        Returns dict if cache hit, None if miss or Redis unavailable.
        """
        if not self.redis:
            return None

        try:
            cached = self.redis.get(key)
            if cached:
                self.hits += 1
                logger.info(f"Cache HIT — key: {key[:50]}...")
                return json.loads(cached)
            else:
                self.misses += 1
                logger.info(f"Cache MISS — key: {key[:50]}...")
                return None

        except redis.exceptions.RedisError as e:
            logger.warning(f"Redis GET error: {e}")
            return None

    # Set in cache
    def set(self, key: str, value: dict) -> bool:
        """
        Store response in cache with 15 min TTL.
        Returns True if stored, False if Redis unavailable.
        """
        if not self.redis:
            return False

        try:
            serialized = json.dumps(value)
            self.redis.setex(
                name=key,
                time=CACHE_TTL,
                value=serialized
            )
            logger.info(
                f"Cache SET — key: {key[:50]}... TTL: {CACHE_TTL}s"
            )
            return True

        except redis.exceptions.RedisError as e:
            logger.warning(f"Redis SET error: {e}")
            return False

    # Delete from cache
    def delete(self, key: str) -> bool:
        """Delete a specific key from cache."""
        if not self.redis:
            return False
        try:
            self.redis.delete(key)
            logger.info(f"Cache DELETE — key: {key[:50]}...")
            return True
        except redis.exceptions.RedisError as e:
            logger.warning(f"Redis DELETE error: {e}")
            return False

    # Stats for /health 
    def get_stats(self) -> dict:
        """
        Return cache statistics for the /health endpoint.
        """
        total    = self.hits + self.misses
        hit_rate = round((self.hits / total) * 100, 1) if total > 0 else 0.0

        return {
            "hits":         self.hits,
            "misses":       self.misses,
            "total":        total,
            "hit_rate_pct": hit_rate,
            "redis_connected": self.redis is not None,
            "ttl_seconds":  CACHE_TTL
        }

    # Redis available check 
    @property
    def is_available(self) -> bool:
        """True if Redis is connected and ready."""
        return self.redis is not None

# Singleton instance 
cache_service = CacheService()