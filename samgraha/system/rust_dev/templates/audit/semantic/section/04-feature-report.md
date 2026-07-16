# Semantic Section Report — Feature

**Document:** {{ document_path }}
**Standard:** `documentation-standards/04-feature-standards.md`
**Rubric Files:** `audit/semantic/section/04-feature/*.md`
**Auditor:** LLM ({{ model_name }})
**Audit Date:** {{ created_at }}
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
| 1 | Purpose | **required** | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 2 | Functional Requirements | **required** | {{ sections.functional_requirements.score }} / 100 | {{ sections.functional_requirements.previous_score | default('—') }} | {{ sections.functional_requirements.trend_display }} |
| 3 | Acceptance Criteria | **required** | {{ sections.acceptance_criteria.score }} / 100 | {{ sections.acceptance_criteria.previous_score | default('—') }} | {{ sections.acceptance_criteria.trend_display }} |
| 4 | Business Rules | optional | {{ sections.business_rules.score }} / 100 | {{ sections.business_rules.previous_score | default('—') }} | {{ sections.business_rules.trend_display }} |
| 5 | Inputs | optional | {{ sections.inputs.score }} / 100 | {{ sections.inputs.previous_score | default('—') }} | {{ sections.inputs.trend_display }} |
| 6 | Outputs | optional | {{ sections.outputs.score }} / 100 | {{ sections.outputs.previous_score | default('—') }} | {{ sections.outputs.trend_display }} |
| 7 | Constraints | optional | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 8 | Dependencies | optional | {{ sections.dependencies.score }} / 100 | {{ sections.dependencies.previous_score | default('—') }} | {{ sections.dependencies.trend_display }} |
| 9 | Non-Goals | optional | {{ sections.non_goals.score }} / 100 | {{ sections.non_goals.previous_score | default('—') }} | {{ sections.non_goals.trend_display }} |
| 10 | Future Extensions | optional | {{ sections.future_extensions.score }} / 100 | {{ sections.future_extensions.previous_score | default('—') }} | {{ sections.future_extensions.trend_display }} |
| 11 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |
| 12 | Observability | not in standard | {{ sections.observability.score }} / 100 | {{ sections.observability.previous_score | default('—') }} | {{ sections.observability.trend_display }} |
| 13 | Stakeholders | not in standard | {{ sections.stakeholders.score }} / 100 | {{ sections.stakeholders.previous_score | default('—') }} | {{ sections.stakeholders.trend_display }} |
| 14 | Success Criteria | not in standard | {{ sections.success_criteria.score }} / 100 | {{ sections.success_criteria.previous_score | default('—') }} | {{ sections.success_criteria.trend_display }} |
| — | Generic (unmatched sections) | n/a | {{ sections.generic.score }} / 100 | {{ sections.generic.previous_score | default('—') }} | {{ sections.generic.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Purpose — `section/04-feature/01-purpose.md` — **required**

**Why this matters:** Purpose defines the feature's reason for existence and the problem it solves. A well-written purpose ensures everyone agrees on why the feature matters before discussing how to build it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display | default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display | default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display | default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt | default('—') }} |

C1: problem statement is clear and specific. C2: target users or stakeholders are identified. C3: purpose is concise and implementation-free.

## 2. Functional Requirements — `02-functional_requirements.md` — **required**

**Why this matters:** Functional requirements describe what the system must do. They must be complete, unambiguous, testable, and implementation-independent.

**Section Score: {{ sections.functional_requirements.score }} / 100** ({{ sections.functional_requirements.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['functional_requirements.C1'].previous_passed_display | default('—') }} | {{ results['functional_requirements.C1'].passed_display }} | {{ results['functional_requirements.C1'].trend_display }} | {{ results['functional_requirements.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['functional_requirements.C2'].previous_passed_display | default('—') }} | {{ results['functional_requirements.C2'].passed_display }} | {{ results['functional_requirements.C2'].trend_display }} | {{ results['functional_requirements.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['functional_requirements.C3'].previous_passed_display | default('—') }} | {{ results['functional_requirements.C3'].passed_display }} | {{ results['functional_requirements.C3'].trend_display }} | {{ results['functional_requirements.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['functional_requirements.C4'].previous_passed_display | default('—') }} | {{ results['functional_requirements.C4'].passed_display }} | {{ results['functional_requirements.C4'].trend_display }} | {{ results['functional_requirements.C4'].evidence.excerpt | default('—') }} |

C1: all requirements uniquely identified. C2: each requirement is testable. C3: no implementation language. C4: no duplicate or conflicting requirements.

## 3. Acceptance Criteria — `03-acceptance_criteria.md` — **required**

**Why this matters:** Acceptance criteria define conditions a feature must satisfy for stakeholder sign-off. They must be pass/fail testable, scoped to a single behavior, and written from the user's perspective.

**Section Score: {{ sections.acceptance_criteria.score }} / 100** ({{ sections.acceptance_criteria.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['acceptance_criteria.C1'].previous_passed_display | default('—') }} | {{ results['acceptance_criteria.C1'].passed_display }} | {{ results['acceptance_criteria.C1'].trend_display }} | {{ results['acceptance_criteria.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['acceptance_criteria.C2'].previous_passed_display | default('—') }} | {{ results['acceptance_criteria.C2'].passed_display }} | {{ results['acceptance_criteria.C2'].trend_display }} | {{ results['acceptance_criteria.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['acceptance_criteria.C3'].previous_passed_display | default('—') }} | {{ results['acceptance_criteria.C3'].passed_display }} | {{ results['acceptance_criteria.C3'].trend_display }} | {{ results['acceptance_criteria.C3'].evidence.excerpt | default('—') }} |

C1: every criterion is pass/fail testable. C2: each criterion tests a single behavior. C3: criteria use structured Given/When/Then format.

## 4. Business Rules — `04-business_rules.md`

**Why this matters:** Business rules encode domain logic, policies, calculations, and decision logic the system must enforce. They must be atomic, unambiguous, and expressed declaratively.

**Section Score: {{ sections.business_rules.score }} / 100** ({{ sections.business_rules.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['business_rules.C1'].previous_passed_display | default('—') }} | {{ results['business_rules.C1'].passed_display }} | {{ results['business_rules.C1'].trend_display }} | {{ results['business_rules.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['business_rules.C2'].previous_passed_display | default('—') }} | {{ results['business_rules.C2'].passed_display }} | {{ results['business_rules.C2'].trend_display }} | {{ results['business_rules.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['business_rules.C3'].previous_passed_display | default('—') }} | {{ results['business_rules.C3'].passed_display }} | {{ results['business_rules.C3'].trend_display }} | {{ results['business_rules.C3'].evidence.excerpt | default('—') }} |

C1: each rule is atomic and unambiguous. C2: rules are expressed declaratively. C3: exception paths are documented.

## 5. Inputs — `05-inputs.md`

**Why this matters:** Inputs define the data and triggers the system receives. They must specify source, format, frequency, volume, and validation rules.

**Section Score: {{ sections.inputs.score }} / 100** ({{ sections.inputs.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['inputs.C1'].previous_passed_display | default('—') }} | {{ results['inputs.C1'].passed_display }} | {{ results['inputs.C1'].trend_display }} | {{ results['inputs.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['inputs.C2'].previous_passed_display | default('—') }} | {{ results['inputs.C2'].passed_display }} | {{ results['inputs.C2'].trend_display }} | {{ results['inputs.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['inputs.C3'].previous_passed_display | default('—') }} | {{ results['inputs.C3'].passed_display }} | {{ results['inputs.C3'].trend_display }} | {{ results['inputs.C3'].evidence.excerpt | default('—') }} |

C1: every input has a defined source and format. C2: validation rules are specified. C3: input frequency and volume are quantified.

## 6. Outputs — `06-outputs.md`

**Why this matters:** Outputs define what the system produces or exposes. They must specify format, destination, frequency, and data structure.

**Section Score: {{ sections.outputs.score }} / 100** ({{ sections.outputs.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['outputs.C1'].previous_passed_display | default('—') }} | {{ results['outputs.C1'].passed_display }} | {{ results['outputs.C1'].trend_display }} | {{ results['outputs.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['outputs.C2'].previous_passed_display | default('—') }} | {{ results['outputs.C2'].passed_display }} | {{ results['outputs.C2'].trend_display }} | {{ results['outputs.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['outputs.C3'].previous_passed_display | default('—') }} | {{ results['outputs.C3'].passed_display }} | {{ results['outputs.C3'].trend_display }} | {{ results['outputs.C3'].evidence.excerpt | default('—') }} |

C1: every output has a defined consumer and format. C2: output schema or structure is specified. C3: output frequency and volume are quantified.

## 7. Constraints — `07-constraints.md`

**Why this matters:** Constraints define boundaries the implementation must operate within. They must be specific, justified, and non-negotiable.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['constraints.C1'].previous_passed_display | default('—') }} | {{ results['constraints.C1'].passed_display }} | {{ results['constraints.C1'].trend_display }} | {{ results['constraints.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['constraints.C2'].previous_passed_display | default('—') }} | {{ results['constraints.C2'].passed_display }} | {{ results['constraints.C2'].trend_display }} | {{ results['constraints.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['constraints.C3'].previous_passed_display | default('—') }} | {{ results['constraints.C3'].passed_display }} | {{ results['constraints.C3'].trend_display }} | {{ results['constraints.C3'].evidence.excerpt | default('—') }} |

C1: each constraint is specific and measurable. C2: each constraint has a clear justification. C3: no contradictory constraints.

## 8. Dependencies — `08-dependencies.md`

**Why this matters:** Dependencies enumerate external systems, services, libraries, or teams the feature relies on. They must specify dependency type, version, interface contract, and failure impact.

**Section Score: {{ sections.dependencies.score }} / 100** ({{ sections.dependencies.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['dependencies.C1'].previous_passed_display | default('—') }} | {{ results['dependencies.C1'].passed_display }} | {{ results['dependencies.C1'].trend_display }} | {{ results['dependencies.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['dependencies.C2'].previous_passed_display | default('—') }} | {{ results['dependencies.C2'].passed_display }} | {{ results['dependencies.C2'].trend_display }} | {{ results['dependencies.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['dependencies.C3'].previous_passed_display | default('—') }} | {{ results['dependencies.C3'].passed_display }} | {{ results['dependencies.C3'].trend_display }} | {{ results['dependencies.C3'].evidence.excerpt | default('—') }} |

C1: every dependency has a name and version. C2: interface or integration point is documented. C3: failure impact is assessed for each dependency.

## 9. Non-Goals — `09-non_goals.md`

**Why this matters:** Non-goals explicitly state what the feature will NOT address. They prevent scope creep and set stakeholder expectations.

**Section Score: {{ sections.non_goals.score }} / 100** ({{ sections.non_goals.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['non_goals.C1'].previous_passed_display | default('—') }} | {{ results['non_goals.C1'].passed_display }} | {{ results['non_goals.C1'].trend_display }} | {{ results['non_goals.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['non_goals.C2'].previous_passed_display | default('—') }} | {{ results['non_goals.C2'].passed_display }} | {{ results['non_goals.C2'].trend_display }} | {{ results['non_goals.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['non_goals.C3'].previous_passed_display | default('—') }} | {{ results['non_goals.C3'].passed_display }} | {{ results['non_goals.C3'].trend_display }} | {{ results['non_goals.C3'].evidence.excerpt | default('—') }} |

C1: each non-goal is specific and explicitly excluded. C2: exclusion rationale is provided. C3: non-goals are distinct from future extensions.

## 10. Future Extensions — `10-future_extensions.md`

**Why this matters:** Future extensions document planned or possible enhancements beyond the current scope. They must be clearly marked as out-of-scope, prioritized, and linked to trigger conditions.

**Section Score: {{ sections.future_extensions.score }} / 100** ({{ sections.future_extensions.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['future_extensions.C1'].previous_passed_display | default('—') }} | {{ results['future_extensions.C1'].passed_display }} | {{ results['future_extensions.C1'].trend_display }} | {{ results['future_extensions.C1'].evidence.excerpt | default('—') }} |
| C2 | recommended | 30 | {{ results['future_extensions.C2'].previous_passed_display | default('—') }} | {{ results['future_extensions.C2'].passed_display }} | {{ results['future_extensions.C2'].trend_display }} | {{ results['future_extensions.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['future_extensions.C3'].previous_passed_display | default('—') }} | {{ results['future_extensions.C3'].passed_display }} | {{ results['future_extensions.C3'].trend_display }} | {{ results['future_extensions.C3'].evidence.excerpt | default('—') }} |

C1: extensions are clearly marked as out of scope. C2: each extension has a trigger condition. C3: architectural impact is noted.

## 11. Traceability — `11-traceability.md`

**Why this matters:** Traceability maps requirements back to Vision and forward to Design, Technical, and Implementation. Without it, impact analysis is impossible.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['traceability.C1'].previous_passed_display | default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display | default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['traceability.C3'].previous_passed_display | default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt | default('—') }} |

C1: every requirement has at least one trace link. C2: every test case traces to a requirement. C3: traceability is bidirectional and complete.

## 12. Observability — `12-observability.md` — not in Required Sections table

**Why this matters:** A feature must be observable in production. Operators need to determine current health, diagnose failures, and track business outcomes without modifying code.

**Section Score: {{ sections.observability.score }} / 100** ({{ sections.observability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['observability.C1'].previous_passed_display | default('—') }} | {{ results['observability.C1'].passed_display }} | {{ results['observability.C1'].trend_display }} | {{ results['observability.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['observability.C2'].previous_passed_display | default('—') }} | {{ results['observability.C2'].passed_display }} | {{ results['observability.C2'].trend_display }} | {{ results['observability.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['observability.C3'].previous_passed_display | default('—') }} | {{ results['observability.C3'].passed_display }} | {{ results['observability.C3'].trend_display }} | {{ results['observability.C3'].evidence.excerpt | default('—') }} |

C1: SLIs (rate, error, latency) enumerated and linked to performance targets. C2: logging strategy defined with structured fields and correlation ID. C3: alert thresholds specified for primary failure modes.

## 13. Stakeholders — `13-stakeholders.md` — not in Required Sections table

**Why this matters:** Stakeholders identify individuals or groups with interest in the feature's outcome. They must specify role, responsibility, and engagement model.

**Section Score: {{ sections.stakeholders.score }} / 100** ({{ sections.stakeholders.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['stakeholders.C1'].previous_passed_display | default('—') }} | {{ results['stakeholders.C1'].passed_display }} | {{ results['stakeholders.C1'].trend_display }} | {{ results['stakeholders.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['stakeholders.C2'].previous_passed_display | default('—') }} | {{ results['stakeholders.C2'].passed_display }} | {{ results['stakeholders.C2'].trend_display }} | {{ results['stakeholders.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['stakeholders.C3'].previous_passed_display | default('—') }} | {{ results['stakeholders.C3'].passed_display }} | {{ results['stakeholders.C3'].trend_display }} | {{ results['stakeholders.C3'].evidence.excerpt | default('—') }} |

C1: every stakeholder has a defined role and responsibility. C2: decision authority is assigned. C3: engagement model or frequency is documented.

## 14. Success Criteria — `14-success_criteria.md` — not in Required Sections table

**Why this matters:** Success criteria define how stakeholders will verify the feature delivers its intended value. They must be measurable, time-bound, and tied to business outcomes.

**Section Score: {{ sections.success_criteria.score }} / 100** ({{ sections.success_criteria.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['success_criteria.C1'].previous_passed_display | default('—') }} | {{ results['success_criteria.C1'].passed_display }} | {{ results['success_criteria.C1'].trend_display }} | {{ results['success_criteria.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['success_criteria.C2'].previous_passed_display | default('—') }} | {{ results['success_criteria.C2'].passed_display }} | {{ results['success_criteria.C2'].trend_display }} | {{ results['success_criteria.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['success_criteria.C3'].previous_passed_display | default('—') }} | {{ results['success_criteria.C3'].passed_display }} | {{ results['success_criteria.C3'].trend_display }} | {{ results['success_criteria.C3'].evidence.excerpt | default('—') }} |

C1: criteria are specific, measurable, and time-bound. C2: criteria are tied to business outcomes. C3: criteria include leading and lagging indicators.

## Generic — `generic.md` (sections with no matching semantic_type)

**Why this matters:** Catches feature-relevant content an author wrote under a heading that doesn't match any of the 14 named section types above — still judged for relevance and non-duplication.

**Section Score: {{ sections.generic.score }} / 100** ({{ sections.generic.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['generic.C1'].previous_passed_display | default('—') }} | {{ results['generic.C1'].passed_display }} | {{ results['generic.C1'].trend_display }} | {{ results['generic.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['generic.C2'].previous_passed_display | default('—') }} | {{ results['generic.C2'].passed_display }} | {{ results['generic.C2'].trend_display }} | {{ results['generic.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['generic.C3'].previous_passed_display | default('—') }} | {{ results['generic.C3'].passed_display }} | {{ results['generic.C3'].trend_display }} | {{ results['generic.C3'].evidence.excerpt | default('—') }} |

C1: content is technically substantive. C2: section purpose is clearly stated. C3: content does not duplicate other sections.

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
| Domain | feature |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/04-feature/*.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
