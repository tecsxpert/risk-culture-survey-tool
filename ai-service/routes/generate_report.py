import json
import logging
import threading
import requests as http_requests
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.groq_client import groq_client
from services.cache_service import cache_service
from services.job_store import job_store
from services.tracker import record_response_time

logger = logging.getLogger("generate_report")

generate_report_bp = Blueprint("generate_report", __name__)

# Load prompt 
def load_prompt() -> str:
    try:
        with open(
            "prompts/generate_report_prompt.txt", "r", encoding="utf-8"
        ) as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("generate_report_prompt.txt not found")
        raise

# Parse report response 
def parse_report(content: str) -> dict:
    """Safely parse the AI report JSON response."""
    cleaned = content.strip()
    if cleaned.startswith("```"):
        lines   = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()

    parsed = json.loads(cleaned)

    # Validate required fields
    required = [
        "title", "executive_summary",
        "overview", "top_items", "recommendations"
    ]
    for field in required:
        if field not in parsed:
            raise ValueError(f"Missing field: {field}")

    # Validate top_items
    if not isinstance(parsed["top_items"], list) or \
       len(parsed["top_items"]) == 0:
        raise ValueError("top_items must be a non-empty list")

    # Validate recommendations
    if not isinstance(parsed["recommendations"], list) or \
       len(parsed["recommendations"]) == 0:
        raise ValueError("recommendations must be a non-empty list")

    return parsed

# Send webhook notification 
def send_webhook(webhook_url: str, job_id: str, status: str):
    """
    POST to webhook URL when job completes or fails.
    Fails silently — webhook errors never crash the app.
    """
    if not webhook_url:
        return

    try:
        job = job_store.get_job(job_id)
        http_requests.post(
            webhook_url,
            json={
                "job_id":  job_id,
                "status":  status,
                "result":  job.get("result"),
                "error":   job.get("error")
            },
            timeout=10
        )
        logger.info(f"Webhook sent to {webhook_url} for job {job_id}")
    except Exception as e:
        logger.warning(f"Webhook failed for job {job_id}: {e}")

# Background processing function
def process_report_job(job_id: str, survey_data: str, webhook_url: str):
    """
    Runs in a background thread.
    1. Mark job as processing
    2. Call Groq to generate report
    3. Parse response
    4. Mark job complete or failed
    5. Send webhook if configured
    """
    job_store.set_processing(job_id)
    logger.info(f"Processing report job: {job_id}")

    try:
        # Load prompt
        system_prompt = load_prompt()

        # Call Groq
        ai_result = groq_client.chat(
            system_prompt=system_prompt,
            user_message=(
                f"Generate a risk culture report based on the "
                f"following survey data:\n\n{survey_data}"
            ),
            temperature=0.4,
            max_tokens=1500
        )

        record_response_time(ai_result["response_time_ms"])

        if ai_result["is_fallback"]:
            job_store.set_failed(
                job_id,
                "AI service temporarily unavailable"
            )
            send_webhook(webhook_url, job_id, "failed")
            return

        # Parse report
        parsed_report = parse_report(ai_result["content"])

        # Build complete result
        result = {
            "report":       parsed_report,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "meta": {
                "confidence":       0.9,
                "model_used":       ai_result["model_used"],
                "tokens_used":      ai_result["tokens_used"],
                "response_time_ms": ai_result["response_time_ms"],
                "cached":           False,
                "is_fallback":      False
            }
        }

        job_store.set_complete(job_id, result)
        send_webhook(webhook_url, job_id, "complete")
        logger.info(f"Report job complete: {job_id}")

    except (json.JSONDecodeError, ValueError) as e:
        error_msg = f"Failed to parse AI report: {e}"
        logger.error(f"Job {job_id} parse error: {e}")
        job_store.set_failed(job_id, error_msg)
        send_webhook(webhook_url, job_id, "failed")

    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        logger.error(f"Job {job_id} unexpected error: {e}")
        job_store.set_failed(job_id, error_msg)
        send_webhook(webhook_url, job_id, "failed")

# ===============================================================
# ROUTES
# ===============================================================
@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    """
    POST /generate-report
    Body: {
        "survey_data": "text of survey responses",
        "webhook_url": "https://..." (optional)
    }

    Returns job_id IMMEDIATELY — does not wait for AI.

    Response:
    {
        "job_id":      str,
        "status":      "pending",
        "message":     str,
        "poll_url":    str,
        "created_at":  str
    }
    """

    # 1. Validate input 
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "Request body must be JSON",
            "code":  "INVALID_JSON"
        }), 400

    survey_data = data.get("survey_data", "").strip()
    webhook_url = data.get("webhook_url", None)

    if not survey_data:
        return jsonify({
            "error": "Field 'survey_data' is required",
            "code":  "MISSING_SURVEY_DATA"
        }), 400

    if len(survey_data) < 20:
        return jsonify({
            "error": "Field 'survey_data' must be at least 20 characters",
            "code":  "SURVEY_DATA_TOO_SHORT"
        }), 400

    if len(survey_data) > 10000:
        return jsonify({
            "error": "Field 'survey_data' must not exceed 10000 characters",
            "code":  "SURVEY_DATA_TOO_LONG"
        }), 400

    # 2. Create job
    job_id = job_store.create_job(webhook_url=webhook_url)

    # 3. Start background thread
    thread = threading.Thread(
        target=process_report_job,
        args=(job_id, survey_data, webhook_url),
        daemon=True
    )
    thread.start()

    logger.info(f"Report job started in background: {job_id}")

    # 4. Return job_id immediately
    return jsonify({
        "job_id":     job_id,
        "status":     "pending",
        "message":    (
            "Report generation started. "
            "Poll the status URL to check progress."
        ),
        "poll_url":   f"/generate-report/{job_id}",
        "created_at": job_store.get_job(job_id)["created_at"]
    }), 202

@generate_report_bp.route(
    "/generate-report/<job_id>", methods=["GET"]
)
def get_report_status(job_id: str):
    """
    GET /generate-report/<job_id>
    Poll this to check job status and get result when complete.

    Response when pending/processing:
    {
        "job_id":  str,
        "status":  "pending" | "processing",
        "message": str
    }

    Response when complete:
    {
        "job_id":       str,
        "status":       "complete",
        "created_at":   str,
        "completed_at": str,
        "result": {
            "report": {
                "title":             str,
                "executive_summary": str,
                "overview":          str,
                "top_items":         list,
                "recommendations":   list
            },
            "generated_at": str,
            "meta":         dict
        }
    }
    """
    job = job_store.get_job(job_id)

    if not job:
        return jsonify({
            "error": f"Job '{job_id}' not found",
            "code":  "JOB_NOT_FOUND"
        }), 404

    # 1. Still running
    if job["status"] in ["pending", "processing"]:
        return jsonify({
            "job_id":     job_id,
            "status":     job["status"],
            "created_at": job["created_at"],
            "message":    "Report is being generated. Check back shortly."
        }), 202

    # 2. Failed
    if job["status"] == "failed":
        return jsonify({
            "job_id":       job_id,
            "status":       "failed",
            "created_at":   job["created_at"],
            "completed_at": job["completed_at"],
            "error":        job["error"]
        }), 500

    # 3. Complete
    return jsonify({
        "job_id":       job_id,
        "status":       "complete",
        "created_at":   job["created_at"],
        "completed_at": job["completed_at"],
        "result":       job["result"]
    }), 200

@generate_report_bp.route("/generate-report/jobs", methods=["GET"])
def list_jobs():
    """
    GET /generate-report/jobs
    Returns all jobs with their status counts.
    Useful for monitoring and demo.
    """
    jobs  = job_store.list_jobs()
    stats = job_store.count()

    return jsonify({
        "stats": stats,
        "jobs":  [
            {
                "job_id":       j["id"],
                "status":       j["status"],
                "created_at":   j["created_at"],
                "completed_at": j["completed_at"],
                "has_result":   j["result"] is not None,
                "has_error":    j["error"] is not None
            }
            for j in jobs
        ]
    }), 200