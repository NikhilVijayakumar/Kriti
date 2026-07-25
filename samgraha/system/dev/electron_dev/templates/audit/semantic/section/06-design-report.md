# Semantic Section Report — Design

**Document:** {{ document_path }}
**Standard:** `documentation-standards/06-design-standards.md`
**Audit Date:** {{ created_at }}
**Auditor:** LLM ({{ model_name }})
**Revision:** {{ revision_number }}

---

## Score

**Semantic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the section scores below, for sections actually present in the document
section_score = sum of passed criterion points in that section, capped at 100
# calculation: semantic_section_v1
```

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs — this revision is the baseline every future run is compared against.{% endif %}

### Score by Model

| Model | Runs | Avg Score | Min | Max |
|---|---:|---:|---:|---|
{% for m in model_scores -%}
| {{ m.model_name }} | {{ m.run_count }} | {{ m.avg_score }} / 100 | {{ m.min_score }} / 100 | {{ m.max_score }} / 100 |
{% endfor %}

### Section Scores

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Design Principles | **required** | {{ sections.design_principles.score }} / 100 | {{ sections.design_principles.previous_score | default('—') }} | {{ sections.design_principles.trend_display }} |
| 2 | UX Principles | **required** | {{ sections.ux_principles.score }} / 100 | {{ sections.ux_principles.previous_score | default('—') }} | {{ sections.ux_principles.trend_display }} |
| 3 | Accessibility | **required** | {{ sections.accessibility.score }} / 100 | {{ sections.accessibility.previous_score | default('—') }} | {{ sections.accessibility.trend_display }} |
| 4 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Constraints | optional | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 6 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Design Principles — `section/06-design/01-design_principles.md`

**Why this matters:** Design principles are the foundational rules guiding visual and interaction decisions. They ensure consistency, coherence, and a unified product identity across all surfaces.

**Section Score: {{ sections.design_principles.score }} / 100** ({{ sections.design_principles.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['design_principles.C1'].previous_passed_display \| default('—') }} | {{ results['design_principles.C1'].passed_display }} | {{ results['design_principles.C1'].trend_display }} | {{ results['design_principles.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['design_principles.C2'].previous_passed_display \| default('—') }} | {{ results['design_principles.C2'].passed_display }} | {{ results['design_principles.C2'].trend_display }} | {{ results['design_principles.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['design_principles.C3'].previous_passed_display \| default('—') }} | {{ results['design_principles.C3'].passed_display }} | {{ results['design_principles.C3'].trend_display }} | {{ results['design_principles.C3'].evidence.excerpt \| default('—') }} |

C1: design principles are documented and distinct. C2: principles consistently applied across components. C3: principles used as decision-making criteria in reviews.

## 2. UX Principles — `02-ux_principles.md`

**Why this matters:** UX principles operationalize human-centered design into actionable heuristics. They govern interaction patterns, information architecture, and user flows to ensure intuitive and efficient experiences.

**Section Score: {{ sections.ux_principles.score }} / 100** ({{ sections.ux_principles.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['ux_principles.C1'].previous_passed_display \| default('—') }} | {{ results['ux_principles.C1'].passed_display }} | {{ results['ux_principles.C1'].trend_display }} | {{ results['ux_principles.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['ux_principles.C2'].previous_passed_display \| default('—') }} | {{ results['ux_principles.C2'].passed_display }} | {{ results['ux_principles.C2'].trend_display }} | {{ results['ux_principles.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 20 | {{ results['ux_principles.C3'].previous_passed_display \| default('—') }} | {{ results['ux_principles.C3'].passed_display }} | {{ results['ux_principles.C3'].trend_display }} | {{ results['ux_principles.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['ux_principles.C4'].previous_passed_display \| default('—') }} | {{ results['ux_principles.C4'].passed_display }} | {{ results['ux_principles.C4'].trend_display }} | {{ results['ux_principles.C4'].evidence.excerpt \| default('—') }} |

C1: UX principles documented and grounded in HCI heuristics. C2: user flows define happy and error paths. C3: consistency in navigation, labeling, and feedback. C4: primary task step count is bounded with numeric limit and explicit exception criteria.

## 3. Accessibility — `03-accessibility.md`

**Why this matters:** Accessibility ensures the product is usable by people with diverse abilities. Compliance with WCAG standards is both a legal requirement and a design quality benchmark.

**Section Score: {{ sections.accessibility.score }} / 100** ({{ sections.accessibility.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['accessibility.C1'].previous_passed_display \| default('—') }} | {{ results['accessibility.C1'].passed_display }} | {{ results['accessibility.C1'].trend_display }} | {{ results['accessibility.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['accessibility.C2'].previous_passed_display \| default('—') }} | {{ results['accessibility.C2'].passed_display }} | {{ results['accessibility.C2'].trend_display }} | {{ results['accessibility.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 20 | {{ results['accessibility.C3'].previous_passed_display \| default('—') }} | {{ results['accessibility.C3'].passed_display }} | {{ results['accessibility.C3'].trend_display }} | {{ results['accessibility.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['accessibility.C4'].previous_passed_display \| default('—') }} | {{ results['accessibility.C4'].passed_display }} | {{ results['accessibility.C4'].trend_display }} | {{ results['accessibility.C4'].evidence.excerpt \| default('—') }} |

C1: WCAG 2.1 AA compliance for all screens. C2: keyboard navigation and focus management work. C3: ARIA labels and semantic structure correct. C4: internationalization readiness — RTL support, string externalization, locale-aware formatting.

## 4. Purpose — `04-purpose.md`

**Why this matters:** Design purpose defines the strategic intent behind visual and interaction decisions. Every element must serve a clear functional or communicative goal aligned with product vision.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: design purpose documented for each major screen. C2: purpose traceable to user or business need. C3: no unexplained decorative elements.

## 5. Constraints — `05-constraints.md`

**Why this matters:** Design constraints define the boundaries within which design decisions must operate — platform limitations, brand guidelines, technical dependencies, and regulatory requirements that shape the feasible solution space.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['constraints.C1'].previous_passed_display \| default('—') }} | {{ results['constraints.C1'].passed_display }} | {{ results['constraints.C1'].trend_display }} | {{ results['constraints.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['constraints.C2'].previous_passed_display \| default('—') }} | {{ results['constraints.C2'].passed_display }} | {{ results['constraints.C2'].trend_display }} | {{ results['constraints.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['constraints.C3'].previous_passed_display \| default('—') }} | {{ results['constraints.C3'].passed_display }} | {{ results['constraints.C3'].trend_display }} | {{ results['constraints.C3'].evidence.excerpt \| default('—') }} |

C1: all design constraints documented and categorized. C2: brand and platform constraints have defined sources. C3: constraint conflicts identified with fallback strategies.

## 6. Traceability — `06-traceability.md`

**Why this matters:** Design traceability ensures every design decision, component, and visual element can be linked back to a requirement, principle, or user need. It prevents orphaned designs and enables impact analysis.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['traceability.C1'].previous_passed_display \| default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display \| default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['traceability.C3'].previous_passed_display \| default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt \| default('—') }} |

C1: all design components traceable to requirements. C2: bidirectional traceability matrix exists. C3: design change log records rationale and affected requirements.

---

## All Findings

{% if findings | length > 0 %}
| Section | Criterion | Severity | Evidence | Message | New This Run? |
|---|---|---|---|---|---|
{% for f in findings -%}
| {{ f.section_type }} | {{ f.criterion_id }} | {{ f.severity }} | {{ f.evidence.excerpt | default('—') }} | {{ f.message }} | {{ 'Yes — regression' if f.is_new_finding else 'No — carried over' }} |
{% endfor %}
{% else %}
No findings.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | design |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/06-design/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
