# Title and Metadata Semantic Audit

This section details the Title and Metadata Semantic Audit.

## Version
1.0.0

## Engineering Intent
Enforces the PCEMS 2026 title/author/affiliation typography spec, the CMT3 portal's PDF export rules, and the submission's exclusivity clause — the three whole-submission checks that gate everything else.

## Audit Objectives
- Title is Arial Bold 14pt centered; authors are Arial 12pt Bold centered; affiliations are Arial 11pt centered; corresponding author's e-mail is included; at least 4-5 keywords in Arial 12pt bold under a "Keywords:" label.
- All PDF fonts are scalable and embedded; Document Security/Protection is strictly disabled.
- Manuscript content is not detected as substantially similar to concurrent submissions or external databases.

## Expected Quality
- Every metadata element matches its font/size/alignment spec exactly, not approximately.
- The exported PDF opens without a security prompt in any standard reader.

## Red Flags
- Missing corresponding-author e-mail.
- Fewer than 4 keywords.
- Non-embedded or non-scalable font in the exported PDF.
- Document Security enabled on the PDF.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Title, author, affiliation, and keyword typography match the spec exactly |
| C2 | mandatory | 0 or 35 | All PDF fonts are scalable and embedded, and Document Security/Protection is disabled |
| C3 | mandatory | 0 or 25 | Manuscript content is unique and not detected in concurrent submissions or external databases |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "excerpt": "PDF metadata: Security=Enabled, Fonts=[Arial(not embedded)]" },
  "message": "PDF has Document Security enabled and an unembedded font — both violate CMT3 export rules."
}
```
