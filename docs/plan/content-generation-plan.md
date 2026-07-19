# Plan: Hybrid Content Generation (Scripts + MCP)

## Problem

Templates use `[Description of what content should go here]` bracket placeholders
(127 section templates across 15 domains). `content_fill()` looks for
`<!-- TODO: ... -->` markers. They never match. Result: all content stays empty,
scores are 0.0.

## Architecture: Three Composable Steps

Not a pipeline. Three independent steps that compose:

```
[Documents + Templates] ──> extract_content_gaps.py ──> content-gaps.json
                                                                │
                                                                v
                                                        MCP generates content
                                                        (reads schema, section_catalog,
                                                         templates, upstream context)
                                                                │
                                                                v
[Documents + MCP content] ──> apply_content.py ──> filled documents
```

### Step 1: `extract_content_gaps.py` (Script — deterministic)

**Input:** Scaffolded document + section_catalog + templates
**Output:** `content-gaps.json` — structured list of what content is needed

Scans documents for `[...]` bracket placeholders. For each marker:
- Extracts instruction text (e.g., "One sentence stating why the product exists")
- Maps to `section_catalog` entry (domain + semantic_type)
- Reads corresponding template from `templates` table/file
- Gathers upstream context from completed domains
- Outputs gap with: id, instruction, section_catalog_id, content_type, context

**Key:** Each gap maps to a `section_catalog` entry, so MCP knows the
section type, mandatory status, and sort order.

### Step 2: MCP Content Generation (Semantic — LLM)

**Input:** `content-gaps.json` + schema context
**Output:** `content-responses.json` — generated prose for each gap

MCP reads the gap report and uses the schema to generate content:
- `section_catalog` → what section type, mandatory/optional
- `templates` → the template definition and instructions
- `standard_docs` → the documentation standard for this domain
- Upstream context → content from higher-tier documents

MCP can:
- Generate content directly (call LLM with gap + context)
- Store content in DB (via `compile` or custom table)
- Write content to files (for script consumption)

### Step 3: `apply_content.py` (Script — deterministic)

**Input:** Documents + `content-responses.json`
**Output:** Updated documents with `[...]` markers replaced

Simple string replacement: find `[instruction]`, replace with generated content.
Validates all markers were replaced.

## Gap Report Format

```json
{
  "document": "01-vision",
  "domain": "vision",
  "gaps": [
    {
      "id": "gap-001",
      "marker": "[One sentence stating why the product exists and the problem it addresses]",
      "instruction": "One sentence stating why the product exists and the problem it addresses",
      "section_catalog": {
        "id": 1,
        "semantic_type": "purpose",
        "name": "Purpose",
        "mandatory": true
      },
      "content_type": "prose",
      "template_ref": "generation/document/01-vision.md",
      "upstream_context": {
        "philosophy": ["Core belief: documentation should be generated, not manually written..."]
      },
      "position": {"line": 15, "column": 0}
    }
  ],
  "summary": {
    "total_gaps": 45,
    "by_content_type": {"prose": 30, "table_row": 10, "bullet_list": 5},
    "by_domain": {"vision": 8, "philosophy": 4}
  }
}
```

## Response Format

```json
{
  "responses": [
    {
      "id": "gap-001",
      "content": "Kriti exists because teams waste weeks building documentation that never gets used — bridging the gap between product ideas and production-ready docs."
    }
  ]
}
```

## File Changes

### New Scripts

1. **`extract_content_gaps.py`** (~250 lines)
   - Scans documents for `[...]` markers
   - Maps markers to `section_catalog` entries
   - Reads templates for context
   - Gathers upstream context
   - Outputs structured gap report

2. **`apply_content.py`** (~100 lines)
   - Reads content-responses.json
   - Replaces `[...]` markers in documents
   - Validates replacement success
   - Reports: N markers replaced, M remaining

### Modified Files

3. **`_common.py`** — Add marker utilities
   - `extract_bracket_markers(content) -> list[dict]`
   - `replace_bracket_marker(content, marker_id, replacement) -> str`

4. **`init.py`** — Update `content_fill()` to use new approach
   - Replace regex-based `<!-- TODO -->` matching with `[...]` marker detection
   - Call `extract_content_gaps.py` to produce gap report
   - (Semantic step happens outside init.py — via MCP)
   - Call `apply_content.py` to inject responses

### Schema Alignment

5. **`extract_content_gaps.py`** reads from knowledge-hub schema:
   - `section_catalog` — maps markers to section types
   - `templates` — reads template content for context
   - `standard_docs` — reads documentation standards

   This means the gap report is schema-aware: each gap knows its
   section_catalog_id, so MCP can use this to query the DB for
   additional context (rules, relationships, etc.).

## Implementation Order

1. Build `extract_content_gaps.py` — marker extraction + section_catalog mapping
2. Build `apply_content.py` — marker replacement
3. Update `_common.py` with marker utilities
4. Update `content_fill()` in init.py
5. Test: scaffold vision → extract gaps → manually write 5 responses → apply → verify
6. Update proposal §11 and §24

## Verification

1. Run `extract_content_gaps.py` on a scaffolded vision document
2. Verify it extracts all `[...]` markers with correct section_catalog mappings
3. Manually write 3-5 content responses
4. Run `apply_content.py` to inject them
5. Verify the document has real content where markers were
6. Run evaluate_rules.py — scores should improve from 0.0

## MCP Integration Notes

The gap report is designed for MCP consumption:
- Each gap has a `section_catalog.id` — MCP can query the DB for
  additional context (rules, relationships, upstream dependencies)
- The `content_type` field tells MCP what kind of content to generate
- The `upstream_context` field provides the raw material for generation
- MCP can store generated content back to the DB (via `compile` or
  custom storage) for future reference

This means MCP doesn't need to re-scan documents — it reads the gap
report and generates content based on the structured context.
