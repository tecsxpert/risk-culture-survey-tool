import uuid
import logging
from datetime import datetime, timezone
from threading import Lock

logger = logging.getLogger("JobStore")

# Job status constants
STATUS_PENDING    = "pending"
STATUS_PROCESSING = "processing"
STATUS_COMPLETE   = "complete"
STATUS_FAILED     = "failed"
class JobStore:
    """
    Thread-safe in-memory store for async job tracking.

    Each job has:
        id          : unique UUID
        status      : pending → processing → complete/failed
        created_at  : ISO timestamp
        completed_at: ISO timestamp (when done)
        result      : the generated report (when complete)
        error       : error message (when failed)
        webhook_url : optional URL to call when complete
    """

    def __init__(self):
        self._jobs = {}
        self._lock = Lock()
        logger.info("JobStore initialised")

    def create_job(self, webhook_url: str = None) -> str:
        """
        Create a new job and return its ID.
        Status starts as 'pending'.
        """
        job_id = str(uuid.uuid4())

        with self._lock:
            self._jobs[job_id] = {
                "id":           job_id,
                "status":       STATUS_PENDING,
                "created_at":   datetime.now(timezone.utc).isoformat(),
                "completed_at": None,
                "result":       None,
                "error":        None,
                "webhook_url":  webhook_url
            }

        logger.info(f"Job created: {job_id}")
        return job_id

    def get_job(self, job_id: str) -> dict | None:
        """Get a job by ID. Returns None if not found."""
        with self._lock:
            return self._jobs.get(job_id)

    def set_processing(self, job_id: str):
        """Mark job as processing."""
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = STATUS_PROCESSING
                logger.info(f"Job processing: {job_id}")

    def set_complete(self, job_id: str, result: dict):
        """Mark job as complete with result."""
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"]       = STATUS_COMPLETE
                self._jobs[job_id]["result"]        = result
                self._jobs[job_id]["completed_at"]  = (
                    datetime.now(timezone.utc).isoformat()
                )
                logger.info(f"Job complete: {job_id}")

    def set_failed(self, job_id: str, error: str):
        """Mark job as failed with error message."""
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"]       = STATUS_FAILED
                self._jobs[job_id]["error"]         = error
                self._jobs[job_id]["completed_at"]  = (
                    datetime.now(timezone.utc).isoformat()
                )
                logger.error(f"Job failed: {job_id} — {error}")

    def list_jobs(self) -> list:
        """Return all jobs sorted by created_at descending."""
        with self._lock:
            jobs = list(self._jobs.values())
        return sorted(
            jobs,
            key=lambda j: j["created_at"],
            reverse=True
        )

    def count(self) -> dict:
        """Return counts by status."""
        with self._lock:
            jobs = list(self._jobs.values())

        return {
            "total":      len(jobs),
            "pending":    sum(1 for j in jobs if j["status"] == STATUS_PENDING),
            "processing": sum(1 for j in jobs if j["status"] == STATUS_PROCESSING),
            "complete":   sum(1 for j in jobs if j["status"] == STATUS_COMPLETE),
            "failed":     sum(1 for j in jobs if j["status"] == STATUS_FAILED)
        }

# Singleton instance
job_store = JobStore()