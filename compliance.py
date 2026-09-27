def analyze_compliance(requirements, rag):
    results = []
    evidence = []
    for r in requirements:
        hits = rag.search(r["statement"], k=3)
        refs = []
        for h in hits:
            refs.append(h["source"])
            evidence.append({
                "requirement_id": r["id"],
                "source": h["source"],
                "score": h["score"],
                "excerpt": h["text"][:500]
            })
        if refs:
            status = "Evidence found - human review required"
            confidence = min(0.95, 0.55 + sum(h["score"] for h in hits[:2]) / 4)
        else:
            status = "No supporting evidence found"
            confidence = 0.30
        r["regulations"] = refs
        results.append({
            "requirement_id": r["id"],
            "status": status,
            "sources": refs,
            "confidence": round(confidence, 2),
            "gap": "Specify applicable control/evidence and obtain authorized review."
        })
    return results, evidence
