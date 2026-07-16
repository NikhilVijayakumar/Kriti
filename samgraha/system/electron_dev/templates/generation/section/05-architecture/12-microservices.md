# Desktop Service Architecture — Generation Template

> **Domain:** architecture
> **Section:** desktop_service_architecture
> **Source:** `documentation-standards/05-architecture-standards.md` §Desktop Service Architecture
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Desktop Service Architecture section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / component_responsibilities | Desktop Service Architecture must define the process-scoped components that Feature Technical Design's component responsibilities section references |
| `constrains` | engineering / code_standards | Service boundaries and IPC contracts constrain implementation code standards |

## Template

```markdown
## Desktop Service Architecture

### Process Model

[1 paragraph: overview of the three-process architecture — Main, Renderer, Preload — and why process isolation is the primary service boundary in desktop applications]

#### Main Process Services
- **Responsibility:** [what the Main process owns — system access, OS integration, lifecycle management]
- **Isolation Boundary:** [what is protected by running in Main — file system, network, native modules]
- **Interfaces:** [IPC handle registration, app lifecycle events, system tray integration]

#### Renderer Process Services
- **Responsibility:** [what the Renderer process owns — UI rendering, user interaction, DOM management]
- **Isolation Boundary:** [what is protected by running in Renderer — no direct system access, sandboxed execution]
- **Interfaces:** [IPC invoke calls, DOM event listeners, UI state mutations]

#### Preload Script Services
- **Responsibility:** [what the Preload script owns — contextBridge API surface, secure channel exposure]
- **Isolation Boundary:** [what crosses the boundary — whitelisted IPC channels, typed API objects]
- **Interfaces:** [contextBridge.exposeInMainWorld, ipcRenderer.invoke, ipcRenderer.send]

### IPC Channel Design

[1 paragraph: how IPC channels form the service communication layer between processes]

#### Channel Naming Convention

| Pattern | Direction | Use Case |
|---------|-----------|----------|
| `domain:action` | Renderer → Main | Request-response: invoke a Main process service method |
| `domain:event` | Main → Renderer | Push notification: broadcast state changes or system events |
| `domain:command` | Renderer → Main | Fire-and-forget: trigger side effects without response |

#### Channel Inventory

| Channel Name | Pattern | Sender | Receiver | Payload Contract | Response Type |
|-------------|---------|--------|----------|-----------------|---------------|
| `[domain:action]` | request-response | Renderer | Main | `{input: [type]}` | `{result: [type]}` |
| `[domain:event]` | broadcast | Main | Renderer | `{event: [type], data: [type]}` | none |
| `[domain:command]` | fire-and-forget | Renderer | Main | `{command: [type]}` | void |

### Service Registry

[1 paragraph: how the service registry provides singleton service factories and dependency resolution within the Main process]

#### Registry Pattern

```
ServiceRegistry
├── register(name, factory)    — bind a service name to a factory function
├── resolve(name)              — return singleton instance, creating on first access
├── dispose(name)              — tear down a single service
└── disposeAll()               — orderly shutdown of all registered services
```

#### Registered Services

| Service Name | Factory | Dependencies | Lifecycle Scope |
|-------------|---------|-------------|-----------------|
| `[ServiceName]` | `[factory function]` | `[dependency list]` | `[process / window / app]` |

### Service Lifecycle

[1 paragraph: the four-phase lifecycle every desktop service follows]

| Phase | Trigger | Behavior | Failure Mode |
|-------|---------|----------|--------------|
| **INIT** | App startup or first resolve | Allocate resources, establish connections, load configuration | Retry with backoff or degrade gracefully |
| **LOADING** | Dependencies resolved | Fetch initial data, warm caches, register IPC handlers | Queue requests until ready |
| **COMPLETED** | All async work settled | Service fully operational, ready to handle requests | Log and emit health status |
| **DISPOSED** | App shutdown or explicit teardown | Release resources, unregister IPC handlers, flush pending work | Force-kill after timeout |

### Process Health Monitoring

[1 paragraph: how the application monitors process health and handles failures]

#### Health Check Protocol

| Check Type | Interval | Scope | Failure Action |
|-----------|----------|-------|----------------|
| **Renderer heartbeat** | [interval] | Main → Renderer | [reload / destroy window / show error] |
| **Main process responsiveness** | [interval] | Renderer → Main (invoke ping) | [show dialog / attempt recovery] |
| **Service readiness** | per-request | Registry query | [queue / reject / fallback] |

#### Recovery Strategies

| Failure Scenario | Detection | Recovery |
|-----------------|-----------|----------|
| Renderer crash | Process exit event | [recreate window / restore state from Main] |
| Main process hang | Heartbeat timeout | [show unresponsive dialog / force restart] |
| IPC channel timeout | Promise rejection after [ms] | [retry / show error / degrade feature] |
| Service initialization failure | INIT phase error | [skip dependent features / show limited mode] |

### Service Dependency Graph

[Diagram showing service dependencies across process boundaries]

### Configuration Lock

[1 paragraph: how configuration is loaded once at INIT and becomes immutable for the service lifetime — prevents runtime state drift between processes]

```
Configuration Lifecycle:
1. Main process loads config from disk at INIT
2. Config object is frozen (Object.freeze)
3. Renderer receives config via IPC at window creation
4. No runtime config mutation — restart required for changes
```

### Storage Domains

| Domain | Process | Purpose | Persistence |
|--------|---------|---------|-------------|
| **Local** | Renderer | UI state, ephemeral cache | sessionStorage |
| **Vault** | Main | Credentials, secrets, tokens | encrypted file system |
| **Document** | Main | User files, project data | file system (user-chosen path) |

### Service Diagram

[Architecture diagram showing three processes, service registry in Main, contextBridge boundary, and IPC channels connecting services]
```

## Examples

**Correct:**
> **File System Service**
> - **Responsibility:** All file system operations — read, write, watch, stat — are serialized through this service. No other Main process service may call `fs` directly.
> - **Isolation Boundary:** Runs in Main process with full file system access. Renderer process has zero file system access.
> - **Interfaces:** Exposes `file:read`, `file:write`, `file:watch`, `file:stat` IPC channels. Returns typed `Result<T, FileError>` responses.
>
> **Service Registry:**
> - `register('fileSystem', () => new FileSystemService(config.storage.documentPath))`
> - `resolve('fileSystem')` returns singleton, creating on first call
> - Dependencies: `configuration` (must be INIT-complete before resolve)
>
> **IPC Channel: `file:read`**
> - Pattern: request-response
> - Sender: Renderer
> - Receiver: Main (FileSystemService)
> - Payload: `{ path: string, encoding?: BufferEncoding }`
> - Response: `{ ok: true, data: Buffer } | { ok: false, error: FileError }`

**Incorrect:**
> The Electron app uses IPC to communicate between the main process and renderer. The main process runs a file system service that the renderer calls via `ipcRenderer.invoke('read-file', filePath)`. It uses `fs/promises` internally and wraps errors in a custom `FileError` class. The service is registered as a singleton in a `ServiceContainer` class.
> *Why wrong: mixes implementation details (class names, import paths, error class names) with architectural description. Architecture should define the service boundary, channel contract, and lifecycle — not the internal implementation of the service itself.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** tables and bullet lists
- **Audience:** architect
- **Do:** Define each process as a service boundary; specify IPC channel contracts with payload and response types; document the service registry pattern with lifecycle phases; include process health monitoring strategy
- **Don't:** Describe internal class hierarchies or function signatures; specify library versions or package names; conflate service architecture with implementation code; omit failure modes and recovery strategies

**Required subsections:** Process Model (Main/Renderer/Preload), IPC Channel Design, Service Registry, Service Lifecycle, Process Health Monitoring
**Optional subsections:** Configuration Lock, Storage Domains, Service Dependency Graph
**Required diagrams:** service architecture diagram showing three processes and IPC channels
**Required cross-references:** Component Model, Communication Paths, Data Flow, Security Considerations

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
