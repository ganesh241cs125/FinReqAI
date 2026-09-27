def risk_for(r):
    low = r["statement"].lower()
    impact = 2
    probability = 2
    if any(k in low for k in ["money", "transfer", "payment", "fraud"]):
        impact += 2
    if any(k in low for k in ["security", "authentication", "privacy", "customer data"]):
        impact += 1
    if any(k in low for k in ["should", "fast", "secure", "available"]):
        probability += 1
    impact = min(5, impact)
    probability = min(5, probability)
    score = impact * probability
    level = "Low" if score <= 4 else "Medium" if score <= 9 else "High" if score <= 16 else "Critical"
    return {
        "requirement_id": r["id"],
        "impact": impact,
        "probability": probability,
        "score": score,
        "level": level,
        "reason": "Based on financial impact, security sensitivity and requirement uncertainty."
    }

def analyze_risk(requirements):
    results = []
    for r in requirements:
        item = risk_for(r)
        r["risk_level"] = item["level"]
        results.append(item)
    return results
