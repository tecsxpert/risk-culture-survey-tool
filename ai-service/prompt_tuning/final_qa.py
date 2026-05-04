import sys
import os
import time
import requests

BASE_URL = "http://127.0.0.1:5000"

# 30 survey inputs — one per demo record category 
QA_INPUTS = [
    # Leadership & Governance
    {
        "id": 1,
        "text": "Our board never discusses risk appetite in meetings. The risk committee is a rubber stamp exercise with no real decisions made.",
        "expected": "Leadership & Governance"
    },
    {
        "id": 2,
        "text": "Senior executives openly bypass risk controls when under pressure. Junior staff see this and copy the behaviour.",
        "expected": "Leadership & Governance"
    },
    {
        "id": 3,
        "text": "The CEO mentioned risk management once in a town hall two years ago. Since then it has never come up in any leadership communication.",
        "expected": "Leadership & Governance"
    },
    {
        "id": 4,
        "text": "Our risk governance framework has not been updated since 2020. Nobody knows who owns it or when it will be reviewed.",
        "expected": "Leadership & Governance"
    },
    # Risk Awareness
    {
        "id": 5,
        "text": "Most employees in our department cannot name the top three operational risks we face. Risk awareness is very low.",
        "expected": "Risk Awareness"
    },
    {
        "id": 6,
        "text": "When I ask colleagues about our risk appetite statement, they have never heard of it. Nobody has explained it to frontline staff.",
        "expected": "Risk Awareness"
    },
    {
        "id": 7,
        "text": "Our last risk awareness survey scored 2.1 out of 5. Staff could not identify emerging risks in their own areas of work.",
        "expected": "Risk Awareness"
    },
    # Communication & Reporting
    {
        "id": 8,
        "text": "Risk reports are sent to the executive team but we never get any feedback. It feels like nobody reads them.",
        "expected": "Communication & Reporting"
    },
    {
        "id": 9,
        "text": "There is no clear escalation pathway for reporting risks. Staff do not know who to tell when they identify a problem.",
        "expected": "Communication & Reporting"
    },
    {
        "id": 10,
        "text": "When I raised a risk concern to my manager, I was told not to bother senior leadership with it. The message is clear — stay silent.",
        "expected": "Communication & Reporting"
    },
    # Accountability
    {
        "id": 11,
        "text": "Risk owners are assigned in our register but none of them ever update their risks. There are no consequences for ignoring them.",
        "expected": "Accountability"
    },
    {
        "id": 12,
        "text": "After our last audit, action items were assigned to managers but six months later not one of them has been completed.",
        "expected": "Accountability"
    },
    {
        "id": 13,
        "text": "Nobody takes ownership of risks in our organisation. Everyone assumes someone else is responsible for managing them.",
        "expected": "Accountability"
    },
    # Training & Competency
    {
        "id": 14,
        "text": "Our risk training module was last updated in 2018. New joiners complete it during onboarding and never receive any refresher.",
        "expected": "Training & Competency"
    },
    {
        "id": 15,
        "text": "I have been in this role for eight months and received no training on how to identify or escalate risks in my area.",
        "expected": "Training & Competency"
    },
    {
        "id": 16,
        "text": "Training completion rates for risk modules are below 40 percent in our department. Managers do not prioritise it.",
        "expected": "Training & Competency"
    },
    # Policies & Procedures
    {
        "id": 17,
        "text": "Our risk policy is 180 pages long and written in legal language. Nobody reads it and staff routinely bypass the procedures.",
        "expected": "Policies & Procedures"
    },
    {
        "id": 18,
        "text": "The data protection procedure was updated three months ago but no communication was sent to staff. We are still following the old process.",
        "expected": "Policies & Procedures"
    },
    {
        "id": 19,
        "text": "Policy exceptions are approved verbally with no documentation. There is no audit trail of who approved what or why.",
        "expected": "Policies & Procedures"
    },
    # Incident & Near Miss
    {
        "id": 20,
        "text": "Staff are afraid to report near misses because the last person who did was blamed and disciplined. Fear stops people speaking up.",
        "expected": "Incident & Near Miss"
    },
    {
        "id": 21,
        "text": "A serious near miss occurred last month but was not reported because the team did not want it to reflect badly on their performance.",
        "expected": "Incident & Near Miss"
    },
    {
        "id": 22,
        "text": "We have no process for sharing lessons learned from incidents. The same mistakes happen repeatedly across different teams.",
        "expected": "Incident & Near Miss"
    },
    # Culture & Behaviour
    {
        "id": 23,
        "text": "In our team it is normal to skip approval processes to meet deadlines. Senior staff do it openly and nobody questions them.",
        "expected": "Culture & Behaviour"
    },
    {
        "id": 24,
        "text": "Anyone who raises risk concerns is seen as a blocker and not a team player. The culture actively discourages speaking up about risks.",
        "expected": "Culture & Behaviour"
    },
    {
        "id": 25,
        "text": "Risk management is treated as a compliance box-ticking exercise. Nobody believes it adds real value to how we run the business.",
        "expected": "Culture & Behaviour"
    },
    # Mixed/Challenging inputs
    {
        "id": 26,
        "text": "The board approved a new risk appetite statement but it has never been communicated below director level. Most staff have never heard of it.",
        "expected": "Leadership & Governance"
    },
    {
        "id": 27,
        "text": "During our risk workshop half the attendees could not explain what a risk control is. Basic risk concepts are not understood.",
        "expected": "Risk Awareness"
    },
    {
        "id": 28,
        "text": "Our three lines of defence model is documented but nobody in the first line knows they are risk owners. The model exists on paper only.",
        "expected": "Accountability"
    },
    {
        "id": 29,
        "text": "New joiners shadow experienced staff who routinely cut corners. By the end of onboarding the new staff are already bypassing controls.",
        "expected": "Culture & Behaviour"
    },
    {
        "id": 30,
        "text": "Our incident reporting system is so complicated that staff give up halfway through. The process itself is a barrier to reporting.",
        "expected": "Incident & Near Miss"
    }
]

# Query inputs 
QUERY_INPUTS = [
    "What is the role of the board in risk culture?",
    "How can organisations improve incident reporting?",
    "What are signs of poor risk accountability?",
    "How should risk appetite be communicated?",
    "What makes risk training effective?",
    "How does peer behaviour influence risk decisions?",
    "What is the difference between risk culture and compliance?",
    "How can managers encourage staff to speak up about risks?",
    "What are common barriers to risk communication?",
    "How do you measure improvement in risk culture?"
]

# Scoring 
def score_categorise(result: dict, expected: str) -> dict:
    score    = 0
    feedback = []

    if result.get("category") and result.get("meta"):
        score += 1
        feedback.append("✓ Valid structure")
    else:
        feedback.append("✗ Invalid structure")

    if result.get("category") == expected:
        score += 2
        feedback.append(f"✓ Correct: {result.get('category')}")
    else:
        feedback.append(
            f"✗ Wrong: got '{result.get('category')}' "
            f"expected '{expected}'"
        )

    if float(result.get("confidence", 0)) >= 0.7:
        score += 1
        feedback.append(f"✓ Confidence {result.get('confidence')}")
    else:
        feedback.append(f"✗ Low confidence {result.get('confidence')}")

    meta = result.get("meta", {})
    if all(k in meta for k in ["confidence", "model_used", "tokens_used",
                                "response_time_ms", "cached"]):
        score += 1
        feedback.append("✓ Meta complete")
    else:
        feedback.append("✗ Meta incomplete")

    return {"score": score, "max": 5, "feedback": feedback}

def score_query(result: dict) -> dict:
    score    = 0
    feedback = []

    answer = result.get("answer", "")
    if answer and len(answer) > 20:
        score += 1
        feedback.append("✓ Answer provided")
    else:
        feedback.append("✗ No answer")

    word_count = len(answer.split())
    if 40 <= word_count <= 250:
        score += 1
        feedback.append(f"✓ Good length: {word_count} words")
    else:
        feedback.append(f"✗ Bad length: {word_count} words")

    if len(result.get("sources", [])) > 0:
        score += 1
        feedback.append(f"✓ {len(result.get('sources', []))} sources")
    else:
        feedback.append("✗ No sources")

    meta = result.get("meta", {})
    if all(k in meta for k in ["confidence", "model_used", "tokens_used",
                                "response_time_ms", "cached"]):
        score += 1
        feedback.append("✓ Meta complete")
    else:
        feedback.append("✗ Meta incomplete")

    if "•" not in answer and "\n-" not in answer:
        score = min(score + 1, 5)
        feedback.append("✓ No bullets")

    return {"score": min(score, 5), "max": 5, "feedback": feedback}

# Check system ready 
def check_ready() -> bool:
    try:
        r    = requests.get(f"{BASE_URL}/health", timeout=5)
        data = r.json()
        print(f"[Check] Status    : {data.get('status')}")
        print(f"[Check] ChromaDB  : {data.get('chromadb', {}).get('doc_count')} docs")
        print(f"[Check] Redis     : {data.get('cache', {}).get('redis_connected')}")

        if data.get("chromadb", {}).get("doc_count", 0) < 30:
            print(
                "[ERROR] ChromaDB has less than 30 docs. "
                "Run: python prompt_tuning/seed_30_records.py"
            )
            return False
        if data.get("status") != "healthy":
            print("[ERROR] Flask is not healthy")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Flask not running: {e}")
        return False

# Run categorise QA 
def run_categorise_qa():
    print("\n" + "═" * 60)
    print("QA: /categorise — 30 demo inputs")
    print("═" * 60)

    total_score  = 0
    failed_items = []
    wrong_cats   = []

    for item in QA_INPUTS:
        if item["id"] > 1:
            time.sleep(2)

        try:
            r = requests.post(
                f"{BASE_URL}/categorise",
                json={"text": item["text"], "skip_cache": True},
                timeout=30
            )
            data = r.json()

            if r.status_code != 200:
                print(f"Input {item['id']:02d}: ERROR {r.status_code}")
                failed_items.append(item["id"])
                continue

            scoring = score_categorise(data, item["expected"])
            total_score += scoring["score"]

            status = "✓" if scoring["score"] >= 4 else "✗"
            print(
                f"Input {item['id']:02d} [{status}] "
                f"Expected: {item['expected']:<30} "
                f"Got: {data.get('category'):<30} "
                f"Score: {scoring['score']}/5"
            )

            if data.get("category") != item["expected"]:
                wrong_cats.append({
                    "id":       item["id"],
                    "expected": item["expected"],
                    "got":      data.get("category")
                })

            if scoring["score"] < 3:
                failed_items.append(item["id"])

        except Exception as e:
            print(f"Input {item['id']:02d}: ERROR — {e}")
            failed_items.append(item["id"])

    max_score = len(QA_INPUTS) * 5
    avg_score = round(total_score / len(QA_INPUTS), 1)

    print(f"\n{'─' * 60}")
    print(f"Total : {total_score}/{max_score}")
    print(f"Avg   : {avg_score}/5")
    print(f"Status: {'PASS ✓' if avg_score >= 4 else 'NEEDS WORK ✗'}")

    if wrong_cats:
        print(f"\nWrong categories ({len(wrong_cats)}):")
        for w in wrong_cats:
            print(
                f"  Input {w['id']:02d}: "
                f"expected '{w['expected']}' "
                f"got '{w['got']}'"
            )

    return avg_score, wrong_cats

# Run query QA 
def run_query_qa():
    print("\n" + "═" * 60)
    print("QA: /query — 10 demo questions")
    print("═" * 60)

    total_score  = 0
    failed_items = []

    for i, question in enumerate(QUERY_INPUTS, 1):
        if i > 1:
            time.sleep(3)

        try:
            r = requests.post(
                f"{BASE_URL}/query",
                json={"question": question, "skip_cache": True},
                timeout=40
            )
            data = r.json()

            if r.status_code != 200:
                print(f"Query {i:02d}: ERROR {r.status_code}")
                failed_items.append(i)
                continue

            scoring = score_query(data)
            total_score += scoring["score"]

            answer = data.get("answer", "")
            status = "✓" if scoring["score"] >= 4 else "✗"
            print(
                f"Query {i:02d} [{status}] "
                f"Score: {scoring['score']}/5 — "
                f"{question[:50]}..."
            )
            print(f"         Answer: {answer[:80]}...")

            if scoring["score"] < 3:
                failed_items.append(i)

        except Exception as e:
            print(f"Query {i:02d}: ERROR — {e}")
            failed_items.append(i)

    max_score = len(QUERY_INPUTS) * 5
    avg_score = round(total_score / len(QUERY_INPUTS), 1)

    print(f"\n{'─' * 60}")
    print(f"Total : {total_score}/{max_score}")
    print(f"Avg   : {avg_score}/5")
    print(f"Status: {'PASS ✓' if avg_score >= 4 else 'NEEDS WORK ✗'}")

    return avg_score

# Run generate-report QA 
def run_generate_report_qa():
    print("\n" + "═" * 60)
    print("QA: /generate-report — demo survey data")
    print("═" * 60)

    survey_data = """
    Risk Culture Survey Results — Demo Organisation — May 2026

    Total respondents: 47 employees across 5 departments

    Key findings:
    1. Leadership: 78% of staff say senior management never 
       discusses risk in team meetings
    2. Risk Awareness: Average score 2.1/5 — staff cannot 
       identify top operational risks
    3. Incident Reporting: 3 near misses went unreported 
       last quarter due to fear of blame
    4. Training: Risk training last updated 2019, 
       completion rate only 42%
    5. Accountability: 0% of risk action items completed 
       on time in last 6 months

    Overall risk culture score: 2.3 out of 5.0
    Survey completion rate: 78%
    Benchmark comparison: Below industry average of 3.4/5
    """

    print("Submitting report generation job...")
    r = requests.post(
        f"{BASE_URL}/generate-report",
        json={"survey_data": survey_data},
        timeout=10
    )

    if r.status_code != 202:
        print(f"ERROR: Could not submit job — {r.status_code}")
        return 0

    job_id = r.json().get("job_id")
    print(f"Job created: {job_id[:8]}...")
    print("Polling for completion...")

    for attempt in range(30):
        time.sleep(3)
        poll = requests.get(
            f"{BASE_URL}/generate-report/{job_id}",
            timeout=10
        )
        status = poll.json().get("status")
        print(f"  [{(attempt+1)*3}s] Status: {status}")

        if status == "complete":
            result = poll.json().get("result", {})
            report = result.get("report", {})
            meta   = result.get("meta", {})

            print(f"\n  Title      : {report.get('title', '')[:60]}")
            print(f"  Exec summ  : {report.get('executive_summary', '')[:80]}...")
            print(f"  Top items  : {len(report.get('top_items', []))}")
            print(f"  Recs       : {len(report.get('recommendations', []))}")
            print(f"  is_fallback: {meta.get('is_fallback', False)}")

            score = 0
            if report.get("title"):              score += 2
            if report.get("executive_summary"):  score += 2
            if report.get("overview"):           score += 2
            if len(report.get("top_items", [])) >= 3:    score += 2
            if len(report.get("recommendations", [])) >= 3: score += 2

            print(f"\n  Score : {score}/10")
            print(
                f"  Status: "
                f"{'PASS ✓' if score >= 8 else 'NEEDS WORK ✗'}"
            )
            return score

        elif status == "failed":
            error = poll.json().get("error", "unknown")
            print(f"  Job failed: {error}")
            # Check if it's a fallback
            result = poll.json().get("result", {})
            if result and result.get("meta", {}).get("is_fallback"):
                print("  Fallback response returned — is_fallback: True")
                return 6  # partial score for fallback
            return 0

    print("  Timeout waiting for job")
    return 0

# Main 
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 14 — FINAL PROMPT QA")
    print("30 demo records — all outputs must be demo-ready")
    print("=" * 60)

    if not check_ready():
        print("\nFix issues above then re-run")
        sys.exit(1)

    # Run all QA tests
    cat_score,  wrong_cats = run_categorise_qa()
    query_score            = run_query_qa()
    report_score           = run_generate_report_qa()

    # Final summary
    print("\n" + "=" * 60)
    print("FINAL QA SUMMARY")
    print("=" * 60)
    print(
        f"  /categorise      : {cat_score}/5 avg "
        f"({'PASS ✓' if cat_score >= 4 else 'NEEDS WORK ✗'})"
    )
    print(
        f"  /query           : {query_score}/5 avg "
        f"({'PASS ✓' if query_score >= 4 else 'NEEDS WORK ✗'})"
    )
    print(
        f"  /generate-report : {report_score}/10 "
        f"({'PASS ✓' if report_score >= 8 else 'NEEDS WORK ✗'})"
    )

    overall_pass = (
        cat_score >= 4 and
        query_score >= 4 and
        report_score >= 8
    )

    print(f"\n  Day 14 status: {'COMPLETE ✓' if overall_pass else 'NEEDS WORK ✗'}")
    print("=" * 60)