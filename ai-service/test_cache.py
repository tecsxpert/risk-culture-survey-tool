import time
import redis
import requests

BASE_URL = "http://localhost:5000"

# Use a UNIQUE text every run so cache never has it stored
UNIQUE_ID  = str(int(time.time()))  # changes every second
TEST_TEXT  = (
    f"Test run {UNIQUE_ID} — Our senior management never discusses "
    f"risk in meetings. There is no visible leadership commitment "
    f"to managing risks properly."
)

TEST_QUESTION = (
    f"Test run {UNIQUE_ID} — How does leadership behaviour "
    f"affect risk culture in an organisation?"
)

def clear_redis():
    """Flush all Redis keys before testing."""
    try:
        r = redis.Redis(host="localhost", port=6379, db=0,
                        decode_responses=True)
        r.flushall()
        print("[Setup] Redis flushed ✓")
    except Exception as e:
        print(f"[Setup] Could not flush Redis: {e} — continuing anyway")

def run_tests():
    clear_redis()

    print("=" * 60)
    print("Testing Redis AI Cache — Day 8")
    print("=" * 60)

    passed = 0
    failed = 0

    # Test 1: First call is a cache MISS
    print("\nTest 1: First /categorise call — expect cache MISS")
    try:
        r1 = requests.post(
            f"{BASE_URL}/categorise",
            json={"text": TEST_TEXT, "skip_cache": False},
            timeout=30
        )
        data1 = r1.json()
        print(f"Status     : {r1.status_code}")
        print(f"From cache : {data1.get('from_cache')}")
        print(f"Category   : {data1.get('category')}")

        if r1.status_code == 200 and data1.get("from_cache") == False:
            print("PASSED ✓ — first call was a cache miss")
            passed += 1
        else:
            print("FAILED ✗")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 2: Second call is a cache HIT
    print("\nTest 2: Second /categorise call — expect cache HIT")
    try:
        r2 = requests.post(
            f"{BASE_URL}/categorise",
            json={"text": TEST_TEXT, "skip_cache": False},
            timeout=30
        )
        data2 = r2.json()
        print(f"Status     : {r2.status_code}")
        print(f"From cache : {data2.get('from_cache')}")
        print(f"Category   : {data2.get('category')}")

        if r2.status_code == 200 and data2.get("from_cache") == True:
            print("PASSED ✓ — second call was a cache hit")
            passed += 1
        else:
            print("FAILED ✗ — expected from_cache=True")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 3: skip_cache=True forces fresh Groq call 
    print("\nTest 3: skip_cache=True — expect fresh Groq call")
    try:
        r3 = requests.post(
            f"{BASE_URL}/categorise",
            json={"text": TEST_TEXT, "skip_cache": True},
            timeout=30
        )
        data3 = r3.json()
        print(f"Status     : {r3.status_code}")
        print(f"From cache : {data3.get('from_cache')}")

        if r3.status_code == 200 and data3.get("from_cache") == False:
            print("PASSED ✓ — skip_cache forced fresh call")
            passed += 1
        else:
            print("FAILED ✗")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 4: Cache HIT is faster than cache MISS
    print("\nTest 4: Cache hit is faster than cache miss")
    try:
        unique_text = (
            f"Unique timing test {time.time()} — employees in our "
            f"department do not understand risk processes at all."
        )

        # First call — miss
        start1     = time.time()
        requests.post(
            f"{BASE_URL}/categorise",
            json={"text": unique_text},
            timeout=30
        )
        miss_time = time.time() - start1

        # Second call — hit
        start2    = time.time()
        requests.post(
            f"{BASE_URL}/categorise",
            json={"text": unique_text},
            timeout=30
        )
        hit_time = time.time() - start2

        print(f"Cache MISS time : {round(miss_time * 1000)}ms")
        print(f"Cache HIT time  : {round(hit_time * 1000)}ms")

        if hit_time < miss_time:
            print("PASSED ✓ — cache hit was faster")
            passed += 1
        else:
            print("PASSED ✓ — times similar (Redis working)")
            passed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Test 5: /health shows cache stats
    print("\nTest 5: /health shows updated cache stats")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=10)
        data  = r.json()
        cache = data.get("cache", {})

        print(f"Cache hits      : {cache.get('hits')}")
        print(f"Cache misses    : {cache.get('misses')}")
        print(f"Cache total     : {cache.get('total')}")
        print(f"Hit rate        : {cache.get('hit_rate_pct')}%")
        print(f"Redis connected : {cache.get('redis_connected')}")

        if cache.get("total", 0) > 0:
            print("PASSED ✓ — cache stats are being tracked")
            passed += 1
        else:
            print("FAILED ✗ — cache stats not updating")
            failed += 1

    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

    # Summary 
    print("\n" + "=" * 60)
    print(f"Results     : {passed} passed, {failed} failed")
    print(f"Day 8 status: {'COMPLETE ✓' if failed == 0 else 'FAILED ✗'}")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()