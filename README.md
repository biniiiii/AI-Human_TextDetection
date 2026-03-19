# AI-Generated Text Detection System

A full-stack web application that detects whether text is AI-generated or human-written, powered by fine-tuned BERT models.

## 🌐 Live Demo
- **Frontend:** https://ai-human-text-detection.vercel.app
- **Backend:** https://biniiiii-veritai-backend.hf.space

---

## 🛠️ Tech Stack

**Frontend**
- Next.js 16, TypeScript, Tailwind CSS
- Deployed on Vercel

**Backend**
- FastAPI, Python 3.11
- Deployed on Hugging Face Spaces (Docker)

**AI Models**
- Fine-tuned DistilBERT (`biniiiii/distilbert-ai-detection`)
- Fine-tuned ALBERT (`biniiiii/albert-ai-detection`)
- GPT-2 for perplexity scoring
- LIME for explainability

**Database**
- SQLite (via SQLAlchemy)

---

## ✨ Features

- Detects AI-generated vs Human-written text
- Confidence score and probability breakdown
- Perplexity scoring using GPT-2
- LIME word-level explainability
- Detection history with search and filter
- Multiple model support (DistilBERT & ALBERT)
- Feedback system

---

## 🚀 Running Locally

### Backend
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

---

## 🔧 Environment Variables

**Frontend (`frontend/.env.local`)**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (`backend/.env`)**
```
DEFAULT_MODEL_NAME=biniiiii/distilbert-ai-detection
ALBERT_MODEL_NAME=biniiiii/albert-ai-detection
```

---

## 🏫 About

Minor Project — Khwopa College of Engineering
Bachelor of Computer Engineering (BCT), 2079 Batch