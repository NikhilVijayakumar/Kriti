# base_academic — Usecase Atomicity Proposal (Section Pipeline Split + Whole-Paper Polish + Humanize Split)

## 0. Why This Document Exists

The prior granularity pass
(`docs/proposal/archive/base_academic-usecase-granularity-proposal.md`) is
implemented — every usecase in `plan/usecase/*.md` now has a `Depends on`
field, a phrased-as-SQL `Completion criteria`, and a real
`script/verify/uc*.py` file (confirmed: `script/verify/` exists and is
populated, every `.md` file in `plan/usecase/` has all three fields).
`5d-cross-section-semantic-audit.md` / `5e-document-semantic-audit.md` are
built, `academic_semantic_runs.scope` exists in
`schema/09-academic_semantic_runs.sql` with the 3-way
`CHECK (scope IN ('section','cross-section','document'))`.

That proposal fixed *ordering and verification*. It didn't fix
*granularity* — three usecases still do several unrelated things behind one
`Script:` line, and this is now the concrete complaint: `3-mathematics-and-
diagrams.md`, `4-assemble-paper-structure.md`, and `5c-humanize.md` are each
a bundle of steps that should be independently checkable, independently
re-runnable, and independently auditable, rather than one opaque multi-step
script.

Confirmed on disk today:

- **`4-assemble-paper-structure.md`'s single `generate-section` prompt
  (`prompt/assemble-paper-structure/generate-section.md`) does initial
  content generation, evidence citation, and (implicitly, per its Rule 4
  "include proper structure") math/diagram weaving all in one LLM call.**
  There is no step boundary between "write the section" and "cite the
  section" and "add the table/equation" — a failure or a desired re-run of
  just the citation quality can't happen without regenerating the whole
  section's prose.
- **`generate-section.md`'s JSON output includes `citations_used`, and it
  is silently dropped.** `script/assemble-paper-structure/
  persist_section_draft.py` calls `academic_schema.upsert_narrative(conn,
  paper_id, domain, sections, stage=..., iteration=..., validated=...,
  model=...)` — no `citations` parameter exists on that function
  (`script/common/academic_schema.py:276-278`), and no table stores them.
  The `references` structural domain (last in `_master-schema.yaml`'s
  `sections:` list) has no mechanism to be built *from* what the other 11
  domains actually cited — it's generated the same context-free way as
  every other domain via the same `generate-section` prompt, even though
  its correct content is strictly a function of the other domains' output.
- **No per-section character/word budget enforcement step exists.**
  `calculation/deterministic/{domain}.yaml` already carries a
  `word_count_in_range` check per domain (e.g. `abstract.yaml:8`, `{min:
  100, max: 500}`) — but that's an *audit* check, run once by
  `5-deterministic-audit.md`, with no step that acts on a FAIL by trimming
  or expanding the draft. A section that's 800 words when the budget is
  500 fails deterministic audit and stops there; nothing tries to fit it.
  There's also no whole-paper total budget anywhere — 12 independent
  per-domain ranges can each individually pass while the concatenated
  paper blows a journal's page limit, and nothing checks the sum.
- **`schema/07-academic_narratives.sql`'s own comment documents a prior
  decision this proposal reverses.** Line 2-3: `"stage progresses generate
  → humanize (no separate deepen stage — enrichment passes are folded into
  the generation step)."` That was the right call when generation was one
  step. It's the wrong call now that the user is explicitly asking for
  citation, enrichment, and budget-fitting to be separable, auditable
  steps — §4 below extends the `stage` enum and says so explicitly rather
  than quietly contradicting the existing comment.
- **`3-mathematics-and-diagrams.md` bundles two unrelated analysis
  outputs — mathematics and architecture/diagrams — behind one usecase.**
  Its own `Script:` line already names them as parallel, independent
  prompt pairs (`module-analysis-mathematics` + `module-analysis-
  architecture`, `cross-module-analysis-mathematics` + `-architecture` +
  `-dependencies` + `-interactions`) that happen to share the same
  gather/persist scripts. Nothing about them is coupled — a repo could
  need its architecture diagrams re-run without touching its math
  formalization, and today there's no way to verify or re-run one without
  the other.
- **`5c-humanize.md`'s single `humanize-section` prompt
  (`prompt/humanize/humanifier.md`) does mechanical, NLP-detectable pattern
  fixing (Layer 1: "vary sentence length", "break parallel structure" —
  things `textstat`/`nltk` measure directly) and LLM judgment work (Layer
  2/3: technical detail injection, voice matching) in one call — the exact
  split `5b-plagiarism-forensic-audit.md` already uses successfully
  one step up (`deterministic-fingerprint-check` before
  `plagiarism-fingerprint-audit`), not applied to its own downstream
  usecase.
- **No whole-paper semantic polish (generation) step exists — only whole-
  paper semantic *audit* (`5d`/`5e`) does.** Audit measures whether the
  assembled paper reads well; nothing acts on that measurement. Today, if
  `5d`/`5e` finds a narrative-arc or terminology-consistency problem, the
  only remedy the pipeline offers is re-running individual sections'
  `generate-section` (losing per-section audit progress) — there's no
  step that revises the whole paper for structure/narrative-style/detail-
  balance the way `5d`/`5e` scores it.

## 1. Scope

Same boundary as the prior proposal: `base_academic/plan/usecase/*.md`,
the scripts/prompts/schema/calculation files they name, and
`script/schema/standard.yaml`'s usecase registry. Doesn't touch
`0-classify-repo.md`, `00-schema-init.md`, `1-novelty-analysis.md`,
`2-gap-analysis.md`, `5b-plagiarism-forensic-audit.md`, `6a`/`6b`/
`calculate.md` bodies — they're already atomic (each does one script-kind
of work) and are only touched here where a dependency name changes because
something upstream got renumbered.

## 2. Full Pipeline Shape (After This Proposal)

```
00  schema-init
0   classify-repo                              [[GATE]] HAS_DOCS
1   novelty-analysis           ─┐
2   gap-analysis                ├─ independent, parallel
3a  mathematics-analysis        │
3b  diagram-architecture-analysis ┘
        │
        ▼  [[GATE]] all four have results
4a  generate-section-draft        (per structural domain — initial deep content)
        │
        ▼  [[GATE]] every structural domain has a stage='generate' row
4b  section-citations             (per domain — in-repo evidence citations
        │                          for all 12 + external literature search
        │                          for CITE_CONTEXT_DOMAINS + collate into
        │                          the `references` domain)
        ▼  [[GATE]] every domain has a stage='cite' row
4c  section-supplementary-content (per domain — weave in math/tables/diagrams
        │                          from 3a/3b findings, where relevant)
        ▼  [[GATE]] every domain has a stage='enrich' row
4d  section-budget-fit            (per domain — trim/expand to fit configured
        │                          min/max word budget)
        ▼  [[GATE]] every domain has a stage='budget-fit' row, in-range
5   deterministic-audit           (per domain — mechanical checks, extended
        │                          for citation-count / budget / placeholder
        │                          checks on the new stages' output)
5a  semantic-audit                (per domain — 'section-part' runs per new
        │                          stage's artifact + one 'section-full' run;
        │                          mandatory, both deterministic-eligible
        │                          domains AND the parts within them)
        ▼  [[GATE]] every domain PASS on deterministic + full semantic
5b  plagiarism-forensic-audit     (per domain — unchanged)
5c  humanize-deterministic        (per flagged domain — NLP-lib mechanical fix)
5d  humanize-semantic             (per still-flagged domain — LLM rewrite)
        │
        ▼  [[GATE]] every domain PASS, all flags resolved
4e  document-narrative-polish     (whole paper — structure / narrative-style /
        │                          content-detail sub-steps, semantic
        │                          generation, NOT audit)
        ▼  [[GATE]] polish complete for all domains
5e  cross-section-semantic-audit  (renumbered from 5d — unchanged body)
5f  document-semantic-audit       (renumbered from 5e — unchanged body,
        │                          now also runs the new total-budget
        │                          deterministic check, §6)
        ▼  [[GATE]] both PASS
6   calculate  →  6a render-charts  →  6b render-audit-report
        └────────────────────────────→  6c render-paper
```

Rationale for `4e` sitting *after* `5d` (humanize-semantic) rather than
directly after `4d` (budget-fit): polishing narrative-arc/structure before
plagiarism/humanize would risk the humanize pass re-introducing the exact
AI-fingerprint patterns polish just smoothed over. Polish is the last
content-shaping step before the two audits that gate rendering — it revises
what humanize already made safe, not the other way around.

## 3. Split Usecase 3 → `3a-mathematics-analysis` / `3b-diagram-architecture-analysis`

Both reuse the existing `_shared/analysis/*` scripts verbatim (
`gather-module-evidence`, `gather-cross-module-evidence`, `persist-module-
analysis`, `persist-cross-module-analysis` are already `analysis_kind`-
parameterized — no new script needed, this is a usecase-file and dispatch-
filter split, not a code split).

```markdown
# Use-case 3a — Mathematics Analysis

**Depends on**: `classify-repo` (HAS_DOCS)

**Script**: Per-module + cross-module triads — `gather-module-evidence` →
`module-analysis-mathematics` → `persist-module-analysis` (kind=`mathematics`)
+ `gather-cross-module-evidence` → `cross-module-analysis-mathematics` →
`persist-cross-module-analysis` (kind=`mathematics`)

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind='mathematics'` >= 1

**Verify script**: `script/verify/uc3a_math_analysis.py --paper-id <id>`

**Rule**: Runs after classify-repo (HAS_DOCS only). Independent of 3b —
either can re-run without the other. Accumulates.
```

```markdown
# Use-case 3b — Diagram & Architecture Analysis

**Depends on**: `classify-repo` (HAS_DOCS)

**Script**: Per-module + cross-module triads — `gather-module-evidence` →
`module-analysis-architecture` → `persist-module-analysis` (kind=
`architecture`) + `gather-cross-module-evidence` →
`cross-module-analysis-architecture` + `cross-module-analysis-dependencies` +
`cross-module-analysis-interactions` → `persist-cross-module-analysis`
(3 kinds)

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind IN ('architecture','dependencies','interactions')` >= 1

**Verify script**: `script/verify/uc3b_diagram_architecture.py --paper-id <id>`

**Rule**: Runs after classify-repo (HAS_DOCS only). Independent of 3a.
Accumulates.
```

`cross-module-analysis-mathematics` is registered in `standard.yaml` with
the comment `# registered, not yet dispatched — see run_full_workflow.py
note` (`script/schema/standard.yaml:118`) — this split is also where that
gets wired in, since 3a now needs it dispatched.

`4a`'s `Depends on` changes from `mathematics-and-diagrams` to `3a` + `3b`
(both, since it needs both math formalization and architecture diagrams to
weave in during `4c`).

## 4. Split Usecase 4 → `4a` Draft / `4b` Citations / `4c` Supplementary Content / `4d` Budget Fit

### Schema change — `academic_narratives.stage` enum, extended

```sql
-- schema/07-academic_narratives.sql
stage TEXT NOT NULL DEFAULT 'generate'
      CHECK (stage IN ('generate','cite','enrich','budget-fit','polish','humanize')),
```

Reverses the file's own comment (§0) — replaced with:

```sql
-- stage progresses generate -> cite -> enrich -> budget-fit -> polish ->
-- humanize. Each stage is a separately checkable, separately re-runnable
-- usecase (base_academic-usecase-atomicity-proposal.md); iteration
-- increments within each stage. The orchestrator always reads the
-- most-processed version (latest stage in this order, then latest
-- iteration within that stage).
```

`upsert_narrative()` (`script/common/academic_schema.py:276`) needs no
signature change — `stage` is already a parameter, only the CHECK
constraint's allowed values grow.

### `4a` — Generate Section Draft

```markdown
# Use-case 4a — Generate Section Draft

**Depends on**: `novelty-analysis` + `gap-analysis` + `mathematics-analysis`
(3a) + `diagram-architecture-analysis` (3b)

**Script**: Per-domain triad — `gather-domain-evidence` → `generate-section`
(prompt, trimmed — citation/math-weaving rules removed, see below) →
`persist-section-draft` (stage=`generate`)

**Inputs**: Repo documentation, analysis docs, novelty/gap findings,
`templates/generation/markdown/{domain}.md` per structural domain

**Action**: Generate every structural domain **except `references`** —
`references` has no content of its own to generate pre-citation, its real
content is strictly a function of what 4b collates from the other 11
domains (§0). Running `generate-section` on it here would produce a draft
4b immediately overwrites — throwaway work this split removes rather than
carrying forward. Initial deep content — structure, argument, claims
grounded in evidence. No external-literature citation pass and no explicit
math/table weaving here (moved to 4b/4c) — `generate-section.md`'s Rule 1
("cite evidence") stays for in-repo grounding markers only; Rule 4's
"proper structure" narrows to headings/flow, not diagram/equation
insertion.

**Completion criteria**:
- Every structural domain **except `references`** has >= 1
  `academic_narratives` row with `stage='generate'`

**Verify script**: `script/verify/uc4a_generate_section.py --paper-id <id>`

**Rule**: Runs after novelty + gap + math + diagram analyses all have
results. Per-domain triads expanded at runtime.
```

### `4b` — Section Citations

Closes the gap named in §0: `citations_used` is currently generated by the
LLM and discarded. This usecase is what actually consumes it, and is the
only place the `references` domain gets real content instead of a
context-free `generate-section` call.

**Schema addition** — one new table, since citations don't fit the
existing heading+text shape of `academic_narrative_sections`:

```sql
-- schema/21-academic_section_citations.sql
CREATE TABLE IF NOT EXISTS academic_section_citations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id    INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id   INTEGER NOT NULL REFERENCES academic_domains(id) ON DELETE CASCADE,
    source_kind TEXT    NOT NULL CHECK (source_kind IN ('in-repo','literature')),
    citation    TEXT    NOT NULL,   -- formatted citation text
    created_at  TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_academic_section_citations_lookup
    ON academic_section_citations(paper_id, domain_id);
```

```markdown
# Use-case 4b — Section Citations

**Depends on**: `generate-section-draft` (4a — every domain has a
`stage='generate'` row)

**Script**: Two parts —
1. Per-domain (all 12 structural domains except `references`) —
   `gather-domain-evidence` (mode=`citation`) → `generate-section`'s
   existing evidence-citation output → new `persist-section-citations.py`
   (writes `academic_section_citations`, `source_kind='in-repo'`)
2. Per `CITE_CONTEXT_DOMAINS` (`related-work`, `introduction`,
   `discussion` — `script/schema/run_full_workflow.py:28`) — unchanged
   `literature-review-pass` (prompt) → `persist-section-citations.py`
   (`source_kind='literature'`) + `persist-section-draft` (stage=`cite`,
   updates the domain's draft with literature context woven in)
3. Deterministic — new `collate_references.py`: reads all
   `academic_section_citations` rows for the paper, deduplicates, formats
   a bibliography, writes it as the `references` domain's **first**
   `academic_narratives` row (`stage='cite'` — `references` has no
   `stage='generate'` row, by design, per 4a's skip above)

**Inputs**: Each domain's `stage='generate'` draft, citation corpus/lookup

**Action**: Attach real, queryable citations to every domain (previously
silently dropped, §0) and build the `references` section from what other
sections actually cited, instead of generating it context-free.

**Completion criteria**:
- Every non-`references` structural domain has >= 1
  `academic_section_citations` row
- `references` domain has a `stage='cite'` `academic_narratives` row

**Verify script**: `script/verify/uc4b_section_citations.py --paper-id <id>`

**Rule**: Runs after 4a. `references` domain's citation collation runs last
within this usecase (needs every other domain's citations first).
```

### `4c` — Section Supplementary Content

```markdown
# Use-case 4c — Section Supplementary Content

**Depends on**: `section-citations` (4b) + `mathematics-analysis` (3a) +
`diagram-architecture-analysis` (3b)

**Script**: Per-domain — `gather-domain-evidence` (mode=`enrich`, pulls
`academic_cross_module_analysis` kind=`mathematics`/`architecture`/
`dependencies`/`interactions`) → new `section-enrichment` (prompt) →
`persist-section-draft` (stage=`enrich`)

**Inputs**: Each domain's `stage='cite'` draft, 3a/3b findings relevant to
that domain (e.g. `methodology`/`results` pull `mathematics` +
`architecture`; domains with no relevant cross-cutting findings pass
through unchanged)

**Action**: Weave in equations, tables, and diagram references where the
domain's content actually calls for them — the step `generate-section.md`
used to do implicitly (§0). Domains with nothing relevant to add are a
no-op pass-through (still produces a `stage='enrich'` row, unchanged text)
so the completeness gate (§below) has one uniform predicate.

**Completion criteria**:
- Every structural domain has >= 1 `academic_narratives` row with
  `stage='enrich'`

**Verify script**: `script/verify/uc4c_section_enrichment.py --paper-id <id>`

**Rule**: Runs after 4b. Per-domain, independently re-runnable.
```

### `4d` — Section Budget Fit

Turns today's audit-only `word_count_in_range` check (§0) into something
the pipeline acts on, and adds the whole-paper total the per-domain ranges
never summed.

**New calculation file** — whole-paper total, one level up from the
per-domain ranges already in `calculation/deterministic/{domain}.yaml`:

```yaml
# calculation/summary/paper-budget.yaml
total_word_count:
  min: 4000
  max: 8000
  # A concrete system (pcems_2026, eswa_journal) overrides this to match
  # its actual venue's page/word limit — same override mechanism every
  # other calculation/ file already uses.
```

```markdown
# Use-case 4d — Section Budget Fit

**Depends on**: `section-supplementary-content` (4c)

**Script**: Per-domain, conditional loop (max 3 attempts) — deterministic
`check-word-budget.py` (reads `calculation/deterministic/{domain}.yaml`'s
`word_count_in_range` config) → if out of range: new `fit-to-budget`
(prompt, trim or expand toward the configured range, preserving all
citations from 4b and enrichment from 4c) → `persist-section-draft`
(stage=`budget-fit`) → re-check. If still out of range after 3 attempts,
persists anyway and flags for deterministic-audit (5) to catch as before —
this step doesn't invent a new failure mode, it just tries harder than
"generate once and audit."

**Inputs**: Each domain's `stage='enrich'` draft,
`calculation/deterministic/{domain}.yaml` per-domain range,
`calculation/summary/paper-budget.yaml` whole-paper total

**Action**: Fit each section into its configured min/max, and check the
running sum against the whole-paper total after all domains are fit — if
the sum still exceeds the total even with every domain individually
in-range, flag the largest domains (by word count) for another fit pass
biased toward `min` rather than the domain's own `max`.

**Completion criteria**:
- Every structural domain has >= 1 `academic_narratives` row with
  `stage='budget-fit'`
- `SUM(word_count) FROM academic_narratives WHERE stage='budget-fit'` is
  within `paper-budget.yaml`'s range

**Verify script**: `script/verify/uc4d_section_budget_fit.py --paper-id <id>`

**Rule**: Runs after 4c. Gates `deterministic-audit` (5) — a section that
never got a `stage='budget-fit'` row hasn't gone through the pipeline's
budget check yet.
```

## 5. New Usecase `4e` — Document Narrative Polish

Semantic *generation*, not audit — the counterpart to `5e`/`5f`'s
*measurement* of the same concerns (structure, narrative-arc, terminology
consistency). Placed after humanize (§2's ordering rationale) and before
the renumbered `5e`/`5f`, since those audits should score the *polished*
document, not the pre-polish one.

```markdown
# Use-case 4e — Document Narrative Polish

**Depends on**: `humanize-deterministic` (5c) + `humanize-semantic` (5d) —
both usecases always run to completion, even as a no-op when
plagiarism-forensic-audit (5b) flagged no domain (5c/5d's own completion
criteria are satisfied trivially in that case, same "always produces a
checkable row" pattern 4c uses for domains with nothing to enrich). 4e's
gate is on 5c+5d *completing*, not on any domain having actually been
rewritten.

**Script**: Whole-document, 3 sequential sub-steps (each reads the
previous step's output, not the original — genuinely sequential, not
parallel triads) —
1. `gather-document-evidence` (reused verbatim from `script/document-audit/
   gather_document_evidence.py` — its `concatenate_sections()` is already
   generic full-text concatenation keyed only on `_master-schema.yaml`
   order, not audit-specific; confirmed no `mode` param or score-oriented
   filtering exists in it today, so it's a direct import, not a new
   variant) → `structure-polish` (prompt — section ordering within each
   domain, heading consistency, transition sentences between domains) →
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
(not duplicated logic) as this usecase's own completion gate. **Design
constraint, to prevent a 4d↔4e fight**: `content-detail-polish` (sub-step
3) may not grow any single domain's word count by more than 10% over its
`stage='budget-fit'` (4d) value — enforced by the prompt's own
instructions plus a deterministic post-check in `persist-section-draft`
that rejects (and does not persist) a `content-detail-polish` result
exceeding the cap, re-running the sub-step once with an explicit
"tighten, don't lengthen further" instruction before accepting it as-is.
This caps the retry to O(1) per domain instead of an open-ended 4d⇄4e
cycle.

**Completion criteria**:
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
```

## 6. Audit Extension — Parts vs. Full, and the New Whole-Document Budget Check

### `5a-semantic-audit` — extended to run at two scopes per domain

Reuses `academic_semantic_runs.scope` (already exists, §0) rather than a
new table or a new usecase per part — the request for "multiple audits per
section" is multiple *runs* of the existing usecase, not multiple new
usecases:

```sql
-- schema/09-academic_semantic_runs.sql
scope TEXT NOT NULL DEFAULT 'section'
      CHECK (scope IN ('section-part','section-full','cross-section','document')),
```

(`'section'` renamed to `'section-full'` for clarity now that `'section-
part'` exists alongside it — no deployed rows yet, §5 of the prior
proposal already established that this table has no backward-compat
constraint.)

**Code impact of the rename** — the schema change alone isn't sufficient;
`script/common/academic_schema.py` hardcodes the old value in four
places and all four need to update:

1. The registered completion predicate `_uc_sem_audit`
   (`@_register_usecase("semantic-audit", ...)`, line 572-588): decorator
   description string and `WHERE scope='section'` query → `'section-full'`
2. `get_domain_scores(conn, paper_id, domain=None, scope="section")`
   (line 394): default param → `"section-full"`
3. `get_latest_semantic_score(conn, paper_id, domain, model="",
   scope="section")` (line 406): default param → `"section-full"`
4. `upsert_semantic_score(conn, paper_id, domain, model, score, result=None,
   scope="section", computed_against=None)` (line 346-358): default param
   → `"section-full"` **and** the conditional on line 355
   (`if scope == "section"`) must become `if scope in ("section-full",
   "section-part")` — both per-domain scopes require `domain_id` resolution,
   not just the old `"section"` value. This is not a trivial string swap
   like the other three.

`uc5a_semantic_audit.py` itself needs no change — it only calls
`usecase_status()`, which delegates to `_uc_sem_audit`, so the fix is
one function, not the verify script.

```markdown
# Use-case 5a — Semantic Audit (extended)

**Script**: Per-domain, two kinds of run —
- **Parts** (one run per new-stage artifact from 4b/4c/4d): `gather-
  domain-evidence` (mode=`audit-part`, scoped to just the citations table
  or just the enrichment diff or just the budget-fit diff) →
  `semantic-audit-part` (prompt, focused mini-rubric per part kind) →
  `persist-domain-semantic-score` (`scope='section-part'`)
- **Full** (unchanged from today): `gather-domain-evidence` (mode=`audit`)
  → `semantic-audit` (prompt, existing full-domain rubric) →
  `persist-domain-semantic-score` (`scope='section-full'`)

**Completion criteria**:
- >= 1 `scope='section-part'` run per (domain, part-kind) for
  `part-kind IN ('citations','enrichment','budget-fit')`
- >= 1 `scope='section-full'` run per domain (existing bar, unchanged)

**Rule**: Mandatory for every domain — both parts and full, no domain
skips either. (Existing "only runs for domains that passed deterministic
audit" rule is unchanged — parts audits for a domain that failed
deterministic don't run either.) **Decision, not left open**: a domain
where 4c was a no-op (nothing relevant to enrich) still gets a full
`scope='section-part'` run for `part-kind='enrichment'` — it trivially
passes (nothing changed, nothing to flag) but the run exists, same
uniform-completeness-predicate reasoning 4c itself uses for its own no-op
rows. No domain is exempt from the completion criteria's count.
```

### `5-deterministic-audit` — extended checks

New checks added to `calculation/deterministic/{domain}.yaml` files (same
rule engine, e.g. `min_citation_count` already exists on
`references.yaml:6` and generalizes trivially to per-domain minimums):

| Check | Applies to | Rule (existing engine) |
|---|---|---|
| `citation_marker_present` | 10 of 12 structural domains | `min_citation_count`, `config: {min: 1}` |
| `budget_fit_applied` | All 12 | new rule — `stage='budget-fit'` row exists |
| `word_count_in_range` | All 12 (existing, §0) | unchanged |

**`citation_marker_present` is excluded, not just set to `min: 0`, for
`abstract` and `title-and-metadata`** — not merely "evidence-free" (§0's
draft wording) but actively contradictory for `abstract`:
`calculation/deterministic/abstract.yaml:15-19` already has check `ab-003`
`no_citations` (warning severity) asserting the abstract should contain
*no* citation markers. Adding `citation_marker_present` with `min: 1` to
`abstract.yaml` would make deterministic-audit assert both "must have a
citation" and "must not have a citation" on the same domain. Both checks
are omitted from `abstract.yaml` and `title-and-metadata.yaml` entirely,
not added with `min: 0` — a `min: 0` check that always trivially passes
is dead weight the ladder says not to add.

**New — whole-document scope**, mirroring `academic_semantic_runs`'
already-established nullable-domain pattern (prior proposal §5):

```sql
-- schema/20-academic_deterministic_findings.sql
domain_id TEXT REFERENCES academic_domains(id) ON DELETE CASCADE,  -- now nullable
scope     TEXT NOT NULL DEFAULT 'section' CHECK (scope IN ('section','document')),  -- NEW
UNIQUE(paper_id, domain_id, scope, run_number)  -- was UNIQUE(paper_id, domain_id, run_number)
```

`document-semantic-audit` (renumbered `5f`, §7) gains one deterministic
pre-check before its semantic pass: total word count against
`calculation/summary/paper-budget.yaml`, written as a `scope='document'`,
`domain_id=NULL` row — same table, no new one, matching this proposal's
own §5 precedent for `academic_semantic_runs`.

## 7. Split `5c-humanize.md` → `5c` (Deterministic NLP Fix) + `5d` (Semantic LLM Fix)

Mirrors `5b`'s already-working pattern (`deterministic-fingerprint-check`
before `plagiarism-fingerprint-audit`) one usecase later than where it was
first applied.

**Renumbering** (frees `5d`/`5e` for the split; existing cross-section/
document audit files shift to `5e`/`5f` — filename letters aren't read by
`standard.yaml` or any verify script, they're purely the doc's own index,
so this is a rename with no code impact):

| Today | Becomes |
|---|---|
| `5c-humanize.md` | `5c-humanize-deterministic.md` |
| *(new)* | `5d-humanize-semantic.md` |
| `5d-cross-section-semantic-audit.md` | `5e-cross-section-semantic-audit.md` |
| `5e-document-semantic-audit.md` | `5f-document-semantic-audit.md` |

```markdown
# Use-case 5c — Humanize (Deterministic)

**Depends on**: `plagiarism-forensic-audit` (5b, FAIL after targeted
rewrite — unchanged trigger)

**Script**: Per-domain — `gather-humanize-context` (unchanged) → new
`nlp-fingerprint-fix.py` (deterministic — uses `textstat`/`nltk`-class
mechanical fixes: sentence-length variance normalization, parallel-
structure breaking, paragraph-length variation — Layer 1 of today's
`humanifier.md`, made deterministic instead of LLM-guessed) →
`persist-humanize-pass` (`pass_kind='deterministic'`)

**Inputs**: Flagged domain's draft, flagged spans from 5b

**Action**: Mechanical AI-fingerprint fixes a library can do reliably and
cheaply — same cost logic as 5b's own deterministic pre-screen: catch what
doesn't need an LLM call before paying for one.

**Completion criteria**:
- Every FAIL-flagged domain has >= 1 `academic_humanize_passes` row with
  `pass_kind='deterministic'`

**Verify script**: `script/verify/uc5c_humanize_deterministic.py --paper-id <id>`

**Rule**: Runs first. Re-checks against 5b's flagged patterns after
fixing — domains resolved by the deterministic pass alone skip 5d.
```

```markdown
# Use-case 5d — Humanize (Semantic)

**Depends on**: `humanize-deterministic` (5c — only for domains still
above the risk threshold after the deterministic pass)

**Script**: Per-domain — `gather-humanize-context` (re-run, now over the
5c-fixed draft) → `humanize-section` (prompt, trimmed to Layers 2-3 only —
technical DNA injection + voice restoration, since Layer 1 moved to 5c) →
`persist-humanize-pass` (`pass_kind='semantic'`)

**Completion criteria**:
- Every domain still FAIL after 5c has >= 1 `academic_humanize_passes`
  row with `pass_kind='semantic'`

**Verify script**: `script/verify/uc5d_humanize_semantic.py --paper-id <id>`

**Rule**: Only runs for domains still flagged after 5c. Gates `4e`
(document polish, §5) and the renumbered `5e`/`5f`.
```

**Schema change** — `academic_humanize_passes` gains `pass_kind`, and its
UNIQUE constraint must widen to match: today's
`UNIQUE(paper_id, domain_id, iteration)`
(`schema/13-academic_humanize_passes.sql:15`) would collide the moment 5c
and 5d write passes for the same domain at the same `iteration` — which
is exactly what this split does on every domain that reaches 5d. Left
unchanged, the 5d insert either fails the UNIQUE constraint or (depending
on `persist_humanize_pass.py`'s upsert logic) silently overwrites 5c's
row, losing the deterministic pass's own `change_summary`/`risk_flags`:

```sql
-- schema/13-academic_humanize_passes.sql
pass_kind TEXT NOT NULL DEFAULT 'semantic'
          CHECK (pass_kind IN ('deterministic','semantic')),  -- NEW
-- UNIQUE(paper_id, domain_id, iteration) becomes:
UNIQUE(paper_id, domain_id, iteration, pass_kind)
```

## 8. Schema Changes — Consolidated

| File | Change |
|---|---|
| `schema/07-academic_narratives.sql` | `stage` CHECK grows to `('generate','cite','enrich','budget-fit','polish','humanize')` — reverses the file's own "folded into generation" comment (§4) |
| `schema/09-academic_semantic_runs.sql` | `scope` CHECK becomes `('section-part','section-full','cross-section','document')` (§6) |
| `schema/13-academic_humanize_passes.sql` | New `pass_kind` column, `CHECK IN ('deterministic','semantic')`; UNIQUE constraint widens from `(paper_id, domain_id, iteration)` to `(paper_id, domain_id, iteration, pass_kind)` — without this, 5c's and 5d's rows for the same domain+iteration collide (§7) |
| `schema/20-academic_deterministic_findings.sql` | `domain_id` becomes nullable, new `scope` column `CHECK IN ('section','document')`, UNIQUE constraint gains `scope` (§6) |
| `schema/21-academic_section_citations.sql` **(new)** | New table — citations per (paper, domain), `source_kind IN ('in-repo','literature')` (§4) |

No migration/backfill for any of these — same standing precedent as the
prior proposal (§5 there): no `base_academic` rows are deployed yet, so
every `schema/*.sql` file is edited in place with its final shape.

## 9. Full Dependency Graph — All Usecases (Post-Split)

| Usecase | Depends on | Verify script |
|---|---|---|
| `schema-init` | — | `uc0_schema_init.py` |
| `classify-repo` | `schema-init` | `uc0b_classify_repo.py` |
| `novelty-analysis` | `classify-repo` (HAS_DOCS) | `uc1_novelty.py` |
| `gap-analysis` | `classify-repo` (HAS_DOCS) | `uc2_gaps.py` |
| `mathematics-analysis` (**3a**, split) | `classify-repo` (HAS_DOCS) | `uc3a_math_analysis.py` |
| `diagram-architecture-analysis` (**3b**, split) | `classify-repo` (HAS_DOCS) | `uc3b_diagram_architecture.py` |
| `generate-section-draft` (**4a**, split) | `novelty` + `gap` + `3a` + `3b` | `uc4a_generate_section.py` |
| `section-citations` (**4b**, new) | `4a` | `uc4b_section_citations.py` |
| `section-supplementary-content` (**4c**, new) | `4b` + `3a` + `3b` | `uc4c_section_enrichment.py` |
| `section-budget-fit` (**4d**, new) | `4c` | `uc4d_section_budget_fit.py` |
| `deterministic-audit` | `4d` (per domain) | `uc5_det_audit.py` (extended checks, §6) |
| `semantic-audit` | `deterministic-audit` (per domain, PASS) | `uc5a_semantic_audit.py` (extended scopes, §6) |
| `plagiarism-forensic-audit` | `4d` (per domain) — same relationship as today's `assemble-paper-structure` dependency, target renamed since that usecase is what split into `4a`-`4d` (§4); still "runs once the domain has a finished pre-audit draft" | `uc5b_plagiarism.py` |
| `humanize-deterministic` (**5c**, split) | `plagiarism-forensic-audit` (FAIL) | `uc5c_humanize_deterministic.py` |
| `humanize-semantic` (**5d**, new) | `5c` (still FAIL) | `uc5d_humanize_semantic.py` |
| `document-narrative-polish` (**4e**, new) | `5c` + `5d` (both always complete, no-op or not — §5) | `uc4e_document_polish.py` |
| `cross-section-semantic-audit` (**5e**, renumbered) | `4e` | `uc5e_cross_section_audit.py` |
| `document-semantic-audit` (**5f**, renumbered) | `5e` | `uc5f_document_audit.py` (adds §6's document-scope deterministic check) |
| `calculate` | `semantic-audit` + `deterministic-audit` + `5e` + `5f` | `uc6_calculate.py` |
| `render-charts` | `calculate` | `uc6a_render_charts.py` |
| `render-audit-report` | `render-charts` | `uc6b_render_audit_report.py` |
| `render-paper` | `5f` (PASS) | `uc6c_render_paper.py` |

**File count.** `plan/usecase/` goes from 16 files to 22: `3` splits to
`3a`/`3b` (net +1), `4` splits to `4a`/`4b`/`4c`/`4d` (net +3), `4e` is new
(+1), `5c` splits to `5c`/`5d` with `5d`/`5e` renumbered to `5e`/`5f`
(net +1). 22 verify scripts total (16 existing renamed/extended in place +
6 new: `3a`, `3b` replace `3`'s single script; `4a`-`4d` replace `4`'s;
`4e`, `5d` are wholly new).

## 10. New/Changed Scripts, Prompts, Calculation Files — Consolidated

**New scripts:**

| File | Purpose |
|---|---|
| `script/assemble-paper-structure/persist_section_citations.py` | Writes `academic_section_citations` (§4b) |
| `script/assemble-paper-structure/collate_references.py` | Builds `references` domain draft from collated citations (§4b) |
| `script/assemble-paper-structure/check_word_budget.py` | Deterministic word-count check against `calculation/deterministic/{domain}.yaml` + `paper-budget.yaml` (§4d) |
| `script/humanize/nlp_fingerprint_fix.py` | Deterministic mechanical fixes (sentence-length variance, parallel-structure breaking) (§7) |
| 6 new verify scripts | §9's table |

**Changed scripts:**

| File | Change |
|---|---|
| `script/common/academic_schema.py` | 4 call sites (§6's code-impact note): `_uc_sem_audit`'s decorator string + `WHERE scope='section'` → `'section-full'`; `get_domain_scores()`, `get_latest_semantic_score()`, and `upsert_semantic_score()` default params → `"section-full"`; `upsert_semantic_score()` line 355 conditional → `if scope in ("section-full", "section-part")` (not a trivial string swap — both per-domain scopes need `domain_id` resolution) |
| `script/humanize/persist_humanize_pass.py` | Gains `pass_kind` param, passed through to the new column (§7) |
| `script/assemble-paper-structure/persist_section_draft.py` | No signature change — `stage` was already a passthrough param (§4); gains the `content-detail-polish` 10%-cap rejection check used by 4e (§5) |

**New prompts:**

| File | Purpose |
|---|---|
| `prompt/assemble-paper-structure/section-enrichment.md` | 4c's math/table/diagram weaving pass |
| `prompt/assemble-paper-structure/fit-to-budget.md` | 4d's trim/expand pass |
| `prompt/document-polish/structure-polish.md` | 4e sub-step 1 |
| `prompt/document-polish/narrative-style-polish.md` | 4e sub-step 2 |
| `prompt/document-polish/content-detail-polish.md` | 4e sub-step 3 |
| `prompt/semantic-audit/semantic-audit-part.md` | 5a's parts-scope rubric (citations/enrichment/budget-fit mini-rubrics) |

**Changed prompts:**

| File | Change |
|---|---|
| `prompt/assemble-paper-structure/generate-section.md` | Rule 1 narrows to in-repo grounding only (external lit moves to 4b); Rule 4 narrows to headings/flow (math/table weaving moves to 4c) |
| `prompt/humanize/humanifier.md` | Splits into `humanifier.md` (Layers 2-3 only, 5d) — Layer 1 becomes `nlp_fingerprint_fix.py`'s deterministic logic, not a prompt |

**New/changed calculation files:**

| File | Change |
|---|---|
| `calculation/summary/paper-budget.yaml` **(new)** | Whole-paper `total_word_count` range (§4d) |
| `calculation/deterministic/{domain}.yaml` (all 12) | New `citation_marker_present`, `budget_fit_applied` checks (§6) |
| `calculation/semantic/document/{domain}.md` (per-domain rubrics, existing) | No change — still back `scope='section-full'` runs |
| `calculation/semantic/section-parts.yaml` **(new)** | Mini-rubrics for `citations`/`enrichment`/`budget-fit` parts audits (§6) |

## 11. Open Questions

- **`fit-to-budget`'s trim strategy when a section is far over budget** —
  whether the prompt should be told to cut whole paragraphs (risking lost
  claims that then fail deterministic audit for missing content) or
  compress sentence-by-sentence (safer, may not reach the target). Left to
  the prompt's own design, not resolved here — same "not this proposal's
  job to write the finished prompt text" boundary as §12.
- ~~`document-narrative-polish` (4e) budget re-violation~~ — resolved in
  §5: 10% per-domain growth cap on `content-detail-polish`, plus a bounded
  single re-invocation of 4d's fit script if the whole-paper sum still
  exceeds budget after the cap.
- ~~Per-domain parts audit granularity for a no-op 4c~~ — resolved in §6:
  still runs, trivially passes, no domain is exempt from the count.

## 12. Explicitly Out of Scope

The full text of all 6 new usecase files beyond the worked shape above (§3-
§7 give complete bodies, but §9's table is the authority on final naming —
any prose/wording refinement at authoring time is not fixed by this
document), the 6 new prompts' actual instruction text beyond the one-line
purpose in §10, `nlp_fingerprint_fix.py`'s actual NLP-library choice and
implementation (whether `textstat`, `nltk`, or a hand-rolled sentence-
length/parallel-structure detector — a library-selection call, not a
granularity call), `collate_references.py`'s citation-formatting/dedup
logic, `fit-to-budget.md`'s exact trim/expand instructions, and the 3
`document-polish/*.md` prompts' exact rubric wording. This proposal
specifies each new usecase's location, dependency, data source, schema
shape, and completion-predicate — not its finished prompt or script text.
