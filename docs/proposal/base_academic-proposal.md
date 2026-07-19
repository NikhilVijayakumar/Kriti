# base_academic — System Proposal (New System)

## 1. Class / Position in Taxonomy

Class `academic`, abstract base, proposed path `academic/base_academic/`
— does not exist yet. Shared by `pcems_2026` (subclass `paper`) and
`eswa_journal` (subclass `journal`). This document verifies the
taxonomy proposal's §2.3/§4 assumption (4 shared domains:
introduction, methodology, conclusion, references) against the two
systems' actual file content, and corrects it where the assumption
doesn't hold.

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

## 7. Workflow per Use Case (target `init.py` phase plan)

Shared *shape*, per-system domain lists: `generate(semantic, scaffold
first if templates existed — see §9 caveat)` →
`audit(semantic only, no deterministic step)` → `fix(semantic,
document-level only, no section-scoped regenerate)`, gated tier-by-tier
per each system's own `tiers.yaml`. This is genuinely different from
`base_dev`'s pattern in one structural way worth naming explicitly:
there is no `validate.py`-driven deterministic gate in the audit phase
for either academic system today — the entire audit phase is one
semantic LLM call per domain, not a script step feeding into a semantic
step.

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
