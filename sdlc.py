import re

MODELS = [
    "Waterfall",
    "Iterative Waterfall",
    "V-Model",
    "Prototype",
    "Incremental",
    "Spiral",
    "RAD",
    "Agile"
]


def extract_factors(requirements, project_description):
    text = " ".join(
        r.get("statement", "") for r in requirements
    ) + " " + project_description

    low = re.sub(r"\s+", " ", text.lower())

    def has(*phrases):
        return any(phrase in low for phrase in phrases)

    # Stable requirements must take priority over generic words
    # such as "change" appearing in negative sentences.
    stable = has(
        "requirements are stable",
        "stable requirements",
        "not expected to change",
        "not expected to change during development",
        "will not change",
        "unlikely to change",
        "fixed requirements",
        "requirements are clearly defined",
        "requirements are well defined"
    )

    changing = has(
        "requirements change frequently",
        "frequently changing requirements",
        "frequent requirement changes",
        "evolving requirements",
        "changing requirements",
        "requirements are uncertain",
        "continuously changing",
        "changing customer needs"
    )

    if stable:
        stability = 5
    elif changing:
        stability = 2
    else:
        stability = 3

    # Explicit security threats, not ordinary payment functionality.
    security = (
        5 if has(
            "cybersecurity threats",
            "security threats",
            "high security risk",
            "fraud prevention",
            "fraud detection",
            "data breach",
            "sensitive personal data",
            "unauthorized access",
            "security vulnerabilities",
            "cyber attacks",
            "malicious attacks"
        )
        else 3 if has(
            "authentication",
            "data protection",
            "secure access",
            "encryption"
        )
        else 2
    )

    # High failure impact must be explicitly indicated.
    failure = (
        5 if has(
            "high financial risk",
            "serious consequences",
            "life critical",
            "mission critical",
            "safety critical",
            "loss of life",
            "critical financial transactions",
            "major financial loss"
        )
        else 3 if has(
            "banking system",
            "online banking",
            "financial transactions"
        )
        else 2
    )

    regulatory = (
        5 if has(
            "regulatory requirements",
            "regulatory compliance",
            "strict compliance",
            "financial regulations",
            "healthcare regulations",
            "medical regulations",
            "audit requirements",
            "legal compliance"
        )
        else 3 if has(
            "healthcare",
            "medical",
            "banking"
        )
        else 2
    )

    complexity = (
        5 if has(
            "large-scale",
            "highly complex",
            "complex integrations",
            "multiple external systems",
            "distributed architecture",
            "complex system"
        )
        else 4 if len(requirements) >= 10
        else 3
    )

    continuous = (
        5 if has(
            "continuous delivery",
            "continuous deployment",
            "frequent releases",
            "regular releases",
            "multiple releases",
            "short sprints",
            "regular updates"
        )
        else 2
    )

    verification = (
        5 if has(
            "strict verification",
            "strict validation",
            "verification and validation",
            "mandatory testing",
            "strict testing",
            "formal testing",
            "safety critical",
            "test every requirement"
        )
        else 2
    )

    stakeholder = (
        5 if has(
            "frequent customer feedback",
            "continuous user feedback",
            "stakeholder feedback",
            "frequent feedback",
            "sprint review",
            "changing customer needs",
            "regular user feedback"
        )
        else 2
    )

    prototype = (
        5 if has(
            "unclear requirements",
            "uncertain requirements",
            "unsure about",
            "unclear user interface",
            "uncertain workflow",
            "initial prototype",
            "working prototype",
            "experiment with different designs",
            "test different designs",
            "initial working model",
            "user interface requirements are unclear"
        )
        else 2
    )

    modular = (
        5 if has(
            "multiple releases",
            "independent modules",
            "independently",
            "phased delivery",
            "module by module",
            "increment by increment",
            "gradually building",
            "staged delivery",
            "separate releases",
            "deliver each module",
            "deliver modules independently"
        )
        else 2
    )

    time_pressure = (
        5 if has(
            "short deadline",
            "limited time",
            "rapid development",
            "six weeks",
            "quick delivery",
            "tight deadline",
            "within a few weeks"
        )
        else 2
    )

    planned_refinement = (
        5 if has(
            "planned revisions",
            "limited revisions",
            "review previous phases",
            "refine previous phases",
            "feedback after each phase",
            "revisit previous phases",
            "iterative phase reviews"
        )
        else 2
    )

    return {
        "requirement_stability": stability,
        "regulatory_criticality": regulatory,
        "security_risk": security,
        "complexity": complexity,
        "continuous_delivery": continuous,
        "formal_verification": verification,
        "stakeholder_change": stakeholder,
        "failure_impact": failure,
        "prototype_need": prototype,
        "modular_delivery": modular,
        "time_pressure": time_pressure,
        "planned_refinement": planned_refinement
    }
def score(f):
    s = {model: 0.0 for model in MODELS}

    stability = f["requirement_stability"]
    formal = f["formal_verification"]
    risk = f["security_risk"]
    failure = f["failure_impact"]
    complexity = f["complexity"]
    stakeholder = f["stakeholder_change"]
    prototype = f["prototype_need"]
    modular = f["modular_delivery"]
    continuous = f["continuous_delivery"]
    time = f["time_pressure"]
    regulatory = f["regulatory_criticality"]
    refinement = f["planned_refinement"]

    # 1. Waterfall: stable and clearly defined requirements
    s["Waterfall"] = (
        stability * 7
        + formal * 1
    )

    # 2. Iterative Waterfall: sequential phases with planned revisions
    s["Iterative Waterfall"] = (
        stability * 4
        + formal * 2
        + complexity * 1
        + refinement * 4
    )

    # 3. V-Model: strict verification and validation
    s["V-Model"] = (
        formal * 8
        + regulatory * 2
        + failure * 2
    )

    # 4. Prototype: unclear requirements and experimental design
    s["Prototype"] = (
        prototype * 8
        + stakeholder * 3
        + (6 - stability) * 2
    )

    # 5. Incremental: independent modules and phased releases
    s["Incremental"] = (
        modular * 9
        + continuous * 2
        + complexity * 1
    )

    # 6. Spiral: explicitly high risk and uncertainty
    s["Spiral"] = (
        failure * 5
        + risk * 4
        + complexity * 2
        + (6 - stability) * 2
    )

    # 7. RAD: short timelines and rapid development
    s["RAD"] = (
        time * 8
        + prototype * 2
        + modular * 2
    )

    # 8. Agile: frequent changes and continuous feedback
    s["Agile"] = (
        stakeholder * 6
        + (6 - stability) * 4
        + continuous * 2
    )

    # Normalize all scores to 0-100.
    max_possible = max(s.values()) or 1

    normalized = {
        model: round(value / max_possible * 100, 1)
        for model, value in s.items()
    }

    return dict(
        sorted(
            normalized.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

def recommend(requirements, description):
    factors = extract_factors(requirements, description)
    scores = score(factors)

    primary = next(iter(scores))

    explanation = (
        f"{primary} receives the highest deterministic suitability "
        f"score based on the project's requirements, risk, complexity, "
        f"verification needs, delivery approach and stakeholder involvement. "
        f"Security risk: {factors['security_risk']}/5, "
        f"regulatory criticality: {factors['regulatory_criticality']}/5, "
        f"requirement stability: {factors['requirement_stability']}/5. "
        "This recommendation is advisory and requires human approval."
    )

    workflow = workflow_for(primary)

    return {
        "factors": factors,
        "scores": scores,
        "recommendation": primary,
        "explanation": explanation,
        "workflow": workflow
    }


def workflow_for(model):
    workflows = {
        "Waterfall": [
            "Requirements gathering and formal sign-off",
            "System and architecture design",
            "Implementation",
            "Integration and testing",
            "Deployment",
            "Maintenance"
        ],

        "Iterative Waterfall": [
            "Requirements analysis",
            "Initial system design",
            "Implementation",
            "Testing and evaluation",
            "Review and refine previous phases",
            "Final deployment and maintenance"
        ],

        "V-Model": [
            "Requirements analysis",
            "System and architectural design",
            "Module and detailed design",
            "Implementation",
            "Unit testing",
            "Integration and system testing",
            "Acceptance testing and validation"
        ],

        "Prototype": [
            "Initial requirement gathering",
            "Build an initial prototype",
            "Collect user feedback",
            "Refine prototype",
            "Finalize requirements",
            "Develop and test the final system",
            "Deployment"
        ],

        "Incremental": [
            "Identify system requirements",
            "Divide system into increments",
            "Design first increment",
            "Implement and test increment",
            "Deliver working increment",
            "Repeat for remaining increments",
            "Integrate complete system"
        ],

        "Spiral": [
            "Determine objectives and alternatives",
            "Identify and analyze risks",
            "Develop and test a prototype",
            "Evaluate results with stakeholders",
            "Plan the next spiral cycle",
            "Repeat until system completion",
            "Final deployment"
        ],

        "RAD": [
            "Requirements planning",
            "User design and prototyping",
            "Rapid application development",
            "Continuous user feedback",
            "Testing and integration",
            "Deployment"
        ],

        "Agile": [
            "Create and prioritize product backlog",
            "Sprint planning",
            "Design and development",
            "Continuous testing",
            "Sprint review and stakeholder feedback",
            "Sprint retrospective",
            "Repeat and release working software"
        ]
    }

    return [
        {
            "phase": f"Phase {index + 1}",
            "activities": [activity],
            "gate": "Review and approval"
        }
        for index, activity in enumerate(
            workflows.get(model, workflows["Waterfall"])
        )
    ]
