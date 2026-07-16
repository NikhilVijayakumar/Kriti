# Deterministic Section Report â€” Vision

**Document:** {{ document_path }}
**Standard:** `documentation-standards/01-vision-standards.md`
**Rule Files:** `audit/deterministic/section/01-vision/*.yaml`
**Auditor:** System (deterministic engine)
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ 'â†‘ Improved' if score > previous_score else 'â†“ Regressed' if score < previous_score else 'â†’ Unchanged' }} vs. previous run){% else %}(baseline â€” first audit of this document){% endif %}

```
overall = average of the 10 section scores below
section_score = 100 Ã— (Î£ weight of passed rules in that section) / (Î£ weight of all rules in that section)
# calculation: deterministic_section_v1
```

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs â€” this revision is the baseline every future run is compared against.{% endif %}

### Section Scores

| # | Section | Required | Weight | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---:|---|
| 1 | Purpose | **required** | 4.0 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('â€”') }} | {{ sections.purpose.trend_display }} |
| 2 | Vision Statement | **required** | 4.8 | {{ sections.vision_statement.score }} / 100 | {{ sections.vision_statement.previous_score | default('â€”') }} | {{ sections.vision_statement.trend_display }} |
| 3 | Problem | **required** | 6.0 | {{ sections.problem.score }} / 100 | {{ sections.problem.previous_score | default('â€”') }} | {{ sections.problem.trend_display }} |
| 4 | Solution | **required** | 5.5 | {{ sections.solution.score }} / 100 | {{ sections.solution.previous_score | default('â€”') }} | {{ sections.solution.trend_display }} |
| 5 | Target Audience | **required** | 4.0 | {{ sections.target_audience.score }} / 100 | {{ sections.target_audience.previous_score | default('â€”') }} | {{ sections.target_audience.trend_display }} |
| 6 | Pillars | optional | 1.1 | {{ sections.pillars.score }} / 100 | {{ sections.pillars.previous_score | default('â€”') }} | {{ sections.pillars.trend_display }} |
| 7 | Philosophy | optional | 0.8 | {{ sections.philosophy.score }} / 100 | {{ sections.philosophy.previous_score | default('â€”') }} | {{ sections.philosophy.trend_display }} |
| 8 | Guiding Principles | optional | 0.8 | {{ sections.guiding_principles.score }} / 100 | {{ sections.guiding_principles.previous_score | default('â€”') }} | {{ sections.guiding_principles.trend_display }} |
| 9 | Success Criteria | optional | 1.3 | {{ sections.success_criteria.score }} / 100 | {{ sections.success_criteria.previous_score | default('â€”') }} | {{ sections.success_criteria.trend_display }} |
| 10 | Traceability | optional | 1.3 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('â€”') }} | {{ sections.traceability.trend_display }} |

The 5 required sections carry 24.3 of the document's 29.6 total rule weight â€” a document can only pass if those five are both present and internally sound; the remaining five are recommended-quality signal, not gating.

---

## 1. Purpose â€” weight 4.0 â€” **required**

**Why this matters:** Purpose is what tells a reader why Vision Documentation exists at all before they read a single direction statement. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-purpose-001 | Purpose section exists | error (mandatory) | 1.5 | {{ results['vis-sec-purpose-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-purpose-001'].status }} | {{ results['vis-sec-purpose-001'].trend_display }} | {{ results['vis-sec-purpose-001'].evidence \| default('â€”') }} |
| vis-sec-purpose-002 | States vision intent | error (mandatory) | 1.0 | {{ results['vis-sec-purpose-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-purpose-002'].status }} | {{ results['vis-sec-purpose-002'].trend_display }} | {{ results['vis-sec-purpose-002'].evidence \| default('â€”') }} |
| vis-sec-purpose-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['vis-sec-purpose-003'].previous_status \| default('â€”') }} | {{ results['vis-sec-purpose-003'].status }} | {{ results['vis-sec-purpose-003'].trend_display }} | {{ results['vis-sec-purpose-003'].evidence \| default('â€”') }} |
| vis-sec-purpose-004 | Scope boundaries defined | warning (recommended) | 0.5 | {{ results['vis-sec-purpose-004'].previous_status \| default('â€”') }} | {{ results['vis-sec-purpose-004'].status }} | {{ results['vis-sec-purpose-004'].trend_display }} | {{ results['vis-sec-purpose-004'].evidence \| default('â€”') }} |

## 2. Vision Statement â€” weight 4.8 â€” **required**

**Why this matters:** Vision Statement is the core aspirational statement â€” where the product is going. A vague or technology-leaking vision statement gives Philosophy and Feature nothing concrete to derive against.

**Section Score: {{ sections.vision_statement.score }} / 100** ({{ sections.vision_statement.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-vs-001 | Vision Statement section exists | error (mandatory) | 1.5 | {{ results['vis-sec-vs-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-vs-001'].status }} | {{ results['vis-sec-vs-001'].trend_display }} | {{ results['vis-sec-vs-001'].evidence \| default('â€”') }} |
| vis-sec-vs-002 | Describes long-term direction | error (mandatory) | 1.0 | {{ results['vis-sec-vs-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-vs-002'].status }} | {{ results['vis-sec-vs-002'].trend_display }} | {{ results['vis-sec-vs-002'].evidence \| default('â€”') }} |
| vis-sec-vs-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['vis-sec-vs-003'].previous_status \| default('â€”') }} | {{ results['vis-sec-vs-003'].status }} | {{ results['vis-sec-vs-003'].trend_display }} | {{ results['vis-sec-vs-003'].evidence \| default('â€”') }} |
| vis-sec-vs-004 | Concise (â‰¤ 500 words) | warning (recommended) | 0.3 | {{ results['vis-sec-vs-004'].previous_status \| default('â€”') }} | {{ results['vis-sec-vs-004'].status }} | {{ results['vis-sec-vs-004'].trend_display }} | {{ results['vis-sec-vs-004'].evidence \| default('â€”') }} |

## 3. Problem â€” weight 6.0 â€” **required**

**Why this matters:** Problem is what motivates the entire vision. A section that mixes problem and solution gives Philosophy and Feature no clean handoff â€” they can't derive against a problem that's half-solved already.

**Section Score: {{ sections.problem.score }} / 100** ({{ sections.problem.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-problem-001 | Problem section exists | error (mandatory) | 1.5 | {{ results['vis-sec-problem-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-problem-001'].status }} | {{ results['vis-sec-problem-001'].trend_display }} | {{ results['vis-sec-problem-001'].evidence \| default('â€”') }} |
| vis-sec-problem-002 | States the problem clearly | error (mandatory) | 1.0 | {{ results['vis-sec-problem-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-problem-002'].status }} | {{ results['vis-sec-problem-002'].trend_display }} | {{ results['vis-sec-problem-002'].evidence \| default('â€”') }} |
| vis-sec-problem-003 | Does not describe solutions | error (mandatory) | 1.0 | {{ results['vis-sec-problem-003'].previous_status \| default('â€”') }} | {{ results['vis-sec-problem-003'].status }} | {{ results['vis-sec-problem-003'].trend_display }} | {{ results['vis-sec-problem-003'].evidence \| default('â€”') }} |
| vis-sec-problem-004 | Technology-independent | error (mandatory) | 1.0 | {{ results['vis-sec-problem-004'].previous_status \| default('â€”') }} | {{ results['vis-sec-problem-004'].status }} | {{ results['vis-sec-problem-004'].trend_display }} | {{ results['vis-sec-problem-004'].evidence \| default('â€”') }} |
| vis-sec-problem-005 | Has measurable impact | warning (recommended) | 0.5 | {{ results['vis-sec-problem-005'].previous_status \| default('â€”') }} | {{ results['vis-sec-problem-005'].status }} | {{ results['vis-sec-problem-005'].trend_display }} | {{ results['vis-sec-problem-005'].evidence \| default('â€”') }} |

## 4. Solution â€” weight 5.5 â€” **required**

**Why this matters:** Solution is the aspirational approach â€” what the product will do, not how. A section that leaks into implementation details crosses into Architecture's territory and makes the document stale the moment those details change.

**Section Score: {{ sections.solution.score }} / 100** ({{ sections.solution.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-solution-001 | Solution section exists | error (mandatory) | 1.5 | {{ results['vis-sec-solution-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-solution-001'].status }} | {{ results['vis-sec-solution-001'].trend_display }} | {{ results['vis-sec-solution-001'].evidence \| default('â€”') }} |
| vis-sec-solution-002 | Describes the proposed approach | error (mandatory) | 1.0 | {{ results['vis-sec-solution-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-solution-002'].status }} | {{ results['vis-sec-solution-002'].trend_display }} | {{ results['vis-sec-solution-002'].evidence \| default('â€”') }} |
| vis-sec-solution-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['vis-sec-solution-003'].previous_status \| default('â€”') }} | {{ results['vis-sec-solution-003'].status }} | {{ results['vis-sec-solution-003'].trend_display }} | {{ results['vis-sec-solution-003'].evidence \| default('â€”') }} |
| vis-sec-solution-004 | No implementation specifics (code, APIs, schemas, libraries) | error (mandatory) | 1.0 | {{ results['vis-sec-solution-004'].previous_status \| default('â€”') }} | {{ results['vis-sec-solution-004'].status }} | {{ results['vis-sec-solution-004'].trend_display }} | {{ results['vis-sec-solution-004'].evidence \| default('â€”') }} |
| vis-sec-solution-005 | Addresses the stated problem | warning (recommended) | 0.5 | {{ results['vis-sec-solution-005'].previous_status \| default('â€”') }} | {{ results['vis-sec-solution-005'].status }} | {{ results['vis-sec-solution-005'].trend_display }} | {{ results['vis-sec-solution-005'].evidence \| default('â€”') }} |

## 5. Target Audience â€” weight 4.0 â€” **required**

**Why this matters:** Target Audience tells Philosophy who the product serves â€” the user model that drives guiding principles. A missing or vague audience section gives Philosophy nothing to reason about.

**Section Score: {{ sections.target_audience.score }} / 100** ({{ sections.target_audience.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-ta-001 | Target Audience section exists | error (mandatory) | 1.5 | {{ results['vis-sec-ta-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-ta-001'].status }} | {{ results['vis-sec-ta-001'].trend_display }} | {{ results['vis-sec-ta-001'].evidence \| default('â€”') }} |
| vis-sec-ta-002 | Identifies who the product serves | error (mandatory) | 1.0 | {{ results['vis-sec-ta-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-ta-002'].status }} | {{ results['vis-sec-ta-002'].trend_display }} | {{ results['vis-sec-ta-002'].evidence \| default('â€”') }} |
| vis-sec-ta-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['vis-sec-ta-003'].previous_status \| default('â€”') }} | {{ results['vis-sec-ta-003'].status }} | {{ results['vis-sec-ta-003'].trend_display }} | {{ results['vis-sec-ta-003'].evidence \| default('â€”') }} |
| vis-sec-ta-004 | At least two audience segments | warning (recommended) | 0.5 | {{ results['vis-sec-ta-004'].previous_status \| default('â€”') }} | {{ results['vis-sec-ta-004'].status }} | {{ results['vis-sec-ta-004'].trend_display }} | {{ results['vis-sec-ta-004'].evidence \| default('â€”') }} |

## 6. Pillars â€” weight 1.1 â€” optional

**Why this matters:** Pillars distill the vision into core values that guide every downstream decision. A document without them gives Philosophy no explicit anchor for its guiding principles.

**Section Score: {{ sections.pillars.score }} / 100** ({{ sections.pillars.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-pillars-001 | Pillars section exists | suggestion | 0.3 | {{ results['vis-sec-pillars-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-pillars-001'].status }} | {{ results['vis-sec-pillars-001'].trend_display }} | {{ results['vis-sec-pillars-001'].evidence \| default('â€”') }} |
| vis-sec-pillars-002 | Technology-independent | warning (recommended) | 0.5 | {{ results['vis-sec-pillars-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-pillars-002'].status }} | {{ results['vis-sec-pillars-002'].trend_display }} | {{ results['vis-sec-pillars-002'].evidence \| default('â€”') }} |
| vis-sec-pillars-003 | Lists at least three pillars | suggestion | 0.3 | {{ results['vis-sec-pillars-003'].previous_status \| default('â€”') }} | {{ results['vis-sec-pillars-003'].status }} | {{ results['vis-sec-pillars-003'].trend_display }} | {{ results['vis-sec-pillars-003'].evidence \| default('â€”') }} |

## 7. Philosophy â€” weight 0.8 â€” optional

**Why this matters:** Philosophy in Vision is a preview of what the dedicated Philosophy document will expand. Its absence means the vision has no explicit values layer.

**Section Score: {{ sections.philosophy.score }} / 100** ({{ sections.philosophy.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-philosophy-001 | Philosophy section exists | suggestion | 0.3 | {{ results['vis-sec-philosophy-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-philosophy-001'].status }} | {{ results['vis-sec-philosophy-001'].trend_display }} | {{ results['vis-sec-philosophy-001'].evidence \| default('â€”') }} |
| vis-sec-philosophy-002 | Has substantive content (â‰¥ 1 paragraph) | warning (recommended) | 0.5 | {{ results['vis-sec-philosophy-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-philosophy-002'].status }} | {{ results['vis-sec-philosophy-002'].trend_display }} | {{ results['vis-sec-philosophy-002'].evidence \| default('â€”') }} |

## 8. Guiding Principles â€” weight 0.8 â€” optional

**Why this matters:** Guiding Principles in Vision are the seeds that Philosophy's Guiding Principles section expands. Without them, Philosophy has no explicit upstream to trace back to.

**Section Score: {{ sections.guiding_principles.score }} / 100** ({{ sections.guiding_principles.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-gp-001 | Guiding Principles section exists | suggestion | 0.3 | {{ results['vis-sec-gp-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-gp-001'].status }} | {{ results['vis-sec-gp-001'].trend_display }} | {{ results['vis-sec-gp-001'].evidence \| default('â€”') }} |
| vis-sec-gp-002 | Has substantive content (â‰¥ 1 paragraph) | warning (recommended) | 0.5 | {{ results['vis-sec-gp-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-gp-002'].status }} | {{ results['vis-sec-gp-002'].trend_display }} | {{ results['vis-sec-gp-002'].evidence \| default('â€”') }} |

## 9. Success Criteria â€” weight 1.3 â€” optional

**Why this matters:** Success Criteria in Vision are the seeds that Feature's Acceptance Criteria section expands. Without them, Feature has no explicit upstream success definition to trace.

**Section Score: {{ sections.success_criteria.score }} / 100** ({{ sections.success_criteria.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-sc-001 | Success Criteria section exists | suggestion | 0.3 | {{ results['vis-sec-sc-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-sc-001'].status }} | {{ results['vis-sec-sc-001'].trend_display }} | {{ results['vis-sec-sc-001'].evidence \| default('â€”') }} |
| vis-sec-sc-002 | Technology-independent | warning (recommended) | 0.5 | {{ results['vis-sec-sc-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-sc-002'].status }} | {{ results['vis-sec-sc-002'].trend_display }} | {{ results['vis-sec-sc-002'].evidence \| default('â€”') }} |
| vis-sec-sc-003 | Measurable (quantifiable or verifiable) | warning (recommended) | 0.5 | {{ results['vis-sec-sc-003'].previous_status \| default('â€”') }} | {{ results['vis-sec-sc-003'].status }} | {{ results['vis-sec-sc-003'].trend_display }} | {{ results['vis-sec-sc-003'].evidence \| default('â€”') }} |

## 10. Traceability â€” weight 1.3 â€” optional

**Why this matters:** Traceability is what makes the derivation chain enforceable â€” without it, nothing stops a downstream domain from silently drifting away from what Vision actually says.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-sec-trace-001 | Traceability section exists | suggestion | 0.3 | {{ results['vis-sec-trace-001'].previous_status \| default('â€”') }} | {{ results['vis-sec-trace-001'].status }} | {{ results['vis-sec-trace-001'].trend_display }} | {{ results['vis-sec-trace-001'].evidence \| default('â€”') }} |
| vis-sec-trace-002 | Links to upstream origins | warning (recommended) | 0.5 | {{ results['vis-sec-trace-002'].previous_status \| default('â€”') }} | {{ results['vis-sec-trace-002'].status }} | {{ results['vis-sec-trace-002'].trend_display }} | {{ results['vis-sec-trace-002'].evidence \| default('â€”') }} |
| vis-sec-trace-003 | Links to downstream consumers | warning (recommended) | 0.5 | {{ results['vis-sec-trace-003'].previous_status \| default('â€”') }} | {{ results['vis-sec-trace-003'].status }} | {{ results['vis-sec-trace-003'].trend_display }} | {{ results['vis-sec-trace-003'].evidence \| default('â€”') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('â€”') }} | {{ 'Yes â€” regression' if r.is_new_failure else 'No â€” carried over' }} |
{% endfor %}
{% else %}
No failures across all 10 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | vision |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/01-vision/*.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
