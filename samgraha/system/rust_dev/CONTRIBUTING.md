# Contributing to rust_dev

If you wish to extend the `rust_dev` system, follow these guidelines:

## Adding a New Generation Template
1. Create the template in `templates/generation/section/NN-domain/`.
2. Ensure it includes a YAML front-matter header, `Relationships` table, `Generation note`, and `Audit Fix` stub.
3. Use H1 for the top-level section title.

## Adding a New Semantic Audit Rule
1. Create the `.md` rule in `audit/semantic/section/NN-domain/`.
2. Follow the standard format with `Severity`, `Context & Rationale`, `Audit Check`, `Anti-patterns`, and `Remediation`.
3. Avoid slot collisions with existing base_dev rules.

## Adding Deterministic Rules
1. If adding a new section, create a corresponding structural `.yaml` file in `audit/deterministic/section/`.
2. Update the domain-level `.yaml` in `audit/deterministic/document/` to require the new semantic type.

## Updating Relationships
If your changes introduce new cross-domain dependencies, document them in `00-domain-relationships.md` and update the relevant `*-relationships.yaml` files.
