from datetime import datetime, timezone
from pathlib import Path
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from .config import FRONTEND_ORIGIN, KB_DIR
from .db.database import init_db, list_projects, get_requirements, get_artifact, get_audits, save_approval, save_audit
from .models.schemas import ProjectInput, ApprovalRequest
from .agents.coordinator import analyze_project, rag

app = FastAPI(title="FinReqAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    rag.rebuild()

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "rag_documents": len(rag.chunks),
        "llm_mode": "OpenAI" if __import__("app.agents.common", fromlist=["LLM"]).LLM.enabled else "Demo"
    }

@app.post("/api/projects/analyze")
def analyze(payload: ProjectInput):
    return analyze_project(payload)

@app.get("/api/projects")
def projects():
    return list_projects()

@app.get("/api/projects/{project_id}/requirements")
def requirements(project_id: str):
    return get_requirements(project_id)

@app.get("/api/projects/{project_id}/artifact/{artifact_type}", response_class=PlainTextResponse)
def artifact(project_id: str, artifact_type: str):
    content = get_artifact(project_id, artifact_type)
    if content is None:
        raise HTTPException(404, "Artifact not found")
    return content

@app.get("/api/projects/{project_id}/audit")
def audit(project_id: str):
    return get_audits(project_id)

@app.post("/api/projects/{project_id}/approve")
def approve(project_id: str, request: ApprovalRequest):
    now = datetime.now(timezone.utc).isoformat()
    save_approval(project_id, request.requirement_id, request.decision, request.comment, now)
    # In this prototype, approval is also an auditable event. A production system should
    # enforce authorization and update the requirement transactionally.
    save_audit(project_id, "human-reviewer", "requirement_approval", request.model_dump(), now)
    return {"status": "recorded", "message": "Human approval event recorded."}

@app.post("/api/knowledge/upload")
async def upload_knowledge(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in {".pdf", ".docx", ".txt", ".md"}:
        raise HTTPException(400, "Only PDF, DOCX, TXT and MD are supported.")
    safe = Path(file.filename).name
    destination = KB_DIR / safe
    destination.write_bytes(await file.read())
    rag.rebuild()
    return {"status": "uploaded", "filename": safe, "chunks": len(rag.chunks)}
