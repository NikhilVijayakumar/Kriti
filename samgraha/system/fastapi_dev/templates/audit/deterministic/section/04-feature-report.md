# Deterministic Section Report — Feature

**Document:** {{ document_path }}
**Standard:** `documentation-standards/04-feature-standards.md`
**Rule Files:** `audit/deterministic/section/04-feature/*.yaml`
**Auditor:** System (deterministic engine)
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 11 section scores below
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
| 1 | Purpose | **required** | 4.0 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 2 | Functional Requirements | **required** | 4.0 | {{ sections.functional_requirements.score }} / 100 | {{ sections.functional_requirements.previous_score | default('—') }} | {{ sections.functional_requirements.trend_display }} |
| 3 | Acceptance Criteria | **required** | 4.0 | {{ sections.acceptance_criteria.score }} / 100 | {{ sections.acceptance_criteria.previous_score | default('—') }} | {{ sections.acceptance_criteria.trend_display }} |
| 4 | Business Rules | optional | 2.5 | {{ sections.business_rules.score }} / 100 | {{ sections.business_rules.previous_score | default('—') }} | {{ sections.business_rules.trend_display }} |
| 5 | Inputs | optional | 1.5 | {{ sections.inputs.score }} / 100 | {{ sections.inputs.previous_score | default('—') }} | {{ sections.inputs.trend_display }} |
| 6 | Outputs | optional | 1.5 | {{ sections.outputs.score }} / 100 | {{ sections.outputs.previous_score | default('—') }} | {{ sections.outputs.trend_display }} |
| 7 | Constraints | optional | 1.5 | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 8 | Dependencies | optional | 2.0 | {{ sections.dependencies.score }} / 100 | {{ sections.dependencies.previous_score | default('—') }} | {{ sections.dependencies.trend_display }} |
| 9 | Non-Goals | optional | 2.0 | {{ sections.non_goals.score }} / 100 | {{ sections.non_goals.previous_score | default('—') }} | {{ sections.non_goals.trend_display }} |
| 10 | Future Extensions | optional | 2.0 | {{ sections.future_extensions.score }} / 100 | {{ sections.future_extensions.previous_score | default('—') }} | {{ sections.future_extensions.trend_display }} |
| 11 | Traceability | optional | 1.5 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

The 3 required sections carry 12.0 of the document's 26.5 total rule weight — a document can only pass if those three are both present and internally sound; the remaining eight are recommended-quality signal, not gating.

---

## 1. Purpose — weight 4.0 — **required**

**Why this matters:** Purpose defines the feature's reason for existence and the problem it solves. Without it, every downstream section has no shared context to build on.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-purpose-001 | Purpose section exists | error (mandatory) | 1.5 | {{ results['feat-sec-purpose-001'].previous_status | default('—') }} | {{ results['feat-sec-purpose-001'].status }} | {{ results['feat-sec-purpose-001'].trend_display }} | {{ results['feat-sec-purpose-001'].evidence | default('—') }} |
| feat-sec-purpose-002 | States feature intent | error (mandatory) | 1.0 | {{ results['feat-sec-purpose-002'].previous_status | default('—') }} | {{ results['feat-sec-purpose-002'].status }} | {{ results['feat-sec-purpose-002'].trend_display }} | {{ results['feat-sec-purpose-002'].evidence | default('—') }} |
| feat-sec-purpose-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['feat-sec-purpose-003'].previous_status | default('—') }} | {{ results['feat-sec-purpose-003'].status }} | {{ results['feat-sec-purpose-003'].trend_display }} | {{ results['feat-sec-purpose-003'].evidence | default('—') }} |
| feat-sec-purpose-004 | Scope boundaries defined | warning (recommended) | 0.5 | {{ results['feat-sec-purpose-004'].previous_status | default('—') }} | {{ results['feat-sec-purpose-004'].status }} | {{ results['feat-sec-purpose-004'].trend_display }} | {{ results['feat-sec-purpose-004'].evidence | default('—') }} |

## 2. Functional Requirements — weight 4.0 — **required**

**Why this matters:** Functional Requirements are the core of what the feature must do. Without individually listed, testable requirements, there's nothing for Design, Technical, or QA to work against.

**Section Score: {{ sections.functional_requirements.score }} / 100** ({{ sections.functional_requirements.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-freq-001 | Functional Requirements section exists | error (mandatory) | 1.5 | {{ results['feat-sec-freq-001'].previous_status | default('—') }} | {{ results['feat-sec-freq-001'].status }} | {{ results['feat-sec-freq-001'].trend_display }} | {{ results['feat-sec-freq-001'].evidence | default('—') }} |
| feat-sec-freq-002 | Requirements listed individually (≥ 2 distinct requirements) | error (mandatory) | 1.0 | {{ results['feat-sec-freq-002'].previous_status | default('—') }} | {{ results['feat-sec-freq-002'].status }} | {{ results['feat-sec-freq-002'].trend_display }} | {{ results['feat-sec-freq-002'].evidence | default('—') }} |
| feat-sec-freq-003 | Each requirement is testable | warning (recommended) | 0.5 | {{ results['feat-sec-freq-003'].previous_status | default('—') }} | {{ results['feat-sec-freq-003'].status }} | {{ results['feat-sec-freq-003'].trend_display }} | {{ results['feat-sec-freq-003'].evidence | default('—') }} |
| feat-sec-freq-004 | Technology-independent | error (mandatory) | 1.0 | {{ results['feat-sec-freq-004'].previous_status | default('—') }} | {{ results['feat-sec-freq-004'].status }} | {{ results['feat-sec-freq-004'].trend_display }} | {{ results['feat-sec-freq-004'].evidence | default('—') }} |

## 3. Acceptance Criteria — weight 4.0 — **required**

**Why this matters:** Acceptance Criteria are the pass/fail tests for the feature. Without them, there's no way to verify the feature was implemented correctly — every requirement is unverifiable.

**Section Score: {{ sections.acceptance_criteria.score }} / 100** ({{ sections.acceptance_criteria.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-ac-001 | Acceptance Criteria section exists | error (mandatory) | 1.5 | {{ results['feat-sec-ac-001'].previous_status | default('—') }} | {{ results['feat-sec-ac-001'].status }} | {{ results['feat-sec-ac-001'].trend_display }} | {{ results['feat-sec-ac-001'].evidence | default('—') }} |
| feat-sec-ac-002 | Criteria are testable | error (mandatory) | 1.0 | {{ results['feat-sec-ac-002'].previous_status | default('—') }} | {{ results['feat-sec-ac-002'].status }} | {{ results['feat-sec-ac-002'].trend_display }} | {{ results['feat-sec-ac-002'].evidence | default('—') }} |
| feat-sec-ac-003 | Covers happy path and edge cases | warning (recommended) | 0.5 | {{ results['feat-sec-ac-003'].previous_status | default('—') }} | {{ results['feat-sec-ac-003'].status }} | {{ results['feat-sec-ac-003'].trend_display }} | {{ results['feat-sec-ac-003'].evidence | default('—') }} |
| feat-sec-ac-004 | Technology-independent | error (mandatory) | 1.0 | {{ results['feat-sec-ac-004'].previous_status | default('—') }} | {{ results['feat-sec-ac-004'].status }} | {{ results['feat-sec-ac-004'].trend_display }} | {{ results['feat-sec-ac-004'].evidence | default('—') }} |

## 4. Business Rules — weight 2.5 — optional

**Why this matters:** Business Rules encode domain logic, policies, and decision logic the system must enforce. Without them, Acceptance Criteria have no domain grounding.

**Section Score: {{ sections.business_rules.score }} / 100** ({{ sections.business_rules.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-br-001 | Business Rules section exists | warning (recommended) | 0.5 | {{ results['feat-sec-br-001'].previous_status | default('—') }} | {{ results['feat-sec-br-001'].status }} | {{ results['feat-sec-br-001'].trend_display }} | {{ results['feat-sec-br-001'].evidence | default('—') }} |
| feat-sec-br-002 | Rules are clearly stated | warning (recommended) | 0.5 | {{ results['feat-sec-br-002'].previous_status | default('—') }} | {{ results['feat-sec-br-002'].status }} | {{ results['feat-sec-br-002'].trend_display }} | {{ results['feat-sec-br-002'].evidence | default('—') }} |
| feat-sec-br-003 | Rules trace to requirements | warning (recommended) | 0.5 | {{ results['feat-sec-br-003'].previous_status | default('—') }} | {{ results['feat-sec-br-003'].status }} | {{ results['feat-sec-br-003'].trend_display }} | {{ results['feat-sec-br-003'].evidence | default('—') }} |
| feat-sec-br-004 | Technology-independent | error (mandatory) | 1.0 | {{ results['feat-sec-br-004'].previous_status | default('—') }} | {{ results['feat-sec-br-004'].status }} | {{ results['feat-sec-br-004'].trend_display }} | {{ results['feat-sec-br-004'].evidence | default('—') }} |

## 5. Inputs — weight 1.5 — optional

**Why this matters:** Inputs define the data and triggers the feature consumes. Without them, boundary testing and data flow verification are impossible.

**Section Score: {{ sections.inputs.score }} / 100** ({{ sections.inputs.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-inputs-001 | Inputs section exists | warning (recommended) | 0.5 | {{ results['feat-sec-inputs-001'].previous_status | default('—') }} | {{ results['feat-sec-inputs-001'].status }} | {{ results['feat-sec-inputs-001'].trend_display }} | {{ results['feat-sec-inputs-001'].evidence | default('—') }} |
| feat-sec-inputs-002 | Inputs are enumerated | warning (recommended) | 0.5 | {{ results['feat-sec-inputs-002'].previous_status | default('—') }} | {{ results['feat-sec-inputs-002'].status }} | {{ results['feat-sec-inputs-002'].trend_display }} | {{ results['feat-sec-inputs-002'].evidence | default('—') }} |
| feat-sec-inputs-003 | Each input has a source | warning (recommended) | 0.5 | {{ results['feat-sec-inputs-003'].previous_status | default('—') }} | {{ results['feat-sec-inputs-003'].status }} | {{ results['feat-sec-inputs-003'].trend_display }} | {{ results['feat-sec-inputs-003'].evidence | default('—') }} |

## 6. Outputs — weight 1.5 — optional

**Why this matters:** Outputs define what the feature produces or exposes. Without them, integration testing and consumer contract verification are impossible.

**Section Score: {{ sections.outputs.score }} / 100** ({{ sections.outputs.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-outputs-001 | Outputs section exists | warning (recommended) | 0.5 | {{ results['feat-sec-outputs-001'].previous_status | default('—') }} | {{ results['feat-sec-outputs-001'].status }} | {{ results['feat-sec-outputs-001'].trend_display }} | {{ results['feat-sec-outputs-001'].evidence | default('—') }} |
| feat-sec-outputs-002 | Outputs are enumerated | warning (recommended) | 0.5 | {{ results['feat-sec-outputs-002'].previous_status | default('—') }} | {{ results['feat-sec-outputs-002'].status }} | {{ results['feat-sec-outputs-002'].trend_display }} | {{ results['feat-sec-outputs-002'].evidence | default('—') }} |
| feat-sec-outputs-003 | Each output has a consumer | warning (recommended) | 0.5 | {{ results['feat-sec-outputs-003'].previous_status | default('—') }} | {{ results['feat-sec-outputs-003'].status }} | {{ results['feat-sec-outputs-003'].trend_display }} | {{ results['feat-sec-outputs-003'].evidence | default('—') }} |

## 7. Constraints — weight 1.5 — optional

**Why this matters:** Constraints define boundaries the implementation must operate within. Without them, Implementation and Build have no explicit restrictions to respect.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-con-001 | Constraints section exists | warning (recommended) | 0.5 | {{ results['feat-sec-con-001'].previous_status | default('—') }} | {{ results['feat-sec-con-001'].status }} | {{ results['feat-sec-con-001'].trend_display }} | {{ results['feat-sec-con-001'].evidence | default('—') }} |
| feat-sec-con-002 | Constraints are clearly stated | warning (recommended) | 0.5 | {{ results['feat-sec-con-002'].previous_status | default('—') }} | {{ results['feat-sec-con-002'].status }} | {{ results['feat-sec-con-002'].trend_display }} | {{ results['feat-sec-con-002'].evidence | default('—') }} |
| feat-sec-con-003 | Constraints trace to philosophy | warning (recommended) | 0.5 | {{ results['feat-sec-con-003'].previous_status | default('—') }} | {{ results['feat-sec-con-003'].status }} | {{ results['feat-sec-con-003'].trend_display }} | {{ results['feat-sec-con-003'].evidence | default('—') }} |

## 8. Dependencies — weight 2.0 — optional

**Why this matters:** Dependencies enumerate external systems, services, or teams the feature relies on. Without them, integration surprises and resilience planning are impossible.

**Section Score: {{ sections.dependencies.score }} / 100** ({{ sections.dependencies.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-dep-001 | Dependencies section exists | warning (recommended) | 0.5 | {{ results['feat-sec-dep-001'].previous_status | default('—') }} | {{ results['feat-sec-dep-001'].status }} | {{ results['feat-sec-dep-001'].trend_display }} | {{ results['feat-sec-dep-001'].evidence | default('—') }} |
| feat-sec-dep-002 | Dependencies are enumerated | warning (recommended) | 0.5 | {{ results['feat-sec-dep-002'].previous_status | default('—') }} | {{ results['feat-sec-dep-002'].status }} | {{ results['feat-sec-dep-002'].trend_display }} | {{ results['feat-sec-dep-002'].evidence | default('—') }} |
| feat-sec-dep-003 | Dependencies are not circular | error (mandatory) | 1.0 | {{ results['feat-sec-dep-003'].previous_status | default('—') }} | {{ results['feat-sec-dep-003'].status }} | {{ results['feat-sec-dep-003'].trend_display }} | {{ results['feat-sec-dep-003'].evidence | default('—') }} |

## 9. Non-Goals — weight 2.0 — optional

**Why this matters:** Non-Goals explicitly state what the feature will NOT address. Without them, scope creep has no explicit boundary.

**Section Score: {{ sections.non_goals.score }} / 100** ({{ sections.non_goals.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-ng-001 | Non-Goals section exists | warning (recommended) | 0.5 | {{ results['feat-sec-ng-001'].previous_status | default('—') }} | {{ results['feat-sec-ng-001'].status }} | {{ results['feat-sec-ng-001'].trend_display }} | {{ results['feat-sec-ng-001'].evidence | default('—') }} |
| feat-sec-ng-002 | Non-Goals are explicitly stated | warning (recommended) | 0.5 | {{ results['feat-sec-ng-002'].previous_status | default('—') }} | {{ results['feat-sec-ng-002'].status }} | {{ results['feat-sec-ng-002'].trend_display }} | {{ results['feat-sec-ng-002'].evidence | default('—') }} |
| feat-sec-ng-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['feat-sec-ng-003'].previous_status | default('—') }} | {{ results['feat-sec-ng-003'].status }} | {{ results['feat-sec-ng-003'].trend_display }} | {{ results['feat-sec-ng-003'].evidence | default('—') }} |

## 10. Future Extensions — weight 2.0 — optional

**Why this matters:** Future Extensions document planned or possible enhancements beyond current scope. Without them, architectural foresight is lost and scope creep is harder to prevent.

**Section Score: {{ sections.future_extensions.score }} / 100** ({{ sections.future_extensions.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-fe-001 | Future Extensions section exists | warning (recommended) | 0.5 | {{ results['feat-sec-fe-001'].previous_status | default('—') }} | {{ results['feat-sec-fe-001'].status }} | {{ results['feat-sec-fe-001'].trend_display }} | {{ results['feat-sec-fe-001'].evidence | default('—') }} |
| feat-sec-fe-002 | Extensions are enumerated | warning (recommended) | 0.5 | {{ results['feat-sec-fe-002'].previous_status | default('—') }} | {{ results['feat-sec-fe-002'].status }} | {{ results['feat-sec-fe-002'].trend_display }} | {{ results['feat-sec-fe-002'].evidence | default('—') }} |
| feat-sec-fe-003 | Extensions do not contradict current scope | error (mandatory) | 1.0 | {{ results['feat-sec-fe-003'].previous_status | default('—') }} | {{ results['feat-sec-fe-003'].status }} | {{ results['feat-sec-fe-003'].trend_display }} | {{ results['feat-sec-fe-003'].evidence | default('—') }} |

## 11. Traceability — weight 1.5 — optional

**Why this matters:** Traceability maps requirements back to Vision and forward to Design, Technical, and Implementation. Without it, impact analysis is impossible.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-sec-trace-001 | Traceability section exists | warning (recommended) | 0.5 | {{ results['feat-sec-trace-001'].previous_status | default('—') }} | {{ results['feat-sec-trace-001'].status }} | {{ results['feat-sec-trace-001'].trend_display }} | {{ results['feat-sec-trace-001'].evidence | default('—') }} |
| feat-sec-trace-002 | Links to upstream (Vision) | warning (recommended) | 0.5 | {{ results['feat-sec-trace-002'].previous_status | default('—') }} | {{ results['feat-sec-trace-002'].status }} | {{ results['feat-sec-trace-002'].trend_display }} | {{ results['feat-sec-trace-002'].evidence | default('—') }} |
| feat-sec-trace-003 | Links to downstream (Feature Design, Feature Technical) | warning (recommended) | 0.5 | {{ results['feat-sec-trace-003'].previous_status | default('—') }} | {{ results['feat-sec-trace-003'].status }} | {{ results['feat-sec-trace-003'].trend_display }} | {{ results['feat-sec-trace-003'].evidence | default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 11 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | feature |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/04-feature/*.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
