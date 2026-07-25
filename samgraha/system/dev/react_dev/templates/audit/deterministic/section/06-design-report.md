# Deterministic Section Report — Design

**Document:** {{ document_path }}
**Standard:** `documentation-standards/06-design-standards.md`
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 6 section scores below
section_score = 100 × (Σ weight of passed rules in that section) / (Σ weight of all rules in that section)
# calculation: deterministic_section_v1
```

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs — this revision is the baseline every future run is compared against.{% endif %}

### Section Scores

| # | Section | Required | Weight | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---:|---|
| 1 | Design Principles | **required** | 4.0 | {{ sections.design_principles.score }} / 100 | {{ sections.design_principles.previous_score | default('—') }} | {{ sections.design_principles.trend_display }} |
| 2 | UX Principles | **required** | 4.0 | {{ sections.ux_principles.score }} / 100 | {{ sections.ux_principles.previous_score | default('—') }} | {{ sections.ux_principles.trend_display }} |
| 3 | Accessibility | **required** | 4.0 | {{ sections.accessibility.score }} / 100 | {{ sections.accessibility.previous_score | default('—') }} | {{ sections.accessibility.trend_display }} |
| 4 | Purpose | optional | 2.5 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Constraints | optional | 2.5 | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 6 | Traceability | optional | 1.5 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

The 3 required sections carry 12.0 of the document's 18.5 total rule weight — a document can only pass if those three are both present and internally sound; the remaining three are recommended-quality signal, not gating.

---

## 1. Design Principles — `section/06-design/01-design_principles.yaml` — weight 4.0 — **required**

**Why this matters:** Design principles are the foundational rules guiding visual and interaction decisions. They ensure consistency, coherence, and a unified product identity across all surfaces. Without them, every downstream design decision is made on ad-hoc judgment with no shared foundation.

**Section Score: {{ sections.design_principles.score }} / 100** ({{ sections.design_principles.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| design-sec-dp-001 | Design principles section exists | error (mandatory) | 1.5 | {{ results['design-sec-dp-001'].previous_status \| default('—') }} | {{ results['design-sec-dp-001'].status }} | {{ results['design-sec-dp-001'].trend_display }} | {{ results['design-sec-dp-001'].evidence \| default('—') }} |
| design-sec-dp-002 | At least two distinct design principles enumerated | error (mandatory) | 1.0 | {{ results['design-sec-dp-002'].previous_status \| default('—') }} | {{ results['design-sec-dp-002'].status }} | {{ results['design-sec-dp-002'].trend_display }} | {{ results['design-sec-dp-002'].evidence \| default('—') }} |
| design-sec-dp-003 | No implementation technology references | error (mandatory) | 1.0 | {{ results['design-sec-dp-003'].previous_status \| default('—') }} | {{ results['design-sec-dp-003'].status }} | {{ results['design-sec-dp-003'].trend_display }} | {{ results['design-sec-dp-003'].evidence \| default('—') }} |
| design-sec-dp-004 | Traces to Philosophy (guided_by) | warning (recommended) | 0.5 | {{ results['design-sec-dp-004'].previous_status \| default('—') }} | {{ results['design-sec-dp-004'].status }} | {{ results['design-sec-dp-004'].trend_display }} | {{ results['design-sec-dp-004'].evidence \| default('—') }} |

## 2. UX Principles — `02-ux_principles.yaml` — weight 4.0 — **required**

**Why this matters:** UX principles operationalize human-centered design into actionable heuristics. They govern interaction patterns, information architecture, and user flows to ensure intuitive and efficient experiences. Without them, UX decisions are reactive rather than principled.

**Section Score: {{ sections.ux_principles.score }} / 100** ({{ sections.ux_principles.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| design-sec-ux-001 | UX principles section exists | error (mandatory) | 1.5 | {{ results['design-sec-ux-001'].previous_status \| default('—') }} | {{ results['design-sec-ux-001'].status }} | {{ results['design-sec-ux-001'].trend_display }} | {{ results['design-sec-ux-001'].evidence \| default('—') }} |
| design-sec-ux-002 | At least two distinct UX principles enumerated | error (mandatory) | 1.0 | {{ results['design-sec-ux-002'].previous_status \| default('—') }} | {{ results['design-sec-ux-002'].status }} | {{ results['design-sec-ux-002'].trend_display }} | {{ results['design-sec-ux-002'].evidence \| default('—') }} |
| design-sec-ux-003 | No implementation technology references | error (mandatory) | 1.0 | {{ results['design-sec-ux-003'].previous_status \| default('—') }} | {{ results['design-sec-ux-003'].status }} | {{ results['design-sec-ux-003'].trend_display }} | {{ results['design-sec-ux-003'].evidence \| default('—') }} |
| design-sec-ux-004 | Principles are user-centered | warning (recommended) | 0.5 | {{ results['design-sec-ux-004'].previous_status \| default('—') }} | {{ results['design-sec-ux-004'].status }} | {{ results['design-sec-ux-004'].trend_display }} | {{ results['design-sec-ux-004'].evidence \| default('—') }} |

## 3. Accessibility — `03-accessibility.yaml` — weight 4.0 — **required**

**Why this matters:** Accessibility ensures the product is usable by people with diverse abilities. Compliance with WCAG standards is both a legal requirement and a design quality benchmark. Without explicit accessibility requirements, every interaction pattern is assumed accessible until proven otherwise.

**Section Score: {{ sections.accessibility.score }} / 100** ({{ sections.accessibility.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| design-sec-a11y-001 | Accessibility section exists | error (mandatory) | 1.5 | {{ results['design-sec-a11y-001'].previous_status \| default('—') }} | {{ results['design-sec-a11y-001'].status }} | {{ results['design-sec-a11y-001'].trend_display }} | {{ results['design-sec-a11y-001'].evidence \| default('—') }} |
| design-sec-a11y-002 | At least two distinct accessibility requirements enumerated | error (mandatory) | 1.0 | {{ results['design-sec-a11y-002'].previous_status \| default('—') }} | {{ results['design-sec-a11y-002'].status }} | {{ results['design-sec-a11y-002'].trend_display }} | {{ results['design-sec-a11y-002'].evidence \| default('—') }} |
| design-sec-a11y-003 | References an accessibility standard (WCAG, Section 508, ADA) | warning (recommended) | 0.5 | {{ results['design-sec-a11y-003'].previous_status \| default('—') }} | {{ results['design-sec-a11y-003'].status }} | {{ results['design-sec-a11y-003'].trend_display }} | {{ results['design-sec-a11y-003'].evidence \| default('—') }} |
| design-sec-a11y-004 | No implementation technology references | error (mandatory) | 1.0 | {{ results['design-sec-a11y-004'].previous_status \| default('—') }} | {{ results['design-sec-a11y-004'].status }} | {{ results['design-sec-a11y-004'].trend_display }} | {{ results['design-sec-a11y-004'].evidence \| default('—') }} |

## 4. Purpose — `04-purpose.yaml` — weight 2.5 — optional

**Why this matters:** Purpose defines the strategic intent behind visual and interaction decisions. Every element must serve a clear functional or communicative goal aligned with product vision. Without it, design decisions look decorative rather than purposeful.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| design-sec-purpose-001 | Purpose section present | warning (recommended) | 0.5 | {{ results['design-sec-purpose-001'].previous_status \| default('—') }} | {{ results['design-sec-purpose-001'].status }} | {{ results['design-sec-purpose-001'].trend_display }} | {{ results['design-sec-purpose-001'].evidence \| default('—') }} |
| design-sec-purpose-002 | States design intent | warning (recommended) | 0.5 | {{ results['design-sec-purpose-002'].previous_status \| default('—') }} | {{ results['design-sec-purpose-002'].status }} | {{ results['design-sec-purpose-002'].trend_display }} | {{ results['design-sec-purpose-002'].evidence \| default('—') }} |
| design-sec-purpose-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['design-sec-purpose-003'].previous_status \| default('—') }} | {{ results['design-sec-purpose-003'].status }} | {{ results['design-sec-purpose-003'].trend_display }} | {{ results['design-sec-purpose-003'].evidence \| default('—') }} |
| design-sec-purpose-004 | Scope boundaries defined | warning (recommended) | 0.5 | {{ results['design-sec-purpose-004'].previous_status \| default('—') }} | {{ results['design-sec-purpose-004'].status }} | {{ results['design-sec-purpose-004'].trend_display }} | {{ results['design-sec-purpose-004'].evidence \| default('—') }} |

## 5. Constraints — `05-constraints.yaml` — weight 2.5 — optional

**Why this matters:** Design constraints define the boundaries within which design decisions must operate — platform limitations, brand guidelines, technical dependencies, and regulatory requirements that shape the feasible solution space. Without them, constraints are discovered late in implementation.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| design-sec-con-001 | Constraints section present | warning (recommended) | 0.5 | {{ results['design-sec-con-001'].previous_status \| default('—') }} | {{ results['design-sec-con-001'].status }} | {{ results['design-sec-con-001'].trend_display }} | {{ results['design-sec-con-001'].evidence \| default('—') }} |
| design-sec-con-002 | Constraints are clearly stated as discrete restrictions | warning (recommended) | 0.5 | {{ results['design-sec-con-002'].previous_status \| default('—') }} | {{ results['design-sec-con-002'].status }} | {{ results['design-sec-con-002'].trend_display }} | {{ results['design-sec-con-002'].evidence \| default('—') }} |
| design-sec-con-003 | Traces to Philosophy (constrained_by) | warning (recommended) | 0.5 | {{ results['design-sec-con-003'].previous_status \| default('—') }} | {{ results['design-sec-con-003'].status }} | {{ results['design-sec-con-003'].trend_display }} | {{ results['design-sec-con-003'].evidence \| default('—') }} |
| design-sec-con-004 | Technology-independent | error (mandatory) | 1.0 | {{ results['design-sec-con-004'].previous_status \| default('—') }} | {{ results['design-sec-con-004'].status }} | {{ results['design-sec-con-004'].trend_display }} | {{ results['design-sec-con-004'].evidence \| default('—') }} |

## 6. Traceability — `06-traceability.yaml` — weight 1.5 — optional

**Why this matters:** Design traceability ensures every design decision, component, and visual element can be linked back to a requirement, principle, or user need. Without it, orphaned designs accumulate and impact analysis is impossible.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| design-sec-trace-001 | Traceability section present | warning (recommended) | 0.5 | {{ results['design-sec-trace-001'].previous_status \| default('—') }} | {{ results['design-sec-trace-001'].status }} | {{ results['design-sec-trace-001'].trend_display }} | {{ results['design-sec-trace-001'].evidence \| default('—') }} |
| design-sec-trace-002 | Links to Philosophy (traceable_to) | warning (recommended) | 0.5 | {{ results['design-sec-trace-002'].previous_status \| default('—') }} | {{ results['design-sec-trace-002'].status }} | {{ results['design-sec-trace-002'].trend_display }} | {{ results['design-sec-trace-002'].evidence \| default('—') }} |
| design-sec-trace-003 | Links to downstream (Feature Design — derives) | warning (recommended) | 0.5 | {{ results['design-sec-trace-003'].previous_status \| default('—') }} | {{ results['design-sec-trace-003'].status }} | {{ results['design-sec-trace-003'].trend_display }} | {{ results['design-sec-trace-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 6 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | design |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/06-design/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
