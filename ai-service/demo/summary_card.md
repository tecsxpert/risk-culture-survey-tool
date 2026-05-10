# Summary Card
## Risk Culture Survey Tool | Demo Day — 9 May 2026
**Developer:** AI Developer 2 | **Model:** LLaMA-3.3-70b via Groq

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.11 | AI service language |
| Framework | Flask 3.x | REST API on port 5000 |
| AI Model | Groq — LLaMA-3.3-70b | Free tier, no credit card |
| Vector DB | ChromaDB | Stores 30 knowledge documents |
| Embeddings | sentence-transformers | all-MiniLM-L6-v2 model |
| Cache | Redis 7 | 15 min TTL, 98% faster hits |
| Server | Gunicorn | Production WSGI server |

---

## 6 Endpoints

| # | Endpoint | Method | Purpose | Avg Time |
|---|----------|--------|---------|----------|
| 1 | /health | GET | Service health, uptime, cache stats | 15ms |
| 2 | /categorise | POST | Classifies survey text into 1 of 8 categories | 1132ms |
| 3 | /query | POST | RAG pipeline — answers questions from knowledge base | 1086ms |
| 4 | /generate-report | POST | Async report — returns job_id instantly | 32ms |
| 5 | /generate-report/<id> | GET | Poll job status and get completed report | 21ms |
| 6 | /generate-report/jobs | GET | List all report jobs with stats | 25ms |

---

## 8 Risk Culture Categories

---

## Key Features

| Feature | Detail |
|---------|--------|
| Redis Cache | 15 min TTL — 98% faster on cache hits |
| Fallback Service | Pre-written responses when Groq fails |
| Async Jobs | Report generation never blocks the user |
| Retry Logic | 3 retries with 2/4/8s backoff on Groq errors |
| Meta Object | Every response includes confidence, tokens, time |
| Offline Model | sentence-transformers cached locally — no network |

---

## Dry Run Results — 6 May 2026

| Endpoint | Fresh Call | Cache Hit | Status |
|----------|-----------|-----------|--------|
| GET /health | 15ms | — | PASS ✓ |
| POST /categorise | 1132ms | 32ms | PASS ✓ |
| POST /query | 1086ms | 22ms | PASS ✓ |
| POST /generate-report | 32ms (submit) | — | PASS ✓ |
| GET /generate-report/<id> | 21ms | — | PASS ✓ |
| GET /generate-report/jobs | 25ms | — | PASS ✓ |

**Final QA Scores:** /categorise 4.8/5 · /query 5.0/5 · /report 10/10

---

## Demo Day Setup

```bash
# 1. Start Redis
redis-server.exe

# 2. Seed ChromaDB (30 records)
python prompt_tuning/seed_30_records.py

# 3. Start Flask
python app.py

# 4. Verify
curl http://127.0.0.1:5000/health
```

> ⚠️ Use 127.0.0.1 not localhost on Windows

---

## GitHub Repository
**Link:** [Shared by mentor before Day 1]

**AI Service folder:** `ai-service/`

**Key files:**
- `routes/` — all 4 endpoint files
- `services/` — groq, chroma, cache, fallback, tracker
- `prompts/` — 3 prompt template files
- `benchmark/` — performance results
- `prompt_tuning/` — QA scripts and results