# End-to-End Testing — Generation Template

> **Domain:** qa
> **Section:** e2e_testing
> **Source:** `documentation-standards/12-qa-standards.md` §End-to-End Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the End-to-End Testing section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / runtime_behavior | Critical runtime workflows must map to Feature Technical(10) runtime behavior |
| `derives_from` | feature / purpose | Pass/fail criteria must trace to Feature requirements |

## Template

```markdown
## End-to-End Testing

### Critical Runtime Workflows

| Workflow | Runtime Behavior Reference | Expected Outcome | Pass/Fail Criteria |
|---------|-----------------|------------------|-------------------|
| [Workflow 1] | Feature Technical(10) §[section] | [Expected result] | [Measurable criteria] |

### Workflow Flowchart
[Flowchart showing happy path and critical edge cases]
```

## Examples

**Correct:**
> ### Critical Runtime Workflows
>
> | Workflow | Runtime Behavior Reference | Expected Outcome | Pass/Fail Criteria |
> |---------|-----------------|------------------|-------------------|
> | CLI ingest command | Feature Technical(10) §Runtime Behavior — Ingest Pipeline | Input file parsed and written to output store | Process exits 0; output row count matches; no panics logged |
> | Client request round-trip | Feature Technical(10) §Runtime Behavior — Request Handling | Request routed through service layer, response returned | Response status matches contract; latency under budget |

**Incorrect:**
> Test that the binary runs and doesn't crash.
> *Why wrong: critical runtime workflows must be mapped to specific Feature Technical(10) runtime behavior references with measurable pass/fail criteria.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Link each workflow to a specific Feature Technical(10) runtime_behavior section; define expected outcomes as observable system states; write pass/fail criteria as automated assertions
- **Don't:** List workflows without a Feature Technical(10) reference; describe expected outcomes in subjective terms; leave pass/fail criteria implicit

**Required subsections:** Critical Runtime Workflows table
**Optional subsections:** none
**Required diagrams:** flowchart of runtime workflow paths
**Required cross-references:** Feature Technical(10), Feature(04), Implementation(13)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
