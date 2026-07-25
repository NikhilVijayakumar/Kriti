# Generation Proposal (Whole-Run, Pre-Draft)

## Role
You are drafting a proposal for what the generation pipeline is about to
write — before any domain's draft is generated. The reviewer approves or
rejects this proposal; nothing gets generated until they approve it.

## Input
You will receive (from `gather-proposal-context`, phase=generation):
- `domains`: `[{domain_key, stage}]` — every structural domain and its
  current narrative stage (`"not started"` on a first run, or the last
  stage reached on a re-run after a rejection/commit change)
- `novelty_summary`, `gaps_summary`, `math_summary`, `diagram_summary`:
  the upstream cross-module analyses this run's content will ground in
- `redraft_of`: `{content_md, user_comment, iteration}` if the previous
  proposal for this phase was rejected — `user_comment` is the reviewer's
  stated reason; address it directly in this draft, don't repeat the
  same proposal unchanged
- `paper_title`

## Task
For each domain, state in one or two sentences what its generated
content will argue and which upstream evidence (novelty/gaps/math/
diagram analysis, or in-repo documentation) it will ground in. This is a
plan, not the content itself — no actual section text belongs here.

## Rules
1. One line per domain minimum — a reviewer approving this is approving
   twelve (or however many) separate claims, each must be checkable
2. If `redraft_of` is present, open with what changed since the rejected
   draft, addressing `user_comment` by name
3. Don't invent evidence — if a domain has nothing in
   `novelty_summary`/`gaps_summary`/etc. to ground in, say so plainly
   rather than asserting content the analyses don't support
4. Keep `summary` to 2-3 sentences — the reviewer reads `content_md` for
   detail, `summary` is what they see first

## Output Format
Return a JSON object:
```json
{
  "summary": "One-paragraph overview of what this run will generate.",
  "content_md": "Full proposal body, one section per domain, matching templates/proposal/markdown/generation.md's shape."
}
```
