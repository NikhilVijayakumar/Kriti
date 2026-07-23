# fastapi_dev — System Proposal

## 1. Class / Position in Taxonomy

Class `dev`, subclass `backend`, `extends: base_dev`, `drops:
[06-design, 09-feature-design]`. Proposed path
`dev/backend/fastapi_dev/` (currently flat at
`samgraha/system/fastapi_dev/`). `SYSTEM.md`'s TOML frontmatter already
declares this relationship informally, predating the `system.yaml`
extends/drops mechanism: `base = "base_dev"`, `dropped_from_base =
["06-design", "09-feature-design"]`, `technology = "Python / FastAPI"`,
`methodology = "Layered Backend Engineering"`. `CHANGELOG.md` shows this
system was substantially reworked recently (`[1.0.0] - 2026-07-15`,
4 days before this proposal): new API-specific semantic audit rules,
OpenAPI schema validation check added, Tier 3 realigned to
`feature-technical` only, `11-prototype` refocused from visual mockups
to API endpoints.

## 2. What It Has

14 domains (16 minus `06-design`, `09-feature-design`):
vision, philosophy, security, feature, architecture, engineering,
external-context, feature-technical, prototype, qa, implementation,
build, readme, product-guide.

**Tier structure changed by the drops** (confirmed by reading
`plan/core/tiers.yaml` directly, not assumed):

| Tier | Domains |
|---|---|
| 1 | vision, philosophy |
| 2 | security, feature, architecture, engineering, external-context *(design removed)* |
| 3 | feature-technical *(feature-design removed — was a 2-domain tier, now 1)* |
| 4 | prototype |
| 5 | implementation |
| 6 | qa |
| 7 | build |
| 8 | readme, product-guide |

Edges referencing the dropped domains are correctly removed too (e.g.
no `design → feature-technical` edge) — `tiers.yaml` was properly
regenerated post-drop, not left stale. This is the opposite of the
LIM-001 concern documented for the academic systems (stale copy-pasted
`loop.yaml`) — worth noting as a positive precedent.

## 3. What It Inherits vs Overrides vs Adds

Unlike `react_dev`/`electron_dev` (near-total zero-diff copies of
`base_dev`), `fastapi_dev` has **real, substantive overrides** — the
drops ripple into actual content changes, not just a smaller domain
list:

| Area | Result |
|---|---|
| `documentation-standards/*.md` | 14 files present (2 fewer than base_dev, as expected from drops) |
| `calculation/**` | Identical to `base_dev`, 0 diff |
| `templates/audit/**` | Identical to `base_dev`, 0 diff |
| `templates/generation/document/*.md` | Same 14-file set as doc-standards (06, 09 absent) |
| `audit/deterministic/document/*.yaml` | **11 files genuinely overridden** (content differs from base_dev's, not just present/absent) — `02-philosophy`, `02-philosophy-relationships`, `04-feature-relationships`, `05-architecture`, `07-engineering`, `08-external-context-relationships`, `10-feature-technical`, `10-feature-technical-relationships`, `12-qa`, `14-build`, `16-product-guide` all differ from base_dev's version, reflecting the removed design/feature-design references downstream |
| `templates/generation/section/**` | 8 net-new files: `05-architecture/12-layered_architecture.md`, `07-engineering/{09-versioning,10-migration_strategy}.md`, `10-feature-technical/18-layer_implementation.md`, `12-qa/10-api_testing.md`, `13-implementation/08-feature_folder_structure.md`, `14-build/10-api_validation.md`, `16-product-guide/07-development_workflow.md`, plus `11-prototype/03-mock-apis.md` **replaced** with `03-prototype-endpoints.md` (renamed+rewritten, not just added — matches CHANGELOG's "refocused from visual mockups to API endpoints") |
| `audit/deterministic/section/**` | 10 net-new files matching the new/renamed templates above |
| `audit/semantic/section/**` | 8 net-new files: `03-security/10-api_auth_patterns.md`, `05-architecture/12-layered_architecture.md`, `07-engineering/{10-versioning,11-async_patterns,12-response_models}.md`, `10-feature-technical/21-layer_implementation.md` |
| `script/mapping.yaml`, `script/policy.yaml` | Genuinely overridden (differ from base_dev's) |
| `script/schema/03-security/`, `script/schema/14-build/` | 2 new check definitions added: `external-ref-isolation`, `openapi-schema-valid` — **schema+manifest only, no executable script — see §10** |
| `plan/core/tiers.yaml` | Genuinely regenerated to match the 14-domain graph (§2) |
| `script/windows/`, `script/ubuntu/` | **Identical to base_dev, 0 diff** — despite 2 new checks being declared in `mapping.yaml`/`schema/`, no corresponding `.ps1`/`.sh` exists for either (see §10) |

## 4. Use Cases

Same 4 use cases as `base_dev` (`repo_new`/`repo_existing` ×
`case_1_no_documentation`/`case_2_has_documentation`) — the use-case
*names* are unchanged by the domain drops, only the per-use-case tier
content shrinks per §2.

## 5. Workflow per Use Case (target `init.py` phase plan)

`fastapi_dev` needs its own `init.py`, distinct from `base_dev`'s,
because tier composition genuinely changed (tier 2 loses `design`, tier
3 shrinks from 2 domains to 1). Partial phase table for
`repo_new/case_1_no_documentation`, showing the delta from `base_dev`'s
16-domain version:

```
tier2-{security,feature,architecture,engineering,external-context}-scaffold   script
  # no tier2-design-scaffold phase — domain doesn't exist here
tier2-external-context-content → tier2-engineering-content   # ordering exception unchanged
tier2-validate/calculate/report/fix                          # same script pattern, fewer inputs

tier3-feature-technical-scaffold    script   depends_on: [tier2-fix]
  # no tier3-feature-design-scaffold phase — domain doesn't exist here,
  # so tier 3 has one generation phase instead of two parallel ones
tier3-feature-technical-content     semantic depends_on: [tier3-feature-technical-scaffold]
tier3-validate/calculate/report/fix  # same pattern

# tiers 1, 4-8 unchanged in shape from base_dev's plan
```

## 6. Deterministic Audit via Script

18 checks inherited unchanged from `base_dev` (§3 — `script/windows`/`ubuntu`
0-diff) — none of them targeted `06-design`/`09-feature-design` anyway,
so nothing needed removing. On top, 2 new checks are *declared*
(`external-ref-isolation` in `03-security`'s schema, `openapi-schema-valid`
in `14-build`'s schema, plus an `api-endpoint-reachable` entry appearing
in `mapping.yaml`) but **none of the three has an actual executable
script** — see §10, this is the system's main gap.

## 7. Generation via Script (`scaffold.py`)

Same mechanism as every dev-class system. 14 domains instead of 16,
plus the 8 net-new/renamed sections in §3. `11-prototype`'s
`03-mock-apis.md`→`03-prototype-endpoints.md` rename is a real content
swap, not additive — `scaffold.py`'s logic (read whatever's in
`templates/generation/section/{domain}/`) handles this transparently
since it doesn't hardcode section names, just reads what's present.

## 8. Report & Calculation via Script (`calculate.py` + `report.py`)

`calculation/**` is a 0-diff copy of `base_dev`'s 7 formulas. The
14-domain section rollup uses the same `deterministic_section_v1`/
`semantic_section_v1` formulas — per `calculation/README.md`'s own
description ("unweighted average rollup... excluding absent optional
sections"), the formula itself is domain-count-agnostic, so no formula
change is needed for the 2 fewer domains, only fewer inputs at
calculation time.

## 9. Script Language Priority Applied

- `scripts/init.py`, `scaffold.py`, `validate.py`, `calculate.py`,
  `report.py`, `plan_generation.py` — same set as every dev-class
  system, `fastapi_dev`'s own since its content genuinely differs from
  `base_dev`'s (§3), not inherited wholesale like `react_dev`'s
- **New, greenfield (no `.ps1`/`.sh` to port from) Python scripts
  needed:** `external-ref-isolation.py`, `openapi-schema-valid.py`,
  `api-endpoint-reachable.py` — these 3 checks exist only as
  schema/manifest declarations today (§6/§10), so under the
  script-language-priority policy they should be authored directly in
  Python rather than as a `.ps1`+`.sh` pair that later needs
  consolidating, since there's no existing implementation to port from.

## 10. Open Questions / Risks Specific to `fastapi_dev`

- **3 declared checks have no executable script.**
  `external-ref-isolation` and `openapi-schema-valid` have a
  `manifest.yaml`+`schema.json` pair under `script/schema/` but no
  `.ps1`/`.sh` under `script/windows/`/`script/ubuntu/` — confirmed by
  directly listing both directories, no matching files exist.
  `api-endpoint-reachable` appears in `mapping.yaml` but has no schema
  files either. These 3 checks are declared but unimplemented — a
  `validate.py` built against the current `mapping.yaml` would either
  error or silently skip them depending on how missing-script handling
  is written; worth deciding which before `validate.py` exists.
- The `SYSTEM.md` TOML manifest (`base = "base_dev"`,
  `dropped_from_base = [...]`) is a hand-authored, informal precursor
  to the same information now expressed in `system.yaml`'s `extends`/
  `drops` fields — worth confirming these two files agree (they did, at
  the time of this read) and considering whether `SYSTEM.md` becomes
  redundant once `class`/`subclass` fields land in `system.yaml`
  (taxonomy proposal §4), or whether it's kept as human-readable
  changelog-adjacent context `system.yaml` doesn't carry.

## 11. Explicitly Out of Scope

Actual script implementation for the 3 gap checks in §10. Any change to
domain content/rules themselves beyond what's already been authored.
