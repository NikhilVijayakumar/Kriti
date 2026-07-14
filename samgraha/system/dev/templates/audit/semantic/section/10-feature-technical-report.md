# Semantic Section Report — Feature Technical

**Document:** {{ document_path }}
**Standard:** `documentation-standards/10-feature-technical-standards.md`
**Rubric Files:** `audit/semantic/section/10-feature-technical/*.md`
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
| 2 | Participating Components | **required** | {{ sections.participating_components.score }} / 100 | {{ sections.participating_components.previous_score | default('—') }} | {{ sections.participating_components.trend_display }} |
| 3 | Component Interactions | **required** | {{ sections.component_interactions.score }} / 100 | {{ sections.component_interactions.previous_score | default('—') }} | {{ sections.component_interactions.trend_display }} |
| 4 | Data Ownership | **required** | {{ sections.data_ownership.score }} / 100 | {{ sections.data_ownership.previous_score | default('—') }} | {{ sections.data_ownership.trend_display }} |
| 5 | Feature Specification | optional | {{ sections.feature_specification.score }} / 100 | {{ sections.feature_specification.previous_score | default('—') }} | {{ sections.feature_specification.trend_display }} |
| 6 | Component Responsibilities | optional | {{ sections.component_responsibilities.score }} / 100 | {{ sections.component_responsibilities.previous_score | default('—') }} | {{ sections.component_responsibilities.trend_display }} |
| 7 | Runtime Behavior | optional | {{ sections.runtime_behavior.score }} / 100 | {{ sections.runtime_behavior.previous_score | default('—') }} | {{ sections.runtime_behavior.trend_display }} |
| 8 | Communication Paths | optional | {{ sections.communication_paths.score }} / 100 | {{ sections.communication_paths.previous_score | default('—') }} | {{ sections.communication_paths.trend_display }} |
| 9 | Integration Points | optional | {{ sections.integration_points.score }} / 100 | {{ sections.integration_points.previous_score | default('—') }} | {{ sections.integration_points.trend_display }} |
| 10 | External Dependencies | optional | {{ sections.external_dependencies.score }} / 100 | {{ sections.external_dependencies.previous_score | default('—') }} | {{ sections.external_dependencies.trend_display }} |
| 11 | Runtime Constraints | optional | {{ sections.runtime_constraints.score }} / 100 | {{ sections.runtime_constraints.previous_score | default('—') }} | {{ sections.runtime_constraints.trend_display }} |
| 12 | Architectural Constraints | optional | {{ sections.architectural_constraints.score }} / 100 | {{ sections.architectural_constraints.previous_score | default('—') }} | {{ sections.architectural_constraints.trend_display }} |
| 13 | Security Considerations | optional | {{ sections.security_considerations.score }} / 100 | {{ sections.security_considerations.previous_score | default('—') }} | {{ sections.security_considerations.trend_display }} |
| 14 | Performance Considerations | optional | {{ sections.performance_considerations.score }} / 100 | {{ sections.performance_considerations.previous_score | default('—') }} | {{ sections.performance_considerations.trend_display }} |
| 15 | Failure Handling | optional | {{ sections.failure_handling.score }} / 100 | {{ sections.failure_handling.previous_score | default('—') }} | {{ sections.failure_handling.trend_display }} |
| 16 | Extension Points | optional | {{ sections.extension_points.score }} / 100 | {{ sections.extension_points.previous_score | default('—') }} | {{ sections.extension_points.trend_display }} |
| 17 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |
| — | Generic (unmatched sections) | n/a | {{ sections.generic.score }} / 100 | {{ sections.generic.previous_score | default('—') }} | {{ sections.generic.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Purpose — `section/10-feature-technical/01-purpose.md` — **required**

**Why this matters:** Purpose defines why Feature Technical Documentation exists. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display | default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display | default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display | default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt | default('—') }} |

C1: technical problem and motivation clearly stated. C2: engineering value proposition articulated. C3: success criteria for technical impact defined.

## 2. Participating Components — `02-participating_components.md` — **required**

**Why this matters:** Participating Components is the inventory of every module, service, or sub-system involved in the feature. A missing or incomplete list means downstream sections reference components that were never formally introduced.

**Section Score: {{ sections.participating_components.score }} / 100** ({{ sections.participating_components.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['participating_components.C1'].previous_passed_display | default('—') }} | {{ results['participating_components.C1'].passed_display }} | {{ results['participating_components.C1'].trend_display }} | {{ results['participating_components.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['participating_components.C2'].previous_passed_display | default('—') }} | {{ results['participating_components.C2'].passed_display }} | {{ results['participating_components.C2'].trend_display }} | {{ results['participating_components.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['participating_components.C3'].previous_passed_display | default('—') }} | {{ results['participating_components.C3'].passed_display }} | {{ results['participating_components.C3'].trend_display }} | {{ results['participating_components.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['participating_components.C4'].previous_passed_display | default('—') }} | {{ results['participating_components.C4'].passed_display }} | {{ results['participating_components.C4'].trend_display }} | {{ results['participating_components.C4'].evidence.excerpt | default('—') }} |

C1: all participating components enumerated. C2: deployment unit specified per component. C3: each component has a defined feature role. C4: state model documented per component.

## 3. Component Interactions — `03-component_interactions.md` — **required**

**Why this matters:** Component Interactions describes how components communicate and depend on each other. Without it, readers cannot understand the feature's data flow, call patterns, or coupling characteristics.

**Section Score: {{ sections.component_interactions.score }} / 100** ({{ sections.component_interactions.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['component_interactions.C1'].previous_passed_display | default('—') }} | {{ results['component_interactions.C1'].passed_display }} | {{ results['component_interactions.C1'].trend_display }} | {{ results['component_interactions.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['component_interactions.C2'].previous_passed_display | default('—') }} | {{ results['component_interactions.C2'].passed_display }} | {{ results['component_interactions.C2'].trend_display }} | {{ results['component_interactions.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['component_interactions.C3'].previous_passed_display | default('—') }} | {{ results['component_interactions.C3'].passed_display }} | {{ results['component_interactions.C3'].trend_display }} | {{ results['component_interactions.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['component_interactions.C4'].previous_passed_display | default('—') }} | {{ results['component_interactions.C4'].passed_display }} | {{ results['component_interactions.C4'].trend_display }} | {{ results['component_interactions.C4'].evidence.excerpt | default('—') }} |

C1: all component interactions identified. C2: each interaction specifies direction and communication type. C3: no undocumented cyclic dependencies. C4: data contracts or interfaces referenced per interaction.

## 4. Data Ownership — `04-data_ownership.md` — **required**

**Why this matters:** Data Ownership assigns authoritative ownership for each data entity. Without it, multiple components may silently write to the same data, creating consistency bugs.

**Section Score: {{ sections.data_ownership.score }} / 100** ({{ sections.data_ownership.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['data_ownership.C1'].previous_passed_display | default('—') }} | {{ results['data_ownership.C1'].passed_display }} | {{ results['data_ownership.C1'].trend_display }} | {{ results['data_ownership.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['data_ownership.C2'].previous_passed_display | default('—') }} | {{ results['data_ownership.C2'].passed_display }} | {{ results['data_ownership.C2'].trend_display }} | {{ results['data_ownership.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['data_ownership.C3'].previous_passed_display | default('—') }} | {{ results['data_ownership.C3'].passed_display }} | {{ results['data_ownership.C3'].trend_display }} | {{ results['data_ownership.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['data_ownership.C4'].previous_passed_display | default('—') }} | {{ results['data_ownership.C4'].passed_display }} | {{ results['data_ownership.C4'].trend_display }} | {{ results['data_ownership.C4'].evidence.excerpt | default('—') }} |

C1: all data entities have designated owners. C2: write authority is assigned and non-conflicting. C3: data lifecycle documented per entity. C4: data retention and purging policies defined.

## 5. Feature Specification — `05-feature_specification.md` — optional

**Why this matters:** Feature Specification defines the technical boundaries, inputs, outputs, and behavioral contract. Without it, Implementation has no declarative contract to code against.

**Section Score: {{ sections.feature_specification.score }} / 100** ({{ sections.feature_specification.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['feature_specification.C1'].previous_passed_display | default('—') }} | {{ results['feature_specification.C1'].passed_display }} | {{ results['feature_specification.C1'].trend_display }} | {{ results['feature_specification.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['feature_specification.C2'].previous_passed_display | default('—') }} | {{ results['feature_specification.C2'].passed_display }} | {{ results['feature_specification.C2'].trend_display }} | {{ results['feature_specification.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['feature_specification.C3'].previous_passed_display | default('—') }} | {{ results['feature_specification.C3'].passed_display }} | {{ results['feature_specification.C3'].trend_display }} | {{ results['feature_specification.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['feature_specification.C4'].previous_passed_display | default('—') }} | {{ results['feature_specification.C4'].passed_display }} | {{ results['feature_specification.C4'].trend_display }} | {{ results['feature_specification.C4'].evidence.excerpt | default('—') }} |

C1: feature scope with inclusion and exclusion criteria. C2: preconditions and postconditions defined. C3: input and output specifications with types. C4: feature-level invariants documented.

## 6. Component Responsibilities — `06-component_responsibilities.md` — optional

**Why this matters:** Component Responsibilities defines what each participating component owns, preventing overlap and gaps in accountability.

**Section Score: {{ sections.component_responsibilities.score }} / 100** ({{ sections.component_responsibilities.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['component_responsibilities.C1'].previous_passed_display | default('—') }} | {{ results['component_responsibilities.C1'].passed_display }} | {{ results['component_responsibilities.C1'].trend_display }} | {{ results['component_responsibilities.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['component_responsibilities.C2'].previous_passed_display | default('—') }} | {{ results['component_responsibilities.C2'].passed_display }} | {{ results['component_responsibilities.C2'].trend_display }} | {{ results['component_responsibilities.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['component_responsibilities.C3'].previous_passed_display | default('—') }} | {{ results['component_responsibilities.C3'].passed_display }} | {{ results['component_responsibilities.C3'].trend_display }} | {{ results['component_responsibilities.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['component_responsibilities.C4'].previous_passed_display | default('—') }} | {{ results['component_responsibilities.C4'].passed_display }} | {{ results['component_responsibilities.C4'].trend_display }} | {{ results['component_responsibilities.C4'].evidence.excerpt | default('—') }} |

C1: all components have explicit responsibility statements. C2: no overlapping responsibilities across components. C3: each component has a primary single responsibility. C4: gap analysis performed for uncovered capabilities.

## 7. Runtime Behavior — `07-runtime_behavior.md` — optional

**Why this matters:** Runtime Behavior describes the feature's operational execution model — startup, steady-state, state transitions, and shutdown. Without it, Implementation cannot determine the correct lifecycle sequence.

**Section Score: {{ sections.runtime_behavior.score }} / 100** ({{ sections.runtime_behavior.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['runtime_behavior.C1'].previous_passed_display | default('—') }} | {{ results['runtime_behavior.C1'].passed_display }} | {{ results['runtime_behavior.C1'].trend_display }} | {{ results['runtime_behavior.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['runtime_behavior.C2'].previous_passed_display | default('—') }} | {{ results['runtime_behavior.C2'].passed_display }} | {{ results['runtime_behavior.C2'].trend_display }} | {{ results['runtime_behavior.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['runtime_behavior.C3'].previous_passed_display | default('—') }} | {{ results['runtime_behavior.C3'].passed_display }} | {{ results['runtime_behavior.C3'].trend_display }} | {{ results['runtime_behavior.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['runtime_behavior.C4'].previous_passed_display | default('—') }} | {{ results['runtime_behavior.C4'].passed_display }} | {{ results['runtime_behavior.C4'].trend_display }} | {{ results['runtime_behavior.C4'].evidence.excerpt | default('—') }} |

C1: startup and shutdown sequences documented. C2: state transitions with triggers enumerated. C3: concurrency and threading model described. C4: observable side effects listed.

## 8. Communication Paths — `08-communication_paths.md` — optional

**Why this matters:** Communication Paths documents the data flow topology — message routing, delivery guarantees, and backpressure handling. Without it, readers cannot assess whether data arrives reliably.

**Section Score: {{ sections.communication_paths.score }} / 100** ({{ sections.communication_paths.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['communication_paths.C1'].previous_passed_display | default('—') }} | {{ results['communication_paths.C1'].passed_display }} | {{ results['communication_paths.C1'].trend_display }} | {{ results['communication_paths.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['communication_paths.C2'].previous_passed_display | default('—') }} | {{ results['communication_paths.C2'].passed_display }} | {{ results['communication_paths.C2'].trend_display }} | {{ results['communication_paths.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['communication_paths.C3'].previous_passed_display | default('—') }} | {{ results['communication_paths.C3'].passed_display }} | {{ results['communication_paths.C3'].trend_display }} | {{ results['communication_paths.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['communication_paths.C4'].previous_passed_display | default('—') }} | {{ results['communication_paths.C4'].passed_display }} | {{ results['communication_paths.C4'].trend_display }} | {{ results['communication_paths.C4'].evidence.excerpt | default('—') }} |

C1: all communication paths enumerated source-to-sink. C2: delivery guarantees defined per path. C3: backpressure or flow control documented. C4: serialization format specified per path.

## 9. Integration Points — `09-integration_points.md` — optional

**Why this matters:** Integration Points document every boundary where the feature connects to external systems. Without it, implementation teams may miss integration contracts.

**Section Score: {{ sections.integration_points.score }} / 100** ({{ sections.integration_points.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['integration_points.C1'].previous_passed_display | default('—') }} | {{ results['integration_points.C1'].passed_display }} | {{ results['integration_points.C1'].trend_display }} | {{ results['integration_points.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['integration_points.C2'].previous_passed_display | default('—') }} | {{ results['integration_points.C2'].passed_display }} | {{ results['integration_points.C2'].trend_display }} | {{ results['integration_points.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['integration_points.C3'].previous_passed_display | default('—') }} | {{ results['integration_points.C3'].passed_display }} | {{ results['integration_points.C3'].trend_display }} | {{ results['integration_points.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['integration_points.C4'].previous_passed_display | default('—') }} | {{ results['integration_points.C4'].passed_display }} | {{ results['integration_points.C4'].trend_display }} | {{ results['integration_points.C4'].evidence.excerpt | default('—') }} |

C1: all integration points enumerated with external system. C2: interface contract specified per integration point. C3: error contract documented per boundary. C4: SLA parameters defined for each integration point.

## 10. External Dependencies — `10-external_dependencies.md` — optional

**Why this matters:** External Dependencies capture every third-party library, service, or infrastructure the feature relies on. Without it, version conflicts and license issues surface only in production.

**Section Score: {{ sections.external_dependencies.score }} / 100** ({{ sections.external_dependencies.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['external_dependencies.C1'].previous_passed_display | default('—') }} | {{ results['external_dependencies.C1'].passed_display }} | {{ results['external_dependencies.C1'].trend_display }} | {{ results['external_dependencies.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['external_dependencies.C2'].previous_passed_display | default('—') }} | {{ results['external_dependencies.C2'].passed_display }} | {{ results['external_dependencies.C2'].trend_display }} | {{ results['external_dependencies.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['external_dependencies.C3'].previous_passed_display | default('—') }} | {{ results['external_dependencies.C3'].passed_display }} | {{ results['external_dependencies.C3'].trend_display }} | {{ results['external_dependencies.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['external_dependencies.C4'].previous_passed_display | default('—') }} | {{ results['external_dependencies.C4'].passed_display }} | {{ results['external_dependencies.C4'].trend_display }} | {{ results['external_dependencies.C4'].evidence.excerpt | default('—') }} |

C1: all external dependencies enumerated with version. C2: integration method documented for each dependency. C3: license compatibility verified. C4: no dependencies with known unresolved CVEs.

## 11. Runtime Constraints — `11-runtime_constraints.md` — optional

**Why this matters:** Runtime Constraints specify measurable resource limits the feature must operate within. Without numeric thresholds, performance requirements are ambiguous and unverifiable.

**Section Score: {{ sections.runtime_constraints.score }} / 100** ({{ sections.runtime_constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['runtime_constraints.C1'].previous_passed_display | default('—') }} | {{ results['runtime_constraints.C1'].passed_display }} | {{ results['runtime_constraints.C1'].trend_display }} | {{ results['runtime_constraints.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['runtime_constraints.C2'].previous_passed_display | default('—') }} | {{ results['runtime_constraints.C2'].passed_display }} | {{ results['runtime_constraints.C2'].trend_display }} | {{ results['runtime_constraints.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['runtime_constraints.C3'].previous_passed_display | default('—') }} | {{ results['runtime_constraints.C3'].passed_display }} | {{ results['runtime_constraints.C3'].trend_display }} | {{ results['runtime_constraints.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['runtime_constraints.C4'].previous_passed_display | default('—') }} | {{ results['runtime_constraints.C4'].passed_display }} | {{ results['runtime_constraints.C4'].trend_display }} | {{ results['runtime_constraints.C4'].evidence.excerpt | default('—') }} |

C1: all runtime constraints enumerated with numeric thresholds. C2: measurement units specified per constraint. C3: normal vs burst mode constraints distinguished. C4: hard and soft limits clearly differentiated.

## 12. Architectural Constraints — `12-architectural_constraints.md` — optional

**Why this matters:** Architectural Constraints define the non-negotiable design rules the feature must adhere to. Without them, implementation may violate upstream architectural principles.

**Section Score: {{ sections.architectural_constraints.score }} / 100** ({{ sections.architectural_constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['architectural_constraints.C1'].previous_passed_display | default('—') }} | {{ results['architectural_constraints.C1'].passed_display }} | {{ results['architectural_constraints.C1'].trend_display }} | {{ results['architectural_constraints.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['architectural_constraints.C2'].previous_passed_display | default('—') }} | {{ results['architectural_constraints.C2'].passed_display }} | {{ results['architectural_constraints.C2'].trend_display }} | {{ results['architectural_constraints.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['architectural_constraints.C3'].previous_passed_display | default('—') }} | {{ results['architectural_constraints.C3'].passed_display }} | {{ results['architectural_constraints.C3'].trend_display }} | {{ results['architectural_constraints.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['architectural_constraints.C4'].previous_passed_display | default('—') }} | {{ results['architectural_constraints.C4'].passed_display }} | {{ results['architectural_constraints.C4'].trend_display }} | {{ results['architectural_constraints.C4'].evidence.excerpt | default('—') }} |

C1: all architectural constraints enumerated. C2: dependency direction rules specified. C3: layer isolation rules defined. C4: each constraint linked to an ADR or rationale.

## 13. Security Considerations — `13-security_considerations.md` — optional

**Why this matters:** Security Considerations document the threat model, authentication, authorization, and data protection. Without them, security is treated as an afterthought.

**Section Score: {{ sections.security_considerations.score }} / 100** ({{ sections.security_considerations.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 25 | {{ results['security_considerations.C1'].previous_passed_display | default('—') }} | {{ results['security_considerations.C1'].passed_display }} | {{ results['security_considerations.C1'].trend_display }} | {{ results['security_considerations.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 25 | {{ results['security_considerations.C2'].previous_passed_display | default('—') }} | {{ results['security_considerations.C2'].passed_display }} | {{ results['security_considerations.C2'].trend_display }} | {{ results['security_considerations.C2'].evidence.excerpt | default('—') }} |
| C3 | mandatory | 25 | {{ results['security_considerations.C3'].previous_passed_display | default('—') }} | {{ results['security_considerations.C3'].passed_display }} | {{ results['security_considerations.C3'].trend_display }} | {{ results['security_considerations.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 25 | {{ results['security_considerations.C4'].previous_passed_display | default('—') }} | {{ results['security_considerations.C4'].passed_display }} | {{ results['security_considerations.C4'].trend_display }} | {{ results['security_considerations.C4'].evidence.excerpt | default('—') }} |

C1: threat model documents threats with mitigations (STRIDE/OWASP Top 10 mapping). C2: authentication and authorization model documented. C3: input validation names specific attack vectors (XSS, SQLi, command injection). C4: data protection (transit and at rest) and audit logging defined.

## 14. Performance Considerations — `14-performance_considerations.md` — optional

**Why this matters:** Performance Considerations document latency targets, throughput requirements, and resource utilization. Without them, performance expectations are undocumented and unverifiable.

**Section Score: {{ sections.performance_considerations.score }} / 100** ({{ sections.performance_considerations.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['performance_considerations.C1'].previous_passed_display | default('—') }} | {{ results['performance_considerations.C1'].passed_display }} | {{ results['performance_considerations.C1'].trend_display }} | {{ results['performance_considerations.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['performance_considerations.C2'].previous_passed_display | default('—') }} | {{ results['performance_considerations.C2'].passed_display }} | {{ results['performance_considerations.C2'].trend_display }} | {{ results['performance_considerations.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['performance_considerations.C3'].previous_passed_display | default('—') }} | {{ results['performance_considerations.C3'].passed_display }} | {{ results['performance_considerations.C3'].trend_display }} | {{ results['performance_considerations.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['performance_considerations.C4'].previous_passed_display | default('—') }} | {{ results['performance_considerations.C4'].passed_display }} | {{ results['performance_considerations.C4'].trend_display }} | {{ results['performance_considerations.C4'].evidence.excerpt | default('—') }} |

C1: latency targets with percentile levels specified. C2: throughput and concurrency limits defined. C3: resource utilization profile per transaction. C4: caching strategy with invalidation documented.

## 15. Failure Handling — `15-failure_handling.md` — optional

**Why this matters:** Failure Handling documents how the feature detects, responds to, and recovers from errors. Without it, error handling is inconsistent across components.

**Section Score: {{ sections.failure_handling.score }} / 100** ({{ sections.failure_handling.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['failure_handling.C1'].previous_passed_display | default('—') }} | {{ results['failure_handling.C1'].passed_display }} | {{ results['failure_handling.C1'].trend_display }} | {{ results['failure_handling.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['failure_handling.C2'].previous_passed_display | default('—') }} | {{ results['failure_handling.C2'].passed_display }} | {{ results['failure_handling.C2'].trend_display }} | {{ results['failure_handling.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['failure_handling.C3'].previous_passed_display | default('—') }} | {{ results['failure_handling.C3'].passed_display }} | {{ results['failure_handling.C3'].trend_display }} | {{ results['failure_handling.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['failure_handling.C4'].previous_passed_display | default('—') }} | {{ results['failure_handling.C4'].passed_display }} | {{ results['failure_handling.C4'].trend_display }} | {{ results['failure_handling.C4'].evidence.excerpt | default('—') }} |

C1: all failure modes enumerated with detection mechanism. C2: retry policy defined per failure mode. C3: fallback or degradation behavior documented. C4: data consistency guarantees stated for failure scenarios.

## 16. Extension Points — `16-extension_points.md` — optional

**Why this matters:** Extension Points document where the feature can be customized or extended. Without them, consumers cannot safely extend the feature without risking breakage.

**Section Score: {{ sections.extension_points.score }} / 100** ({{ sections.extension_points.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['extension_points.C1'].previous_passed_display | default('—') }} | {{ results['extension_points.C1'].passed_display }} | {{ results['extension_points.C1'].trend_display }} | {{ results['extension_points.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['extension_points.C2'].previous_passed_display | default('—') }} | {{ results['extension_points.C2'].passed_display }} | {{ results['extension_points.C2'].trend_display }} | {{ results['extension_points.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['extension_points.C3'].previous_passed_display | default('—') }} | {{ results['extension_points.C3'].passed_display }} | {{ results['extension_points.C3'].trend_display }} | {{ results['extension_points.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['extension_points.C4'].previous_passed_display | default('—') }} | {{ results['extension_points.C4'].passed_display }} | {{ results['extension_points.C4'].trend_display }} | {{ results['extension_points.C4'].evidence.excerpt | default('—') }} |

C1: all extension points enumerated with interface signature. C2: extension mechanism and registration described. C3: stability guarantees and deprecation policy documented. C4: default behavior for unextended feature defined.

## 17. Traceability — `17-traceability.md` — optional

**Why this matters:** Traceability documents the links between feature requirements, design decisions, and implementation artifacts. Without it, impact analysis is impossible.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['traceability.C1'].previous_passed_display | default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display | default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['traceability.C3'].previous_passed_display | default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['traceability.C4'].previous_passed_display | default('—') }} | {{ results['traceability.C4'].passed_display }} | {{ results['traceability.C4'].trend_display }} | {{ results['traceability.C4'].evidence.excerpt | default('—') }} |

C1: bidirectional trace between requirements and components. C2: all tests mapped to requirements or specifications. C3: design decisions linked to ADR documents. C4: gaps and untraced elements explicitly documented.

## Generic — `generic.md` (sections with no matching semantic_type)

**Why this matters:** Catches feature-technical content an author wrote under a heading that doesn't match any of the 17 named section types above — still judged for relevance and non-duplication, not given a free pass for being unclassified.

**Section Score: {{ sections.generic.score }} / 100** ({{ sections.generic.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['generic.C1'].previous_passed_display | default('—') }} | {{ results['generic.C1'].passed_display }} | {{ results['generic.C1'].trend_display }} | {{ results['generic.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['generic.C2'].previous_passed_display | default('—') }} | {{ results['generic.C2'].passed_display }} | {{ results['generic.C2'].trend_display }} | {{ results['generic.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['generic.C3'].previous_passed_display | default('—') }} | {{ results['generic.C3'].passed_display }} | {{ results['generic.C3'].trend_display }} | {{ results['generic.C3'].evidence.excerpt | default('—') }} |

C1: content is relevant to the feature-technical domain. C2: no duplication with other named sections. C3: all claims are verifiable and specific.

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
| Domain | feature-technical |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/10-feature-technical/*.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
