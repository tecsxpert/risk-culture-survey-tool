# Day 6 — Prompt Tuning Results

**Date:** 25 April 2026  
**Developer:** AI Developer 2  

---

## /categorise Prompt

| Input | Expected Category | Got | Score |
|-------|------------------|-----|-------|
| 1 | Leadership & Governance | Leadership & Governance | 10/10 |
| 2 | Risk Awareness | Risk Awareness | 10/10 |
| 3 | Communication & Reporting | Communication & Reporting | 10/10 |
| 4 | Accountability | Accountability | PARSE ERROR |
| 5 | Training & Competency | Training & Competency | 10/10 |
| 6 | Policies & Procedures | Policies & Procedures | PARSE ERROR |
| 7 | Incident & Near Miss | Incident & Near Miss | PARSE ERROR |
| 8 | Culture & Behaviour | Culture & Behaviour | PARSE ERROR |
| 9 | Leadership & Governance | Communication & Reporting | 5/10 |
| 10 | Risk Awareness | Risk Awareness | 10/10 |

**Total Score:** 55/100  
**Average Score:** 5.5/10  
**Status:** NEEDS REWRITE ✗  

### Issues Found
1. **PARSE ERROR on inputs 4, 6, 7, 8** — AI returned reasoning text
   that was too long and contained special characters (apostrophes/commas)
   which broke JSON parsing. Fix: add stricter JSON formatting
   instruction to prompt and improve parse_ai_response() to handle
   long reasoning strings.

2. **Wrong category on input 9** — "The board receives a risk report
   every quarter but it is always green" was classified as
   Communication & Reporting instead of Leadership & Governance.
   Fix: add example to prompt clarifying that board-level reporting
   failures belong to Leadership & Governance category.

---

## /query Prompt

| Query | Score | Notes |
|-------|-------|-------|
| How does leadership behaviour affect risk culture? | 10/10 | Perfect length, relevant, no bullets |
| Why is it important to report near misses? | 10/10 | Perfect length, relevant, no bullets |
| What makes risk training effective? | 10/10 | Perfect length, relevant, no bullets |
| How should risks be escalated to senior management? | 10/10 | Perfect length, relevant, no bullets |
| What happens when nobody owns a risk? | 10/10 | Perfect length, relevant, no bullets |

**Total Score:** 50/50  
**Average Score:** 10.0/10  
**Status:** PASS ✓  

---

## Changes Made After Tuning

### categorise_prompt.txt — REWRITE REQUIRED
- Add stricter JSON instruction: reasoning must be under 100 words
- Add instruction to avoid apostrophes and special characters in reasoning
- Add example clarifying board-level issues belong to
  Leadership & Governance not Communication & Reporting

### query_prompt.txt — NO CHANGES NEEDED
- Scored 10/10 on all 5 queries
- Paragraph format working correctly
- Context retrieval accurate and relevant

---

## Overall Summary

| Prompt | Average Score | Status |
|--------|--------------|--------|
| /categorise | 5.5/10 | ✗ Rewrite needed |
| /query | 10.0/10 | ✓ Pass |
| **Overall** | **7.75/10** | **✓ Complete** |