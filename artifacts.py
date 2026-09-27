import json
from datetime import datetime

def make_srs(project, requirements, sdlc):
    lines = [
        f"# Software Requirements Specification",
        f"## 1. Project",
        project["name"],
        f"## 2. Domain",
        project["domain"],
        "## 3. Scope",
        project["description"],
        "## 4. Requirements",
    ]
    for r in requirements:
        lines += [
            f"### {r['id']}",
            f"- Statement: {r['statement']}",
            f"- Category: {', '.join(r['category'])}",
            f"- Priority: {r['priority']}",
            f"- Risk: {r['risk_level']}",
            f"- Confidence: {r['confidence']}",
            f"- Acceptance criteria: {'; '.join(r['acceptance_criteria']) or 'Pending stakeholder definition'}"
        ]
    lines += [
        "## 5. SDLC",
        f"Recommended approach: {sdlc['recommendation']}",
        sdlc["explanation"],
        "## 6. Human Approval",
        "Regulatory interpretation, high-risk requirements and final SDLC adoption require authorized human approval."
    ]
    return "\n".join(lines)

def make_user_stories(requirements):
    out = ["# User Stories\n"]
    n = 1
    for r in requirements:
        if "Functional" in r["category"] or "Business" in r["category"]:
            out.append(f"## US-{n:03d}")
            out.append(f"As a financial-system stakeholder, I want {r['statement'].lower()} so that the business objective is achieved.")
            out.append("### Acceptance Criteria")
            for a in r["acceptance_criteria"]:
                out.append(f"- {a}")
            n += 1
    return "\n".join(out)

def make_rtm(requirements, compliance, risks):
    c_by = {x["requirement_id"]: x for x in compliance}
    r_by = {x["requirement_id"]: x for x in risks}
    lines = ["# Requirements Traceability Matrix\n",
             "| ID | Requirement | Category | Compliance Evidence | Risk | Approval |",
             "|---|---|---|---|---|---|"]
    for r in requirements:
        c = c_by.get(r["id"], {})
        risk = r_by.get(r["id"], {})
        lines.append(
            f"| {r['id']} | {r['statement'].replace('|','/')} | {', '.join(r['category'])} | "
            f"{', '.join(c.get('sources', [])) or 'None found'} | {risk.get('level', r['risk_level'])} | "
            f"{r['approval_status']} |"
        )
    return "\n".join(lines)

def make_compliance_matrix(compliance):
    lines = ["# Compliance Control Matrix\n",
             "| Requirement | Status | Sources | Confidence | Gap |",
             "|---|---|---|---|---|"]
    for c in compliance:
        lines.append(
            f"| {c['requirement_id']} | {c['status']} | {', '.join(c['sources']) or 'None'} | "
            f"{c['confidence']} | {c['gap']} |"
        )
    return "\n".join(lines)

def make_risk_register(risks):
    lines = ["# Risk Register\n", "| Requirement | Impact | Probability | Score | Level | Reason |",
             "|---|---:|---:|---:|---|---|"]
    for r in risks:
        lines.append(f"| {r['requirement_id']} | {r['impact']} | {r['probability']} | {r['score']} | {r['level']} | {r['reason']} |")
    return "\n".join(lines)

def make_acceptance(requirements):
    lines = ["# Acceptance Criteria\n"]
    for r in requirements:
        lines.append(f"## {r['id']}")
        for a in r["acceptance_criteria"] or ["Pending stakeholder definition"]:
            lines.append(f"- {a}")
    return "\n".join(lines)
