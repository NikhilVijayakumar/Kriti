# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_2_has_documention`
**Tier:** 2
**Domains:** security, feature, architecture, engineering, external-context

## Context Available

Existing repo with real code and existing non-conforming documentation. Tier 1 has completed. Stage 1 is migration — restructure existing prose into template shape. Real code is available as additional context.

**Key difference:** Every domain has existing docs (Path B) AND real code context (from Tier 2). Migration can reference actual code to verify content accuracy — if the existing Architecture doc describes a microservices design but the code is a monolith, the migration should flag this discrepancy.

## Procedure

For each domain, migrate the existing document into the template shape, using real code as verification context.

### Per-Domain Migration

| Domain | Target template | Code verification |
|---|---|---|
| security | `templates/generation/document/03-security.md` | Check auth/permissions against actual code |
| feature | `templates/generation/document/04-feature.md` | Check feature list against actual functionality |
| architecture | `templates/generation/document/05-architecture.md` | Verify structure against actual directory layout |
| engineering | `templates/generation/document/07-engineering.md` | Verify practices against actual config |
| external-context | `templates/generation/document/08-external-context.md` | Not code-dependent |

### Migration Process

1. Read existing document.
2. Map content to template's required sections.
3. Cross-reference with real code where applicable — flag discrepancies.
4. Restructure: correct order, fill gaps, resolve discrepancies.
5. Output: template-shaped document with content preserved and verified.

## Within-Tier Ordering

**External Context must complete before Engineering starts.** All other domains migrate in parallel.

## Output

Five documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Stage 1 is migration, not generation. Existing docs change the starting point.
- **vs. `repo_new/case_2_has_documention`:** Real code context available for verification.
