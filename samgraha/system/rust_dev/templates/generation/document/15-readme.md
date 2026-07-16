# README Document — Generation Template

> **Domain:** readme
> **Source standard:** `documentation-standards/15-readme-standards.md`
> **Coherence source:** `audit/semantic/document/15-readme.md`
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate a complete README document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | | Clear definition of README scope and boundaries |
| 2 | Project Name | `project_name` | ✓ | Canonical name matching package manifests |
| 3 | Short Description | `short_description` | ✓ | 1–2 sentences under 200 characters |
| 4 | Overview | `overview` | ✓ | High-level problem and solution narrative |
| 5 | Key Capabilities | `key_capabilities` | ✓ | 3–7 scannable capability items |
| 6 | Repository Structure | `repository_structure` | ✓ | Major directory descriptions, high-level only |
| 7 | Documentation Structure | `documentation_structure` | ✓ | Doc organization with navigation guidance |
| 8 | Installation | `installation` | ✓ | Step-by-step commands with prerequisites |
| 9 | Build | `build` | ✓ | Build commands, prerequisites, expected output |
| 10 | Usage | `usage` | ✓ | Working examples covering primary functions |
| 11 | Getting Started | `getting_started` | ✓ | Zero-to-running path with all prerequisites |
| 12 | Configuration | `configuration` | Conditional | Options with defaults, valid values, and examples |
| 13 | Development | `development` | ✓ | Dev setup, test commands, workflow description |
| 14 | Contributing | `contributing` | ✓ | Contribution process and quality standards |
| 15 | License | `license` | Conditional | License name with link to full text |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/15-readme.md` Engineering Intent.

Sections within a README must describe the same project without contradicting each other. Specifically:

- Usage examples must be achievable with the Installation and Build commands provided
- Getting Started must be a linear superset of Installation + Build + Usage
- Configuration options must be consistent with what Usage examples demonstrate
- Development setup must include prerequisites listed in Installation
- Contributing must reference Development workflow and test commands
- Repository Structure must list directories that Documentation Structure references
- Project Name must match across all references (title, project name section, package manifests)

If any section would reference a command, directory, or option not present in another section, reconcile before outputting.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

This README introduces the [Project Name] repository and guides readers toward detailed documentation. It covers [scope], establishes boundaries via [out of scope], and references the broader documentation ecosystem.

> **What this README is:** [high-level summary of README's role]
> **What this README is not:** [what belongs in other documentation]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* README purpose: what this file introduces, what boundaries apply, and where readers should go for detail. The meta-level "This document defines the standard for README..." language belongs in the standard itself, not in a generated document.

**Correct example:**
> This README introduces the Acme Platform repository and guides readers toward detailed documentation. It covers project overview, setup, usage, and links to architecture, features, and engineering documentation. It does not contain feature specifications, API documentation, or implementation details.

**Incorrect example:**
> This README covers all project documentation including API references, database schemas, and deployment procedures.
> *Why wrong: Purpose section must define README scope and boundaries, not duplicate detailed documentation from other standards.*

**Writing guidance:**
- **Tone:** conversational
- **Voice:** first person plural
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** State what the README is and what it is not; reference the broader documentation ecosystem
- **Don't:** Include feature lists; duplicate content from other documentation standards; use vague scope language

---

### 2. Project Name

**Template:**

```markdown
## Project Name

[Canonical project name exactly as it appears in package manifests]
```

**Correct example:**
> Acme Platform

**Incorrect example:**
> The Acme Platform is a comprehensive project management solution.
> *Why wrong: Project Name section must state only the canonical name, not a description of the project.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Use the exact canonical name from package manifests; verify name matches across documentation
- **Don't:** Add descriptions or taglines; abbreviate the name; use marketing or codenames

---

### 3. Short Description

**Template:**

```markdown
## Short Description

[One to two sentences stating what the project does and who it is for — under 200 characters]
```

**Correct example:**
> A lightweight task scheduler that automates data pipeline orchestration across distributed environments.

**Incorrect example:**
> Acme Scheduler is a tool built with Python 3.12, uses Apache Airflow as its backend, stores data in PostgreSQL, and supports Docker deployment. Install it with pip install acme-scheduler. It has 15 commands and supports cron expressions.
> *Why wrong: Short Description must be one to two sentences under 200 characters summarizing what the project does, not listing technology stack, installation instructions, or feature counts.*

**Writing guidance:**
- **Tone:** conversational
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Write one to two sentences under 200 characters; state what the project does and who it is for
- **Don't:** Include technology stack details; mention installation steps; list feature counts or version numbers

---

### 4. Overview

**Template:**

```markdown
## Overview

[Explain the problem the project solves]
[Describe the project's approach at a high level]
[Reference Vision(01) for deeper context — no implementation details, no architecture diagrams]
```

**Correct example:**
> Managing data pipelines across multiple environments requires consistent scheduling, monitoring, and error handling. Most teams build custom scripts that become difficult to maintain.
>
> Acme Scheduler provides a declarative configuration format and built-in retry logic that lets teams define and deploy pipelines without writing orchestration code.

**Incorrect example:**
> Acme Scheduler is a Python application using the Celery task queue with Redis as a broker. It consists of a scheduler module, a task runner, and a REST API built with FastAPI.
> *Why wrong: Overview must explain the problem and solution at a high level, not describe the technology stack or internal architecture.*

**Writing guidance:**
- **Tone:** inspirational
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** Explain the problem the project solves; describe the approach at a high level; reference Vision for deeper context
- **Don't:** Describe the technology stack; include architecture diagrams; list implementation details or internal components

---

### 5. Key Capabilities

**Template:**

```markdown
## Key Capabilities

- [Capability 1: short descriptive phrase]
- [Capability 2: short descriptive phrase]
- [Capability 3: short descriptive phrase]
<!-- List 3 to 7 capabilities; no implementation details -->
```

**Correct example:**
> - Declarative pipeline configuration
> - Automatic retry and error recovery
> - Multi-environment deployment support
> - Built-in monitoring and alerting
> - CLI and web interface

**Incorrect example:**
> - Uses Celery 5.3.2 with Redis broker
> - Supports Python 3.10, 3.11, and 3.12
> - Has 47 unit tests and 12 integration tests
> - Deploys via Docker Compose or Kubernetes Helm chart
> *Why wrong: Key Capabilities must list high-level capabilities as scannable phrases, not implementation details like library versions, test counts, or deployment mechanisms.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** product owner
- **Do:** List three to seven capabilities as short descriptive phrases; keep each capability independent and scannable
- **Don't:** Include library versions or test counts; describe deployment mechanisms; use technical jargon or implementation details

---

### 6. Repository Structure

**Template:**

```markdown
## Repository Structure

- `src/` — [purpose]
- `tests/` — [purpose]
- `docs/` — [purpose]
- `scripts/` — [purpose]
<!-- High-level descriptions only; no file-level detail -->
```

**Correct example:**
> - `src/` — Application source code
> - `tests/` — Unit and integration tests
> - `docs/` — Documentation by standard
> - `scripts/` — Build and automation scripts
> - `examples/` — Usage examples and templates

**Incorrect example:**
> - `src/core/scheduler/worker.py` — The main worker loop that processes tasks
> - `src/api/routes/v2/health.py` — Health check endpoint returning 200 OK
> *Why wrong: Repository Structure must provide high-level directory descriptions, not file-level implementation details.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** List major directories with one-sentence purpose descriptions; keep descriptions high-level and focused on purpose
- **Don't:** List individual files or modules; include implementation details; describe internal code organization

---

### 7. Documentation Structure

**Template:**

```markdown
## Documentation Structure

[List documentation directories and their purpose]
[Explain the organization principle]
[Provide navigation guidance from README to detailed docs]
```

**Correct example:**
> Documentation lives under `docs/` organized by standard:
>
> - `docs/raw/vision/` — Project goals and context
> - `docs/raw/features/` — Feature specifications
> - `docs/raw/architecture/` — System design
> - `docs/raw/engineering/` — Implementation standards
>
> Start with the [Documentation Navigation](#documentation-navigation) section below for a guided reading order.

**Incorrect example:**
> All documentation is in the docs folder. There is a lot of markdown in there.
> *Why wrong: Documentation Structure must list directories with their purpose and provide navigation guidance, not vague statements about file locations.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** List documentation directories with one-sentence purpose descriptions; provide navigation guidance from README to detailed docs
- **Don't:** Omit directory purposes; list individual files; provide navigation without linking to specific standards

---

### 8. Installation

**Template:**

```markdown
## Installation

### Prerequisites

- [Required tool and version]

### Install

[Step-by-step commands with expected output]
```

**Required subsections:** Prerequisites, Install

**Correct example:**
> ### Prerequisites
>
> - Rust 1.75+ (via rustup)
>
> ### Install
>
> ```bash
> cargo install acme-scheduler
> ```
>
> Verify installation:
>
> ```bash
> acme-scheduler --version
> # Expected: acme-scheduler 2.1.0
> ```

**Incorrect example:**
> Just clone the repo and it works. You might need to install some things first.
> *Why wrong: Installation must provide specific step-by-step commands with prerequisites listed, not vague instructions that leave the reader guessing what to install.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** List prerequisites with version numbers first; provide step-by-step commands with expected output; verify each step works
- **Don't:** Use vague instructions like "install dependencies"; omit version requirements; skip verification steps

---

### 9. Build

**Template:**

```markdown
## Build

### Prerequisites

- [Build tool and version]

### Build Commands

[Build commands with expected output]
[List common build targets]
```

**Required subsections:** Prerequisites, Build Commands

**Correct example:**
> ### Prerequisites
>
> - Rust 1.75+ (edition 2021)
>
> ### Build Commands
>
> ```bash
> cargo build --release
> ```
>
> Produces `target/release/acme-scheduler`.

**Incorrect example:**
> Run the build. It compiles everything and puts the output somewhere in the build directory.
> *Why wrong: Build must list prerequisites, provide specific commands, and describe expected output, not leave the reader guessing about tool versions and where artifacts appear.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** List build prerequisites with version numbers; provide specific build commands; describe expected output and artifact locations
- **Don't:** Omit prerequisite versions; use ambiguous build commands; skip expected output descriptions

---

### 10. Usage

**Template:**

```markdown
## Usage

### Basic Usage

[Working command examples with expected output]

### Common Workflows

[Typical usage patterns]
```

**Required subsections:** Basic Usage
**Optional subsections:** Common Workflows

**Correct example:**
> ### Basic Usage
>
> ```bash
> acme-scheduler run --config config.yaml
> # Started scheduler on port 8080
> ```
>
> ### Common Workflows
>
> ```bash
> acme-scheduler status
> # Active pipelines: 3, Completed: 12, Failed: 0
> ```

**Incorrect example:**
> The scheduler can be used to run pipelines. It supports many options. Check `--help` for more information.
> *Why wrong: Usage must provide working command examples with expected output demonstrating primary functions, not vague descriptions that require the reader to explore help text.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Provide working command examples with expected output; cover primary functions; show common workflows
- **Don't:** Use vague descriptions like "check --help"; omit expected output; skip primary function examples

---

### 11. Getting Started

**Template:**

```markdown
## Getting Started

### Prerequisites

- [Required tools and versions]

### Quick Start

[Step-by-step from clone to running project]
[Prerequisites, install, build, first run in one place]
```

**Required subsections:** Prerequisites, Quick Start

**Correct example:**
> ### Prerequisites
>
> - Python 3.10+
> - Docker 24+
>
> ### Quick Start
>
> ```bash
> git clone https://github.com/acme/scheduler.git
> cd scheduler
> docker compose up
> curl http://localhost:8080/health
> # Expected: {"status":"ok"}
> ```

**Incorrect example:**
> Clone the repo, install dependencies, and run the app. See Installation and Build sections for details.
> *Why wrong: Getting Started must provide a complete, linear zero-to-running path with prerequisites and working commands, not delegate the reader to other sections.*

**Writing guidance:**
- **Tone:** conversational
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** Provide a complete linear path from clone to running project; include all prerequisites and version numbers; verify each step works
- **Don't:** Delegate readers to other sections; omit prerequisites; skip verification steps or expected outcomes

---

### 12. Configuration

**Template:**

```markdown
## Configuration

### Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| [name] | [default] | [purpose] |

### Configuration Files

[List settings files and their purpose]
[State valid values and defaults]
[Provide examples]
```

**Required subsections:** Environment Variables or Configuration Files

**Correct example:**
> ### Environment Variables
>
> | Variable | Default | Description |
> | --- | --- | --- |
> | `SCHEDULER_PORT` | `8080` | HTTP port for the API server |
> | `SCHEDULER_DB` | `sqlite:///local.db` | Database connection string |
>
> ### Configuration Files
>
> `config.yaml` controls pipeline scheduling behavior. See `config.example.yaml` for a documented reference.

**Incorrect example:**
> The config file is in YAML. You can set environment variables too. Change things as needed.
> *Why wrong: Configuration must list specific options with their defaults, valid values, and examples, not vague statements about available configuration mechanisms.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** List configuration options by category; state defaults and valid values; provide working examples for each option
- **Don't:** Omit default values; list internal configuration mechanisms; use vague descriptions without valid value ranges

---

### 13. Development

**Template:**

```markdown
## Development

### Local Setup

[Development environment setup steps]

### Running Tests

[Test commands with expected output]

### Workflow

[Development workflow description]
[Reference coding standards]
```

**Required subsections:** Local Setup, Running Tests
**Optional subsections:** Workflow

**Correct example:**
> ### Local Setup
>
> ```bash
> git clone https://github.com/acme/scheduler.git
> cd scheduler
> cargo build
> ```
>
> ### Running Tests
>
> ```bash
> cargo test
> ```
>
> ### Workflow
>
> Create a feature branch, make changes, run tests, and open a pull request. See [Coding Standards](../engineering/coding-standards.md) for style guidelines.

**Incorrect example:**
> To develop, clone the repo and start coding. Write tests for your changes.
> *Why wrong: Development must provide specific setup steps, test commands, and workflow description, not assume the reader knows the toolchain or contribution process.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Describe development environment setup with specific commands; explain how to run tests; reference coding standards
- **Don't:** Assume prior knowledge of the toolchain; omit test commands; skip workflow description or coding standard references

---

### 14. Contributing

**Template:**

```markdown
## Contributing

### Contribution Process

[Step-by-step contribution workflow]

### Code Review

[Code review expectations and process]

### Quality Standards

[List quality standards for contributions]
[Reference development setup]
```

**Required subsections:** Contribution Process, Code Review, Quality Standards

**Correct example:**
> ### Contribution Process
>
> 1. Fork the repository
> 2. Create a feature branch from `main`
> 3. Make changes and add tests
> 4. Open a pull request against `main`
>
> ### Code Review
>
> All pull requests require one approval. Reviewers check for test coverage, code style, and documentation updates.
>
> ### Quality Standards
>
> - All new code must have tests
> - Documentation must be updated for user-facing changes
> - Commit messages follow Conventional Commits

**Incorrect example:**
> Contributions welcome! Just open a PR.
> *Why wrong: Contributing must describe the full contribution workflow, code review process, and quality standards, not provide a one-line invitation with no actionable guidance.*

**Writing guidance:**
- **Tone:** conversational
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** Describe the full contribution workflow step by step; explain code review expectations; list quality standards for contributions
- **Don't:** Use vague invitations like "contributions welcome"; omit code review process; skip quality standards or testing requirements

---

### 15. License

**Template:**

```markdown
## License

[State the license name]
[Link to or include the full license text]
[Include copyright notices if applicable]
```

**Correct example:**
> This project is licensed under the [Apache License 2.0](LICENSE).
>
> Copyright 2025 Acme Corporation.

**Incorrect example:**
> You can use this software however you want. See the license file for details.
> *Why wrong: License must state the specific license name and provide a direct link to the full license text, not use vague language that leaves the legal terms ambiguous.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State the exact license name; link directly to the full license text; include copyright notices if applicable
- **Don't:** Use vague language like "see license file"; omit the license name; include legal advice or license comparisons

---

## Output Contract

Output a single complete markdown document containing all 15 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified
6. Omit implementation details beyond what the README format requires
