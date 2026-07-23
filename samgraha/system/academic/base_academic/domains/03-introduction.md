# 03. Introduction

**Domain:** `introduction`
**Audit Target:** The generated introduction section.

## Standard Definition

The introduction establishes the scientific and practical gap: why
existing approaches fall short, what specific limitation remains, and what
this paper contributes to close it. It ends with an explicit, enumerable
list of contributions — not a paragraph a reader has to parse contributions
out of by inference.

### Expected Evidence (Deterministic)

1. **Contributions are bullet/numbered-listed**, not buried in prose. A
   missing list is a structural weakness, flaggable mechanically (regex
   for a numbered/bulleted block following a "contributions" heading or
   equivalent cue phrase).
2. **Scope statement present:** the introduction states what the system
   does *and* what it explicitly does not handle.
3. **Gap statement present:** a short (2-3 sentence), locatable statement
   of the unresolved limitation, distinct from the general problem
   description around it.

### Semantic Judgment Criteria

- Is the research gap actually specific, or a restatement of "more work is
  needed in this general area"?
- Does the real-world/application context explain *why this problem
  matters now*, not just that it exists?
- Does each listed contribution correspond to something the paper actually
  delivers later (methodology, results, or analysis), rather than an
  aspirational claim with no matching section downstream?
- Are unsupported claims present — assertions of superiority, robustness,
  or effectiveness with no evidence pointer (table, metric, or citation)
  attached?
