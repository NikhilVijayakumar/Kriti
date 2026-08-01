# Stage 1 - Create

**Use case:** `repo_new/tier7`
**Tier:** 7
**Domains:** build

## Context Available

New repo, no documentation, no code. Tiers 1–6 have completed — all upstream documents exist and have cleared their tier gates. Tier 7 generation uses all upstream outputs as context.

## Procedure

Generate a complete Build document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

- **Implementation** — what was built, how it was built
- **QA** — test strategy, test results, quality gates
- **Engineering** — technical practices, deployment approach
- **Architecture** — system design, infrastructure requirements

### Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| build | `common/tier7/templates/generation/document/build.md` | Implementation, QA, Engineering, Architecture |

Build describes the CI/CD pipeline, deployment process, and release strategy. Since this is a new repo with no code, Build describes the planned build infrastructure.

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. repo_existing/tier7:** real code and real CI/CD configuration available - Build should reflect actual pipeline configuration, actual deployment targets, actual release process. This use case has no code - Build describes the planned infrastructure.
- **vs. repo_existing_no_doc/tier7:** after bootstrap, identical to repo_existing/tier7.