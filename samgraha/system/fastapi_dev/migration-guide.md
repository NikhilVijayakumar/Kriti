# Migration Guide to fastapi_dev

If you are upgrading a repository from `base_dev` to `fastapi_dev`:

1. **Delete Obsolete Domains:** You may safely delete `06-design` and `09-feature-design` from your project's `.planning/` directory.
2. **Update Prototype:** Update your `11-prototype` documents to describe mock endpoints rather than UI mockups.
3. **Add New Sections:** Update your `05-architecture` to include Layered Architecture, and `07-engineering` to include Async Patterns and Response Models.
4. **Update Config:** Set `system = "fastapi_dev"` in your project's configuration.
