from typing import Any, Optional
from pydantic import BaseModel, Field

class ProjectInput(BaseModel):
    name: str = "Untitled Financial Project"
    domain: str = "Digital Banking"
    description: str
    stakeholder: str = "Product Owner"

class Requirement(BaseModel):
    id: str
    statement: str
    category: list[str]
    priority: str
    source: str
    business_justification: str = ""
    dependencies: list[str] = []
    assumptions: list[str] = []
    acceptance_criteria: list[str] = []
    regulations: list[str] = []
    risk_level: str = "Medium"
    confidence: float = 0.75
    approval_status: str = "Pending"
    quality_flags: list[str] = []

class AnalysisResponse(BaseModel):
    project_id: str
    project: dict[str, Any]
    requirements: list[Requirement]
    quality_findings: list[dict[str, Any]]
    conflicts: list[dict[str, Any]]
    compliance: list[dict[str, Any]]
    security: list[dict[str, Any]]
    risks: list[dict[str, Any]]
    sdlc: dict[str, Any]
    artifacts: dict[str, Any]
    next_questions: list[str]
    evidence: list[dict[str, Any]]

class ApprovalRequest(BaseModel):
    requirement_id: str
    decision: str = Field(pattern="^(Approved|Rejected|Modified)$")
    comment: str = ""
