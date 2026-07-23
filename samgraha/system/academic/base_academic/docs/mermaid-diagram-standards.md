# Mermaid Diagram Standards

Shared conventions for all mermaid diagrams emitted by academic-class semantic
steps. Every diagram-emitting prompt includes this file's rules verbatim.

## General Rules

- Every diagram is a fenced ` ```mermaid ` block
- Open with `%%{init: {'theme': 'base'}}%%`
- One diagram per concept — don't overload a single block
- Every diagram must have a caption referenced in prose before or after

## Per-Diagram-Type Rules

### classDiagram (module-level architecture)
- One class per major component
- Use `<<stereotype>>` annotations for design patterns:
  - `<<Singleton Component>>`, `<<Facade>>`, `<<Factory>>`, `<<Observer>>`
- Show relationships: `-->` (dependency), `*--` (composition), `o--` (aggregation), `<|--` (inheritance)
- Keep to 8-12 classes maximum

### flowchart TD (cross-module dependencies/interactions)
- Use `classDef` color-coded tiers:
  ```mermaid
  classDef core fill:#e1f5fe,stroke:#0288d1
  classDef support fill:#f3e5f5,stroke:#7b1fa2
  classDef shared fill:#e8f5e9,stroke:#388e3c
  classDef external fill:#fff3e0,stroke:#f57c00
  ```
- Apply tier classes to nodes: `class A core`
- Show coupling direction with arrows
- Keep to 15-20 nodes maximum

### No Diagram Sections
- `mathematics.md`: LaTeX only (`$...$` / `$$...$$`), no mermaid
- `novelty.md`: prose with evidence links only
- `gaps.md`: prose with code references only

## Evidence Links
When referencing code in diagrams or prose, use:
```
[SymbolName](file:///path/to/file.py#L42)
```
This pattern is already proven in `Bodha/docs/paper/Amsha/cross_module/novelty.md`.
