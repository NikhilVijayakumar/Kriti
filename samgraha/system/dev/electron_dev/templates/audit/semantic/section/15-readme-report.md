# Semantic Section Report — README

**Document:** {{ document_path }}
**Standard:** `documentation-standards/15-readme-standards.md`
**Rubric Files:** `audit/semantic/section/15-readme/*.md`
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
| 1 | Project Name | **required** | {{ sections.project_name.score }} / 100 | {{ sections.project_name.previous_score | default('—') }} | {{ sections.project_name.trend_display }} |
| 2 | Short Description | **required** | {{ sections.short_description.score }} / 100 | {{ sections.short_description.previous_score | default('—') }} | {{ sections.short_description.trend_display }} |
| 3 | Overview | **required** | {{ sections.overview.score }} / 100 | {{ sections.overview.previous_score | default('—') }} | {{ sections.overview.trend_display }} |
| 4 | Purpose | **required** | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Key Capabilities | **required** | {{ sections.key_capabilities.score }} / 100 | {{ sections.key_capabilities.previous_score | default('—') }} | {{ sections.key_capabilities.trend_display }} |
| 6 | Repository Structure | **required** | {{ sections.repository_structure.score }} / 100 | {{ sections.repository_structure.previous_score | default('—') }} | {{ sections.repository_structure.trend_display }} |
| 7 | Documentation Structure | **required** | {{ sections.documentation_structure.score }} / 100 | {{ sections.documentation_structure.previous_score | default('—') }} | {{ sections.documentation_structure.trend_display }} |
| 8 | Getting Started | **required** | {{ sections.getting_started.score }} / 100 | {{ sections.getting_started.previous_score | default('—') }} | {{ sections.getting_started.trend_display }} |
| 9 | Installation | **required** | {{ sections.installation.score }} / 100 | {{ sections.installation.previous_score | default('—') }} | {{ sections.installation.trend_display }} |
| 10 | Build | **required** | {{ sections.build.score }} / 100 | {{ sections.build.previous_score | default('—') }} | {{ sections.build.trend_display }} |
| 11 | Usage | **required** | {{ sections.usage.score }} / 100 | {{ sections.usage.previous_score | default('—') }} | {{ sections.usage.trend_display }} |
| 12 | Development | **required** | {{ sections.development.score }} / 100 | {{ sections.development.previous_score | default('—') }} | {{ sections.development.trend_display }} |
| 13 | Contributing | **required** | {{ sections.contributing.score }} / 100 | {{ sections.contributing.previous_score | default('—') }} | {{ sections.contributing.trend_display }} |
| 14 | Configuration | optional | {{ sections.configuration.score }} / 100 | {{ sections.configuration.previous_score | default('—') }} | {{ sections.configuration.trend_display }} |
| 15 | License | optional | {{ sections.license.score }} / 100 | {{ sections.license.previous_score | default('—') }} | {{ sections.license.trend_display }} |
| — | Generic (unmatched sections) | n/a | {{ sections.generic.score }} / 100 | {{ sections.generic.previous_score | default('—') }} | {{ sections.generic.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Project Name — `section/15-readme/01-project_name.md` — **required**

**Why this matters:** Project Name states the canonical name exactly as it appears in package manifests. It exists so every reference to the project resolves to one unambiguous name.

**Section Score: {{ sections.project_name.score }} / 100** ({{ sections.project_name.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 60 | {{ results['project_name.C1'].previous_passed_display | default('—') }} | {{ results['project_name.C1'].passed_display }} | {{ results['project_name.C1'].trend_display }} | {{ results['project_name.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 40 | {{ results['project_name.C2'].previous_passed_display | default('—') }} | {{ results['project_name.C2'].passed_display }} | {{ results['project_name.C2'].trend_display }} | {{ results['project_name.C2'].evidence.excerpt | default('—') }} |

C1: section contains only the canonical name, no description. C2: name matches package manifest(s).

## 2. Short Description — `02-short_description.md` — **required**

**Why this matters:** Short Description is the one/two-sentence answer to "what is this and who is it for" — the first thing a reader evaluates before deciding to read further.

**Section Score: {{ sections.short_description.score }} / 100** ({{ sections.short_description.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['short_description.C1'].previous_passed_display | default('—') }} | {{ results['short_description.C1'].passed_display }} | {{ results['short_description.C1'].trend_display }} | {{ results['short_description.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['short_description.C2'].previous_passed_display | default('—') }} | {{ results['short_description.C2'].passed_display }} | {{ results['short_description.C2'].trend_display }} | {{ results['short_description.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['short_description.C3'].previous_passed_display | default('—') }} | {{ results['short_description.C3'].passed_display }} | {{ results['short_description.C3'].trend_display }} | {{ results['short_description.C3'].evidence.excerpt | default('—') }} |

C1: under 200 characters, 1-2 sentences. C2: states what it does and who it's for. C3: no technology stack, install steps, or version/feature counts.

## 3. Overview — `03-overview.md` — **required**

**Why this matters:** Overview explains the problem the project solves and the approach taken, at a level a new reader can absorb before touching code. It bridges Short Description and the detailed docs.

**Section Score: {{ sections.overview.score }} / 100** ({{ sections.overview.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['overview.C1'].previous_passed_display | default('—') }} | {{ results['overview.C1'].passed_display }} | {{ results['overview.C1'].trend_display }} | {{ results['overview.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['overview.C2'].previous_passed_display | default('—') }} | {{ results['overview.C2'].passed_display }} | {{ results['overview.C2'].trend_display }} | {{ results['overview.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['overview.C3'].previous_passed_display | default('—') }} | {{ results['overview.C3'].passed_display }} | {{ results['overview.C3'].trend_display }} | {{ results['overview.C3'].evidence.excerpt | default('—') }} |

C1: problem stated before solution/approach. C2: no technology stack or architecture-level detail. C3: references Vision or Key Capabilities for deeper context.

## 4. Purpose — `04-purpose.md` — **required**

**Why this matters:** Purpose defines what the README is and is not — the boundary between README and the rest of the documentation ecosystem.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 50 | {{ results['purpose.C1'].previous_passed_display | default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display | default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['purpose.C3'].previous_passed_display | default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt | default('—') }} |

C1: explicitly states README's scope boundary (what it is, what it is not). C2: references the broader documentation ecosystem rather than duplicating it. C3: boundary is specific (named exclusions), not vague.

## 5. Key Capabilities — `05-key_capabilities.md` — **required**

**Why this matters:** Key Capabilities is a scannable list of what the project can do, letting a reader assess fit in seconds. It stays at the capability level.

**Section Score: {{ sections.key_capabilities.score }} / 100** ({{ sections.key_capabilities.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['key_capabilities.C1'].previous_passed_display | default('—') }} | {{ results['key_capabilities.C1'].passed_display }} | {{ results['key_capabilities.C1'].trend_display }} | {{ results['key_capabilities.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['key_capabilities.C2'].previous_passed_display | default('—') }} | {{ results['key_capabilities.C2'].passed_display }} | {{ results['key_capabilities.C2'].trend_display }} | {{ results['key_capabilities.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['key_capabilities.C3'].previous_passed_display | default('—') }} | {{ results['key_capabilities.C3'].passed_display }} | {{ results['key_capabilities.C3'].trend_display }} | {{ results['key_capabilities.C3'].evidence.excerpt | default('—') }} |

C1: 3-7 capabilities listed as scannable phrases. C2: no implementation details, versions, or test counts. C3: capabilities are non-overlapping and independently understandable.

## 6. Repository Structure — `06-repository_structure.md` — **required**

**Why this matters:** Repository Structure orients a new contributor to the directory layout at a glance — top-level directories and their purpose.

**Section Score: {{ sections.repository_structure.score }} / 100** ({{ sections.repository_structure.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['repository_structure.C1'].previous_passed_display | default('—') }} | {{ results['repository_structure.C1'].passed_display }} | {{ results['repository_structure.C1'].trend_display }} | {{ results['repository_structure.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['repository_structure.C2'].previous_passed_display | default('—') }} | {{ results['repository_structure.C2'].passed_display }} | {{ results['repository_structure.C2'].trend_display }} | {{ results['repository_structure.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['repository_structure.C3'].previous_passed_display | default('—') }} | {{ results['repository_structure.C3'].passed_display }} | {{ results['repository_structure.C3'].trend_display }} | {{ results['repository_structure.C3'].evidence.excerpt | default('—') }} |

C1: major directories listed with purpose, not files. C2: directory list matches actual repository contents. C3: descriptions are purpose-focused, not implementation-focused.

## 7. Documentation Structure — `07-documentation_structure.md` — **required**

**Why this matters:** Documentation Structure tells a reader where the rest of the documentation lives and in what order to read it.

**Section Score: {{ sections.documentation_structure.score }} / 100** ({{ sections.documentation_structure.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['documentation_structure.C1'].previous_passed_display | default('—') }} | {{ results['documentation_structure.C1'].passed_display }} | {{ results['documentation_structure.C1'].trend_display }} | {{ results['documentation_structure.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['documentation_structure.C2'].previous_passed_display | default('—') }} | {{ results['documentation_structure.C2'].passed_display }} | {{ results['documentation_structure.C2'].trend_display }} | {{ results['documentation_structure.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['documentation_structure.C3'].previous_passed_display | default('—') }} | {{ results['documentation_structure.C3'].passed_display }} | {{ results['documentation_structure.C3'].trend_display }} | {{ results['documentation_structure.C3'].evidence.excerpt | default('—') }} |

C1: documentation directories listed with purpose. C2: organization principle stated. C3: concrete navigation/reading-order guidance provided.

## 8. Getting Started — `08-getting_started.md` — **required**

**Why this matters:** Getting Started guides a user from zero to running the project. It must be step-by-step, copy-paste safe, and resolve all dependencies.

**Section Score: {{ sections.getting_started.score }} / 100** ({{ sections.getting_started.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['getting_started.C1'].previous_passed_display | default('—') }} | {{ results['getting_started.C1'].passed_display }} | {{ results['getting_started.C1'].trend_display }} | {{ results['getting_started.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['getting_started.C2'].previous_passed_display | default('—') }} | {{ results['getting_started.C2'].passed_display }} | {{ results['getting_started.C2'].trend_display }} | {{ results['getting_started.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['getting_started.C3'].previous_passed_display | default('—') }} | {{ results['getting_started.C3'].passed_display }} | {{ results['getting_started.C3'].trend_display }} | {{ results['getting_started.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['getting_started.C4'].previous_passed_display | default('—') }} | {{ results['getting_started.C4'].passed_display }} | {{ results['getting_started.C4'].trend_display }} | {{ results['getting_started.C4'].evidence.excerpt | default('—') }} |

C1: prerequisites listed with versions. C2: copy-paste safe commands. C3: verification step present. C4: troubleshooting section included.

## 9. Installation — `09-installation.md` — **required**

**Why this matters:** Installation gets the project onto a machine — prerequisites and exact commands, with a way to verify it worked.

**Section Score: {{ sections.installation.score }} / 100** ({{ sections.installation.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['installation.C1'].previous_passed_display | default('—') }} | {{ results['installation.C1'].passed_display }} | {{ results['installation.C1'].trend_display }} | {{ results['installation.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 35 | {{ results['installation.C2'].previous_passed_display | default('—') }} | {{ results['installation.C2'].passed_display }} | {{ results['installation.C2'].trend_display }} | {{ results['installation.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['installation.C3'].previous_passed_display | default('—') }} | {{ results['installation.C3'].passed_display }} | {{ results['installation.C3'].trend_display }} | {{ results['installation.C3'].evidence.excerpt | default('—') }} |

C1: prerequisites listed with version numbers. C2: step-by-step commands, copy-paste safe. C3: verification step with expected output.

## 10. Build — `10-build.md` — **required**

**Why this matters:** Build documents how to produce a build artifact from source — prerequisites, exact commands, and where the output lands.

**Section Score: {{ sections.build.score }} / 100** ({{ sections.build.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['build.C1'].previous_passed_display | default('—') }} | {{ results['build.C1'].passed_display }} | {{ results['build.C1'].trend_display }} | {{ results['build.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 35 | {{ results['build.C2'].previous_passed_display | default('—') }} | {{ results['build.C2'].passed_display }} | {{ results['build.C2'].trend_display }} | {{ results['build.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['build.C3'].previous_passed_display | default('—') }} | {{ results['build.C3'].passed_display }} | {{ results['build.C3'].trend_display }} | {{ results['build.C3'].evidence.excerpt | default('—') }} |

C1: build prerequisites listed with versions. C2: specific, runnable build commands. C3: expected output/artifact location described.

## 11. Usage — `11-usage.md` — **required**

**Why this matters:** Usage demonstrates the project's primary functions with real, runnable examples and their expected output — proof the thing works.

**Section Score: {{ sections.usage.score }} / 100** ({{ sections.usage.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['usage.C1'].previous_passed_display | default('—') }} | {{ results['usage.C1'].passed_display }} | {{ results['usage.C1'].trend_display }} | {{ results['usage.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['usage.C2'].previous_passed_display | default('—') }} | {{ results['usage.C2'].passed_display }} | {{ results['usage.C2'].trend_display }} | {{ results['usage.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['usage.C3'].previous_passed_display | default('—') }} | {{ results['usage.C3'].passed_display }} | {{ results['usage.C3'].trend_display }} | {{ results['usage.C3'].evidence.excerpt | default('—') }} |

C1: working command/code examples for primary functions. C2: expected output shown. C3: common workflows demonstrated beyond a single command.

## 12. Development — `12-development.md` — **required**

**Why this matters:** Development gets a contributor from clone to running the test suite and understanding the workflow — the audience is someone about to change code.

**Section Score: {{ sections.development.score }} / 100** ({{ sections.development.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['development.C1'].previous_passed_display | default('—') }} | {{ results['development.C1'].passed_display }} | {{ results['development.C1'].trend_display }} | {{ results['development.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 40 | {{ results['development.C2'].previous_passed_display | default('—') }} | {{ results['development.C2'].passed_display }} | {{ results['development.C2'].trend_display }} | {{ results['development.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['development.C3'].previous_passed_display | default('—') }} | {{ results['development.C3'].passed_display }} | {{ results['development.C3'].trend_display }} | {{ results['development.C3'].evidence.excerpt | default('—') }} |

C1: Local Setup has specific setup commands. C2: Running Tests has an actual, correct test command. C3: Workflow references coding standards.

## 13. Contributing — `13-contributing.md` — **required**

**Why this matters:** Contributing tells an external contributor how to submit a change that gets accepted — process, review expectations, and quality bar.

**Section Score: {{ sections.contributing.score }} / 100** ({{ sections.contributing.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['contributing.C1'].previous_passed_display | default('—') }} | {{ results['contributing.C1'].passed_display }} | {{ results['contributing.C1'].trend_display }} | {{ results['contributing.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['contributing.C2'].previous_passed_display | default('—') }} | {{ results['contributing.C2'].passed_display }} | {{ results['contributing.C2'].trend_display }} | {{ results['contributing.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['contributing.C3'].previous_passed_display | default('—') }} | {{ results['contributing.C3'].passed_display }} | {{ results['contributing.C3'].trend_display }} | {{ results['contributing.C3'].evidence.excerpt | default('—') }} |

C1: Contribution Process is a concrete, sequential workflow. C2: Code Review expectations stated (approvals, what's checked). C3: Quality Standards specific enough to self-check against.

## 14. Configuration — `14-configuration.md` — optional

**Why this matters:** Configuration documents the environment variables and config files that control runtime behavior — each with a default, valid values, and a working example.

**Section Score: {{ sections.configuration.score }} / 100** ({{ sections.configuration.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['configuration.C1'].previous_passed_display | default('—') }} | {{ results['configuration.C1'].passed_display }} | {{ results['configuration.C1'].trend_display }} | {{ results['configuration.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['configuration.C2'].previous_passed_display | default('—') }} | {{ results['configuration.C2'].passed_display }} | {{ results['configuration.C2'].trend_display }} | {{ results['configuration.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['configuration.C3'].previous_passed_display | default('—') }} | {{ results['configuration.C3'].passed_display }} | {{ results['configuration.C3'].trend_display }} | {{ results['configuration.C3'].evidence.excerpt | default('—') }} |

C1: configuration options listed with defaults (table form). C2: valid values stated per option. C3: working example provided.

## 15. License — `15-license.md` — optional

**Why this matters:** License states the exact license name with a direct link to the full text and copyright notice. Legal terms of use must be unambiguous.

**Section Score: {{ sections.license.score }} / 100** ({{ sections.license.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 50 | {{ results['license.C1'].previous_passed_display | default('—') }} | {{ results['license.C1'].passed_display }} | {{ results['license.C1'].trend_display }} | {{ results['license.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['license.C2'].previous_passed_display | default('—') }} | {{ results['license.C2'].passed_display }} | {{ results['license.C2'].trend_display }} | {{ results['license.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 20 | {{ results['license.C3'].previous_passed_display | default('—') }} | {{ results['license.C3'].passed_display }} | {{ results['license.C3'].trend_display }} | {{ results['license.C3'].evidence.excerpt | default('—') }} |

C1: specific license name stated. C2: direct link to full license text provided. C3: copyright notice included.

## Generic — `generic.md` (sections with no matching semantic_type)

**Why this matters:** Catches README-relevant content an author wrote under a heading that doesn't match any of the 15 named section types above — still judged for relevance and non-duplication, not given a free pass for being unclassified.

**Section Score: {{ sections.generic.score }} / 100** ({{ sections.generic.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 20 | {{ results['generic.C1'].previous_passed_display | default('—') }} | {{ results['generic.C1'].passed_display }} | {{ results['generic.C1'].trend_display }} | {{ results['generic.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 20 | {{ results['generic.C2'].previous_passed_display | default('—') }} | {{ results['generic.C2'].passed_display }} | {{ results['generic.C2'].trend_display }} | {{ results['generic.C2'].evidence.excerpt | default('—') }} |
| C3 | mandatory | 20 | {{ results['generic.C3'].previous_passed_display | default('—') }} | {{ results['generic.C3'].passed_display }} | {{ results['generic.C3'].trend_display }} | {{ results['generic.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['generic.C4'].previous_passed_display | default('—') }} | {{ results['generic.C4'].passed_display }} | {{ results['generic.C4'].trend_display }} | {{ results['generic.C4'].evidence.excerpt | default('—') }} |
| C5 | recommended | 20 | {{ results['generic.C5'].previous_passed_display | default('—') }} | {{ results['generic.C5'].passed_display }} | {{ results['generic.C5'].trend_display }} | {{ results['generic.C5'].evidence.excerpt | default('—') }} |

C1: project name and one-liner present. C2: target audience identified. C3: getting-started path completable in ≤5 minutes; license stated. C4: technology stack noted. C5: problem statement clear; troubleshooting section present.

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
| Domain | readme |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/15-readme/*.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
