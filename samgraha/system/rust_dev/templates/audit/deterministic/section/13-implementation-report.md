# Deterministic Section Report — Implementation

**Document:** {{ document_path }}
**Standard:** `documentation-standards/13-implementation-standards.md`
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 6 section scores below
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
| 1 | Generation Plan | **required** | 4.0 | {{ sections.generation_plan.score }} / 100 | {{ sections.generation_plan.previous_score | default('—') }} | {{ sections.generation_plan.trend_display }} |
| 2 | Security Fix Plan | **required** | 3.5 | {{ sections.security_fix_plan.score }} / 100 | {{ sections.security_fix_plan.previous_score | default('—') }} | {{ sections.security_fix_plan.trend_display }} |
| 3 | Purpose | optional | 1.5 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 4 | Refactor Plan | optional | 3.0 | {{ sections.refactor_plan.score }} / 100 | {{ sections.refactor_plan.previous_score | default('—') }} | {{ sections.refactor_plan.trend_display }} |
| 5 | Change Request Plan | optional | 3.0 | {{ sections.change_request_plan.score }} / 100 | {{ sections.change_request_plan.previous_score | default('—') }} | {{ sections.change_request_plan.trend_display }} |
| 6 | Enhancement Plan | optional | 3.0 | {{ sections.enhancement_plan.score }} / 100 | {{ sections.enhancement_plan.previous_score | default('—') }} | {{ sections.enhancement_plan.trend_display }} |

The 2 required sections carry 7.5 of the document's 18.0 total rule weight — a document can only pass if those two are both present and internally sound; the remaining four are recommended-quality signal, not gating.

---

## 1. Generation Plan — `section/13-implementation/01-generation_plan.yaml` — weight 4.0 — **required**

**Why this matters:** Generation Plan is the implementation's step-by-step blueprint — it defines what code is generated, in what order, and from what sources. A missing or empty generation plan leaves downstream Build with no verifiable implementation path.

**Section Score: {{ sections.generation_plan.score }} / 100** ({{ sections.generation_plan.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| impl-sec-gen-001 | Generation Plan section exists | error (mandatory) | 1.5 | {{ results['impl-sec-gen-001'].previous_status \| default('—') }} | {{ results['impl-sec-gen-001'].status }} | {{ results['impl-sec-gen-001'].trend_display }} | {{ results['impl-sec-gen-001'].evidence \| default('—') }} |
| impl-sec-gen-002 | Defines at least one generation step or phase | error (mandatory) | 1.0 | {{ results['impl-sec-gen-002'].previous_status \| default('—') }} | {{ results['impl-sec-gen-002'].status }} | {{ results['impl-sec-gen-002'].trend_display }} | {{ results['impl-sec-gen-002'].evidence \| default('—') }} |
| impl-sec-gen-003 | References Feature Technical component responsibilities or runtime behavior | warning (recommended) | 0.5 | {{ results['impl-sec-gen-003'].previous_status \| default('—') }} | {{ results['impl-sec-gen-003'].status }} | {{ results['impl-sec-gen-003'].trend_display }} | {{ results['impl-sec-gen-003'].evidence \| default('—') }} |
| impl-sec-gen-004 | References Engineering Documentation code or build standards | warning (recommended) | 0.5 | {{ results['impl-sec-gen-004'].previous_status \| default('—') }} | {{ results['impl-sec-gen-004'].status }} | {{ results['impl-sec-gen-004'].trend_display }} | {{ results['impl-sec-gen-004'].evidence \| default('—') }} |
| impl-sec-gen-005 | References Security Documentation threat model or constraints | warning (recommended) | 0.5 | {{ results['impl-sec-gen-005'].previous_status \| default('—') }} | {{ results['impl-sec-gen-005'].status }} | {{ results['impl-sec-gen-005'].trend_display }} | {{ results['impl-sec-gen-005'].evidence \| default('—') }} |

## 2. Security Fix Plan — `02-security_fix_plan.yaml` — weight 3.5 — **required**

**Why this matters:** Security Fix Plan is the implementation's remediation record — it defines what security issues are fixed, how, and what threats they address. A missing or empty security fix plan leaves the build without a verifiable security remediation path.

**Section Score: {{ sections.security_fix_plan.score }} / 100** ({{ sections.security_fix_plan.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| impl-sec-fix-001 | Security Fix Plan section exists | error (mandatory) | 1.5 | {{ results['impl-sec-fix-001'].previous_status \| default('—') }} | {{ results['impl-sec-fix-001'].status }} | {{ results['impl-sec-fix-001'].trend_display }} | {{ results['impl-sec-fix-001'].evidence \| default('—') }} |
| impl-sec-fix-002 | Defines at least one security fix or remediation step | error (mandatory) | 1.0 | {{ results['impl-sec-fix-002'].previous_status \| default('—') }} | {{ results['impl-sec-fix-002'].status }} | {{ results['impl-sec-fix-002'].trend_display }} | {{ results['impl-sec-fix-002'].evidence \| default('—') }} |
| impl-sec-fix-003 | References Security Documentation threat model or mitigation strategies | warning (recommended) | 0.5 | {{ results['impl-sec-fix-003'].previous_status \| default('—') }} | {{ results['impl-sec-fix-003'].status }} | {{ results['impl-sec-fix-003'].trend_display }} | {{ results['impl-sec-fix-003'].evidence \| default('—') }} |
| impl-sec-fix-004 | Each fix references the specific threat or vulnerability it addresses | warning (recommended) | 0.5 | {{ results['impl-sec-fix-004'].previous_status \| default('—') }} | {{ results['impl-sec-fix-004'].status }} | {{ results['impl-sec-fix-004'].trend_display }} | {{ results['impl-sec-fix-004'].evidence \| default('—') }} |

## 3. Purpose — `03-purpose.yaml` — weight 1.5 — optional

**Why this matters:** Purpose tells a reader why this Implementation Documentation exists before they read a single plan section. A Purpose section that's missing, vague, or generic undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| impl-sec-purpose-001 | Purpose section exists | warning (recommended) | 0.5 | {{ results['impl-sec-purpose-001'].previous_status \| default('—') }} | {{ results['impl-sec-purpose-001'].status }} | {{ results['impl-sec-purpose-001'].trend_display }} | {{ results['impl-sec-purpose-001'].evidence \| default('—') }} |
| impl-sec-purpose-002 | States implementation intent — why this documentation exists | warning (recommended) | 0.5 | {{ results['impl-sec-purpose-002'].previous_status \| default('—') }} | {{ results['impl-sec-purpose-002'].status }} | {{ results['impl-sec-purpose-002'].trend_display }} | {{ results['impl-sec-purpose-002'].evidence \| default('—') }} |
| impl-sec-purpose-003 | Defines scope boundaries — what the documentation is and is not | warning (recommended) | 0.5 | {{ results['impl-sec-purpose-003'].previous_status \| default('—') }} | {{ results['impl-sec-purpose-003'].status }} | {{ results['impl-sec-purpose-003'].trend_display }} | {{ results['impl-sec-purpose-003'].evidence \| default('—') }} |

## 4. Refactor Plan — `04-refactor_plan.yaml` — weight 3.0 — optional

**Why this matters:** Refactor Plan documents a restructuring that changes internal design without changing external behavior. It exists so a reviewer can confirm the refactor is behavior-preserving before and after, not just trust the diff.

**Section Score: {{ sections.refactor_plan.score }} / 100** ({{ sections.refactor_plan.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| implementation-sec-refactor_plan-001 | Refactor Plan section exists | error (mandatory) | 1.5 | {{ results['implementation-sec-refactor_plan-001'].previous_status \| default('—') }} | {{ results['implementation-sec-refactor_plan-001'].status }} | {{ results['implementation-sec-refactor_plan-001'].trend_display }} | {{ results['implementation-sec-refactor_plan-001'].evidence \| default('—') }} |
| implementation-sec-refactor_plan-002 | Has substantive content — not empty or placeholder only | error (mandatory) | 1.0 | {{ results['implementation-sec-refactor_plan-002'].previous_status \| default('—') }} | {{ results['implementation-sec-refactor_plan-002'].status }} | {{ results['implementation-sec-refactor_plan-002'].trend_display }} | {{ results['implementation-sec-refactor_plan-002'].evidence \| default('—') }} |
| implementation-sec-refactor_plan-003 | Specific to this project — not generic boilerplate | warning (recommended) | 0.5 | {{ results['implementation-sec-refactor_plan-003'].previous_status \| default('—') }} | {{ results['implementation-sec-refactor_plan-003'].status }} | {{ results['implementation-sec-refactor_plan-003'].trend_display }} | {{ results['implementation-sec-refactor_plan-003'].evidence \| default('—') }} |

## 5. Change Request Plan — `05-change_request_plan.yaml` — weight 3.0 — optional

**Why this matters:** Change Request Plan documents a modification driven by an external request — its impact, how to undo it if wrong, and what tests need updating. It exists so scope creep and untested side effects are caught before merge.

**Section Score: {{ sections.change_request_plan.score }} / 100** ({{ sections.change_request_plan.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| implementation-sec-change_request_plan-001 | Change Request Plan section exists | error (mandatory) | 1.5 | {{ results['implementation-sec-change_request_plan-001'].previous_status \| default('—') }} | {{ results['implementation-sec-change_request_plan-001'].status }} | {{ results['implementation-sec-change_request_plan-001'].trend_display }} | {{ results['implementation-sec-change_request_plan-001'].evidence \| default('—') }} |
| implementation-sec-change_request_plan-002 | Has substantive content — not empty or placeholder only | error (mandatory) | 1.0 | {{ results['implementation-sec-change_request_plan-002'].previous_status \| default('—') }} | {{ results['implementation-sec-change_request_plan-002'].status }} | {{ results['implementation-sec-change_request_plan-002'].trend_display }} | {{ results['implementation-sec-change_request_plan-002'].evidence \| default('—') }} |
| implementation-sec-change_request_plan-003 | Specific to this project — not generic boilerplate | warning (recommended) | 0.5 | {{ results['implementation-sec-change_request_plan-003'].previous_status \| default('—') }} | {{ results['implementation-sec-change_request_plan-003'].status }} | {{ results['implementation-sec-change_request_plan-003'].trend_display }} | {{ results['implementation-sec-change_request_plan-003'].evidence \| default('—') }} |

## 6. Enhancement Plan — `06-enhancement_plan.yaml` — weight 3.0 — optional

**Why this matters:** Enhancement Plan documents an improvement to existing functionality that must not change core behavior. It exists to distinguish "made it better" from "changed what it does," with a measurable target for the improvement claim.

**Section Score: {{ sections.enhancement_plan.score }} / 100** ({{ sections.enhancement_plan.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| implementation-sec-enhancement_plan-001 | Enhancement Plan section exists | error (mandatory) | 1.5 | {{ results['implementation-sec-enhancement_plan-001'].previous_status \| default('—') }} | {{ results['implementation-sec-enhancement_plan-001'].status }} | {{ results['implementation-sec-enhancement_plan-001'].trend_display }} | {{ results['implementation-sec-enhancement_plan-001'].evidence \| default('—') }} |
| implementation-sec-enhancement_plan-002 | Has substantive content — not empty or placeholder only | error (mandatory) | 1.0 | {{ results['implementation-sec-enhancement_plan-002'].previous_status \| default('—') }} | {{ results['implementation-sec-enhancement_plan-002'].status }} | {{ results['implementation-sec-enhancement_plan-002'].trend_display }} | {{ results['implementation-sec-enhancement_plan-002'].evidence \| default('—') }} |
| implementation-sec-enhancement_plan-003 | Specific to this project — not generic boilerplate | warning (recommended) | 0.5 | {{ results['implementation-sec-enhancement_plan-003'].previous_status \| default('—') }} | {{ results['implementation-sec-enhancement_plan-003'].status }} | {{ results['implementation-sec-enhancement_plan-003'].trend_display }} | {{ results['implementation-sec-enhancement_plan-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 6 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | implementation |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/13-implementation/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
