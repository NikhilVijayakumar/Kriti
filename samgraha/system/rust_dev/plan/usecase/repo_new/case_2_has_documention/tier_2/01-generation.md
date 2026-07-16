# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_2_has_documention`
**Tier:** 2
**Domains:** security, feature, architecture, engineering, external-context

## Context Available

New repo with some pre-existing hand-written documentation. No code. Tier 1 has completed. Tier 2 domains may have existing docs that need migration, or may need generation from scratch.

**Key difference from `case_1_no_documentation`:** Some domains already have hand-written docs. Migration restructures existing prose into the template shape — content is preserved, only structure changes.

## Procedure

For each domain, check if pre-existing documentation exists.

### Per-Domain Decision

| Domain | Action if docs exist | Action if no docs |
|---|---|---|
| security | Migrate into `templates/generation/document/03-security.md` shape | Generate from scratch |
| feature | Migrate into `templates/generation/document/04-feature.md` shape | Generate from scratch |
| architecture | Migrate into `templates/generation/document/05-architecture.md` shape | Generate from scratch |
| engineering | Migrate into `templates/generation/document/07-engineering.md` shape | Generate from scratch |
| external-context | Migrate into `templates/generation/document/08-external-context.md` shape | Generate from scratch |

### Migration Process

1. Read existing document.
2. Map content to template's required sections.
3. Restructure: correct section order, fill missing sections, remove misplaced content.
4. Output: template-shaped document with original content preserved.

## Within-Tier Ordering

**External Context must complete before Engineering starts.** All other domains process in parallel.

## Output

Five documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Stage 1 is migration, not pure generation.
- **vs. `repo_existing/case_2_has_documention`:** No code context — identical procedure.
