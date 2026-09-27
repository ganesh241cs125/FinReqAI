from .common import LLM

def classify(requirements):
    system = """Classify each requirement using only these labels when applicable:
Business, Stakeholder, Functional, Security, Privacy, Regulatory, Performance,
Availability, Usability, Data Management, Integration, Audit/Reporting, Operational.
Return JSON {"requirements":[{"id":"","category":[]}]}. Multiple labels allowed."""
    fallback = {"requirements": []}
    for r in requirements:
        c = list(r.get("category", []))
        low = r["statement"].lower()
        mapping = {
            "security": ["secure","authentication","authorization","encrypt","fraud"],
            "privacy": ["privacy","personal data","customer data"],
            "performance": ["fast","seconds","latency","performance"],
            "availability": ["24/7","available","availability","uptime"],
            "data management": ["data","history","record","database"],
            "audit/reporting": ["audit","report","log"],
            "integration": ["api","integrate","legacy"],
            "regulatory": ["regulation","compliance","policy","regulatory"]
        }
        for label, terms in mapping.items():
            if any(t in low for t in terms):
                proper = {
                    "security":"Security","privacy":"Privacy","performance":"Performance",
                    "availability":"Availability","data management":"Data Management",
                    "audit/reporting":"Audit/Reporting","integration":"Integration",
                    "regulatory":"Regulatory"
                }[label]
                c.append(proper)
        fallback["requirements"].append({"id": r["id"], "category": list(dict.fromkeys(c))})
    result = LLM.json(system, str(requirements), fallback)
    by_id = {x["id"]: x for x in result.get("requirements", [])}
    for r in requirements:
        if r["id"] in by_id and by_id[r["id"]].get("category"):
            r["category"] = list(dict.fromkeys(by_id[r["id"]]["category"]))
    return requirements
