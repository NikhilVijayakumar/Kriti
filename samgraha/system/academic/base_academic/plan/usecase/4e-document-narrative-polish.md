# Use-case 4e — Document Narrative Polish

**Depends on**: `humanize-semantic` (5d — every flagged domain resolved,
or `humanize-deterministic` alone if no domain needed the semantic pass)

**Script**: Whole-document, 3 sequential sub-steps (each reads the
previous step's output, not the original — genuinely sequential, not
parallel triads) —
1. `gather-document-evidence` (reused from `document-audit/`) →
   `structure-polish` (prompt — section ordering within each domain,
   heading consistency, transition sentences between domains) →
   `persist-section-draft` (stage=`polish`, per domain, only for domains
   the pass actually changed)
2. `gather-document-evidence` (re-run, now over `stage='polish'` where
   present else `stage='budget-fit'`) → `narrative-style-polish` (prompt
   — voice/tone consistency across all 12 domains, terminology
   normalization) → `persist-section-draft` (stage=`polish`)
3. `gather-document-evidence` (re-run) → `content-detail-polish` (prompt
   — balances level of detail so no domain is disproportionately thin/
   dense relative to its budget from 4d) → `persist-section-draft`
   (stage=`polish`)

**Inputs**: Full concatenated document (all domains' latest drafts, per
`_master-schema.yaml` order — same concatenation `5f`/`6c` already do)

**Action**: Three independent revision passes over the whole assembled
paper, each targeting one cross-cutting concern named in the request
(structure, narrative style, content detail) — a step a reader would
recognize as "the editor's pass," distinct from both per-section
generation (4a-4d) and per-section/whole-document audit (5/5a/5e/5f).
Each sub-step must preserve every citation (4b) and stay within the
budget fit from 4d — a rule enforced by re-running `4d`'s budget check
(not duplicated logic) as this usecase's own completion gate.

**Design constraint, to prevent a 4d↔4e fight**: `content-detail-polish`
(sub-step 3) may not grow any single domain's word count by more than 10%
over its `stage='budget-fit'` (4d) value — enforced by the prompt's own
instructions plus a deterministic post-check in `persist-section-draft`
that rejects (and does not persist) a `content-detail-polish` result
exceeding the cap, re-running the sub-step once with an explicit
"tighten, don't lengthen further" instruction before accepting it as-is.
This caps the retry to O(1) per domain instead of an open-ended 4d⇄4e
cycle.

**Completion criteria** (checked by verify script):
- Every structural domain has a `stage='polish'` row (even if unchanged
  by all 3 sub-steps — still gets a row, so completeness is one uniform
  predicate)
- Whole-paper word count (post-polish) still within
  `calculation/summary/paper-budget.yaml`'s range — the 10% per-domain cap
  bounds worst case but doesn't guarantee the sum (12 domains each at
  +10% can still exceed the total); if this check fails, 4e re-invokes
  `4d`'s fit script directly on the polished text (one bounded pass, not
  a new open-ended loop back through 4a-4c) rather than failing outright

**Verify script**: `script/verify/uc4e_document_polish.py --paper-id <id>`

**Rule**: Runs after humanize resolves all flags. Gates the renumbered
`5e`/`5f` (cross-section/document audits score the polished document).
Re-runnable — a later targeted fix to one domain invalidates polish the
same way it invalidates `5e`/`5f` today (`computed_against` staleness
tracking, already specified in the prior proposal §5, applies here too —
`4e`'s own re-run is what re-validates it).
