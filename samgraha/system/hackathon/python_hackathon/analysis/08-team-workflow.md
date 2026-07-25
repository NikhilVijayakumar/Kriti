# Team Workflow Analysis Prompt

Guides the per-team analysis for the Team Workflow domain — read by
whichever agent runs it via MCP, after scoring has completed. Explains
how well a team collaborated based on git history. Not parsed by a
script — this is a prompt.

## Version
1.0.0

## Analysis Intent
Team Workflow scores (weight: 8) measure collaboration quality through
git history analysis. A hackathon is a team effort — this domain
rewards evidence of real collaboration vs solo work. Scores are partly
deterministic (commit counts, author diversity) and partly semantic
(task division clarity).

## Inputs
- `standard_domain_scores` DB table — all teams' team-workflow domain
  scores (queried via MCP)
- Per-team deterministic findings: total commit count, unique author
  count, commit message quality, branch structure, PR/merge evidence
- Semantic findings: task division clarity from README or commit
  history, GitFlow adherence, collaboration patterns

## Narrative Guidance
The Team Workflow narrative must cover:
1. **Score Overview** — team's workflow score out of 8, with competition
   average comparison.
2. **Commit Activity** — total commit count (minimum 5 expected). Is
   the history indicative of iterative development or a single bulk
   commit?
3. **Author Diversity** — how many unique contributors? Single-author
   repos score poorly even with many commits. Name the author count.
4. **Commit Quality** — are commit messages descriptive and
   conventional? "fix", "update", "wip" messages signal low workflow
   discipline.
5. **Branch Strategy** — is there evidence of feature branches, PRs,
   or merge commits? Or is everything on `main`? GitFlow signals are
   rewarded.
6. **Task Division** — semantic analysis: can you tell from the git
   history or README who worked on what? Clear division of labor is a
   positive signal.
7. **Strengths** — many contributors, clean commit messages, PR-based
   workflow, clear task ownership.
8. **Weaknesses** — single author, "wip" commits, no branch strategy,
   all commits in one burst, unclear who did what.
9. **Recommendations** — "use conventional commit messages
   (feat/fix/chore)", "create feature branches for remaining work",
   "add a CONTRIBUTING.md or section in README documenting team roles".

## Visualization Guidance
- `domain_scores` — always include.
- `commit_timeline` — include: scatter plot of commits over time per
  author, color-coded by contributor.
- `author_contribution` — include: pie chart of commit distribution
  across team members.

## Output Schema
```json
{
  "domain": "08-team-workflow",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "Commit Activity", "text": "..."},
    {"heading": "Author Diversity", "text": "..."},
    {"heading": "Commit Quality", "text": "..."},
    {"heading": "Branch Strategy", "text": "..."},
    {"heading": "Task Division", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
