# Day 10 — Week 2 AI Quality Review Results

**Date:** 30 April 2026
**Developer:** AI Developer 2
**Target:** Average score >= 4/5 per endpoint

---

## /categorise — 10 Fresh Inputs

| Input | Expected Category | Got | Score |
|-------|------------------|-----|-------|
| 1 | Leadership & Governance | Leadership & Governance | 5/5 |
| 2 | Risk Awareness | Risk Awareness | 5/5 |
| 3 | Communication & Reporting | Communication & Reporting | 5/5 |
| 4 | Accountability | Accountability | 5/5 |
| 5 | Training & Competency | Training & Competency | 5/5 |
| 6 | Policies & Procedures | Policies & Procedures | 5/5 |
| 7 | Incident & Near Miss | Incident & Near Miss | 5/5 |
| 8 | Culture & Behaviour | Culture & Behaviour | 5/5 |
| 9 | Leadership & Governance | Communication & Reporting | 3/5 |
| 10 | Risk Awareness | Risk Awareness | 5/5 |

**Total Score:** 48/50
**Average Score:** 4.8/5
**Status:** PASS ✓

### Issue Found — Input 9
- Text: "The board approved a new risk appetite statement last year
  but it has never been communicated to staff below director level."
- AI classified as Communication & Reporting instead of
  Leadership & Governance
- Root cause: The sentence mentions "communicated" which triggers
  the Communication category even though the failure is a
  board-level governance issue
- Fix planned: Add clarifying example to categorise_prompt.txt
  in Day 14 final QA

---

## /query — 10 Fresh Inputs

| Query | Score | Notes |
|-------|-------|-------|
| What is the role of the board in risk culture? | 5/5 | 91 words, 3 sources |
| How can organisations improve incident reporting rates? | 5/5 | 93 words, 3 sources |
| What are the signs of poor risk accountability? | 5/5 | 75 words, 3 sources |
| How should risk appetite be communicated to staff? | 5/5 | 85 words, 3 sources |
| What makes a risk training programme effective? | 5/5 | 95 words, 3 sources |
| How does peer behaviour influence individual risk decisions? | 5/5 | 117 words, 3 sources |
| What is the difference between risk culture and compliance? | 5/5 | 104 words, 3 sources |
| How can managers encourage staff to speak up about risks? | 5/5 | 100 words, 3 sources |
| What are common barriers to good risk communication? | 5/5 | 87 words, 3 sources |
| How do you measure improvement in risk culture over time? | 5/5 | 98 words, 3 sources |

**Total Score:** 50/50
**Average Score:** 5.0/5
**Status:** PASS ✓

---

## Changes Made This Week
- categorise_prompt.txt: Added confidence range guide and
  richer category descriptions (Day 6)
- query_prompt.txt: Added paragraph format instruction and
  stronger context-only rules (Day 6)
- Both prompts significantly improved from initial versions

---

## Overall Summary

| Endpoint | Total | Avg Score | Status |
|----------|-------|-----------|--------|
| /categorise | 48/50 | 4.8/5 | ✓ PASS |
| /query | 50/50 | 5.0/5 | ✓ PASS |
| **Overall** | **98/100** | **4.9/5** | **✓ COMPLETE** |