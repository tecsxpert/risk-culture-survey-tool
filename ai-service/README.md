# AI Risk Categorisation Service

## 📌 Overview
This project is a Flask-based API that categorizes risk-related text using an AI integration layer.

---

## 🚀 Features
- Input validation and sanitization
- Risk categorization endpoint (`/categorise`)
- Structured JSON response
- Fallback handling for AI failures

---

## 🛠️ Tech Stack
- Python
- Flask
- REST API

---

## 🔗 API Endpoint

### POST /categorise

#### Request:
```json
{
  "text": "There is high financial risk due to compliance failure"
}

### Response
{
  "category": "High Risk",
  "confidence": 0.85,
  "reasoning": "Mock response for development",
  "generated_at": "2026-04-25T10:00:00",
  "is_fallback": false
}

### How To Run
python app.py

