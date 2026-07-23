# base_academic — System Proposal (New System)

## 1. Class / Position in Taxonomy

Class `academic`, abstract base, proposed path `academic/base_academic/`
— does not exist yet. Shared by `pcems_2026` (subclass `paper`) and
`eswa_journal` (subclass `journal`). This document verifies the
taxonomy proposal's §2.3/§4 assumption (4 shared domains:
introduction, methodology, conclusion, references) against the two
systems' actual file content, and corrects it where the assumption
doesn't hold.

The system is implemented as a **samgraha knowledge standard** driven
through the **MCP protocol** (JSON-RPC over stdio), matching the
architecture proven by `python_hackathon`. All orchestration — usecase
registration, step execution, semantic reasoning, score persistence —
flows through samgraha's `mcp` binary, never through direct subprocess
calls to scripts.

## 2. What It Should Have — Findings From Comparing Both Systems

**Verdict up front: the 4 domain-name matches do not mean shared
content.** Read side by side, each of the 4 candidate domains differs
in depth, rigor, and in one case (`conclusion`) directly *contradicts*
the other system's rule. This is the single most important finding in
this document — it corrects, not confirms, the taxonomy proposal's
assumption.

**`introduction`:**
- `pcems_2026`: 3 bracketed prompts (broader problem space, gap,
  objectives/contributions), plus typography rules. Minimal.
- `eswa_journal`: 6 structured subsections (Global Domain Problem,
  Technical Gap & Limitations, Proposed Solution Overview,
  Contributions — with an explicit audit rule requiring a
  bulleted/numbered list and the literal words "novel," "statistically
  validated," "complexity" — Scope Boundaries), plus Do/Don't writing
  guidance.
- **Verdict: too divergent to share as one content file.**
  `eswa_journal`'s version is roughly 4x the structural depth of
  `pcems_2026`'s.

**`methodology`:**
- `pcems_2026`: single bracket (explain methodology, include
  algorithms/equations), typography only.
- `eswa_journal`: mandatory Visual Hierarchy (separate Logical
  Architecture + Physical Architecture subsections, each requiring its
  own diagram), mandatory Algorithmic Clarity (pseudocode/algorithm
  block required), Mathematical Grounding, mandatory Complexity
  Analysis (formal Big-O notation + a complexity comparison table
  against baselines).
- **Verdict: too divergent to share.** `eswa_journal`'s rigor bar (Q1
  journal) is substantially higher than `pcems_2026`'s (conference
  paper) for this domain specifically.

**`conclusion`:**
- `pcems_2026`: "[Summarize the main contributions and findings]
  [**Discuss future work**]" — future work is explicitly requested here.
- `eswa_journal`: "Don't: Introduce any new claims, citations, or
  future work (**future work belongs in the Limitations section**)."
- **Verdict: these two systems' rules directly contradict each other**,
  not just differ in depth. `pcems_2026` has no `limitations` domain at
  all, so it has nowhere else to put future-work discussion — its
  `conclusion` domain has to carry it. `eswa_journal` has a dedicated
  `limitations` domain and explicitly forbids future-work content from
  leaking into `conclusion`. A shared `base_academic/conclusion`
  content file cannot satisfy both rules simultaneously without an
  override — this is not a case where a lowest-common-denominator core
  works either, since the two rules are opposites, not different
  strictness levels of the same rule.

**`references`:**
- `pcems_2026`: "All references MUST be formatted in APA style," 8pt
  font requirement. Format/typography-focused.
- `eswa_journal`: 35-45 reference count target, a specific percentage
  distribution (60-70% recent, 20% classics, 10-20% architecture, 2-4%
  ESWA-specific), Q1/Q2 Scopus + CORE A/A* quality bar, explicit
  predatory-journal rejection rule. No citation *style* (APA or
  otherwise) mentioned at all — a completely different axis of
  concern (quality/quantity vs. formatting).
- **Verdict: too divergent to share** — not contradictory like
  `conclusion`, but non-overlapping concerns (formatting vs.
  quality/distribution) rather than the same rule at different depths.

## 3. Proposed `base_academic` Content

Given §2's findings, **`base_academic` should NOT contain shared
`documentation-standards/` content for the 4 nominally-common
domains.** Forcing a shared file would mean either (a) a
lowest-common-denominator so thin it adds nothing beyond what each
system already writes independently, or (b) `conclusion`'s literal
contradiction unresolved. Both systems would need to override the
shared file entirely anyway, which provides zero deduplication benefit
over each system just keeping its own file — the taxonomy proposal's
assumed savings don't materialize at the content level.

**What genuinely IS shareable, confirmed by direct file comparison
(not assumption):**

- **`calculation/summary/{score_bands,trend}.yaml` — byte-for-byte
  identical** between `pcems_2026` and `eswa_journal`, confirmed by
  diff.
- **`calculation/summary/final_score.yaml` — identical except a single
  comment string** naming which system it belongs to (the formula
  itself, "passes the one bucket through unchanged," is the same).
- **`calculation/validation/scoring_validation.yaml` — identical
  except the `description` field's system name.**
- **`calculation/semantic/document.yaml` — same structural shape**
  (one rubric file per paper domain, redistributed checks across
  domains, mandatory-failure-forfeits-that-domain's-points logic),
  differing only in the domain list and which specific checks live
  where (expected — domain lists differ, §2).
- **`plan/core/loop.yaml`'s shape and prose framing** — near-identical
  structure in both systems (same section order: `threshold`,
  `max_iterations`/`fallback`, `within_tier_ordering`, `path_selection`
  with an `evidence` step + Path A/B, `scoring`, `validate`,
  `fix_loop`, `tier_gate`), differing only in the domain-specific
  values (which domains get the `evidence` step, which
  `within_tier_ordering` pairs apply). This is templatable as a
  parameterized base file, not byte-identical the way `calculation/`
  is, but structurally proven shared, not assumed.
- **`relationship_types` vocabulary** — both systems use the exact same
  closed set (`guides`, `requires`, `validates`, `informs`), confirmed
  by reading both `00-domain-relationships.md` files.
- **The class-level policy statement itself**: "no deterministic layer,
  no section-scoped audits, semantic_document bucket only,
  document-level-only fix loop" — both systems' `loop.yaml` state this
  in nearly identical prose, confirming it's a genuine shared design
  decision, not two independent choices that happened to match.

So `base_academic` is real, but **narrower than the taxonomy proposal
assumed**: it shares process/calculation infrastructure, not
documentation-standards content. Proposed contents:

```
academic/base_academic/
├── system.yaml                          # abstract: true
├── calculation/
│   ├── summary/{final_score,score_bands,trend}.yaml    # shared, near/fully identical
│   └── validation/scoring_validation.yaml.template      # shared shape, system name parameterized
├── plan/core/loop.yaml.template          # shared shape, domain-specific values parameterized
└── docs/
    └── relationship-types.md              # shared vocabulary reference (guides/requires/validates/informs)
```

No `documentation-standards/`, no `00-domain-relationships.md`, no
`audit/` at the base level — every one of those is genuinely
system-specific, confirmed by §2, not just assumed per the archived
Knowledge System Evolution Proposal's Principle 4.

## 4. What `pcems_2026` Adds on Top

All 6 domains stay entirely `pcems_2026`'s own (§2 shows even the
nominally-shared 4 need full content, not overrides of a thin base):
`title-and-metadata`, `introduction`, `methodology`, `findings`,
`conclusion`, `references` — see `pcems_2026-proposal.md` §2 for full
content summary.

## 5. What `eswa_journal` Adds on Top

All 11 domains stay entirely `eswa_journal`'s own, same reasoning:
`abstract`, `introduction`, `related-work`, `problem-definition`,
`methodology`, `experimental-setup`, `results`, `implications`,
`limitations`, `conclusion`, `references` — see
`eswa_journal-proposal.md` §2 for full content summary.

## 6. Use Cases (shared shape, if any)

Confirmed shared shape: both systems have exactly one implied use case
— "existing project with implementation/evidence, no
[format]-compliant paper written yet" — neither has a `plan/usecase/`
directory (unlike every dev-class system), and both rely on
`loop.yaml`'s `path_selection.evidence` step to optionally pull
concrete numbers from an implementation artifact. LIM-001's
characterization ("generate paper sections from project evidence,
semantic-only audit") holds for both, confirmed directly, not just
inferred from the evidence table.

## 7. Workflow per Use Case — MCP-Driven Architecture

All orchestration flows through **samgraha's MCP binary** (JSON-RPC
over stdio), matching the architecture proven by `python_hackathon`.
No script is ever subprocess-called directly by the orchestrator —
every execution goes through `run_script_step` / `prepare_semantic_step`
/ `complete_semantic_step`, which record an `execution` row in
`knowledge.db` automatically.

### 7.1 samgraha's Orchestration Tables (knowledge.db)

Samgraha owns these tables, created and migrated by its Rust
`crates/registry` const migrations (`schema/knowledge/*.sql`):

| Table | Purpose |
|-------|---------|
| `usecase` | One row per declared usecase (standard, name, description) |
| `script` | One row per registered script (name, location, purpose) |
| `prompt` | One row per registered prompt (name, location) |
| `step` | One row per step in a usecase's ordered sequence (kind: deterministic/semantic) |
| `step_script` | Links deterministic steps to their script |
| `step_prompt` | Links semantic steps to their prompt |
| `execution` | Execution log: one row per actual run (step_id, repo_root, status, timestamp) |
| `custom_data_tables` | Catalog of standard-owned tables in knowledge.db |

### 7.2 Standard's Custom Tables (academic-specific)

The standard owns its own normalized tables in the same `knowledge.db`
file, catalogued via `standard.yaml`'s `custom_tables:` section and
created by `init_schema.py`. Samgraha never creates or migrates these —
it only records their existence in `custom_data_tables`:

| Table | Purpose |
|-------|---------|
| `academic_papers` | One row per registered paper |
| `academic_domains` | Lookup: scoring domains, weights |
| `academic_semantic_runs` | One row per (paper, domain, model) semantic evaluation |
| `academic_semantic_dimension_scores` | Per-dimension score+evidence for a semantic run |
| `academic_semantic_findings` | Per-run strengths/weaknesses/recommendations |
| `academic_narratives` | One row per (paper, domain) narrative-generation run |
| `academic_narrative_sections` | Per-narrative {heading, text} sections |
| `academic_templates` | Catalog of markdown/html report templates on disk |

### 7.3 Standard Manifest (`standard.yaml`)

The `standard.yaml` manifest registers all scripts, prompts, usecases,
steps, and custom tables with samgraha at `register_standard` time.
Every script entry follows samgraha's fixed capability-script contract:

```
scripts:
  - name: <step-name>
    location: <script.py>
    purpose: "<description>"
```

Every script receives `--repo-root`, `--in` (JSON payload file), `--out`
(JSON envelope file) and writes a result envelope `{status, message,
written}` to `--out`. The `_adapter.py` module provides shared glue:
`parse_step_args()` resolves `knowledge.db` from `--repo-root`, and
`run_driver()` runs the actual driver script as a subprocess with
translated CLI args.

### 7.4 Semantic Triad Pattern

Semantic steps follow samgraha's documented triad (three consecutive
steps: pre-script → semantic → post-script):

**Audit triad (per domain):**
1. `run_domain_evidence.py` — gathers evidence from the paper's
   implementation artifacts for the domain
2. `audit/semantic/document/{domain}.prompt.md` — clean standalone
   prompt extracted from the `*.yaml` rubric (the yaml itself stays as
   the machine-readable spec, unregistered)
3. `persist_domain_semantic_score.py` — persists the agent's
   per-domain semantic score

**Narrative triad (per domain + competition-wide):**
1. `fetch_score_context.py` — reads this paper's/all papers' scores
   from the normalized tables
2. `analysis/{domain}.md` — narrative prompt for the agent to write over
3. `persist_narrative.py` — persists the narrative sections

### 7.5 Wrapper Scripts

Every `wrap_*.py` is a thin subprocess adapter — no business logic
changed, only the calling convention. The `_adapter.py` module provides
shared glue for samgraha's fixed `--repo-root`/`--in`/`--out` contract:
`parse_step_args()` resolves `knowledge.db`, `run_driver()` runs the
driver as a subprocess and writes the samgraha capability envelope to
`--out`.

### 7.6 Full Workflow Orchestrator (`run_full_workflow.py`)

Master orchestrator that drives every step through the **real MCP
protocol** — spawns the built `mcp` binary, speaks JSON-RPC over stdio.
Never subprocess-calls scripts directly, so every execution
(deterministic or semantic) gets tracked exactly the way any MCP client
driving samgraha normally would.

Execution order:
1. `register_standard` — (re)registers `standard.yaml`'s usecases/steps/
   scripts/prompts into knowledge.db
2. `schema-init` — creates academic-specific tables, seeds domains and
   templates from the real filesystem
3. `semantic-audit` / `narrative-analysis` — pre-script runs
   automatically; semantic step is only STAGED (`prepare_semantic_step`
   called, prompt fetched). Completing it needs an actual model reasoning
   over that prompt — this is why samgraha splits
   prepare/complete_semantic_step. Every staged-but-incomplete item is
   written to the workflow report so an agent driving MCP directly knows
   exactly which `step_id` to call next.
4. `render` — run once; harmless to rerun later once semantic steps are
   completed.

Writes a JSON report (`ran`/`failed`/`pending_semantic`) next to
`knowledge.db` so progress survives between runs — rerunning is
idempotent for everything except re-staging semantic steps it already
staged.

## 8. Deterministic Audit via Script

Confirmed absent in both (§2, §6 of each system's own proposal).
Cross-system comparison of candidates (see each system's own §6 for
full lists): `eswa_journal`'s rules are far richer
script-check candidates (word counts, reference counts, regex-matchable
statistical-test mentions, structural section-presence checks) than
`pcems_2026`'s (mostly typography, which needs real font metadata
unavailable in plain Markdown). If a deterministic layer gets built for
either academic system, `eswa_journal` is the stronger first candidate
— not a `base_academic`-level decision, since the checks themselves are
domain-specific either way, but worth noting here since it affects
whether `base_academic` should reserve a `validate.py` contract slot
for a future deterministic bucket even though neither concrete system
uses one today.

## 9. Generation via Script (`scaffold.py`)

**Neither system has `templates/generation/document/{domain}.md`
authored yet** — confirmed empty/near-empty in both (`pcems_2026`:
completely empty; `eswa_journal`: only `templates/generation/humanifier.md`
exists, which is not a per-domain template — see
`eswa_journal-proposal.md` §10 for a separate, policy-level flag on
that file). This means `base_academic`'s `scaffold.py` can specify the
*mechanism* (read `templates/generation/document/{domain}.md`, create
heading skeleton) but has nothing to test against in either concrete
system today — both are blocked on template authoring first,
independent of any `base_academic` extraction work.

## 10. Report & Calculation via Script (`calculate.py` + `report.py`)

This is `base_academic`'s strongest, most concretely evidenced value
(§3) — `calculate.py` implementing `final_score_v1`-equivalent (verify
exact stable ID matches, not confirmed byte-for-byte in this pass),
`score_bands_v1`, `trend_v1` from genuinely identical formula files
across both systems, plus the shared `scoring_validation.yaml`
pre-check pattern (`val-001`/`val-002` style bounds-checking before
trusting `calculate.py`'s output — a capability `base_dev`'s
calculation shape doesn't have at all, worth considering whether it
should be backported there too, out of scope for this document).

`report.py` renders `templates/audit/summary/{domain}-report.md` per
system (report templates themselves are domain-specific, only the
calculation feeding them is shared).

## 11. Script Language Priority Applied

`base_academic` needs Python versions of whatever generic
`calculate.py`/`report.py` logic is genuinely shared (§3, §10) —
greenfield, no existing scripts to port in either concrete system.

## 12. Open Questions / Risks Specific to `base_academic`

**The central finding of this document:** the taxonomy proposal's
assumption of a clean 4-domain shared documentation-standards base
**does not hold** under direct content comparison — 3 of 4 domains are
too divergent in depth to share, and the 4th (`conclusion`) has an
outright contradictory rule between the two systems. What DOES hold,
confirmed rather than assumed, is sharing at the
*calculation/process-shape* layer: `calculation/summary/*.yaml` is
genuinely near-identical, `plan/core/loop.yaml`'s structure and framing
match closely, and the class-level "no deterministic layer, semantic
bucket only" policy is a real shared decision in both systems' own
words. **Recommendation: scope `base_academic` down to §3's narrower
content** (calculation + loop shape + relationship-type vocabulary),
not the taxonomy proposal's original 4-domain documentation-standards
sharing — and flag this correction back to that proposal rather than
silently diverging from it.

A secondary, smaller finding: both systems are currently blocked from
generating anything at all (§9) — this is true independent of whether
`base_academic` gets built, and arguably more urgent, since it affects
whether either system can be used today, not just how cleanly they
share infrastructure.

**MCP dependency:** the full workflow orchestrator requires samgraha's
`mcp` binary to be built (`cargo build --release` in the samgraha
repo). Without it, scripts can still be invoked directly, but execution
tracking and semantic step staging only work through MCP.

## 13. Explicitly Out of Scope

Actual script implementation. Migrating `pcems_2026`/`eswa_journal` to
extend this base — that's the taxonomy proposal's migration step docs;
this document only specifies (and corrects) what `base_academic` should
contain. Resolving the `conclusion` domain's cross-system contradiction
(§2) — noted as a finding, not a decision made here, since it belongs
to each system's own content, not to the shared base. Updating the
taxonomy proposal's §2.3/§4 text to reflect this document's narrower
scope — flagged as a needed follow-up edit, not performed in this
document.
