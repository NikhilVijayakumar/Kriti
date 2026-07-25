# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 5
**Domains:** implementation

## Context Available

New repo, no documentation, no code. Tiers 1–4 have completed — all upstream documents exist and have cleared their tier gates. Tier 5 generation uses all upstream outputs as context.

## Procedure

Generate a complete Implementation document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

- **Vision** — what to build and why
- **Philosophy** — principles, values, trade-offs
- **Feature** — feature list, priorities
- **Architecture** — system design, component boundaries
- **Design** — user experience, interaction patterns
- **Engineering** — technical practices
- **External Context** — market landscape, constraints
- **Security** — threat model, requirements
- **Feature Design** — detailed feature specifications
- **Feature Technical** — technical feature specifications
- **Prototype** — prototype plan, validation results

### Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| implementation | `templates/generation/document/13-implementation.md` | Feature Technical, Engineering, Prototype |

Implementation translates Feature Technical specifications into a concrete implementation plan. Since this is a new repo with no code, the plan describes what will be built, not what has been built.

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Tier 5 generation there has real code available. Implementation should reflect the actual codebase — what exists, what needs to be added, what needs to change. This use case has no code — implementation describes the planned build from scratch.
- **vs. `repo_new/case_2_has_documentation` / `repo_existing/case_2_has_documentation`:** No difference — neither has pre-existing implementation docs.
