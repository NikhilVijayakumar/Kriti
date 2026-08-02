# samgraha — rust_dev activation blocked: `resolve_manifest_path` layout gap

**Component:** samgraha tooling (`E:\Python\samgraha`)
**Severity:** HIGH (blocks activating any standard whose manifest lives under `common/schema-manifest/`)
**Status:** OPEN

---

## TL;DR

`rust_dev` cannot be activated in a repo because the global registry holds a stale,
incomplete copy of the standard, and `samgraha`'s `resolve_manifest_path` does not
recognize rust_dev's manifest location (`common/schema-manifest/standard.yaml`), so the
registry cannot be re-populated from the real source root either.

## Symptom

`samgraha_register_standard` (activate) fails:

```
declared location does not exist: E:\Python\Kriti\.samgraha\rust_dev\../script/seeder.py
```

## Root cause (2 compounding problems)

### 1. Registry copy is incomplete

`standards.db` `operation_log` (ids 12–19) shows every `register_globally`/`update_standard`
for rust_dev used:

```
path = E:\Python\Kriti\samgraha\system\dev\rust_dev\common\schema-manifest
```

i.e. the **manifest directory only**, not the standard's source root. The registry copy at
`E:\MCP\Samgraha\release\samgraha\bin\registry\common\rust_dev\` therefore holds only:

- `standard.yaml`
- `standard.metadata.json`

It is missing the entire standard tree — `common/script/seeder.py`,
`common/schema/*.sql`, `domain/`, `tier*/`, `plan/`, `script/`, `templates/`.

Activation (`activate_standard` in `register_standard.rs`) copies that incomplete tree into
`<repo>\.samgraha\rust_dev\`, then resolves `seeder_script: ../script/seeder.py` against the
manifest dir → `<repo>\.samgraha\rust_dev\..\script\seeder.py`, which does not exist.

### 2. `resolve_manifest_path` doesn't know rust_dev's layout

`E:\Python\samgraha\crates\services\src\register_standard.rs:418`:

```rust
pub fn resolve_manifest_path(standard_path: &Path) -> Result<PathBuf> {
    let primary = standard_path.join("standard.yaml");
    if primary.is_file() { return Ok(primary); }
    let alt = standard_path.join("script/schema/standard.yaml");
    if alt.is_file() { return Ok(alt); }
    bail!("No standard.yaml at {} or {}", ...);
}
```

Only two layouts supported:

- `<root>/standard.yaml`
- `<root>/script/schema/standard.yaml` (pcems_2026 style)

rust_dev declares its manifest at `<root>/common/schema-manifest/standard.yaml`
(proposal 1 restructure). So `register_standard_globally` with
`path = E:\Python\Kriti\samgraha\system\dev\rust_dev` fails with:

```
No standard.yaml at E:\Python\Kriti\samgraha\system\dev\rust_dev\standard.yaml or
E:\Python\Kriti\samgraha\system\dev\rust_dev\script/schema/standard.yaml
```

The only workaround that currently "succeeds" is passing the manifest dir itself — which is
exactly what created problem 1.

## Fix plan (when batching samgraha fixes)

1. Extend `resolve_manifest_path` to also accept `<root>/common/schema-manifest/standard.yaml`.
   Add a test mirroring the existing `nested-manifest` tests in `register_standard.rs`.
2. Rebuild samgraha binaries (`cli.exe` / `mcp.exe`).
3. Re-register rust_dev globally from the **full source root**:
   `samgraha_register_standard_globally(path = E:\Python\Kriti\samgraha\system\dev\rust_dev)`.
   Confirms registry copy now contains the whole tree.
4. Activate: `samgraha_register_standard(standard_name = rust_dev, repo_path = E:\Python\Kriti)`.
   Seeder runs, creates 10 `dev_*` tables, seeds 13 domains + 96 usecases.
5. Re-run `samgraha_validate_standard_metadata` (Layer A + B) and
   `samgraha_get_standard_usecases` to confirm.

## Side notes / related observations

- `verify_status` for rust_dev is `unverified` (no `smoke_test` declared in the manifest;
  that is by design, not part of this issue).
- The registry `standard.yaml` is byte-identical to the source manifest — only the *tree*
  around it is missing.
- Guardrail to prevent recurrence: `register_standard_globally` passing a directory that
  contains only a manifest (vs a full standard root) should be rejected or warned about.
