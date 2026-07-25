# Semantic Section Report — Prototype

**Document:** {{ document_path }}
**Standard:** `documentation-standards/11-prototype-standards.md`
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
| 1 | Scope | **required** | {{ sections.scope.score }} / 100 | {{ sections.scope.previous_score | default('—') }} | {{ sections.scope.trend_display }} |
| 2 | Mock APIs | **required** | {{ sections.mock_apis.score }} / 100 | {{ sections.mock_apis.previous_score | default('—') }} | {{ sections.mock_apis.trend_display }} |
| 3 | Data Model | **required** | {{ sections.data_model.score }} / 100 | {{ sections.data_model.previous_score | default('—') }} | {{ sections.data_model.trend_display }} |
| 4 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Constraints | optional | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 6 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Scope — `section/11-prototype/01-scope.md`

**Why this matters:** Prototype scope defines the boundary between what is simulated and what is real. Over-scoping inflates cost and delays answers; under-scoping produces misleading results. Scope must explicitly state inclusion and exclusion boundaries relative to the prototype purpose.

**Section Score: {{ sections.scope.score }} / 100** ({{ sections.scope.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['scope.C1'].previous_passed_display \| default('—') }} | {{ results['scope.C1'].passed_display }} | {{ results['scope.C1'].trend_display }} | {{ results['scope.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 35 | {{ results['scope.C2'].previous_passed_display \| default('—') }} | {{ results['scope.C2'].passed_display }} | {{ results['scope.C2'].trend_display }} | {{ results['scope.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['scope.C3'].previous_passed_display \| default('—') }} | {{ results['scope.C3'].passed_display }} | {{ results['scope.C3'].trend_display }} | {{ results['scope.C3'].evidence.excerpt \| default('—') }} |

C1: in-scope and out-of-scope lists present. C2: scope items map to the stated prototype purpose. C3: fidelity level is defined per scope item.

## 2. Mock APIs — `02-mock_apis.md`

**Why this matters:** Prototypes often depend on external services that do not exist or are impractical to call during simulation. Mock APIs must faithfully represent the real interface contract without implementing production logic. Mismatched mocks produce false confidence or false negatives.

**Section Score: {{ sections.mock_apis.score }} / 100** ({{ sections.mock_apis.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['mock_apis.C1'].previous_passed_display \| default('—') }} | {{ results['mock_apis.C1'].passed_display }} | {{ results['mock_apis.C1'].trend_display }} | {{ results['mock_apis.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['mock_apis.C2'].previous_passed_display \| default('—') }} | {{ results['mock_apis.C2'].passed_display }} | {{ results['mock_apis.C2'].trend_display }} | {{ results['mock_apis.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['mock_apis.C3'].previous_passed_display \| default('—') }} | {{ results['mock_apis.C3'].passed_display }} | {{ results['mock_apis.C3'].trend_display }} | {{ results['mock_apis.C3'].evidence.excerpt \| default('—') }} |

C1: every external dependency has a mock or stub. C2: mock responses match real API schema (or documented deviation). C3: mock includes at least one error scenario.

## 3. Data Model — `03-data_model.md`

**Why this matters:** A prototype's data model is a simplified representation of real domain entities and their relationships. The model must be sufficient to exercise the prototype scenario without introducing unrealistic constraints or omitted fields that would invalidate simulation results.

**Section Score: {{ sections.data_model.score }} / 100** ({{ sections.data_model.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['data_model.C1'].previous_passed_display \| default('—') }} | {{ results['data_model.C1'].passed_display }} | {{ results['data_model.C1'].trend_display }} | {{ results['data_model.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['data_model.C2'].previous_passed_display \| default('—') }} | {{ results['data_model.C2'].passed_display }} | {{ results['data_model.C2'].trend_display }} | {{ results['data_model.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['data_model.C3'].previous_passed_display \| default('—') }} | {{ results['data_model.C3'].passed_display }} | {{ results['data_model.C3'].trend_display }} | {{ results['data_model.C3'].evidence.excerpt \| default('—') }} |

C1: core entities and relationships are documented. C2: no PII, secrets, or production data in the model. C3: seed or fixture data covers at least 2 scenarios.

## 4. Purpose — `04-purpose.md`

**Why this matters:** A prototype must have a clearly stated purpose that defines what question it answers or what risk it mitigates. Without an explicit purpose, a prototype cannot be evaluated for fitness. The purpose drives simulation fidelity, scope, and termination criteria.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: purpose explicitly stated in the prototype entry point or README. C2: purpose references a falsifiable question with explicit success and failure thresholds. C3: stakeholder or audience is identified.

## 5. Constraints — `05-constraints.md`

**Why this matters:** Constraints capture the known limitations, assumptions, and guardrails of a prototype. Every prototype operates under artificial conditions; undisclosed constraints mislead evaluators into overgeneralizing results. Constraints must be surfaced, documented, and traceable to the prototype purpose.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['constraints.C1'].previous_passed_display \| default('—') }} | {{ results['constraints.C1'].passed_display }} | {{ results['constraints.C1'].trend_display }} | {{ results['constraints.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['constraints.C2'].previous_passed_display \| default('—') }} | {{ results['constraints.C2'].passed_display }} | {{ results['constraints.C2'].trend_display }} | {{ results['constraints.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['constraints.C3'].previous_passed_display \| default('—') }} | {{ results['constraints.C3'].passed_display }} | {{ results['constraints.C3'].trend_display }} | {{ results['constraints.C3'].evidence.excerpt \| default('—') }} |

C1: all known constraints and assumptions are documented. C2: each constraint includes an impact on result generalizability. C3: constraints are traceable to scope items or mock decisions.

## 6. Traceability — `06-traceability.md`

**Why this matters:** Traceability connects prototype artifacts — purpose, scope, mocks, data model, constraints — into a coherent chain. Every design decision should be traceable back to the prototype purpose and forward to the code or configuration that implements it. Broken traceability means broken auditability.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['traceability.C1'].previous_passed_display \| default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display \| default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['traceability.C3'].previous_passed_display \| default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt \| default('—') }} |

C1: every artifact traces to a purpose or scope item. C2: no orphaned code, mocks, or data without a trace. C3: traceability matrix or equivalent is documented.

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
| Domain | prototype |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/11-prototype/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
