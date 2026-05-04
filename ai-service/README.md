# AI Service — Risk Culture Survey Tool

Flask-based AI microservice providing intelligent analysis
of risk culture survey data using Groq LLaMA-3.3-70b.

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Language |
| Flask 3.x | Web framework |
| Groq API (LLaMA-3.3-70b) | AI model — free tier |
| ChromaDB | Vector database for RAG pipeline |
| sentence-transformers | Text embeddings (all-MiniLM-L6-v2) |
| Redis 7 | AI response cache (15 min TTL) |
| flask-limiter | Rate limiting (30 req/min) |

---

## Prerequisites

- Python 3.11+
- Redis 7 (running on port 6379)
- Groq API key (free at console.groq.com)

---

## Setup

### Step 1 — Clone and navigate
```bash
cd ai-service
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Configure environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Step 4 — Download AI model (first time only)
```bash
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models')
print('Model ready')
"
```

### Step 5 — Seed ChromaDB with demo data
```bash
python prompt_tuning/seed_30_records.py
```

### Step 6 — Start Redis
```bash
# Linux/Mac
redis-server

# Windows
redis-server.exe
```

### Step 7 — Start the service
```bash
python app.py
```

Service runs on: http://localhost:5000

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GROQ_API_KEY | Yes | — | Groq API key from console.groq.com |
| CHROMA_PATH | No | ./chroma_data | ChromaDB storage path |
| CHROMA_COLLECTION | No | risk_culture_docs | Collection name |
| REDIS_HOST | No | localhost | Redis host |
| REDIS_PORT | No | 6379 | Redis port |
| REDIS_DB | No | 0 | Redis database number |
| TRANSFORMERS_OFFLINE | No | 1 | Prevent HuggingFace network calls |
| SENTENCE_TRANSFORMERS_HOME | No | ./models | Model cache path |

---

## API Endpoints

### GET /health
Returns service health status.

**Response:**
```json
{
  "status": "healthy",
  "uptime": { "seconds": 120, "human": "0h 2m 0s" },
  "groq": {
    "model": "llama-3.3-70b-versatile",
    "key_loaded": true,
    "avg_response_time_ms": 1204.5,
    "response_times_tracked": 10
  },
  "chromadb": { "status": "connected", "doc_count": 30 },
  "cache": {
    "hits": 45, "misses": 12,
    "hit_rate_pct": 78.9,
    "redis_connected": true
  }
}
```

---

### POST /categorise
Classifies survey response into a risk culture category.

**Request:**
```json
{
  "text": "Our senior management never discusses risk in meetings.",
  "skip_cache": false
}
```

**Response:**
```json
{
  "category": "Leadership & Governance",
  "confidence": 0.9,
  "reasoning": "The response describes a lack of visible risk commitment from senior leadership...",
  "generated_at": "2026-05-03T10:00:00+00:00",
  "from_cache": false,
  "meta": {
    "confidence": 0.9,
    "model_used": "llama-3.3-70b-versatile",
    "tokens_used": 487,
    "response_time_ms": 1204,
    "cached": false,
    "is_fallback": false
  }
}
```

**Categories:**
- Leadership & Governance
- Risk Awareness
- Communication & Reporting
- Accountability
- Training & Competency
- Policies & Procedures
- Incident & Near Miss
- Culture & Behaviour

---

### POST /query
RAG pipeline — answers questions using knowledge base.

**Request:**
```json
{
  "question": "How does leadership behaviour affect risk culture?",
  "skip_cache": false
}
```

**Response:**
```json
{
  "answer": "Leadership behaviour is the single most important driver of risk culture...",
  "sources": [
    {
      "id": "demo_001",
      "category": "Leadership & Governance",
      "source": "demo_records",
      "score": 0.1823,
      "preview": "The board of directors plays a critical role..."
    }
  ],
  "chunks_used": 3,
  "generated_at": "2026-05-03T10:00:00+00:00",
  "from_cache": false,
  "meta": {
    "confidence": 1.0,
    "model_used": "llama-3.3-70b-versatile",
    "tokens_used": 512,
    "response_time_ms": 1456,
    "cached": false,
    "is_fallback": false
  }
}
```

---

### POST /generate-report
Async report generation — returns job_id immediately.

**Request:**
```json
{
  "survey_data": "Survey results: 47 respondents...",
  "webhook_url": "https://your-app.com/webhook"
}
```

**Response (202 Accepted):**
```json
{
  "job_id": "a3f9b2c1-...",
  "status": "pending",
  "message": "Report generation started. Poll the status URL.",
  "poll_url": "/generate-report/a3f9b2c1-...",
  "created_at": "2026-05-03T10:00:00+00:00"
}
```

---

### GET /generate-report/{job_id}
Poll for report status and result.

**Response when complete:**
```json
{
  "job_id": "a3f9b2c1-...",
  "status": "complete",
  "created_at": "2026-05-03T10:00:00+00:00",
  "completed_at": "2026-05-03T10:00:12+00:00",
  "result": {
    "report": {
      "title": "Risk Culture Assessment Report — May 2026",
      "executive_summary": "The organisation demonstrates...",
      "overview": "Key patterns observed across...",
      "top_items": [...],
      "recommendations": [...]
    },
    "meta": { "is_fallback": false, ... }
  }
}
```

---

### GET /generate-report/jobs
List all report generation jobs.

---

## Docker

### Build
```bash
docker build -t risk-culture-ai .
```

### Run
```bash
docker run -p 5000:5000 \
  -e GROQ_API_KEY=your_key_here \
  -e REDIS_HOST=redis \
  risk-culture-ai
```

---

## Project Structure