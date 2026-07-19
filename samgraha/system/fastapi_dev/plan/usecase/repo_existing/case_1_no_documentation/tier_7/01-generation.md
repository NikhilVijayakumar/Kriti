# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 7
**Domains:** build

## Context Available

Existing repo with real code but no documentation. Tiers 1–6 have completed. Tier 7 generation uses all upstream outputs plus real code as context.

**Key difference from `repo_new`:** Real code exists. Build should reference actual CI/CD configuration files, actual build scripts, actual deployment targets. The document describes the real build infrastructure — what's configured, what's missing, what needs to change.

## Procedure

Generate a complete Build document from scratch using the document-level generation template.

### Generation

| Domain | Template | Key code-specific context |
|---|---|---|
| build | `templates/generation/document/14-build.md` | Actual CI/CD config, build scripts, deployment targets |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Tier 7 there has no code — Build describes planned infrastructure. This use case has real code — Build describes actual infrastructure and gaps.
- **vs. `repo_new/case_2_has_documentation` / `repo_existing/case_2_has_documentation`:** No difference — neither has pre-existing Build docs.
