# rust_dev — System Proposal

## 1. Class / Position in Taxonomy

Class `dev`, subclass `build` (only member), `extends: base_dev`,
`drops: [06-design, 09-feature-design, 11-prototype]` — the largest drop
of any dev-class system. Proposed path `dev/build/rust_dev/` (currently
flat at `samgraha/system/rust_dev/`). `SYSTEM.md`'s TOML manifest
confirms: `base = "base_dev"`, `domains = 13`, `technology = "Rust /
Cargo"`, `methodology = "Systems Engineering"`. `CHANGELOG.md` shows the
same recent rework date as `fastapi_dev`'s (`[1.0.0] - 2026-07-15`):
Rust-specific templates for architecture/engineering/feature-technical,
new semantic audit rules (ownership, async, unsafe), a Cargo audit
check, and explicitly: *"Dropped `11-prototype` domain (systems require
full implementation from start)"* — a real methodological reason for
the third drop, not an incidental one.

## 2. What It Has

13 domains (16 minus `06-design`, `09-feature-design`, `11-prototype`):
vision, philosophy, security, feature, architecture, engineering,
external-context, feature-technical, implementation, qa, build, readme,
product-guide.

**Tier structure, read directly from `plan/core/tiers.yaml`:**

| Tier | Domains |
|---|---|
| 1 | vision, philosophy |
| 2 | security, feature, architecture, engineering, external-context |
| 3 | feature-technical |
| *(4 — absent)* | *prototype removed entirely, not renumbered — see §10* |
| 5 | implementation |
| 6 | qa |
| 7 | build |
| 8 | readme, product-guide |

**Notable: tier 4 is skipped, not renumbered.** `tiers.yaml` goes
`1, 2, 3, 5, 6, 7, 8` — confirmed by reading the file directly, not a
transcription error on my part. `SYSTEM.md`'s `[domain_tiers]` table
matches this same gap. This appears intentional (tier numbers track
`base_dev`'s original derivation semantics — tier 4 *is* "Validation
via Prototype" — rather than being a sequential index), but see §10 for
why this matters for `init.py`.

## 3. What It Inherits vs Overrides vs Adds

`rust_dev` has the most extensive customization of any dev-class system
examined so far — real overrides even in domains it *keeps* (not just
net-new sections), on top of the 3 drops:

| Area | Result |
|---|---|
| `calculation/**` | Identical to `base_dev`, 0 diff |
| `documentation-standards/*.md` | 13 files present |
| `plan/core/tiers.yaml` | Regenerated for the 13-domain graph, tier 4 gap intentional (§2, §10) |
| `templates/generation/section/**` | **9 net-new files** (`05-architecture/{12-crate_architecture,13-trait_design}.md`, `07-engineering/{09-ownership_patterns,10-async_patterns,11-unsafe_guidelines}.md`, `10-feature-technical/{18-crate_implementation,19-error_implementation}.md`, `12-qa/{10-property_testing,11-benchmark_testing}.md`, `13-implementation/08-crate_folder_structure.md`, `14-build/10-crate_publishing.md`, `16-product-guide/07-development_workflow.md`) **plus 11 existing files genuinely rewritten in place**, not just additions: `04-feature/{02-functional_requirements,06-outputs}.md`, `05-architecture/02-system_overview.md`, `07-engineering/{01-guiding_principles,02-rationale,06-code_standards}.md`, `08-external-context/{01-purpose,03-constraints}.md`, `12-qa/{01-purpose,05-e2e-testing}.md`, `13-implementation/{03-generation_plan,05-change_request_plan}.md`, `15-readme/{08-installation,09-build,13-development}.md` |
| `script/mapping.yaml`, `policy.yaml` | Overridden — 4 new checks added with their own caching strategy (`cargo-audit`: ttl/86400s, `lint-standards`: always_rerun override, `crate-dependency-graph`: fingerprint, `unsafe-code-scan`: always_rerun) |
| `script/{windows,ubuntu}/` | **4 new checks, fully implemented as `.ps1`+`.sh` pairs** (not schema-only like `fastapi_dev`'s gaps): `cargo-audit`, `crate-dependency-graph`, `cargo-fmt`, `unsafe-code-scan` — confirmed present in both platform directories |
| `script/schema/03-security/external-ref-isolation.*` | Present, but **no executable script** — same gap as `fastapi_dev`'s (§10), likely a shared, still-unimplemented draft check that propagated into both systems rather than a `rust_dev`-specific miss |

The 11 in-place rewrites (vs. purely additive changes) are the clearest
signal this system diverges more from `base_dev` in its *shared*
domains than any other dev-class system reviewed — Rust's ownership
model and systems-engineering framing evidently required rewording even
generic sections like `07-engineering/01-guiding_principles.md`, not
just adding Rust-specific new ones.

## 4. Use Cases

Same 4 use case *names* as `base_dev`, tier content reduced per §2 (no
tier-4/prototype stage exists in this system's use cases at all).

## 5. Workflow per Use Case (target `init.py` phase plan)

`rust_dev` needs its own `init.py`. Partial phase table for
`repo_new/case_1_no_documentation`, showing the delta:

```
tier3-feature-technical-scaffold/content/validate/calculate/report/fix
  depends_on: [tier2-fix]

# NO tier4-* phases at all — prototype domain doesn't exist in this system

tier5-implementation-scaffold
  depends_on: [tier3-fix]   # skips straight from tier3's fix to tier5's generate
  # base_dev's tier5-implementation would depend_on [tier4-fix]; here it's [tier3-fix]
```

This is the one place the tier-4 gap (§2/§10) has a real mechanical
consequence: `init.py`'s `depends_on` for `implementation`'s phases
must point at `tier3-fix`, not a nonexistent `tier4-fix` — an `init.py`
generator that naively computes "depends on previous tier number minus
one" would break here. It must instead depend on "whatever tier
immediately precedes this one **in this system's own tier list**," not
assume base_dev's numbering.

## 6. Deterministic Audit via Script

18 checks inherited from `base_dev` minus the 2 that targeted dropped
domains (`design-tokens-in-implementation` for `06-design`,
`mock-api-runs` for `11-prototype`) = 16 inherited, confirmed by the
`script/windows` file-list diff. Plus 4 new, fully-implemented
Rust-specific checks (§3): `cargo-audit` (security), `crate-dependency-graph`
(architecture), `cargo-fmt` (engineering), `unsafe-code-scan`
(engineering) — **20 working checks total**, the most complete
check-script coverage of any system examined in this pass. One gap
shared with `fastapi_dev`: `external-ref-isolation` is declared
(schema+manifest) but has no executable in either system.

## 7. Generation via Script (`scaffold.py`)

Same mechanism as every dev-class system, 13 domains. The 9 net-new
Rust-specific sections scaffold like any other; the 11 in-place
rewrites (§3) don't affect `scaffold.py`'s logic at all since it reads
whatever's present at scaffold time — the rewrites matter to the
semantic content-fill phase (different prompt content) and to
`validate.py`'s rules (different rule text), not to scaffolding.

## 8. Report & Calculation via Script (`calculate.py` + `report.py`)

`calculation/**` is a 0-diff copy of `base_dev`'s 7 formulas — no
Rust-specific scoring logic exists or is implied. **Cross-check against
the author guide's own §11.2 worked `calculate.py` example, which uses
`rust_dev` as its illustrative system:** that example is a generic,
invented-looking scoring stub (`return {"total": 82, "band": "Good",
"breakdown": {"deterministic": 90, "semantic": 74}}`) and does not
reflect this system's actual `calculation/` files (which use the real
`deterministic_document_v1`/etc. stable-ID formulas shared with
`base_dev`). The guide's choice of `rust_dev` as its example system
appears to be illustrative naming only — the example's *content* isn't
sourced from this system's real calculation formulas, so `calculate.py`
should be built from the real `calculation/*.yaml` files (identical to
`base_dev`'s), not from the guide's simplified example.

## 9. Script Language Priority Applied

- `scripts/init.py`, `scaffold.py`, `validate.py`, `calculate.py`,
  `report.py`, `plan_generation.py` — `rust_dev`'s own, given the
  extensive real customization in §3
- 4 new checks (`cargo-audit`, `crate-dependency-graph`, `cargo-fmt`,
  `unsafe-code-scan`) → consolidate each `.ps1`+`.sh` pair into a single
  `.py`, same as the 16 inherited checks (`base_dev`'s proposal §9)
- `external-ref-isolation.py` — greenfield, no existing implementation
  to port (shared gap with `fastapi_dev`, §6)

## 10. Open Questions / Risks Specific to `rust_dev`

- **Tier 4's absence (not renumbered) needs an explicit decision before
  `init.py` is built.** Confirmed real, not a read error — both
  `tiers.yaml` and `SYSTEM.md`'s `[domain_tiers]` skip it consistently.
  If this is intentional (preserving `base_dev`'s tier semantics as
  stable identifiers), `init.py`'s phase-dependency logic must be
  written to read the *actual* tier list in order, not assume
  contiguous integers — flagged concretely in §5.
- Given 11 shared-domain sections were rewritten in place (§3), this
  system is the strongest evidence among the 4 concrete dev systems
  that a subclass-level base (`dev/build/base_build/`, per the taxonomy
  proposal §4.1's deferred-until-second-sibling rule) would have real
  content to share if/when a second systems-language system (Go, C++,
  Zig, ...) joins the `build` subclass — worth keeping in mind as a
  forward pointer, not acted on now since `rust_dev` is still the only
  member.
- `external-ref-isolation`'s missing implementation (§6) is shared with
  `fastapi_dev` — worth fixing once, wherever the real source of that
  check ends up living (possibly `base_dev`, since it appears in two
  unrelated concrete systems' schemas), rather than twice independently.

## 11. Explicitly Out of Scope

Actual script implementation, including `external-ref-isolation`'s
missing executable. Deciding/renumbering the tier-4 gap — flagged as a
finding requiring a decision, not resolved here. Any change to domain
content beyond what's already authored.
