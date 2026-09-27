def analyze_security(requirements):
    out = []
    for r in requirements:
        low = r["statement"].lower()
        findings = []
        if any(k in low for k in ["transfer", "payment", "money"]):
            findings += ["Authentication", "Authorization", "Transaction integrity", "Audit logging"]
        if any(k in low for k in ["customer", "personal", "data", "history"]):
            findings += ["Sensitive-data protection", "Access control", "Data retention"]
        if "login" in low or "password" in low:
            findings += ["Credential protection", "Rate limiting", "Session security"]
        if any(k in low for k in ["secure", "authentication", "encrypt"]):
            findings += ["Encryption", "Strong authentication", "Security monitoring"]
        if not findings:
            findings = ["Review requirement for authentication, authorization and data protection impact."]
        out.append({
            "requirement_id": r["id"],
            "controls": list(dict.fromkeys(findings)),
            "status": "Review required"
        })
    return out
