# Documentation - Deterministic Audit

**Repository:** `{{ repo_name }}`
**Date:** `{{ evaluation_date }}`

## Rule Executions
| Rule ID | Description | Passed | Weight | Mandatory |
|---------|-------------|--------|--------|-----------|
{{#each deterministic_rules}}
| `{{ this.id }}` | {{ this.description }} | {{ this.passed }} | {{ this.weight }} | {{ this.mandatory }} |
{{/each}}

## Findings
{{ deterministic_findings }}
