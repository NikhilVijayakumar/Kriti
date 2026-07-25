# Domain Relationships

## Purpose

Cross-domain dependency map for the frontend engineering documentation standards in this directory — the agreed target model for how frontend systems are engineered. Use it to see what a domain feeds into, or what feeds into it, without opening every standard document.

This file is system-specific to `react_dev`. It reflects frontend engineering domain relationships, not generic software engineering.

## Sections

### All Declared Relationships

A domain can have more than one parent — e.g. Feature derives from both Vision and Philosophy, not just Vision. Each parent gets its own row.

| From | Relationship | To |
|------|--------------|-----|
| vision | inspires | philosophy |
| vision | derives | feature |
| philosophy | derives | feature |
| vision | derives | security |
| philosophy | derives | security |
| philosophy | guides | architecture |
| philosophy | guides | design |
| philosophy | guides | engineering |
| security | guides | architecture |
| security | guides | engineering |
| architecture | soft-aligns-with (mutual, non-mandatory) | engineering |
| external-context | informs | engineering |
| feature | derives | feature-design |
| design | derives | feature-design |
| external-context | informs | feature-design |
| feature | derives | feature-technical |
| engineering | derives | feature-technical |
| architecture | derives | feature-technical |
| external-context | informs | feature-technical |
| prototype | validates | feature-design |
| prototype | validates | feature-technical |
| feature-technical | derives | implementation |
| engineering | derives | implementation |
| prototype | informs | implementation |
| qa | validates | implementation |
| qa | informs | build |
| implementation | derives | build |
| readme | references | vision |
| readme | requires | build |

`product-guide` declares no relationships — flat content describing the finished product's usage, same as `help` always has been. It isn't part of the derivation graph; it's written after everything else, referencing all of it informally rather than through a machine-readable edge.

### Frontend-Specific Domain Concerns

Each domain has frontend-specific focus areas that distinguish this system from generic software engineering:

| Domain | Frontend-Specific Concern |
|--------|---------------------------|
| 01-vision | Component-driven development, user experience as engineering concern, performance budgets |
| 02-philosophy | Functional components, hooks-only state, TypeScript everywhere, no class components |
| 03-security | XSS prevention, CSP headers, dependency auditing, secret-free client code |
| 04-feature | Feature = component + hooks + types + tests, feature isolation boundaries |
| 05-architecture | Component tree as architecture, unidirectional data flow, state architecture |
| 06-design | Atomic Design methodology, design tokens, theme sovereignty, accessibility |
| 07-engineering | React/TypeScript patterns, hooks conventions, error boundaries, i18n |
| 08-external-context | UI framework selection, state management preferences, styling decisions |
| 09-feature-design | UI feature design, component hierarchy per feature, state ownership |
| 10-feature-technical | Component implementation, hook implementation, type implementation |
| 11-prototype | Storybook prototypes, throwaway HTML, user testing |
| 12-qa | Component testing, visual regression, accessibility testing |
| 13-implementation | Component folder structure, barrel exports, feature folders |
| 14-build | Vite configuration, code splitting, bundle analysis, asset pipeline |
| 15-readme | Frontend README, setup instructions, development workflow |
| 16-product-guide | Component catalog, design system docs, contribution guidelines |

### Traceability Chain

```text
Tier 1                  Tier 2                                              Tier 3

Vision ── inspires ──> Philosophy
   │                       │
   ├───────────────────────┼──> Security ── guides ──> Architecture
   │                       │                └─ guides ──> Engineering
   │                       │
   ├───────────────────────┴──> Feature
   │                       ├──> Architecture ──┐ soft-aligns, non-mandatory
   │                       ├──> Design         │ (most frameworks expect an
   │                       └──> Engineering ◄──┘  architecture, none require one)
   │
External Context (independent) ── informs ──> Engineering
                                └─ informs ──> Feature Design, Feature Technical

Feature ─┬─ (+ Design, + External Context if any) ──────> Feature Design ──┐
         └─ (+ Architecture, + Engineering, + External Context if any) ──> Feature Technical ─┤
                                                                                                ↓
                                                                          Tier 4 ── Prototype (validates both)
                                                                                                ↓
                                                              Tier 5 ── Implementation (+ Engineering, informed by Prototype)
                                                                                                ↓
                                                                        Tier 6 ── QA (validates Implementation)
                                                                                                ↓
                                                                              Tier 7 ── Build (+ QA informs)
                                                                                                ↓
                                                          Tier 8 ── Readme (requires Build, for install/run instructions)
                                                                                                ↓
                                                                              Product Guide (requires everything, incl. Readme)
```

### Document Authoring Order — Tiered Model

Filenames in this directory carry a `NN-` prefix showing the order docs get written in, not audit priority. Docs in the same tier have no dependency on each other (with one noted exception) and can be authored in parallel.

**Tier 1 — Foundational.** No dependencies on anything else.

| # | File | Derived From |
|---|------|--------------|
| 00 | `00-domain-relationships.md` | meta — not an authored artifact |
| 01 | `01-vision-standards.md` | initial idea (no standard — see below) |
| 02 | `02-philosophy-standards.md` | vision |

**Tier 2 — Independent.** Each derives only from Tier 1, not from each other, with two exceptions: External Context informs Engineering directly, and Architecture/Engineering have a soft, non-mandatory best-practice relationship (most frameworks expect an architecture to follow, but nothing requires one to exist first).

| # | File | Derived From |
|---|------|--------------|
| 03 | `03-security-standards.md` | vision + philosophy (**draft**, not yet registered) — guides Architecture(05) and Engineering(07) downstream as a constraint, not a peer |
| 04 | `04-feature-standards.md` | vision + philosophy |
| 05 | `05-architecture-standards.md` | philosophy; soft/non-mandatory relationship with Engineering(07) |
| 06 | `06-design-standards.md` | philosophy |
| 07 | `07-engineering-standards.md` | philosophy; soft/non-mandatory relationship with Architecture(05); informed by External Context(08) |
| 08 | `08-external-context-standards.md` | independent — informs Engineering(07) directly, and informs Feature Design(09)/Feature Technical(10) downstream |

**Tier 3 — Derived.** Each combines multiple Tier 2 outputs.

| # | File | Derived From |
|---|------|--------------|
| 09 | `09-feature-design-standards.md` | feature(04) + design(06) + external-context(08) if any |
| 10 | `10-feature-technical-standards.md` | feature(04) + engineering(07) + architecture(05) + external-context(08) if any |

**Tier 4 — Validation.**

| # | File | Derived From |
|---|------|--------------|
| 11 | `11-prototype-standards.md` | feature-design(09) + feature-technical(10) — validates, doesn't derive |

**Tier 5 — Realization (draft, not yet registered).**

| # | File | Derived From |
|---|------|--------------|
| 12 | `13-implementation-standards.md` | feature-technical(10) + engineering(07) + prototype(11) |

**Tier 6 — Validation of the built artifact.** Tests what Implementation(13) actually produced — inserted here rather than alongside Prototype(11) because Prototype validates the *design* (Feature Design/Feature Technical) before anything is built, while QA validates the *build* itself, which doesn't exist until Tier 5 completes.

| # | File | Derived From |
|---|------|--------------|
| 13 | `12-qa-standards.md` | implementation(13) — validates, doesn't derive; also references engineering(07) testing standards, architecture(05), and security(03) threat model per-section |

**Tier 7 — Packaging (draft, not yet registered).**

| # | File | Derived From |
|---|------|--------------|
| 14 | `14-build-standards.md` | Implementation(13); informed by QA(12) — packaging shouldn't proceed on a build QA hasn't validated |

**Tier 8 — Final overview.** Written last, after everything above has settled.

| # | File | Derived From |
|---|------|--------------|
| 15 | `15-readme-standards.md` | vision (final refactor pass — see below); needs Build(14) to exist for install/run instructions |
| 16 | `16-product-guide-standards.md` | the finished product itself — needs everything else, including README, to be accurate |

**Initial idea has no standard.** It's not a kept artifact — a rough idea gets folded straight into Vision (01) and, downstream, into Feature (04) as one of its derivation inputs. Nothing audits the idea stage itself.

**README plays both ends.** Early on it can hold the initial idea (or a separate idea doc can be used instead) before Vision exists. Once every other standard doc in the chain is complete, README gets refactored into the structure `15-readme-standards.md` defines — including install/run instructions, which is why README sits after Build(14) rather than before Implementation(13): a README that must stay implementation-detail-free could be written earlier, but a conventional README needs build/run instructions, which don't exist until Build(14) does.

**Security, Implementation, and Build are drafts.** None has a `StandardDefinition` in `crates/standards/src/builtin.rs`, so none is enforced or audited yet.

* **Security** is fully specified: project-wide threat model, data classification, and security principles, once — Architecture's, Engineering's, and Feature Technical's own Security Considerations/Standards sections derive from it rather than duplicate it. See `03-security-standards.md`'s "Relationship to Per-Domain Security Sections" for the exact ownership split.
* **Implementation** is fully specified: the as-built, one-to-one counterpart to Feature Technical, distinct from Engineering's Code Standards by scope (per-feature vs repo-wide). See `13-implementation-standards.md`'s "Relationship to Engineering's Code Standards."
* **Build** is fully specified: project-wide versioning/packaging/distribution/provenance policy, distinct from Engineering's Build Standards section, which stays scoped to CI/CD mechanics. See `14-build-standards.md`'s "Relationship to Engineering's Build Standards."

### Cross-Domain Dependency Matrix

This matrix shows which domains depend on which. Rows depend on columns.

|  | vision | philosophy | security | feature | architecture | design | engineering | external-context |
|--|--------|------------|----------|---------|--------------|--------|-------------|------------------|
| **feature-design** | | | | ✓ | | ✓ | | ✓ |
| **feature-technical** | | | | ✓ | ✓ | | ✓ | ✓ |
| **prototype** | | | | | | | | |
| **implementation** | | | | | | | ✓ | |
| **qa** | | | | | ✓ | | ✓ | |
| **build** | | | | | | | | |
| **readme** | ✓ | | | | | | | |
| **product-guide** | | | | | | | | |

### Frontend Engineering Tier Summary

| Tier | Purpose | Frontend Focus |
|------|---------|----------------|
| 1 | Foundational | Vision and philosophy — why we build frontend systems this way |
| 2 | Independent | Security, feature definition, architecture, design, engineering, external context — each a standalone concern |
| 3 | Derived | Feature design and technical — combines multiple Tier 2 outputs into per-feature plans |
| 4 | Validation | Prototype — validates design before anything is built |
| 5 | Realization | Implementation — builds the actual components, hooks, types |
| 6 | Validation | QA — validates the built artifact (component tests, visual regression, a11y) |
| 7 | Packaging | Build — bundles, optimizes, deploys |
| 8 | Final | README and Product Guide — documentation for developers and users |

### Machine-Readable Format (proposed, not yet implemented)

Everything above (the relationship table, the tier tables) is prose and markdown tables — readable by a human, not by an engine. A future `plan/` orchestration layer (tier-by-tier documentation generation/audit/fix, gated so a defect never propagates past the tier it's caught in) needs this same information as data. No new relationships are introduced here — this is a transcription of the table and tiers above into the shape that layer would read, proposed for discussion, **not created as an actual file yet**.

```yaml
tiers:
  - tier: 1
    domains: [vision, philosophy]
  - tier: 2
    domains: [security, feature, architecture, design, engineering, external-context]
  - tier: 3
    domains: [feature-design, feature-technical]
  - tier: 4
    domains: [prototype]
  - tier: 5
    domains: [implementation]
  - tier: 6
    domains: [qa]
  - tier: 7
    domains: [build]
  - tier: 8
    domains: [readme, product-guide]

relationships:
  - { from: vision, type: inspires, to: philosophy }
  - { from: vision, type: derives, to: feature }
  - { from: philosophy, type: derives, to: feature }
  - { from: vision, type: derives, to: security }
  - { from: philosophy, type: derives, to: security }
  - { from: philosophy, type: guides, to: architecture }
  - { from: philosophy, type: guides, to: design }
  - { from: philosophy, type: guides, to: engineering }
  - { from: security, type: guides, to: architecture }
  - { from: security, type: guides, to: engineering }
  - { from: architecture, type: soft_aligns_with, to: engineering, mandatory: false, mutual: true }
  - { from: external-context, type: informs, to: engineering }
  - { from: external-context, type: informs, to: feature-design }
  - { from: external-context, type: informs, to: feature-technical }
  - { from: feature, type: derives, to: feature-design }
  - { from: design, type: derives, to: feature-design }
  - { from: feature, type: derives, to: feature-technical }
  - { from: engineering, type: derives, to: feature-technical }
  - { from: architecture, type: derives, to: feature-technical }
  - { from: prototype, type: validates, to: feature-design }
  - { from: prototype, type: validates, to: feature-technical }
  - { from: feature-technical, type: derives, to: implementation }
  - { from: engineering, type: derives, to: implementation }
  - { from: prototype, type: informs, to: implementation }
  - { from: qa, type: validates, to: implementation }
  - { from: qa, type: informs, to: build }
  - { from: implementation, type: derives, to: build }
  - { from: readme, type: references, to: vision }
  - { from: readme, type: requires, to: build }

relationship_types:   # closed set — no custom types without updating this file first
  - inspires           # tier-gating: strict
  - derives            # tier-gating: strict
  - guides              # tier-gating: strict
  - soft_aligns_with     # tier-gating: none — mutual, non-mandatory (Architecture/Engineering exception)
  - informs               # tier-gating: none — cross-cutting (External Context's role)
  - validates               # tier-gating: strict, but validates rather than derives (Prototype's role)
  - requires                 # tier-gating: strict
  - references                # tier-gating: none — a citation, not a dependency (Readme→Vision)
```

**`product-guide` is the only domain not in the `relationships` list above** — documented as intentionally outside the derivation graph (see the note under "All Declared Relationships"). `qa` was a real gap as of the previous revision of this file (mentioned nowhere, in prose or table) and has now been placed: Tier 6, between Implementation(13) and Build(14) — it validates what Implementation actually produced (mirroring how Prototype validates the design, one tier earlier, before anything is built), and its result informs whether Build should proceed.

## Usage

Check this before adding a new relationship to a domain — if the relationship isn't in the table above, add it here too, otherwise this document drifts out of sync with itself the same way it drifted out of sync with code before this rewrite. When `security`, `implementation`, and `build` get registered as real `StandardDefinition`s in `crates/standards/src/builtin.rs`, that code should be written to match this file, not the other way around. If the "Machine-Readable Format" section above is ever turned into a real `plan/tiers.yaml`, this file's prose/table version stays authoritative — that file would be a transcription of this one, not a second independently-maintained copy.
