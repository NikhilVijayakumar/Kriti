# Semantic Section Report — Feature Design

**Document:** {{ document_path }}
**Standard:** `documentation-standards/09-feature-design-standards.md`
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
| 1 | User Experience | **required** | {{ sections.user_experience.score }} / 100 | {{ sections.user_experience.previous_score | default('—') }} | {{ sections.user_experience.trend_display }} |
| 2 | Workflow | **required** | {{ sections.workflow.score }} / 100 | {{ sections.workflow.previous_score | default('—') }} | {{ sections.workflow.trend_display }} |
| 3 | States | **required** | {{ sections.states.score }} / 100 | {{ sections.states.previous_score | default('—') }} | {{ sections.states.trend_display }} |
| 4 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Non-Goals | optional | {{ sections.non_goals.score }} / 100 | {{ sections.non_goals.previous_score | default('—') }} | {{ sections.non_goals.trend_display }} |
| 6 | Constraints | optional | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 7 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. User Experience — `section/09-feature-design/01-user_experience.md`

**Why this matters:** User experience evaluates how a feature feels, flows, and responds from the user's perspective. It ensures the design minimizes friction, meets accessibility standards, and delivers a coherent interaction model aligned with user expectations.

**Section Score: {{ sections.user_experience.score }} / 100** ({{ sections.user_experience.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['user_experience.C1'].previous_passed_display \| default('—') }} | {{ results['user_experience.C1'].passed_display }} | {{ results['user_experience.C1'].trend_display }} | {{ results['user_experience.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 25 | {{ results['user_experience.C2'].previous_passed_display \| default('—') }} | {{ results['user_experience.C2'].passed_display }} | {{ results['user_experience.C2'].trend_display }} | {{ results['user_experience.C2'].evidence.excerpt \| default('—') }} |
| C3 | mandatory | 25 | {{ results['user_experience.C3'].previous_passed_display \| default('—') }} | {{ results['user_experience.C3'].passed_display }} | {{ results['user_experience.C3'].trend_display }} | {{ results['user_experience.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['user_experience.C4'].previous_passed_display \| default('—') }} | {{ results['user_experience.C4'].passed_display }} | {{ results['user_experience.C4'].trend_display }} | {{ results['user_experience.C4'].evidence.excerpt \| default('—') }} |

C1: primary user flow is logical and minimal-friction. C2: visual hierarchy guides user to primary action. C3: accessibility basics (contrast, keyboard nav) met. C4: interaction feedback present for all states.

## 2. Workflow — `02-workflow.md`

**Why this matters:** Workflow examines the sequence of user actions and system responses required to accomplish a feature's goal. It ensures the workflow is complete, efficient, handles branching paths, and accounts for the full lifecycle from entry to exit.

**Section Score: {{ sections.workflow.score }} / 100** ({{ sections.workflow.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['workflow.C1'].previous_passed_display \| default('—') }} | {{ results['workflow.C1'].passed_display }} | {{ results['workflow.C1'].trend_display }} | {{ results['workflow.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 35 | {{ results['workflow.C2'].previous_passed_display \| default('—') }} | {{ results['workflow.C2'].passed_display }} | {{ results['workflow.C2'].trend_display }} | {{ results['workflow.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['workflow.C3'].previous_passed_display \| default('—') }} | {{ results['workflow.C3'].passed_display }} | {{ results['workflow.C3'].trend_display }} | {{ results['workflow.C3'].evidence.excerpt \| default('—') }} |

C1: workflow has clear start, steps, and end defined. C2: all branching paths (success/error/cancel) documented. C3: workflow length is justified and minimal.

## 3. States — `03-states.md`

**Why this matters:** States covers every visual and interactive state a UI component or screen can exhibit. Exhaustive state enumeration prevents runtime surprises by ensuring designers and developers agree on what the user sees during loading, empty, error, success, disabled, and edge conditions.

**Section Score: {{ sections.states.score }} / 100** ({{ sections.states.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['states.C1'].previous_passed_display \| default('—') }} | {{ results['states.C1'].passed_display }} | {{ results['states.C1'].trend_display }} | {{ results['states.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['states.C2'].previous_passed_display \| default('—') }} | {{ results['states.C2'].passed_display }} | {{ results['states.C2'].trend_display }} | {{ results['states.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 20 | {{ results['states.C3'].previous_passed_display \| default('—') }} | {{ results['states.C3'].passed_display }} | {{ results['states.C3'].trend_display }} | {{ results['states.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['states.C4'].previous_passed_display \| default('—') }} | {{ results['states.C4'].passed_display }} | {{ results['states.C4'].trend_display }} | {{ results['states.C4'].evidence.excerpt \| default('—') }} |

C1: all core states (default/loading/empty/error/success) defined. C2: state transitions and trigger actions documented. C3: empty and error states provide recovery guidance. C4: states defined for light and dark mode.

## 4. Purpose — `04-purpose.md`

**Why this matters:** Purpose defines the core rationale for a feature — what problem it solves and why it exists. A clear purpose ensures alignment across stakeholders and prevents scope creep by anchoring all decisions to the feature's intended value.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: purpose is explicitly stated and unambiguous. C2: purpose aligns with product strategy and user needs. C3: purpose is distinguishable from implementation details.

## 5. Non-Goals — `05-non_goals.md`

**Why this matters:** Non-goals explicitly define what a feature will not do, preventing scope creep and managing stakeholder expectations. They establish boundaries between this feature and adjacent work, clarify intentional omissions.

**Section Score: {{ sections.non_goals.score }} / 100** ({{ sections.non_goals.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['non_goals.C1'].previous_passed_display \| default('—') }} | {{ results['non_goals.C1'].passed_display }} | {{ results['non_goals.C1'].trend_display }} | {{ results['non_goals.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['non_goals.C2'].previous_passed_display \| default('—') }} | {{ results['non_goals.C2'].passed_display }} | {{ results['non_goals.C2'].trend_display }} | {{ results['non_goals.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['non_goals.C3'].previous_passed_display \| default('—') }} | {{ results['non_goals.C3'].passed_display }} | {{ results['non_goals.C3'].trend_display }} | {{ results['non_goals.C3'].evidence.excerpt \| default('—') }} |

C1: non-goals are explicitly listed with identifiers. C2: each non-goal includes a rationale. C3: non-goals do not contradict stated goals.

## 6. Constraints — `06-constraints.md`

**Why this matters:** Constraints document the boundaries within which a feature must be designed and built — technical, business, temporal, and regulatory. Auditing constraints ensures all limitations are surfaced early, trade-offs are explicit.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['constraints.C1'].previous_passed_display \| default('—') }} | {{ results['constraints.C1'].passed_display }} | {{ results['constraints.C1'].trend_display }} | {{ results['constraints.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['constraints.C2'].previous_passed_display \| default('—') }} | {{ results['constraints.C2'].passed_display }} | {{ results['constraints.C2'].trend_display }} | {{ results['constraints.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 20 | {{ results['constraints.C3'].previous_passed_display \| default('—') }} | {{ results['constraints.C3'].passed_display }} | {{ results['constraints.C3'].trend_display }} | {{ results['constraints.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['constraints.C4'].previous_passed_display \| default('—') }} | {{ results['constraints.C4'].passed_display }} | {{ results['constraints.C4'].trend_display }} | {{ results['constraints.C4'].evidence.excerpt \| default('—') }} |

C1: constraints are enumerated with source attribution. C2: hard vs. soft constraints are distinguished. C3: no design-violating constraints exist. C4: constraints include device/browser/OS minimums.

## 7. Traceability — `07-traceability.md`

**Why this matters:** Traceability ensures every design decision, requirement, and state can be linked back to the feature's purpose and forward to implementation artifacts. It creates a navigable chain from user need → specification → design → code → test.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['traceability.C1'].previous_passed_display \| default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 35 | {{ results['traceability.C2'].previous_passed_display \| default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['traceability.C3'].previous_passed_display \| default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt \| default('—') }} |

C1: design elements traceable to requirements. C2: bidirectional traceability exists (req↔design↔test). C3: no orphaned design elements without requirement.

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
| Domain | feature-design |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/09-feature-design/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
