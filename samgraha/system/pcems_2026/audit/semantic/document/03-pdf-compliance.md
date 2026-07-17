# PDF Compliance Audit

This section details the PDF Compliance Audit for PCEMS 2026.

## Version
1.0.0

## Engineering Intent
Enforces the PDF export rules required by the Microsoft Research paper submission portal (CMT3).

## Audit Objectives
- Verify that only scalable fonts are used.
- Verify all fonts are embedded in the PDF.
- Verify that Adobe Document Protection or Document Security is strictly disabled.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | All fonts in the PDF are scalable and embedded |
| C2 | mandatory | 0 or 50 | Document Security / Protection is disabled |
