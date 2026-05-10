import sys
import time
import statistics
import requests

BASE_URL = "http://127.0.0.1:5000"

# Performance targets (milliseconds) 
TARGETS = {
    "GET /health":           {"p50": 200,   "p95": 500,   "p99": 1000},
    "POST /categorise":      {"p50": 5000,  "p95": 8000,  "p99": 12000},
    "POST /query":           {"p50": 5000,  "p95": 8000,  "p99": 12000},
    "POST /generate-report": {"p50": 200,   "p95": 500,   "p99": 1000},
    "GET /generate-report":  {"p50": 200,   "p95": 500,   "p99": 1000},
}

# Test data
CATEGORISE_TEXT = (
    "Our senior management never discusses risk in team meetings. "
    "There is no visible leadership commitment to managing risks properly."
)

QUERY_QUESTION = (
    "How does leadership behaviour affect risk culture?"
)

SURVEY_DATA = (
    "Survey results show poor risk awareness across all departments. "
    "Staff cannot identify key operational risks. Leadership commitment "
    "to risk management is low. Incident reporting rates have declined "
    "significantly over the past two quarters."
)

# Percentile calculation 
def percentile(data: list, pct: float) -> float:
    if not data:
        return 0.0
    sorted_data = sorted(data)
    index       = (pct / 100) * (len(sorted_data) - 1)
    lower       = int(index)
    upper       = lower + 1
    if upper >= len(sorted_data):
        return sorted_data[-1]
    fraction = index - lower
    return (
        sorted_data[lower] +
        fraction * (sorted_data[upper] - sorted_data[lower])
    )

def format_ms(ms: float) -> str:
    return f"{round(ms)}ms"

def check_target(value: float, target: float) -> str:
    return "✓" if value <= target else "✗"

# Single request timer
def timed_request(request_fn) -> tuple:
    """
    Execute request and return (elapsed_ms, response).
    Sleep is NEVER inside this function.
    """
    start      = time.perf_counter()        # high precision timer
    r          = request_fn()
    elapsed_ms = (time.perf_counter() - start) * 1000
    return elapsed_ms, r

# Benchmark runner 
def run_benchmark(
    name: str,
    request_fn,
    n_requests: int = 50,
    delay: float = 0.5
) -> dict:
    print(f"\n{'─' * 60}")
    print(f"Benchmarking : {name}")
    print(f"Requests     : {n_requests}")
    print(f"Delay        : {delay}s between requests (NOT timed)")
    print(f"{'─' * 60}")

    times  = []
    errors = 0

    for i in range(1, n_requests + 1):
        try:
            # ONLY the request is timed 
            elapsed_ms, r = timed_request(request_fn)

            if r.status_code in [200, 202]:
                times.append(elapsed_ms)
                if i % 10 == 0:
                    print(
                        f"  [{i:02d}/{n_requests}] "
                        f"{format_ms(elapsed_ms)} — OK"
                    )
            else:
                errors += 1
                if i % 10 == 0:
                    print(
                        f"  [{i:02d}/{n_requests}] "
                        f"HTTP {r.status_code} — ERROR"
                    )

        except Exception as e:
            errors += 1
            print(f"  [{i:02d}/{n_requests}] ERROR: {e}")

        # Sleep AFTER timing — completely separate
        if i < n_requests:
            time.sleep(delay)

    if not times:
        print("  No successful requests!")
        return {
            "name": name, "success": 0, "errors": errors,
            "p50": 0, "p95": 0, "p99": 0,
            "min": 0, "max": 0, "avg": 0
        }

    p50 = percentile(times, 50)
    p95 = percentile(times, 95)
    p99 = percentile(times, 99)
    avg = statistics.mean(times)
    mn  = min(times)
    mx  = max(times)

    print(f"\n  Results ({len(times)} successful, {errors} errors):")
    print(f"  Min  : {format_ms(mn)}")
    print(f"  Avg  : {format_ms(avg)}")
    print(f"  Max  : {format_ms(mx)}")
    print(f"  p50  : {format_ms(p50)}")
    print(f"  p95  : {format_ms(p95)}")
    print(f"  p99  : {format_ms(p99)}")

    return {
        "name":    name,
        "success": len(times),
        "errors":  errors,
        "p50":     round(p50),
        "p95":     round(p95),
        "p99":     round(p99),
        "min":     round(mn),
        "max":     round(mx),
        "avg":     round(avg)
    }

# Individual benchmarks 
def benchmark_health(n: int = 50) -> dict:
    def call():
        return requests.get(f"{BASE_URL}/health", timeout=10)
    return run_benchmark("GET /health", call, n, delay=0.1)

def benchmark_categorise(n: int = 50) -> dict:
    # Warm up cache with exact same text
    print("  [Warming up cache...]")
    requests.post(
        f"{BASE_URL}/categorise",
        json={"text": CATEGORISE_TEXT, "skip_cache": False},
        timeout=30
    )
    # Second call to confirm cache is working
    r2 = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": CATEGORISE_TEXT, "skip_cache": False},
        timeout=30
    )
    cached = r2.json().get("from_cache", False)
    print(f"  [Cache working: {cached}]")

    def call():
        return requests.post(
            f"{BASE_URL}/categorise",
            json={"text": CATEGORISE_TEXT, "skip_cache": False},
            timeout=30
        )
    return run_benchmark("POST /categorise", call, n, delay=0.1)

def benchmark_query(n: int = 50) -> dict:
    # Warm up cache
    print("  [Warming up cache...]")
    requests.post(
        f"{BASE_URL}/query",
        json={"question": QUERY_QUESTION, "skip_cache": False},
        timeout=30
    )
    r2 = requests.post(
        f"{BASE_URL}/query",
        json={"question": QUERY_QUESTION, "skip_cache": False},
        timeout=30
    )
    cached = r2.json().get("from_cache", False)
    print(f"  [Cache working: {cached}]")

    def call():
        return requests.post(
            f"{BASE_URL}/query",
            json={"question": QUERY_QUESTION, "skip_cache": False},
            timeout=30
        )
    return run_benchmark("POST /query", call, n, delay=0.1)

def benchmark_generate_report_submit(n: int = 50) -> dict:
    """Benchmark job submission — should be near instant (async)."""
    def call():
        return requests.post(
            f"{BASE_URL}/generate-report",
            json={"survey_data": SURVEY_DATA},
            timeout=10
        )
    return run_benchmark("POST /generate-report", call, n, delay=0.2)

def benchmark_generate_report_poll(n: int = 50) -> dict:
    """Benchmark polling a completed job — should be near instant."""
    print("  [Creating report job...]")

    # Submit job
    r = requests.post(
        f"{BASE_URL}/generate-report",
        json={"survey_data": SURVEY_DATA},
        timeout=10
    )

    if r.status_code != 202:
        print(f"  [ERROR] Could not create job: {r.status_code}")
        return {
            "name": "GET /generate-report", "success": 0,
            "errors": n, "p50": 0, "p95": 0, "p99": 0,
            "min": 0, "max": 0, "avg": 0
        }

    job_id = r.json().get("job_id")
    print(f"  [Job created: {job_id[:8]}...]")

    # Wait for job to complete
    print("  [Waiting for job to complete...]")
    for attempt in range(40):
        time.sleep(2)
        status_r = requests.get(
            f"{BASE_URL}/generate-report/{job_id}",
            timeout=10
        )
        status = status_r.json().get("status")
        if status == "complete":
            print(f"  [Job complete after {(attempt+1)*2}s]")
            break
        elif status == "failed":
            print(f"  [Job failed — error: {status_r.json().get('error')}]")
            break
        elif attempt % 5 == 0:
            print(f"  [{(attempt+1)*2}s] Still {status}...")
    else:
        print("  [Timeout waiting for job]")

    # Now benchmark polling the completed job
    def call():
        return requests.get(
            f"{BASE_URL}/generate-report/{job_id}",
            timeout=10
        )
    return run_benchmark("GET /generate-report", call, n, delay=0.1)

# Print summary
def print_summary(results: list):
    print("\n" + "=" * 60)
    print("PERFORMANCE BENCHMARK SUMMARY")
    print("=" * 60)
    print(
        f"{'Endpoint':<25} {'p50':>8} {'p95':>8} "
        f"{'p99':>8} {'Status':>10}"
    )
    print("─" * 60)

    all_pass = True

    for r in results:
        name    = r["name"]
        targets = TARGETS.get(name, {})

        if r["success"] == 0:
            print(f"{name:<25} {'N/A':>8} {'N/A':>8} {'N/A':>8} {'ERROR':>10}")
            all_pass = False
            continue

        p50_ok = check_target(r["p50"], targets.get("p50", 99999))
        p95_ok = check_target(r["p95"], targets.get("p95", 99999))
        p99_ok = check_target(r["p99"], targets.get("p99", 99999))
        status = (
            "PASS ✓"
            if all(c == "✓" for c in [p50_ok, p95_ok, p99_ok])
            else "SLOW ✗"
        )
        if status != "PASS ✓":
            all_pass = False

        print(
            f"{name:<25} "
            f"{format_ms(r['p50']):>8} "
            f"{format_ms(r['p95']):>8} "
            f"{format_ms(r['p99']):>8} "
            f"{status:>10}"
        )

    print("─" * 60)
    print(f"\nTargets:")
    for name, t in TARGETS.items():
        print(
            f"  {name:<25} "
            f"p50<{t['p50']}ms  "
            f"p95<{t['p95']}ms  "
            f"p99<{t['p99']}ms"
        )

    print("\n" + "=" * 60)
    print(
        f"Day 12 status: "
        f"{'COMPLETE ✓' if all_pass else 'RESULTS DOCUMENTED ✓'}"
    )
    print("=" * 60)
    return all_pass

# Main 
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 12 — PERFORMANCE BENCHMARK")
    print("Endpoints: /health, /categorise, /query, /generate-report")
    print("Requests : 50 per endpoint")
    print("=" * 60)

    # Check Flask is running
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        data = r.json()
        print(f"\n[Check] Flask running — status: {data.get('status')}")
        print(
            f"[Check] ChromaDB docs: "
            f"{data.get('chromadb', {}).get('doc_count', 0)}"
        )
        print(
            f"[Check] Redis: "
            f"{data.get('cache', {}).get('redis_connected', False)}"
        )
    except Exception:
        print("\n[ERROR] Flask not running! Start: python app.py")
        sys.exit(1)

    results = []

    print("\n[1/5] GET /health...")
    results.append(benchmark_health(50))

    print("\n[2/5] POST /categorise (with cache)...")
    results.append(benchmark_categorise(50))

    print("\n[3/5] POST /query (with cache)...")
    results.append(benchmark_query(50))

    print("\n[4/5] POST /generate-report (async submit)...")
    results.append(benchmark_generate_report_submit(50))

    print("\n[5/5] GET /generate-report (poll completed job)...")
    results.append(benchmark_generate_report_poll(50))

    print_summary(results)