# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 3
**Domains:** feature-design, feature-technical

## Context Available

Existing repo with real code but no documentation. Tiers 1–2 have completed. Tier 3 generation uses all upstream outputs plus real code as context.

**Key difference from `repo_new`:** Real code exists. Feature Technical generation should reflect actual code patterns, actual module interfaces, actual data models. Feature Design generation should reflect actual UI components and user flows visible in code.

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Upstream Context

All Tier 1–2 documents plus the real codebase.

### Per-Domain Generation

| Domain | Template | Key code-specific context |
|---|---|---|
| feature-design | `templates/generation/document/09-feature-design.md` | Existing UI components, user flows visible in code |
| feature-technical | `templates/generation/document/10-feature-technical.md` | Actual module interfaces, data models, API contracts |

## Within-Tier Ordering

No ordering constraint — both domains generate in parallel.

## Output

Two documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Tier 3 there has no code — Feature Technical invents interfaces. This use case has real code — generation describes actual interfaces.
- **vs. `repo_new/case_2_has_documentation` / `repo_existing/case_2_has_documentation`:** No difference — neither has pre-existing feature-design/feature-technical docs.
