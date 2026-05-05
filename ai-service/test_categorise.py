import requests
import json

BASE_URL = "http://localhost:5000"

# Test cases — one per category
test_cases = [
    {
        "label": "Leadership & Governance",
        "text": "Our senior management never talks about risk in team meetings. "
                "There is no visible commitment from leadership to manage risks properly."
    },
    {
        "label": "Risk Awareness",
        "text": "Most employees in our department do not know what the risk register is "
                "or how to report a risk they have identified."
    },
    {
        "label": "Training & Competency",
        "text": "We have not received any risk management training in over two years. "
                "New joiners are not trained on risk procedures during onboarding."
    },
    {
        "label": "Incident & Near Miss",
        "text": "Staff are afraid to report near misses because they worry about "
                "being blamed. Many incidents go unreported as a result."
    },
    {
        "label": "Empty text — expect 400",
        "text": ""
    }
]


def run_tests():
    print("=" * 60)
    print("Testing POST /categorise")
    print("=" * 60)

    passed = 0
    failed = 0

    for i, case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {case['label']}")
        print(f"Input : {case['text'][:60]}{'...' if len(case['text']) > 60 else ''}")

        try:
            response = requests.post(
                f"{BASE_URL}/categorise",
                json={"text": case["text"]},
                timeout=30
            )

            print(f"Status: {response.status_code}")
            data = response.json()

            if response.status_code == 200:
                print(f"Category   : {data.get('category')}")
                print(f"Confidence : {data.get('confidence')}")
                print(f"Reasoning  : {data.get('reasoning')}")
                print(f"Fallback   : {data.get('is_fallback')}")
                passed += 1
            else:
                print(f"Error : {data.get('error')}")
                if case["label"] == "Empty text — expect 400":
                    print("(Expected 400 — PASS)")
                    passed += 1
                else:
                    failed += 1

        except requests.exceptions.ConnectionError:
            print("ERROR: Cannot connect. Is Flask running on port 5000?")
            print("Run: python app.py")
            failed += 1
        except Exception as e:
            print(f"ERROR: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("Day 3 status:", "COMPLETE ✓" if failed == 0 else "FAILED ✗")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()