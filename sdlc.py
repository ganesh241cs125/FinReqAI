MODELS = ["Agile", "DevSecOps", "V-Model", "Spiral", "Waterfall", "Hybrid"]

def extract_factors(requirements, project_description):
    text = " ".join(r["statement"] for r in requirements) + " " + project_description
    low = text.lower()
    return {
        "requirement_stability": 2 if any(x in low for x in ["change", "evolving", "frequent"]) else 4,
        "regulatory_criticality": 5 if any(x in low for x in ["regulatory","compliance","bank","financial"]) else 2,
        "security_risk": 5 if any(x in low for x in ["secure","authentication","fraud","payment","money"]) else 3,
        "complexity": 4 if len(requirements) >= 8 else 3,
        "continuous_delivery": 5 if any(x in low for x in ["continuous","deploy","release"]) else 2,
        "formal_verification": 4 if any(x in low for x in ["verification","validation","strict"]) else 2,
        "stakeholder_change": 4 if any(x in low for x in ["customer","stakeholder","feedback"]) else 3,
        "failure_impact": 5 if any(x in low for x in ["money","payment","bank","financial"]) else 2
    }

def score(f):
    s = {m: 0.0 for m in MODELS}
    # Transparent deterministic rules, not LLM-generated scores.
    s["Agile"] += f["stakeholder_change"] * 4 + (6-f["requirement_stability"]) * 5
    s["DevSecOps"] += f["security_risk"] * 6 + f["continuous_delivery"] * 5 + f["regulatory_criticality"] * 2
    s["V-Model"] += f["formal_verification"] * 7 + f["regulatory_criticality"] * 3
    s["Spiral"] += f["complexity"] * 4 + f["security_risk"] * 4 + (6-f["requirement_stability"]) * 4
    s["Waterfall"] += f["requirement_stability"] * 6 + f["formal_verification"] * 2
    s["Hybrid"] += f["regulatory_criticality"] * 4 + f["security_risk"] * 4 + (6-f["requirement_stability"]) * 3
    # Normalize to a human-readable 0-100 scale.
    max_possible = max(s.values()) or 1
    normalized = {k: round(v / max_possible * 100, 1) for k, v in s.items()}
    return dict(sorted(normalized.items(), key=lambda x: x[1], reverse=True))

def recommend(requirements, description):
    factors = extract_factors(requirements, description)
    scores = score(factors)
    primary = next(iter(scores))
    explanation = (
        f"{primary} receives the highest deterministic suitability score because "
        f"the project profile indicates security risk {factors['security_risk']}/5, "
        f"regulatory criticality {factors['regulatory_criticality']}/5, "
        f"requirement stability {factors['requirement_stability']}/5 and "
        f"continuous-delivery need {factors['continuous_delivery']}/5. "
        "The recommendation is advisory and requires authorized human approval."
    )
    workflow = workflow_for(primary)
    return {"factors": factors, "scores": scores, "recommendation": primary, "explanation": explanation, "workflow": workflow}

def workflow_for(model):
    common = [
        {"phase":"Requirements","activities":["Validate requirements","Classify requirements","Map evidence"],"gate":"Approved requirement baseline"},
        {"phase":"Design","activities":["Architecture design","Threat modelling","Compliance review"],"gate":"Design/security approval"},
        {"phase":"Implementation","activities":["Development","Code review","Static analysis"],"gate":"Build quality gate"},
        {"phase":"Verification","activities":["Functional tests","Security tests","Traceability checks"],"gate":"Test exit criteria"},
        {"phase":"Release","activities":["Compliance review","Human approval","Deployment"],"gate":"Production readiness approval"},
        {"phase":"Operations","activities":["Monitoring","Incident response","Requirement change management"],"gate":"Operational review"}
    ]
    if model == "Waterfall":
        common[0]["activities"].append("Formal baseline and sign-off")
    elif model == "V-Model":
        common[3]["activities"].append("Map every requirement to verification/validation tests")
    elif model == "Spiral":
        common.insert(2, {"phase":"Risk Cycle","activities":["Identify risks","Prototype risky components","Review mitigation"],"gate":"Risk acceptance"})
    elif model == "Agile":
        for x in common:
            x["activities"].append("Iterative backlog refinement")
    elif model == "DevSecOps":
        for x in common:
            x["activities"].append("Continuous security and compliance automation")
    else:
        for x in common:
            x["activities"].append("Use risk-based tailoring")
    return common
