# FinReqAI

Agentic AI system for financial-sector requirements engineering and SDLC recommendation.

## What it does

FinReqAI accepts a financial project description and can:

1. Extract structured functional/non-functional requirements.
2. Classify requirements across business, functional, security, privacy, compliance, performance, availability, data, integration and audit dimensions.
3. Detect ambiguity, incompleteness, duplicates and conflicts.
4. Retrieve evidence from a local financial knowledge base (RAG).
5. Perform compliance and security analysis.
6. Assign risk levels.
7. Route important decisions for human approval.
8. Recommend an SDLC using deterministic multi-criteria scoring plus an LLM explanation when configured.
9. Generate SRS, user stories, acceptance criteria, risk register, compliance matrix and requirements traceability data.
10. Keep an audit trail.

## Architecture

```text
React UI
   |
FastAPI
   |
Coordinator
   +-- Requirement Extraction
   +-- Classification
   +-- Clarification / Quality
   +-- Conflict Detection
   +-- Compliance + RAG
   +-- Security
   +-- Risk
   +-- Human Approval
   +-- SDLC Engine
   +-- Documentation
   |
SQLite + Local RAG Index
```

## Important

This is a college-project prototype. It is NOT a legal compliance system and must not be used to make real regulatory decisions. Compliance findings are evidence-based suggestions and require human review.

## Requirements

- Python 3.11+
- Node.js 20+
- Optional: OpenAI API key

The application also works in DEMO mode without an API key. Demo mode uses deterministic extraction/classification rules so you can run and demonstrate the workflow.

## Backend setup

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt

copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS

uvicorn app.main:app --reload --port 8000
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally:

http://localhost:5173

The frontend expects the backend at `http://localhost:8000`.

## Optional OpenAI mode

Edit `backend/.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5.6
```

If the selected model is unavailable to your account, use another model available to you.

## Quick demo

Paste:

```text
We want to build a mobile banking application. Customers should be able
to log in, view account balances, add beneficiaries, transfer money,
download transaction history and receive transaction notifications.
High-value transactions should require additional authentication.
The application should be secure, highly available and fast.
```

Then click **Analyze Project**.

You should see:
- requirements
- categories
- quality findings
- compliance evidence
- security findings
- risk levels
- SDLC scores
- generated artifacts
- traceability

## Knowledge base

Place approved reference documents in:

```text
backend/knowledge_base/
```

The included sample files are synthetic demonstration policies. Do not represent them as actual regulations.

Supported uploads:
- PDF
- DOCX
- TXT
- MD

## API

- `GET /api/health`
- `POST /api/projects/analyze`
- `GET /api/projects`
- `GET /api/projects/{project_id}`
- `POST /api/projects/{project_id}/approve`
- `POST /api/projects/{project_id}/documents`
- `GET /api/projects/{project_id}/artifact/{artifact_type}`
- `GET /api/projects/{project_id}/audit`

## Project structure

```text
FinReqAI/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── rag/
│   │   ├── rules/
│   │   ├── db/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── knowledge_base/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── sample_data/
├── docs/
└── README.md
```

## Suggested academic contribution

For your report, describe the system as:

**"An Agentic AI-based financial requirements engineering assistant combining structured requirement analysis, retrieval-grounded compliance evidence, deterministic SDLC multi-criteria decision analysis, and human-in-the-loop approval."**

Do not claim that an LLM alone guarantees compliance or SDLC correctness.
