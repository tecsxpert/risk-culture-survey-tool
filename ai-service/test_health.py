import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    print("=" * 60)
    print("Testing GET /health")
    print("=" * 60)

    passed = 0
    failed = 0

    # Test 1: Health endpoint returns 200
    print("\nTest 1: GET /health returns 200")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Status  : {response.status_code}")

        if response.status_code in [200, 503]:
            data = response.json()
            print(f"Overall : {data.get('status')}")
            passed += 1
            print("PASSED ✓")
        else:
            print(f"FAILED ✗ — unexpected status {response.status_code}")
            failed += 1

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect. Is Flask running? → python app.py")
        failed += 1

    # Test 2: Response has all required fields
    print("\nTest 2: Response contains all required fields")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        data     = response.json()

        required_fields = [
            "status", "timestamp", "uptime",
            "groq", "chromadb", "cache"
        ]
        missing = [f for f in required_fields if f not in data]

        if not missing:
            print("All required fields present ✓")
            passed += 1
        else:
            print(f"FAILED ✗ — missing fields: {missing}")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 3: Groq section has required fields
    print("\nTest 3: Groq section is complete")
    try:
        response  = requests.get(f"{BASE_URL}/health", timeout=10)
        data      = response.json()
        groq_data = data.get("groq", {})

        groq_fields = [
            "model", "key_loaded",
            "avg_response_time_ms",
            "response_times_tracked"
        ]
        missing = [f for f in groq_fields if f not in groq_data]

        if not missing:
            print(f"Model         : {groq_data.get('model')}")
            print(f"Key loaded    : {groq_data.get('key_loaded')}")
            print(f"Avg resp time : {groq_data.get('avg_response_time_ms')}ms")
            print(f"Times tracked : {groq_data.get('response_times_tracked')}")
            passed += 1
            print("PASSED ✓")
        else:
            print(f"FAILED ✗ — missing groq fields: {missing}")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 4: ChromaDB section is complete
    print("\nTest 4: ChromaDB section is complete")
    try:
        response     = requests.get(f"{BASE_URL}/health", timeout=10)
        data         = response.json()
        chroma_data  = data.get("chromadb", {})

        if "status" in chroma_data and "doc_count" in chroma_data:
            print(f"Status    : {chroma_data.get('status')}")
            print(f"Doc count : {chroma_data.get('doc_count')}")
            passed += 1
            print("PASSED ✓")
        else:
            print("FAILED ✗ — missing chromadb fields")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 5: Cache section is complete
    print("\nTest 5: Cache section is complete")
    try:
        response   = requests.get(f"{BASE_URL}/health", timeout=10)
        data       = response.json()
        cache_data = data.get("cache", {})

        cache_fields = ["hits", "misses", "total", "hit_rate_pct"]
        missing      = [f for f in cache_fields if f not in cache_data]

        if not missing:
            print(f"Hits        : {cache_data.get('hits')}")
            print(f"Misses      : {cache_data.get('misses')}")
            print(f"Total       : {cache_data.get('total')}")
            print(f"Hit rate    : {cache_data.get('hit_rate_pct')}%")
            passed += 1
            print("PASSED ✓")
        else:
            print(f"FAILED ✗ — missing cache fields: {missing}")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 6: Uptime is tracked correctly
    print("\nTest 6: Uptime is tracked")
    try:
        response    = requests.get(f"{BASE_URL}/health", timeout=10)
        data        = response.json()
        uptime_data = data.get("uptime", {})

        if "seconds" in uptime_data and "human" in uptime_data:
            print(f"Uptime seconds : {uptime_data.get('seconds')}")
            print(f"Uptime human   : {uptime_data.get('human')}")
            assert uptime_data["seconds"] >= 0, "Uptime cannot be negative"
            passed += 1
            print("PASSED ✓")
        else:
            print("FAILED ✗ — missing uptime fields")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Print full response
    print("\n" + "─" * 60)
    print("Full /health response:")
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    print(json.dumps(response.json(), indent=2))

    # Summary
    print("\n" + "=" * 60)
    print(f"Results  : {passed} passed, {failed} failed")
    print(f"Day 7 status: {'COMPLETE ✓' if failed == 0 else 'FAILED ✗'}")
    print("=" * 60)

if __name__ == "__main__":
    test_health()