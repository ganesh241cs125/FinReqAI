import re
from .common import LLM

VAGUE = ["fast", "user-friendly", "secure", "easy", "efficient", "soon", "appropriate", "adequate", "robust"]

def analyze_quality(requirements):
    findings = []
    for r in requirements:
        low = r["statement"].lower()
        flags = []
        for word in VAGUE:
            if re.search(r"\b" + re.escape(word) + r"\b", low):
                flags.append(f"Ambiguous term: {word}")
        if len(r["statement"].split()) < 5:
            flags.append("Possibly incomplete requirement")
        if not r.get("acceptance_criteria"):
            flags.append("Missing acceptance criteria")
        r["quality_flags"] = flags
        if flags:
            findings.append({
                "requirement_id": r["id"],
                "severity": "Medium" if len(flags) < 2 else "High",
                "flags": flags,
                "recommendation": "Ask the stakeholder for measurable and testable details."
            })

    # duplicate / near duplicate check
    for i in range(len(requirements)):
        for j in range(i+1, len(requirements)):
            a = set(requirements[i]["statement"].lower().split())
            b = set(requirements[j]["statement"].lower().split())
            if a and b:
                overlap = len(a & b) / max(1, len(a | b))
                if overlap >= 0.65:
                    findings.append({
                        "requirement_id": requirements[j]["id"],
                        "severity": "Medium",
                        "flags": [f"Potential duplicate of {requirements[i]['id']}"],
                        "recommendation": "Review whether the requirements should be merged."
                    })
    return findings

def detect_conflicts(requirements):
    conflicts = []
    positives = [
        ("require", "otp"), ("must", "authentication"), ("should", "authentication")
    ]
    for i in range(len(requirements)):
        for j in range(i+1, len(requirements)):
            a = requirements[i]["statement"].lower()
            b = requirements[j]["statement"].lower()
            neg_a = any(x in a for x in ["never", "must not", "should not", "without"])
            neg_b = any(x in b for x in ["never", "must not", "should not", "without"])
            shared = set(a.split()) & set(b.split())
            security_terms = {"otp","authentication","password","encrypt","verification"}
            if shared & security_terms and neg_a != neg_b:
                conflicts.append({
                    "requirements": [requirements[i]["id"], requirements[j]["id"]],
                    "severity": "High",
                    "reason": "Potentially contradictory positive and negative security statements.",
                    "action": "Request stakeholder clarification."
                })
    return conflicts

def clarification_questions(requirements, quality_findings):
    qs = []
    for f in quality_findings:
        for flag in f["flags"]:
            if "Ambiguous term" in flag:
                word = flag.split(":")[-1].strip()
                qs.append(f"What measurable definition should be used for '{word}' in {f['requirement_id']}?")
            elif "acceptance" in flag.lower():
                qs.append(f"What acceptance criteria should be used for {f['requirement_id']}?")
    return list(dict.fromkeys(qs))[:8]
