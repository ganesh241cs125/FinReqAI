import re
from .common import LLM

def extract_requirements(description: str):
    system = """You are a software requirements engineer for financial systems.
Extract requirements only from the supplied text. Return JSON:
{"requirements":[{"statement":"","category":[],"priority":"","source":"","business_justification":"","acceptance_criteria":[],"confidence":0.0}]}
Do not invent regulations."""
    fallback = rule_extract(description)
    result = LLM.json(system, description, fallback)
    requirements = result.get("requirements", fallback["requirements"])
    for i, r in enumerate(requirements, 1):
        r.setdefault("id", f"REQ-{i:03d}")
        r.setdefault("category", ["Functional"])
        r.setdefault("priority", "Medium")
        r.setdefault("source", "Project Description")
        r.setdefault("business_justification", "")
        r.setdefault("acceptance_criteria", [])
        r.setdefault("confidence", 0.75)
    return requirements

def rule_extract(text):
    sentences = [s.strip() for s in re.split(r'[\n.;]+', text) if len(s.strip()) > 12]
    reqs = []
    for s in sentences:
        low = s.lower()
        if any(k in low for k in [
            "want to", "should", "shall", "must", "allow", "customer",
            "user", "application", "system", "able to", "require"
        ]):
            category = ["Functional"]
            if any(k in low for k in ["secure", "authentication", "encrypt", "password", "fraud"]):
                category += ["Security"]
            if any(k in low for k in ["privacy", "personal data", "customer data"]):
                category += ["Privacy"]
            if any(k in low for k in ["fast", "seconds", "performance", "response"]):
                category += ["Performance"]
            if any(k in low for k in ["24/7", "available", "availability", "uptime"]):
                category += ["Availability"]
            priority = "High" if any(k in low for k in ["money", "transfer", "authentication", "secure"]) else "Medium"
            reqs.append({
                "statement": s,
                "category": list(dict.fromkeys(category)),
                "priority": priority,
                "source": "Project Description",
                "business_justification": "Supports the stated project objective.",
                "acceptance_criteria": [f"The requirement can be verified against: {s}"],
                "confidence": 0.82
            })
    if not reqs:
        reqs = [{
            "statement": text.strip(),
            "category": ["Business"],
            "priority": "Medium",
            "source": "Project Description",
            "business_justification": "Needs stakeholder refinement.",
            "acceptance_criteria": [],
            "confidence": 0.55
        }]
    return {"requirements": reqs}

# injected singleton
