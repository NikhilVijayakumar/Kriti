# Feature Design Document — Generation Template

> **Domain:** feature-design
> **Source standard:** `documentation-standards/09-feature-design-standards.md`
> **Coherence source:** `audit/semantic/document/09-feature-design.md`
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate a complete Feature Design document for a system feature. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | | Definition of Feature Design, scope boundaries, one-to-one relationship with Feature Specification |
| 2 | User Experience | `user_experience` | ✓ | Complete user-facing experience covering discovery, interaction, feedback, errors, empty, loading, and success states |
| 3 | Workflow | `workflow` | ✓ | Ordered sequence of user actions and system responses including branching and error recovery |
| 4 | States | `states` | ✓ | Every observable UI state and all valid transitions between them |
| 5 | Constraints | `constraints` | | External user-facing constraints with source citation and binding vs. advisory distinction |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/09-feature-design.md` Engineering Intent.

User Experience, Workflow, and States must describe the same feature without contradicting each other. Specifically:

- Every user action in Workflow must appear in the User Experience section's interaction description
- Every state in States must correspond to a visible condition described in User Experience (error, empty, loading, success)
- State transitions in States must align with the step sequence in Workflow
- Constraint impacts in Constraints must be reflected in User Experience behavior or Workflow steps
- The collection as a whole must read as one feature design, not several independent descriptions

If any section would introduce a user action, state, or interaction not present in another section, reconcile before outputting.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

> **Feature Design purpose:** [1-2 sentences: what this Feature Design defines for this specific feature — how users should experience it]

> **Scope boundaries:**
> - **In scope:** [user experience concerns this document covers for this feature]
> - **Out of scope:** [concerns explicitly excluded, with the owning standard identified]

> **One-to-one relationship:** This Feature Design corresponds to exactly one Feature Specification: [Feature name].
```

> **Generation note:** When generating for a specific system, fill this template with *that feature's* design purpose: what user experience this document defines and what it intentionally excludes. The meta-level "This document defines the standard for Feature Design Documentation..." language belongs in the standard itself, not in a generated document.

**Correct example:**
> **Feature Design purpose:** This Feature Design defines how users discover, configure, and run data export reports — including scheduling, format selection, and delivery notification.
>
> **Scope boundaries:**
> - **In scope:** Report configuration UX, export workflow, delivery notification experience
> - **Out of scope:** Data pipeline architecture (Feature Technical Design), report data schema (Architecture)
>
> **One-to-one relationship:** This Feature Design corresponds to exactly one Feature Specification: Report Export.

**Incorrect example:**
> Feature Design covers authentication using OAuth 2.0, including token storage with Redis and session management via JWT middleware.
> *Why wrong: introduces implementation details (OAuth, Redis, JWT), which belongs in Feature Technical Design or Engineering, not Feature Design.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Define scope boundaries explicitly; state the one-to-one relationship with Feature; explain what this Feature Design is and is not
- **Don't:** Include implementation details or technology references; leave scope boundaries ambiguous; conflate with Design or Architecture standards

---

### 2. User Experience

**Template:**

```markdown
## User Experience

> **semantic_type:** `user_experience`
> **scope:** [what UX concerns this section covers]
> **out_of_scope:** [what UX concerns are excluded]
> **contributes:** [how this section feeds downstream documents]
> **relationships:** [which upstream documents this derives from]
> **responsibilities:** [what this section is responsible for defining]
> **generation_rules:** [rules for generating this section]
> **enhancement_rules:** [rules for improving this section]
> **validation_rules:** [rules for validating this section]
> **audit_rules:** [rules for auditing this section]

[Introduction: overall UX intent for the feature, derived from Feature Specification]

### Discovery

[How users first encounter and access the feature — entry points, labels, onboarding]

### Primary Interaction

[Core user flow — what users do to accomplish the feature's purpose]

### Feedback and Response

[How the system communicates results of user actions — confirmations, status messages]

### Error Handling

[What users see and can do when something goes wrong — messages, retry options, fallback paths]

### Empty State

[What users see when there is no data or content to display — guidance, next steps]

### Loading State

[What users see while the system is processing — spinners, progress indicators, status text]

### Success State

[What users see when the task completes successfully — confirmation, summary, next actions]

### Accessibility

[How the experience accommodates assistive technologies — screen reader support, keyboard navigation, color contrast]

### Localization

[How the experience adapts for different languages and regions — text expansion, RTL layout, date/number formats]
```

**Correct example:**
> **Discovery:** Users encounter the Export feature via a dedicated "Export" button on the Report Builder page. First-time users see a brief tooltip explaining available formats.
>
> **Error Handling:** When export fails, users see a clear inline message explaining the cause (e.g., "Report exceeds 10,000 row limit for CSV format") and a suggestion (e.g., "Try PDF format or reduce filters"). A retry button is available. No technical error codes are shown.

**Incorrect example:**
> The `DataFetchError` component renders when the API call returns a 500 status. It calls `retryRequest()` with exponential backoff (initial delay 1000ms, max 5 retries). The error boundary catches exceptions from the `FeatureController` class.
> *Why wrong: describes implementation internals (API status codes, retry logic, class names) rather than the user-facing experience.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Describe every interaction from the user's perspective; cover all states including error, empty, loading, and success; reference Design Principles that govern the UX
- **Don't:** Reference APIs, frameworks, or component names; describe internal system behavior or processing logic; skip error, empty, or loading states

**Required subsections:** Discovery, Primary Interaction, Feedback and Response, Error Handling, Empty State, Loading State, Success State
**Optional subsections:** Accessibility, Localization
**Required diagrams:** flowchart (primary user interaction flow)
**Required cross-references:** Feature Specification, Design Documentation UX Principles

---

### 3. Workflow

**Template:**

```markdown
## Workflow

> **semantic_type:** `workflow`
> **scope:** [what workflow concerns this section covers]
> **out_of_scope:** [what workflow concerns are excluded]
> **contributes:** [how this section feeds downstream documents]
> **relationships:** [which upstream documents this derives from]
> **responsibilities:** [what this section is responsible for defining]
> **generation_rules:** [rules for generating this section]
> **enhancement_rules:** [rules for improving this section]
> **validation_rules:** [rules for validating this section]
> **audit_rules:** [rules for auditing this section]

### Primary Workflow

[Step-by-step sequence of user actions and system responses]

1. User does X → System responds with Y
2. User does A → System responds with B
3. ...

### Alternative Workflows

[Branching paths for different user choices or conditions]

### Error Recovery

[What happens and what users can do when a step fails]
```

**Correct example:**
> **Primary Workflow**
>
> 1. User selects report to export → System displays export configuration form with format options
> 2. User selects format and delivery method → System validates selection and shows estimated file size
> 3. User confirms export → System begins processing and displays progress indicator
> 4. System completes export → User sees confirmation with download link and delivery status
>
> **Error Recovery**
>
> If export fails due to data volume, the system displays a message explaining the limit, suggests reducing filters or choosing a different format, and preserves the user's configuration so they can adjust without re-entering data.

**Incorrect example:**
> 1. User clicks submit → `handleSubmit()` dispatches an action to the Redux store
> 2. The middleware calls `POST /api/items/:id` with the form payload
> 3. On success, the router navigates to `/items/:id`
> *Why wrong: describes implementation mechanics (Redux, API routes, router navigation) instead of user actions and observable system responses.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Write each step as user action → observable system response; include error recovery paths for every failure point; ensure every functional requirement maps to at least one workflow step
- **Don't:** Describe implementation mechanics or API calls; skip error recovery or branching paths; use function names, class names, or route paths

**Required subsections:** Primary Workflow, Error Recovery
**Optional subsections:** Alternative Workflows
**Required diagrams:** flowchart (primary workflow)
**Required cross-references:** Feature Specification, User Experience

---

### 4. States

**Template:**

```markdown
## States

> **semantic_type:** `states`
> **scope:** [what state concerns this section covers]
> **out_of_scope:** [what state concerns are excluded]
> **contributes:** [how this section feeds downstream documents]
> **relationships:** [which upstream documents this derives from]
> **responsibilities:** [what this section is responsible for defining]
> **generation_rules:** [rules for generating this section]
> **enhancement_rules:** [rules for improving this section]
> **validation_rules:** [rules for validating this section]
> **audit_rules:** [rules for auditing this section]

### State Definitions

| State | Description | What User Sees |
|-------|-------------|----------------|
| Initial | [condition] | [user-visible description] |
| Active | [condition] | [user-visible description] |
| Processing | [condition] | [user-visible description] |
| Empty | [condition] | [user-visible description] |
| Error | [condition] | [user-visible description] |
| Success | [condition] | [user-visible description] |

### State Transitions

| From | To | Trigger | User Action |
|------|----|---------|-------------|
| Initial | Active | [trigger] | [user action] |
| Active | Processing | [trigger] | [user action] |
| Processing | Success | [trigger] | [system response] |
| Processing | Error | [trigger] | [system response] |
| ... | ... | ... | ... |
```

**Correct example:**
> **State Definitions**
>
> | State | Description | What User Sees |
> |-------|-------------|----------------|
> | Initial | Feature has not been activated | Entry point with a prompt to begin |
> | Configuring | User is setting export options | Form with format, delivery, and filter options |
> | Processing | Export is being generated | Progress indicator with estimated time remaining |
> | Empty | No data matches current filters | Message explaining why and suggesting filter adjustments |
> | Error | Export failed | Error message with cause and retry option |
> | Success | Export completed | Confirmation with download link and delivery status |

**Incorrect example:**
> | State | Description | What User Sees |
> |-------|-------------|----------------|
> | IDLE | Store state is `idle` | Component renders null |
> | FETCHING | Axios request in flight | `<Loader />` component mounted |
> | CACHED | Data in localStorage | Data hydrated into store |
> *Why wrong: describes internal state management (Redux store states, Axios, localStorage, component rendering) rather than observable user-facing states.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Enumerate every observable UI state including empty and error states; document all valid transitions with explicit triggers; describe what the user sees in each state
- **Don't:** Describe internal state management or component lifecycle; omit transition triggers or leave them implicit; reference framework-specific state concepts

**Required subsections:** State Definitions, State Transitions
**Optional subsections:** none
**Required diagrams:** state (state transition diagram)
**Required cross-references:** User Experience, Workflow

---

### 5. Constraints

**Template:**

```markdown
## Constraints

> **semantic_type:** `constraints`
> **scope:** [what constraint concerns this section covers]
> **out_of_scope:** [what constraint concerns are excluded]
> **contributes:** [how this section feeds downstream documents]
> **relationships:** [which upstream documents this derives from]
> **responsibilities:** [what this section is responsible for defining]
> **generation_rules:** [rules for generating this section]
> **enhancement_rules:** [rules for improving this section]
> **validation_rules:** [rules for validating this section]
> **audit_rules:** [rules for auditing this section]

| Constraint | Type | Source | Impact on Design |
|-----------|------|--------|-----------------|
| [description] | Hard/Advisory | [External Context source] | [what it prevents or requires] |
| ... | ... | ... | ... |
```

**Correct example:**
> | Constraint | Type | Source | Impact on Design |
> |-----------|------|--------|-----------------|
> | Maximum report size is 10,000 rows for CSV export | Hard | Platform Data Limits | Users must be warned when report exceeds limit; alternative format suggested |
> | Export must support right-to-left text in reports | Hard | Localization Requirements | Export format must preserve RTL text direction; preview must mirror layout |
> | Dark mode preview is preferred but not mandatory | Advisory | Design System Guidelines | Color choices in PDF export should work in both themes if feasible |

**Incorrect example:**
> | Constraint | Type | Source | Impact on Design |
> |-----------|------|--------|-----------------|
> | Use `maxlength="128"` on the input element | Hard | HTML spec | Input validation in the DOM layer |
> | Must use CSS `direction: rtl` for Arabic | Hard | W3C CSS spec | Stylesheet must set text direction |
> *Why wrong: describes implementation techniques (HTML attributes, CSS properties) rather than user-facing design constraints.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Cite the source of every constraint; distinguish hard constraints from advisory preferences; state the concrete impact on design decisions
- **Don't:** Describe implementation techniques (HTML attributes, CSS properties); omit source attribution; conflate constraints with implementation preferences

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** External Context, Platform requirements

## Output Contract

Output a single complete markdown document containing all 5 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
