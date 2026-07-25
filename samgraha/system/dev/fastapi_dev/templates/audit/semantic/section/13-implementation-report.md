# Semantic Section Report — Implementation

**Document:** {{ document_path }}
**Standard:** `documentation-standards/13-implementation-standards.md`
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
| 1 | Generation Plan | **required** | {{ sections.generation_plan.score }} / 100 | {{ sections.generation_plan.previous_score | default('—') }} | {{ sections.generation_plan.trend_display }} |
| 2 | Security Fix Plan | **required** | {{ sections.security_fix_plan.score }} / 100 | {{ sections.security_fix_plan.previous_score | default('—') }} | {{ sections.security_fix_plan.trend_display }} |
| 3 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 4 | Refactor Plan | optional | {{ sections.refactor_plan.score }} / 100 | {{ sections.refactor_plan.previous_score | default('—') }} | {{ sections.refactor_plan.trend_display }} |
| 5 | Change Request Plan | optional | {{ sections.change_request_plan.score }} / 100 | {{ sections.change_request_plan.previous_score | default('—') }} | {{ sections.change_request_plan.trend_display }} |
| 6 | Enhancement Plan | optional | {{ sections.enhancement_plan.score }} / 100 | {{ sections.enhancement_plan.previous_score | default('—') }} | {{ sections.enhancement_plan.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Generation Plan — `section/13-implementation/01-generation_plan.md`

**Why this matters:** Code generation plan and approach — defines what is generated, from what sources, in what order, and under what constraints.

**Section Score: {{ sections.generation_plan.score }} / 100** ({{ sections.generation_plan.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['generation_plan.C1'].previous_passed_display \| default('—') }} | {{ results['generation_plan.C1'].passed_display }} | {{ results['generation_plan.C1'].trend_display }} | {{ results['generation_plan.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['generation_plan.C2'].previous_passed_display \| default('—') }} | {{ results['generation_plan.C2'].passed_display }} | {{ results['generation_plan.C2'].trend_display }} | {{ results['generation_plan.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['generation_plan.C3'].previous_passed_display \| default('—') }} | {{ results['generation_plan.C3'].passed_display }} | {{ results['generation_plan.C3'].trend_display }} | {{ results['generation_plan.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 2. Security Fix Plan — `02-security_fix_plan.md`

**Why this matters:** Security fix plan and remediation — defines what security issues are fixed, how they're addressed, and what threats they mitigate.

**Section Score: {{ sections.security_fix_plan.score }} / 100** ({{ sections.security_fix_plan.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['security_fix_plan.C1'].previous_passed_display \| default('—') }} | {{ results['security_fix_plan.C1'].passed_display }} | {{ results['security_fix_plan.C1'].trend_display }} | {{ results['security_fix_plan.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['security_fix_plan.C2'].previous_passed_display \| default('—') }} | {{ results['security_fix_plan.C2'].passed_display }} | {{ results['security_fix_plan.C2'].trend_display }} | {{ results['security_fix_plan.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['security_fix_plan.C3'].previous_passed_display \| default('—') }} | {{ results['security_fix_plan.C3'].passed_display }} | {{ results['security_fix_plan.C3'].trend_display }} | {{ results['security_fix_plan.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 3. Purpose — `03-purpose.md`

**Why this matters:** Implementation purpose and scope — defines why this implementation documentation exists and what it covers.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 4. Refactor Plan — `04-refactor_plan.md`

**Why this matters:** Refactor Plan documents a restructuring that changes internal design without changing external behavior. It exists so a reviewer can confirm the refactor is behavior-preserving before and after, not just trust the diff.

**Section Score: {{ sections.refactor_plan.score }} / 100** ({{ sections.refactor_plan.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['refactor_plan.C1'].previous_passed_display \| default('—') }} | {{ results['refactor_plan.C1'].passed_display }} | {{ results['refactor_plan.C1'].trend_display }} | {{ results['refactor_plan.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 35 | {{ results['refactor_plan.C2'].previous_passed_display \| default('—') }} | {{ results['refactor_plan.C2'].passed_display }} | {{ results['refactor_plan.C2'].trend_display }} | {{ results['refactor_plan.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['refactor_plan.C3'].previous_passed_display \| default('—') }} | {{ results['refactor_plan.C3'].passed_display }} | {{ results['refactor_plan.C3'].trend_display }} | {{ results['refactor_plan.C3'].evidence.excerpt \| default('—') }} |

C1: target architecture stated concretely. C2: behavior preservation strategy specified. C3: before/after test verification described.

## 5. Change Request Plan — `05-change_request_plan.md`

**Why this matters:** Change Request Plan documents a modification driven by an external request — its impact, how to undo it if wrong, and what tests need updating. It exists so scope creep and untested side effects are caught before merge.

**Section Score: {{ sections.change_request_plan.score }} / 100** ({{ sections.change_request_plan.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['change_request_plan.C1'].previous_passed_display \| default('—') }} | {{ results['change_request_plan.C1'].passed_display }} | {{ results['change_request_plan.C1'].trend_display }} | {{ results['change_request_plan.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 35 | {{ results['change_request_plan.C2'].previous_passed_display \| default('—') }} | {{ results['change_request_plan.C2'].passed_display }} | {{ results['change_request_plan.C2'].trend_display }} | {{ results['change_request_plan.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['change_request_plan.C3'].previous_passed_display \| default('—') }} | {{ results['change_request_plan.C3'].passed_display }} | {{ results['change_request_plan.C3'].trend_display }} | {{ results['change_request_plan.C3'].evidence.excerpt \| default('—') }} |

C1: impact analysis identifies affected components. C2: rollback strategy is concrete. C3: test updates identified (updated vs. new).

## 6. Enhancement Plan — `06-enhancement_plan.md`

**Why this matters:** Enhancement Plan documents an improvement to existing functionality that must not change core behavior. It exists to distinguish "made it better" from "changed what it does," with a measurable target for the improvement claim.

**Section Score: {{ sections.enhancement_plan.score }} / 100** ({{ sections.enhancement_plan.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['enhancement_plan.C1'].previous_passed_display \| default('—') }} | {{ results['enhancement_plan.C1'].passed_display }} | {{ results['enhancement_plan.C1'].trend_display }} | {{ results['enhancement_plan.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['enhancement_plan.C2'].previous_passed_display \| default('—') }} | {{ results['enhancement_plan.C2'].passed_display }} | {{ results['enhancement_plan.C2'].trend_display }} | {{ results['enhancement_plan.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['enhancement_plan.C3'].previous_passed_display \| default('—') }} | {{ results['enhancement_plan.C3'].passed_display }} | {{ results['enhancement_plan.C3'].trend_display }} | {{ results['enhancement_plan.C3'].evidence.excerpt \| default('—') }} |

C1: improvement target is measurable. C2: regression verification described. C3: explicit statement that core behavior is unchanged.

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
| Domain | implementation |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/13-implementation/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
