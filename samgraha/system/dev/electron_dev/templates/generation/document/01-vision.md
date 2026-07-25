# Vision Document — Generation Template

> **Domain:** vision
> **Source standard:** `documentation-standards/01-vision-standards.md`
> **Coherence source:** `audit/semantic/document/01-vision.md`
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate a complete Vision document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | ✓ | Single paragraph stating why the product exists; no implementation details |
| 2 | Vision | `vision_statement` | ✓ | 1-2 paragraphs describing the aspirational future state of the product |
| 3 | Problem | `problem` | ✓ | 1-3 paragraphs with concrete examples and quantified impact where possible |
| 4 | Solution | `solution` | ✓ | 1-2 paragraphs describing the product-level approach to solving the problem |
| 5 | Target Audience | `target_audience` | ✓ | 1-2 paragraphs defining users by goals and needs, not technical profiles |
| 6 | Platform Pillars | `pillars` | | 3-5 named pillars, each with a one-sentence description |
| 7 | Philosophy | `philosophy` | | 3-5 principles expressed as memorable values with brief rationale |
| 8 | Guiding Principles | `guiding_principles` | | 3-5 enduring principles with rationale; stable across feature changes |
| 9 | Success Criteria | `success_criteria` | | 3-6 observable outcomes tied to the Vision; measurable or evaluable |
| 10 | Traceability | `traceability` | | Tier diagram, list of downstream standards, non-contradiction rule statement |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/01-vision.md` Engineering Intent.

All sections must cohere as a single vision — Problem, Solution, and Vision Statement must align without contradiction. Purpose must explain why; Vision must paint the future state that Purpose enables. Problem must describe pain that Solution addresses. Target Audience must match the users who experience the Problem. Pillars and Philosophy must express values that guide the Solution. Success Criteria must be observable outcomes of the Vision being realized. No section may contain implementation details — Vision is technology-independent by design.

## Sections

---

### 1. Purpose

**Template:**

```markdown
[One sentence stating why the product exists and the problem it addresses]
[One sentence stating the intended value or outcome for users]
[One sentence reinforcing the core identity of the product]
```

**Correct example:**
> DataSync exists to help teams move information between systems without manual intervention, eliminating hours of repetitive data entry each week. DataSync is the bridge that turns fragmented data into a single source of truth.

**Incorrect example:**
> DataSync is a Python-based ETL pipeline using Apache Airflow that runs daily cron jobs to sync PostgreSQL databases via REST APIs.
> *Why wrong: Contains implementation details (technology stack, scheduling mechanism, protocol) that belong in downstream documentation.*

**Writing guidance:**
- **Tone:** inspirational
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** Write from the user's world, not the engineer's; anchor the purpose in the problem space; keep the language stable enough to survive technology changes
- **Don't:** Name programming languages, frameworks, or infrastructure; describe what the product does or how it works; use jargon that requires domain expertise to understand

---

### 2. Vision

**Template:**

```markdown
[Aspirational statement describing the desired future state of the product]
[What the product will enable or become once fully realized]
```

**Correct example:**
> CloudBridge will become the trusted backbone for cross-organization data exchange, where any team can connect to any data source within minutes and trust that the information is accurate and current.

**Incorrect example:**
> CloudBridge will migrate from REST to GraphQL by Q3, reaching 10,000 API calls per second with sub-50ms latency on AWS.
> *Why wrong: Describes a technology roadmap with specific implementation targets rather than an aspirational future state.*

**Writing guidance:**
- **Tone:** inspirational
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Paint a vivid picture of the fully realized product state; write in the future tense with aspirational language; tie the vision back to the Purpose section's "why"
- **Don't:** Mention specific technologies, release timelines, or implementation milestones; describe current product state or features; use metrics or benchmarks that belong in Success Criteria

---

### 3. Problem

**Template:**

```markdown
[Description of the real-world pain or gap the product addresses]
[Concrete example illustrating the problem in context]
[Quantified impact where possible — cost, time, frequency]
```

**Correct example:**
> Teams that need to consolidate data from multiple sources spend hours each week on manual copying and pasting between spreadsheets. A mid-size operations team reports losing 12 hours per week to data reconciliation tasks, leading to delayed reports and costly errors.

**Incorrect example:**
> Teams struggle with data silos. DataSync solves this by using scheduled Python scripts and a Redis cache layer to automatically merge CSV files.
> *Why wrong: Mixes solution details into the Problem section. The Problem section should describe pain, not how the product addresses it.*

**Writing guidance:**
- **Tone:** concrete
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Use specific, quantifiable examples of the pain; describe the problem from the user's perspective; include the cost of inaction
- **Don't:** Mention the product name or any solution approach; describe the problem in abstract or theoretical terms; include technical error messages or stack traces

---

### 4. Solution

**Template:**

```markdown
[High-level description of what the product does to solve the stated problem]
[How the product's approach delivers value to the target audience]
```

**Correct example:**
> DataSync automates the collection, transformation, and delivery of data across connected systems. It provides a single place to define data flows and ensures that information stays consistent wherever it is used.

**Incorrect example:**
> DataSync uses Python with Celery workers and RabbitMQ to queue data jobs, storing results in a PostgreSQL database with a React dashboard for monitoring.
> *Why wrong: Describes architecture and implementation technology instead of the product-level approach.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Describe the approach at the product level using action verbs; connect the solution directly back to the Problem section; keep descriptions at the "what it does" level
- **Don't:** Name libraries, frameworks, or databases; describe data flows, APIs, or internal system boundaries; discuss trade-offs between technology options

---

### 5. Target Audience

**Template:**

```markdown
[Description of the intended users or consumers by their goals and needs]
[Who benefits from the product and who makes adoption decisions]
[What the audience expects or requires from the product]
```

**Correct example:**
> CloudBridge serves operations teams who need to consolidate data from multiple sources into a single, reliable view. These teams prioritize accuracy and speed over technical flexibility, and their managers make adoption decisions based on time savings and error reduction.

**Incorrect example:**
> CloudBridge is used by Python developers with 5+ years of experience who write pandas scripts and prefer CLI tools with YAML configuration.
> *Why wrong: Describes the audience by technical profile instead of goals and needs.*

**Writing guidance:**
- **Tone:** conversational
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Describe audiences by their goals, pain points, and decision-making criteria; distinguish between end users and decision-makers; include what each audience expects from the product
- **Don't:** List programming skills, tool proficiencies, or job titles as the defining trait; write user stories or persona cards; conflate technical users with the primary audience

---

### 6. Platform Pillars

**Template:**

```markdown
## [Pillar Name 1]

[One-sentence description of this pillar and its role in the product]

## [Pillar Name 2]

[One-sentence description of this pillar and its role in the product]

## [Pillar Name 3]

[One-sentence description of this pillar and its role in the product]
```

**Correct example:**
> **Reliable Connections** — Every connection to an external system is resilient, recoverable, and transparent in its status.
> **Data Integrity** — Information delivered through the product is always accurate and traceable to its source.
> **Simple Configuration** — Setting up a new data flow requires no coding and minimal manual steps.

**Incorrect example:**
> **Microservices** — The product uses a microservices architecture for scalability.
> **Docker Containers** — All components run in Docker for consistent deployment.
> *Why wrong: Describes technology choices instead of foundational capability pillars.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Name each pillar with a memorable, two-word phrase; write one sentence per pillar that explains its role in the product; ensure pillars cover the full product scope without overlap
- **Don't:** Name specific technologies or components; use abstract nouns without a clear product connection; list more than five pillars

---

### 7. Philosophy

**Template:**

```markdown
[Statement of the product's core philosophy — the values that guide decisions]

## [Philosophy Value 1]

[One-sentence description of this value and why it matters]

## [Philosophy Value 2]

[One-sentence description of this value and why it matters]

## [Philosophy Value 3]

[One-sentence description of this value and why it matters]
```

**Correct example:**
> **Clarity Over Cleverness** — Every feature should be immediately understandable to the person using it, even if that means a less elegant implementation.
> **Trust by Default** — Users should never have to wonder whether their data is correct; accuracy is assumed, not requested.

**Incorrect example:**
> **Use FastAPI** — The product favors high-performance Python web frameworks.
> *Why wrong: States technology preferences rather than guiding values.*

**Writing guidance:**
- **Tone:** inspirational
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Express each value as a memorable phrase with a one-sentence rationale; tie each value back to the product's purpose; keep the language abstract enough to survive technology changes
- **Don't:** Name frameworks, databases, or deployment targets; write rules that require specific tools; list more than five values

---

### 8. Guiding Principles

**Template:**

```markdown
[Introductory paragraph explaining that these principles guide all downstream decisions]

## [Principle 1]

[One-sentence statement of the principle and its rationale]

## [Principle 2]

[One-sentence statement of the principle and its rationale]

## [Principle 3]

[One-sentence statement of the principle and its rationale]
```

**Correct example:**
> **Fail Safely** — When a connection to an external system fails, the product preserves existing data and retries automatically rather than losing work.
> **Show, Don't Assume** — Every automated action should be visible to the user so they can verify correctness.

**Incorrect example:**
> **Use Kubernetes** — The product should always be deployed on Kubernetes for orchestration.
> *Why wrong: States technology mandates rather than enduring principles.*

**Writing guidance:**
- **Tone:** inspirational
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Phrase each principle as a decision rule that applies across technologies; include a one-sentence rationale for each; ensure principles are testable against real decisions
- **Don't:** Name programming languages, frameworks, or cloud providers; write principles that are only true for one implementation; list more than five principles

---

### 9. Success Criteria

**Template:**

```markdown
* [Observable outcome tied to the Vision — what success looks like]
* [Observable outcome tied to the Vision — what success looks like]
* [Observable outcome tied to the Vision — what success looks like]
```

**Correct example:**
> * Teams report spending less than 2 hours per week on data reconciliation tasks.
> * At least 80% of new data flows are set up without engineering support.
> * Data delivered through the product is accurate 99.9% of the time as verified by audits.

**Incorrect example:**
> * The API response time is under 200ms.
> * The test suite achieves 95% code coverage.
> *Why wrong: Describes implementation-level metrics rather than observable outcomes tied to the Vision.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** product owner
- **Do:** Write each criterion as a measurable or evaluable outcome; tie every criterion directly to the Vision statement; use concrete units of measure where possible
- **Don't:** Describe technical benchmarks like latency or throughput; include test coverage or deployment frequency; list more than six criteria

---

### 10. Traceability

**Template:**

```markdown
Tier 0: Vision (Purpose)
    ├──→ Tier 1: [Downstream Standard 1]
    ├──→ Tier 1: [Downstream Standard 2]
    └──→ Tier 2: [Downstream Standard 3]
```

**Correct example:**
> Tier 0: Vision (Purpose, Problem, Solution)
>     ├──→ Tier 1: Philosophy (Values, Principles)
>     ├──→ Tier 1: Features (Feature List, Feature Details)
>     └──→ Tier 2: Architecture (System Design, Technology Choices)
>
> **Non-contradiction rule:** No downstream document may state a goal, constraint, or priority that contradicts the Vision. When conflicts arise, the Vision takes precedence.

**Incorrect example:**
> Vision traces to the README and the CI/CD pipeline configuration.
> *Why wrong: References an implementation artifact instead of the documentation hierarchy.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Include a tier diagram showing the derivation hierarchy; list every downstream standard that derives from Vision; state the non-contradiction rule explicitly
- **Don't:** Reference source code files, CI/CD pipelines, or infrastructure artifacts; omit standards from the diagram; use prose where a diagram would be clearer

---

## Output Contract

Output a single complete markdown document containing all 10 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified (as markdown image references or Mermaid code blocks)
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
