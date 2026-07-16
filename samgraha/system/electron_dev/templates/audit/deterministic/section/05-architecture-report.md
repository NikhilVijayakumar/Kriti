# Deterministic Section Report — Architecture

**Document:** {{ document_path }}
**Standard:** `documentation-standards/05-architecture-standards.md`
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
| 1 | Purpose | optional | 4.0 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 2 | System Overview | **required** | 5.0 | {{ sections.system_overview.score }} / 100 | {{ sections.system_overview.previous_score | default('—') }} | {{ sections.system_overview.trend_display }} |
| 3 | Component Model | **required** | 7.0 | {{ sections.component_model.score }} / 100 | {{ sections.component_model.previous_score | default('—') }} | {{ sections.component_model.trend_display }} |
| 4 | Communication Paths | **required** | 6.0 | {{ sections.communication_paths.score }} / 100 | {{ sections.communication_paths.previous_score | default('—') }} | {{ sections.communication_paths.trend_display }} |
| 5 | Data Flow | **required** | 5.0 | {{ sections.data_flow.score }} / 100 | {{ sections.data_flow.previous_score | default('—') }} | {{ sections.data_flow.trend_display }} |
| 6 | Security Considerations | **required** | 6.0 | {{ sections.security_considerations.score }} / 100 | {{ sections.security_considerations.previous_score | default('—') }} | {{ sections.security_considerations.trend_display }} |
| 7 | Rationale | optional | 1.8 | {{ sections.rationale.score }} / 100 | {{ sections.rationale.previous_score | default('—') }} | {{ sections.rationale.trend_display }} |
| 8 | Constraints | optional | 3.0 | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 9 | Traceability | optional | 1.8 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |
| 10 | Operational Readiness | not in standard | 0.6 | {{ sections.operational_readiness.score }} / 100 | {{ sections.operational_readiness.previous_score | default('—') }} | {{ sections.operational_readiness.trend_display }} |
| 11 | Observability | not in standard | 0.6 | {{ sections.observability.score }} / 100 | {{ sections.observability.previous_score | default('—') }} | {{ sections.observability.trend_display }} |

The 5 required sections carry 29.0 of the document's 46.8 total rule weight — a document can only pass if those five are both present and internally sound; the remaining six are recommended-quality signal, not gating.

---

## 1. Purpose — `section/05-architecture/01-purpose.yaml` — weight 4.0

**Why this matters:** Purpose is what tells a reader why Architecture Documentation exists at all before they read a single component. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-purpose-001 | Purpose section exists | error (mandatory) | 1.5 | {{ results['arch-sec-purpose-001'].previous_status \| default('—') }} | {{ results['arch-sec-purpose-001'].status }} | {{ results['arch-sec-purpose-001'].trend_display }} | {{ results['arch-sec-purpose-001'].evidence \| default('—') }} |
| arch-sec-purpose-002 | States architectural intent | error (mandatory) | 1.0 | {{ results['arch-sec-purpose-002'].previous_status \| default('—') }} | {{ results['arch-sec-purpose-002'].status }} | {{ results['arch-sec-purpose-002'].trend_display }} | {{ results['arch-sec-purpose-002'].evidence \| default('—') }} |
| arch-sec-purpose-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['arch-sec-purpose-003'].previous_status \| default('—') }} | {{ results['arch-sec-purpose-003'].status }} | {{ results['arch-sec-purpose-003'].trend_display }} | {{ results['arch-sec-purpose-003'].evidence \| default('—') }} |
| arch-sec-purpose-004 | Scope boundaries defined | warning (recommended) | 0.5 | {{ results['arch-sec-purpose-004'].previous_status \| default('—') }} | {{ results['arch-sec-purpose-004'].status }} | {{ results['arch-sec-purpose-004'].trend_display }} | {{ results['arch-sec-purpose-004'].evidence \| default('—') }} |

## 2. System Overview — `02-system_overview.yaml` — weight 5.0 — **required**

**Why this matters:** This is the entry point for anyone new to the system — its purpose, capabilities, and structural approach in one place. Without it, every downstream section (Component Model, Data Flow) has no shared context to build on.

**Section Score: {{ sections.system_overview.score }} / 100** ({{ sections.system_overview.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-so-001 | Section exists | error (mandatory) | 1.5 | {{ results['arch-sec-so-001'].previous_status \| default('—') }} | {{ results['arch-sec-so-001'].status }} | {{ results['arch-sec-so-001'].trend_display }} | {{ results['arch-sec-so-001'].evidence \| default('—') }} |
| arch-sec-so-002 | Has Overview and Diagram subsections | error (mandatory) | 1.0 | {{ results['arch-sec-so-002'].previous_status \| default('—') }} | {{ results['arch-sec-so-002'].status }} | {{ results['arch-sec-so-002'].trend_display }} | {{ results['arch-sec-so-002'].evidence \| default('—') }} |
| arch-sec-so-003 | Describes system purpose | error (mandatory) | 1.0 | {{ results['arch-sec-so-003'].previous_status \| default('—') }} | {{ results['arch-sec-so-003'].status }} | {{ results['arch-sec-so-003'].trend_display }} | {{ results['arch-sec-so-003'].evidence \| default('—') }} |
| arch-sec-so-004 | Technology-independent | error (mandatory) | 1.0 | {{ results['arch-sec-so-004'].previous_status \| default('—') }} | {{ results['arch-sec-so-004'].status }} | {{ results['arch-sec-so-004'].trend_display }} | {{ results['arch-sec-so-004'].evidence \| default('—') }} |
| arch-sec-so-005 | Includes a diagram | warning (recommended) | 0.5 | {{ results['arch-sec-so-005'].previous_status \| default('—') }} | {{ results['arch-sec-so-005'].status }} | {{ results['arch-sec-so-005'].trend_display }} | {{ results['arch-sec-so-005'].evidence \| default('—') }} |

## 3. Component Model — `03-component_model.yaml` — weight 7.0 — **required**

**Why this matters:** This is where responsibility and ownership become explicit and checkable — every downstream section (Data Flow's ownership boundaries, Security's trust boundaries) depends on Component Model having named the components and assigned them clean, non-overlapping responsibilities first.

**Section Score: {{ sections.component_model.score }} / 100** ({{ sections.component_model.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-cm-001 | Section exists | error (mandatory) | 1.5 | {{ results['arch-sec-cm-001'].previous_status \| default('—') }} | {{ results['arch-sec-cm-001'].status }} | {{ results['arch-sec-cm-001'].trend_display }} | {{ results['arch-sec-cm-001'].evidence \| default('—') }} |
| arch-sec-cm-002 | Has Components and Component Diagram subsections | error (mandatory) | 1.0 | {{ results['arch-sec-cm-002'].previous_status \| default('—') }} | {{ results['arch-sec-cm-002'].status }} | {{ results['arch-sec-cm-002'].trend_display }} | {{ results['arch-sec-cm-002'].evidence \| default('—') }} |
| arch-sec-cm-003 | Every component has a Responsibility field | error (mandatory) | 1.0 | {{ results['arch-sec-cm-003'].previous_status \| default('—') }} | {{ results['arch-sec-cm-003'].status }} | {{ results['arch-sec-cm-003'].trend_display }} | {{ results['arch-sec-cm-003'].evidence \| default('—') }} |
| arch-sec-cm-004 | Every component has an Ownership field | error (mandatory) | 1.0 | {{ results['arch-sec-cm-004'].previous_status \| default('—') }} | {{ results['arch-sec-cm-004'].status }} | {{ results['arch-sec-cm-004'].trend_display }} | {{ results['arch-sec-cm-004'].evidence \| default('—') }} |
| arch-sec-cm-005 | No overlapping responsibilities | error (mandatory) | 1.0 | {{ results['arch-sec-cm-005'].previous_status \| default('—') }} | {{ results['arch-sec-cm-005'].status }} | {{ results['arch-sec-cm-005'].trend_display }} | {{ results['arch-sec-cm-005'].evidence \| default('—') }} |
| arch-sec-cm-006 | Technology-independent | error (mandatory) | 1.0 | {{ results['arch-sec-cm-006'].previous_status \| default('—') }} | {{ results['arch-sec-cm-006'].status }} | {{ results['arch-sec-cm-006'].trend_display }} | {{ results['arch-sec-cm-006'].evidence \| default('—') }} |
| arch-sec-cm-007 | Component relationship diagram present | warning (recommended) | 0.5 | {{ results['arch-sec-cm-007'].previous_status \| default('—') }} | {{ results['arch-sec-cm-007'].status }} | {{ results['arch-sec-cm-007'].trend_display }} | {{ results['arch-sec-cm-007'].evidence \| default('—') }} |

## 4. Communication Paths — `04-communication_paths.yaml` — weight 6.0 — **required**

**Why this matters:** Undocumented communication between components is exactly the "hidden coupling" architecture exists to prevent. This section forces every interaction implied by Component Model to be named, classified, and made visible.

**Section Score: {{ sections.communication_paths.score }} / 100** ({{ sections.communication_paths.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-comm-001 | Section exists | error (mandatory) | 1.5 | {{ results['arch-sec-comm-001'].previous_status \| default('—') }} | {{ results['arch-sec-comm-001'].status }} | {{ results['arch-sec-comm-001'].trend_display }} | {{ results['arch-sec-comm-001'].evidence \| default('—') }} |
| arch-sec-comm-002 | Has Communication Paths and Communication Diagram subsections | error (mandatory) | 1.0 | {{ results['arch-sec-comm-002'].previous_status \| default('—') }} | {{ results['arch-sec-comm-002'].status }} | {{ results['arch-sec-comm-002'].trend_display }} | {{ results['arch-sec-comm-002'].evidence \| default('—') }} |
| arch-sec-comm-003 | Every Component Model interaction has a documented path (cross-checked against §3) | error (mandatory) | 1.0 | {{ results['arch-sec-comm-003'].previous_status \| default('—') }} | {{ results['arch-sec-comm-003'].status }} | {{ results['arch-sec-comm-003'].trend_display }} | {{ results['arch-sec-comm-003'].evidence \| default('—') }} |
| arch-sec-comm-004 | Every path has a classified pattern (sync/async/event-driven/queue-based) | error (mandatory) | 1.0 | {{ results['arch-sec-comm-004'].previous_status \| default('—') }} | {{ results['arch-sec-comm-004'].status }} | {{ results['arch-sec-comm-004'].trend_display }} | {{ results['arch-sec-comm-004'].evidence \| default('—') }} |
| arch-sec-comm-005 | Technology-independent | error (mandatory) | 1.0 | {{ results['arch-sec-comm-005'].previous_status \| default('—') }} | {{ results['arch-sec-comm-005'].status }} | {{ results['arch-sec-comm-005'].trend_display }} | {{ results['arch-sec-comm-005'].evidence \| default('—') }} |
| arch-sec-comm-006 | Sequence diagram present | warning (recommended) | 0.5 | {{ results['arch-sec-comm-006'].previous_status \| default('—') }} | {{ results['arch-sec-comm-006'].status }} | {{ results['arch-sec-comm-006'].trend_display }} | {{ results['arch-sec-comm-006'].evidence \| default('—') }} |

## 5. Data Flow — `05-data_flow.yaml` — weight 5.0 — **required**

**Why this matters:** Data ownership is the piece of architecture most likely to be assumed rather than written down — until two components both think they own the same record. This section forces every major data path to name its owner at each boundary.

**Section Score: {{ sections.data_flow.score }} / 100** ({{ sections.data_flow.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-df-001 | Section exists | error (mandatory) | 1.5 | {{ results['arch-sec-df-001'].previous_status \| default('—') }} | {{ results['arch-sec-df-001'].status }} | {{ results['arch-sec-df-001'].trend_display }} | {{ results['arch-sec-df-001'].evidence \| default('—') }} |
| arch-sec-df-002 | Has Data Paths and Data Flow Diagram subsections | error (mandatory) | 1.0 | {{ results['arch-sec-df-002'].previous_status \| default('—') }} | {{ results['arch-sec-df-002'].status }} | {{ results['arch-sec-df-002'].trend_display }} | {{ results['arch-sec-df-002'].evidence \| default('—') }} |
| arch-sec-df-003 | Data ownership boundaries defined per path | error (mandatory) | 1.0 | {{ results['arch-sec-df-003'].previous_status \| default('—') }} | {{ results['arch-sec-df-003'].status }} | {{ results['arch-sec-df-003'].trend_display }} | {{ results['arch-sec-df-003'].evidence \| default('—') }} |
| arch-sec-df-004 | Technology-independent | error (mandatory) | 1.0 | {{ results['arch-sec-df-004'].previous_status \| default('—') }} | {{ results['arch-sec-df-004'].status }} | {{ results['arch-sec-df-004'].trend_display }} | {{ results['arch-sec-df-004'].evidence \| default('—') }} |
| arch-sec-df-005 | Data flow diagram present | warning (recommended) | 0.5 | {{ results['arch-sec-df-005'].previous_status \| default('—') }} | {{ results['arch-sec-df-005'].status }} | {{ results['arch-sec-df-005'].trend_display }} | {{ results['arch-sec-df-005'].evidence \| default('—') }} |

## 6. Security Considerations — `06-security_considerations.yaml` — weight 6.0 — **required**

**Why this matters:** Security bolted on after the fact is the classic failure mode this section exists to prevent — every external interface named in Component Model needs a trust boundary here, and every named threat needs a mitigation, not just an acknowledgment.

**Section Score: {{ sections.security_considerations.score }} / 100** ({{ sections.security_considerations.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-sec-001 | Section exists | error (mandatory) | 1.5 | {{ results['arch-sec-sec-001'].previous_status \| default('—') }} | {{ results['arch-sec-sec-001'].status }} | {{ results['arch-sec-sec-001'].trend_display }} | {{ results['arch-sec-sec-001'].evidence \| default('—') }} |
| arch-sec-sec-002 | Has Trust Boundaries and Threat Model subsections | error (mandatory) | 1.0 | {{ results['arch-sec-sec-002'].previous_status \| default('—') }} | {{ results['arch-sec-sec-002'].status }} | {{ results['arch-sec-sec-002'].trend_display }} | {{ results['arch-sec-sec-002'].evidence \| default('—') }} |
| arch-sec-sec-003 | Trust boundaries defined for all external interfaces (cross-checked against §3) | error (mandatory) | 1.0 | {{ results['arch-sec-sec-003'].previous_status \| default('—') }} | {{ results['arch-sec-sec-003'].status }} | {{ results['arch-sec-sec-003'].trend_display }} | {{ results['arch-sec-sec-003'].evidence \| default('—') }} |
| arch-sec-sec-004 | Every listed threat has a mitigation | error (mandatory) | 1.0 | {{ results['arch-sec-sec-004'].previous_status \| default('—') }} | {{ results['arch-sec-sec-004'].status }} | {{ results['arch-sec-sec-004'].trend_display }} | {{ results['arch-sec-sec-004'].evidence \| default('—') }} |
| arch-sec-sec-005 | Technology-independent | error (mandatory) | 1.0 | {{ results['arch-sec-sec-005'].previous_status \| default('—') }} | {{ results['arch-sec-sec-005'].status }} | {{ results['arch-sec-sec-005'].trend_display }} | {{ results['arch-sec-sec-005'].evidence \| default('—') }} |
| arch-sec-sec-006 | Trust boundary diagram present | warning (recommended) | 0.5 | {{ results['arch-sec-sec-006'].previous_status \| default('—') }} | {{ results['arch-sec-sec-006'].status }} | {{ results['arch-sec-sec-006'].trend_display }} | {{ results['arch-sec-sec-006'].evidence \| default('—') }} |

## 7. Rationale — `07-rationale.yaml` — weight 1.8 — optional

**Why this matters:** Rationale is how a future maintainer tells the difference between "this is deliberate" and "this looks like it could be improved." Without it, every architectural decision looks equally negotiable, including the ones that aren't.

**Section Score: {{ sections.rationale.score }} / 100** ({{ sections.rationale.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-rat-001 | Section present | warning (recommended) | 0.5 | {{ results['arch-sec-rat-001'].previous_status \| default('—') }} | {{ results['arch-sec-rat-001'].status }} | {{ results['arch-sec-rat-001'].trend_display }} | {{ results['arch-sec-rat-001'].evidence \| default('—') }} |
| arch-sec-rat-002 | Each decision has alternatives documented | warning (recommended) | 0.5 | {{ results['arch-sec-rat-002'].previous_status \| default('—') }} | {{ results['arch-sec-rat-002'].status }} | {{ results['arch-sec-rat-002'].trend_display }} | {{ results['arch-sec-rat-002'].evidence \| default('—') }} |
| arch-sec-rat-003 | Each decision has a rejection reason | warning (recommended) | 0.5 | {{ results['arch-sec-rat-003'].previous_status \| default('—') }} | {{ results['arch-sec-rat-003'].status }} | {{ results['arch-sec-rat-003'].trend_display }} | {{ results['arch-sec-rat-003'].evidence \| default('—') }} |
| arch-sec-rat-004 | References architectural goals | warning (recommended) | 0.3 | {{ results['arch-sec-rat-004'].previous_status \| default('—') }} | {{ results['arch-sec-rat-004'].status }} | {{ results['arch-sec-rat-004'].trend_display }} | {{ results['arch-sec-rat-004'].evidence \| default('—') }} |

## 8. Constraints — `08-constraints.yaml` — weight 3.0 — optional

**Why this matters:** A constraint with no source is indistinguishable from a preference someone made up. This section forces every hard constraint to be attributable — to External Context, Platform Pillars, or an explicit organizational rule — so it can be challenged or retired when its source changes.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-con-001 | Section present | warning (recommended) | 0.5 | {{ results['arch-sec-con-001'].previous_status \| default('—') }} | {{ results['arch-sec-con-001'].status }} | {{ results['arch-sec-con-001'].trend_display }} | {{ results['arch-sec-con-001'].evidence \| default('—') }} |
| arch-sec-con-002 | Hard constraints have source attribution | error (mandatory) | 1.0 | {{ results['arch-sec-con-002'].previous_status \| default('—') }} | {{ results['arch-sec-con-002'].status }} | {{ results['arch-sec-con-002'].trend_display }} | {{ results['arch-sec-con-002'].evidence \| default('—') }} |
| arch-sec-con-003 | Hard and soft constraints are distinguished | warning (recommended) | 0.5 | {{ results['arch-sec-con-003'].previous_status \| default('—') }} | {{ results['arch-sec-con-003'].status }} | {{ results['arch-sec-con-003'].trend_display }} | {{ results['arch-sec-con-003'].evidence \| default('—') }} |
| arch-sec-con-004 | Technology-independent | error (mandatory) | 1.0 | {{ results['arch-sec-con-004'].previous_status \| default('—') }} | {{ results['arch-sec-con-004'].status }} | {{ results['arch-sec-con-004'].trend_display }} | {{ results['arch-sec-con-004'].evidence \| default('—') }} |

## 9. Traceability — `09-traceability.yaml` — weight 1.8 — optional

**Why this matters:** Traceability is what makes the non-contradiction rule enforceable — without a stated derivation chain and a list of downstream standards, nothing stops a Feature Technical Design from silently drifting away from what Architecture actually permits.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-trace-001 | Section present | warning (recommended) | 0.5 | {{ results['arch-sec-trace-001'].previous_status \| default('—') }} | {{ results['arch-sec-trace-001'].status }} | {{ results['arch-sec-trace-001'].trend_display }} | {{ results['arch-sec-trace-001'].evidence \| default('—') }} |
| arch-sec-trace-002 | Derivation chain documented | warning (recommended) | 0.5 | {{ results['arch-sec-trace-002'].previous_status \| default('—') }} | {{ results['arch-sec-trace-002'].status }} | {{ results['arch-sec-trace-002'].trend_display }} | {{ results['arch-sec-trace-002'].evidence \| default('—') }} |
| arch-sec-trace-003 | Non-contradiction rule stated | warning (recommended) | 0.5 | {{ results['arch-sec-trace-003'].previous_status \| default('—') }} | {{ results['arch-sec-trace-003'].status }} | {{ results['arch-sec-trace-003'].trend_display }} | {{ results['arch-sec-trace-003'].evidence \| default('—') }} |
| arch-sec-trace-004 | Downstream standards listed | warning (recommended) | 0.3 | {{ results['arch-sec-trace-004'].previous_status \| default('—') }} | {{ results['arch-sec-trace-004'].status }} | {{ results['arch-sec-trace-004'].trend_display }} | {{ results['arch-sec-trace-004'].evidence \| default('—') }} |

## 10. Operational Readiness — `10-operational_readiness.yaml` — weight 0.6 — not in Required Sections table

**Why this matters:** Not a formal requirement of the Architecture standard, but a document that skips deployment/rollback/monitoring guidance entirely leaves Engineering to invent an operational story with no architectural grounding.

**Section Score: {{ sections.operational_readiness.score }} / 100** ({{ sections.operational_readiness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-or-001 | Section present (recommended, not required) | suggestion | 0.3 | {{ results['arch-sec-or-001'].previous_status \| default('—') }} | {{ results['arch-sec-or-001'].status }} | {{ results['arch-sec-or-001'].trend_display }} | {{ results['arch-sec-or-001'].evidence \| default('—') }} |
| arch-sec-or-002 | If present, covers monitoring, alerting, deployment, and rollback | warning | 0.3 | {{ results['arch-sec-or-002'].previous_status \| default('—') }} | {{ results['arch-sec-or-002'].status }} | {{ results['arch-sec-or-002'].trend_display }} | {{ results['arch-sec-or-002'].evidence \| default('—') }} |

## 11. Observability — `11-observability.yaml` — weight 0.6 — not in Required Sections table

**Why this matters:** Same rationale as Operational Readiness — not required, but a system with no documented logging/metrics/tracing strategy pushes that decision to whoever implements it, with no architectural input.

**Section Score: {{ sections.observability.score }} / 100** ({{ sections.observability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| arch-sec-obs-001 | Section present (recommended, not required) | suggestion | 0.3 | {{ results['arch-sec-obs-001'].previous_status \| default('—') }} | {{ results['arch-sec-obs-001'].status }} | {{ results['arch-sec-obs-001'].trend_display }} | {{ results['arch-sec-obs-001'].evidence \| default('—') }} |
| arch-sec-obs-002 | If present, covers logging, metrics, and tracing | warning | 0.3 | {{ results['arch-sec-obs-002'].previous_status \| default('—') }} | {{ results['arch-sec-obs-002'].status }} | {{ results['arch-sec-obs-002'].trend_display }} | {{ results['arch-sec-obs-002'].evidence \| default('—') }} |

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
| Domain | architecture |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/05-architecture/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
