You are verifying whether an extracted claim is grounded in its cited evidence.

## Paper title
{{paper_title}}

## Claim row
- **Table**: {{table_name}}
- **Row ID**: {{row_id}}
- **Source evidence**: {{source_evidence}}
- **Relevance note**: {{relevance_note}}

## Evidence file content
{{#evidence_content}}
{{.}}
{{/evidence_content}}
{{^evidence_content}}
[No evidence content provided — file empty or unreadable]
{{/evidence_content}}

## Reasoning chain (follow in order)
1. Restate the claim being checked, in your own words.
2. Restate what the cited evidence actually says, separately, before comparing.
3. Compare: does the evidence fully support the claim, partially support it, or not support it at all? Name the gap if there is one.
4. Only then output PASS/FAIL — the verdict is the last step, not the first.

Write your analysis as a short paragraph, then end with a verdict line:

VERDICT: PASS
— or —
VERDICT: FAIL
Evidence note: <one-sentence explanation of why>
