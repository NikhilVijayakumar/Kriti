# Semantic Section Report — Architecture

**Document:** {{ document_path }}
**Standard:** `documentation-standards/05-architecture-standards.md`
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
| 1 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 2 | System Overview | **required** | {{ sections.system_overview.score }} / 100 | {{ sections.system_overview.previous_score | default('—') }} | {{ sections.system_overview.trend_display }} |
| 3 | Component Model | **required** | {{ sections.component_model.score }} / 100 | {{ sections.component_model.previous_score | default('—') }} | {{ sections.component_model.trend_display }} |
| 4 | Communication Paths | **required** | {{ sections.communication_paths.score }} / 100 | {{ sections.communication_paths.previous_score | default('—') }} | {{ sections.communication_paths.trend_display }} |
| 5 | Data Flow | **required** | {{ sections.data_flow.score }} / 100 | {{ sections.data_flow.previous_score | default('—') }} | {{ sections.data_flow.trend_display }} |
| 6 | Security Considerations | **required** | {{ sections.security_considerations.score }} / 100 | {{ sections.security_considerations.previous_score | default('—') }} | {{ sections.security_considerations.trend_display }} |
| 7 | Rationale | optional | {{ sections.rationale.score }} / 100 | {{ sections.rationale.previous_score | default('—') }} | {{ sections.rationale.trend_display }} |
| 8 | Constraints | optional | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 9 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |
| 10 | Operational Readiness | not in standard | {{ sections.operational_readiness.score }} / 100 | {{ sections.operational_readiness.previous_score | default('—') }} | {{ sections.operational_readiness.trend_display }} |
| 11 | Observability | not in standard | {{ sections.observability.score }} / 100 | {{ sections.observability.previous_score | default('—') }} | {{ sections.observability.trend_display }} |
| — | Generic (unmatched sections) | n/a | {{ sections.generic.score }} / 100 | {{ sections.generic.previous_score | default('—') }} | {{ sections.generic.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Purpose — `section/05-architecture/01-purpose.md`

**Why this matters:** Defines the architectural intent, scope, and key qualities the system optimizes for. A clear purpose is what lets a reader evaluate whether every later architectural decision actually fits.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: architectural purpose is clearly stated with scope boundaries. C2: primary architectural goals and their priorities are defined. C3: purpose is consistent with requirements and downstream sections.

## 2. System Overview — `02-system_overview.md` — **required**

**Why this matters:** The entry point for understanding the whole architecture — system purpose, deployment context, architectural style, and relationship to external systems, all in one place before the reader goes section by section.

**Section Score: {{ sections.system_overview.score }} / 100** ({{ sections.system_overview.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['system_overview.C1'].previous_passed_display \| default('—') }} | {{ results['system_overview.C1'].passed_display }} | {{ results['system_overview.C1'].trend_display }} | {{ results['system_overview.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['system_overview.C2'].previous_passed_display \| default('—') }} | {{ results['system_overview.C2'].passed_display }} | {{ results['system_overview.C2'].trend_display }} | {{ results['system_overview.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['system_overview.C3'].previous_passed_display \| default('—') }} | {{ results['system_overview.C3'].passed_display }} | {{ results['system_overview.C3'].trend_display }} | {{ results['system_overview.C3'].evidence.excerpt \| default('—') }} |

C1: system purpose and architectural style are clearly described. C2: deployment context and external dependencies are identified. C3: overview is consistent with the detailed sections that follow it.

## 3. Component Model — `03-component_model.md` — **required**

**Why this matters:** Identifies the major structural elements — every component needs a clear responsibility, defined interfaces, and known dependencies, or nothing downstream (Communication Paths, Data Flow) has a stable foundation to reference.

**Section Score: {{ sections.component_model.score }} / 100** ({{ sections.component_model.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['component_model.C1'].previous_passed_display \| default('—') }} | {{ results['component_model.C1'].passed_display }} | {{ results['component_model.C1'].trend_display }} | {{ results['component_model.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['component_model.C2'].previous_passed_display \| default('—') }} | {{ results['component_model.C2'].passed_display }} | {{ results['component_model.C2'].trend_display }} | {{ results['component_model.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 20 | {{ results['component_model.C3'].previous_passed_display \| default('—') }} | {{ results['component_model.C3'].passed_display }} | {{ results['component_model.C3'].trend_display }} | {{ results['component_model.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['component_model.C4'].previous_passed_display \| default('—') }} | {{ results['component_model.C4'].passed_display }} | {{ results['component_model.C4'].trend_display }} | {{ results['component_model.C4'].evidence.excerpt \| default('—') }} |

C1: all system components identified. C2: each component has a clear responsibility. C3: interfaces between components documented. C4: no overlapping component responsibilities.

## 4. Communication Paths — `04-communication_paths.md` — **required**

**Why this matters:** Defines how components actually interact — directionality, protocol, synchronization model, quality-of-service — precisely enough that integration testing and failure-mode analysis are possible from the document alone.

**Section Score: {{ sections.communication_paths.score }} / 100** ({{ sections.communication_paths.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['communication_paths.C1'].previous_passed_display \| default('—') }} | {{ results['communication_paths.C1'].passed_display }} | {{ results['communication_paths.C1'].trend_display }} | {{ results['communication_paths.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['communication_paths.C2'].previous_passed_display \| default('—') }} | {{ results['communication_paths.C2'].passed_display }} | {{ results['communication_paths.C2'].trend_display }} | {{ results['communication_paths.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['communication_paths.C3'].previous_passed_display \| default('—') }} | {{ results['communication_paths.C3'].passed_display }} | {{ results['communication_paths.C3'].trend_display }} | {{ results['communication_paths.C3'].evidence.excerpt \| default('—') }} |

C1: all inter-component paths identified with protocol and direction. C2: synchronization model and quality-of-service defined per path. C3: error handling and retry strategies documented.

## 5. Data Flow — `05-data_flow.md` — **required**

**Why this matters:** Data flow is what makes impact analysis and data governance possible — schemas, direction, processing semantics, and lineage need to be traceable from this section, not reverse-engineered from the code later.

**Section Score: {{ sections.data_flow.score }} / 100** ({{ sections.data_flow.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['data_flow.C1'].previous_passed_display \| default('—') }} | {{ results['data_flow.C1'].passed_display }} | {{ results['data_flow.C1'].trend_display }} | {{ results['data_flow.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['data_flow.C2'].previous_passed_display \| default('—') }} | {{ results['data_flow.C2'].passed_display }} | {{ results['data_flow.C2'].trend_display }} | {{ results['data_flow.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['data_flow.C3'].previous_passed_display \| default('—') }} | {{ results['data_flow.C3'].passed_display }} | {{ results['data_flow.C3'].trend_display }} | {{ results['data_flow.C3'].evidence.excerpt \| default('—') }} |

C1: all major data flows identified with sources and sinks. C2: processing semantics (sync/async, batch/stream) defined. C3: data transformations and storage boundaries documented.

## 6. Security Considerations — `06-security_considerations.md` — **required**

**Why this matters:** Threat model boundaries, trust zones, and auth flows need to be identified with risks explicitly mapped to mitigations — a security section that describes controls without naming the threats they mitigate hasn't actually done threat modeling.

**Section Score: {{ sections.security_considerations.score }} / 100** ({{ sections.security_considerations.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['security_considerations.C1'].previous_passed_display \| default('—') }} | {{ results['security_considerations.C1'].passed_display }} | {{ results['security_considerations.C1'].trend_display }} | {{ results['security_considerations.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['security_considerations.C2'].previous_passed_display \| default('—') }} | {{ results['security_considerations.C2'].passed_display }} | {{ results['security_considerations.C2'].trend_display }} | {{ results['security_considerations.C2'].evidence.excerpt \| default('—') }} |
| C3 | mandatory | 20 | {{ results['security_considerations.C3'].previous_passed_display \| default('—') }} | {{ results['security_considerations.C3'].passed_display }} | {{ results['security_considerations.C3'].trend_display }} | {{ results['security_considerations.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['security_considerations.C4'].previous_passed_display \| default('—') }} | {{ results['security_considerations.C4'].passed_display }} | {{ results['security_considerations.C4'].trend_display }} | {{ results['security_considerations.C4'].evidence.excerpt \| default('—') }} |

C1: trust boundaries and attack surface enumerated. C2: threat model uses a structured methodology (STRIDE/PASTA/OWASP) with threats mapped to mitigations. C3: authentication and authorization mechanisms described. C4: data protection at rest and in transit addressed per classification.

## 7. Rationale — `07-rationale.md`

**Why this matters:** Preserves why the architecture looks the way it does — tied to an architectural goal, not a technology preference — so a future maintainer can tell "deliberate" apart from "arbitrary."

**Section Score: {{ sections.rationale.score }} / 100** ({{ sections.rationale.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['rationale.C1'].previous_passed_display \| default('—') }} | {{ results['rationale.C1'].passed_display }} | {{ results['rationale.C1'].trend_display }} | {{ results['rationale.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['rationale.C2'].previous_passed_display \| default('—') }} | {{ results['rationale.C2'].passed_display }} | {{ results['rationale.C2'].trend_display }} | {{ results['rationale.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['rationale.C3'].previous_passed_display \| default('—') }} | {{ results['rationale.C3'].passed_display }} | {{ results['rationale.C3'].trend_display }} | {{ results['rationale.C3'].evidence.excerpt \| default('—') }} |

C1: each entry has Context, Decision, Alternatives Considered, and Rejection Reason. C2: rejection reason is architectural, not implementation/technology-level. C3: every decision ties to a named architectural goal or pillar.

## 8. Constraints — `08-constraints.md`

**Why this matters:** Architectural constraints are non-negotiable, system-wide properties driven by architectural decisions — distinct from feature-level constraints, and useless if nobody can tell which constraints are actually load-bearing.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['constraints.C1'].previous_passed_display \| default('—') }} | {{ results['constraints.C1'].passed_display }} | {{ results['constraints.C1'].trend_display }} | {{ results['constraints.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['constraints.C2'].previous_passed_display \| default('—') }} | {{ results['constraints.C2'].passed_display }} | {{ results['constraints.C2'].trend_display }} | {{ results['constraints.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['constraints.C3'].previous_passed_display \| default('—') }} | {{ results['constraints.C3'].passed_display }} | {{ results['constraints.C3'].trend_display }} | {{ results['constraints.C3'].evidence.excerpt \| default('—') }} |

C1: constraints are architectural, not implementation-specific. C2: each constraint has a documented justification. C3: no contradictory constraints.

## 9. Traceability — `09-traceability.md`

**Why this matters:** Maps architecture decisions back to requirements and forward to implementation, so no requirement is silently lost between specification and design, and impact analysis is actually possible.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['traceability.C1'].previous_passed_display \| default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display \| default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['traceability.C3'].previous_passed_display \| default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt \| default('—') }} |

C1: architecture elements are traceable to source requirements or decisions. C2: cross-references between architecture sections are present and resolvable. C3: decision records (ADR) referenced with stable numeric or slug IDs, not title-only.

## 10. Operational Readiness — `10-operational_readiness.md` — not in Required Sections table

**Why this matters:** Ensures the system can be deployed, operated, scaled, and recovered by teams who didn't build it — deployment automation, rollback procedures, runbooks, and DR plans, documented rather than tribal knowledge.

**Section Score: {{ sections.operational_readiness.score }} / 100** ({{ sections.operational_readiness.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['operational_readiness.C1'].previous_passed_display \| default('—') }} | {{ results['operational_readiness.C1'].passed_display }} | {{ results['operational_readiness.C1'].trend_display }} | {{ results['operational_readiness.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['operational_readiness.C2'].previous_passed_display \| default('—') }} | {{ results['operational_readiness.C2'].passed_display }} | {{ results['operational_readiness.C2'].trend_display }} | {{ results['operational_readiness.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 20 | {{ results['operational_readiness.C3'].previous_passed_display \| default('—') }} | {{ results['operational_readiness.C3'].passed_display }} | {{ results['operational_readiness.C3'].trend_display }} | {{ results['operational_readiness.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['operational_readiness.C4'].previous_passed_display \| default('—') }} | {{ results['operational_readiness.C4'].passed_display }} | {{ results['operational_readiness.C4'].trend_display }} | {{ results['operational_readiness.C4'].evidence.excerpt \| default('—') }} |

C1: deployment automation and production promotion gating documented. C2: rollback procedure defined with a time target. C3: runbooks linked per failure mode with on-call routing. C4: RTO/RPO targets and DR plan documented.

## 11. Observability — `11-observability.md` — not in Required Sections table

**Why this matters:** Defines the observability infrastructure itself — telemetry backend, trace collection pattern, metrics retention, correlation ID strategy — so any feature's instrumentation has somewhere real to land.

**Section Score: {{ sections.observability.score }} / 100** ({{ sections.observability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['observability.C1'].previous_passed_display \| default('—') }} | {{ results['observability.C1'].passed_display }} | {{ results['observability.C1'].trend_display }} | {{ results['observability.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['observability.C2'].previous_passed_display \| default('—') }} | {{ results['observability.C2'].passed_display }} | {{ results['observability.C2'].trend_display }} | {{ results['observability.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['observability.C3'].previous_passed_display \| default('—') }} | {{ results['observability.C3'].passed_display }} | {{ results['observability.C3'].trend_display }} | {{ results['observability.C3'].evidence.excerpt \| default('—') }} |

C1: telemetry backend identified and correlation ID strategy documented. C2: log aggregation pipeline with retention policy described. C3: SLO monitoring architecture and on-call routing documented.

## Generic — `generic.md` (sections with no matching semantic_type)

**Why this matters:** Catches architecture-relevant content an author wrote under a heading that doesn't match any of the 11 named section types above — still judged for relevance and non-duplication, not given a free pass for being unclassified.

**Section Score: {{ sections.generic.score }} / 100** ({{ sections.generic.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['generic.C1'].previous_passed_display \| default('—') }} | {{ results['generic.C1'].passed_display }} | {{ results['generic.C1'].trend_display }} | {{ results['generic.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['generic.C2'].previous_passed_display \| default('—') }} | {{ results['generic.C2'].passed_display }} | {{ results['generic.C2'].trend_display }} | {{ results['generic.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['generic.C3'].previous_passed_display \| default('—') }} | {{ results['generic.C3'].passed_display }} | {{ results['generic.C3'].trend_display }} | {{ results['generic.C3'].evidence.excerpt \| default('—') }} |

C1: content is architecture-relevant, not implementation-specific. C2: claims and assertions are justified by evidence or reasoning. C3: no duplication of content from other architecture section types.

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
| Domain | architecture |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/05-architecture/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
