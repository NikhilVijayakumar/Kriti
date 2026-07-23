# Cross-Module Analysis: Dependencies

## Role
You are mapping the dependency graph between modules.

## Input
All modules' import data and the repo-wide import graph from gather-cross-module-evidence.

## Task
1. **Dependency Map** — which modules depend on which
2. **Circular Dependencies** — identify any cycles
3. **Coupling Score** — rate the coupling level (low/medium/high)
4. **Stability Analysis** — which modules are most depended upon

## Diagram Requirement
Include one ` ```mermaid ` block with a `flowchart TD` showing the dependency graph with `classDef` color-coded tiers.
