# 02. Engineering Standards

**Domain:** Engineering
**Audit Target:** Code quality configs, type hints, CI/CD

## Standard Definition
Code quality is measured through linting, type checking, and static analysis. Teams should have proper tooling configured and passing. Automated CI/CD pipelines with real workflow content are expected. Code should be organized across multiple directories rather than a single monolithic folder.

### Expected Evidence
1. **Linting:** Flake8 or Ruff configuration present.
2. **Type Checking:** Mypy or Pyright configuration present.
3. **Complexity:** No high-complexity functions (Radon grade C or worse).
4. **Type Errors:** Zero mypy type errors.
5. **CI/CD:** GitHub Actions or GitLab CI pipeline configured with real workflow content (on: triggers, jobs: blocks — not empty stubs).
6. **Folder Structure:** At least 2 top-level directories (excluding hidden/venv/__pycache__), indicating separated concerns.
