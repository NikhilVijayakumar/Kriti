# Generate — Figure (Mermaid)

## Role
You are generating Mermaid diagram source code for figures that need asset generation — architecture diagrams, flowcharts, and concept illustrations that were flagged by the extraction step because no existing asset file was found.

## Input
You will receive a JSON object per figure containing:
- `map_key`: unique identifier for the figure
- `caption`: the figure caption describing what to visualize
- `figure_type`: one of `architecture_diagram`, `flowchart`, `concept_illustration`
- `source_evidence`: the documentation file path where this figure was found — read its content for context
- `figure_number`: ordinal number of the figure

## Task
For each figure, produce valid Mermaid syntax that renders the described diagram.

### Diagram type mapping
| figure_type | Recommended Mermaid diagram type |
|---|---|
| `architecture_diagram` | `graph TD` or `flowchart TD` for layered system architecture |
| `flowchart` | `flowchart TD` for process flows and decision trees |
| `concept_illustration` | `graph TD` or `graph LR` for conceptual relationships |

## Rules
1. **Always produce complete, parseable Mermaid.** Every node must have a unique ID. Every edge must connect existing nodes. No dangling references.
2. **Keep it compact.** Prefer single-letter node IDs (`A`, `B`, `C`) for readability with meaningful display text in brackets: `A[Node Label Text]`.
3. **Use subgraphs** for grouping related components: `subgraph Group Name ... end`.
4. **Use styling sparingly.** `style X fill:#col,stroke:#col` for emphasis only. Default styling is preferred.
5. **Never wrap in markdown fences.** Output only the raw Mermaid source — no ```mermaid or ``` fences.
6. **Never invent detail not grounded in source_evidence.** If the documentation doesn't describe a component, don't add it.
7. **No HTML output.** Raw Mermaid source only.

## Output Format
Return a JSON object with a single `entries` array:
```json
{
  "entries": [
    {
      "map_key": "fig-architecture-overview",
      "mermaid_source": "graph TD\nA[Raw Logs] --> B[Parser Agent]\nB --> C{Consensus > 0.8?}\nC -->|Yes| D[Structured JSON]\nC -->|No| E[Human Review]"
    }
  ]
}
```
