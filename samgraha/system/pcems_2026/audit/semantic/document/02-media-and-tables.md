# Media and Tables Audit

This section details the Media and Tables Audit for PCEMS 2026.

## Version
1.0.0

## Engineering Intent
Ensures correct inline placement of tables and figures, and checks image alpha-channel compliance.

## Audit Objectives
- Ensure tables and figures are embedded immediately after their first reference.
- Prevent aggregation of media at the end of the document.
- Verify images do not contain transparent pixels.
- Ensure tables use native MS Word table structures.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Images and tables are placed inline immediately after their first reference, not at the end of the manuscript |
| C2 | mandatory | 0 or 50 | No embedded images contain transparent pixels (alpha-channel) |
