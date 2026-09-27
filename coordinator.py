import uuid
from datetime import datetime, timezone
from .extraction import extract_requirements
from .classification import classify
from .quality import analyze_quality, detect_conflicts, clarification_questions
from .compliance import analyze_compliance
from .security import analyze_security
from .risk import analyze_risk
from ..rules.sdlc import recommend
from ..services.artifacts import (
    make_srs, make_user_stories, make_rtm, make_compliance_matrix,
    make_risk_register, make_acceptance
)
from ..rag.retriever import LocalRAG
from ..db import database as db

rag = LocalRAG()

def analyze_project(payload):
    project_id = str(uuid.uuid4())
    created = datetime.now(timezone.utc).isoformat()
    project = {
        "id": project_id,
        "name": payload.name,
        "domain": payload.domain,
        "description": payload.description,
        "stakeholder": payload.stakeholder,
        "created_at": created
    }

    raw = extract_requirements(payload.description)
    requirements = classify(raw)
    for i, r in enumerate(requirements, 1):
        r["id"] = r.get("id") or f"REQ-{i:03d}"
        r.setdefault("approval_status", "Pending")
        r.setdefault("risk_level", "Medium")
        r.setdefault("regulations", [])
        r.setdefault("quality_flags", [])

    quality = analyze_quality(requirements)
    conflicts = detect_conflicts(requirements)
    compliance, evidence = analyze_compliance(requirements, rag)
    security = analyze_security(requirements)
    risks = analyze_risk(requirements)
    sdlc = recommend(requirements, payload.description)

    artifacts = {
        "srs": make_srs(project, requirements, sdlc),
        "user_stories": make_user_stories(requirements),
        "acceptance_criteria": make_acceptance(requirements),
        "traceability_matrix": make_rtm(requirements, compliance, risks),
        "compliance_matrix": make_compliance_matrix(compliance),
        "risk_register": make_risk_register(risks)
    }

    db.save_project(project)
    db.save_requirements(project_id, requirements)
    for k, v in artifacts.items():
        db.save_artifact(project_id, k, v, created)
    db.save_audit(project_id, "system", "project_analyzed", {
        "requirements": len(requirements),
        "conflicts": len(conflicts),
        "quality_findings": len(quality),
        "sdlc": sdlc["recommendation"]
    }, created)

    return {
        "project_id": project_id,
        "project": project,
        "requirements": requirements,
        "quality_findings": quality,
        "conflicts": conflicts,
        "compliance": compliance,
        "security": security,
        "risks": risks,
        "sdlc": sdlc,
        "artifacts": artifacts,
        "next_questions": clarification_questions(requirements, quality),
        "evidence": evidence
    }
