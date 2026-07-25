# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 6
**Domains:** qa

## Context Available

New repo, no documentation, no code. Tiers 1–5 have completed — all upstream documents exist and have cleared their tier gates. Tier 6 generation uses all upstream outputs as context.

## Procedure

Generate a complete QA document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

- **Implementation** — what was built, how it was built
- **Feature** — what should work, acceptance criteria
- **Feature Design** — detailed feature specifications
- **Feature Technical** — technical feature specifications
- **Prototype** — prototype validation results

### Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| qa | `templates/generation/document/12-qa.md` | Implementation, Feature, Feature Technical |

QA validates that Implementation delivers what Feature and Feature Technical specified. Since this is a new repo with no code, QA describes the test strategy and plan for what will be built.

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Tier 6 generation there has real code and real test results available. QA should reflect actual test coverage, actual failures, actual gaps. This use case has no code — QA describes the planned test strategy.
- **vs. `repo_new/case_2_has_documentation` / `repo_existing/case_2_has_documentation`:** No difference — neither has pre-existing QA docs.
