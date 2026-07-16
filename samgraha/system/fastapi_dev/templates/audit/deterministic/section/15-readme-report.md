# Deterministic Section Report — README

**Document:** {{ document_path }}
**Standard:** `documentation-standards/15-readme-standards.md`
**Rule Files:** `audit/deterministic/section/15-readme/*.yaml`
**Auditor:** System (deterministic engine)
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 15 section scores below
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
| 1 | Project Name | **required** | 3.0 | {{ sections.project_name.score }} / 100 | {{ sections.project_name.previous_score | default('—') }} | {{ sections.project_name.trend_display }} |
| 2 | Short Description | **required** | 3.0 | {{ sections.short_description.score }} / 100 | {{ sections.short_description.previous_score | default('—') }} | {{ sections.short_description.trend_display }} |
| 3 | Overview | **required** | 3.0 | {{ sections.overview.score }} / 100 | {{ sections.overview.previous_score | default('—') }} | {{ sections.overview.trend_display }} |
| 4 | Purpose | **required** | 3.0 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Key Capabilities | **required** | 3.0 | {{ sections.key_capabilities.score }} / 100 | {{ sections.key_capabilities.previous_score | default('—') }} | {{ sections.key_capabilities.trend_display }} |
| 6 | Repository Structure | **required** | 3.0 | {{ sections.repository_structure.score }} / 100 | {{ sections.repository_structure.previous_score | default('—') }} | {{ sections.repository_structure.trend_display }} |
| 7 | Documentation Structure | **required** | 3.0 | {{ sections.documentation_structure.score }} / 100 | {{ sections.documentation_structure.previous_score | default('—') }} | {{ sections.documentation_structure.trend_display }} |
| 8 | Getting Started | **required** | 3.0 | {{ sections.getting_started.score }} / 100 | {{ sections.getting_started.previous_score | default('—') }} | {{ sections.getting_started.trend_display }} |
| 9 | Installation | **required** | 3.0 | {{ sections.installation.score }} / 100 | {{ sections.installation.previous_score | default('—') }} | {{ sections.installation.trend_display }} |
| 10 | Build | **required** | 3.0 | {{ sections.build.score }} / 100 | {{ sections.build.previous_score | default('—') }} | {{ sections.build.trend_display }} |
| 11 | Usage | **required** | 3.0 | {{ sections.usage.score }} / 100 | {{ sections.usage.previous_score | default('—') }} | {{ sections.usage.trend_display }} |
| 12 | Development | **required** | 3.0 | {{ sections.development.score }} / 100 | {{ sections.development.previous_score | default('—') }} | {{ sections.development.trend_display }} |
| 13 | Contributing | **required** | 3.0 | {{ sections.contributing.score }} / 100 | {{ sections.contributing.previous_score | default('—') }} | {{ sections.contributing.trend_display }} |
| 14 | Configuration | optional | 3.0 | {{ sections.configuration.score }} / 100 | {{ sections.configuration.previous_score | default('—') }} | {{ sections.configuration.trend_display }} |
| 15 | License | optional | 3.0 | {{ sections.license.score }} / 100 | {{ sections.license.previous_score | default('—') }} | {{ sections.license.trend_display }} |

The 13 required sections carry 39.0 of the document's 45.0 total rule weight — a document can only pass if those thirteen are both present and internally sound; the remaining two are recommended-quality signal, not gating.

---

## 1. Project Name — weight 3.0 — **required**

**Why this matters:** Project Name is the canonical identifier — every reference to the project in docs, packages, and repos must resolve to one unambiguous name. A missing or incorrect project name means readers can't reliably find or refer to the project.

**Section Score: {{ sections.project_name.score }} / 100** ({{ sections.project_name.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-name-001 | Project name section exists | error (mandatory) | 1.5 | {{ results['readme-sec-name-001'].previous_status \| default('—') }} | {{ results['readme-sec-name-001'].status }} | {{ results['readme-sec-name-001'].trend_display }} | {{ results['readme-sec-name-001'].evidence \| default('—') }} |
| readme-sec-name-002 | Project name is present and non-empty | error (mandatory) | 1.0 | {{ results['readme-sec-name-002'].previous_status \| default('—') }} | {{ results['readme-sec-name-002'].status }} | {{ results['readme-sec-name-002'].trend_display }} | {{ results['readme-sec-name-002'].evidence \| default('—') }} |
| readme-sec-name-003 | Project name matches repository name | warning (recommended) | 0.5 | {{ results['readme-sec-name-003'].previous_status \| default('—') }} | {{ results['readme-sec-name-003'].status }} | {{ results['readme-sec-name-003'].trend_display }} | {{ results['readme-sec-name-003'].evidence \| default('—') }} |

## 2. Short Description — weight 3.0 — **required**

**Why this matters:** Short Description is the one/two-sentence answer to "what is this and who is it for" — the first thing a reader evaluates before deciding to read further. A missing or bloated description loses readers before they reach the substance.

**Section Score: {{ sections.short_description.score }} / 100** ({{ sections.short_description.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-short-001 | Short description section exists | error (mandatory) | 1.5 | {{ results['readme-sec-short-001'].previous_status \| default('—') }} | {{ results['readme-sec-short-001'].status }} | {{ results['readme-sec-short-001'].trend_display }} | {{ results['readme-sec-short-001'].evidence \| default('—') }} |
| readme-sec-short-002 | Short description is concise (one to two sentences) | error (mandatory) | 1.0 | {{ results['readme-sec-short-002'].previous_status \| default('—') }} | {{ results['readme-sec-short-002'].status }} | {{ results['readme-sec-short-002'].trend_display }} | {{ results['readme-sec-short-002'].evidence \| default('—') }} |
| readme-sec-short-003 | Short description states purpose | warning (recommended) | 0.5 | {{ results['readme-sec-short-003'].previous_status \| default('—') }} | {{ results['readme-sec-short-003'].status }} | {{ results['readme-sec-short-003'].trend_display }} | {{ results['readme-sec-short-003'].evidence \| default('—') }} |

## 3. Overview — weight 3.0 — **required**

**Why this matters:** Overview explains the problem the project solves and the approach taken, at a level a new reader can absorb before touching code. It bridges Short Description and the detailed docs — narrative, not technical.

**Section Score: {{ sections.overview.score }} / 100** ({{ sections.overview.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-overview-001 | Overview section exists | error (mandatory) | 1.5 | {{ results['readme-sec-overview-001'].previous_status \| default('—') }} | {{ results['readme-sec-overview-001'].status }} | {{ results['readme-sec-overview-001'].trend_display }} | {{ results['readme-sec-overview-001'].evidence \| default('—') }} |
| readme-sec-overview-002 | Overview provides context | error (mandatory) | 1.0 | {{ results['readme-sec-overview-002'].previous_status \| default('—') }} | {{ results['readme-sec-overview-002'].status }} | {{ results['readme-sec-overview-002'].trend_display }} | {{ results['readme-sec-overview-002'].evidence \| default('—') }} |
| readme-sec-overview-003 | Overview references Architecture Documentation | warning (recommended) | 0.5 | {{ results['readme-sec-overview-003'].previous_status \| default('—') }} | {{ results['readme-sec-overview-003'].status }} | {{ results['readme-sec-overview-003'].trend_display }} | {{ results['readme-sec-overview-003'].evidence \| default('—') }} |

## 4. Purpose — weight 3.0 — **required**

**Why this matters:** Purpose defines what the README is and is not — the boundary between README and the rest of the documentation ecosystem. Without it, readers don't know when to stop reading the README and go elsewhere.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-purpose-001 | Purpose section exists | error (mandatory) | 1.5 | {{ results['readme-sec-purpose-001'].previous_status \| default('—') }} | {{ results['readme-sec-purpose-001'].status }} | {{ results['readme-sec-purpose-001'].trend_display }} | {{ results['readme-sec-purpose-001'].evidence \| default('—') }} |
| readme-sec-purpose-002 | Purpose states project intent | error (mandatory) | 1.0 | {{ results['readme-sec-purpose-002'].previous_status \| default('—') }} | {{ results['readme-sec-purpose-002'].status }} | {{ results['readme-sec-purpose-002'].trend_display }} | {{ results['readme-sec-purpose-002'].evidence \| default('—') }} |
| readme-sec-purpose-003 | Purpose defines scope boundaries | warning (recommended) | 0.5 | {{ results['readme-sec-purpose-003'].previous_status \| default('—') }} | {{ results['readme-sec-purpose-003'].status }} | {{ results['readme-sec-purpose-003'].trend_display }} | {{ results['readme-sec-purpose-003'].evidence \| default('—') }} |

## 5. Key Capabilities — weight 3.0 — **required**

**Why this matters:** Key Capabilities is a scannable list of what the project can do, letting a reader assess fit in seconds. Without it, readers must read the entire document to determine if the project meets their needs.

**Section Score: {{ sections.key_capabilities.score }} / 100** ({{ sections.key_capabilities.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-capabilities-001 | Key capabilities section exists | error (mandatory) | 1.5 | {{ results['readme-sec-capabilities-001'].previous_status \| default('—') }} | {{ results['readme-sec-capabilities-001'].status }} | {{ results['readme-sec-capabilities-001'].trend_display }} | {{ results['readme-sec-capabilities-001'].evidence \| default('—') }} |
| readme-sec-capabilities-002 | Key capabilities lists features | error (mandatory) | 1.0 | {{ results['readme-sec-capabilities-002'].previous_status \| default('—') }} | {{ results['readme-sec-capabilities-002'].status }} | {{ results['readme-sec-capabilities-002'].trend_display }} | {{ results['readme-sec-capabilities-002'].evidence \| default('—') }} |
| readme-sec-capabilities-003 | Key capabilities references Feature Documentation | warning (recommended) | 0.5 | {{ results['readme-sec-capabilities-003'].previous_status \| default('—') }} | {{ results['readme-sec-capabilities-003'].status }} | {{ results['readme-sec-capabilities-003'].trend_display }} | {{ results['readme-sec-capabilities-003'].evidence \| default('—') }} |

## 6. Repository Structure — weight 3.0 — **required**

**Why this matters:** Repository Structure orients a new contributor to the directory layout at a glance. Without it, newcomers must explore the filesystem blindly to understand where things live.

**Section Score: {{ sections.repository_structure.score }} / 100** ({{ sections.repository_structure.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-repo-001 | Repository structure section exists | error (mandatory) | 1.5 | {{ results['readme-sec-repo-001'].previous_status \| default('—') }} | {{ results['readme-sec-repo-001'].status }} | {{ results['readme-sec-repo-001'].trend_display }} | {{ results['readme-sec-repo-001'].evidence \| default('—') }} |
| readme-sec-repo-002 | Repository structure describes layout | error (mandatory) | 1.0 | {{ results['readme-sec-repo-002'].previous_status \| default('—') }} | {{ results['readme-sec-repo-002'].status }} | {{ results['readme-sec-repo-002'].trend_display }} | {{ results['readme-sec-repo-002'].evidence \| default('—') }} |
| readme-sec-repo-003 | Repository structure lists key directories | warning (recommended) | 0.5 | {{ results['readme-sec-repo-003'].previous_status \| default('—') }} | {{ results['readme-sec-repo-003'].status }} | {{ results['readme-sec-repo-003'].trend_display }} | {{ results['readme-sec-repo-003'].evidence \| default('—') }} |

## 7. Documentation Structure — weight 3.0 — **required**

**Why this matters:** Documentation Structure tells a reader where the rest of the documentation lives and in what order to read it. Without it, the README is an island — readers can't find the deeper docs.

**Section Score: {{ sections.documentation_structure.score }} / 100** ({{ sections.documentation_structure.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-doc-struct-001 | Documentation structure section exists | error (mandatory) | 1.5 | {{ results['readme-sec-doc-struct-001'].previous_status \| default('—') }} | {{ results['readme-sec-doc-struct-001'].status }} | {{ results['readme-sec-doc-struct-001'].trend_display }} | {{ results['readme-sec-doc-struct-001'].evidence \| default('—') }} |
| readme-sec-doc-struct-002 | Documentation structure describes docs layout | error (mandatory) | 1.0 | {{ results['readme-sec-doc-struct-002'].previous_status \| default('—') }} | {{ results['readme-sec-doc-struct-002'].status }} | {{ results['readme-sec-doc-struct-002'].trend_display }} | {{ results['readme-sec-doc-struct-002'].evidence \| default('—') }} |
| readme-sec-doc-struct-003 | Documentation structure references knowledge hub | warning (recommended) | 0.5 | {{ results['readme-sec-doc-struct-003'].previous_status \| default('—') }} | {{ results['readme-sec-doc-struct-003'].status }} | {{ results['readme-sec-doc-struct-003'].trend_display }} | {{ results['readme-sec-doc-struct-003'].evidence \| default('—') }} |

## 8. Getting Started — weight 3.0 — **required**

**Why this matters:** Getting Started guides a user from zero to running the project. Without it, a new user must piece together instructions from Installation, Build, and Usage to figure out the actual first step.

**Section Score: {{ sections.getting_started.score }} / 100** ({{ sections.getting_started.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-start-001 | Getting started section exists | error (mandatory) | 1.5 | {{ results['readme-sec-start-001'].previous_status \| default('—') }} | {{ results['readme-sec-start-001'].status }} | {{ results['readme-sec-start-001'].trend_display }} | {{ results['readme-sec-start-001'].evidence \| default('—') }} |
| readme-sec-start-002 | Getting started provides quick start instructions | error (mandatory) | 1.0 | {{ results['readme-sec-start-002'].previous_status \| default('—') }} | {{ results['readme-sec-start-002'].status }} | {{ results['readme-sec-start-002'].trend_display }} | {{ results['readme-sec-start-002'].evidence \| default('—') }} |
| readme-sec-start-003 | Getting started has prerequisites | warning (recommended) | 0.5 | {{ results['readme-sec-start-003'].previous_status \| default('—') }} | {{ results['readme-sec-start-003'].status }} | {{ results['readme-sec-start-003'].trend_display }} | {{ results['readme-sec-start-003'].evidence \| default('—') }} |

## 9. Installation — weight 3.0 — **required**

**Why this matters:** Installation gets the project onto a machine — prerequisites and exact commands. Without explicit install steps, users hit silent failures or waste time figuring out dependencies.

**Section Score: {{ sections.installation.score }} / 100** ({{ sections.installation.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-install-001 | Installation section exists | error (mandatory) | 1.5 | {{ results['readme-sec-install-001'].previous_status \| default('—') }} | {{ results['readme-sec-install-001'].status }} | {{ results['readme-sec-install-001'].trend_display }} | {{ results['readme-sec-install-001'].evidence \| default('—') }} |
| readme-sec-install-002 | Installation provides steps | error (mandatory) | 1.0 | {{ results['readme-sec-install-002'].previous_status \| default('—') }} | {{ results['readme-sec-install-002'].status }} | {{ results['readme-sec-install-002'].trend_display }} | {{ results['readme-sec-install-002'].evidence \| default('—') }} |
| readme-sec-install-003 | Installation lists dependencies | warning (recommended) | 0.5 | {{ results['readme-sec-install-003'].previous_status \| default('—') }} | {{ results['readme-sec-install-003'].status }} | {{ results['readme-sec-install-003'].trend_display }} | {{ results['readme-sec-install-003'].evidence \| default('—') }} |

## 10. Build — weight 3.0 — **required**

**Why this matters:** Build documents how to produce a build artifact from source. Without it, contributors don't know how to compile or package the project, and may produce inconsistent artifacts.

**Section Score: {{ sections.build.score }} / 100** ({{ sections.build.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-build-001 | Build section exists | error (mandatory) | 1.5 | {{ results['readme-sec-build-001'].previous_status \| default('—') }} | {{ results['readme-sec-build-001'].status }} | {{ results['readme-sec-build-001'].trend_display }} | {{ results['readme-sec-build-001'].evidence \| default('—') }} |
| readme-sec-build-002 | Build provides instructions | error (mandatory) | 1.0 | {{ results['readme-sec-build-002'].previous_status \| default('—') }} | {{ results['readme-sec-build-002'].status }} | {{ results['readme-sec-build-002'].trend_display }} | {{ results['readme-sec-build-002'].evidence \| default('—') }} |
| readme-sec-build-003 | Build references Build Documentation | warning (recommended) | 0.5 | {{ results['readme-sec-build-003'].previous_status \| default('—') }} | {{ results['readme-sec-build-003'].status }} | {{ results['readme-sec-build-003'].trend_display }} | {{ results['readme-sec-build-003'].evidence \| default('—') }} |

## 11. Usage — weight 3.0 — **required**

**Why this matters:** Usage demonstrates the project's primary functions with real, runnable examples. Without concrete examples, readers can't verify the project does what they need, and they have no starting point for their own use.

**Section Score: {{ sections.usage.score }} / 100** ({{ sections.usage.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-usage-001 | Usage section exists | error (mandatory) | 1.5 | {{ results['readme-sec-usage-001'].previous_status \| default('—') }} | {{ results['readme-sec-usage-001'].status }} | {{ results['readme-sec-usage-001'].trend_display }} | {{ results['readme-sec-usage-001'].evidence \| default('—') }} |
| readme-sec-usage-002 | Usage provides examples | error (mandatory) | 1.0 | {{ results['readme-sec-usage-002'].previous_status \| default('—') }} | {{ results['readme-sec-usage-002'].status }} | {{ results['readme-sec-usage-002'].trend_display }} | {{ results['readme-sec-usage-002'].evidence \| default('—') }} |
| readme-sec-usage-003 | Usage references Feature Documentation | warning (recommended) | 0.5 | {{ results['readme-sec-usage-003'].previous_status \| default('—') }} | {{ results['readme-sec-usage-003'].status }} | {{ results['readme-sec-usage-003'].trend_display }} | {{ results['readme-sec-usage-003'].evidence \| default('—') }} |

## 12. Development — weight 3.0 — **required**

**Why this matters:** Development gets a contributor from clone to running the test suite and understanding the workflow. Without it, contributors guess at setup steps and may submit code that doesn't match project conventions.

**Section Score: {{ sections.development.score }} / 100** ({{ sections.development.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-dev-001 | Development section exists | error (mandatory) | 1.5 | {{ results['readme-sec-dev-001'].previous_status \| default('—') }} | {{ results['readme-sec-dev-001'].status }} | {{ results['readme-sec-dev-001'].trend_display }} | {{ results['readme-sec-dev-001'].evidence \| default('—') }} |
| readme-sec-dev-002 | Development provides guidelines | error (mandatory) | 1.0 | {{ results['readme-sec-dev-002'].previous_status \| default('—') }} | {{ results['readme-sec-dev-002'].status }} | {{ results['readme-sec-dev-002'].trend_display }} | {{ results['readme-sec-dev-002'].evidence \| default('—') }} |
| readme-sec-dev-003 | Development references Engineering Documentation | warning (recommended) | 0.5 | {{ results['readme-sec-dev-003'].previous_status \| default('—') }} | {{ results['readme-sec-dev-003'].status }} | {{ results['readme-sec-dev-003'].trend_display }} | {{ results['readme-sec-dev-003'].evidence \| default('—') }} |

## 13. Contributing — weight 3.0 — **required**

**Why this matters:** Contributing tells an external contributor how to submit a change that gets accepted. Without it, contributors don't know the process, review expectations, or quality bar, and first-time contributors have to guess or ask.

**Section Score: {{ sections.contributing.score }} / 100** ({{ sections.contributing.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-contrib-001 | Contributing section exists | error (mandatory) | 1.5 | {{ results['readme-sec-contrib-001'].previous_status \| default('—') }} | {{ results['readme-sec-contrib-001'].status }} | {{ results['readme-sec-contrib-001'].trend_display }} | {{ results['readme-sec-contrib-001'].evidence \| default('—') }} |
| readme-sec-contrib-002 | Contributing provides process | error (mandatory) | 1.0 | {{ results['readme-sec-contrib-002'].previous_status \| default('—') }} | {{ results['readme-sec-contrib-002'].status }} | {{ results['readme-sec-contrib-002'].trend_display }} | {{ results['readme-sec-contrib-002'].evidence \| default('—') }} |
| readme-sec-contrib-003 | Contributing defines PR process | warning (recommended) | 0.5 | {{ results['readme-sec-contrib-003'].previous_status \| default('—') }} | {{ results['readme-sec-contrib-003'].status }} | {{ results['readme-sec-contrib-003'].trend_display }} | {{ results['readme-sec-contrib-003'].evidence \| default('—') }} |

## 14. Configuration — weight 3.0 — optional

**Why this matters:** Configuration documents the environment variables and config files that control runtime behavior. Without it, users must read source code to discover what's configurable.

**Section Score: {{ sections.configuration.score }} / 100** ({{ sections.configuration.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-configuration-001 | Configuration section exists | error (mandatory) | 1.5 | {{ results['readme-sec-configuration-001'].previous_status \| default('—') }} | {{ results['readme-sec-configuration-001'].status }} | {{ results['readme-sec-configuration-001'].trend_display }} | {{ results['readme-sec-configuration-001'].evidence \| default('—') }} |
| readme-sec-configuration-002 | Configuration has substantive content | error (mandatory) | 1.0 | {{ results['readme-sec-configuration-002'].previous_status \| default('—') }} | {{ results['readme-sec-configuration-002'].status }} | {{ results['readme-sec-configuration-002'].trend_display }} | {{ results['readme-sec-configuration-002'].evidence \| default('—') }} |
| readme-sec-configuration-003 | Configuration is specific to this project | warning (recommended) | 0.5 | {{ results['readme-sec-configuration-003'].previous_status \| default('—') }} | {{ results['readme-sec-configuration-003'].status }} | {{ results['readme-sec-configuration-003'].trend_display }} | {{ results['readme-sec-configuration-003'].evidence \| default('—') }} |

## 15. License — weight 3.0 — optional

**Why this matters:** License states the exact license name with a link to the full text. Without it, the legal terms of use are ambiguous, which may block adoption in commercial or regulated environments.

**Section Score: {{ sections.license.score }} / 100** ({{ sections.license.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-sec-license-001 | License section exists | error (mandatory) | 1.5 | {{ results['readme-sec-license-001'].previous_status \| default('—') }} | {{ results['readme-sec-license-001'].status }} | {{ results['readme-sec-license-001'].trend_display }} | {{ results['readme-sec-license-001'].evidence \| default('—') }} |
| readme-sec-license-002 | License has substantive content | error (mandatory) | 1.0 | {{ results['readme-sec-license-002'].previous_status \| default('—') }} | {{ results['readme-sec-license-002'].status }} | {{ results['readme-sec-license-002'].trend_display }} | {{ results['readme-sec-license-002'].evidence \| default('—') }} |
| readme-sec-license-003 | License is specific to this project | warning (recommended) | 0.5 | {{ results['readme-sec-license-003'].previous_status \| default('—') }} | {{ results['readme-sec-license-003'].status }} | {{ results['readme-sec-license-003'].trend_display }} | {{ results['readme-sec-license-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 15 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | readme |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/15-readme/*.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
