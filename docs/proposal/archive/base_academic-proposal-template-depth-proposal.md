# base_academic — Proposal Template Depth Proposal

## 0. Why This Document Exists

The proposal-gate feature (`base_academic-proposal-gate-workflow-
proposal.md`, implemented) added a fourth template kind,
`templates/proposal/**`, so a human reviews what generation/audit/
report/fix is about to do before it happens. Comparing what actually
shipped against the other two template kinds it sits alongside:

- **`templates/generation/markdown/{domain}.md`** (worked example,
  `methodology.md`, confirmed on disk): 4 named content sections
  (`Overview`, `Algorithm/Procedure`, `Complexity Analysis`,
  `Architecture`) plus a `{{#citations}}` loop. Bounded shape, model
  fills named slots.
- **`templates/report/markdown/domain/{domain}/summary.md`** (confirmed
  on disk): 100% computed fields — `final_score`, `score_band`,
  `deterministic_score`, `semantic_score`, `trend` — zero free text.
  Every number traces to a specific SQL query
  (`generate_audit_report.py`'s `_get_single_domain_summary_data()`).
- **`templates/proposal/markdown/{generation,audit,report,fix}.md`**
  (confirmed on disk, all four): one header line
  (`commit`/`status`/`source`/`iteration`), one `{{ summary }}` field,
  then `{{{ content_md }}}` — a single opaque blob of free text the
  drafting prompt wrote, with **zero structured, script-verified
  fields in the body**. Every other template kind in the system is
  either fully computed (report) or bounded-and-labeled free text
  (generation); the proposal template is the only kind where the entire
  content a human is approving comes from unstructured prose written by
  the same model whose future work that approval unblocks.
- **`gather_proposal_context.py`'s audit branch returns literal
  placeholder strings, not data** (confirmed on disk,
  `_gather_audit_context()`, lines 82-88):
  ```python
  domain_details.append({
      "domain_key": key,
      "det_rule_count": "(from deterministic rules)",
      "rubric_summary": "(from semantic rubric)",
  })
  ```
  These two fields were specified in the original proposal's §4 worked
  example as real numbers/summaries. They ship as the literal strings
  above, for every domain, on every run — the audit-proposal prompt
  receives no actual rule count or rubric content, just a string that
  says "(from deterministic rules)". The model drafting the proposal
  has to either invent plausible-sounding numbers or omit them; a
  reviewer reading the rendered proposal cannot tell which.
- **Real per-domain rule data exists and is already loaded elsewhere in
  the same pipeline** — `calculation/generation/{domain}.yaml`
  (confirmed, `methodology.yaml`: 10 checks — `word_count_in_range`
  `min:600/max:1500`, `min_diagram_count min:1`, `min_formula_count
  min:1`, `min_citation_count min:1`, plus 6 more, each with `id`,
  `severity`, `description`) is read by both `check_word_budget.py`
  (generation-time) and `deterministic_audit.py` (audit-time,
  `generation-content-depth-and-verification-proposal.md`, implemented).
  A third reader — `gather_proposal_context.py`'s audit branch — could
  load the same file and report `"10 checks (3 critical, 7 warning):
  word count 600-1500, ≥1 diagram, ≥1 formula, ≥1 citation..."` instead
  of a placeholder string. It doesn't.
- **The semantic rubric file it should summarize exists too** —
  `prompt/semantic-audit/semantic-audit.md` names its rubric source
  explicitly: `audit/semantic/document/{domain}.md` — "scoring criteria
  with weights and pass/fail thresholds." `_gather_audit_context()`
  never opens this file.
- **`_gather_generation_context()`'s analysis summaries are truncated to
  500 characters with no indication anything was cut** (confirmed,
  line 51: `analyses[kind] = row["content"][:500] if row else
  "(none yet)"`) — a novelty or gap analysis longer than 500 characters
  (the normal case — these are full cross-module analysis documents)
  silently loses its second half before the drafting prompt ever sees
  it, with no `"..."` or truncation marker in the string itself.
- **`_gather_fix_context()`'s `triggering_finding` is a raw, unparsed
  JSON string** (confirmed, line 133: `triggering_finding =
  finding_row["findings"]` — `findings` is `academic_deterministic_
  findings.findings`, documented in schema/20 as "a JSON array of
  `{check_id, rule, passed, detail}` objects"). The fix-proposal prompt
  receives `"[{\"check_id\": \"me-001\", \"rule\": \"word_count_in_
  range\", \"passed\": false, ...}]"` as a literal string to read, not
  a list it can iterate — every fix proposal has to re-parse JSON
  inline in its own reasoning instead of being handed the failed
  checks' names directly.
- **`_gather_report_context()`'s `report_kinds` reports the past, not
  the future** (confirmed, lines 103-105: `SELECT DISTINCT report_kind
  FROM academic_report_history WHERE paper_id=?`) — this is what has
  *already* rendered on prior runs, not what the render this proposal
  is gating is about to (re)produce. On a paper's first-ever report run
  it's an empty list — a report proposal for the very first render says
  nothing about what will be created.

## 1. Scope

`script/propose/gather_proposal_context.py` (all four `_gather_*`
functions gain real, computed fields — no behavior change to its
`--repo-root/--in/--out` contract or its phase dispatch), the four
`templates/proposal/{markdown,html}/*.{md,html}` files (gain a
structured, computed-fields section above `{{{ content_md }}}`, same
"facts vs. narrative" split report templates already use), and the four
`prompt/propose/*.md` files (updated `## Input` sections documenting the
new fields, so the drafting prompt states what to do with numbers it
now actually receives instead of prose-summarizing them itself). Does
not touch `persist_proposal.py`, `render_proposal.py`,
`approve_proposal.py`, `request_fix.py`, `academic_schema.py`'s
predicates, `standard.yaml`'s step wiring, `loop.yaml`, or
`run_full_workflow.py`'s checkpoints — none of those need to change for
a proposal to carry more accurate content; this is entirely a
context-richness and template-structure fix within the existing four
`propose-*` usecases' existing step shape.

## 2. The Core Fix — Facts Are Computed, Narrative Is Written

Every field a reviewer needs to trust without re-deriving it themselves
(a rule count, a rubric's criteria, which report files will change, a
failed check's name) becomes a **computed field**, populated by
`gather_proposal_context.py` from the same source files
`deterministic_audit.py`/`check_word_budget.py`/`generate_audit_report.py`
already read — never restated in prose by the drafting prompt. `content_md`
stays for what only a model can produce: *why* this evidence supports
this domain, *what changed* since a rejection, *which* domain a vague
user comment is actually about. This is the same split
`templates/report/**` already enforces between `summary.md` (all
computed) and the generation templates (all prose) — proposal templates
currently have no equivalent split at all (§0).

## 3. `gather_proposal_context.py` — Real Fields Per Phase

### 3a. `_gather_generation_context()` — budget + minimums per domain, untruncated analysis

```python
def _load_generation_rules(domain_key):
    """calculation/generation/{domain}.yaml's checks — same file
    check_word_budget.py and deterministic_audit.py already read
    (generation-content-depth-and-verification-proposal.md §5b: one
    file serves both stages so a rule change doesn't need syncing)."""
    path = os.path.join(_CALC_GEN_DIR, f"{domain_key}.yaml")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    checks = data.get("checks", [])
    wc = next((c["config"] for c in checks if c.get("rule") == "word_count_in_range"), None)
    return {
        "word_min": wc.get("min") if wc else None,
        "word_max": wc.get("max") if wc else None,
        "check_count": len(checks),
        "critical_count": sum(1 for c in checks if c.get("severity") == "critical"),
        "check_names": [c["name"] for c in checks],
    }
```

`_gather_generation_context()`'s `domain_details` entries gain
`word_min`/`word_max`/`check_count`/`critical_count`/`check_names` from
this helper, alongside the existing `domain_key`/`stage`. Analysis
summaries lose the silent 500-character cut — either the full `content`
(these are already stored as a single row's `TEXT` column, not paginated,
so there's no size concern the truncation was ever protecting against)
or, if a length cap is still wanted for a large-repo edge case, an
explicit `"... [truncated, N chars total]"` suffix so a reviewer can
tell content was cut rather than assuming they read all of it.

### 3b. `_gather_audit_context()` — the placeholder strings, replaced

```python
def _load_semantic_rubric(domain_key):
    """audit/semantic/document/{domain}.md — the file prompt/semantic-
    audit/semantic-audit.md names as its rubric source. Returns None if
    absent (the audit itself would fail the same way at run time —
    semantic-audit.md's own §Rules: 'If the rubric file does not exist,
    return an error')."""
    path = os.path.join("audit", "semantic", "document", f"{domain_key}.md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    criterion_count = text.count("\n- **C")  # rubric's own criterion-list convention
    return {"criterion_count": criterion_count, "rubric_path": path}


def _gather_audit_context(conn, paper_id, models=None):
    domains = [r[0] for r in conn.execute(
        "SELECT key FROM academic_domains ORDER BY sort_order").fetchall()]
    domain_details = []
    for key in domains:
        rules = _load_generation_rules(key)  # §3a's helper, reused —
                                              # same file, same audit-time meaning
        rubric = _load_semantic_rubric(key)
        domain_details.append({
            "domain_key": key,
            "det_rule_count": rules["check_count"] if rules else 0,
            "det_critical_count": rules["critical_count"] if rules else 0,
            "rubric_criterion_count": rubric["criterion_count"] if rubric else 0,
            "rubric_found": rubric is not None,
        })
    return {"domains": domain_details, "models": models or ["default"]}
```

No placeholder strings survive — a domain with no rule file reports
`det_rule_count: 0`, honestly, rather than a string implying data that
isn't there. `_load_generation_rules()` is shared with §3a rather than
duplicated (one file, one meaning, one reader — same "don't implement
the same rule twice" reasoning the generation-content-depth proposal
already applied to `check_word_budget.py`/`deterministic_audit.py`).

### 3c. `_gather_report_context()` — what will render, not what already did

```python
def _gather_report_context(conn, paper_id):
    domains = [r[0] for r in conn.execute(
        "SELECT key FROM academic_domains ORDER BY sort_order").fetchall()]
    score_row = conn.execute(
        "SELECT final_score, score_band FROM academic_score_history "
        "WHERE paper_id=? AND domain_id IS NULL "
        "ORDER BY calculated_at DESC LIMIT 1", (paper_id,)).fetchone()
    # The 6 per-domain report kinds (report-granularity-and-audit-
    # governance-proposal.md §2b) x every domain, plus the 2 whole-run
    # reports — this is what render-charts/render-audit-report/
    # render-paper are about to (re)write, not a history query.
    per_domain_kinds = ["deterministic", "semantic-full", "semantic-part",
                        "plagiarism", "humanize", "summary"]
    return {
        "current_final_score": score_row["final_score"] if score_row else None,
        "current_score_band": score_row["score_band"] if score_row else None,
        "domain_count": len(domains),
        "per_domain_kind_count": len(per_domain_kinds),
        "total_domain_reports": len(domains) * len(per_domain_kinds),
        "whole_run_reports": ["pipeline-progress", "whole-paper-summary"],
    }
```

Fixes both the `domain_id IS NULL` gap (the original query had no such
filter — on a paper with per-domain score rows already in
`academic_score_history`, `ORDER BY created_at DESC LIMIT 1` could
return a per-domain row instead of the whole-paper one, reporting the
wrong score entirely) and the past-vs-future gap (§0): a first-time
report proposal now says "72 domain reports + 2 whole-run reports will
be produced," not an empty list.

### 3d. `_gather_fix_context()` — parsed findings, not a JSON string

```python
def _gather_fix_context(conn, paper_id, domain_id, user_comment):
    ...
    triggering_findings = []
    if target_domain:
        finding_row = conn.execute(
            "SELECT findings FROM academic_deterministic_findings "
            "WHERE paper_id=? AND domain_id=? AND verdict='FAIL' "
            "ORDER BY created_at DESC LIMIT 1",
            (paper_id, target_domain["id"])).fetchone()
        if finding_row:
            all_checks = json.loads(finding_row["findings"])
            triggering_findings = [c for c in all_checks if not c.get("passed")]
    return {
        "target_domain": target_domain,
        "user_comment": user_comment,
        "triggering_findings": triggering_findings,  # list of {check_id, rule, detail}, not a JSON string
        "triggering_finding_count": len(triggering_findings),
    }
```

## 4. Templates — Computed Header Table Above `content_md`

Each of the four markdown templates gains a structured block between the
existing metadata line and `{{{ content_md }}}` — mirrors `summary.md`'s
all-computed shape (§0), never touched by the drafting prompt:

`generation.md`, new block:
```
## What Will Be Generated (computed)

| Domain | Stage | Word Range | Rule Checks (critical) |
|---|---|---|---|
{{#domains}}
| {{ domain_key }} | {{ stage }} | {{ word_min }}-{{ word_max }} | {{ check_count }} ({{ critical_count }}) |
{{/domains}}
```

`audit.md`, new block:
```
## What Will Be Audited (computed)

**Models this round:** {{#models}}{{ . }} {{/models}}

| Domain | Deterministic Checks | Rubric Criteria |
|---|---|---|
{{#domains}}
| {{ domain_key }} | {{ det_rule_count }} ({{ det_critical_count }} critical) | {{#rubric_found}}{{ rubric_criterion_count }}{{/rubric_found}}{{^rubric_found}}rubric not found{{/rubric_found}} |
{{/domains}}
```

`report.md`, new block:
```
## What Will Render (computed)

**Current score:** {{ current_final_score }} ({{ current_score_band }})
**Per-domain reports:** {{ total_domain_reports }} ({{ domain_count }} domains × {{ per_domain_kind_count }} kinds)
**Whole-run reports:** {{#whole_run_reports}}{{ . }} {{/whole_run_reports}}
```

`fix.md`, new block:
```
## Failing Checks This Fix Addresses (computed)

{{#triggering_findings}}
- **{{ rule }}** ({{ check_id }}): {{ detail }}
{{/triggering_findings}}
{{^triggering_findings}}
(no deterministic findings — this fix is driven by `user_comment` alone)
{{/triggering_findings}}
```

HTML templates gain the equivalent `<table>` block, matching
`whole-paper-summary.html`'s existing table markup style (already the
precedent every report HTML template follows). `{{{ content_md }}}`
stays exactly where it is in all eight files — this is additive, not a
restructure of what already renders correctly.

## 5. Prompts — Document What the Model No Longer Has to Restate

Each `prompt/propose/*.md`'s `## Input` section gains one line per new
field (e.g. audit-proposal.md: "`domains[].det_rule_count`,
`domains[].rubric_criterion_count` — already computed, the template
renders these directly; don't repeat them in `content_md`, write about
what they *mean* for this round instead"). This is the point of §2's
split: the prompt's job narrows to reasoning a human still needs (why,
what changed, which domain), not restating numbers a table now shows
more reliably than prose can.

## 6. New/Changed Files — Consolidated

| File | Change |
|---|---|
| `script/propose/gather_proposal_context.py` | `_load_generation_rules()` + `_load_semantic_rubric()` new helpers (§3a/§3b); all four `_gather_*` functions gain computed fields, `_gather_audit_context()`'s two placeholder strings removed entirely (§3b); `_gather_report_context()`'s score query gains `domain_id IS NULL` (bug fix, §3c) and reports forward-looking counts instead of history; `_gather_fix_context()` parses `findings` JSON instead of passing it through as a string (§3d) |
| `templates/proposal/markdown/{generation,audit,report,fix}.md` | New computed-fields block above `{{{ content_md }}}` (§4) |
| `templates/proposal/html/{generation,audit,report,fix}.html` | Same block as `<table>` markup (§4) |
| `prompt/propose/{generation,audit,report,fix}-proposal.md` | `## Input` documents the new computed fields; rules note not to restate them in `content_md` (§5) |

## 7. Explicitly Out of Scope

Any change to `persist_proposal.py`/`render_proposal.py`/
`approve_proposal.py`/`request_fix.py` (none of the new fields change
what gets persisted or how approval works — `content_md` is still one
`TEXT` column, the computed fields are template-render-time additions
sourced fresh from `gather_proposal_context.py`'s envelope each time,
same as `report_kinds`/`current_final_score` already are today), any
change to `academic_schema.py`'s five proposal predicates or
`standard.yaml`'s step wiring (the four `propose-*` usecases keep their
existing 4-step shape — gather/prompt/persist/render — this proposal
only deepens what step 1 gathers and what steps 3-4's template renders),
`audit/semantic/document/{domain}.md`'s own rubric file format (read,
not changed, by §3b's new helper — if a concrete system's rubric files
don't follow the `- **C1**...` criterion-list convention
`_load_semantic_rubric()` counts against, `criterion_count` degrades to
`0` the same way a missing rule file already degrades to `det_rule_count:
0`, never a crash), and per-domain proposal granularity (still one
proposal per phase per run, `base_academic-proposal-gate-workflow-
proposal.md` §2/§11 — the computed table inside that one document is
what's deepening, not the number of proposals a reviewer approves).
