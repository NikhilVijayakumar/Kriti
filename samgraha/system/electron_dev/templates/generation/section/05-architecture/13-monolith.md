# Single-Process Desktop Architecture — Generation Template

> **Domain:** architecture
> **Section:** single_process_architecture
> **Source:** `documentation-standards/05-architecture-standards.md` §Single-Process Desktop Architecture
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Single-Process Desktop Architecture section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `alternative_to` | architecture / desktop_service_architecture | Single-Process Architecture is a simplification of the three-process model for applications that do not need full process isolation |
| `constrains` | engineering / code_standards | Single-process constraint eliminates IPC patterns; all service communication is in-process |

## Template

```markdown
## Single-Process Desktop Architecture

### Architecture Decision

[1 paragraph: when and why a desktop application chooses to run all logic in the Main process, eliminating Renderer process service responsibilities]

#### When Single-Process Applies

| Criterion | Requirement |
|-----------|-------------|
| **UI complexity** | [minimal UI — dialogs, settings panels, system tray menus] |
| **Security surface** | [no untrusted content rendering, no user-provided HTML] |
| **Performance** | [no IPC overhead tolerance, low-latency requirement] |
| **Offline operation** | [full functionality without network, no cloud sync] |

#### When to Migrate to Three-Process

| Trigger | Signal | Migration Priority |
|---------|--------|-------------------|
| User-provided content | [rendering markdown, HTML, or third-party data] | **Critical** — renderer sandbox is mandatory |
| Multi-window UI | [multiple BrowserWindow instances with shared state] | **High** — IPC abstraction eliminates shared-state bugs |
| Plugin system | [loading untrusted extensions or addons] | **Critical** — process isolation prevents privilege escalation |
| Background sync | [periodic network operations independent of UI] | **Medium** — background process avoids blocking main thread |

### Bundled Services

[1 paragraph: in single-process mode, all services run inside the Main process and communicate via direct function calls instead of IPC]

#### Service Inventory

| Service | Responsibility | Dependencies | Initialization Order |
|---------|---------------|-------------|---------------------|
| `[ServiceName]` | [what it owns] | `[dependency list]` | [1-based order] |

#### Initialization Sequence

```
Application Start
├── 1. Configuration Service    (load and freeze config)
├── 2. Storage Service          (initialize databases, open file handles)
├── 3. [Domain Service]         (depends on Configuration + Storage)
├── 4. [Domain Service]         (depends on Configuration)
├── 5. UI Service               (depends on all domain services)
└── 6. Window Creation          (depends on UI Service)
```

#### Shutdown Sequence

```
Application Quit
├── 1. Close all windows
├── 2. Flush pending operations (timeout: [ms])
├── 3. Dispose services in reverse initialization order
├── 4. Release file handles and database connections
└── 5. Exit process
```

### Preload Script as Isolation Boundary

[1 paragraph: even in single-process architecture, the Preload script defines the API surface exposed to the Renderer — this boundary is critical when the Renderer handles any user-provided content]

#### contextBridge API Surface

| API Name | Methods | Return Type | Process |
|----------|---------|-------------|---------|
| `[apiName]` | `[method1, method2]` | `[type]` | Preload (bridge) |

#### Isolation Rules

| Rule | Description |
|------|-------------|
| **No direct fs access** | Renderer must never import or call `fs` — all file operations go through Preload-exposed API |
| **No native modules** | Renderer must not import native Node.js modules — use Preload bridge for system operations |
| **No process object** | Renderer must not access `process`, `require`, or `global` — contextBridge strips these |
| **Channel whitelist** | Preload only exposes channels listed in the API contract — no dynamic channel registration |

### Single-Process Tradeoffs

| Advantage | Disadvantage |
|-----------|-------------|
| Zero IPC overhead — direct function calls | No process isolation — a Renderer crash takes down the entire app |
| Simpler debugging — single call stack | No sandbox — Renderer has implicit access to Main process capabilities |
| Shared memory — no serialization cost | State mutations are uncontrolled — any service can modify any other service's data |
| Faster startup — no process spawning | No security boundary — user-provided content has same privilege as application code |
| Lower memory footprint — one V8 heap | Harder to reason about concurrency — shared event loop |

### Configuration Lock

[1 paragraph: configuration is loaded once at startup, frozen, and shared across all services — no IPC config transfer needed in single-process mode]

```
Configuration Lifecycle (Single-Process):
1. Configuration Service loads from disk
2. Config object frozen with Object.freeze
3. All services receive reference at initialization
4. No runtime mutation — restart required for changes
```

### Storage Domains

| Domain | Purpose | Persistence | Access Pattern |
|--------|---------|-------------|----------------|
| **Local** | UI state, ephemeral cache | sessionStorage | direct read/write |
| **Vault** | Credentials, secrets, tokens | encrypted file system | async read/write via Storage Service |
| **Document** | User files, project data | file system (user-chosen path) | async read/write via Storage Service |

### Architecture Diagram

[Diagram showing single Main process with bundled services, Preload script boundary, and Renderer with restricted API access]
```

## Examples

**Correct:**
> **Settings Dialog Application**
>
> This application manages system preferences through a settings dialog. It runs entirely in the Main process because:
> - The UI contains no user-provided content — only application-controlled form elements
> - All configuration is read from and written to local files on the same machine
> - No network communication is required
> - The UI is a single BrowserWindow with a fixed set of settings panels
>
> **Bundled Services:**
> | Service | Responsibility | Initialization Order |
> |---------|---------------|---------------------|
> | Configuration | Load settings from disk, freeze, provide accessors | 1 |
> | Storage | Manage file read/write for settings and backup | 2 |
> | Validation | Validate settings values against schema | 3 (depends on Configuration) |
> | UI | Manage BrowserWindow lifecycle and settings panel rendering | 4 (depends on all) |
>
> **Preload Isolation:** Even though the app runs in single-process mode, the Preload script exposes only `settings:get`, `settings:set`, and `settings:validate` — the Renderer cannot access `fs`, `process`, or any other Node.js global.

**Incorrect:**
> The application runs everything in one process for simplicity. The main process handles all the business logic and also renders the UI. There's no IPC because everything runs in the same V8 heap. If we need to scale, we can add IPC later.
> *Why wrong: describes implementation approach without architectural analysis. Missing: when single-process is appropriate, what isolation boundaries exist, initialization/shutdown sequences, tradeoff analysis, and the Preload script's role as a security boundary.*

## Writing Guidance

- **Tone:** analytical
- **Voice:** imperative
- **Structure:** tables and diagrams
- **Audience:** architect
- **Do:** Clearly state the decision criteria for single-process vs. three-process; document the Preload script as a hard isolation boundary even in single-process mode; provide initialization and shutdown sequences; analyze tradeoffs explicitly
- **Don't:** Treat single-process as a simplification that removes all architecture; omit the Preload boundary — it is required even in single-process apps; conflate single-process with monolithic web applications; skip failure analysis because "there's no IPC to fail"

**Required subsections:** Architecture Decision, Bundled Services, Preload Script as Isolation Boundary, Single-Process Tradeoffs
**Optional subsections:** Configuration Lock, Storage Domains, Migration Path to Three-Process
**Required diagrams:** architecture diagram showing Main process, Preload boundary, and Renderer
**Required cross-references:** Desktop Service Architecture (the three-process alternative), Security Considerations, Component Model

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
