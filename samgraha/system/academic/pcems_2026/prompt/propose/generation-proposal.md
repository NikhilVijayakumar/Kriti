# Generation Proposal (Whole-Run, Pre-Draft)

## Role
You are drafting a proposal for what the generation pipeline is about to
write — before any domain's draft is generated. The reviewer approves or
rejects this proposal; nothing gets generated until they approve it.

## Input
You will receive (from `gather-proposal-context`, phase=generation):
- `domains`: `[{domain_key, stage, word_min, word_max, check_count,
  critical_count}]` — every structural domain and its current narrative
  stage, word budget range, and deterministic rule counts. The template
  renders these in the "What Will Be Generated" table; don't restate
  the numbers in `content_md` — write about *why* each domain's
  content will take the shape the rules require.
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

## Domain Guide Grounding
Each domain's content should be traceable to specific guide sections:
- title-and-metadata → Template §1, header format
- introduction → Writing Guide §2, Reviewer Expectations/03
- methodology → Writing Guide §4, Mathematics/01-03
- findings → Writing Guide §5, Tables/01-03, Figures/01-03
- conclusion → Writing Guide §6, Philosophy contribution threading
- references → Writing Guide §7, IEEE numbered style per sample papers (template says APA — see 07-references.md), 15–30 count
- novelty → Philosophy contribution visibility
- gaps → Writing Guide gap-analysis framing
- mathematics → Mathematics/01-03 formatting rules
- tables → Tables/01-03 standards (validation-only)
- figures → Figures/01-03 standards (validation-only)

## Rules
1. One line per domain minimum — a reviewer approving this is approving
   eleven (or however many) separate claims, each must be checkable
2. If `redraft_of` is present, open with what changed since the rejected
   draft, addressing `user_comment` by name
3. Don't invent evidence — if a domain has nothing in
   `novelty_summary`/`gaps_summary`/etc. to ground in, say so plainly
   rather than asserting content the analyses don't support
4. Keep `summary` to 2-3 sentences — the reviewer reads `content_md` for
   detail, `summary` is what they see first
5. The "What Will Be Generated" table is computed from the same rule
   files `deterministic_audit.py` reads — don't repeat those numbers in
   `content_md`, write about what they mean for this domain's content

## Output Format
Return a JSON object:
```json
{
  "summary": "One-paragraph overview of what this run will generate.",
  "content_md": "Full proposal body, one section per domain, matching templates/proposal/markdown/generation.md's shape.",
  "computed_context": "<pass through the full domains array and analysis summaries from Input — persist stores this for template rendering>"
}
```
