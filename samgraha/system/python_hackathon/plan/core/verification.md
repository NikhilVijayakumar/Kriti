# Verification Scripts — python_hackathon

9 scripts total: 7 per-use-case verify scripts, 1 orchestrator, 1 coverage report.

## Per-use-case verify scripts

| Script | Use-case | Exit 0 | Exit 1 |
|---|---|---|---|
| `verify_usecase_1_init.py` | 1 (Init) | DB openable, schema correct, all teams registered | Lists missing teams |
| `verify_usecase_2a_audit_deterministic.py` | 2a (Det Audit) | 10/10 domains per team | Lists missing (team, domain) pairs |
| `verify_usecase_2b_audit_semantic.py` | 2b (Sem Audit) | >=1 semantic row per domain per team | Lists missing combos |
| `verify_usecase_3_calculate.py` | 3 (Calculate) | One entry per team, no None fields | Names team/domain/field |
| `verify_usecase_4_analysis.py` | 4 (Analysis) | Narrative for every data-holding combo + competition-wide row | Lists missing combos |
| `verify_usecase_5_markdown_charts.py` | 5 (MD+Charts) | All PNG+MD exist, non-zero, no `{{}}` leftovers | Lists missing/stale files |
| `verify_usecase_6_html_report.py` | 6 (HTML) | All HTML exist, non-zero, no `{{}}`, no empty base64 | Lists issues |
| `verify_usecase_7_pdf_generation.py` | 7 (PDF) | One PDF per team, correct page count | Lists issues |

All accept `--standard python_hackathon [--team <name>]`. All print structured output on failure (which team, which domain, which file).

## Orchestrator

`verify_all_usecases.py --standard python_hackathon [--team <name>] [--stop-on-fail]`

- Calls each verify script's check function directly (not subprocess)
- Strict order: 1 -> 2a -> 2b -> 3 -> 4 -> 5 -> 6 -> 7
- `--stop-on-fail` (default True): halts at first failure
- Freshness cross-check: flags stale outputs (e.g. markdown newer than latest audit write)

## Coverage report (not a verify script)

`coverage_report.py --standard python_hackathon [--team <name>]`

- Answers "how far along is each team right now" (softer than strict yes/no)
- Useful mid-competition when most teams are legitimately incomplete
- Produces markdown report via `templates/reports/coverage-status.md`
- Shares query logic with verify_usecase_2a/2b scripts

## Coverage vs. verify — distinction

- **Verify scripts**: strict yes/no, pipeline-consistent state check. Fails = something is wrong.
- **Coverage report**: progress snapshot, not a failure detector. Incomplete = normal during competition.
