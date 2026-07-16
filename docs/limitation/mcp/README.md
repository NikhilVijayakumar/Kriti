# Samgraha MCP Engine — Limitation / Feature-Request Log

These are engine-level gaps in the MCP audit engine itself — not fixable by editing standard/YAML content in `samgraha/system/*`. Found during the `rust_dev` standard review (`docs/rust_dev-proposal.md`, `docs/error_list/rust_dev/`).

---

## MCP-001: No `scope: collection` support for individual checks

**Severity:** Medium
**Affects:** Any domain with a "must exist somewhere in the collection, not in every document" requirement. Confirmed impact: `rust_dev`'s Architecture domain (`crate_architecture`).

### Problem

A check can only declare scope at the **file** level (`scope: document` or `scope: section` in the YAML header). There is no way for an individual check within a file to say "this must be true for the collection as a whole" (e.g. "at least one architecture document defines `crate_architecture`") as opposed to "this must be true for every document individually."

### Evidence

`samgraha/system/rust_dev/audit/deterministic/document/05-architecture.yaml`:
```yaml
scope: document   # file-level, line 4

rules:
  - id: arch-doc-rust-001
    description: "Crate Architecture required"
    condition: "document contains the crate_architecture section"
    mandatory: true
    evidence:
      type: section_presence
      required_semantic_types:
        - crate_architecture
```
`crate_architecture` is a collection-level requirement per `documentation-standards/05-architecture-standards.md` (at least one architecture doc must define it — not every one). Because the check inherits the file's `scope: document`, it fires on every architecture document in the repo. If there are 9 architecture docs, 8 produce false-positive findings.

### Requested Fix

Add an optional `scope:` field on individual checks that overrides the file-level default:
```yaml
rules:
  - id: arch-doc-rust-001
    scope: collection   # fires once across all docs in the domain, not per-document
    evidence:
      type: section_presence
      required_semantic_types:
        - crate_architecture
```
When `scope: collection` is set, the engine should evaluate the condition against the union of documents in the domain and report a single pass/fail for the domain, not one per document.

**Workaround considered and rejected:** restructuring into a separate `audit/deterministic/collection/` file tree with file-level `scope: collection`. Rejected because it fragments a domain's checks across two directories for what is conceptually one rule set, and still requires this same engine feature to interpret `scope: collection` at all — the file-level split doesn't avoid needing the feature, it just moves where it's declared.

---

## MCP-002: `keyword_absence` only supports substring matching — no word-boundary or regex mode

**Severity:** Low
**Affects:** Every domain using `keyword_absence` evidence (57 usages across `rust_dev` alone, e.g. Vision's technology-independence check).

### Problem

The `keyword_absence` evidence type checks a section's text against category-based keyword lists (`programming_languages`, `frameworks`, `libraries`, etc.) using plain substring matching. There is no `match:`/`word_boundary`/regex option to require a whole-word match.

### Evidence

`samgraha/system/rust_dev/audit/deterministic/section/01-vision/09-success_criteria.yaml`:
```yaml
- id: vis-sec-sc-002
  description: "Success Criteria are technology-independent"
  evidence:
    type: keyword_absence
    categories:
      - programming_languages
      - frameworks
      - libraries
```
No `keyword_absence` usage anywhere in the codebase has a `match_mode`, `word_boundary`, or regex field — confirmed by repo-wide search. Consequences of substring-only matching:
- `"pipelines"` contains `"pip"` → false-positive keyword hit on a word that has nothing to do with the Python package manager.
- `"aspires"` does not satisfy a keyword list expecting `"aspiration"` → false negative (missed match) on the morphological variant.

### Requested Fix

**Option A (preferred) — add a `match:` field to the evidence block:**
```yaml
evidence:
  type: keyword_absence
  categories:
    - programming_languages
  match: word_boundary   # default: substring, for backwards compatibility
```

**Option B — allow categories to hold regex patterns instead of plain strings:**
```yaml
keywords:
  - pattern: "\\bpip\\b"
```

Option A is lower-effort and preserves the existing category-list authoring model; Option B is more powerful but requires migrating every existing keyword list to pattern form.

---

## Status

Both items are logged here because they require changes to the MCP engine itself (the code that interprets these YAML evidence types), not to any standard's content. No workaround exists in `samgraha/system/rust_dev` that fully resolves either — see `docs/error_list/rust_dev/15-third-pass-audit-checks.md` (GAP-1, GAP-2) for the content-side audit trail.
