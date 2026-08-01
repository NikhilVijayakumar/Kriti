# Stage 1 - Create

**Use case:** `repo_new/tier6`
**Tier:** 6
**Domains:** qa

## Context Available

New repo, no documentation, no code. Tiers 1–5 have completed — all upstream documents exist and have cleared their tier gates. Tier 6 generation uses all upstream outputs as context.

## Procedure

Generate a complete QA document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

- **Implementation** — what was built, how it was built
- **Feature** — what should work, acceptance criteria
- **Feature Technical** — technical feature specifications

### Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| qa | `common/tier6/templates/generation/document/qa.md` | Implementation, Feature, Feature Technical |

QA validates that Implementation delivers what Feature and Feature Technical specified. Since this is a new repo with no code, QA describes the test strategy and plan for what will be built.

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. repo_existing/tier6:** real code and real test results available - QA should reflect actual test coverage, actual failures, actual gaps. This use case has no code - QA describes the planned test strategy.
- **vs. repo_existing_no_doc/tier6:** after bootstrap, identical to repo_existing/tier6.