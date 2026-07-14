# Deterministic Section Report — QA

**Document:** {{ document_path }}
**Standard:** `documentation-standards/12-qa-standards.md`
**Rule Files:** `audit/deterministic/section/12-qa/*.yaml`
**Auditor:** System (deterministic engine)
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 9 section scores below
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
| 1 | Test Strategy | **required** | 3.5 | {{ sections.test_strategy.score }} / 100 | {{ sections.test_strategy.previous_score | default('—') }} | {{ sections.test_strategy.trend_display }} |
| 2 | Unit Testing | **required** | 3.5 | {{ sections.unit_testing.score }} / 100 | {{ sections.unit_testing.previous_score | default('—') }} | {{ sections.unit_testing.trend_display }} |
| 3 | Integration Testing | **required** | 3.5 | {{ sections.integration_testing.score }} / 100 | {{ sections.integration_testing.previous_score | default('—') }} | {{ sections.integration_testing.trend_display }} |
| 4 | Security Testing | **required** | 3.5 | {{ sections.security_testing.score }} / 100 | {{ sections.security_testing.previous_score | default('—') }} | {{ sections.security_testing.trend_display }} |
| 5 | Purpose | optional | 1.5 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 6 | E2E Testing | **required** | 3.0 | {{ sections.e2e_testing.score }} / 100 | {{ sections.e2e_testing.previous_score | default('—') }} | {{ sections.e2e_testing.trend_display }} |
| 7 | Smoke Testing | **required** | 3.0 | {{ sections.smoke_testing.score }} / 100 | {{ sections.smoke_testing.previous_score | default('—') }} | {{ sections.smoke_testing.trend_display }} |
| 8 | Load Testing | **required** | 3.0 | {{ sections.load_testing.score }} / 100 | {{ sections.load_testing.previous_score | default('—') }} | {{ sections.load_testing.trend_display }} |
| 9 | Scalability Testing | **required** | 3.0 | {{ sections.scalability_testing.score }} / 100 | {{ sections.scalability_testing.previous_score | default('—') }} | {{ sections.scalability_testing.trend_display }} |

The 8 required sections carry 26.0 of the document's 27.5 total rule weight — a document can only pass if those eight are both present and internally sound; Purpose is recommended-quality signal, not gating.

---

## 1. Test Strategy — weight 3.5 — **required**

**Why this matters:** Test Strategy defines the overall testing philosophy and approach that every other test type section derives from. A missing or vague strategy gives the individual test sections no coherence — they become a list of activities without a unifying rationale.

**Section Score: {{ sections.test_strategy.score }} / 100** ({{ sections.test_strategy.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-strategy-001 | Test Strategy section exists | error (mandatory) | 1.5 | {{ results['qa-sec-strategy-001'].previous_status \| default('—') }} | {{ results['qa-sec-strategy-001'].status }} | {{ results['qa-sec-strategy-001'].trend_display }} | {{ results['qa-sec-strategy-001'].evidence \| default('—') }} |
| qa-sec-strategy-002 | Defines overall testing approach and philosophy | error (mandatory) | 1.0 | {{ results['qa-sec-strategy-002'].previous_status \| default('—') }} | {{ results['qa-sec-strategy-002'].status }} | {{ results['qa-sec-strategy-002'].trend_display }} | {{ results['qa-sec-strategy-002'].evidence \| default('—') }} |
| qa-sec-strategy-003 | Defines coverage goals or metrics | warning (recommended) | 0.5 | {{ results['qa-sec-strategy-003'].previous_status \| default('—') }} | {{ results['qa-sec-strategy-003'].status }} | {{ results['qa-sec-strategy-003'].trend_display }} | {{ results['qa-sec-strategy-003'].evidence \| default('—') }} |
| qa-sec-strategy-004 | References Architecture Documentation for test scope | warning (recommended) | 0.5 | {{ results['qa-sec-strategy-004'].previous_status \| default('—') }} | {{ results['qa-sec-strategy-004'].status }} | {{ results['qa-sec-strategy-004'].trend_display }} | {{ results['qa-sec-strategy-004'].evidence \| default('—') }} |

## 2. Unit Testing — weight 3.5 — **required**

**Why this matters:** Unit Testing is the foundation of the test pyramid. A section that's missing or generic gives developers no guidance on how to structure their tests or what coverage is expected.

**Section Score: {{ sections.unit_testing.score }} / 100** ({{ sections.unit_testing.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-unit-001 | Unit Testing section exists | error (mandatory) | 1.5 | {{ results['qa-sec-unit-001'].previous_status \| default('—') }} | {{ results['qa-sec-unit-001'].status }} | {{ results['qa-sec-unit-001'].trend_display }} | {{ results['qa-sec-unit-001'].evidence \| default('—') }} |
| qa-sec-unit-002 | Defines what components or modules are covered | error (mandatory) | 1.0 | {{ results['qa-sec-unit-002'].previous_status \| default('—') }} | {{ results['qa-sec-unit-002'].status }} | {{ results['qa-sec-unit-002'].trend_display }} | {{ results['qa-sec-unit-002'].evidence \| default('—') }} |
| qa-sec-unit-003 | Defines naming conventions or test structure | warning (recommended) | 0.5 | {{ results['qa-sec-unit-003'].previous_status \| default('—') }} | {{ results['qa-sec-unit-003'].status }} | {{ results['qa-sec-unit-003'].trend_display }} | {{ results['qa-sec-unit-003'].evidence \| default('—') }} |
| qa-sec-unit-004 | References Engineering Documentation testing standards | warning (recommended) | 0.5 | {{ results['qa-sec-unit-004'].previous_status \| default('—') }} | {{ results['qa-sec-unit-004'].status }} | {{ results['qa-sec-unit-004'].trend_display }} | {{ results['qa-sec-unit-004'].evidence \| default('—') }} |

## 3. Integration Testing — weight 3.5 — **required**

**Why this matters:** Integration Testing verifies that component boundaries work as designed. Without it, individual units may pass in isolation while the system fails at every seam.

**Section Score: {{ sections.integration_testing.score }} / 100** ({{ sections.integration_testing.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-integration-001 | Integration Testing section exists | error (mandatory) | 1.5 | {{ results['qa-sec-integration-001'].previous_status \| default('—') }} | {{ results['qa-sec-integration-001'].status }} | {{ results['qa-sec-integration-001'].trend_display }} | {{ results['qa-sec-integration-001'].evidence \| default('—') }} |
| qa-sec-integration-002 | Defines which component interfaces are tested | error (mandatory) | 1.0 | {{ results['qa-sec-integration-002'].previous_status \| default('—') }} | {{ results['qa-sec-integration-002'].status }} | {{ results['qa-sec-integration-002'].trend_display }} | {{ results['qa-sec-integration-002'].evidence \| default('—') }} |
| qa-sec-integration-003 | Contains at least one integration test scenario | warning (recommended) | 0.5 | {{ results['qa-sec-integration-003'].previous_status \| default('—') }} | {{ results['qa-sec-integration-003'].status }} | {{ results['qa-sec-integration-003'].trend_display }} | {{ results['qa-sec-integration-003'].evidence \| default('—') }} |
| qa-sec-integration-004 | References Architecture Documentation for communication paths | warning (recommended) | 0.5 | {{ results['qa-sec-integration-004'].previous_status \| default('—') }} | {{ results['qa-sec-integration-004'].status }} | {{ results['qa-sec-integration-004'].trend_display }} | {{ results['qa-sec-integration-004'].evidence \| default('—') }} |

## 4. Security Testing — weight 3.5 — **required**

**Why this matters:** Security Testing ensures threats are validated against, not just documented. A missing or shallow section means the Security domain's threat model goes untested.

**Section Score: {{ sections.security_testing.score }} / 100** ({{ sections.security_testing.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-security-001 | Security Testing section exists | error (mandatory) | 1.5 | {{ results['qa-sec-security-001'].previous_status \| default('—') }} | {{ results['qa-sec-security-001'].status }} | {{ results['qa-sec-security-001'].trend_display }} | {{ results['qa-sec-security-001'].evidence \| default('—') }} |
| qa-sec-security-002 | Defines which threats or attack vectors are tested | error (mandatory) | 1.0 | {{ results['qa-sec-security-002'].previous_status \| default('—') }} | {{ results['qa-sec-security-002'].status }} | {{ results['qa-sec-security-002'].trend_display }} | {{ results['qa-sec-security-002'].evidence \| default('—') }} |
| qa-sec-security-003 | Defines test methods (SAST, DAST, penetration, etc.) | warning (recommended) | 0.5 | {{ results['qa-sec-security-003'].previous_status \| default('—') }} | {{ results['qa-sec-security-003'].status }} | {{ results['qa-sec-security-003'].trend_display }} | {{ results['qa-sec-security-003'].evidence \| default('—') }} |
| qa-sec-security-004 | References Security Documentation threat model | warning (recommended) | 0.5 | {{ results['qa-sec-security-004'].previous_status \| default('—') }} | {{ results['qa-sec-security-004'].status }} | {{ results['qa-sec-security-004'].trend_display }} | {{ results['qa-sec-security-004'].evidence \| default('—') }} |

## 5. Purpose — weight 1.5 — optional

**Why this matters:** Purpose defines why QA Documentation exists before a reader examines a single test type. A missing Purpose section means readers must infer the document's intent from its content.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-purpose-001 | Purpose section exists | warning (recommended) | 0.5 | {{ results['qa-sec-purpose-001'].previous_status \| default('—') }} | {{ results['qa-sec-purpose-001'].status }} | {{ results['qa-sec-purpose-001'].trend_display }} | {{ results['qa-sec-purpose-001'].evidence \| default('—') }} |
| qa-sec-purpose-002 | States QA intent | warning (recommended) | 0.5 | {{ results['qa-sec-purpose-002'].previous_status \| default('—') }} | {{ results['qa-sec-purpose-002'].status }} | {{ results['qa-sec-purpose-002'].trend_display }} | {{ results['qa-sec-purpose-002'].evidence \| default('—') }} |
| qa-sec-purpose-003 | Defines scope boundaries | warning (recommended) | 0.5 | {{ results['qa-sec-purpose-003'].previous_status \| default('—') }} | {{ results['qa-sec-purpose-003'].status }} | {{ results['qa-sec-purpose-003'].trend_display }} | {{ results['qa-sec-purpose-003'].evidence \| default('—') }} |

## 6. E2E Testing — weight 3.0 — **required**

**Why this matters:** E2E Testing verifies critical user journeys through the full system. Without it, integration seams that unit and integration tests can't see go unvalidated.

**Section Score: {{ sections.e2e_testing.score }} / 100** ({{ sections.e2e_testing.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-e2e_testing-001 | E2E Testing section exists | error (mandatory) | 1.5 | {{ results['qa-sec-e2e_testing-001'].previous_status \| default('—') }} | {{ results['qa-sec-e2e_testing-001'].status }} | {{ results['qa-sec-e2e_testing-001'].trend_display }} | {{ results['qa-sec-e2e_testing-001'].evidence \| default('—') }} |
| qa-sec-e2e_testing-002 | Has substantive content (not empty or placeholder) | error (mandatory) | 1.0 | {{ results['qa-sec-e2e_testing-002'].previous_status \| default('—') }} | {{ results['qa-sec-e2e_testing-002'].status }} | {{ results['qa-sec-e2e_testing-002'].trend_display }} | {{ results['qa-sec-e2e_testing-002'].evidence \| default('—') }} |
| qa-sec-e2e_testing-003 | Content is project-specific, not generic boilerplate | warning (recommended) | 0.5 | {{ results['qa-sec-e2e_testing-003'].previous_status \| default('—') }} | {{ results['qa-sec-e2e_testing-003'].status }} | {{ results['qa-sec-e2e_testing-003'].trend_display }} | {{ results['qa-sec-e2e_testing-003'].evidence \| default('—') }} |

## 7. Smoke Testing — weight 3.0 — **required**

**Why this matters:** Smoke Testing is the fast post-deploy check that catches catastrophic failures. Without it, broken deploys can reach production traffic before any automated check runs.

**Section Score: {{ sections.smoke_testing.score }} / 100** ({{ sections.smoke_testing.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-smoke_testing-001 | Smoke Testing section exists | error (mandatory) | 1.5 | {{ results['qa-sec-smoke_testing-001'].previous_status \| default('—') }} | {{ results['qa-sec-smoke_testing-001'].status }} | {{ results['qa-sec-smoke_testing-001'].trend_display }} | {{ results['qa-sec-smoke_testing-001'].evidence \| default('—') }} |
| qa-sec-smoke_testing-002 | Has substantive content (not empty or placeholder) | error (mandatory) | 1.0 | {{ results['qa-sec-smoke_testing-002'].previous_status \| default('—') }} | {{ results['qa-sec-smoke_testing-002'].status }} | {{ results['qa-sec-smoke_testing-002'].trend_display }} | {{ results['qa-sec-smoke_testing-002'].evidence \| default('—') }} |
| qa-sec-smoke_testing-003 | Content is project-specific, not generic boilerplate | warning (recommended) | 0.5 | {{ results['qa-sec-smoke_testing-003'].previous_status \| default('—') }} | {{ results['qa-sec-smoke_testing-003'].status }} | {{ results['qa-sec-smoke_testing-003'].trend_display }} | {{ results['qa-sec-smoke_testing-003'].evidence \| default('—') }} |

## 8. Load Testing — weight 3.0 — **required**

**Why this matters:** Load Testing validates performance targets against defined traffic profiles. Without it, performance is assumed from production experience rather than tested against known thresholds.

**Section Score: {{ sections.load_testing.score }} / 100** ({{ sections.load_testing.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-load_testing-001 | Load Testing section exists | error (mandatory) | 1.5 | {{ results['qa-sec-load_testing-001'].previous_status \| default('—') }} | {{ results['qa-sec-load_testing-001'].status }} | {{ results['qa-sec-load_testing-001'].trend_display }} | {{ results['qa-sec-load_testing-001'].evidence \| default('—') }} |
| qa-sec-load_testing-002 | Has substantive content (not empty or placeholder) | error (mandatory) | 1.0 | {{ results['qa-sec-load_testing-002'].previous_status \| default('—') }} | {{ results['qa-sec-load_testing-002'].status }} | {{ results['qa-sec-load_testing-002'].trend_display }} | {{ results['qa-sec-load_testing-002'].evidence \| default('—') }} |
| qa-sec-load_testing-003 | Content is project-specific, not generic boilerplate | warning (recommended) | 0.5 | {{ results['qa-sec-load_testing-003'].previous_status \| default('—') }} | {{ results['qa-sec-load_testing-003'].status }} | {{ results['qa-sec-load_testing-003'].trend_display }} | {{ results['qa-sec-load_testing-003'].evidence \| default('—') }} |

## 9. Scalability Testing — weight 3.0 — **required**

**Why this matters:** Scalability Testing characterizes how the system behaves as load grows beyond current levels — where it breaks and how it degrades. Without it, capacity planning is based on hope rather than data.

**Section Score: {{ sections.scalability_testing.score }} / 100** ({{ sections.scalability_testing.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-sec-scalability_testing-001 | Scalability Testing section exists | error (mandatory) | 1.5 | {{ results['qa-sec-scalability_testing-001'].previous_status \| default('—') }} | {{ results['qa-sec-scalability_testing-001'].status }} | {{ results['qa-sec-scalability_testing-001'].trend_display }} | {{ results['qa-sec-scalability_testing-001'].evidence \| default('—') }} |
| qa-sec-scalability_testing-002 | Has substantive content (not empty or placeholder) | error (mandatory) | 1.0 | {{ results['qa-sec-scalability_testing-002'].previous_status \| default('—') }} | {{ results['qa-sec-scalability_testing-002'].status }} | {{ results['qa-sec-scalability_testing-002'].trend_display }} | {{ results['qa-sec-scalability_testing-002'].evidence \| default('—') }} |
| qa-sec-scalability_testing-003 | Content is project-specific, not generic boilerplate | warning (recommended) | 0.5 | {{ results['qa-sec-scalability_testing-003'].previous_status \| default('—') }} | {{ results['qa-sec-scalability_testing-003'].status }} | {{ results['qa-sec-scalability_testing-003'].trend_display }} | {{ results['qa-sec-scalability_testing-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 9 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | qa |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/12-qa/*.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
