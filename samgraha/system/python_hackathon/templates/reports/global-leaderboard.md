# Hackathon Global Leaderboard

**Date Generated:** `{{ report_date }}`
**Total Teams Evaluated:** `{{ total_teams }}`

---

## Final Competition Results

The following leaderboard represents the final grading of all hackathon submissions across the 10 engineering domains. Scores have been standardized (Z-score applied) and bounded out of 20 points to ensure fair relative grading.

| Rank | Team / Repo | Total Score | Inf | Eng | Tst | Doc | Sec | MLOps | Run | T-W | D-Q | AI-E |
|------|-------------|-------------|-----|-----|-----|-----|-----|-------|-----|-----|-----|------|
{{#each teams as |team|}}
| **{{ team.rank }}** | `{{ team.repo_name }}` | **{{ team.final_score }}/20** | {{ team.scores.infrastructure }} | {{ team.scores.engineering }} | {{ team.scores.testing }} | {{ team.scores.documentation }} | {{ team.scores.security }} | {{ team.scores.mlops }} | {{ team.scores.runtime }} | {{ team.scores.team_workflow }} | {{ team.scores.data_quality }} | {{ team.scores.ai_explanations }} |
{{/each}}

---

## Statistical Overview

| Domain Section | Global Mean | Global Std Dev |
|----------------|-------------|----------------|
| Infrastructure | {{ global_stats.infrastructure.mean }} | {{ global_stats.infrastructure.stdev }} |
| Engineering | {{ global_stats.engineering.mean }} | {{ global_stats.engineering.stdev }} |
| Testing | {{ global_stats.testing.mean }} | {{ global_stats.testing.stdev }} |
| Documentation | {{ global_stats.documentation.mean }} | {{ global_stats.documentation.stdev }} |
| Security | {{ global_stats.security.mean }} | {{ global_stats.security.stdev }} |
| MLOps | {{ global_stats.mlops.mean }} | {{ global_stats.mlops.stdev }} |
| Runtime | {{ global_stats.runtime.mean }} | {{ global_stats.runtime.stdev }} |
| Team Workflow | {{ global_stats.team_workflow.mean }} | {{ global_stats.team_workflow.stdev }} |
| Data Quality | {{ global_stats.data_quality.mean }} | {{ global_stats.data_quality.stdev }} |
| AI Explanations | {{ global_stats.ai_explanations.mean }} | {{ global_stats.ai_explanations.stdev }} |
