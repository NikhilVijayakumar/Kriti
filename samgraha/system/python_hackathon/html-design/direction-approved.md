# Direction Approved

**Date**: 2026-07-20

## What was shown

Three parallel directions, each producing 2 representative pages
(`01-infrastructure-summary`, `global-leaderboard`), per the huashu-design
skill's mandatory three-direction gate:

| Direction | Logic | Screenshots |
|---|---|---|
| A — Swiss Monochrome | 🎲 Roulette (`date +%S` → 58 → style #19) | `design-demos/swiss-monochrome-{summary,leaderboard}.png` |
| B — Chatbot Arena reference | 🏆 Real-world reference (lmarena.ai leaderboard) | `design-demos/arena-ref-{summary,leaderboard}.png` |
| C — GitHub Primer | 🧠 Best-designer pick (status-color language, CI-checks analog) | `design-demos/primer-{summary,leaderboard}.png` |

## User's decision

First response: "leaderboard c is better summary b is beeter so may be we
van mix and match or stick with c" — ambiguous between two paths (mix
C+B, or C alone). Asked to confirm before locking in.

**Final answer** (AskUserQuestion): **"Stick with C for both"** —
GitHub Primer direction, for both the leaderboard and the
domain-summary page types, and by extension the full page set (all 5
template kinds × 10 domains + team-final-summary + global-leaderboard).

## Rationale (user-facing reasoning offered, accepted)

One consistent design system end-to-end beats mixing two visual
languages across a 31-page-per-team deck — a judge/team flipping
through the full report should see one coherent report, not two
different apps stitched together. C's status-color language (green
Success / yellow Attention / red Danger) already read well on both
page types shown.

## What this locks

- Color carries semantic meaning only (score-band status), never
  decoration — GitHub Primer's actual palette: success `#1a7f37`/
  `#dafbe1`, attention `#9a6700`/`#fff8c5`, danger `#cf222e`/`#ffebe9`.
- Monospace + `tabular-nums` for every literal score/count/identifier.
- Light background (print/PDF-friendly, per the per-team PDF export
  requirement).
- Status badges as the primary at-a-glance signal, applied identically
  across every page type so the color key is learned once.

## Not yet decided (next step)

Building out the full HTML template set (all 5 kinds × 10 domains +
2 aggregate pages) wired to real data via `render_reports.py`'s
existing 5 fetch functions, matching the demo pages' structure and
Primer's visual language exactly.
