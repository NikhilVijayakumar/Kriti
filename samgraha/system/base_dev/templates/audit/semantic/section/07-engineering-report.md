# Semantic Section Report — Engineering

**Document:** {{ document_path }}
**Standard:** `documentation-standards/07-engineering-standards.md`
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
| 1 | Guiding Principles | **required** | {{ sections.guiding_principles.score }} / 100 | {{ sections.guiding_principles.previous_score | default('—') }} | {{ sections.guiding_principles.trend_display }} |
| 2 | Rationale | **required** | {{ sections.rationale.score }} / 100 | {{ sections.rationale.previous_score | default('—') }} | {{ sections.rationale.trend_display }} |
| 3 | Build Standards | **required** | {{ sections.build_standards.score }} / 100 | {{ sections.build_standards.previous_score | default('—') }} | {{ sections.build_standards.trend_display }} |
| 4 | Testing Standards | **required** | {{ sections.testing_standards.score }} / 100 | {{ sections.testing_standards.previous_score | default('—') }} | {{ sections.testing_standards.trend_display }} |
| 5 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 6 | Code Standards | optional | {{ sections.code_standards.score }} / 100 | {{ sections.code_standards.previous_score | default('—') }} | {{ sections.code_standards.trend_display }} |
| 7 | Constraints | optional | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 8 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Guiding Principles — `section/07-engineering/01-guiding_principles.md`

**Why this matters:** Engineering guiding principles — the non-negotiable rules that guide every engineering decision in the system.

**Section Score: {{ sections.guiding_principles.score }} / 100** ({{ sections.guiding_principles.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['guiding_principles.C1'].previous_passed_display \| default('—') }} | {{ results['guiding_principles.C1'].passed_display }} | {{ results['guiding_principles.C1'].trend_display }} | {{ results['guiding_principles.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['guiding_principles.C2'].previous_passed_display \| default('—') }} | {{ results['guiding_principles.C2'].passed_display }} | {{ results['guiding_principles.C2'].trend_display }} | {{ results['guiding_principles.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['guiding_principles.C3'].previous_passed_display \| default('—') }} | {{ results['guiding_principles.C3'].passed_display }} | {{ results['guiding_principles.C3'].trend_display }} | {{ results['guiding_principles.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 2. Rationale — `02-rationale.md`

**Why this matters:** Engineering rationale — explains why engineering standards exist and what trade-offs were made.

**Section Score: {{ sections.rationale.score }} / 100** ({{ sections.rationale.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['rationale.C1'].previous_passed_display \| default('—') }} | {{ results['rationale.C1'].passed_display }} | {{ results['rationale.C1'].trend_display }} | {{ results['rationale.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['rationale.C2'].previous_passed_display \| default('—') }} | {{ results['rationale.C2'].passed_display }} | {{ results['rationale.C2'].trend_display }} | {{ results['rationale.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['rationale.C3'].previous_passed_display \| default('—') }} | {{ results['rationale.C3'].passed_display }} | {{ results['rationale.C3'].trend_display }} | {{ results['rationale.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 3. Build Standards — `03-build_standards.md`

**Why this matters:** Build standards — defines how code is built, tested, and released, including versioning strategy and dependency management.

**Section Score: {{ sections.build_standards.score }} / 100** ({{ sections.build_standards.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['build_standards.C1'].previous_passed_display \| default('—') }} | {{ results['build_standards.C1'].passed_display }} | {{ results['build_standards.C1'].trend_display }} | {{ results['build_standards.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['build_standards.C2'].previous_passed_display \| default('—') }} | {{ results['build_standards.C2'].passed_display }} | {{ results['build_standards.C2'].trend_display }} | {{ results['build_standards.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['build_standards.C3'].previous_passed_display \| default('—') }} | {{ results['build_standards.C3'].passed_display }} | {{ results['build_standards.C3'].trend_display }} | {{ results['build_standards.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 4. Testing Standards — `04-testing_standards.md`

**Why this matters:** Testing standards — defines what tests exist, what they cover, and what quality gates they enforce.

**Section Score: {{ sections.testing_standards.score }} / 100** ({{ sections.testing_standards.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['testing_standards.C1'].previous_passed_display \| default('—') }} | {{ results['testing_standards.C1'].passed_display }} | {{ results['testing_standards.C1'].trend_display }} | {{ results['testing_standards.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['testing_standards.C2'].previous_passed_display \| default('—') }} | {{ results['testing_standards.C2'].passed_display }} | {{ results['testing_standards.C2'].trend_display }} | {{ results['testing_standards.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['testing_standards.C3'].previous_passed_display \| default('—') }} | {{ results['testing_standards.C3'].passed_display }} | {{ results['testing_standards.C3'].trend_display }} | {{ results['testing_standards.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 5. Purpose — `05-purpose.md`

**Why this matters:** Engineering purpose — defines why this engineering documentation exists and what it covers.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 6. Code Standards — `06-code_standards.md`

**Why this matters:** Code standards — defines coding conventions including naming, formatting, documentation, and style guidelines.

**Section Score: {{ sections.code_standards.score }} / 100** ({{ sections.code_standards.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['code_standards.C1'].previous_passed_display \| default('—') }} | {{ results['code_standards.C1'].passed_display }} | {{ results['code_standards.C1'].trend_display }} | {{ results['code_standards.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['code_standards.C2'].previous_passed_display \| default('—') }} | {{ results['code_standards.C2'].passed_display }} | {{ results['code_standards.C2'].trend_display }} | {{ results['code_standards.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['code_standards.C3'].previous_passed_display \| default('—') }} | {{ results['code_standards.C3'].passed_display }} | {{ results['code_standards.C3'].trend_display }} | {{ results['code_standards.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 7. Constraints — `07-constraints.md`

**Why this matters:** Engineering constraints — defines the boundaries on engineering decisions that must hold regardless of design.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['constraints.C1'].previous_passed_display \| default('—') }} | {{ results['constraints.C1'].passed_display }} | {{ results['constraints.C1'].trend_display }} | {{ results['constraints.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['constraints.C2'].previous_passed_display \| default('—') }} | {{ results['constraints.C2'].passed_display }} | {{ results['constraints.C2'].trend_display }} | {{ results['constraints.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['constraints.C3'].previous_passed_display \| default('—') }} | {{ results['constraints.C3'].passed_display }} | {{ results['constraints.C3'].trend_display }} | {{ results['constraints.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 8. Traceability — `08-traceability.md`

**Why this matters:** Engineering traceability — maps engineering decisions back to Philosophy and Architecture and forward to Implementation.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['traceability.C1'].previous_passed_display \| default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display \| default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['traceability.C3'].previous_passed_display \| default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

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
| Domain | engineering |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/07-engineering/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
