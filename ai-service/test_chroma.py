from services.chroma_client import chroma_client

print("=" * 60)
print("Testing ChromaDB Setup")
print("=" * 60)

passed = 0
failed = 0

# Reset for clean test 
print("\n[Setup] Resetting collection for clean test...")
chroma_client.reset_collection()
print(f"Documents after reset: {chroma_client.count()}")


#Test 1: Add documents 
print("\nTest 1: Add documents")
sample_docs = [
    {
        "id": "doc_001",
        "text": (
            "Leadership plays a critical role in shaping risk culture. "
            "When senior management visibly supports risk management, "
            "employees are more likely to follow risk processes."
        ),
        "metadata": {"category": "Leadership & Governance", "source": "test"}
    },
    {
        "id": "doc_002",
        "text": (
            "Risk awareness training helps employees understand how to "
            "identify and report risks in their daily work. Regular training "
            "improves overall risk culture scores significantly."
        ),
        "metadata": {"category": "Training & Competency", "source": "test"}
    },
    {
        "id": "doc_003",
        "text": (
            "Incident reporting is essential for learning from near misses. "
            "Organisations with strong reporting cultures experience fewer "
            "major incidents over time."
        ),
        "metadata": {"category": "Incident & Near Miss", "source": "test"}
    },
    {
        "id": "doc_004",
        "text": (
            "Clear accountability structures ensure that risk owners take "
            "responsibility for managing their identified risks. Without "
            "accountability, risk registers become outdated quickly."
        ),
        "metadata": {"category": "Accountability", "source": "test"}
    },
    {
        "id": "doc_005",
        "text": (
            "Communication of risk policies must be clear and accessible "
            "to all staff. Poor communication leads to inconsistent "
            "application of risk procedures across departments."
        ),
        "metadata": {"category": "Communication & Reporting", "source": "test"}
    }
]

try:
    count = chroma_client.add_documents(sample_docs)
    assert count == 5, f"Expected 5, got {count}"
    assert chroma_client.count() == 5, "Collection count mismatch"
    print(f"  Added    : {count} documents")
    print(f"  DB count : {chroma_client.count()}")
    print("  PASSED ✓")
    passed += 1
except Exception as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1


# Test 2: Query returns correct result 
print("\nTest 2: Query — leadership related question")
try:
    results = chroma_client.query(
        "How does management behaviour affect risk culture?",
        n_results=2
    )
    assert len(results) > 0, "No results returned"
    top = results[0]
    assert "id" in top
    assert "text" in top
    assert "score" in top
    assert "metadata" in top

    print(f"  Top result ID       : {top['id']}")
    print(f"  Top result category : {top['metadata'].get('category')}")
    print(f"  Similarity score    : {top['score']}")
    print(f"  Text preview        : {top['text'][:80]}...")
    print("  PASSED ✓")
    passed += 1
except Exception as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1


# Test 3: Query returns correct result for different topic 
print("\nTest 3: Query — incident reporting question")
try:
    results = chroma_client.query(
        "Why should employees report near misses?",
        n_results=2
    )
    assert len(results) > 0
    top = results[0]
    print(f"  Top result ID       : {top['id']}")
    print(f"  Top result category : {top['metadata'].get('category')}")
    print(f"  Similarity score    : {top['score']}")
    print("  PASSED ✓")
    passed += 1
except Exception as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1


# Test 4: Empty collection query 
print("\nTest 4: Query on empty collection returns empty list")
try:
    chroma_client.reset_collection()
    results = chroma_client.query("any query", n_results=3)
    assert results == [], f"Expected [], got {results}"
    print("  Empty list returned correctly")
    print("  PASSED ✓")
    passed += 1
except Exception as e:
    print(f"  FAILED ✗ — {e}")
    failed += 1


# Summary
print("\n" + "=" * 60)
print(f"Results : {passed} passed, {failed} failed")
print("Day 4 status:", "COMPLETE ✓" if failed == 0 else "FAILED ✗")
print("=" * 60)