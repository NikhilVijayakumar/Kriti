# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 6
**Domains:** qa

## Context Available

Existing repo with real code but no documentation. Tiers 1–5 have completed. Tier 6 generation uses all upstream outputs plus real code as context.

**Key difference from `repo_new`:** Real code exists. QA should reference actual test files, actual test coverage data, actual test frameworks in use. The document describes the real testing state — what's tested, what's not, what gaps exist.

## Procedure

Generate a complete QA document from scratch using the document-level generation template.

### Generation

| Domain | Template | Key code-specific context |
|---|---|---|
| qa | `templates/generation/document/12-qa.md` | Actual test files, test frameworks, coverage data |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Tier 6 there has no code — QA describes the planned test strategy. This use case has real code — QA describes the actual testing state and gaps.
- **vs. `repo_new/case_2_has_documention` / `repo_existing/case_2_has_documention`:** No difference — neither has pre-existing QA docs.
