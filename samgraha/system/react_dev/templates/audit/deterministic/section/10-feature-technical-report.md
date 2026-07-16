# Deterministic Section Report — Feature Technical

**Document:** {{ document_path }}
**Standard:** `documentation-standards/10-feature-technical-standards.md`
**Rule Files:** `audit/deterministic/section/10-feature-technical/*.yaml`
**Auditor:** System (deterministic engine)
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 17 section scores below
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
| 2 | Participating Components | **required** | 4.0 | {{ sections.participating_components.score }} / 100 | {{ sections.participating_components.previous_score | default('—') }} | {{ sections.participating_components.trend_display }} |
| 3 | Component Interactions | **required** | 4.0 | {{ sections.component_interactions.score }} / 100 | {{ sections.component_interactions.previous_score | default('—') }} | {{ sections.component_interactions.trend_display }} |
| 4 | Data Ownership | **required** | 4.0 | {{ sections.data_ownership.score }} / 100 | {{ sections.data_ownership.previous_score | default('—') }} | {{ sections.data_ownership.trend_display }} |
| 5 | Feature Specification | optional | 1.8 | {{ sections.feature_specification.score }} / 100 | {{ sections.feature_specification.previous_score | default('—') }} | {{ sections.feature_specification.trend_display }} |
| 6 | Component Responsibilities | optional | 1.8 | {{ sections.component_responsibilities.score }} / 100 | {{ sections.component_responsibilities.previous_score | default('—') }} | {{ sections.component_responsibilities.trend_display }} |
| 7 | Runtime Behavior | optional | 1.8 | {{ sections.runtime_behavior.score }} / 100 | {{ sections.runtime_behavior.previous_score | default('—') }} | {{ sections.runtime_behavior.trend_display }} |
| 8 | Communication Paths | optional | 1.8 | {{ sections.communication_paths.score }} / 100 | {{ sections.communication_paths.previous_score | default('—') }} | {{ sections.communication_paths.trend_display }} |
| 9 | Integration Points | optional | 1.8 | {{ sections.integration_points.score }} / 100 | {{ sections.integration_points.previous_score | default('—') }} | {{ sections.integration_points.trend_display }} |
| 10 | External Dependencies | optional | 1.3 | {{ sections.external_dependencies.score }} / 100 | {{ sections.external_dependencies.previous_score | default('—') }} | {{ sections.external_dependencies.trend_display }} |
| 11 | Runtime Constraints | optional | 1.3 | {{ sections.runtime_constraints.score }} / 100 | {{ sections.runtime_constraints.previous_score | default('—') }} | {{ sections.runtime_constraints.trend_display }} |
| 12 | Architectural Constraints | optional | 1.3 | {{ sections.architectural_constraints.score }} / 100 | {{ sections.architectural_constraints.previous_score | default('—') }} | {{ sections.architectural_constraints.trend_display }} |
| 13 | Security Considerations | optional | 1.8 | {{ sections.security_considerations.score }} / 100 | {{ sections.security_considerations.previous_score | default('—') }} | {{ sections.security_considerations.trend_display }} |
| 14 | Performance Considerations | optional | 1.3 | {{ sections.performance_considerations.score }} / 100 | {{ sections.performance_considerations.previous_score | default('—') }} | {{ sections.performance_considerations.trend_display }} |
| 15 | Failure Handling | optional | 1.8 | {{ sections.failure_handling.score }} / 100 | {{ sections.failure_handling.previous_score | default('—') }} | {{ sections.failure_handling.trend_display }} |
| 16 | Extension Points | optional | 1.8 | {{ sections.extension_points.score }} / 100 | {{ sections.extension_points.previous_score | default('—') }} | {{ sections.extension_points.trend_display }} |
| 17 | Traceability | optional | 1.3 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

The 4 required sections carry 16.0 of the document's 37.9 total rule weight — a document can only pass if those four are both present and internally sound; the remaining thirteen are recommended-quality signal, not gating.

---

## 1. Purpose — weight 4.0 — **required**

**Why this matters:** Purpose defines why Feature Technical Documentation exists before a reader sees a single component or interaction. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-purpose-001 | Purpose section exists | error (mandatory) | 1.5 | {{ results['ft-sec-purpose-001'].previous_status \| default('—') }} | {{ results['ft-sec-purpose-001'].status }} | {{ results['ft-sec-purpose-001'].trend_display }} | {{ results['ft-sec-purpose-001'].evidence \| default('—') }} |
| ft-sec-purpose-002 | States feature technical intent | error (mandatory) | 1.0 | {{ results['ft-sec-purpose-002'].previous_status \| default('—') }} | {{ results['ft-sec-purpose-002'].status }} | {{ results['ft-sec-purpose-002'].trend_display }} | {{ results['ft-sec-purpose-002'].evidence \| default('—') }} |
| ft-sec-purpose-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['ft-sec-purpose-003'].previous_status \| default('—') }} | {{ results['ft-sec-purpose-003'].status }} | {{ results['ft-sec-purpose-003'].trend_display }} | {{ results['ft-sec-purpose-003'].evidence \| default('—') }} |
| ft-sec-purpose-004 | Scope boundaries defined | warning (recommended) | 0.5 | {{ results['ft-sec-purpose-004'].previous_status \| default('—') }} | {{ results['ft-sec-purpose-004'].status }} | {{ results['ft-sec-purpose-004'].trend_display }} | {{ results['ft-sec-purpose-004'].evidence \| default('—') }} |

## 2. Participating Components — weight 4.0 — **required**

**Why this matters:** Participating Components is the inventory of every module, service, or sub-system involved in the feature. A missing or incomplete list means downstream sections (Component Interactions, Data Ownership, Runtime Behavior) reference components that were never formally introduced.

**Section Score: {{ sections.participating_components.score }} / 100** ({{ sections.participating_components.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-components-001 | Participating Components section exists | error (mandatory) | 1.5 | {{ results['ft-sec-components-001'].previous_status \| default('—') }} | {{ results['ft-sec-components-001'].status }} | {{ results['ft-sec-components-001'].trend_display }} | {{ results['ft-sec-components-001'].evidence \| default('—') }} |
| ft-sec-components-002 | Lists components participating in the feature | error (mandatory) | 1.0 | {{ results['ft-sec-components-002'].previous_status \| default('—') }} | {{ results['ft-sec-components-002'].status }} | {{ results['ft-sec-components-002'].trend_display }} | {{ results['ft-sec-components-002'].evidence \| default('—') }} |
| ft-sec-components-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['ft-sec-components-003'].previous_status \| default('—') }} | {{ results['ft-sec-components-003'].status }} | {{ results['ft-sec-components-003'].trend_display }} | {{ results['ft-sec-components-003'].evidence \| default('—') }} |
| ft-sec-components-004 | Defines component boundaries | warning (recommended) | 0.5 | {{ results['ft-sec-components-004'].previous_status \| default('—') }} | {{ results['ft-sec-components-004'].status }} | {{ results['ft-sec-components-004'].trend_display }} | {{ results['ft-sec-components-004'].evidence \| default('—') }} |

## 3. Component Interactions — weight 4.0 — **required**

**Why this matters:** Component Interactions describes how components communicate and depend on each other. Without it, readers cannot understand the feature's data flow, call patterns, or coupling characteristics — all of which are essential for Implementation.

**Section Score: {{ sections.component_interactions.score }} / 100** ({{ sections.component_interactions.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-interactions-001 | Component Interactions section exists | error (mandatory) | 1.5 | {{ results['ft-sec-interactions-001'].previous_status \| default('—') }} | {{ results['ft-sec-interactions-001'].status }} | {{ results['ft-sec-interactions-001'].trend_display }} | {{ results['ft-sec-interactions-001'].evidence \| default('—') }} |
| ft-sec-interactions-002 | Describes how components communicate and interact | error (mandatory) | 1.0 | {{ results['ft-sec-interactions-002'].previous_status \| default('—') }} | {{ results['ft-sec-interactions-002'].status }} | {{ results['ft-sec-interactions-002'].trend_display }} | {{ results['ft-sec-interactions-002'].evidence \| default('—') }} |
| ft-sec-interactions-003 | Technology-independent (no protocols, frameworks, or implementation specifics) | error (mandatory) | 1.0 | {{ results['ft-sec-interactions-003'].previous_status \| default('—') }} | {{ results['ft-sec-interactions-003'].status }} | {{ results['ft-sec-interactions-003'].trend_display }} | {{ results['ft-sec-interactions-003'].evidence \| default('—') }} |
| ft-sec-interactions-004 | Defines interaction patterns (sync, async, event-driven) | warning (recommended) | 0.5 | {{ results['ft-sec-interactions-004'].previous_status \| default('—') }} | {{ results['ft-sec-interactions-004'].status }} | {{ results['ft-sec-interactions-004'].trend_display }} | {{ results['ft-sec-interactions-004'].evidence \| default('—') }} |

## 4. Data Ownership — weight 4.0 — **required**

**Why this matters:** Data Ownership assigns authoritative ownership for each data entity to a specific component. Without it, multiple components may silently write to the same data, creating consistency bugs that surface only at runtime.

**Section Score: {{ sections.data_ownership.score }} / 100** ({{ sections.data_ownership.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-data-001 | Data Ownership section exists | error (mandatory) | 1.5 | {{ results['ft-sec-data-001'].previous_status \| default('—') }} | {{ results['ft-sec-data-001'].status }} | {{ results['ft-sec-data-001'].trend_display }} | {{ results['ft-sec-data-001'].evidence \| default('—') }} |
| ft-sec-data-002 | Defines which components own or are responsible for which data | error (mandatory) | 1.0 | {{ results['ft-sec-data-002'].previous_status \| default('—') }} | {{ results['ft-sec-data-002'].status }} | {{ results['ft-sec-data-002'].trend_display }} | {{ results['ft-sec-data-002'].evidence \| default('—') }} |
| ft-sec-data-003 | Technology-independent (no database schemas, storage technologies, or implementation specifics) | error (mandatory) | 1.0 | {{ results['ft-sec-data-003'].previous_status \| default('—') }} | {{ results['ft-sec-data-003'].status }} | {{ results['ft-sec-data-003'].trend_display }} | {{ results['ft-sec-data-003'].evidence \| default('—') }} |
| ft-sec-data-004 | Defines data lifecycle (create, read, update, delete) | warning (recommended) | 0.5 | {{ results['ft-sec-data-004'].previous_status \| default('—') }} | {{ results['ft-sec-data-004'].status }} | {{ results['ft-sec-data-004'].trend_display }} | {{ results['ft-sec-data-004'].evidence \| default('—') }} |

## 5. Feature Specification — weight 1.8 — optional

**Why this matters:** Feature Specification defines the technical boundaries, inputs, outputs, and behavioral contract of the feature. Without it, Implementation has no declarative contract to code against.

**Section Score: {{ sections.feature_specification.score }} / 100** ({{ sections.feature_specification.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-spec-001 | Feature Specification section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-spec-001'].previous_status \| default('—') }} | {{ results['ft-sec-spec-001'].status }} | {{ results['ft-sec-spec-001'].trend_display }} | {{ results['ft-sec-spec-001'].evidence \| default('—') }} |
| ft-sec-spec-002 | Defines technical behavior of the feature | warning (recommended) | 0.5 | {{ results['ft-sec-spec-002'].previous_status \| default('—') }} | {{ results['ft-sec-spec-002'].status }} | {{ results['ft-sec-spec-002'].trend_display }} | {{ results['ft-sec-spec-002'].evidence \| default('—') }} |
| ft-sec-spec-003 | Technology-independent | error (non-mandatory) | 1.0 | {{ results['ft-sec-spec-003'].previous_status \| default('—') }} | {{ results['ft-sec-spec-003'].status }} | {{ results['ft-sec-spec-003'].trend_display }} | {{ results['ft-sec-spec-003'].evidence \| default('—') }} |

## 6. Component Responsibilities — weight 1.8 — optional

**Why this matters:** Component Responsibilities defines what each participating component owns within the feature, preventing overlap and gaps in accountability.

**Section Score: {{ sections.component_responsibilities.score }} / 100** ({{ sections.component_responsibilities.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-resp-001 | Component Responsibilities section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-resp-001'].previous_status \| default('—') }} | {{ results['ft-sec-resp-001'].status }} | {{ results['ft-sec-resp-001'].trend_display }} | {{ results['ft-sec-resp-001'].evidence \| default('—') }} |
| ft-sec-resp-002 | Defines responsibilities for each participating component | warning (recommended) | 0.5 | {{ results['ft-sec-resp-002'].previous_status \| default('—') }} | {{ results['ft-sec-resp-002'].status }} | {{ results['ft-sec-resp-002'].trend_display }} | {{ results['ft-sec-resp-002'].evidence \| default('—') }} |
| ft-sec-resp-003 | Aligns with Architecture component model | error (non-mandatory) | 1.0 | {{ results['ft-sec-resp-003'].previous_status \| default('—') }} | {{ results['ft-sec-resp-003'].status }} | {{ results['ft-sec-resp-003'].trend_display }} | {{ results['ft-sec-resp-003'].evidence \| default('—') }} |

## 7. Runtime Behavior — weight 1.8 — optional

**Why this matters:** Runtime Behavior describes the feature's operational execution model — startup, steady-state, state transitions, and shutdown. Without it, Implementation cannot determine the correct lifecycle sequence.

**Section Score: {{ sections.runtime_behavior.score }} / 100** ({{ sections.runtime_behavior.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-runtime-001 | Runtime Behavior section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-runtime-001'].previous_status \| default('—') }} | {{ results['ft-sec-runtime-001'].status }} | {{ results['ft-sec-runtime-001'].trend_display }} | {{ results['ft-sec-runtime-001'].evidence \| default('—') }} |
| ft-sec-runtime-002 | Describes runtime behavior | warning (recommended) | 0.5 | {{ results['ft-sec-runtime-002'].previous_status \| default('—') }} | {{ results['ft-sec-runtime-002'].status }} | {{ results['ft-sec-runtime-002'].trend_display }} | {{ results['ft-sec-runtime-002'].evidence \| default('—') }} |
| ft-sec-runtime-003 | Technology-independent | error (non-mandatory) | 1.0 | {{ results['ft-sec-runtime-003'].previous_status \| default('—') }} | {{ results['ft-sec-runtime-003'].status }} | {{ results['ft-sec-runtime-003'].trend_display }} | {{ results['ft-sec-runtime-003'].evidence \| default('—') }} |

## 8. Communication Paths — weight 1.8 — optional

**Why this matters:** Communication Paths documents the data flow topology across the feature — message routing, delivery guarantees, and backpressure handling. Without it, readers cannot assess whether data arrives reliably and in order.

**Section Score: {{ sections.communication_paths.score }} / 100** ({{ sections.communication_paths.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-comm-001 | Communication Paths section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-comm-001'].previous_status \| default('—') }} | {{ results['ft-sec-comm-001'].status }} | {{ results['ft-sec-comm-001'].trend_display }} | {{ results['ft-sec-comm-001'].evidence \| default('—') }} |
| ft-sec-comm-002 | Defines communication paths between components | warning (recommended) | 0.5 | {{ results['ft-sec-comm-002'].previous_status \| default('—') }} | {{ results['ft-sec-comm-002'].status }} | {{ results['ft-sec-comm-002'].trend_display }} | {{ results['ft-sec-comm-002'].evidence \| default('—') }} |
| ft-sec-comm-003 | Technology-independent (no protocols, message brokers, or implementation specifics) | error (non-mandatory) | 1.0 | {{ results['ft-sec-comm-003'].previous_status \| default('—') }} | {{ results['ft-sec-comm-003'].status }} | {{ results['ft-sec-comm-003'].trend_display }} | {{ results['ft-sec-comm-003'].evidence \| default('—') }} |

## 9. Integration Points — weight 1.8 — optional

**Why this matters:** Integration Points document every boundary where the feature connects to external systems. Without it, implementation teams may miss integration contracts and fail at system boundaries.

**Section Score: {{ sections.integration_points.score }} / 100** ({{ sections.integration_points.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-integration-001 | Integration Points section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-integration-001'].previous_status \| default('—') }} | {{ results['ft-sec-integration-001'].status }} | {{ results['ft-sec-integration-001'].trend_display }} | {{ results['ft-sec-integration-001'].evidence \| default('—') }} |
| ft-sec-integration-002 | Defines integration points with external systems | warning (recommended) | 0.5 | {{ results['ft-sec-integration-002'].previous_status \| default('—') }} | {{ results['ft-sec-integration-002'].status }} | {{ results['ft-sec-integration-002'].trend_display }} | {{ results['ft-sec-integration-002'].evidence \| default('—') }} |
| ft-sec-integration-003 | Technology-independent (no specific APIs, external systems, or implementation specifics) | error (non-mandatory) | 1.0 | {{ results['ft-sec-integration-003'].previous_status \| default('—') }} | {{ results['ft-sec-integration-003'].status }} | {{ results['ft-sec-integration-003'].trend_display }} | {{ results['ft-sec-integration-003'].evidence \| default('—') }} |

## 10. External Dependencies — weight 1.3 — optional

**Why this matters:** External Dependencies capture every third-party library, service, or infrastructure the feature relies on. Without it, version conflicts and license issues surface only in production.

**Section Score: {{ sections.external_dependencies.score }} / 100** ({{ sections.external_dependencies.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-extdep-001 | External Dependencies section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-extdep-001'].previous_status \| default('—') }} | {{ results['ft-sec-extdep-001'].status }} | {{ results['ft-sec-extdep-001'].trend_display }} | {{ results['ft-sec-extdep-001'].evidence \| default('—') }} |
| ft-sec-extdep-002 | Lists external dependencies | warning (recommended) | 0.5 | {{ results['ft-sec-extdep-002'].previous_status \| default('—') }} | {{ results['ft-sec-extdep-002'].status }} | {{ results['ft-sec-extdep-002'].trend_display }} | {{ results['ft-sec-extdep-002'].evidence \| default('—') }} |
| ft-sec-extdep-003 | Defines dependency nature (required, optional, version constraints) | warning (recommended) | 0.5 | {{ results['ft-sec-extdep-003'].previous_status \| default('—') }} | {{ results['ft-sec-extdep-003'].status }} | {{ results['ft-sec-extdep-003'].trend_display }} | {{ results['ft-sec-extdep-003'].evidence \| default('—') }} |

## 11. Runtime Constraints — weight 1.3 — optional

**Why this matters:** Runtime Constraints specify measurable resource limits the feature must operate within. Without numeric thresholds, performance requirements are ambiguous and unverifiable.

**Section Score: {{ sections.runtime_constraints.score }} / 100** ({{ sections.runtime_constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-rtcon-001 | Runtime Constraints section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-rtcon-001'].previous_status \| default('—') }} | {{ results['ft-sec-rtcon-001'].status }} | {{ results['ft-sec-rtcon-001'].trend_display }} | {{ results['ft-sec-rtcon-001'].evidence \| default('—') }} |
| ft-sec-rtcon-002 | Defines runtime constraints (latency, throughput, memory, availability) | warning (recommended) | 0.5 | {{ results['ft-sec-rtcon-002'].previous_status \| default('—') }} | {{ results['ft-sec-rtcon-002'].status }} | {{ results['ft-sec-rtcon-002'].trend_display }} | {{ results['ft-sec-rtcon-002'].evidence \| default('—') }} |
| ft-sec-rtcon-003 | Has measurable thresholds | warning (recommended) | 0.5 | {{ results['ft-sec-rtcon-003'].previous_status \| default('—') }} | {{ results['ft-sec-rtcon-003'].status }} | {{ results['ft-sec-rtcon-003'].trend_display }} | {{ results['ft-sec-rtcon-003'].evidence \| default('—') }} |

## 12. Architectural Constraints — weight 1.3 — optional

**Why this matters:** Architectural Constraints define the non-negotiable design rules the feature must adhere to. Without them, implementation may violate architectural principles that were decided upstream.

**Section Score: {{ sections.architectural_constraints.score }} / 100** ({{ sections.architectural_constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-archcon-001 | Architectural Constraints section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-archcon-001'].previous_status \| default('—') }} | {{ results['ft-sec-archcon-001'].status }} | {{ results['ft-sec-archcon-001'].trend_display }} | {{ results['ft-sec-archcon-001'].evidence \| default('—') }} |
| ft-sec-archcon-002 | Defines architectural constraints | warning (recommended) | 0.5 | {{ results['ft-sec-archcon-002'].previous_status \| default('—') }} | {{ results['ft-sec-archcon-002'].status }} | {{ results['ft-sec-archcon-002'].trend_display }} | {{ results['ft-sec-archcon-002'].evidence \| default('—') }} |
| ft-sec-archcon-003 | References Architecture domain as source of constraints | warning (recommended) | 0.5 | {{ results['ft-sec-archcon-003'].previous_status \| default('—') }} | {{ results['ft-sec-archcon-003'].status }} | {{ results['ft-sec-archcon-003'].trend_display }} | {{ results['ft-sec-archcon-003'].evidence \| default('—') }} |

## 13. Security Considerations — weight 1.8 — optional

**Why this matters:** Security Considerations document the threat model, authentication, authorization, and data protection requirements. Without them, security is treated as an afterthought rather than a design constraint.

**Section Score: {{ sections.security_considerations.score }} / 100** ({{ sections.security_considerations.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-security-001 | Security Considerations section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-security-001'].previous_status \| default('—') }} | {{ results['ft-sec-security-001'].status }} | {{ results['ft-sec-security-001'].trend_display }} | {{ results['ft-sec-security-001'].evidence \| default('—') }} |
| ft-sec-security-002 | Defines security aspects (authentication, authorization, encryption, data protection) | warning (recommended) | 0.5 | {{ results['ft-sec-security-002'].previous_status \| default('—') }} | {{ results['ft-sec-security-002'].status }} | {{ results['ft-sec-security-002'].trend_display }} | {{ results['ft-sec-security-002'].evidence \| default('—') }} |
| ft-sec-security-003 | Technology-independent (no specific security libraries or frameworks) | error (non-mandatory) | 1.0 | {{ results['ft-sec-security-003'].previous_status \| default('—') }} | {{ results['ft-sec-security-003'].status }} | {{ results['ft-sec-security-003'].trend_display }} | {{ results['ft-sec-security-003'].evidence \| default('—') }} |

## 14. Performance Considerations — weight 1.3 — optional

**Why this matters:** Performance Considerations document latency targets, throughput requirements, and resource utilization profiles. Without them, performance expectations are undocumented and unverifiable.

**Section Score: {{ sections.performance_considerations.score }} / 100** ({{ sections.performance_considerations.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-perf-001 | Performance Considerations section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-perf-001'].previous_status \| default('—') }} | {{ results['ft-sec-perf-001'].status }} | {{ results['ft-sec-perf-001'].trend_display }} | {{ results['ft-sec-perf-001'].evidence \| default('—') }} |
| ft-sec-perf-002 | Defines performance aspects (latency, throughput, optimization) | warning (recommended) | 0.5 | {{ results['ft-sec-perf-002'].previous_status \| default('—') }} | {{ results['ft-sec-perf-002'].status }} | {{ results['ft-sec-perf-002'].trend_display }} | {{ results['ft-sec-perf-002'].evidence \| default('—') }} |
| ft-sec-perf-003 | Has measurable performance targets | warning (recommended) | 0.5 | {{ results['ft-sec-perf-003'].previous_status \| default('—') }} | {{ results['ft-sec-perf-003'].status }} | {{ results['ft-sec-perf-003'].trend_display }} | {{ results['ft-sec-perf-003'].evidence \| default('—') }} |

## 15. Failure Handling — weight 1.8 — optional

**Why this matters:** Failure Handling documents how the feature detects, responds to, and recovers from errors. Without it, error handling is left to individual developer judgment, leading to inconsistent recovery behavior.

**Section Score: {{ sections.failure_handling.score }} / 100** ({{ sections.failure_handling.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-failure-001 | Failure Handling section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-failure-001'].previous_status \| default('—') }} | {{ results['ft-sec-failure-001'].status }} | {{ results['ft-sec-failure-001'].trend_display }} | {{ results['ft-sec-failure-001'].evidence \| default('—') }} |
| ft-sec-failure-002 | Defines failure modes (error handling, retry, fallback, recovery) | warning (recommended) | 0.5 | {{ results['ft-sec-failure-002'].previous_status \| default('—') }} | {{ results['ft-sec-failure-002'].status }} | {{ results['ft-sec-failure-002'].trend_display }} | {{ results['ft-sec-failure-002'].evidence \| default('—') }} |
| ft-sec-failure-003 | Technology-independent (no specific error-handling libraries or frameworks) | error (non-mandatory) | 1.0 | {{ results['ft-sec-failure-003'].previous_status \| default('—') }} | {{ results['ft-sec-failure-003'].status }} | {{ results['ft-sec-failure-003'].trend_display }} | {{ results['ft-sec-failure-003'].evidence \| default('—') }} |

## 16. Extension Points — weight 1.8 — optional

**Why this matters:** Extension Points document where the feature can be customized or extended by other features. Without them, consumers cannot safely extend the feature without risking breakage.

**Section Score: {{ sections.extension_points.score }} / 100** ({{ sections.extension_points.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-extension-001 | Extension Points section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-extension-001'].previous_status \| default('—') }} | {{ results['ft-sec-extension-001'].status }} | {{ results['ft-sec-extension-001'].trend_display }} | {{ results['ft-sec-extension-001'].evidence \| default('—') }} |
| ft-sec-extension-002 | Defines extension mechanisms (plugin, hook, override) | warning (recommended) | 0.5 | {{ results['ft-sec-extension-002'].previous_status \| default('—') }} | {{ results['ft-sec-extension-002'].status }} | {{ results['ft-sec-extension-002'].trend_display }} | {{ results['ft-sec-extension-002'].evidence \| default('—') }} |
| ft-sec-extension-003 | Technology-independent (no specific extension frameworks or plugin systems) | error (non-mandatory) | 1.0 | {{ results['ft-sec-extension-003'].previous_status \| default('—') }} | {{ results['ft-sec-extension-003'].status }} | {{ results['ft-sec-extension-003'].trend_display }} | {{ results['ft-sec-extension-003'].evidence \| default('—') }} |

## 17. Traceability — weight 1.3 — optional

**Why this matters:** Traceability documents the links between feature requirements, design decisions, and implementation artifacts. Without it, impact analysis is impossible and untraced elements silently accumulate.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-sec-trace-001 | Traceability section exists | suggestion (optional) | 0.3 | {{ results['ft-sec-trace-001'].previous_status \| default('—') }} | {{ results['ft-sec-trace-001'].status }} | {{ results['ft-sec-trace-001'].trend_display }} | {{ results['ft-sec-trace-001'].evidence \| default('—') }} |
| ft-sec-trace-002 | Links to upstream domains (Feature, Engineering, Architecture) | warning (recommended) | 0.5 | {{ results['ft-sec-trace-002'].previous_status \| default('—') }} | {{ results['ft-sec-trace-002'].status }} | {{ results['ft-sec-trace-002'].trend_display }} | {{ results['ft-sec-trace-002'].evidence \| default('—') }} |
| ft-sec-trace-003 | Links to downstream implementation | warning (recommended) | 0.5 | {{ results['ft-sec-trace-003'].previous_status \| default('—') }} | {{ results['ft-sec-trace-003'].status }} | {{ results['ft-sec-trace-003'].trend_display }} | {{ results['ft-sec-trace-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 17 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | feature-technical |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/10-feature-technical/*.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
