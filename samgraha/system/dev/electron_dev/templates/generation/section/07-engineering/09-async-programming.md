# Electron Async Patterns — Generation Template

> **Domain:** engineering
> **Section:** electron_async_patterns
> **Source:** `documentation-standards/07-engineering-standards.md` §Electron Async Patterns
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Electron Async Patterns section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / desktop_service_architecture | Async patterns implement the IPC communication contracts defined in Desktop Service Architecture |
| `constrains` | feature-technical / communication_paths | Async patterns constrain how feature technical designs implement cross-process communication |
| `implements` | architecture / service_registry | Async patterns implement the service lifecycle (INIT→LOADING→COMPLETED) defined in the service registry |

## Template

```markdown
## Electron Async Patterns

### IPC Async Invoke Pattern

[1 paragraph: how Renderer process code calls Main process services via Promise-based IPC invoke — the primary request-response mechanism across process boundaries]

#### Invoke Contract

```typescript
// Renderer process — caller
const result = await window.api.[domain:action](payload)

// Preload script — bridge
ipcRenderer.invoke('[domain:action]', payload)

// Main process — handler
ipcMain.handle('[domain:action]', async (event, payload) => {
  const service = registry.resolve('[ServiceName]')
  return service.[method](payload)
})
```

#### Invoke Error Handling

| Error Category | Detection | Handler Pattern |
|---------------|-----------|----------------|
| **Service unavailable** | Main process handler not registered | Throw `ServiceError` with context; Renderer displays fallback |
| **Validation failure** | Input schema mismatch | Return structured `ValidationError`; Renderer shows field-level errors |
| **Timeout** | Promise does not resolve within [ms] | Cancel pending; show timeout error; log for diagnostics |
| **Process crash** | IPC channel destroyed | Detect via `ipcRenderer` error event; trigger recovery strategy |
| **Serialization failure** | Payload contains non-serializable types | Fail fast at call site; never send functions, Buffers, or class instances |

#### Invoke Pattern Rules

| Rule | Rationale |
|------|-----------|
| **Always await** | Every `ipcRenderer.invoke` must be awaited — never fire-and-forget invoke calls |
| **Structured errors** | Return typed error objects, not error strings — enables Renderer to categorize and display appropriately |
| **Idempotent handlers** | Main process handlers must be idempotent — retries must not create duplicate side effects |
| **Channel naming** | Follow `domain:action` convention — enables IPC audit and rate limiting |
| **Payload validation** | Main process must validate all payloads — Renderer input is untrusted |

### IPC Event-Driven Pattern

[1 paragraph: how Main process pushes state changes and system events to Renderer processes via IPC event channels — the primary broadcast mechanism]

#### Event Contract

```typescript
// Main process — emitter
function emitToRenderers(channel: string, data: unknown) {
  BrowserWindow.getAllWindows().forEach(win => {
    if (!win.isDestroyed()) {
      win.webContents.send(channel, data)
    }
  })
}

// Preload script — bridge
ipcRenderer.on('[domain:event]', (event, data) => { /* forward to handler */ })

// Renderer process — listener
window.api.on('[domain:event]', (data) => {
  // Update UI state
})
```

#### Event Pattern Rules

| Rule | Rationale |
|------|-----------|
| **Never send payloads to destroyed windows** | Guard with `win.isDestroyed()` check before every send |
| **Clean up listeners** | Renderer must remove IPC event listeners on component unmount — prevent memory leaks |
| **Event naming** | Use `domain:event` convention — distinguish from invoke channels |
| **Payload immutability** | Events must not share mutable references — serialize before send |
| **Backpressure** | Main process must not flood Renderer — batch updates or debounce high-frequency events |

### Fire-and-Forget IPC Pattern

[1 paragraph: when and how to use one-way IPC send without response — for side effects that do not require acknowledgment]

#### Send Contract

```typescript
// Renderer process — sender
window.api.[domain:command](payload)

// Preload script — bridge
ipcRenderer.send('[domain:command]', payload)

// Main process — listener
ipcMain.on('[domain:command]', (event, payload) => {
  // Perform side effect — no return
})
```

#### When to Use Fire-and-Forget

| Scenario | Pattern |
|----------|---------|
| Logging or analytics | `send` — no response needed, fire and forget |
| Window close request | `send` — Main process decides, no return value |
| Background job submission | `send` — job queued; poll or listen for completion event |
| Settings mutation | `invoke` preferred — confirmation of write success is critical |

### Background Job State Machine

[1 paragraph: how long-running operations are modeled as state machines — INIT→LOADING→COMPLETED with explicit state transitions and failure handling]

#### State Machine Definition

```
States:
  INIT        — job created, not yet started
  LOADING     — async work in progress
  COMPLETED   — work finished successfully
  FAILED      — work finished with error
  CANCELLED   — work interrupted by user or system

Transitions:
  INIT → LOADING        — start work
  LOADING → COMPLETED   — work finished
  LOADING → FAILED      — error occurred
  LOADING → CANCELLED   — user cancel or timeout
  FAILED → LOADING      — retry
  CANCELLED → INIT      — reset
```

#### Background Job Implementation

| Component | Process | Responsibility |
|-----------|---------|---------------|
| **Job Dispatcher** | Renderer | Creates job, sends to Main via IPC, displays progress |
| **Job Executor** | Main | Runs async work, reports progress events, emits completion |
| **Job Monitor** | Renderer | Listens for progress events, updates UI state machine |
| **Job Store** | Main | Persists job state, enables resume after crash/restart |

#### Job Progress Reporting

```typescript
// Main process — progress emitter
function emitJobProgress(jobId: string, state: JobState, progress?: number) {
  emitToRenderers('job:progress', { jobId, state, progress, timestamp: Date.now() })
}

// Renderer process — progress listener
window.api.on('job:progress', ({ jobId, state, progress }) => {
  updateJobState(jobId, state, progress)
})
```

### MountedRef Guard Pattern

[1 paragraph: preventing state updates on unmounted components — critical in Electron where window close can unmount components while async IPC calls are in-flight]

#### Pattern Implementation

```typescript
// In async IPC callback or event listener
useEffect(() => {
  let mounted = true

  async function fetchData() {
    const result = await window.api.[domain:action](params)
    if (mounted) {
      setData(result)
    }
  }

  fetchData()

  return () => { mounted = false }
}, [params])
```

#### Guard Rules

| Rule | Description |
|------|-------------|
| **Every async callback** | Every `.then()` or `await` continuation must check `mounted` before calling `setState` |
| **Every event listener** | Every IPC event listener must be removed in the effect cleanup function |
| **Every interval** | Every `setInterval` must be cleared on unmount |
| **Window close** | On `beforeunload`, set all mounted refs to false and cancel pending IPC calls |

### Error Handling Across Processes

[1 paragraph: how errors propagate from Main process through IPC to Renderer — typed error serialization, error boundaries, and recovery strategies]

#### Error Serialization

```typescript
// Main process — structured error
class ServiceError extends Error {
  constructor(
    public code: string,        // 'FILE_NOT_FOUND', 'VALIDATION_FAILED', etc.
    public message: string,
    public details?: unknown    // additional context
  ) { super(message) }
}

// IPC serialization
ipcMain.handle('[domain:action]', async (event, payload) => {
  try {
    return { ok: true, data: await service.execute(payload) }
  } catch (error) {
    return {
      ok: false,
      error: { code: error.code, message: error.message, details: error.details }
    }
  }
})
```

#### Error Handling Layers

| Layer | Process | Responsibility |
|-------|---------|---------------|
| **Service layer** | Main | Catch domain errors, wrap in structured `ServiceError` |
| **IPC handler layer** | Main | Catch serialization errors, convert to IPC-compatible format |
| **Bridge layer** | Preload | Ensure error objects survive IPC serialization |
| **Caller layer** | Renderer | Categorize error by code, display appropriate UI feedback |
| **Boundary layer** | Renderer | React error boundary catches unhandled rendering errors |

#### Error Recovery Strategies

| Error Type | Recovery |
|-----------|----------|
| **Transient network** | Retry with exponential backoff (max [n] attempts, base [ms]) |
| **Validation error** | Show field-level errors, do not retry |
| **Service unavailable** | Show degraded mode, queue request for retry when service recovers |
| **Serialization error** | Log and fail fast — indicates code bug, not runtime error |
| **Process crash** | Detect via IPC channel destroy, trigger full app recovery |
| **Unhandled exception** | Log to file, show user-friendly error dialog, offer restart |

### Concurrency Control

[1 paragraph: managing concurrent IPC calls — deduplication, cancellation, and ordering guarantees]

| Pattern | Implementation |
|---------|---------------|
| **Deduplication** | Cancel previous identical request before starting new one |
| **Cancellation** | Use `AbortController` where supported; for IPC, track request IDs and ignore stale responses |
| **Ordering** | Sequence ID on IPC messages; Renderer ignores responses with ID < last processed |
| **Rate limiting** | Main process throttles high-frequency channels (file watch, progress events) |
| **Batching** | Accumulate rapid changes and send batched update after [ms] debounce |

### Async Pattern Decision Matrix

| Scenario | Recommended Pattern | Alternative |
|----------|-------------------|-------------|
| Request-response | `ipcRenderer.invoke` | — |
| State broadcast | IPC event channel | — |
| Side effect | `ipcRenderer.send` | `invoke` if confirmation needed |
| Long-running work | Background job state machine | `invoke` with progress events |
| High-frequency updates | Debounced IPC events | Batched event channel |
| Component lifecycle | MountedRef guard | AbortController + cleanup |

### Async Diagram

[Sequence diagram showing Renderer→Preload→Main IPC flow with error handling, state machine transitions, and mountedRef guard points]
```

## Examples

**Correct:**
> **File Read Pattern:**
>
> Renderer calls `window.api['file:read']({ path: '/documents/report.md' })`. The Preload bridge forwards via `ipcRenderer.invoke('file:read', { path })`. Main process handler resolves the `fileSystem` service from the registry, calls `service.read(path)`, and returns `{ ok: true, data: { content: '...', stat: { size: 1024, mtime: ... } } }`. If the file does not exist, Main returns `{ ok: false, error: { code: 'FILE_NOT_FOUND', message: 'File does not exist', details: { path } } }`. Renderer checks `result.ok` and either updates the editor state or displays a file-not-found message.
>
> **MountedRef Guard:**
>
> When the user navigates away from the file editor while a file read is in-flight, the cleanup function sets `mounted = false`. When the IPC response arrives, the continuation checks `if (!mounted) return` — preventing the state update on an unmounted component. The IPC event listener for `file:changed` is removed in the same cleanup function.

**Incorrect:**
> Use `ipcRenderer.invoke` for everything. Handle errors with try/catch. Use useEffect to clean up event listeners. For long operations, show a loading spinner and await the response.
> *Why wrong: too vague and misses critical desktop-specific patterns — no mention of MountedRef guard, no structured error serialization across processes, no background job state machine, no concurrency control. Desktop async patterns require process-aware error handling that generic async patterns do not.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** code examples with tables
- **Audience:** engineer
- **Do:** Define every IPC pattern with code examples and error handling; document the MountedRef guard as mandatory for all async IPC callbacks; provide the background job state machine with explicit states and transitions; include error serialization across process boundaries
- **Don't:** Treat IPC as regular async/await — it crosses process boundaries with serialization constraints; omit error handling — every IPC call can fail in process-specific ways; skip cleanup patterns — unmounted component state updates cause silent failures; use generic JavaScript async patterns without desktop-specific adaptations

**Required subsections:** IPC Async Invoke Pattern, IPC Event-Driven Pattern, Background Job State Machine, MountedRef Guard Pattern, Error Handling Across Processes
**Optional subsections:** Fire-and-Forget IPC Pattern, Concurrency Control, Async Pattern Decision Matrix
**Required diagrams:** sequence diagram of IPC async flow with error handling
**Required cross-references:** Desktop Service Architecture (IPC channel definitions), Service Registry (service resolution), Code Standards (error class conventions)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
