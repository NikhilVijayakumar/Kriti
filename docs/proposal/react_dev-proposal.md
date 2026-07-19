# react_dev — System Proposal

## 1. Class / Position in Taxonomy

Class `dev`, subclass `frontend` (paired with `electron_dev`), `extends:
base_dev`, no drops. Proposed path `dev/frontend/react_dev/` (currently
flat at `samgraha/system/react_dev/`).

## 2. What It Has

16 domains — identical set to `base_dev` (no drops). Tier structure and
the full relationship graph (`00-domain-relationships.md`'s YAML block)
are **byte-identical** to `base_dev`'s — only the prose framing at the
top of the file and the tier-description table got React-flavored
wording (e.g. tier 1 described as "why we build frontend systems this
way," tier 6 as "component tests, visual regression, a11y"). No
structural difference in the graph itself.

File inventory delta vs. `base_dev` (see §3 for the full diff):
- `documentation-standards/`: 0 files different (identical)
- `audit/`: 6 new section-level files (3 deterministic + 3 matching
  semantic — see §3)
- `calculation/`: 0 files different (identical)
- `templates/generation/`: 13 new section templates
- `templates/audit/`: 0 files different (identical)
- `script/`: 0 files different (identical — same 18 checks as `base_dev`)
- `plan/`: 0 files different (identical)

## 3. What It Inherits vs Overrides vs Adds

Full directory diff against `base_dev`, actually run, not assumed:

| Area | Result |
|---|---|
| `documentation-standards/*.md` | **Identical to base_dev, 0 diff.** react_dev adds zero domain-standards content of its own. |
| `script/**` | **Identical to base_dev, 0 diff.** No React-specific check scripts exist — the 18 checks are pure duplicates. |
| `calculation/**` | **Identical to base_dev, 0 diff.** |
| `templates/audit/**` | **Identical to base_dev, 0 diff.** |
| `plan/**` (core + usecase) | **Identical to base_dev, 0 diff.** Same 4 use cases, same 8-tier loop. |
| `00-domain-relationships.md` | Same YAML graph, cosmetic prose delta only (React-flavored tier descriptions). |
| `templates/generation/section/**` | **13 net-new files, genuinely React-specific:** `05-architecture/12-component_architecture.md`, `06-design/07-design_tokens.md`, `07-engineering/{09-hook_conventions,10-component_patterns,11-state_management,12-internationalization}.md`, `09-feature-design/08-user_flow.md`, `10-feature-technical/18-component_implementation.md`, `12-qa/{10-visual_testing,11-component_testing}.md`, `13-implementation/08-feature_folder_structure.md`, `14-build/10-bundle_analysis.md`, `16-product-guide/07-development_workflow.md` |
| `audit/deterministic/section/**` | **3 net-new files:** `05-architecture/12-component_architecture.yaml`, `07-engineering/{10-hook_conventions,11-component_patterns,12-state_management}.yaml` (4 actually), `12-qa/{10-visual_testing,11-component_testing}.yaml` |
| `audit/semantic/section/**` | Same 6 files, semantic counterpart of the deterministic set above |

**Finding worth flagging:** every file under `documentation-standards/`,
`script/`, `calculation/`, `templates/audit/`, and `plan/` is a
zero-delta copy of `base_dev`'s. That's ~85 files (16 doc-standards + 36
script pair + schema/mapping/policy + 7 calculation + audit report
templates + 48 plan/usecase docs) carried in full that would, under real
`extends`/`drops` resolution (author guide §4), resolve from `base_dev`
automatically and never need to exist in `react_dev`'s own tree at all.
This is exactly the maintenance-multiplier LIM-001 describes: today, a
fix to any of these 85 files in `base_dev` requires manually
re-copying into `react_dev` (and `electron_dev`, `fastapi_dev`,
`rust_dev`) by hand, with no signal if one copy is missed.

## 4. Use Cases

Identical to `base_dev`'s 4 use cases (`plan/usecase/` is a 0-diff
copy) — `repo_new/case_1_no_documentation`, `repo_new/case_2_has_documentation`,
`repo_existing/case_1_no_documentation`, `repo_existing/case_2_has_documentation`.

## 5. Workflow per Use Case (target `init.py` phase plan)

Since domains, tiers, and the relationship graph are identical to
`base_dev`'s, `react_dev`'s phase *shape* is identical too — same 8
tiers, same `within_tier_ordering` exception (external-context before
engineering in tier 2), same generate→audit→fix pattern per phase.

**Concrete recommendation:** `react_dev` does not need its own
hand-authored `init.py`. Its plan is `base_dev`'s plan, with 6 extra
leaf-level phases inserted for the React-specific sections listed in §3
(each new section template gets its own scaffold/content-fill pair
nested inside its parent domain's existing generation phase, not a new
top-level phase — `05-architecture`'s generation phase now scaffolds 12
sections instead of 11, for instance). If `base_dev`'s `init.py` is
authored generically enough (reads `tiers.yaml` + counts section
templates present, per author guide §11A.2's transform), `react_dev`
inheriting it costs nothing extra — the section count difference falls
out of reading `react_dev`'s own `templates/generation/section/` at
scaffold time, not a different `init.py`.

## 6. Deterministic Audit via Script

`script/**` is a 0-diff copy of `base_dev`'s 18 checks — no
React-specific check scripts exist (no ESLint-rule check, no
prop-types/TypeScript check, nothing bundle-size-specific despite
`bundle_analysis.md` existing as a section template). This is a gap
worth flagging in §10 rather than a finding to act on unprompted.

## 7. Generation via Script (`scaffold.py`)

`scaffold.py` for `react_dev` reads the same 16
`templates/generation/document/{domain}.md` files as `base_dev`, plus
the 13 additional React-specific section templates layered on top (§3).
Under the scaffold/content-fill split from the execution-model
proposal, these 13 sections scaffold exactly like any other section —
heading from template, mechanical, no LLM — the "React-specific" part
is entirely in what semantic content-fill later writes under each
heading, not in the scaffold step itself.

## 8. Report & Calculation via Script (`calculate.py` + `report.py`)

`calculation/**` is a 0-diff copy of `base_dev`'s 7 formulas — same
stable IDs (`deterministic_document_v1` through `trend_v1`), same
25/25/25/25 weighting. `react_dev`'s `calculate.py`/`report.py` are, by
this evidence, identical to `base_dev`'s — no React-specific scoring
logic exists or is implied by anything in the current tree.

## 9. Script Language Priority Applied

Given §6's finding (zero React-specific check scripts exist),
`react_dev` needs **no new `.py` files of its own** beyond what
`base_dev`'s proposal already specifies (`init.py`, `scaffold.py`,
`validate.py`, `calculate.py`, `report.py`, `plan_generation.py`, plus
the 18 ported check scripts) — all inherited wholesale under real
`extends` resolution. The only genuinely `react_dev`-scoped work is
authoring content for the 13 net-new section templates (a semantic/LLM
concern, not a script one) and, per §10, deciding whether any of the 7
audit-rule-less sections warrant a new deterministic check.

## 10. Open Questions / Risks Specific to `react_dev`

- **7 of the 13 React-specific section templates have no audit rule at
  all**, deterministic or semantic: `06-design/07-design_tokens.md`,
  `07-engineering/12-internationalization.md`,
  `09-feature-design/08-user_flow.md`,
  `10-feature-technical/18-component_implementation.md`,
  `13-implementation/08-feature_folder_structure.md`,
  `14-build/10-bundle_analysis.md`,
  `16-product-guide/07-development_workflow.md`. Only 6 of the 13 got a
  matching audit file (`component_architecture`, `hook_conventions`,
  `component_patterns`, `state_management`, `visual_testing`,
  `component_testing`). Sections without an audit rule can be generated
  but never scored/validated — worth deciding whether this is
  intentional (some sections are informational-only, not audited) or a
  gap to fill, before wiring `validate.py`.
- §3's ~85-file duplication is the single largest finding here — worth
  confirming with whoever owns the real `extends` merge implementation
  whether it's safe to start *dropping* these zero-delta files from
  `react_dev`'s tree now (relying on inheritance to resolve them) or
  whether that migration needs to wait for a specific verification step.

## 11. Explicitly Out of Scope

Actual script implementation. Any change to domain content, audit
rules, or the relationship graph itself. Deciding whether/how to
physically remove the ~85 zero-delta duplicate files from `react_dev`'s
tree — flagged in §10 as a finding, not executed here.
