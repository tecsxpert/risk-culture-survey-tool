import requests

BASE_URL = "http://localhost:5000"

# Seed ChromaDB before testing 
def seed_chroma():
    """Add sample docs so ChromaDB has something to retrieve."""
    print("[Setup] Seeding ChromaDB with sample documents...")
    from services.chroma_client import chroma_client

    chroma_client.reset_collection()
    chroma_client.add_documents([
        {
            "id": "doc_001",
            "text": (
                "Leadership plays a critical role in shaping risk culture. "
                "When senior management visibly supports risk management, "
                "employees are more likely to follow risk processes."
            ),
            "metadata": {"category": "Leadership & Governance", "source": "risk_guide"}
        },
        {
            "id": "doc_002",
            "text": (
                "Risk awareness training helps employees understand how to "
                "identify and report risks in their daily work. Regular "
                "training improves overall risk culture scores significantly."
            ),
            "metadata": {"category": "Training & Competency", "source": "risk_guide"}
        },
        {
            "id": "doc_003",
            "text": (
                "Incident reporting is essential for learning from near misses. "
                "Organisations with strong reporting cultures experience fewer "
                "major incidents over time."
            ),
            "metadata": {"category": "Incident & Near Miss", "source": "risk_guide"}
        },
        {
            "id": "doc_004",
            "text": (
                "Clear accountability structures ensure risk owners take "
                "responsibility for managing their identified risks. Without "
                "accountability, risk registers become outdated quickly."
            ),
            "metadata": {"category": "Accountability", "source": "risk_guide"}
        },
        {
            "id": "doc_005",
            "text": (
                "Communication of risk policies must be clear and accessible "
                "to all staff. Poor communication leads to inconsistent "
                "application of risk procedures across departments."
            ),
            "metadata": {"category": "Communication & Reporting", "source": "risk_guide"}
        }
    ])
    print(f"Seeded {chroma_client.count()} documents\n")


# Test cases 
test_cases = [
    {
        "label":    "Leadership question",
        "question": "How does senior management influence risk culture?"
    },
    {
        "label":    "Training question",
        "question": "Why is risk awareness training important for employees?"
    },
    {
        "label":    "Incident reporting question",
        "question": "What are the benefits of reporting near misses?"
    },
    {
        "label":    "Empty question — expect 400",
        "question": ""
    },
    {
        "label":    "Too short — expect 400",
        "question": "Why?"
    }
]


def run_tests():
    print("=" * 60)
    print("Testing POST /query — RAG Pipeline")
    print("=" * 60)

    passed = 0
    failed = 0

    for i, case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {case['label']}")
        q = case["question"]
        print(f"Question: {q[:70]}{'...' if len(q) > 70 else ''}")

        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"question": q},
                timeout=30
            )
            print(f"Status  : {response.status_code}")
            data = response.json()

            if response.status_code == 200:
                print(f"Answer  : {data.get('answer', '')[:120]}...")
                print(f"Chunks  : {data.get('chunks_used')}")
                sources = data.get("sources", [])
                for s in sources:
                    print(f"  Source: [{s['category']}] score={s['score']}")
                meta = data.get("meta", {})
                print(f"Tokens  : {meta.get('tokens_used')}")
                print(f"Time ms : {meta.get('response_time_ms')}")
                print(f"Fallback: {meta.get('is_fallback')}")
                passed += 1

            else:
                error = data.get("error", "Unknown error")
                print(f"Error   : {error}")
                if case["label"] in ["Empty question — expect 400",
                                     "Too short — expect 400"]:
                    print("(Expected error — PASS)")
                    passed += 1
                else:
                    failed += 1

        except requests.exceptions.ConnectionError:
            print("ERROR: Cannot connect. Is Flask running? → python app.py")
            failed += 1
        except Exception as e:
            print(f"ERROR: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results : {passed} passed, {failed} failed")
    print("Day 5 status:", "COMPLETE ✓" if failed == 0 else "FAILED ✗")
    print("=" * 60)


if __name__ == "__main__":
    seed_chroma()
    run_tests()