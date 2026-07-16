# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 2
**Domains:** security, feature, architecture, engineering, external-context

## Context Available

Existing repo with real code but no documentation. Tier 1 has completed — Vision and Philosophy documents exist and have cleared the tier gate. Tier 2 generation uses Tier 1 outputs plus real code as context.

**Key difference from `repo_new`:** Real code exists. Architecture, Engineering, and Feature generation should reflect the actual codebase structure — what's actually built, what patterns are used, what the real component boundaries are. Generation produces documentation that describes reality, not a plausible-sounding design.

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Upstream Context

- **Vision** — `vision.md` (Tier 1): product purpose, problem, solution
- **Philosophy** — `philosophy.md` (Tier 1): principles, values, trade-offs
- **Real code** — the existing codebase: directory structure, entry points, key modules, configuration files, build scripts

### Per-Domain Generation

| Domain | Template | Key upstream inputs | Code-specific context |
|---|---|---|---|
| security | `templates/generation/document/03-security.md` | Vision, Philosophy | Existing auth, permissions, dependency audit results |
| feature | `templates/generation/document/04-feature.md` | Vision, Philosophy | Existing feature set visible in code |
| architecture | `templates/generation/document/05-architecture.md` | Philosophy | Actual directory structure, module boundaries, dependency graph |
| engineering | `templates/generation/document/07-engineering.md` | Philosophy | Actual language, frameworks, linting config, test setup |
| external-context | `templates/generation/document/08-external-context.md` | Vision | Market analysis — not code-dependent |

Architecture and Engineering generation should reflect the actual code structure. If the code uses a monorepo with 5 modules, the Architecture document describes a monorepo with 5 modules — not a microservices design that doesn't exist.

## Within-Tier Ordering

**External Context must complete before Engineering starts.** All other domains generate in parallel.

Execution order:
1. External Context, Security, Feature, Architecture — parallel
2. Engineering — after External Context completes

## Output

Five documents, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Tier 2 generation there has no code — Architecture and Engineering invent a plausible design from the product idea. This use case has real code — generation describes what exists.
- **vs. `repo_new/case_2_has_documention`:** No difference — neither has pre-existing docs at Tier 2.
- **vs. `repo_existing/case_2_has_documention`:** Tier 2 there starts with existing non-conforming docs. This use case generates from scratch against real code.
