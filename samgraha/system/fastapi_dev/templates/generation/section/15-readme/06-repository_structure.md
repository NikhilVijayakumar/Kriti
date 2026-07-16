# Repository Structure — Generation Template

> **Domain:** readme
> **Section:** repository_structure
> **Source:** `documentation-standards/15-readme-standards.md` §Repository Structure
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Repository Structure section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / project_layout | Repository Structure must reflect Engineering(07) project layout |

## Template

```markdown
## Repository Structure

- `src/` — [purpose]
- `tests/` — [purpose]
- `docs/` — [purpose]
- `scripts/` — [purpose]
<!-- High-level descriptions only; no file-level detail -->
```

## Examples

**Correct:**
> - `src/` — Application source code
> - `tests/` — Unit and integration tests
> - `docs/` — Documentation by standard
> - `scripts/` — Build and automation scripts
> - `examples/` — Usage examples and templates

**Incorrect:**
> - `src/core/scheduler/worker.py` — The main worker loop that processes tasks
> - `src/api/routes/v2/health.py` — Health check endpoint returning 200 OK
> *Why wrong: Repository Structure must provide high-level directory descriptions, not file-level implementation details.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** List major directories with one-sentence purpose descriptions; keep descriptions high-level and focused on purpose
- **Don't:** List individual files or modules; include implementation details; describe internal code organization

**Minimum content:** 1 subsection
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Documentation Structure, Getting Started, Development

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
