# FinReqAI Project Guide

## Core workflow

1. Project input
2. Requirement extraction
3. Requirement classification
4. Requirement quality analysis
5. Conflict detection
6. RAG evidence retrieval
7. Compliance analysis
8. Security analysis
9. Risk analysis
10. Human approval
11. SDLC multi-criteria scoring
12. Artifact generation
13. Audit logging

## What is deterministic?

- Basic requirement extraction fallback
- Classification fallback
- Quality checks
- Conflict heuristics
- RAG retrieval
- Risk scoring
- SDLC scoring
- Artifact generation

## What is LLM-assisted?

When an API key is configured:
- Requirement extraction
- Classification
- Future explanation extensions

The architecture deliberately keeps SDLC scoring deterministic so that the project can explain why scores changed.

## Production extensions

For a production-quality research prototype, add:
- proper authentication and RBAC
- immutable audit storage
- encrypted secrets
- signed/versioned knowledge sources
- source allowlisting
- prompt-injection defenses
- stronger semantic embeddings
- evaluation dataset and automated metrics
- background jobs
- PostgreSQL
- model/version tracking
- approval permissions
- document exports to DOCX/PDF
- richer multi-agent orchestration
