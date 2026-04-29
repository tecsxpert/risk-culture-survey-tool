import sys
import os
import json

# Add parent directory to path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.groq_client import groq_client
from services.chroma_client import chroma_client

# ===============================================================
# 10 REAL RISK CULTURE SURVEY INPUTS FOR TESTING
# ===============================================================
TEST_INPUTS = [
    {
        "id": 1,
        "text": (
            "Our CEO never mentions risk management in town halls. "
            "Senior leaders treat risk as a compliance checkbox rather "
            "than something that genuinely matters to the business."
        ),
        "expected_category": "Leadership & Governance"
    },
    {
        "id": 2,
        "text": (
            "Most of my colleagues do not know what our risk appetite "
            "statement says. When I ask them about operational risks "
            "in their area, they look confused and say it is not their job."
        ),
        "expected_category": "Risk Awareness"
    },
    {
        "id": 3,
        "text": (
            "When I tried to escalate a risk I identified last quarter, "
            "my manager told me to handle it myself and not bother "
            "senior management. There is no clear channel for reporting "
            "risks upward in this organisation."
        ),
        "expected_category": "Communication & Reporting"
    },
    {
        "id": 4,
        "text": (
            "Nobody takes ownership of the risks on our register. "
            "Risk owners are assigned but they never update their risks "
            "and there are no consequences for ignoring them."
        ),
        "expected_category": "Accountability"
    },
    {
        "id": 5,
        "text": (
            "I joined this company six months ago and have received "
            "no training on how to identify or report risks. New "
            "employees are expected to figure out risk processes on their own."
        ),
        "expected_category": "Training & Competency"
    },
    {
        "id": 6,
        "text": (
            "Our risk policies are 200 pages long and written in legal "
            "language that nobody can understand. Staff routinely bypass "
            "procedures because they do not know they exist."
        ),
        "expected_category": "Policies & Procedures"
    },
    {
        "id": 7,
        "text": (
            "Last month a near miss occurred in our warehouse but nobody "
            "reported it because the last person who reported an incident "
            "was blamed and made to feel responsible. Fear of blame "
            "stops people from speaking up."
        ),
        "expected_category": "Incident & Near Miss"
    },
    {
        "id": 8,
        "text": (
            "In our team it is normal to cut corners to meet deadlines. "
            "Taking risks is seen as being entrepreneurial. Anyone who "
            "raises concerns is seen as a blocker and not a team player."
        ),
        "expected_category": "Culture & Behaviour"
    },
    {
        "id": 9,
        "text": (
            "The board receives a risk report every quarter but it is "
            "always green. Nobody believes the report reflects reality "
            "because managers filter out bad news before it reaches "
            "the top."
        ),
        "expected_category": "Leadership & Governance"
    },
    {
        "id": 10,
        "text": (
            "We completed a risk awareness survey last year and scored "
            "very low. The results were shared with management but "
            "no action was taken. Staff feel their feedback is ignored."
        ),
        "expected_category": "Risk Awareness"
    }
]


# ===============================================================
# SCORING FUNCTIONS
# ===============================================================
def score_categorise_response(result: dict, expected: str) -> dict:
    """
    Score a /categorise response out of 10.

    Scoring criteria:
    - Category correct          : 5 points
    - Confidence >= 0.7         : 2 points
    - Reasoning is meaningful   : 2 points
    - Valid JSON returned        : 1 point
    """
    score = 0
    feedback = []

    # 1 point — valid JSON structure
    if all(k in result for k in ["category", "confidence", "reasoning"]):
        score += 1
        feedback.append("✓ Valid JSON structure (1/1)")
    else:
        feedback.append("✗ Missing fields in JSON (0/1)")

    # 5 points — correct category
    if result.get("category") == expected:
        score += 5
        feedback.append(f"✓ Correct category: {result.get('category')} (5/5)")
    else:
        feedback.append(
            f"✗ Wrong category: got '{result.get('category')}' "
            f"expected '{expected}' (0/5)"
        )

    # 2 points — confidence >= 0.7
    confidence = float(result.get("confidence", 0))
    if confidence >= 0.7:
        score += 2
        feedback.append(f"✓ Confidence {confidence} >= 0.7 (2/2)")
    elif confidence >= 0.5:
        score += 1
        feedback.append(f"~ Confidence {confidence} is low (1/2)")
    else:
        feedback.append(f"✗ Confidence {confidence} too low (0/2)")

    # 2 points — reasoning is meaningful (more than 10 words)
    reasoning = result.get("reasoning", "")
    word_count = len(reasoning.split())
    if word_count >= 15:
        score += 2
        feedback.append(f"✓ Reasoning is meaningful ({word_count} words) (2/2)")
    elif word_count >= 8:
        score += 1
        feedback.append(f"~ Reasoning is brief ({word_count} words) (1/2)")
    else:
        feedback.append(f"✗ Reasoning too short ({word_count} words) (0/2)")

    return {"score": score, "feedback": feedback}


def load_prompt(filename: str) -> str:
    """Load prompt from prompts/ folder."""
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "prompts",
        filename
    )
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def parse_ai_json(content: str) -> dict:
    """Safely parse AI JSON response."""
    cleaned = content.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()
    return json.loads(cleaned)


# ===============================================================
# TEST /categorise PROMPT
# ===============================================================
def test_categorise_prompt():
    print("\n" + "═" * 60)
    print("TESTING: /categorise prompt")
    print("═" * 60)

    system_prompt = load_prompt("categorise_prompt.txt")
    total_score   = 0
    max_score     = len(TEST_INPUTS) * 10
    failed_inputs = []

    for item in TEST_INPUTS:
        print(f"\nInput {item['id']:02d}: {item['text'][:60]}...")
        print(f"Expected : {item['expected_category']}")

        ai_result = groq_client.chat(
            system_prompt=system_prompt,
            user_message=(
                f"Classify this risk culture survey response:\n\n{item['text']}"
            ),
            temperature=0.1,
            max_tokens=200
        )

        if ai_result["is_fallback"]:
            print("SKIPPED — Groq unavailable")
            continue

        try:
            parsed  = parse_ai_json(ai_result["content"])
            scoring = score_categorise_response(parsed, item["expected_category"])

            print(f"Got      : {parsed.get('category')}")
            print(f"Score    : {scoring['score']}/10")
            for f in scoring["feedback"]:
                print(f"           {f}")

            total_score += scoring["score"]

            if scoring["score"] < 7:
                failed_inputs.append({
                    "id":    item["id"],
                    "score": scoring["score"],
                    "text":  item["text"][:80]
                })

        except (json.JSONDecodeError, ValueError) as e:
            print(f"PARSE ERROR: {e}")
            print(f"Raw: {ai_result['content'][:100]}")

    avg_score = round(total_score / len(TEST_INPUTS), 1)

    print("\n" + "─" * 60)
    print(f"CATEGORISE PROMPT RESULTS")
    print(f"Total score : {total_score}/{max_score}")
    print(f"Average     : {avg_score}/10")
    print(f"Status      : {'PASS ✓' if avg_score >= 7 else 'NEEDS REWRITE ✗'}")

    if failed_inputs:
        print(f"\nFailed inputs (score < 7):")
        for f in failed_inputs:
            print(f"  Input {f['id']:02d} scored {f['score']}/10 — {f['text']}...")

    return avg_score


# ===============================================================
# TEST /query PROMPT
# ===============================================================
def seed_chroma_for_testing():
    """Seed ChromaDB with sample docs for query testing."""
    print("\n[Setup] Seeding ChromaDB for query prompt test...")
    chroma_client.reset_collection()
    chroma_client.add_documents([
        {
            "id": "seed_001",
            "text": (
                "Strong leadership commitment is the foundation of good risk culture. "
                "When senior managers visibly champion risk management, employees "
                "follow their example and take risk processes seriously."
            ),
            "metadata": {"category": "Leadership & Governance", "source": "risk_handbook"}
        },
        {
            "id": "seed_002",
            "text": (
                "Regular risk awareness training significantly improves an "
                "organisation's ability to identify and mitigate risks early. "
                "Employees who understand risk processes are 3x more likely "
                "to report concerns before they escalate."
            ),
            "metadata": {"category": "Training & Competency", "source": "risk_handbook"}
        },
        {
            "id": "seed_003",
            "text": (
                "A blame-free reporting culture encourages staff to report "
                "near misses and incidents without fear of punishment. "
                "Organisations that achieve this see a 40% reduction in "
                "major incidents within two years."
            ),
            "metadata": {"category": "Incident & Near Miss", "source": "risk_handbook"}
        },
        {
            "id": "seed_004",
            "text": (
                "Clear risk ownership and accountability structures ensure "
                "that every identified risk has a named owner responsible "
                "for monitoring and mitigation. Without this, risk registers "
                "become outdated and ineffective."
            ),
            "metadata": {"category": "Accountability", "source": "risk_handbook"}
        },
        {
            "id": "seed_005",
            "text": (
                "Effective risk communication involves clear escalation "
                "pathways so that frontline staff can report risks to "
                "senior management quickly. Delays in communication "
                "often allow small risks to become major incidents."
            ),
            "metadata": {"category": "Communication & Reporting", "source": "risk_handbook"}
        }
    ])
    print(f"Seeded {chroma_client.count()} documents ✓")


QUERY_TEST_INPUTS = [
    "How does leadership behaviour affect risk culture?",
    "Why is it important to report near misses?",
    "What makes risk training effective?",
    "How should risks be escalated to senior management?",
    "What happens when nobody owns a risk?"
]

QUERY_SCORING_CRITERIA = [
    "Answer is relevant to the question",
    "Answer uses information from context (not made up)",
    "Answer is 3-5 sentences long",
    "Answer is professional in tone",
    "No bullet points used"
]


def score_query_response(answer: str, question: str) -> dict:
    """Score a /query response out of 10."""
    score    = 0
    feedback = []

    # 2 points — answer length (3-5 sentences approx 50-200 words)
    word_count = len(answer.split())
    if 40 <= word_count <= 250:
        score += 2
        feedback.append(f"✓ Good length: {word_count} words (2/2)")
    elif word_count > 250:
        score += 1
        feedback.append(f"~ Too long: {word_count} words (1/2)")
    else:
        feedback.append(f"✗ Too short: {word_count} words (0/2)")

    # 2 points — no bullet points
    if "•" not in answer and "- " not in answer and "* " not in answer:
        score += 2
        feedback.append("✓ No bullet points — paragraph format (2/2)")
    else:
        feedback.append("✗ Contains bullet points (0/2)")

    # 3 points — answer is relevant (contains risk-related keywords)
    risk_keywords = [
        "risk", "culture", "management", "organisation",
        "report", "leadership", "accountability"
    ]
    found = [k for k in risk_keywords if k.lower() in answer.lower()]
    if len(found) >= 4:
        score += 3
        feedback.append(f"✓ Relevant content — {len(found)} keywords found (3/3)")
    elif len(found) >= 2:
        score += 2
        feedback.append(f"~ Partially relevant — {len(found)} keywords (2/3)")
    else:
        feedback.append(f"✗ Low relevance — only {len(found)} keywords (0/3)")

    # 3 points — does not say "I don't have information" for knowable questions
    if "don't have sufficient information" not in answer.lower():
        score += 3
        feedback.append("✓ Provided a real answer (3/3)")
    else:
        feedback.append("✗ Returned 'no information' for a knowable question (0/3)")

    return {"score": score, "feedback": feedback}


def test_query_prompt():
    print("\n" + "═" * 60)
    print("TESTING: /query prompt (RAG)")
    print("═" * 60)

    seed_chroma_for_testing()
    system_prompt_template = load_prompt("query_prompt.txt")
    total_score            = 0
    max_score              = len(QUERY_TEST_INPUTS) * 10

    for i, question in enumerate(QUERY_TEST_INPUTS, 1):
        print(f"\nQuery {i:02d}: {question}")

        # Retrieve chunks from ChromaDB
        chunks  = chroma_client.query(question, n_results=3)
        context = "\n\n".join([
            f"[Document {j+1}]\n{c['text']}"
            for j, c in enumerate(chunks)
        ])

        system_prompt = system_prompt_template.replace("{context}", context)

        ai_result = groq_client.chat(
            system_prompt=system_prompt,
            user_message=f"Question: {question}",
            temperature=0.3,
            max_tokens=400
        )

        if ai_result["is_fallback"]:
            print("SKIPPED — Groq unavailable")
            continue

        answer  = ai_result["content"]
        scoring = score_query_response(answer, question)

        print(f"Answer   : {answer[:120]}...")
        print(f"Score    : {scoring['score']}/10")
        for f in scoring["feedback"]:
            print(f"           {f}")

        total_score += scoring["score"]

    avg_score = round(total_score / len(QUERY_TEST_INPUTS), 1)

    print("\n" + "─" * 60)
    print(f"QUERY PROMPT RESULTS")
    print(f"Total score : {total_score}/{max_score}")
    print(f"Average     : {avg_score}/10")
    print(f"Status      : {'PASS ✓' if avg_score >= 7 else 'NEEDS REWRITE ✗'}")

    return avg_score


# ===============================================================
# MAIN
# ===============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 6 — PROMPT TUNING EVALUATION")
    print("=" * 60)

    cat_score   = test_categorise_prompt()
    query_score = test_query_prompt()

    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"  /categorise prompt : {cat_score}/10 avg "
          f"{'✓ PASS' if cat_score >= 7 else '✗ REWRITE NEEDED'}")
    print(f"  /query prompt      : {query_score}/10 avg "
          f"{'✓ PASS' if query_score >= 7 else '✗ REWRITE NEEDED'}")
    print()

    overall = (cat_score + query_score) / 2
    print(f"  Overall average    : {overall}/10")
    print(f"  Day 6 status       : "
          f"{'COMPLETE ✓' if overall >= 7 else 'PROMPTS NEED IMPROVEMENT ✗'}")
    print("=" * 60)