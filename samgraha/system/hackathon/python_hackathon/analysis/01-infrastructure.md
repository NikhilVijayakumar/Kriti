# Infrastructure Analysis Prompt

Guides the per-team analysis for the Infrastructure domain — read by
whichever agent runs it via MCP, after scoring has completed. Turns
raw scores into a narrative explaining *why* each team scored as they
did on infrastructure. Not parsed by a script — this is a prompt.

## Version
1.0.0

## Analysis Intent
Infrastructure scores (weight: 8) reflect whether a team's project
can be reproduced locally. This step explains which teams have solid
reproducible environments and which don't, grounded in the actual
files found.

## Inputs
- `standard_domain_scores` DB table — all teams' infrastructure
  domain scores (queried via MCP)
- Per-team deterministic findings: `uv.lock` presence, `Dockerfile`
  presence, `docker-compose.yaml` presence
- Semantic findings: quality of containerization, dependency
  management completeness

## Narrative Guidance
The Infrastructure narrative must cover:
1. **Score Overview** — team's infrastructure score out of 8 (domain
   weight), and how it compares to the competition average.
2. **Dependency Locking** — did the team include a `uv.lock`? If not,
   this is the most common infrastructure failure. Name whether it's
   present or absent.
3. **Containerization** — did the team provide a `Dockerfile`? If so,
   was it functional (not just a stub)? Mention `docker-compose.yaml`
   if present.
4. **Strengths** — what the team did well: complete lock file, working
   Docker setup, multi-stage build, health checks, etc.
5. **Weaknesses** — what's missing: no lock file, no Docker, bare
   Dockerfile without proper entrypoint, missing `.dockerignore`.
6. **Recommendations** — specific actions: "add `uv.lock` by running
   `uv lock`", "create a Dockerfile with python:3.11-slim base".

## Visualization Guidance
- `domain_scores` — always include: this team's infrastructure score
  vs competition average.
- `checklist_coverage` — include: which of the expected evidence items
  (uv.lock, Dockerfile, docker-compose) are present/absent.

## Output Schema
```json
{
  "domain": "01-infrastructure",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "Dependency Locking", "text": "..."},
    {"heading": "Containerization", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
