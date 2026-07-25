# Testing - Deterministic Audit

**Repository:** `{{ repo_name }}`
**Date:** `{{ evaluation_date }}`

## Rule Executions
| Rule ID | Description | Passed | Weight | Mandatory |
|---------|-------------|--------|--------|-----------|
{{#deterministic_rules}}
| `{{ id }}` | {{ description }} | {{ passed }} | {{ weight }} | {{ mandatory }} |
{{/deterministic_rules}}

## Findings
{{ deterministic_findings }}

## Rule Detail
{{#deterministic_rules}}
### {{ id }} — {{ description }}
**Status:** {{ passed }} · **Weight:** {{ weight }} · **Mandatory:** {{ mandatory }} · **Severity:** {{ severity }}

{{ detail }}
{{/deterministic_rules}}
