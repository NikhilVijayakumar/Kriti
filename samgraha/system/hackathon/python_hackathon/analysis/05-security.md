# Security Analysis Prompt

Guides the per-team analysis for the Security domain — read by whichever
agent runs it via MCP, after scoring has completed. Explains a team's
security posture grounded in bandit SAST results. Not parsed by a
script — this is a prompt.

## Version
1.0.0

## Analysis Intent
Security scores (weight: 10) measure whether a team employs basic SAST
and avoids common vulnerability patterns. Hackathon projects often skip
security entirely — this step identifies which teams did and which
didn't, with specific findings.

## Inputs
- `standard_domain_scores` DB table — all teams' security domain
  scores (queried via MCP)
- Per-team deterministic findings: bandit configuration (`.bandit` or
  `pyproject.toml`), bandit scan results (issues by severity/confidence)
- Semantic findings: hardcoded secrets patterns, API key handling,
  serialization safety (pickle vs safe alternatives)

## Narrative Guidance
The Security narrative must cover:
1. **Score Overview** — team's security score out of 10, with
   competition average comparison. Security is medium-weight but
   non-negotiable.
2. **SAST Configuration** — is bandit configured (`.bandit` file or
   `pyproject.toml` section)? Configuration presence demonstrates
   security awareness even if findings exist.
3. **Scan Results** — summary of bandit findings: count by severity
   (HIGH/MEDIUM/LOW) and confidence level. Name the specific issue
   types (e.g., `hardcoded_password`, `eval_usage`).
4. **Hardcoded Secrets** — did the scan find hardcoded API keys,
   passwords, or tokens? This is the most critical security finding
   in a hackathon context. Name the file and pattern.
5. **Serialization Safety** — does the code use `pickle.load` without
   safe alternatives? Pickle deserialization is a common attack vector
   in ML projects.
6. **Strengths** — bandit configured and passing clean, no hardcoded
   secrets, safe serialization patterns, environment variables for
   credentials.
7. **Weaknesses** — no SAST configured, hardcoded secrets found, high-
   severity bandit findings, unsafe pickle usage, eval/exec calls.
8. **Recommendations** — "remove hardcoded API key from `config.py:42`",
   "replace `pickle.load` with `torch.load` with `weights_only=True`",
   "add `.bandit` config to skip false-positive test assertions".

## Visualization Guidance
- `domain_scores` — always include.
- `finding_severity` — include if findings exist: stacked bar of
  HIGH/MEDIUM/LOW by team.
- `vulnerability_types` — include: horizontal bar of most common
  finding types across all teams.

## Output Schema
```json
{
  "domain": "05-security",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "SAST Configuration", "text": "..."},
    {"heading": "Scan Results", "text": "..."},
    {"heading": "Hardcoded Secrets", "text": "..."},
    {"heading": "Serialization Safety", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
