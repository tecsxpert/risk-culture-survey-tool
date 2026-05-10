import time
import json
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

# Demo data — exactly what will be used on Demo Day 
DEMO_CATEGORISE_TEXT = (
    "Our senior management never discusses risk in team meetings. "
    "There is no visible leadership commitment to managing risks "
    "properly and staff feel risk management is just a compliance "
    "checkbox exercise with no real value."
)

DEMO_QUERY_QUESTION = (
    "How does leadership behaviour affect risk culture "
    "in an organisation?"
)

DEMO_SURVEY_DATA = """
Risk Culture Survey Results — Demo Organisation — May 2026

Total respondents: 47 employees across 5 departments

Key findings:
1. Leadership: 78% of staff say senior management never
   discusses risk in team meetings or town halls
2. Risk Awareness: Average score 2.1 out of 5.0
   Staff cannot identify top operational risks
3. Incident Reporting: 3 near misses went unreported
   last quarter due to fear of blame and retaliation
4. Training: Risk training last updated in 2019
   Completion rate only 42% across all departments
5. Accountability: 0% of risk action items completed
   on time in the last 6 months

Overall risk culture score: 2.3 out of 5.0
Survey completion rate: 78%
Industry benchmark: 3.4 out of 5.0
Gap to benchmark: 1.1 points below average
"""

DEMO_ANALYSE_TEXT = (
    "The organisation has shown a pattern of declining risk "
    "culture scores over the past three years. Leadership "
    "engagement with risk management has dropped significantly. "
    "Near miss reporting rates are at an all time low. "
    "Staff surveys indicate fear of blame as the primary barrier "
    "to speaking up about risk concerns."
)

DEMO_RECOMMEND_TEXT = (
    "Survey score: 2.3/5. Key issues: poor leadership engagement, "
    "low risk awareness, fear of blame culture, outdated training, "
    "no accountability for risk action items."
)

def print_header(title: str):
    print(f"\n{'═' * 65}")
    print(f"  {title}")
    print(f"{'═' * 65}")

def print_result(endpoint: str, status: int, time_ms: int,
                 is_fallback: bool, preview: str):
    fallback_str = " [FALLBACK]" if is_fallback else ""
    print(f"\n  Endpoint     : {endpoint}{fallback_str}")
    print(f"  Status       : {status}")
    print(f"  Response time: {time_ms}ms")
    print(f"  Preview      : {preview[:100]}...")

# Check system ready 
def check_system():
    print("=" * 65)
    print("DAY 17 — AI DRY RUN")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    try:
        r    = requests.get(f"{BASE_URL}/health", timeout=10)
        data = r.json()
        print(f"\n[System Check]")
        print(f"  Status   : {data.get('status')}")
        print(
            f"  ChromaDB : "
            f"{data.get('chromadb', {}).get('doc_count')} docs"
        )
        print(
            f"  Redis    : "
            f"{data.get('cache', {}).get('redis_connected')}"
        )
        print(
            f"  Groq key : "
            f"{data.get('groq', {}).get('key_loaded')}"
        )

        if data.get("status") != "healthy":
            print("\n[ERROR] System not healthy — fix before Demo Day!")
            return False

        if data.get("chromadb", {}).get("doc_count", 0) < 30:
            print(
                "\n[ERROR] ChromaDB has less than 30 docs. "
                "Run: python prompt_tuning/seed_30_records.py"
            )
            return False

        print("\n[OK] System healthy — starting dry run...\n")
        return True

    except Exception as e:
        print(f"\n[ERROR] Cannot reach Flask: {e}")
        return False

# Endpoint 1: GET /health 
def run_health():
    print_header("ENDPOINT 1 — GET /health")
    times = []

    for i in range(3):
        start   = time.perf_counter()
        r       = requests.get(f"{BASE_URL}/health", timeout=10)
        elapsed = round((time.perf_counter() - start) * 1000)
        times.append(elapsed)
        print(f"  Run {i+1}: {elapsed}ms — HTTP {r.status_code}")

    data = r.json()
    avg  = round(sum(times) / len(times))

    print(f"\n  Avg response time : {avg}ms")
    print(f"  Status            : {data.get('status')}")
    print(f"  Model             : {data.get('groq', {}).get('model')}")
    print(f"  ChromaDB docs     : {data.get('chromadb', {}).get('doc_count')}")
    print(f"  Redis connected   : {data.get('cache', {}).get('redis_connected')}")
    print(f"  Cache hit rate    : {data.get('cache', {}).get('hit_rate_pct')}%")
    print(f"  Uptime            : {data.get('uptime', {}).get('human')}")

    return {
        "endpoint":    "GET /health",
        "avg_ms":      avg,
        "min_ms":      min(times),
        "max_ms":      max(times),
        "is_fallback": False,
        "status":      "PASS" if avg < 200 else "SLOW"
    }

# Endpoint 2: POST /categorise 
def run_categorise():
    print_header("ENDPOINT 2 — POST /categorise")
    print(f"  Input: {DEMO_CATEGORISE_TEXT[:80]}...")
    print("\n  [Making fresh Groq call — skip_cache=True]")

    start   = time.perf_counter()
    r       = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": DEMO_CATEGORISE_TEXT, "skip_cache": True},
        timeout=30
    )
    elapsed = round((time.perf_counter() - start) * 1000)
    data    = r.json()

    print(f"\n  Category     : {data.get('category')}")
    print(f"  Confidence   : {data.get('confidence')}")
    print(f"  Reasoning    : {data.get('reasoning', '')[:80]}...")
    print(f"  Response time: {elapsed}ms")
    print(f"  is_fallback  : {data.get('meta', {}).get('is_fallback')}")
    print(f"  tokens_used  : {data.get('meta', {}).get('tokens_used')}")

    # Second call — cache hit
    print("\n  [Second call — should be cache hit]")
    start2   = time.perf_counter()
    r2       = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": DEMO_CATEGORISE_TEXT, "skip_cache": False},
        timeout=30
    )
    elapsed2 = round((time.perf_counter() - start2) * 1000)
    data2    = r2.json()
    print(f"  from_cache   : {data2.get('from_cache')}")
    print(f"  Response time: {elapsed2}ms (cache hit)")

    return {
        "endpoint":    "POST /categorise",
        "avg_ms":      elapsed,
        "cache_ms":    elapsed2,
        "min_ms":      min(elapsed, elapsed2),
        "max_ms":      max(elapsed, elapsed2),
        "is_fallback": data.get("meta", {}).get("is_fallback", False),
        "category":    data.get("category"),
        "confidence":  data.get("confidence"),
        "status":      "PASS" if not data.get("meta", {}).get("is_fallback") else "FALLBACK"
    }

# Endpoint 3: POST /query 
def run_query():
    print_header("ENDPOINT 3 — POST /query (RAG Pipeline)")
    print(f"  Question: {DEMO_QUERY_QUESTION}")
    print("\n  [Making fresh Groq call — skip_cache=True]")

    start   = time.perf_counter()
    r       = requests.post(
        f"{BASE_URL}/query",
        json={"question": DEMO_QUERY_QUESTION, "skip_cache": True},
        timeout=40
    )
    elapsed = round((time.perf_counter() - start) * 1000)
    data    = r.json()

    print(f"\n  Answer       : {data.get('answer', '')[:100]}...")
    print(f"  Chunks used  : {data.get('chunks_used')}")
    print(f"  Sources      :")
    for s in data.get("sources", []):
        print(
            f"    - [{s.get('category')}] "
            f"score={s.get('score')} "
            f"{s.get('preview', '')[:50]}..."
        )
    print(f"  Response time: {elapsed}ms")
    print(f"  is_fallback  : {data.get('meta', {}).get('is_fallback')}")
    print(f"  tokens_used  : {data.get('meta', {}).get('tokens_used')}")

    # Cache hit
    print("\n  [Second call — cache hit]")
    start2   = time.perf_counter()
    r2       = requests.post(
        f"{BASE_URL}/query",
        json={"question": DEMO_QUERY_QUESTION, "skip_cache": False},
        timeout=40
    )
    elapsed2 = round((time.perf_counter() - start2) * 1000)
    data2    = r2.json()
    print(f"  from_cache   : {data2.get('from_cache')}")
    print(f"  Response time: {elapsed2}ms (cache hit)")

    return {
        "endpoint":    "POST /query",
        "avg_ms":      elapsed,
        "cache_ms":    elapsed2,
        "min_ms":      min(elapsed, elapsed2),
        "max_ms":      max(elapsed, elapsed2),
        "is_fallback": data.get("meta", {}).get("is_fallback", False),
        "chunks_used": data.get("chunks_used"),
        "status":      "PASS" if not data.get("meta", {}).get("is_fallback") else "FALLBACK"
    }

# Endpoint 4: POST /generate-report 
def run_generate_report():
    print_header("ENDPOINT 4 — POST /generate-report (Async)")
    print("  [Submitting report generation job...]")

    start   = time.perf_counter()
    r       = requests.post(
        f"{BASE_URL}/generate-report",
        json={"survey_data": DEMO_SURVEY_DATA},
        timeout=10
    )
    elapsed = round((time.perf_counter() - start) * 1000)
    data    = r.json()

    job_id = data.get("job_id")
    print(f"\n  job_id       : {job_id[:8] if job_id else 'None'}...")
    print(f"  status       : {data.get('status')}")
    print(f"  Response time: {elapsed}ms (async — instant!)")
    print(f"  poll_url     : {data.get('poll_url')}")

    # Poll for completion
    print(f"\n  [Polling for completion...]")
    poll_start   = time.perf_counter()
    final_status = None
    final_data   = None

    for attempt in range(25):
        time.sleep(3)
        poll   = requests.get(
            f"{BASE_URL}/generate-report/{job_id}",
            timeout=10
        )
        status = poll.json().get("status")
        print(f"  [{(attempt+1)*3}s] Status: {status}")

        if status in ["complete", "failed"]:
            final_status = status
            final_data   = poll.json()
            break

    total_time = round((time.perf_counter() - poll_start) * 1000)

    if final_status == "complete":
        result = final_data.get("result", {})
        report = result.get("report", {})
        print(f"\n  Title        : {report.get('title', '')[:60]}")
        print(
            f"  Exec summary : "
            f"{report.get('executive_summary', '')[:80]}..."
        )
        print(f"  Top items    : {len(report.get('top_items', []))}")
        print(f"  Recs         : {len(report.get('recommendations', []))}")
        print(f"  is_fallback  : {result.get('meta', {}).get('is_fallback')}")
        print(f"  Total time   : {total_time}ms")
    else:
        print(f"\n  Job failed or timed out: {final_status}")

    return {
        "endpoint":      "POST /generate-report",
        "submit_ms":     elapsed,
        "total_ms":      total_time,
        "avg_ms":        elapsed,
        "min_ms":        elapsed,
        "max_ms":        elapsed,
        "is_fallback":   (
            final_data.get("result", {}).get("meta", {}).get("is_fallback", False)
            if final_data else True
        ),
        "final_status":  final_status,
        "status":        "PASS" if final_status == "complete" else "FALLBACK"
    }

# Endpoint 5: GET /generate-report/<job_id> 
def run_poll():
    print_header("ENDPOINT 5 — GET /generate-report/<job_id> (Poll)")

    # Create a job first
    r      = requests.post(
        f"{BASE_URL}/generate-report",
        json={"survey_data": DEMO_SURVEY_DATA},
        timeout=10
    )
    job_id = r.json().get("job_id")
    print(f"  Job created: {job_id[:8]}...")
    print("  Waiting for job to complete...")

    for _ in range(25):
        time.sleep(3)
        poll   = requests.get(
            f"{BASE_URL}/generate-report/{job_id}",
            timeout=10
        )
        status = poll.json().get("status")
        if status in ["complete", "failed"]:
            break

    # Now benchmark polling
    print(f"\n  [Benchmarking poll on completed job]")
    times = []
    for i in range(3):
        start   = time.perf_counter()
        r       = requests.get(
            f"{BASE_URL}/generate-report/{job_id}",
            timeout=10
        )
        elapsed = round((time.perf_counter() - start) * 1000)
        times.append(elapsed)
        print(f"  Run {i+1}: {elapsed}ms — HTTP {r.status_code}")

    avg = round(sum(times) / len(times))
    print(f"\n  Avg response time: {avg}ms")
    print(f"  Job status       : {status}")

    return {
        "endpoint":    "GET /generate-report/<job_id>",
        "avg_ms":      avg,
        "min_ms":      min(times),
        "max_ms":      max(times),
        "is_fallback": False,
        "status":      "PASS" if avg < 500 else "SLOW"
    }

# Endpoint 6: GET /generate-report/jobs 
def run_jobs_list():
    print_header("ENDPOINT 6 — GET /generate-report/jobs")

    start   = time.perf_counter()
    r       = requests.get(
        f"{BASE_URL}/generate-report/jobs",
        timeout=10
    )
    elapsed = round((time.perf_counter() - start) * 1000)
    data    = r.json()

    stats = data.get("stats", {})
    jobs  = data.get("jobs", [])

    print(f"\n  Response time : {elapsed}ms")
    print(f"  Total jobs    : {stats.get('total')}")
    print(f"  Complete      : {stats.get('complete')}")
    print(f"  Failed        : {stats.get('failed')}")
    print(f"  Processing    : {stats.get('processing')}")
    print(f"  Jobs returned : {len(jobs)}")

    return {
        "endpoint":    "GET /generate-report/jobs",
        "avg_ms":      elapsed,
        "min_ms":      elapsed,
        "max_ms":      elapsed,
        "is_fallback": False,
        "total_jobs":  stats.get("total", 0),
        "status":      "PASS" if elapsed < 500 else "SLOW"
    }

# Print final summary 
def print_summary(results: list):
    print("\n" + "=" * 65)
    print("DRY RUN SUMMARY — ALL 6 ENDPOINTS")
    print("=" * 65)
    print(
        f"{'Endpoint':<35} {'Avg ms':>8} "
        f"{'Fallback':>10} {'Status':>8}"
    )
    print("─" * 65)

    all_pass = True
    for r in results:
        fallback = "YES ⚠" if r.get("is_fallback") else "No"
        status   = r.get("status", "UNKNOWN")
        if status not in ["PASS"]:
            all_pass = False

        print(
            f"{r['endpoint']:<35} "
            f"{str(r.get('avg_ms', 'N/A')) + 'ms':>8} "
            f"{fallback:>10} "
            f"{status:>8}"
        )

    print("─" * 65)
    print(
        f"\n  Day 17 status: "
        f"{'COMPLETE ✓ — Ready for Demo Day!' if all_pass else 'ISSUES FOUND ✗'}"
    )
    print("=" * 65)
    return results

# Main 
if __name__ == "__main__":
    if not check_system():
        print("\nFix system issues then re-run.")
        exit(1)

    results = []

    results.append(run_health())
    time.sleep(2)

    results.append(run_categorise())
    time.sleep(3)

    results.append(run_query())
    time.sleep(3)

    results.append(run_generate_report())
    time.sleep(3)

    results.append(run_poll())
    time.sleep(2)

    results.append(run_jobs_list())

    print_summary(results)

    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output    = {
        "timestamp": timestamp,
        "results":   results
    }
    with open(f"dry_run_output_{timestamp}.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved to: dry_run_output_{timestamp}.json")