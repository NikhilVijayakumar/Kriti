# Migration Guide to rust_dev

If you are upgrading a repository from `base_dev` to `rust_dev`:

1. **Delete Obsolete Domains:** You may safely delete `06-design`, `09-feature-design`, and `11-prototype` from your project's `.planning/` directory.
2. **Add New Sections:** Update your `05-architecture` to include Crate Architecture and Trait Design.
3. **Update Config:** Set `system = "rust_dev"` in your project's configuration.

## Domain Mapping

| Dropped `base_dev` Domain | Where Content Belongs in `rust_dev` |
|---|---|
| `06-design` | UI elements discarded. Conceptual models go to `04-feature`. |
| `09-feature-design` | Workflow/states map to `04-feature` API Contracts and State Machines. |
| `11-prototype` | No longer applicable. Systems require full implementations designed in `10-feature-technical`. |

## Upgrading

- All existing slot numbers that clash with the new templates (e.g. slots 09-12 in `07-engineering`) must be correctly renamed or deleted if they were base_dev stubs.
