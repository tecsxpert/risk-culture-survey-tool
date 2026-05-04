import sys
import os
import time
import requests

BASE_URL = "http://localhost:5000"

# ===============================================================
# 10 FRESH INPUTS FOR /categorise
# ===============================================================
CATEGORISE_INPUTS = [
    {
        "id": 1,
        "text": (
            "Our risk committee meets quarterly but the meetings are "
            "just a formality. Decisions are never actually made and "
            "nothing changes after each meeting."
        ),
        "expected": "Leadership & Governance"
    },
    {
        "id": 2,
        "text": (
            "When I asked my team lead what our top three operational "
            "risks are, she said she had no idea. Nobody in our team "
            "has ever been told what risks we are supposed to manage."
        ),
        "expected": "Risk Awareness"
    },
    {
        "id": 3,
        "text": (
            "Risk reports are sent to the executive team every month "
            "but we never get any feedback. It feels like the reports "
            "go into a black hole and nobody reads them."
        ),
        "expected": "Communication & Reporting"
    },
    {
        "id": 4,
        "text": (
            "After our audit findings last year, action items were "
            "assigned to specific managers but six months later none "
            "of them have been completed. There are no consequences "
            "for missing deadlines on risk actions."
        ),
        "expected": "Accountability"
    },
    {
        "id": 5,
        "text": (
            "Our risk management training module is from 2018 and has "
            "never been updated. Staff complete it once during "
            "onboarding and never receive any refresher training."
        ),
        "expected": "Training & Competency"
    },
    {
        "id": 6,
        "text": (
            "The data protection policy was updated six months ago "
            "but nobody was informed. Staff are still following the "
            "old procedures because they do not know the policy changed."
        ),
        "expected": "Policies & Procedures"
    },
    {
        "id": 7,
        "text": (
            "A serious near miss happened in our IT department last "
            "month when a server nearly went down during peak trading. "
            "The engineer who caught it was told not to write it up "
            "because it would reflect badly on the team."
        ),
        "expected": "Incident & Near Miss"
    },
    {
        "id": 8,
        "text": (
            "In our office it is completely normal to skip the approval "
            "process when we are under time pressure. Senior staff do "
            "it openly and nobody questions them. Junior staff copy "
            "the same behaviour."
        ),
        "expected": "Culture & Behaviour"
    },
    {
        "id": 9,
        "text": (
            "The board approved a new risk appetite statement last year "
            "but it has never been communicated to staff below director "
            "level. Most employees have never heard of it."
        ),
        "expected": "Leadership & Governance"
    },
    {
        "id": 10,
        "text": (
            "During our risk workshop last week, half the attendees "
            "could not explain what a risk control is or how to assess "
            "the likelihood of a risk occurring. Basic concepts are "
            "not well understood across the organisation."
        ),
        "expected": "Risk Awareness"
    }
]

# ===============================================================
# 10 FRESH INPUTS FOR /query
# ===============================================================
QUERY_INPUTS = [
    "What is the role of the board in risk culture?",
    "How can organisations improve incident reporting rates?",
    "What are the signs of poor risk accountability?",
    "How should risk appetite be communicated to staff?",
    "What makes a risk training programme effective?",
    "How does peer behaviour influence individual risk decisions?",
    "What is the difference between risk culture and compliance?",
    "How can managers encourage staff to speak up about risks?",
    "What are common barriers to good risk communication?",
    "How do you measure improvement in risk culture over time?"
]

# ===============================================================
# SCORING — out of 5 
# ===============================================================
def score_categorise(result: dict, expected: str) -> dict:
    """Score /categorise response out of 5."""
    score    = 0
    feedback = []

    # 1 point — valid response structure
    if result.get("category") and result.get("meta"):
        score += 1
        feedback.append("✓ Valid response structure (1/1)")
    else:
        feedback.append("✗ Invalid response structure (0/1)")

    # 2 points — correct category
    if result.get("category") == expected:
        score += 2
        feedback.append(
            f"✓ Correct category: {result.get('category')} (2/2)"
        )
    else:
        feedback.append(
            f"✗ Wrong: got '{result.get('category')}' "
            f"expected '{expected}' (0/2)"
        )

    # 1 point — confidence >= 0.7
    confidence = float(result.get("confidence", 0))
    if confidence >= 0.7:
        score += 1
        feedback.append(f"✓ Confidence {confidence} >= 0.7 (1/1)")
    else:
        feedback.append(f"✗ Confidence {confidence} too low (0/1)")

    # 1 point — meta object complete
    meta = result.get("meta", {})
    meta_complete = all(
        k in meta for k in [
            "confidence", "model_used",
            "tokens_used", "response_time_ms", "cached"
        ]
    )
    if meta_complete:
        score += 1
        feedback.append("✓ Meta object complete (1/1)")
    else:
        feedback.append("✗ Meta object incomplete (0/1)")

    return {"score": score, "max": 5, "feedback": feedback}

def score_query(result: dict) -> dict:
    """Score /query response out of 5."""
    score    = 0
    feedback = []

    # 1 point — has answer field
    answer = result.get("answer", "")
    if answer and len(answer) > 20:
        score += 1
        feedback.append("✓ Answer provided (1/1)")
    else:
        feedback.append("✗ No answer provided (0/1)")

    # 1 point — answer length 40-250 words
    word_count = len(answer.split())
    if 40 <= word_count <= 250:
        score += 1
        feedback.append(f"✓ Good length: {word_count} words (1/1)")
    else:
        feedback.append(f"✗ Bad length: {word_count} words (0/1)")

    # 1 point — has sources
    sources = result.get("sources", [])
    if len(sources) > 0:
        score += 1
        feedback.append(f"✓ {len(sources)} sources returned (1/1)")
    else:
        feedback.append("✗ No sources returned (0/1)")

    # 1 point — meta object complete
    meta = result.get("meta", {})
    meta_complete = all(
        k in meta for k in [
            "confidence", "model_used",
            "tokens_used", "response_time_ms", "cached"
        ]
    )
    if meta_complete:
        score += 1
        feedback.append("✓ Meta object complete (1/1)")
    else:
        feedback.append("✗ Meta object incomplete (0/1)")

    # Bonus point — no bullet points (capped at 5)
    if "•" not in answer and "\n-" not in answer:
        score = min(score + 1, 5)
        feedback.append("✓ No bullet points (bonus)")

    return {"score": min(score, 5), "max": 5, "feedback": feedback}

# ===============================================================
# CHECK CHROMA HAS DATA BEFORE RUNNING
# ===============================================================
def check_chroma_ready() -> bool:
    """Verify ChromaDB has documents before running query tests."""
    try:
        r    = requests.get(f"{BASE_URL}/health", timeout=10)
        data = r.json()
        count = data.get("chromadb", {}).get("doc_count", 0)
        print(f"[Check] ChromaDB has {count} documents")
        if count == 0:
            print(
                "[ERROR] ChromaDB is empty! "
                "Run: python prompt_tuning/seed_chroma.py "
                "then restart Flask."
            )
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Cannot reach Flask: {e}")
        return False

# ===============================================================
# RUN CATEGORISE REVIEW
# ===============================================================
def review_categorise():
    print("\n" + "═" * 60)
    print("REVIEWING: /categorise — 10 fresh inputs")
    print("═" * 60)

    total_score  = 0
    failed_items = []

    for item in CATEGORISE_INPUTS:
        print(f"\nInput {item['id']:02d}: {item['text'][:55]}...")
        print(f"Expected : {item['expected']}")

        # Delay to avoid Groq rate limiting
        if item["id"] > 1:
            print("         (waiting 2s...)")
            time.sleep(2)

        try:
            r = requests.post(
                f"{BASE_URL}/categorise",
                json={"text": item["text"], "skip_cache": True},
                timeout=30
            )
            data = r.json()

            if r.status_code != 200:
                print(f"ERROR: HTTP {r.status_code} — {data}")
                failed_items.append(item["id"])
                continue

            scoring = score_categorise(data, item["expected"])
            total_score += scoring["score"]

            print(f"Got      : {data.get('category')}")
            print(f"Score    : {scoring['score']}/{scoring['max']}")
            for f in scoring["feedback"]:
                print(f"           {f}")

            if scoring["score"] < 3:
                failed_items.append(item["id"])

        except Exception as e:
            print(f"ERROR: {e}")
            failed_items.append(item["id"])

    max_score = len(CATEGORISE_INPUTS) * 5
    avg_score = round(total_score / len(CATEGORISE_INPUTS), 1)

    print("\n" + "─" * 60)
    print(f"CATEGORISE RESULTS")
    print(f"Total : {total_score}/{max_score}")
    print(f"Avg   : {avg_score}/5")
    print(
        f"Status: {'PASS ✓' if avg_score >= 4 else 'NEEDS IMPROVEMENT ✗'}"
    )
    if failed_items:
        print(f"Failed inputs: {failed_items}")

    return avg_score

# ===============================================================
# RUN QUERY REVIEW
# ===============================================================
def review_query():
    print("\n" + "═" * 60)
    print("REVIEWING: /query — 10 fresh inputs")
    print("═" * 60)

    total_score  = 0
    failed_items = []

    for i, question in enumerate(QUERY_INPUTS, 1):
        print(f"\nQuery {i:02d}: {question}")

        # Delay to avoid Groq rate limiting
        if i > 1:
            print("         (waiting 3s...)")
            time.sleep(3)

        try:
            r = requests.post(
                f"{BASE_URL}/query",
                json={"question": question, "skip_cache": True},
                timeout=40
            )
            data = r.json()

            if r.status_code != 200:
                print(f"ERROR: HTTP {r.status_code} — {data}")
                failed_items.append(i)
                continue

            scoring = score_query(data)
            total_score += scoring["score"]

            answer = data.get("answer", "")
            print(f"Answer   : {answer[:100]}...")
            print(f"Score    : {scoring['score']}/{scoring['max']}")
            for f in scoring["feedback"]:
                print(f"           {f}")

            if scoring["score"] < 3:
                failed_items.append(i)

        except Exception as e:
            print(f"ERROR: {e}")
            failed_items.append(i)

    max_score = len(QUERY_INPUTS) * 5
    avg_score = round(total_score / len(QUERY_INPUTS), 1)

    print("\n" + "─" * 60)
    print(f"QUERY RESULTS")
    print(f"Total : {total_score}/{max_score}")
    print(f"Avg   : {avg_score}/5")
    print(
        f"Status: {'PASS ✓' if avg_score >= 4 else 'NEEDS IMPROVEMENT ✗'}"
    )
    if failed_items:
        print(f"Failed queries: {failed_items}")

    return avg_score

# ===============================================================
# MAIN
# ===============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 10 — WEEK 2 AI QUALITY REVIEW")
    print("=" * 60)

    # Check Flask is running and ChromaDB has data
    if not check_chroma_ready():
        print("\nABORTED — fix ChromaDB first then re-run")
        sys.exit(1)

    # Run categorise review
    cat_score = review_categorise()

    # Run query review
    query_score = review_query()

    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"  /categorise avg : {cat_score}/5 "
          f"{'✓ PASS' if cat_score >= 4 else '✗ NEEDS IMPROVEMENT'}")
    print(f"  /query avg      : {query_score}/5 "
          f"{'✓ PASS' if query_score >= 4 else '✗ NEEDS IMPROVEMENT'}")

    overall = (cat_score + query_score) / 2
    print(f"  Overall avg     : {overall}/5")
    print(f"  Day 10 status   : "
          f"{'COMPLETE ✓' if overall >= 4 else 'PROMPTS NEED WORK ✗'}")
    print("=" * 60)