# Product Guide Document — Generation Template

> **Domain:** product-guide
> **Source standard:** `documentation-standards/16-product-guide-standards.md`
> **Coherence source:** `audit/semantic/document/16-product-guide.md`
> **Relationships:** `audit/deterministic/document/16-product-guide-relationships.yaml`

Generate a complete Product Guide document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Title | `title` | ✓ | Concise, descriptive heading under 60 characters |
| 2 | Body | `body` | ✓ | Step-by-step instructions with How It Works and Examples |
| 3 | Purpose | `purpose` | | User-facing problem this topic solves |
| 4 | Product Context | `product-context` | | Prerequisites, defaults, version-specific context |
| 5 | Public Contract | `public-contract` | | CLI/MCP/config inputs, outputs, error conditions |
| 6 | Related | `related` | | Cross-references with descriptive labels |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/16-product-guide.md` Engineering Intent.

Sections within a Product Guide topic must describe the same command, concept, or workflow without contradicting each other. Specifically:

- Title must name the exact command or concept described in Content
- Content examples must be achievable with the flags and inputs listed in Public Contract
- Product Context prerequisites must be consistent with what Content examples assume
- Error Conditions in Public Contract must correspond to failure modes described in Content
- Related links must resolve to adjacent Product Guide topics or related standards

If any section would reference a flag, command, or behavior not present in another section, reconcile before outputting.

## Sections

---

### 1. Title

**Template:**

```markdown
# [Command or Concept Name]
```

**Correct example:**
> # Configure Automatic Backups

**Incorrect example:**
> # The Backup System — Everything You Need To Know
> *Why wrong: Over 60 characters, uses marketing language, and tries to be a catch-all instead of naming the specific command or concept.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Use the exact command name or concept name as written in the shipped product; keep under 60 characters; describe the action, not the system
- **Don't:** Use marketing adjectives or superlatives ("Everything You Need To Know"); include parenthetical qualifiers or version numbers in the title; use "How to" prefix when the command name already implies action

---

### 2. Body

**Template:**

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

**Correct example:**
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

**Incorrect example:**
> ## Backup
>
> The backup feature is very powerful and supports many use cases. See the source code for details on how it works internally.
> *Why wrong: No How It Works or Examples subsections, references source code instead of providing actionable user instructions, and lacks concrete examples.*

**Writing guidance:**
- **Tone:** conversational
- **Voice:** second person
- **Structure:** mixed
- **Audience:** AI agent
- **Do:** Start with the user's goal in one sentence before explaining how; provide at least one concrete command or code example with expected output; use headers (How It Works, Examples) to make the content scannable
- **Don't:** Write long paragraphs without subheadings; reference source code, internal architecture, or implementation details; use passive constructions that obscure who performs the action

---

### 3. Purpose

**Template:**

```markdown
## Purpose

[One sentence or short paragraph describing the user-facing problem this topic solves.]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* user-facing problem: what the reader wants to accomplish and why this topic helps. The meta-level "This document defines the standard for Product Guide..." language belongs in the standard itself, not in a generated document.

**Correct example:**
> This topic explains how to configure automatic backups so your data is never lost.

**Incorrect example:**
> This topic covers the backup feature.
> *Why wrong: Vague and passive — describes what the topic "covers" rather than the user-facing problem it solves.*

**Writing guidance:**
- **Tone:** conversational
- **Voice:** second person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Write from the reader's perspective — "you" language; lead with the benefit or outcome the user gets; keep to one sentence or a short paragraph
- **Don't:** Use passive voice or vague phrasing like "this topic covers…"; describe internal implementation details or engineering rationale; exceed two sentences

---

### 4. Product Context

**Template:**

```markdown
## Product Context

[Prerequisites, default behavior, and version-specific context the reader needs before using this feature.]

- **Prerequisites:** [What must already be installed or configured]
- **Default behavior:** [What happens if the user doesn't specify options]
- **Version:** [Applicable product version, if version-specific]
```

**Correct example:**
> - **Prerequisites:** App Server v2.0 or later must be installed
> - **Default behavior:** Backups run daily at 02:00 to the default directory
> - **Version:** Behavior changed in v2.3 — earlier versions require manual scheduling

**Incorrect example:**
> Backup is a useful feature that helps protect your data. It was introduced in v1.0 and has been improved many times since then.
> *Why wrong: Reads like marketing copy — does not state prerequisites, defaults, or version-specific context the reader needs before using the feature.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** List prerequisites as explicit bullet points with exact version numbers; state the default behavior concisely so the reader knows what happens without intervention; note any version-specific behavioral changes
- **Don't:** Write promotional or historical prose ("has been improved many times"); omit minimum version requirements; mix aspirational language with factual prerequisites

---

### 5. Public Contract

**Template:**

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

**Correct example:**
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

**Incorrect example:**
> The backup command accepts a directory flag and writes files. Errors may occur if the directory is not writable.
> *Why wrong: No structured tables, missing types/defaults/required status, and error conditions are buried in prose instead of listed with causes and resolutions.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Use structured tables for every parameter, input, output, and error condition; include type, default value, and required/optional status for every flag; list error conditions with a Resolution column the user can act on
- **Don't:** Bury interface details in prose paragraphs; omit type or default information; list error messages without actionable resolutions

---

### 6. Related

**Template:**

```markdown
## Related

- [Topic Name](link) — brief label explaining why this is relevant
```

**Correct example:**
> - [Scheduled Backups](scheduled-backups.md) — how to change the backup schedule
> - [Restore From Backup](restore-backup.md) — recovering data from a saved snapshot

**Incorrect example:**
> - [Some Other Topic](broken-link.md)
> *Why wrong: Link target does not resolve, and the label gives no indication of why the reader should follow it.*

**Writing guidance:**
- **Tone:** conversational
- **Voice:** second person
- **Structure:** bullet lists
- **Audience:** AI agent
- **Do:** Provide at least one cross-reference with a brief label explaining relevance; link to adjacent Product Guide topics the reader is likely to need next; keep labels descriptive enough to stand alone without context
- **Don't:** Include links without labels or with vague labels ("see also"); link to topics outside the Product Guide domain without clear relevance; duplicate content from the linked topic in the description

---

## Output Contract

Output a single complete markdown document containing all 6 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
