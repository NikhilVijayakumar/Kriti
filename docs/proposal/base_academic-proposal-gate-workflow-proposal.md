# base_academic — Proposal-Gate Workflow (Generation / Audit / Report / Fix) Proposal

*Rev 2 — corrects phase-ordering, `expand_triads()`, `schema-init`, and
rejection-flow gaps found in review of Rev 1. Changes from Rev 1 are
called out inline where the correction isn't self-evident.*

## 0. Why This Document Exists

Every phase of the pipeline — generate a domain's draft, audit it, render
its report, fix what fails — runs today the instant its dependency
predicate is satisfied. Nothing stops between "inputs are ready" and "AI
writes to the database." Confirmed on disk today:

- **No `proposal` concept exists anywhere in the standard.** `templates/`
  has exactly two top-level kinds, `generation/` and `report/` (confirmed
  directory listing) — no `templates/proposal/`. `schema/` has 21
  numbered files, ending at `21-academic_section_citations.sql` — no
  proposal/approval table. `academic_schema.py`'s `_USECASE_PREDICATES`
  registry has no usecase whose name contains "propose" or "approve".
- **`run_full_workflow.py` runs every phase unattended, back to back**
  (confirmed by reading `main()` end to end, not just its docstring —
  see §9's corrected phase map, which replaces Rev 1's docstring-only
  reading). The only thing resembling a gate is `tier_gate`
  (`plan/core/loop.yaml:92-94`) — a score threshold, not a human
  approval.
- **`fix_loop` (`plan/core/loop.yaml:82-90`) already describes the right
  *mechanism* for fixing** ("feed the finding into the domain's own
  generation template's `## Audit Fix slot` and regenerate the whole
  domain document, then re-audit") — but its `trigger` is purely
  mechanical (`Path B AND final_score < threshold.score`) and it has no
  user-comment input at all. A user who wants to say "fix the
  methodology section, it's missing the ablation table" today has no
  entry point.
- **The report layer (already built, implemented, archived) covers the
  *after-the-fact* view** — once an audit has run, its findings render
  to `docs/paper/paper-{id}/audit/domain/{domain}/*.md|html`. That
  mechanism is correct and untouched by this proposal. The gap this
  proposal closes is the *before-the-fact* view: nothing today tells a
  user, in a reviewable document, what generation/audit/report/fix is
  about to do before it happens.
- **`_uc_schema_init`'s required-table set is already short one table**
  (`academic_schema.py:557-568`): it lists 19 names, but 21
  `schema/*.sql` files exist. Confirmed by diff: the required set is
  missing `academic_section_citations` (schema file 21) — a pre-existing
  bug, unrelated to this proposal, that this proposal fixes in the same
  edit as adding the 22nd table (§5), since both changes touch the same
  set literal.

## 1. Scope and Conventions

**Path convention** (matches every prior proposal in this series,
established by `base_academic-proposal.md`'s "proposed path
`academic/base_academic/`"): every path below is relative to
`samgraha/system/academic/base_academic/` unless given as a full repo
path (`docs/paper/...`, `docs/proposal/...`). Not restated per-path, same
as the report-granularity and generation-content-depth proposals it sits
alongside.

Touches: a new fourth template kind, `templates/proposal/**`; a new
`academic_proposals` table; five new usecases registered as **literal
`steps:` blocks in `script/schema/standard.yaml`** (§9b — not
`expand_triads()`, see §9a for why); `script/propose/` (4 scripts) and
`prompt/propose/` (4 prompts); `academic_schema.py` (5 new predicate
registrations + the pre-existing `schema-init` required-set fix, §5);
`plan/core/loop.yaml` (new `proposal_gate:` section + one clause on
`fix_loop.mechanism`); and `run_full_workflow.py` (checkpoint/pause/
resume at the three correct insertion points, §9). Does not touch the
report-rendering layer, the generation templates' content shape, or add
any new MCP tool (§8).

## 2. Core Mechanism — Propose, Then Approve, Then Execute

One rule, applied at four points in the pipeline:

> A phase's usecases (generation's chain, audit's chain, report's
> render chain, or a fix's regenerate-then-reaudit cycle) may not start
> until an `academic_proposals` row for `(paper_id, phase, commit_sha)`
> exists with `status='approved'`.

A proposal is **one document per phase per run**, not one per domain —
the reviewer decides "should this whole batch of work happen," the same
"cross-domain view" shape `pipeline-progress.md`/`whole-paper-summary.md`
already use, not the "one file per domain" shape the report layer uses
for post-hoc findings (§11 explains why per-domain proposals were
rejected).

## 3. Schema — `academic_proposals`

```sql
-- schema/22-academic_proposals.sql
-- One row per proposal draft/decision. A phase's *latest* row for a given
-- (paper, phase, scope_domain) is authoritative — same is_latest pattern
-- as academic_report_history (schema/18).
--
-- status lifecycle: pending -> approved | rejected (terminal, human-
-- decided, immutable once set — is_latest flipping to 0 later does NOT
-- change a decided row's status, it stays true history). A *pending* row
-- that gets superseded by a redraft *before* anyone decided it (stale
-- context, new commit) flips to status='superseded' instead — the one
-- case persist_proposal.py is allowed to rewrite status on an old row
-- (§7b). rejected != superseded: rejected means a human said no;
-- superseded means nobody ever got the chance to decide before the
-- draft went stale.

CREATE TABLE IF NOT EXISTS academic_proposals (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    phase           TEXT    NOT NULL CHECK (phase IN ('generation','audit','report','fix')),
    scope_domain_id INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    -- NULL = whole-paper scope (generation/audit/report, and most fix
    -- proposals). Set only when a fix proposal targets one named domain.
    source          TEXT    NOT NULL CHECK (source IN ('pipeline','user-request')),
    status          TEXT    NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','approved','rejected','superseded')),
    commit_sha      TEXT    NOT NULL DEFAULT '',
    -- same mechanism as academic_deterministic_findings.commit_sha
    -- (report-granularity proposal §4b).
    iteration       INTEGER NOT NULL DEFAULT 0,
    -- redraft count for this (paper, phase, scope_domain) — mirrors
    -- fix_loop.max_iterations (loop.yaml), reused as the same ceiling
    -- for repeated rejection, §6b.
    summary         TEXT    NOT NULL DEFAULT '',
    content_md      TEXT    NOT NULL,
    user_comment    TEXT    NOT NULL DEFAULT '',
    -- raw text driving a user-request fix proposal, OR a rejection
    -- reason on a decided row (§6b) — same column, different moment.
    is_latest       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT    NOT NULL,
    decided_at      TEXT
);
CREATE INDEX IF NOT EXISTS idx_academic_proposals_lookup
    ON academic_proposals(paper_id, phase, scope_domain_id, is_latest);
```

## 4. Templates — `templates/proposal/{markdown,html}/{phase}.{md,html}`

Eight files (4 phases × 2 formats), each a whole-run document (§2):

```
templates/proposal/markdown/generation.md
templates/proposal/markdown/audit.md
templates/proposal/markdown/report.md
templates/proposal/markdown/fix.md
templates/proposal/html/{generation,audit,report,fix}.html
```

`generation.md`:

```
# Generation Proposal — {{ title }}

**Paper ID:** {{ paper_id }}  **Commit:** {{ commit_sha }}  **Status:** {{ status }}
{{#user_comment}}**Prior rejection:** {{ user_comment }}{{/user_comment}}

## What Will Be Generated

{{#domains}}
- **{{ domain_key }}** — {{ content_summary }}
  (grounded in: {{#evidence_sources}}{{ . }}, {{/evidence_sources}})
{{/domains}}

## Upstream Analysis This Proposal Is Based On

- Novelty: {{ novelty_summary }}
- Gaps: {{ gaps_summary }}
- Mathematics: {{ math_summary }}
- Architecture/diagrams: {{ diagram_summary }}

## Approve

Run `approve-proposal --phase generation` after review, or `--reject
--reason "..."` to send back for a redraft (§6b).
```

`audit.md` — same header block, then:

```
## What Will Be Audited

{{#domains}}
- **{{ domain_key }}** — deterministic: {{ det_rule_count }} rules
  (`calculation/generation/{{ domain_key }}.yaml`); semantic rubric:
  {{ rubric_summary }}
{{/domains}}

## Models This Round

{{#models}}- {{ . }}{{/models}}
<!-- from --models, threaded through gather-proposal-context's
     phase=audit branch (§12, resolves Rev-1-review #12) -->
```

`report.md` — same header block, then:

```
## Report Artifacts This Run Will Produce

{{#report_kinds}}- `docs/paper/paper-{{ paper_id }}/audit/{{ . }}`{{/report_kinds}}
- Whole-paper score at time of proposal: {{ current_final_score }} ({{ current_score_band }})
```

`fix.md` — same header block, then:

```
## What Will Change

**Source:** {{ source }}  **Target domain:** {{ target_domain }}
{{#user_comment}}**User request:** {{ user_comment }}{{/user_comment}}
{{^user_comment}}**Triggering finding:** {{ triggering_finding }}{{/user_comment}}

**Current content (excerpt):**
{{ current_excerpt }}

**Proposed change:**
{{ change_summary }}
```

Rendered output lands at `docs/paper/paper-{id}/proposal/{phase}.md` and
`.html` — sibling of the existing `docs/paper/paper-{id}/audit/...` tree.

## 5. `academic_schema.py` — Predicates + the Pre-Existing `schema-init` Fix

Five new `_register_usecase_fn`/`_register_usecase` entries, plus one
one-line fix to the existing `_uc_schema_init` required set (§0):

```python
@_register_usecase("schema-init", "22 academic_* tables exist")
def _uc_schema_init(conn, paper_id):
    ...
    required = {
        "academic_papers", "academic_repos", "academic_domains",
        "academic_modules", "academic_module_analysis",
        "academic_cross_module_analysis", "academic_narratives",
        "academic_narrative_sections", "academic_semantic_runs",
        "academic_semantic_dimension_scores", "academic_semantic_findings",
        "academic_plagiarism_findings", "academic_humanize_passes",
        "academic_templates", "academic_score_history",
        "academic_deterministic_findings",
        "academic_visualization_types", "academic_visualizations",
        "academic_report_history",
        "academic_section_citations",   # <- fixes pre-existing gap (§0)
        "academic_proposals",           # <- this proposal, schema/22
    }
```

```python
def _make_proposal_predicate(phase):
    def predicate(conn, paper_id):
        row = conn.execute(
            "SELECT commit_sha FROM academic_proposals "
            "WHERE paper_id=? AND phase=? AND scope_domain_id IS NULL "
            "AND status='approved' AND is_latest=1", (paper_id, phase),
        ).fetchone()
        if not row:
            return False, [f"no approved {phase} proposal"]
        return True, [f"{phase} proposal approved at {row['commit_sha'][:8]}"]
    return predicate


for _phase in ("generation", "audit", "report"):
    _register_usecase_fn(f"propose-{_phase}",
                          f"an approved {_phase} proposal exists at the current commit",
                          _make_proposal_predicate(_phase))

# propose-fix is domain-scoped (scope_domain_id IS NOT NULL when
# source='user-request' names a domain) — checked by the calling script
# (approve_proposal.py / fix_loop), not by a single whole-paper predicate
# here; no registry entry needed since nothing calls usecase_status()
# with a bare "propose-fix" name (§5b/§6a's verify script takes --domain).

_register_usecase_fn(
    "approve-proposal", "human-decision step — no completion criteria of its own",
    lambda conn, paper_id: (True, ["approve-proposal has no predicate; "
                                    "downstream gates check the row it produces, not this usecase itself"]),
)
# Registered (not left absent) so usecase_status("approve-proposal", ...)
# never returns the registry's "unknown usecase" false-failure if
# anything ever calls it — resolves Rev-1-review #5.
```

## 6. Rejection and Redraft Flow

### 6a. The loop

```
propose (pending) --approve--> approved (terminal)
                  --reject "reason"--> rejected (terminal, decided)
                                       -> next propose invocation reads
                                          the rejected row's user_comment
                                          as redraft context, drafts a
                                          NEW pending row (iteration+1)
```

`gather_proposal_context.py` (§7a), on every invocation, first checks
whether the latest row for `(paper_id, phase, scope_domain)` is
`status='rejected'` — if so, its `user_comment` (the rejection reason)
and its `content_md` (what was rejected) are included in the context
handed to the drafting prompt, so the redraft is informed by *why* it
was rejected, not a blind retry. This reuses the existing gather→
prompt→persist chain unchanged — no new mechanism, just a conditional
read at the top of an already-planned script.

### 6b. Retry ceiling — reuses `fix_loop.max_iterations`

`academic_proposals.iteration` (§3) increments on every redraft.
`gather_proposal_context.py` refuses to draft past `iteration >= 5`
(same ceiling as `fix_loop.max_iterations`, `loop.yaml`) and instead
writes an envelope with `status="error"`, `message="proposal rejected 5
times — escalate to human_review"` — same `fallback: human_review`
`fix_loop` already declares for its own retry ceiling, reused verbatim
rather than inventing a second number.

### 6c. Partial approval — not a new mechanism, routes through `fix`

A reviewer who approves 11 of 12 domains' generation intent but objects
to one (`methodology`) rejects the whole `generation` proposal with a
reason naming the objection (`--reject --reason "everything except
methodology looks right, methodology needs an ablation-table mention"`).
The redraft (§6a) can then state "no change to 11 domains, methodology
revised to include X" and get approved as a whole. If a domain-specific
disagreement keeps recurring after generation is already approved and
running, that's what the `fix` phase is for (scope_domain_id-scoped,
§7d) — proposal-phase review is whole-run by design (§2), not because
partial approval is unsupported but because a *narrower* disagreement
belongs to the phase whose granularity actually matches it.

## 7. Scripts

### 7a. `script/propose/gather_proposal_context.py`

```python
"""gather_proposal_context.py — det step, first in every propose-* chain.
Expected --in payload: {paper_id, phase, domain (fix only, optional),
user_comment (fix only, optional), models (audit only, optional list)}
"""
def _load_paper_meta(conn, paper_id):
    """Shared by all four branches — title, commit_sha context, is
    only fetched once per invocation regardless of phase."""
    return conn.execute(
        "SELECT title FROM academic_papers WHERE id=?", (paper_id,)).fetchone()

def _redraft_context(conn, paper_id, phase, scope_domain_id):
    """§6a — if the latest row is rejected, surface it for the redraft."""
    row = conn.execute(
        "SELECT content_md, user_comment, iteration FROM academic_proposals "
        "WHERE paper_id=? AND phase=? AND scope_domain_id IS ? "
        "AND is_latest=1 AND status='rejected'",
        (paper_id, phase, scope_domain_id)).fetchone()
    return dict(row) if row else None

def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    phase = payload["phase"]
    conn = academic_schema.get_conn(db_path)
    try:
        meta = _load_paper_meta(conn, payload["paper_id"])
        redraft = _redraft_context(conn, payload["paper_id"], phase,
                                    payload.get("scope_domain_id"))
        if redraft and redraft["iteration"] >= 5:
            write_envelope(out_path, status="error",
                           message="proposal rejected 5 times — escalate to human_review")
            return
        if phase == "generation":
            context = _gather_generation_context(conn, payload["paper_id"])
        elif phase == "audit":
            context = _gather_audit_context(conn, payload["paper_id"], payload.get("models"))
        elif phase == "report":
            context = _gather_report_context(conn, payload["paper_id"])
        elif phase == "fix":
            context = _gather_fix_context(conn, payload["paper_id"],
                                           payload.get("domain"),
                                           payload.get("user_comment", ""))
        context["paper_title"] = meta["title"]
        context["redraft_of"] = redraft
    finally:
        conn.close()
    write_envelope(out_path, status="ok", message=f"gathered {phase} context", **context)
```

One file, four private per-phase functions plus two shared helpers
(`_load_paper_meta`, `_redraft_context`) — not four separate scripts.

### 7b. `script/propose/persist_proposal.py`

```python
"""Expected --in payload: {paper_id, phase, scope_domain_id (optional),
source, commit_sha, summary, content_md, user_comment (optional),
iteration (optional, default 0 or redraft_of.iteration+1)}"""
def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    conn = academic_schema.get_conn(db_path)
    try:
        # §3/§6a: only a still-pending previous row gets rewritten to
        # 'superseded' — a decided (approved/rejected) row's status is
        # immutable history, is_latest is the only column that changes.
        conn.execute(
            "UPDATE academic_proposals SET is_latest=0, "
            "status = CASE WHEN status='pending' THEN 'superseded' ELSE status END "
            "WHERE paper_id=? AND phase=? AND scope_domain_id IS ? AND is_latest=1",
            (payload["paper_id"], payload["phase"], payload.get("scope_domain_id")))
        conn.execute(
            "INSERT INTO academic_proposals "
            "(paper_id, phase, scope_domain_id, source, status, commit_sha, "
            " iteration, summary, content_md, user_comment, is_latest, created_at) "
            "VALUES (?,?,?,?,'pending',?,?,?,?,?,1,datetime('now'))",
            (payload["paper_id"], payload["phase"], payload.get("scope_domain_id"),
             payload["source"], payload["commit_sha"], payload.get("iteration", 0),
             payload["summary"], payload["content_md"], payload.get("user_comment", "")))
        conn.commit()
    finally:
        conn.close()
    write_envelope(out_path, status="ok", message=f"proposal drafted, phase={payload['phase']}")
```

### 7c. `script/propose/render_proposal.py`

Loads `templates/proposal/{markdown,html}/{phase}.{md,html}` (§4),
renders with the just-persisted row's context via `chevron.render()`
(same call shape `generate_audit_report.py` already uses), writes to
`docs/paper/paper-{id}/proposal/{phase}.md` and `.html`.

### 7d. `script/propose/approve_proposal.py`

```python
"""approve_proposal.py — the one human-decision step in the standard.
Usage: approve_proposal.py --repo-root <path> --phase <phase>
  [--domain <key>] [--reject --reason "..."]
Idempotent: re-running against an already-decided row is a no-op,
reported in the envelope (status=ok, message notes "already decided"),
not an error.
"""
def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    phase = payload["phase"]
    domain_id = payload.get("scope_domain_id")
    reject = payload.get("reject", False)
    reason = payload.get("reason", "")
    conn = academic_schema.get_conn(db_path)
    try:
        row = conn.execute(
            "SELECT id, status FROM academic_proposals "
            "WHERE paper_id=? AND phase=? AND scope_domain_id IS ? AND is_latest=1",
            (payload["paper_id"], phase, domain_id)).fetchone()
        if not row:
            write_envelope(out_path, status="error", message=f"no proposal for phase={phase}")
            return
        if row["status"] != "pending":
            write_envelope(out_path, status="ok",
                           message=f"already decided: status={row['status']}")
            return
        new_status = "rejected" if reject else "approved"
        conn.execute(
            "UPDATE academic_proposals SET status=?, decided_at=datetime('now'), "
            "user_comment = CASE WHEN ? THEN ? ELSE user_comment END WHERE id=?",
            (new_status, reject, reason, row["id"]))
        conn.commit()
    finally:
        conn.close()
    write_envelope(out_path, status="ok", message=f"phase={phase} {new_status}")
```

### 7e. `script/propose/request_fix.py` — the ad hoc entry point

```python
"""request_fix.py — CLI/MCP-facing entry point for 'fix X' user requests.
Not part of run_full_workflow.py's linear sequence; invoked directly
(e.g. via run_script_step from an interactive session) whenever a user
asks to fix something.
Usage: request_fix.py --repo-root <path> --user-comment "..." [--domain <key>]
"""
def _resolve_domain(conn, domain_arg, user_comment):
    """Exact match against academic_domains.key first. No fallback
    fuzzy-match — a wrong guess means the wrong section gets a fix
    proposal, worse than asking (resolves Rev-1-review #14)."""
    if domain_arg:
        row = conn.execute("SELECT id FROM academic_domains WHERE key=?",
                           (domain_arg,)).fetchone()
        if row:
            return row["id"]
        available = [r["key"] for r in conn.execute(
            "SELECT key FROM academic_domains ORDER BY sort_order")]
        raise ValueError(f"unknown domain '{domain_arg}', available: {available}")
    return None  # whole-paper-scoped fix proposal; the prompt itself
                 # must name a domain from user_comment's free text

def main():
    args = _parse()
    conn = academic_schema.get_conn(_db_path(args.repo_root))
    try:
        paper_id = _resolve_current_paper(conn, args.repo_root)
        domain_id = _resolve_domain(conn, args.domain, args.user_comment)
    finally:
        conn.close()
    _run_propose_fix_chain(args.repo_root, paper_id, domain_id,
                           source="user-request", user_comment=args.user_comment)
```

`_run_propose_fix_chain()` — the actual gather→prompt→persist→render
sequence, same MCP call shape `stage_semantic_triad()`
(`run_full_workflow.py:542-565`) already uses for every other
semantic-step triad in the standard, reused here rather than
reimplemented:

```python
def _run_propose_fix_chain(repo_root, paper_id, domain_id, source, user_comment):
    session = McpSession(_mcp_bin())
    try:
        steps = load_steps(_db_path(repo_root), "base_academic")
        uc_steps = steps_of(steps, "propose-fix")  # 4 literal steps, §9b
        gather, prompt_step, persist, render = uc_steps
        gather_input = {"paper_id": paper_id, "phase": "fix",
                        "scope_domain_id": domain_id, "user_comment": user_comment}
        session.call("run_script_step", {"step_id": gather["id"],
                                         "repo_path": repo_root, "input": gather_input})
        prompt = session.call("prepare_semantic_step", {"step_id": prompt_step["id"],
                                                          "repo_path": repo_root})
        print(f"awaiting agent reasoning over: {prompt.get('prompt_name')}")
        # An interactive agent completes the rest (§8): reason over the
        # prompt, complete_semantic_step, then run_script_step for
        # persist+render — same handoff shape as every other
        # pending_semantic entry run_full_workflow.py already stages.
    finally:
        session.close()
```

This is the literal wiring the request asks for: whatever routes a
user's natural-language fix request calls `request_fix.py`, which stages
(never auto-completes) a `propose-fix` draft — it never regenerates
content itself, that's still `fix_loop.mechanism`'s job, gated on
approval (§6, §9).

## 8. Why No New MCP Tool Is Needed

Propose/approve are ordinary usecases made of ordinary steps —
`kind='semantic'` (the drafting prompt, via `prepare_semantic_step`/
`complete_semantic_step`) and `kind='deterministic'` (gather/persist/
render/approve, via `run_script_step`) — exactly like every other usecase
in the standard. The four existing generic MCP tools are sufficient
because the gate rides the same primitives every other phase already
uses; §9a/§9b show concretely how the steps get into the DB for those
tools to find (Rev 1 asserted this without showing the wiring — the gap
the review's #3 caught).

**For an interactive Claude Code session**: the agent presents rendered
proposal content to the user in chat and waits for explicit approval
before ever calling `approve_proposal.py`. "Reject, change X" (§6c)
re-enters the same propose chain with the rejection reason as context —
the agent does not auto-redraft without a human's stated objection, and
does not auto-approve under any circumstance.

## 9. `run_full_workflow.py` — Corrected Phase Map + Checkpoints

### 9a. Why literal `steps:`, not `expand_triads()`

`expand_triads()` (`run_full_workflow.py:230-535`) exists specifically
for *per-domain/per-module fan-out* — one usecase, N steps, N determined
at runtime by the repo's module/domain count. All five new usecases
(`propose-generation`, `propose-audit`, `propose-report`, `propose-fix`,
`approve-proposal`) are **fixed-shape, whole-run** (§2) — exactly the
shape `schema-init` and `classify-repo` already use with a **literal**
`steps:` list in `standard.yaml` (confirmed: both have concrete `steps:`
blocks, not `steps: []`). Reusing that existing pattern means
`expand_triads()` needs zero changes — this replaces Rev 1's §7/§9,
which asserted the new usecases would just work without specifying
either path, the gap review's #3 correctly caught. §9b gives the literal
YAML.

### 9b. `standard.yaml` — new `scripts:`/`prompts:`/`usecases:` entries

```yaml
scripts:
  - name: gather-proposal-context
    location: ../propose/gather_proposal_context.py
  - name: persist-proposal
    location: ../propose/persist_proposal.py
  - name: render-proposal
    location: ../propose/render_proposal.py
  - name: approve-proposal
    location: ../propose/approve_proposal.py

prompts:
  - name: generation-proposal
    location: ../../prompt/propose/generation-proposal.md
  - name: audit-proposal
    location: ../../prompt/propose/audit-proposal.md
  - name: report-proposal
    location: ../../prompt/propose/report-proposal.md
  - name: fix-proposal
    location: ../../prompt/propose/fix-proposal.md

usecases:
  - name: propose-generation
    description: "draft a whole-run proposal of what generation is about to write"
    steps:
      - {order: 1, kind: deterministic, description: "Gather upstream analysis + domain list", script: gather-proposal-context}
      - {order: 2, kind: semantic, description: "Draft the generation proposal", prompt: generation-proposal}
      - {order: 3, kind: deterministic, description: "Persist proposal (status=pending)", script: persist-proposal}
      - {order: 4, kind: deterministic, description: "Render proposal to markdown+html", script: render-proposal}
  - name: propose-audit
    description: "draft a whole-run proposal of what audit is about to check"
    steps:  # same 4-step shape, gather/prompt/persist/render use audit-proposal
      - {order: 1, kind: deterministic, description: "Gather generation-complete domains + rubrics + models", script: gather-proposal-context}
      - {order: 2, kind: semantic, description: "Draft the audit proposal", prompt: audit-proposal}
      - {order: 3, kind: deterministic, description: "Persist proposal (status=pending)", script: persist-proposal}
      - {order: 4, kind: deterministic, description: "Render proposal to markdown+html", script: render-proposal}
  - name: propose-report
    description: "draft a whole-run proposal of what report artifacts this run will produce"
    steps:
      - {order: 1, kind: deterministic, description: "Gather latest score + report-kind list", script: gather-proposal-context}
      - {order: 2, kind: semantic, description: "Draft the report proposal", prompt: report-proposal}
      - {order: 3, kind: deterministic, description: "Persist proposal (status=pending)", script: persist-proposal}
      - {order: 4, kind: deterministic, description: "Render proposal to markdown+html", script: render-proposal}
  - name: propose-fix
    description: "draft what a fix will change and why, before regenerating a domain"
    steps:
      - {order: 1, kind: deterministic, description: "Gather failing findings or user comment + resolved domain", script: gather-proposal-context}
      - {order: 2, kind: semantic, description: "Draft the fix proposal", prompt: fix-proposal}
      - {order: 3, kind: deterministic, description: "Persist proposal (status=pending)", script: persist-proposal}
      - {order: 4, kind: deterministic, description: "Render proposal to markdown+html", script: render-proposal}
  - name: approve-proposal
    description: "human decision step — flips a pending proposal to approved/rejected"
    steps:
      - {order: 1, kind: deterministic, description: "Flip latest pending proposal to approved or rejected", script: approve-proposal}
```

### 9c. Corrected insertion points

Read against the actual code (not the docstring — Rev 1's error), the
in-code phase labels are: **Phase 4** = analysis usecases
(`run_full_workflow.py:695`), **Phase 5/5b/5c/5d** = generate → cite →
enrich → budget-fit (`:716-799`), **Phase 6** = deterministic-audit
(`:819`), **Phase 7** = semantic-audit (`:856`), **Phase 8** = plagiarism
+ humanize (`:903`), **Phase 9** = document-narrative-polish +
cross-section + document audit (`:938`), **Phase 10** = calculate →
render-charts → render-audit-report → render-paper, one `for` loop, no
gap between iterations (`:965-978`).

Three checkpoints, at the three points where a proposal's dependency is
actually satisfied in this order (not Rev 1's guessed ordering):

1. **`propose-generation`** — after Phase 4 (analyses complete), before
   Phase 5 (`generate-section-draft` starts). Depends on all four
   analysis usecases; gates every `generate-section-draft-{domain}`.
2. **`propose-audit`** — after Phase 5d (`section-budget-fit-total`,
   the actual last generation-chain step before audits in the current
   code order — **not** `document-narrative-polish`/4e, which runs at
   Phase 9, *after* audits, in this codebase today), before Phase 6
   (`deterministic-audit` starts). Depends on `section-budget-fit-total`;
   gates `deterministic-audit-*`.
3. **`propose-report`** — spliced inside Phase 10's `for usecase in
   (...)` loop, between `"calculate"` and `"render-charts"` (not "before
   6a/6b/6c" — Rev 1 invented sub-phase numbers that don't exist in the
   code; Phase 10 is one flat loop over four usecase names). Depends on
   `document-semantic-audit` (end of Phase 9) + `calculate`; gates
   `render-charts`/`render-audit-report`/`render-paper`.

```python
def _checkpoint(session, conn, repo_root, paper_id, phase, commit_sha, report_path):
    status = academic_schema.usecase_status(conn, paper_id, f"propose-{phase}")
    if status[0]:
        return  # already approved at this commit — proceed
    _run_propose_chain(session, repo_root, paper_id, phase, commit_sha)  # 9b's 4 steps
    print(f"awaiting approval: docs/paper/paper-{paper_id}/proposal/{phase}.md")
    print(f"run: approve_proposal.py --phase {phase}  (or --reject --reason ...)")
    report = json.loads(Path(report_path).read_text()) if Path(report_path).exists() else {}
    report["paused_at"] = phase  # §9d
    Path(report_path).write_text(json.dumps(report, indent=2))
    sys.exit(2)  # distinct from 0 (success) / 1 (failure) — "paused, not broken"
```

Called: once right after the Phase-4 analysis loop, once right after the
Phase 5d gate block (`gen_incomplete` check, `:801-817`), once between
`"calculate"` and the remaining three names in Phase 10's loop (splitting
that one loop into `calculate` then the checkpoint then the remaining
three). Re-invoking `run_full_workflow.py` after approval finds
`usecase_status()` already satisfied and proceeds — same idempotent
resume pattern the commit-hash skip-check already established.

### 9d. Exit code 2 — documented convention (resolves review #15)

`run_full_workflow.py`'s module docstring gains one line: "Exit code 2
means the run paused for a proposal decision, not failure or success —
check `workflow-report.json`'s `paused_at` field for which phase, review
the rendered proposal, then `approve_proposal.py` and re-invoke." Callers
(CI, wrapper scripts) branch on `2` as "re-run me later," distinct from
`1` (real failure) and `0` (fully done) — no new file, just the one
`paused_at` key already shown in `_checkpoint()` above.

## 10. New/Changed Files — Consolidated

| File | Change |
|---|---|
| `schema/22-academic_proposals.sql` | New (§3) |
| `templates/proposal/{markdown,html}/{generation,audit,report,fix}.{md,html}` | New, 8 files (§4) |
| `script/schema/standard.yaml` | 4 new `scripts:` entries, 4 new `prompts:` entries, 5 new `usecases:` entries with literal `steps:` (§9b) |
| `script/propose/gather_proposal_context.py` | New, phase-dispatched, redraft-aware (§7a) |
| `script/propose/persist_proposal.py` | New, supersede-only-if-pending (§7b) |
| `script/propose/render_proposal.py` | New (§7c) |
| `script/propose/approve_proposal.py` | New, idempotent approve/reject (§7d) |
| `script/propose/request_fix.py` | New, ad hoc entry point + exact-match domain resolution (§7e) |
| `prompt/propose/{generation,audit,report,fix}-proposal.md` | New, 4 prompts |
| `script/common/academic_schema.py` | `_uc_schema_init` required set gains `academic_section_citations` (pre-existing bug, §0) + `academic_proposals`; 4 new phase predicates + 1 trivial `approve-proposal` predicate (§5) |
| `script/verify/uc_propose_generation.py`, `uc_propose_audit.py`, `uc_propose_report.py`, `uc_propose_fix.py` | New, same shape as existing `uc*.py` verify scripts |
| `plan/core/loop.yaml` | New `proposal_gate:` section; `fix_loop.mechanism` gains one clause |
| `script/schema/run_full_workflow.py` | 3 `_checkpoint()` insertions (Phase 4→5, Phase 5d→6, inside Phase 10's loop); `paused_at` field + exit code 2 documented (§9) |

## 11. Open Questions — Resolved

- **Why one proposal per phase-per-run, not per domain?** A per-domain
  generation proposal turns one review into twelve for a decision
  ("does this batch of work look right") naturally made once. Fix
  proposals are the one exception that can be domain-scoped, because a
  fix, by nature, usually targets one named section (§6c).
- **Multi-model audit granularity (Rev-1-review #12)** — not a gap: the
  audit proposal states which models will run this round
  (`{{#models}}`, §4) and the gate is at the whole-round level, matching
  how the existing commit+model skip-check already works
  (report-granularity proposal §5b). A per-model proposal would
  micromanage a decision ("should this round of audit spend happen")
  that's naturally made once per round, not once per model.
- **Interactive re-draft / partial approval (Rev-1-review #11)** —
  resolved in §6: reject-with-reason re-enters the same chain; no
  separate "partial approval" state is needed because a narrower
  disagreement routes to the domain-scoped `fix` phase instead (§6c).

## 12. Explicitly Out of Scope

Any web/GUI approval surface (§8 — approval is reading a rendered file
and running one script), the full domain-name-matching heuristic beyond
exact-match-or-error (§7e — deliberately narrow, not deferred loosely as
Rev 1 left it), retroactive proposal-gating for papers whose generation/
audit already ran before this feature ships (no backfill — the next
phase transition simply hits its first unsatisfied checkpoint), any
change to the report-rendering layer itself, and any change to
`expand_triads()` (§9a — explicitly not needed, all five new usecases
use literal `steps:` instead).
