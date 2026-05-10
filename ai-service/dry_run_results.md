# Day 17 — AI Dry Run Results

**Date:** 6 May 2026  
**Time:** 17:23:43  
**Developer:** AI Developer 2  
**Purpose:** Verify all 6 endpoints live with real Groq API  
**Status:** COMPLETE ✓ — Ready for Demo Day!

---

## System Health at Dry Run

| Check | Value | Status |
|-------|-------|--------|
| Flask status | healthy | ✓ |
| ChromaDB docs | 30 | ✓ |
| Redis connected | True | ✓ |
| Groq API key | Loaded | ✓ |
| Model | llama-3.3-70b-versatile | ✓ |

---

## Endpoint Results

| Endpoint | Avg Response | Fallback | Status |
|----------|-------------|----------|--------|
| GET /health | 15ms | No | PASS ✓ |
| POST /categorise | 1132ms | No | PASS ✓ |
| POST /query | 1086ms | No | PASS ✓ |
| POST /generate-report (submit) | 32ms | No | PASS ✓ |
| GET /generate-report/<job_id> | 21ms | No | PASS ✓ |
| GET /generate-report/jobs | 25ms | No | PASS ✓ |

---

## Detailed Results

### ENDPOINT 1 — GET /health
| Run | Response Time |
|-----|--------------|
| Run 1 | 31ms |
| Run 2 | 8ms |
| Run 3 | 7ms |
| **Average** | **15ms** |

- Status: healthy
- Model: llama-3.3-70b-versatile
- ChromaDB docs: 30
- Redis connected: True

---

### ENDPOINT 2 — POST /categorise

**Input:** "Our senior management never discusses risk in team
meetings. There is no visible leadership commitment..."

| Field | Value |
|-------|-------|
| Category | Leadership & Governance |
| Confidence | 0.9 |
| Response time (fresh) | 1132ms |
| Response time (cache) | 32ms |
| is_fallback | False |
| tokens_used | 545 |
| from_cache (2nd call) | True |

---

### ENDPOINT 3 — POST /query (RAG Pipeline)

**Question:** "How does leadership behaviour affect risk culture
in an organisation?"

| Field | Value |
|-------|-------|
| Response time (fresh) | 1086ms |
| Response time (cache) | 22ms |
| Chunks used | 3 |
| is_fallback | False |
| tokens_used | 538 |
| from_cache (2nd call) | True |

**Sources retrieved:**
- [Leadership & Governance] score=0.1644
- [Leadership & Governance] score=0.3007
- [Culture & Behaviour] score=0.3131

**Answer preview:** "Leadership behaviour plays a crucial role
in shaping an organisation's risk culture. The tone from the
top..."

---

### ENDPOINT 4 — POST /generate-report (Async)

| Field | Value |
|-------|-------|
| Submit response time | 32ms |
| Job status returned | pending |
| Time to complete | 3 seconds |
| Total pipeline time | 3007ms |
| Top items | 3 |
| Recommendations | 3 |
| is_fallback | False |

**Report title:** "Risk Culture Assessment Report —
Demo Organisation — May 2026"

**Executive summary preview:** "The Demo Organisation's risk
culture health is concerning, with an overall score..."

---

### ENDPOINT 5 — GET /generate-report/<job_id> (Poll)

| Run | Response Time |
|-----|--------------|
| Run 1 | 17ms |
| Run 2 | 17ms |
| Run 3 | 29ms |
| **Average** | **21ms** |

- Job status: complete
- HTTP status: 200

---

### ENDPOINT 6 — GET /generate-report/jobs

| Field | Value |
|-------|-------|
| Response time | 25ms |
| Total jobs | 2 |
| Complete | 2 |
| Failed | 0 |
| Processing | 0 |

---

## Cache Performance

| Endpoint | Fresh Call | Cache Hit | Speed Improvement |
|----------|-----------|-----------|-------------------|
| POST /categorise | 1132ms | 32ms | 97% faster |
| POST /query | 1086ms | 22ms | 98% faster |

---

## Demo Day Talking Points

### What to say about each endpoint:

**GET /health:**
> "This shows our service is healthy — Groq key loaded,
> ChromaDB connected with 30 documents, Redis cache active."

**POST /categorise:**
> "We send a survey response and Groq classifies it into
> one of 8 risk culture categories with a confidence score.
> Fresh call takes 1132ms, cached response takes 32ms."

**POST /query (RAG):**
> "This is our RAG pipeline — we embed the question,
> retrieve the 3 most relevant documents from ChromaDB,
> inject them as context, and Groq answers using only
> our knowledge base. Not general AI knowledge."

**POST /generate-report:**
> "We submit survey data and get a job_id back in 32ms.
> The AI generates a full structured report in the background.
> The job completed in just 3 seconds."

**GET /generate-report/<job_id>:**
> "Polling the job returns the complete report — title,
> executive summary, top findings, and recommendations."

**GET /generate-report/jobs:**
> "This lists all report generation jobs with their status."

---

## Demo Day Checklist

- [x] All 6 endpoints returning correct responses
- [x] No is_fallback: true on any endpoint
- [x] Cache hits under 200ms (32ms and 22ms)
- [x] Generate report completes in under 30 seconds (3s)
- [x] ChromaDB has 30 demo records loaded
- [x] Redis connected and caching correctly
- [x] Groq API key valid and working
- [x] All meta fields present and correct

---

## Demo Day Setup Order

```bash
# 1. Start Redis
& "C:\Users\teja8\Downloads\Redis-x64-3.2.100\redis-server.exe"

# 2. Seed ChromaDB
python prompt_tuning/seed_30_records.py

# 3. Start Flask
python app.py

# 4. Verify system
python -c "import requests; print(requests.get('http://127.0.0.1:5000/health').json()['status'])"
```

**IMPORTANT:** Use 127.0.0.1 not localhost on Windows!

---

## Overall Status

**All 6 endpoints: PASS ✓**  
**Day 17 status: COMPLETE ✓ — Ready for Demo Day!**