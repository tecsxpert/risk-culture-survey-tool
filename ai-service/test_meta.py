import time
import redis
import requests
import json

BASE_URL  = "http://localhost:5000"
UNIQUE_ID = str(int(time.time()))

# Required meta fields per the spec
REQUIRED_META_FIELDS = [
    "confidence",
    "model_used",
    "tokens_used",
    "response_time_ms",
    "cached"
]

def clear_redis():
    try:
        r = redis.Redis(host="localhost", port=6379,
                        db=0, decode_responses=True)
        r.flushall()
        print("[Setup] Redis flushed ✓")
    except Exception as e:
        print(f"[Setup] Redis flush skipped: {e}")

def check_meta(data: dict, endpoint: str) -> tuple[bool, list]:
    """
    Check that meta object exists and has all required fields.
    Returns (passed, list of issues)
    """
    issues = []
    meta   = data.get("meta")

    if not meta:
        issues.append("meta object is missing entirely")
        return False, issues

    for field in REQUIRED_META_FIELDS:
        if field not in meta:
            issues.append(f"meta.{field} is missing")

    # Validate confidence is 0.0-1.0
    if "confidence" in meta:
        c = meta["confidence"]
        if not (0.0 <= float(c) <= 1.0):
            issues.append(f"meta.confidence {c} is out of range 0.0-1.0")

    # Validate cached is boolean
    if "cached" in meta:
        if not isinstance(meta["cached"], bool):
            issues.append(f"meta.cached should be bool, got {type(meta['cached'])}")

    # Validate tokens_used is int
    if "tokens_used" in meta:
        if not isinstance(meta["tokens_used"], int):
            issues.append(
                f"meta.tokens_used should be int, got {type(meta['tokens_used'])}"
            )

    # Validate response_time_ms is number
    if "response_time_ms" in meta:
        if not isinstance(meta["response_time_ms"], (int, float)):
            issues.append("meta.response_time_ms should be a number")

    return len(issues) == 0, issues

def run_tests():
    clear_redis()

    print("=" * 60)
    print("Testing meta object on all responses — Day 9")
    print("=" * 60)

    passed = 0
    failed = 0

    # Test 1: /categorise fresh call has correct meta
    print("\nTest 1: /categorise fresh call — meta object correct")
    try:
        text = (
            f"Test {UNIQUE_ID} — Our CEO never discusses risk management "
            f"in any team meetings or leadership sessions."
        )
        r    = requests.post(
            f"{BASE_URL}/categorise",
            json={"text": text, "skip_cache": True},
            timeout=30
        )
        data = r.json()
        print(f"Status      : {r.status_code}")

        ok, issues = check_meta(data, "/categorise")
        meta        = data.get("meta", {})

        print(f"confidence  : {meta.get('confidence')}")
        print(f"model_used  : {meta.get('model_used')}")
        print(f"tokens_used : {meta.get('tokens_used')}")
        print(f"resp_time   : {meta.get('response_time_ms')}ms")
        print(f"cached      : {meta.get('cached')}")

        if ok and r.status_code == 200 and meta.get("cached") == False:
            print("PASSED ✓")
            passed += 1
        else:
            print(f"FAILED ✗ — issues: {issues}")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 2: /categorise cached call has cached=True in meta
    print("\nTest 2: /categorise cached call — meta.cached = True")
    try:
        text = (
            f"Test {UNIQUE_ID} — Our CEO never discusses risk management "
            f"in any team meetings or leadership sessions."
        )
        # Call twice — second should be cached
        requests.post(
            f"{BASE_URL}/categorise",
            json={"text": text},
            timeout=30
        )
        r2   = requests.post(
            f"{BASE_URL}/categorise",
            json={"text": text},
            timeout=30
        )
        data2 = r2.json()
        meta2 = data2.get("meta", {})

        print(f"from_cache  : {data2.get('from_cache')}")
        print(f"meta.cached : {meta2.get('cached')}")

        if data2.get("from_cache") == True and meta2.get("cached") == True:
            print("PASSED ✓ — cached response has meta.cached = True")
            passed += 1
        else:
            print("FAILED ✗ — meta.cached should be True for cached response")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 3: /query fresh call has correct meta
    print("\nTest 3: /query fresh call — meta object correct")
    try:
        question = (
            f"Test {UNIQUE_ID} — How does leadership behaviour "
            f"affect risk culture in an organisation?"
        )
        r    = requests.post(
            f"{BASE_URL}/query",
            json={"question": question, "skip_cache": True},
            timeout=30
        )
        data = r.json()
        print(f"Status      : {r.status_code}")

        ok, issues = check_meta(data, "/query")
        meta        = data.get("meta", {})

        print(f"confidence  : {meta.get('confidence')}")
        print(f"model_used  : {meta.get('model_used')}")
        print(f"tokens_used : {meta.get('tokens_used')}")
        print(f"resp_time   : {meta.get('response_time_ms')}ms")
        print(f"cached      : {meta.get('cached')}")

        if ok and r.status_code == 200 and meta.get("cached") == False:
            print("PASSED ✓")
            passed += 1
        else:
            print(f"FAILED ✗ — issues: {issues}")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 4: /query cached call has cached=True in meta
    print("\nTest 4: /query cached call — meta.cached = True")
    try:
        question = (
            f"Test {UNIQUE_ID} — How does leadership behaviour "
            f"affect risk culture in an organisation?"
        )
        requests.post(
            f"{BASE_URL}/query",
            json={"question": question},
            timeout=30
        )
        r2   = requests.post(
            f"{BASE_URL}/query",
            json={"question": question},
            timeout=30
        )
        data2 = r2.json()
        meta2 = data2.get("meta", {})

        print(f"from_cache  : {data2.get('from_cache')}")
        print(f"meta.cached : {meta2.get('cached')}")

        if data2.get("from_cache") == True and meta2.get("cached") == True:
            print("PASSED ✓ — cached response has meta.cached = True")
            passed += 1
        else:
            print("FAILED ✗ — meta.cached should be True for cached response")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 5: meta fields have correct data types
    print("\nTest 5: meta field data types are correct")
    try:
        text = (
            f"Type check {UNIQUE_ID} — Nobody reports incidents "
            f"because they are afraid of being blamed by management."
        )
        r    = requests.post(
            f"{BASE_URL}/categorise",
            json={"text": text, "skip_cache": True},
            timeout=30
        )
        data = r.json()
        meta = data.get("meta", {})

        type_checks = [
            ("confidence",       (int, float), meta.get("confidence")),
            ("model_used",       str,           meta.get("model_used")),
            ("tokens_used",      int,           meta.get("tokens_used")),
            ("response_time_ms", (int, float),  meta.get("response_time_ms")),
            ("cached",           bool,          meta.get("cached"))
        ]

        all_ok = True
        for field, expected_type, value in type_checks:
            if isinstance(value, expected_type):
                print(f"  ✓ meta.{field} = {value} ({type(value).__name__})")
            else:
                print(
                    f"  ✗ meta.{field} = {value} "
                    f"(expected {expected_type}, got {type(value).__name__})"
                )
                all_ok = False

        if all_ok:
            print("PASSED ✓ — all meta field types correct")
            passed += 1
        else:
            print("FAILED ✗ — some meta fields have wrong types")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Summary 
    print("\n" + "=" * 60)
    print(f"Results     : {passed} passed, {failed} failed")
    print(f"Day 9 status: {'COMPLETE ✓' if failed == 0 else 'FAILED ✗'}")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()