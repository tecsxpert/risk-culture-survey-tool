import time
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test data 
CATEGORISE_TEXT = (
    "Our senior management never discusses risk in team meetings. "
    "There is no visible leadership commitment to managing risks."
)

QUERY_QUESTION = (
    "How does leadership behaviour affect risk culture?"
)

SURVEY_DATA = (
    "Survey results: 47 respondents. Poor risk awareness across "
    "all departments. Staff cannot identify key operational risks. "
    "Leadership commitment to risk management is very low. "
    "Incident reporting rates have declined significantly."
)

def print_section(title: str):
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}")

def print_result(test: str, passed: bool, detail: str = ""):
    status = "PASS ✓" if passed else "FAIL ✗"
    print(f"  [{status}] {test}")
    if detail:
        print(f"           {detail}")

# ===============================================================
# VERIFY 1 — System Health
# ===============================================================
def verify_health() -> bool:
    print_section("1. SYSTEM HEALTH CHECK")
    all_pass = True

    try:
        r    = requests.get(f"{BASE_URL}/health", timeout=10)
        data = r.json()

        # Overall status
        ok = data.get("status") == "healthy"
        print_result("Flask status is healthy", ok,
                     f"status={data.get('status')}")
        if not ok:
            all_pass = False

        # ChromaDB
        doc_count = data.get("chromadb", {}).get("doc_count", 0)
        ok = doc_count >= 30
        print_result(
            "ChromaDB has 30+ demo records", ok,
            f"doc_count={doc_count}"
        )
        if not ok:
            all_pass = False

        # Redis
        redis_ok = data.get("cache", {}).get("redis_connected", False)
        print_result("Redis is connected", redis_ok,
                     f"redis_connected={redis_ok}")
        if not redis_ok:
            all_pass = False

        # Groq key
        key_ok = data.get("groq", {}).get("key_loaded", False)
        print_result("Groq API key loaded", key_ok,
                     f"key_loaded={key_ok}")
        if not key_ok:
            all_pass = False

        # Response time
        start = time.perf_counter()
        requests.get(f"{BASE_URL}/health", timeout=10)
        elapsed = round((time.perf_counter() - start) * 1000)
        ok = elapsed < 200
        print_result(
            "Health endpoint < 200ms", ok,
            f"response_time={elapsed}ms"
        )
        if not ok:
            all_pass = False

    except Exception as e:
        print(f"  [FAIL ✗] Cannot reach Flask: {e}")
        return False

    return all_pass

# ===============================================================
# VERIFY 2 — Redis Cache Working
# ===============================================================
def verify_cache() -> bool:
    print_section("2. REDIS CACHE VERIFICATION")
    all_pass = True

    # Categorise cache 
    print("\n  Testing /categorise cache:")

    # First call — should be cache miss
    r1 = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": CATEGORISE_TEXT, "skip_cache": True},
        timeout=30
    )
    data1 = r1.json()

    ok = data1.get("from_cache") == False
    print_result(
        "First call is cache MISS", ok,
        f"from_cache={data1.get('from_cache')}"
    )
    if not ok:
        all_pass = False

    # Second call — should be cache hit
    r2 = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": CATEGORISE_TEXT, "skip_cache": False},
        timeout=30
    )
    data2 = r2.json()

    ok = data2.get("from_cache") == True
    print_result(
        "Second call is cache HIT", ok,
        f"from_cache={data2.get('from_cache')}"
    )
    if not ok:
        all_pass = False

    # Cache hit should be fast
    start = time.perf_counter()
    requests.post(
        f"{BASE_URL}/categorise",
        json={"text": CATEGORISE_TEXT, "skip_cache": False},
        timeout=30
    )
    elapsed = round((time.perf_counter() - start) * 1000)
    ok = elapsed < 200
    print_result(
        "Cache hit response < 200ms", ok,
        f"response_time={elapsed}ms"
    )
    if not ok:
        all_pass = False

    # meta.cached should be True on cache hit
    ok = data2.get("meta", {}).get("cached") == True
    print_result(
        "meta.cached = True on cache hit", ok,
        f"meta.cached={data2.get('meta', {}).get('cached')}"
    )
    if not ok:
        all_pass = False

    # Query cache 
    print("\n  Testing /query cache:")

    r3 = requests.post(
        f"{BASE_URL}/query",
        json={"question": QUERY_QUESTION, "skip_cache": True},
        timeout=40
    )
    data3 = r3.json()

    ok = data3.get("from_cache") == False
    print_result(
        "First call is cache MISS", ok,
        f"from_cache={data3.get('from_cache')}"
    )
    if not ok:
        all_pass = False

    r4 = requests.post(
        f"{BASE_URL}/query",
        json={"question": QUERY_QUESTION, "skip_cache": False},
        timeout=40
    )
    data4 = r4.json()

    ok = data4.get("from_cache") == True
    print_result(
        "Second call is cache HIT", ok,
        f"from_cache={data4.get('from_cache')}"
    )
    if not ok:
        all_pass = False

    # Health cache stats 
    print("\n  Checking /health cache stats:")
    r5   = requests.get(f"{BASE_URL}/health", timeout=10)
    data5 = r5.json()
    cache = data5.get("cache", {})

    ok = cache.get("total", 0) > 0
    print_result(
        "Cache stats being tracked", ok,
        f"hits={cache.get('hits')} misses={cache.get('misses')} "
        f"total={cache.get('total')} "
        f"hit_rate={cache.get('hit_rate_pct')}%"
    )
    if not ok:
        all_pass = False

    return all_pass

# ===============================================================
# VERIFY 3 — Performance Targets
# ===============================================================
def verify_performance() -> bool:
    print_section("3. PERFORMANCE TARGETS")
    all_pass = True

    print("\n  Note: Testing with cache hits for realistic production times")

    # Warm up caches
    requests.post(f"{BASE_URL}/categorise",
                  json={"text": CATEGORISE_TEXT}, timeout=30)
    requests.post(f"{BASE_URL}/query",
                  json={"question": QUERY_QUESTION}, timeout=40)

    tests = [
        {
            "name":    "GET /health",
            "target":  200,
            "fn":      lambda: requests.get(
                f"{BASE_URL}/health", timeout=10
            )
        },
        {
            "name":    "POST /categorise (cache hit)",
            "target":  200,
            "fn":      lambda: requests.post(
                f"{BASE_URL}/categorise",
                json={"text": CATEGORISE_TEXT},
                timeout=30
            )
        },
        {
            "name":    "POST /query (cache hit)",
            "target":  200,
            "fn":      lambda: requests.post(
                f"{BASE_URL}/query",
                json={"question": QUERY_QUESTION},
                timeout=40
            )
        },
        {
            "name":    "POST /generate-report (submit)",
            "target":  500,
            "fn":      lambda: requests.post(
                f"{BASE_URL}/generate-report",
                json={"survey_data": SURVEY_DATA},
                timeout=10
            )
        }
    ]

    for test in tests:
        times = []
        for _ in range(5):
            start   = time.perf_counter()
            test["fn"]()
            elapsed = round((time.perf_counter() - start) * 1000)
            times.append(elapsed)
            time.sleep(0.1)

        avg = round(sum(times) / len(times))
        ok  = avg <= test["target"]
        print_result(
            f"{test['name']} avg < {test['target']}ms", ok,
            f"avg={avg}ms  "
            f"min={min(times)}ms  "
            f"max={max(times)}ms"
        )
        if not ok:
            all_pass = False

    return all_pass

# ===============================================================
# VERIFY 4 — Fallback Working
# ===============================================================
def verify_fallback() -> bool:
    print_section("4. FALLBACK SERVICE VERIFICATION")
    all_pass = True

    print("\n  Testing fallback_service directly...")

    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from services.fallback_service import fallback_service

        # Categorise fallback
        result = fallback_service.get_categorise_fallback(
            error="Test error"
        )
        ok = (
            result["category"]            == "Uncategorised" and
            result["meta"]["is_fallback"] == True and
            result["meta"]["tokens_used"] == 0
        )
        print_result(
            "Categorise fallback returns is_fallback: True", ok,
            f"category={result['category']} "
            f"is_fallback={result['meta']['is_fallback']}"
        )
        if not ok:
            all_pass = False

        # Query fallback
        result = fallback_service.get_query_fallback(
            error="Test error"
        )
        ok = (
            result["answer"]              != "" and
            result["sources"]             == [] and
            result["meta"]["is_fallback"] == True
        )
        print_result(
            "Query fallback returns is_fallback: True", ok,
            f"sources={result['sources']} "
            f"is_fallback={result['meta']['is_fallback']}"
        )
        if not ok:
            all_pass = False

        # Generate report fallback
        result = fallback_service.get_generate_report_fallback(
            error="Test error"
        )
        ok = (
            result["report"]["title"]     != "" and
            result["meta"]["is_fallback"] == True
        )
        print_result(
            "Report fallback returns is_fallback: True", ok,
            f"title={result['report']['title'][:40]}... "
            f"is_fallback={result['meta']['is_fallback']}"
        )
        if not ok:
            all_pass = False

        # Rate limit detection
        ok = fallback_service.is_rate_limit_error("HTTP 429")
        print_result(
            "Rate limit error detected correctly", ok,
            "is_rate_limit_error('HTTP 429') = True"
        )
        if not ok:
            all_pass = False

        # Timeout detection
        ok = fallback_service.is_timeout_error("Request timed out")
        print_result(
            "Timeout error detected correctly", ok,
            "is_timeout_error('Request timed out') = True"
        )
        if not ok:
            all_pass = False

    except Exception as e:
        print(f"  [FAIL ✗] Fallback service error: {e}")
        all_pass = False

    return all_pass

# ===============================================================
# VERIFY 5 — All Meta Fields Correct
# ===============================================================
def verify_meta() -> bool:
    print_section("5. META OBJECT VERIFICATION")
    all_pass = True

    REQUIRED_META = [
        "confidence", "model_used", "tokens_used",
        "response_time_ms", "cached"
    ]

    # Categorise meta
    r    = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": CATEGORISE_TEXT, "skip_cache": True},
        timeout=30
    )
    data = r.json()
    meta = data.get("meta", {})

    missing = [f for f in REQUIRED_META if f not in meta]
    ok      = len(missing) == 0
    print_result(
        "/categorise meta has all required fields", ok,
        f"fields={list(meta.keys())}"
        if ok else f"missing={missing}"
    )
    if not ok:
        all_pass = False

    # Confidence range
    ok = 0.0 <= float(meta.get("confidence", -1)) <= 1.0
    print_result(
        "meta.confidence is 0.0-1.0", ok,
        f"confidence={meta.get('confidence')}"
    )
    if not ok:
        all_pass = False

    # Query meta
    r    = requests.post(
        f"{BASE_URL}/query",
        json={"question": QUERY_QUESTION, "skip_cache": True},
        timeout=40
    )
    data = r.json()
    meta = data.get("meta", {})

    missing = [f for f in REQUIRED_META if f not in meta]
    ok      = len(missing) == 0
    print_result(
        "/query meta has all required fields", ok,
        f"fields={list(meta.keys())}"
        if ok else f"missing={missing}"
    )
    if not ok:
        all_pass = False

    return all_pass

# ===============================================================
# VERIFY 6 — Generate Report End to End
# ===============================================================
def verify_generate_report() -> bool:
    print_section("6. GENERATE REPORT END TO END")
    all_pass = True

    print("\n  Submitting report job...")
    r = requests.post(
        f"{BASE_URL}/generate-report",
        json={"survey_data": SURVEY_DATA},
        timeout=10
    )

    ok = r.status_code == 202
    print_result(
        "POST /generate-report returns 202", ok,
        f"status_code={r.status_code}"
    )
    if not ok:
        all_pass = False
        return all_pass

    data   = r.json()
    job_id = data.get("job_id")

    ok = bool(job_id)
    print_result(
        "job_id returned immediately", ok,
        f"job_id={job_id[:8] if job_id else 'None'}..."
    )
    if not ok:
        all_pass = False
        return all_pass

    # Poll for completion
    print(f"\n  Polling job {job_id[:8]}...")
    final_status = None

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

    ok = final_status == "complete"
    print_result(
        "Job completed successfully", ok,
        f"final_status={final_status}"
    )
    if not ok:
        # Check if fallback
        result = final_data.get("result", {})
        if result and result.get("meta", {}).get("is_fallback"):
            print_result(
                "Fallback report returned (Groq unavailable)", True,
                "is_fallback=True — acceptable"
            )
        else:
            all_pass = False
        return all_pass

    # Verify report structure
    result = final_data.get("result", {})
    report = result.get("report", {})

    checks = [
        ("title present",             bool(report.get("title"))),
        ("executive_summary present",  bool(report.get("executive_summary"))),
        ("overview present",           bool(report.get("overview"))),
        ("top_items has 3+ items",     len(report.get("top_items", [])) >= 3),
        ("recommendations has 3+",     len(report.get("recommendations", [])) >= 3),
        ("is_fallback = False",        result.get("meta", {}).get("is_fallback") == False),
    ]

    for check_name, check_ok in checks:
        print_result(check_name, check_ok)
        if not check_ok:
            all_pass = False

    return all_pass

# ===============================================================
# MAIN
# ===============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 16 — FINAL PERFORMANCE VERIFICATION")
    print("=" * 60)
    print(f"Target URL: {BASE_URL}")
    print("Verifying: performance, cache, fallback, meta, report")

    results = {}

    results["health"]          = verify_health()
    results["cache"]           = verify_cache()
    results["performance"]     = verify_performance()
    results["fallback"]        = verify_fallback()
    results["meta"]            = verify_meta()
    results["generate_report"] = verify_generate_report()

    # Final summary 
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION SUMMARY")
    print("=" * 60)

    all_pass = True
    for name, passed in results.items():
        status = "PASS ✓" if passed else "FAIL ✗"
        print(f"  {name:<20} : {status}")
        if not passed:
            all_pass = False

    print("\n" + "=" * 60)
    print(
        f"  Day 16 status: "
        f"{'COMPLETE ✓' if all_pass else 'ISSUES FOUND ✗'}"
    )
    print("=" * 60)