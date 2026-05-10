import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:5000"

TEXT = (
    "Our CEO never mentions risk management in any team meetings. "
    "Leadership treats risk as a compliance checkbox with no real "
    "value to the business."
)

QUESTION = (
    "How does leadership behaviour affect risk culture "
    "in an organisation?"
)

SURVEY = (
    "47 respondents. Risk culture score 2.3 out of 5. "
    "Poor leadership engagement. Low risk awareness. "
    "Staff afraid to report incidents. Training last "
    "updated 2019. Zero risk action items completed on time."
)

def pretty(data):
    print(json.dumps(data, indent=2))
    print()

def section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

# ── Run based on argument ─────────────────────────────────────
arg = sys.argv[1] if len(sys.argv) > 1 else "health"

if arg == "health":
    section("ENDPOINT 1 — GET /health")
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    pretty(r.json())

elif arg == "categorise":
    section("ENDPOINT 2 — POST /categorise (fresh Groq call)")
    r = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": TEXT, "skip_cache": True},
        timeout=30
    )
    pretty(r.json())

elif arg == "cache":
    section("ENDPOINT 2 — POST /categorise (cache hit)")
    r = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": TEXT, "skip_cache": False},
        timeout=30
    )
    data = r.json()
    pretty(data)
    print(f"from_cache   : {data.get('from_cache')}")
    print(f"meta.cached  : {data.get('meta', {}).get('cached')}")

elif arg == "query":
    section("ENDPOINT 3 — POST /query (RAG Pipeline)")
    r = requests.post(
        f"{BASE_URL}/query",
        json={"question": QUESTION, "skip_cache": True},
        timeout=40
    )
    pretty(r.json())

elif arg == "report":
    section("ENDPOINT 4 — POST /generate-report (Async)")
    r = requests.post(
        f"{BASE_URL}/generate-report",
        json={"survey_data": SURVEY},
        timeout=10
    )
    data = r.json()
    pretty(data)

    job_id = data.get("job_id")
    print(f"Polling job: {job_id[:8]}...")

    for i in range(20):
        time.sleep(3)
        poll = requests.get(
            f"{BASE_URL}/generate-report/{job_id}",
            timeout=10
        )
        status = poll.json().get("status")
        print(f"[{(i+1)*3}s] Status: {status}")
        if status == "complete":
            pretty(poll.json())
            break

elif arg == "fallback":
    section("FALLBACK SERVICE DEMO")
    sys.path.append(".")
    from services.fallback_service import fallback_service
    result = fallback_service.get_categorise_fallback(
        "HTTP 429 rate limit exceeded"
    )
    pretty(result)

elif arg == "jobs":
    section("ENDPOINT 6 — GET /generate-report/jobs")
    r = requests.get(
        f"{BASE_URL}/generate-report/jobs",
        timeout=10
    )
    pretty(r.json())

else:
    print("Usage: python demo_video.py [health|categorise|cache|query|report|fallback|jobs]")