# States — Generation Template

> **Domain:** feature-design
> **Section:** states
> **Source:** `documentation-standards/09-feature-design-standards.md` §States
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate the States section for a Feature Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | States must cover every observable condition described in the Feature Specification |
| `derives_from` | design / states | States must apply Design Documentation's state modeling principles |

## Template

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

## Examples

**Correct:**
> **State Definitions**
>
> | State | Description | What User Sees |
> |-------|-------------|----------------|
> | Initial | Feature has not been activated | Entry point with a prompt to begin |
> | Active | Feature is in use | Interactive form with current data |
> | Processing | System is handling user input | Inline spinner with status message |
> | Empty | No data exists to display | Friendly message explaining why and suggesting next steps |
> | Error | Processing failed | Error message with retry option |
> | Success | Task completed | Confirmation message with saved result |

**Incorrect:**
> | State | Description | What User Sees |
> |-------|-------------|----------------|
> | IDLE | Store state is `idle` | Component renders null |
> | FETCHING | Axios request in flight | `<Loader />` component mounted |
> | CACHED | Data in localStorage | Data hydrated into store |
> *Why wrong: describes internal state management (Redux store states, Axios, localStorage, component rendering) rather than observable user-facing states.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Enumerate every observable UI state including empty and error states; document all valid transitions with explicit triggers; describe what the user sees in each state
- **Don't:** Describe internal state management or component lifecycle; omit transition triggers or leave them implicit; reference framework-specific state concepts

**Minimum content:** state table plus transition descriptions
**Length guidance:** moderate
**Required diagrams:** state (state transition diagram)
**Required cross-references:** User Experience, Workflow

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
