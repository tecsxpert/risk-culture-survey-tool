import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.fallback_service import fallback_service

print("=" * 60)
print("DAY 13 — AI Fallback Service Tests")
print("=" * 60)

passed = 0
failed = 0

# Test 1: Categorise fallback 
print("\nTest 1: Categorise fallback response")
try:
    result = fallback_service.get_categorise_fallback(
        error="HTTP 429: rate limit exceeded"
    )

    assert result["category"]             == "Uncategorised"
    assert result["confidence"]           == 0.0
    assert result["from_cache"]           == False
    assert result["generated_at"]         is not None
    assert result["meta"]["is_fallback"]  == True
    assert result["meta"]["confidence"]   == 0.0
    assert result["meta"]["tokens_used"]  == 0
    assert result["meta"]["cached"]       == False
    assert "error" in result["meta"]

    print(f"  category    : {result['category']}")
    print(f"  confidence  : {result['confidence']}")
    print(f"  is_fallback : {result['meta']['is_fallback']}")
    print(f"  error       : {result['meta']['error'][:50]}...")
    print("  PASSED ✓")
    passed += 1

except AssertionError as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1
except Exception as e:
    print(f"  ERROR — {e}")
    failed += 1

# Test 2: Query fallback 
print("\nTest 2: Query fallback response")
try:
    result = fallback_service.get_query_fallback(
        error="Request timed out"
    )

    assert result["answer"]              != ""
    assert result["sources"]             == []
    assert result["chunks_used"]         == 0
    assert result["from_cache"]          == False
    assert result["generated_at"]        is not None
    assert result["meta"]["is_fallback"] == True
    assert result["meta"]["tokens_used"] == 0

    print(f"  answer      : {result['answer'][:80]}...")
    print(f"  sources     : {result['sources']}")
    print(f"  is_fallback : {result['meta']['is_fallback']}")
    print("  PASSED ✓")
    passed += 1

except AssertionError as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1
except Exception as e:
    print(f"  ERROR — {e}")
    failed += 1

# Test 3: Generate report fallback 
print("\nTest 3: Generate report fallback response")
try:
    result = fallback_service.get_generate_report_fallback(
        error="HTTP 429: rate limit exceeded"
    )

    report = result["report"]
    assert report["title"]                != ""
    assert report["executive_summary"]    != ""
    assert report["overview"]             != ""
    assert len(report["top_items"])       >= 1
    assert len(report["recommendations"]) >= 1
    assert result["meta"]["is_fallback"]  == True
    assert result["meta"]["tokens_used"]  == 0

    print(f"  title       : {report['title'][:60]}")
    print(f"  top_items   : {len(report['top_items'])}")
    print(f"  recs        : {len(report['recommendations'])}")
    print(f"  is_fallback : {result['meta']['is_fallback']}")
    print("  PASSED ✓")
    passed += 1

except AssertionError as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1
except Exception as e:
    print(f"  ERROR — {e}")
    failed += 1

# Test 4: Rate limit detection 
print("\nTest 4: Rate limit error detection")
try:
    assert fallback_service.is_rate_limit_error(
        "HTTP 429: rate limit"
    ) == True,  "Should detect 429"

    assert fallback_service.is_rate_limit_error(
        "HTTP 500: server error"
    ) == False, "Should not detect 500 as rate limit"

    assert fallback_service.is_rate_limit_error(
        "rate_limit_exceeded"
    ) == True,  "Should detect rate_limit_exceeded"

    print("  429 detected correctly         ✓")
    print("  500 not detected as rate limit ✓")
    print("  rate_limit_exceeded detected   ✓")
    print("  PASSED ✓")
    passed += 1

except AssertionError as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1

# Test 5: Timeout detection 
print("\nTest 5: Timeout error detection")
try:
    assert fallback_service.is_timeout_error(
        "Request timed out"
    ) == True,  "Should detect 'timed out'"

    assert fallback_service.is_timeout_error(
        "Read timeout occurred"
    ) == True,  "Should detect 'timeout'"

    assert fallback_service.is_timeout_error(
        "HTTP 429 rate limit"
    ) == False, "Should not detect rate limit as timeout"

    print(
        f"  is_timeout_error('Request timed out') = "
        f"{fallback_service.is_timeout_error('Request timed out')} ✓"
    )
    print(
        f"  is_timeout_error('Read timeout') = "
        f"{fallback_service.is_timeout_error('Read timeout occurred')} ✓"
    )
    print(
        f"  is_timeout_error('rate limit') = "
        f"{fallback_service.is_timeout_error('HTTP 429 rate limit')} ✓"
    )
    print("  PASSED ✓")
    passed += 1

except AssertionError as e:
    print(f"  FAILED ✗ — {e}")
    print(
        f"  Debug: is_timeout_error('Request timed out') = "
        f"{fallback_service.is_timeout_error('Request timed out')}"
    )
    print(
        f"  Debug: is_timeout_error('Read timeout occurred') = "
        f"{fallback_service.is_timeout_error('Read timeout occurred')}"
    )
    failed += 1

# Test 6: Retry messages 
print("\nTest 6: Retry messages are human-readable")
try:
    rate_msg    = fallback_service.get_retry_message(
        "HTTP 429 rate limit"
    )
    timeout_msg = fallback_service.get_retry_message(
        "Request timed out"
    )
    generic_msg = fallback_service.get_retry_message(
        "Unknown error"
    )

    assert len(rate_msg)    > 20, "Rate limit message too short"
    assert len(timeout_msg) > 20, "Timeout message too short"
    assert len(generic_msg) > 20, "Generic message too short"

    print(f"  Rate limit : {rate_msg[:60]}...")
    print(f"  Timeout    : {timeout_msg[:60]}...")
    print(f"  Generic    : {generic_msg[:60]}...")
    print("  PASSED ✓")
    passed += 1

except AssertionError as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1

# Test 7: meta object is always complete 
print("\nTest 7: meta object has all required fields")
try:
    required_fields = [
        "confidence", "model_used", "tokens_used",
        "response_time_ms", "cached", "is_fallback", "error"
    ]

    endpoints = [
        (
            "categorise",
            lambda: fallback_service.get_categorise_fallback()
        ),
        (
            "query",
            lambda: fallback_service.get_query_fallback()
        ),
        (
            "generate-report",
            lambda: fallback_service.get_generate_report_fallback()
        )
    ]

    for endpoint, fn in endpoints:
        result  = fn()
        meta    = result.get("meta", {})
        missing = [f for f in required_fields if f not in meta]

        if missing:
            raise AssertionError(
                f"{endpoint} meta missing fields: {missing}"
            )
        print(f"  {endpoint}: all meta fields present ✓")

    print("  PASSED ✓")
    passed += 1

except AssertionError as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1

# Summary 
print("\n" + "=" * 60)
print(f"Results      : {passed} passed, {failed} failed")
print(
    f"Day 13 status: "
    f"{'COMPLETE ✓' if failed == 0 else 'FAILED ✗'}"
)
print("=" * 60)