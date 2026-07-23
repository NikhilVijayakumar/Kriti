# Cross-Module Analysis: Interactions

## Role
You are analyzing how modules interact at runtime — not just static imports, but data flow and control flow.

## Input
All modules' analyses and the dependency graph.

## Task
1. **Data Flow** — how data moves between modules
2. **Control Flow** — which modules orchestrate others
3. **Event Patterns** — callbacks, signals, message passing
4. **Shared State** — any shared databases, caches, or global state

## Diagram Requirement
Include one ` ```mermaid ` block with a `flowchart TD` showing interaction patterns with `classDef` color-coded tiers.
