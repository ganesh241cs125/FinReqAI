# Evaluation Template

Use a manually verified dataset of financial requirements.

## Requirement extraction

- Precision
- Recall
- F1

## Quality analysis

- Completeness
- Correctness
- Ambiguity detection accuracy
- Conflict detection accuracy
- Duplicate detection accuracy
- Testability detection

## Compliance

- Evidence retrieval precision
- Citation correctness
- Control coverage
- Unsupported-claim rate

## SDLC

Compare system recommendation against decisions made independently by experienced reviewers.
Do not report an LLM confidence score as ground truth.

## Human factors

- Human correction rate
- Time per project
- Stakeholder satisfaction
- Traceability coverage

## Hallucination test

Include questions for which no knowledge-base evidence exists. Expected behavior:
"Insufficient evidence; human review required."

## Security tests

- Prompt injection
- Unauthorized access
- Sensitive-data leakage
- Knowledge-base source restriction
