# Deterministic Section Report — Feature Design

**Document:** {{ document_path }}
**Standard:** `documentation-standards/09-feature-design-standards.md`
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 7 section scores below
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
| 1 | User Experience | **required** | 4.0 | {{ sections.user_experience.score }} / 100 | {{ sections.user_experience.previous_score | default('—') }} | {{ sections.user_experience.trend_display }} |
| 2 | Workflow | **required** | 4.0 | {{ sections.workflow.score }} / 100 | {{ sections.workflow.previous_score | default('—') }} | {{ sections.workflow.trend_display }} |
| 3 | States | **required** | 4.0 | {{ sections.states.score }} / 100 | {{ sections.states.previous_score | default('—') }} | {{ sections.states.trend_display }} |
| 4 | Purpose | optional | 1.8 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Non-Goals | optional | 1.8 | {{ sections.non_goals.score }} / 100 | {{ sections.non_goals.previous_score | default('—') }} | {{ sections.non_goals.trend_display }} |
| 6 | Constraints | optional | 1.3 | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 7 | Traceability | optional | 1.3 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

The 3 required sections carry 12.0 of the document's 18.2 total rule weight — a document can only pass if those three are both present and internally sound; the remaining four are recommended-quality signal, not gating.

---

## 1. User Experience — `section/09-feature-design/01-user_experience.yaml` — weight 4.0 — **required**

**Why this matters:** User experience evaluates how a feature feels, flows, and responds from the user's perspective. It ensures the design minimizes friction, meets accessibility standards, and delivers a coherent interaction model aligned with user expectations.

**Section Score: {{ sections.user_experience.score }} / 100** ({{ sections.user_experience.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-sec-ux-001 | User Experience section exists | error (mandatory) | 1.5 | {{ results['fd-sec-ux-001'].previous_status \| default('—') }} | {{ results['fd-sec-ux-001'].status }} | {{ results['fd-sec-ux-001'].trend_display }} | {{ results['fd-sec-ux-001'].evidence \| default('—') }} |
| fd-sec-ux-002 | Describes user-facing behavior | error (mandatory) | 1.0 | {{ results['fd-sec-ux-002'].previous_status \| default('—') }} | {{ results['fd-sec-ux-002'].status }} | {{ results['fd-sec-ux-002'].trend_display }} | {{ results['fd-sec-ux-002'].evidence \| default('—') }} |
| fd-sec-ux-003 | No implementation technology references | error (mandatory) | 1.0 | {{ results['fd-sec-ux-003'].previous_status \| default('—') }} | {{ results['fd-sec-ux-003'].status }} | {{ results['fd-sec-ux-003'].trend_display }} | {{ results['fd-sec-ux-003'].evidence \| default('—') }} |
| fd-sec-ux-004 | Includes user stories or scenarios | warning (recommended) | 0.5 | {{ results['fd-sec-ux-004'].previous_status \| default('—') }} | {{ results['fd-sec-ux-004'].status }} | {{ results['fd-sec-ux-004'].trend_display }} | {{ results['fd-sec-ux-004'].evidence \| default('—') }} |

## 2. Workflow — `02-workflow.yaml` — weight 4.0 — **required**

**Why this matters:** Workflow examines the sequence of user actions and system responses required to accomplish a feature's goal. It ensures the workflow is complete, efficient, handles branching paths, and accounts for the full lifecycle from entry to exit.

**Section Score: {{ sections.workflow.score }} / 100** ({{ sections.workflow.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-sec-workflow-001 | Workflow section exists | error (mandatory) | 1.5 | {{ results['fd-sec-workflow-001'].previous_status \| default('—') }} | {{ results['fd-sec-workflow-001'].status }} | {{ results['fd-sec-workflow-001'].trend_display }} | {{ results['fd-sec-workflow-001'].evidence \| default('—') }} |
| fd-sec-workflow-002 | Describes feature flow (step-by-step) | error (mandatory) | 1.0 | {{ results['fd-sec-workflow-002'].previous_status \| default('—') }} | {{ results['fd-sec-workflow-002'].status }} | {{ results['fd-sec-workflow-002'].trend_display }} | {{ results['fd-sec-workflow-002'].evidence \| default('—') }} |
| fd-sec-workflow-003 | No implementation technology references | error (mandatory) | 1.0 | {{ results['fd-sec-workflow-003'].previous_status \| default('—') }} | {{ results['fd-sec-workflow-003'].status }} | {{ results['fd-sec-workflow-003'].trend_display }} | {{ results['fd-sec-workflow-003'].evidence \| default('—') }} |
| fd-sec-workflow-004 | Defines entry and exit conditions | warning (recommended) | 0.5 | {{ results['fd-sec-workflow-004'].previous_status \| default('—') }} | {{ results['fd-sec-workflow-004'].status }} | {{ results['fd-sec-workflow-004'].trend_display }} | {{ results['fd-sec-workflow-004'].evidence \| default('—') }} |

## 3. States — `03-states.yaml` — weight 4.0 — **required**

**Why this matters:** States covers every visual and interactive state a UI component or screen can exhibit. Exhaustive state enumeration prevents runtime surprises by ensuring designers and developers agree on what the user sees during loading, empty, error, success, disabled, and edge conditions.

**Section Score: {{ sections.states.score }} / 100** ({{ sections.states.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-sec-states-001 | States section exists | error (mandatory) | 1.5 | {{ results['fd-sec-states-001'].previous_status \| default('—') }} | {{ results['fd-sec-states-001'].status }} | {{ results['fd-sec-states-001'].trend_display }} | {{ results['fd-sec-states-001'].evidence \| default('—') }} |
| fd-sec-states-002 | Defines feature states | error (mandatory) | 1.0 | {{ results['fd-sec-states-002'].previous_status \| default('—') }} | {{ results['fd-sec-states-002'].status }} | {{ results['fd-sec-states-002'].trend_display }} | {{ results['fd-sec-states-002'].evidence \| default('—') }} |
| fd-sec-states-003 | Defines valid transitions | warning (recommended) | 0.5 | {{ results['fd-sec-states-003'].previous_status \| default('—') }} | {{ results['fd-sec-states-003'].status }} | {{ results['fd-sec-states-003'].trend_display }} | {{ results['fd-sec-states-003'].evidence \| default('—') }} |
| fd-sec-states-004 | No implementation technology references | error (mandatory) | 1.0 | {{ results['fd-sec-states-004'].previous_status \| default('—') }} | {{ results['fd-sec-states-004'].status }} | {{ results['fd-sec-states-004'].trend_display }} | {{ results['fd-sec-states-004'].evidence \| default('—') }} |

## 4. Purpose — `04-purpose.yaml` — weight 1.8 — optional

**Why this matters:** Purpose defines the core rationale for a feature — what problem it solves and why it exists. A clear purpose ensures alignment across stakeholders and prevents scope creep by anchoring all decisions to the feature's intended value.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-sec-purpose-001 | Purpose section present | info | 0.3 | {{ results['fd-sec-purpose-001'].previous_status \| default('—') }} | {{ results['fd-sec-purpose-001'].status }} | {{ results['fd-sec-purpose-001'].trend_display }} | {{ results['fd-sec-purpose-001'].evidence \| default('—') }} |
| fd-sec-purpose-002 | States feature design intent | warning (recommended) | 0.5 | {{ results['fd-sec-purpose-002'].previous_status \| default('—') }} | {{ results['fd-sec-purpose-002'].status }} | {{ results['fd-sec-purpose-002'].trend_display }} | {{ results['fd-sec-purpose-002'].evidence \| default('—') }} |
| fd-sec-purpose-003 | Technology-independent | error | 1.0 | {{ results['fd-sec-purpose-003'].previous_status \| default('—') }} | {{ results['fd-sec-purpose-003'].status }} | {{ results['fd-sec-purpose-003'].trend_display }} | {{ results['fd-sec-purpose-003'].evidence \| default('—') }} |

## 5. Non-Goals — `05-non_goals.yaml` — weight 1.8 — optional

**Why this matters:** Non-goals explicitly define what a feature will not do, preventing scope creep and managing stakeholder expectations. They establish boundaries between this feature and adjacent work, clarify intentional omissions.

**Section Score: {{ sections.non_goals.score }} / 100** ({{ sections.non_goals.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-sec-nongoals-001 | Non-Goals section present | info | 0.3 | {{ results['fd-sec-nongoals-001'].previous_status \| default('—') }} | {{ results['fd-sec-nongoals-001'].status }} | {{ results['fd-sec-nongoals-001'].trend_display }} | {{ results['fd-sec-nongoals-001'].evidence \| default('—') }} |
| fd-sec-nongoals-002 | Defines excluded features | warning (recommended) | 0.5 | {{ results['fd-sec-nongoals-002'].previous_status \| default('—') }} | {{ results['fd-sec-nongoals-002'].status }} | {{ results['fd-sec-nongoals-002'].trend_display }} | {{ results['fd-sec-nongoals-002'].evidence \| default('—') }} |
| fd-sec-nongoals-003 | Technology-independent | error | 1.0 | {{ results['fd-sec-nongoals-003'].previous_status \| default('—') }} | {{ results['fd-sec-nongoals-003'].status }} | {{ results['fd-sec-nongoals-003'].trend_display }} | {{ results['fd-sec-nongoals-003'].evidence \| default('—') }} |

## 6. Constraints — `06-constraints.yaml` — weight 1.3 — optional

**Why this matters:** Constraints document the boundaries within which a feature must be designed and built — technical, business, temporal, and regulatory. Without them, constraints are discovered late in implementation.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-sec-constraints-001 | Constraints section present | info | 0.3 | {{ results['fd-sec-constraints-001'].previous_status \| default('—') }} | {{ results['fd-sec-constraints-001'].status }} | {{ results['fd-sec-constraints-001'].trend_display }} | {{ results['fd-sec-constraints-001'].evidence \| default('—') }} |
| fd-sec-constraints-002 | Defines design constraints | warning (recommended) | 0.5 | {{ results['fd-sec-constraints-002'].previous_status \| default('—') }} | {{ results['fd-sec-constraints-002'].status }} | {{ results['fd-sec-constraints-002'].trend_display }} | {{ results['fd-sec-constraints-002'].evidence \| default('—') }} |
| fd-sec-constraints-003 | Constraints have clear sources | warning (recommended) | 0.5 | {{ results['fd-sec-constraints-003'].previous_status \| default('—') }} | {{ results['fd-sec-constraints-003'].status }} | {{ results['fd-sec-constraints-003'].trend_display }} | {{ results['fd-sec-constraints-003'].evidence \| default('—') }} |

## 7. Traceability — `07-traceability.yaml` — weight 1.3 — optional

**Why this matters:** Traceability ensures every design decision, requirement, and state can be linked back to the feature's purpose and forward to implementation artifacts. Without it, orphaned designs accumulate and impact analysis is impossible.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-sec-trace-001 | Traceability section present | info | 0.3 | {{ results['fd-sec-trace-001'].previous_status \| default('—') }} | {{ results['fd-sec-trace-001'].status }} | {{ results['fd-sec-trace-001'].trend_display }} | {{ results['fd-sec-trace-001'].evidence \| default('—') }} |
| fd-sec-trace-002 | Links to upstream domains (Feature, Design, External Context) | warning (recommended) | 0.5 | {{ results['fd-sec-trace-002'].previous_status \| default('—') }} | {{ results['fd-sec-trace-002'].status }} | {{ results['fd-sec-trace-002'].trend_display }} | {{ results['fd-sec-trace-002'].evidence \| default('—') }} |
| fd-sec-trace-003 | Links to downstream validation (Prototype, Feature Technical) | warning (recommended) | 0.5 | {{ results['fd-sec-trace-003'].previous_status \| default('—') }} | {{ results['fd-sec-trace-003'].status }} | {{ results['fd-sec-trace-003'].trend_display }} | {{ results['fd-sec-trace-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 7 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | feature-design |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/09-feature-design/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
