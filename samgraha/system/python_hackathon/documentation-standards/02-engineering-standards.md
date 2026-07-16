# 02. Engineering Standards

**Domain:** Engineering Quality
**Audit Target:** `radon.cfg`, `pyproject.toml` (type checkers)

## Standard Definition
Hackathon code must prioritize maintainability. The project should employ automated complexity checks and static type analysis to prevent technical debt from accumulating during rapid development.

### Expected Evidence
1. **Complexity Bounds:** Configuration for Radon (or similar) to enforce cyclomatic complexity limits.
2. **Type Safety:** Use of `mypy` or `pyright` enabled within the repository configuration.
