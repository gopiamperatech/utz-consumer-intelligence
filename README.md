# Utz Consumer Intent Intelligence Prototype

Full-stack demo prototype for converting consumer conversations into measurable marketing and retail actions.

## Stack
- Frontend: React + Vite + Recharts
- Backend: FastAPI + SQLite
- Optional LLM: Azure OpenAI or OpenAI-compatible endpoint
- Optional Vector DB: scaffold notes included in backend comments for FAISS integration

## Project Structure
- `frontend/` React app
- `backend/` FastAPI API and SQLite seed pipeline

## Quick Start

### 1) Backend
```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend defaults to `http://localhost:5173` and calls backend at `http://localhost:8000`.

## Environment
Create `backend/.env` from `.env.example` if you want live LLM summaries.

## Demo APIs
- `GET /health`
- `GET /queries`
- `GET /insights/summary`
- `GET /insights/gaps`
- `GET /actions/recommendations`
- `POST /copilot/ask`
- `GET /products`
- `GET /retailers/availability`

## Suggested Next Enhancements
- Add FAISS embeddings for semantic retrieval over reviews and FAQ content
- Add upload endpoints for first-party data drops
- Add auth and role-based views
- Add retailer, SKU, and geography drilldowns
- Add LangChain or direct Responses API orchestration for richer agent workflows
