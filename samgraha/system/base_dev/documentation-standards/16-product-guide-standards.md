# Product Guide Standard

## Table of Contents

> *Deterministic rules for this domain: `audit/deterministic/document/16-product-guide.yaml`*

- [Purpose](#purpose)
  - [Template](#template)
- [Title](#title)
  - [Template](#template)
- [Content](#content)
  - [Template](#template)
- [Product Context](#product-context)
  - [Template](#template)
- [Public Contract](#public-contract)
  - [Template](#template)
- [Related](#related)
  - [Template](#template)
- [Required Sections](#required-sections)
- [Goals](#goals)
- [Non-Goals](#non-goals)
- [Success Criteria](#success-criteria)
- [Responsibilities](#responsibilities)
- [Scope](#scope)
- [Out of Scope](#out-of-scope)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Traceability](#traceability)
- [Relationships](#relationships)
- [Required Characteristics](#required-characteristics)
- [Generation Rules](#generation-rules)
- [Enhancement Rules](#enhancement-rules)
- [Audit Rules](#audit-rules)
- [Summary](#summary)
- [Documentation Folder](#documentation-folder)
- [Usage](#usage)
- [Standard Cross-References](#standard-cross-references)

---


## Purpose

> *Structural rules: `audit/deterministic/section/16-product-guide/03-purpose.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
[One sentence or short paragraph describing the user-facing problem this topic solves.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> This topic explains how to configure automatic backups so your data is never lost.

**Incorrect:**
> This topic covers the backup feature.
> *Why wrong: Vague and passive — describes what the topic "covers" rather than the user-facing problem it solves.*

### Writing Guidance

- **Tone:** conversational
- **Voice:** second person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Write from the reader's perspective — "you" language; lead with the benefit or outcome the user gets; keep to one sentence or a short paragraph
- **Don't:** Use passive voice or vague phrasing like "this topic covers…"; describe internal implementation details or engineering rationale; exceed two sentences

This document defines the standard for Product Guide documentation — the product docs shipped in `help.db` next to the binary, written for end users and for an LLM looking up how to use Samgraha or how to interpret an error.

Product Guide topics explain **how to use the finished product**. They do not define product vision, architecture, engineering rationale, or any other domain's reasoning — those belong to their own standards, and Product Guide is written last, after everything else exists, because it can't be accurate until the product it describes is finished.

---

## Title

> *Structural rules: `audit/deterministic/section/16-product-guide/01-title.yaml`*

### Template

> **minimum_content:** 1 line
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
# [Command or Concept Name]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> # Configure Automatic Backups

**Incorrect:**
> # The Backup System — Everything You Need To Know
> *Why wrong: Over 60 characters, uses marketing language, and tries to be a catch-all instead of naming the specific command or concept.*

### Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Use the exact command name or concept name as written in the shipped product; keep under 60 characters; describe the action, not the system
- **Don't:** Use marketing adjectives or superlatives ("Everything You Need To Know"); include parenthetical qualifiers or version numbers in the title; use "How to" prefix when the command name already implies action

<!-- TODO: Add content for this section. -->

---

## Content

> *Structural rules: `audit/deterministic/section/16-product-guide/02-body.yaml`*

### Template

> **minimum_content:** 2 subsections
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
## [Feature or Workflow Name]

[1-2 sentences explaining what this feature does and when to use it.]

### How It Works

[Step-by-step instructions or explanation with concrete examples.]

### Examples

[Concrete usage examples showing expected input and output.]
```

**Required subsections:** How It Works, Examples
**Optional subsections:** Tips, Troubleshooting, Limitations
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> ## Configure Automatic Backups
>
> Backups run daily at 02:00 by default. You can change the schedule or target directory.
>
> ### How It Works
>
> The backup service reads the `[backup]` section in your config file and writes compressed snapshots to the specified directory.
>
> ### Examples
>
> Run `app backup --now` to trigger an immediate backup. Output: `Backup saved to /data/backups/2026-07-11.snap`.

**Incorrect:**
> ## Backup
>
> The backup feature is very powerful and supports many use cases. See the source code for details on how it works internally.
> *Why wrong: No How It Works or Examples subsections, references source code instead of providing actionable user instructions, and lacks concrete examples.*

### Writing Guidance

- **Tone:** conversational
- **Voice:** second person
- **Structure:** mixed
- **Audience:** AI agent
- **Do:** Start with the user's goal in one sentence before explaining how; provide at least one concrete command or code example with expected output; use headers (How It Works, Examples) to make the content scannable
- **Don't:** Write long paragraphs without subheadings; reference source code, internal architecture, or implementation details; use passive constructions that obscure who performs the action

<!-- TODO: Add content for this section. -->

---

## Product Context

> *Structural rules: `audit/deterministic/section/16-product-guide/07-product_context.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
## Product Context

[Prerequisites, default behavior, and version-specific context the reader needs before using this feature.]

- **Prerequisites:** [What must already be installed or configured]
- **Default behavior:** [What happens if the user doesn't specify options]
- **Version:** [Applicable product version, if version-specific]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> - **Prerequisites:** App Server v2.0 or later must be installed
> - **Default behavior:** Backups run daily at 02:00 to the default directory
> - **Version:** Behavior changed in v2.3 — earlier versions require manual scheduling

**Incorrect:**
> Backup is a useful feature that helps protect your data. It was introduced in v1.0 and has been improved many times since then.
> *Why wrong: Reads like marketing copy — does not state prerequisites, defaults, or version-specific context the reader needs before using the feature.*

### Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** List prerequisites as explicit bullet points with exact version numbers; state the default behavior concisely so the reader knows what happens without intervention; note any version-specific behavioral changes
- **Don't:** Write promotional or historical prose ("has been improved many times"); omit minimum version requirements; mix aspirational language with factual prerequisites

<!-- TODO: Add content for this section. -->

---

## Public Contract

> *Structural rules: `audit/deterministic/section/16-product-guide/08-public_contract.yaml`*

### Template

> **minimum_content:** 1 subsection
> **length_guidance:** extensive
> **diagram_requirements:** none

```markdown
## Public Contract

### CLI Interface

| Flag | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `--flag` | string | — | yes | [Description] |

### Inputs

| Input | Type | Description |
|-------|------|-------------|
| [name] | [type] | [Description] |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| [name] | [type] | [Description] |

### Error Conditions

| Error | Cause | Resolution |
|-------|-------|------------|
| `[error message]` | [What went wrong] | [How to fix it] |
```

**Required subsections:** CLI Interface or Inputs (at least one), Error Conditions
**Optional subsections:** Config Keys, MCP Parameters
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> ### CLI Interface
>
> | Flag | Type | Default | Required | Description |
> |------|------|---------|----------|-------------|
> | `--dir` | string | `/data/backups` | no | Target directory for snapshots |
>
> ### Error Conditions
>
> | Error | Cause | Resolution |
> |-------|-------|------------|
> | `Backup directory not writable` | Target directory lacks write permissions | Run `chmod u+w` on the target directory |

**Incorrect:**
> The backup command accepts a directory flag and writes files. Errors may occur if the directory is not writable.
> *Why wrong: No structured tables, missing types/defaults/required status, and error conditions are buried in prose instead of listed with causes and resolutions.*

### Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Use structured tables for every parameter, input, output, and error condition; include type, default value, and required/optional status for every flag; list error conditions with a Resolution column the user can act on
- **Don't:** Bury interface details in prose paragraphs; omit type or default information; list error messages without actionable resolutions

<!-- TODO: Add content for this section. -->

---

## Related

> *Structural rules: `audit/deterministic/section/16-product-guide/06-related.yaml`*

### Template

> **minimum_content:** 1 link
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
## Related

- [Topic Name](link) — brief label explaining why this is relevant
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** at least one valid link with descriptive label

### Examples

**Correct:**
> - [Scheduled Backups](scheduled-backups.md) — how to change the backup schedule
> - [Restore From Backup](restore-backup.md) — recovering data from a saved snapshot

**Incorrect:**
> - [Some Other Topic](broken-link.md)
> *Why wrong: Link target does not resolve, and the label gives no indication of why the reader should follow it.*

### Writing Guidance

- **Tone:** conversational
- **Voice:** second person
- **Structure:** bullet lists
- **Audience:** AI agent
- **Do:** Provide at least one cross-reference with a brief label explaining relevance; link to adjacent Product Guide topics the reader is likely to need next; keep labels descriptive enough to stand alone without context
- **Don't:** Include links without labels or with vague labels ("see also"); link to topics outside the Product Guide domain without clear relevance; duplicate content from the linked topic in the description

---

## Required Sections

Every Product Guide topic must contain the following sections.
Sections are identified by heading text; the compiler maps each to a semantic type.

| Section | semantic_type | Required | Aliases | Content Requirements |
|---------|--------------|----------|---------|----------------------|
| Title | `title` | ✓ | Title | Concise, descriptive heading identifying the command, concept, or workflow; under 60 characters; no marketing language |
| Content | `body` | ✓ | Body, Details | Step-by-step instructions or explanations with concrete examples; actionable information organized with headers for scannability |
| Purpose | `purpose` | | Overview | Single sentence or short paragraph describing the user-facing problem this topic solves |
| Product Context | `product-context` | | Context, Background | Prerequisites, default configurations, and product-version context the reader needs before using the feature |
| Public Contract | `public-contract` | | Interface, API | All inputs, outputs, flags, config keys, and error conditions with types, defaults, and required/optional status |
| Related | `related` | | See Also, References, Cross-References | At least one cross-reference with a brief label explaining relevance; links to adjacent Product Guide topics or related standards |

Section headings are case-insensitive. Sections not listed here are stored as `generic` type — preserved but not queryable by type.

---

## Goals

Product Guide aims to:

* Give end users and LLMs a single authoritative place to learn product usage.
* Stay accurate to the shipped product by being written last, not speculatively.
* Keep each topic small enough to be useful as a standalone lookup.

---

## Non-Goals

Product Guide does not define:

* Product Vision or Philosophy
* Architecture or Engineering rationale
* Security threat models
* Feature specifications or technical design
* Source code

These responsibilities belong to other documentation standards.

---

## Success Criteria

Product Guide is successful when:

* A user or LLM can find how to do something without reading source code.
* Every CLI/MCP/config surface has corresponding coverage.
* Topics stay current as the product changes (Accuracy check catches drift).
* A reader lands on the right topic within one or two navigation steps.

---

## Responsibilities

Product Guide is responsible for:

* Explaining how to use a specific command, concept, or workflow
* Documenting the public contract of a CLI/MCP surface (inputs, outputs, error conditions)
* Routing a reader from a symptom (an error, a question) to the right topic
* Staying scoped to one concept per topic — small, single-purpose files

Product Guide is the only domain written after the product is finished, not before.

---

## Scope

Product Guide may describe:

* How to install, configure, and run the product
* What a specific command, flag, or config option does
* Common workflows end to end
* How to interpret a specific error message
* Troubleshooting steps for a specific symptom

Every topic should stay single-purpose — one command, one concept, one guide.

---

## Out of Scope

Product Guide must not describe:

* Product Vision or strategy
* Philosophy or guiding principles
* Architecture or system design
* Engineering rationale or technology choices
* Security threat models
* Feature specifications or technical design
* Source code

These belong to their own documentation standards. Product Guide only explains usage of what already exists.

---

## Inputs

Product Guide derives from the finished product itself — every other domain, once built:

* Vision — for framing what the product is, at a level an end user needs
* Feature / Feature Design — for what a workflow is supposed to do
* Build — for install/run instructions that match what's actually shippable
* README — for the high-level entry point Product Guide expands on

Product Guide should not derive from plans or drafts — only from what's actually shipped.

---

## Outputs

Product Guide provides:

* End-user-facing explanations of how to use the product
* LLM-consumable reference for tool-use and error interpretation (`help.db`)
* The corpus validated by the Product Guide Audit Pipeline (Coverage, Navigation, Quality, Accuracy)

---

## Traceability

```text
Everything else (Vision … Build, README)
              │
              ↓
        Product Guide
```

Product Guide has no formal `relationship(...)` entries in `crates/standards/src/builtin.rs` — it's flat, built-in content, the same as `standards` itself. It doesn't participate in the tiered derivation graph the other 14 domains form; it references all of it informally, through prose and the freeform `Related` section on each topic, rather than through a machine-readable edge. See `00-domain-relationships.md`.

---

## Relationships

Product Guide declares no `relationship(...)` entries — by design, matching how `help` is documented in `00-domain-relationships.md`. Individual topics link elsewhere through their own `Related` section instead of a domain-level graph edge.

---

## Required Characteristics

A Product Guide topic should be:

* Single-purpose — one command, concept, or guide per topic
* Accurate to the shipped product, not aspirational
* Scannable — a reader should find the answer without reading the whole topic
* LLM-consumable — structured enough for `help.db` lookups, not just prose

---

## Generation Rules

When generating Product Guide topics:

* Write for the finished product, not for planned features.
* One topic per command, concept, or workflow.
* Lead with what the user wants to do, not with what the tool is.
* Document the public contract: inputs, outputs, error conditions.
* Use concrete examples over abstract descriptions.
* Keep topics short enough to scan in under a minute.

---

## Enhancement Rules

When enhancing Product Guide topics:

* Verify accuracy against the current shipped product.
* Remove references to features that no longer exist.
* Add topics for new CLI/MCP surfaces not yet covered.
* Improve scannability — headers, short paragraphs, concrete examples.
* Preserve the single-purpose scope of each topic.
* Update cross-references when related topics change.

---

## Audit Rules

| ID | Check | Severity |
|----|-------|----------|
| `help-001` | Has title | error |
| `help-002` | Has purpose | suggestion |
| `help-003` | Has content | error |
| `help-004` | Has product context | suggestion |
| `help-005` | Has public contract | warning |

The corpus is also validated by the **Product Guide Audit Pipeline** (`samgraha audit --pipeline help`) — a separate, deeper check spanning Coverage, Navigation, Quality, and Accuracy against the actual CLI/MCP/config surface, not just per-topic section presence. See [Product Guide Audit Pipeline](../../raw/product-guide/concepts/help-audit.md).

---

## Summary

Product Guide is the end-user- and LLM-facing usage documentation for the finished product — commands, workflows, error interpretation, and troubleshooting — written last, after every other domain has settled, because it can only be accurate once the product it describes actually exists. It declares no formal relationships; it references everything informally instead.

---

## Documentation Folder

Product Guide documents live under:

```text
docs/raw/product-guide/
```

---

## Usage

Written by whoever ships a feature that needs end-user-facing explanation — a help topic is small and single-purpose, one file per concept/command/guide, never a catch-all. Use `samgraha compile --domain help` (done automatically by the release build for the shipped `docs/raw/product-guide/` tree) and `samgraha audit --domain help` to confirm every topic has a title and body before it ships. Two packaging profiles exist: `quickref` (title + body only, for compact contexts) and `full` (all six sections).

## Standard Cross-References

- [Readme Standard](15-readme-standards.md) — the entry point Product Guide expands on
- [Build Standard](14-build-standards.md) — install/run instructions Product Guide must stay accurate to
- [Standards Reference Standard](standards.md) — how this standard itself is documented
- `docs/raw/product-guide/index.md` — the actual Product Guide content tree's table of contents (not this file — this one documents the *standard*, that one is the *content*)
