# Day 14 — Final Prompt QA Results

**Date:** 3 May 2026
**Developer:** AI Developer 2
**Target:** All outputs demo-ready
**ChromaDB docs:** 30
**Redis:** Connected

---

## /categorise — 30 Demo Inputs

| Input | Expected | Got | Score |
|-------|----------|-----|-------|
| 1 | Leadership & Governance | Leadership & Governance | 5/5 |
| 2 | Leadership & Governance | Leadership & Governance | 5/5 |
| 3 | Leadership & Governance | Leadership & Governance | 5/5 |
| 4 | Leadership & Governance | Leadership & Governance | 5/5 |
| 5 | Risk Awareness | Risk Awareness | 5/5 |
| 6 | Risk Awareness | Risk Awareness | 5/5 |
| 7 | Risk Awareness | Risk Awareness | 5/5 |
| 8 | Communication & Reporting | Communication & Reporting | 5/5 |
| 9 | Communication & Reporting | Communication & Reporting | 5/5 |
| 10 | Communication & Reporting | Accountability | 3/5 |
| 11 | Accountability | Accountability | 5/5 |
| 12 | Accountability | Accountability | 5/5 |
| 13 | Accountability | Accountability | 5/5 |
| 14 | Training & Competency | Training & Competency | 5/5 |
| 15 | Training & Competency | Training & Competency | 5/5 |
| 16 | Training & Competency | Training & Competency | 5/5 |
| 17 | Policies & Procedures | Policies & Procedures | 5/5 |
| 18 | Policies & Procedures | Communication & Reporting | 3/5 |
| 19 | Policies & Procedures | Policies & Procedures | 5/5 |
| 20 | Incident & Near Miss | Incident & Near Miss | 5/5 |
| 21 | Incident & Near Miss | Incident & Near Miss | 5/5 |
| 22 | Incident & Near Miss | Incident & Near Miss | 5/5 |
| 23 | Culture & Behaviour | Culture & Behaviour | 5/5 |
| 24 | Culture & Behaviour | Culture & Behaviour | 5/5 |
| 25 | Culture & Behaviour | Culture & Behaviour | 5/5 |
| 26 | Leadership & Governance | Communication & Reporting | 3/5 |
| 27 | Risk Awareness | Risk Awareness | 5/5 |
| 28 | Accountability | Accountability | 5/5 |
| 29 | Culture & Behaviour | Culture & Behaviour | 5/5 |
| 30 | Incident & Near Miss | Incident & Near Miss | 5/5 |

**Total Score:** 144/150
**Average Score:** 4.8/5
**Status:** PASS ✓

### Wrong Categories (3 inputs)

| Input | Expected | Got | Root Cause |
|-------|----------|-----|------------|
| 10 | Communication & Reporting | Accountability | Text mentions "nobody knows who to tell" — AI picked up accountability angle |
| 18 | Policies & Procedures | Communication & Reporting | Text mentions "no communication was sent" — communication keyword triggered |
| 26 | Leadership & Governance | Communication & Reporting | Text mentions "never been communicated" — same communication trigger issue |

**Pattern identified:** When survey responses mention the word "communicated"
or "communication", the AI sometimes classifies as Communication & Reporting
even when the primary issue is governance or policy. This is an acceptable
edge case — 27/30 correct is strong performance.

---

## /query — 10 Demo Questions

| Query | Score | Answer Preview |
|-------|-------|----------------|
| What is the role of the board in risk culture? | 5/5 | The board of directors plays a critical role... |
| How can organisations improve incident reporting? | 5/5 | To improve incident reporting, organisations should... |
| What are signs of poor risk accountability? | 5/5 | Signs of poor risk accountability include overdue... |
| How should risk appetite be communicated? | 5/5 | Risk appetite should be communicated in a way that... |
| What makes risk training effective? | 5/5 | Effective risk training is characterized by... |
| How does peer behaviour influence risk decisions? | 5/5 | Peer behaviour has a significant influence on... |
| What is the difference between risk culture and compliance? | 5/5 | Risk culture and compliance are distinct concepts... |
| How can managers encourage staff to speak up about risks? | 5/5 | Managers can encourage a speak-up culture by... |
| What are common barriers to risk communication? | 5/5 | Common barriers to risk communication include... |
| How do you measure improvement in risk culture? | 5/5 | Measuring improvement in risk culture can be... |

**Total Score:** 50/50
**Average Score:** 5.0/5
**Status:** PASS ✓

---

## /generate-report — Demo Survey Data

| Field | Value | Status |
|-------|-------|--------|
| title | Risk Culture Assessment Report — Demo Organisation — May 2026 | ✓ |
| executive_summary | The Demo Organisation's risk culture health is concerning, with a score of 2.3/5... | ✓ |
| overview | Present and detailed | ✓ |
| top_items | 3 items returned | ✓ |
| recommendations | 3 recommendations returned | ✓ |
| is_fallback | False | ✓ |
| Job completion time | 3 seconds | ✓ |

**Score:** 10/10
**Status:** PASS ✓

---

## Issues Found and Resolution

| Issue | Severity | Resolution |
|-------|----------|------------|
| Input 10 wrong category | Low | Acceptable edge case — ambiguous text |
| Input 18 wrong category | Low | Communication keyword triggers false match |
| Input 26 wrong category | Low | Same communication keyword issue |

All 3 wrong classifications are caused by ambiguous survey responses
that contain keywords from multiple categories. The 90% accuracy rate
(27/30) is above the acceptable threshold for demo purposes.

---

## Demo Readiness Checklist

- [x] /categorise scoring 4.8/5 — above 4.0 target
- [x] /query scoring 5.0/5 — perfect score
- [x] /generate-report scoring 10/10 — perfect score
- [x] All responses have correct meta object
- [x] is_fallback: False on all successful calls
- [x] Report generated in 3 seconds
- [x] 30 demo records seeded in ChromaDB
- [x] Redis cache active and working

---

## Setup Instructions for Demo Day

```bash
# Step 1 — Start Redis
& "C:\Users\Downloads\Redis-x64-3.2.100\redis-server.exe"

# Step 2 — Seed ChromaDB with 30 records
python prompt_tuning/seed_30_records.py

# Step 3 — Start Flask
python app.py

# Step 4 — Verify health
curl http://127.0.0.1:5000/health
```

**IMPORTANT:** Use 127.0.0.1 not localhost on Windows.
localhost adds ~2050ms delay due to DNS resolution.

---

## Overall Summary

| Endpoint | Score | Status |
|----------|-------|--------|
| /categorise | 4.8/5 | ✓ PASS |
| /query | 5.0/5 | ✓ PASS |
| /generate-report | 10/10 | ✓ PASS |
| **Overall** | **All PASS** | **✓ COMPLETE** |

**Day 14 status: COMPLETE ✓**
**All prompts verified demo-ready against 30 seeded records.**