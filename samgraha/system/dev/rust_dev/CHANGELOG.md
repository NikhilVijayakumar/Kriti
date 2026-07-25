# Changelog: rust_dev

## [1.0.0] - 2026-07-15
### Added
- Systems-specific templates for architecture, engineering, and feature technical.
- New Rust-specific semantic audit rules (ownership, async, unsafe).
- Cargo audit check.

### Removed
- Dropped `06-design` domain.
- Dropped `09-feature-design` domain.
- Dropped `11-prototype` domain (systems require full implementation from start).

### Changed
- Re-aligned Tier 3 to only contain `feature-technical`.
- Removed Tier 4 (prototype).
