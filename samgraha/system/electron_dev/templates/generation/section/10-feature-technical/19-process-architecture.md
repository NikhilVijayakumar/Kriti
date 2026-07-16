# Process Architecture Implementation — Generation Template

> **Domain:** feature-technical
> **Section:** process_architecture
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Process Architecture
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Process Architecture Implementation section for a Feature Technical Design document.

## Relationships

This relationship has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / system_overview | Process architecture must be consistent with the system-level process model |
| `derives_from` | security / process_isolation | Process boundaries must respect security isolation requirements |
| `derives_from` | feature-technical / ipc_implementation | Process communication must use defined IPC channel patterns |

## Template

```markdown
## Process Architecture Implementation

### Process Model

| Process | Entry Point | Responsibility | Lifetime |
|---------|------------|----------------|----------|
| Main | `src/main/index.ts` | Service orchestration, window management, native APIs | Application lifetime |
| Renderer | `src/renderer/index.tsx` | UI rendering, user interaction, local state | Per-window, tied to window lifecycle |
| Preload | `src/preload/index.ts` | Bridge API definition, IPC surface | Per-window, injected before renderer |

### Main Process Services

```typescript
// Service initialization order — dependency-aware
export async function initializeMainServices(): Promise<void> {
  // Tier 1: No dependencies
  const logger = LoggerService.getInstance();        // Always first
  const config = ConfigurationService.getInstance();  // Immutable post-init
  const storage = StorageService.getInstance();       // Local/Vault/Document domains

  // Tier 2: Depends on Tier 1
  const vault = VaultService.getInstance();           // Requires config + storage
  const indexer = IndexerService.getInstance();        // Requires storage
  const workspace = WorkspaceService.getInstance();    // Requires config + storage

  // Tier 3: Depends on Tier 1 + 2
  const sync = SyncService.getInstance();              // Requires vault + workspace
  const search = SearchService.getInstance();          // Requires indexer
  const updater = UpdaterService.getInstance();        // Requires config

  // Health check after all services initialized
  await performHealthCheck({ logger, config, storage, vault, indexer, workspace, sync, search, updater });
}
```

### Renderer Process Components

```typescript
// Renderer bootstrap — window-scoped
export function bootstrapRenderer(): void {
  const store = createAppStore();                      // Zustand/Redux, per-window
  const router = createRouter(store);                  // Window-scoped route tree
  const electronAPI = window.electronAPI;              // From contextBridge

  // Subscribe to main-process events
  const unsubscribers = [
    electronAPI.documents.onSyncChange(handleSync),
    electronAPI.vault.onLockChange(handleVaultLock),
    electronAPI.settings.onConfigChange(handleConfigUpdate),
  ];

  // Render
  const root = createRoot(document.getElementById('app'));
  root.render(<App store={store} router={router} />);

  // Cleanup on window close
  window.addEventListener('beforeunload', () => {
    unsubscribers.forEach(fn => fn());
    store.destroy();
  });
}
```

### Preload Script — contextBridge API Surface

```typescript
// preload.ts — runs in isolated context before renderer
import { contextBridge, ipcRenderer } from 'electron';

const api = {
  // Domain-organized API surface — one namespace per domain
  documents: createDocumentsAPI(ipcRenderer),
  vault: createVaultAPI(ipcRenderer),
  settings: createSettingsAPI(ipcRenderer),
  window: createWindowAPI(ipcRenderer),
  workspace: createWorkspaceAPI(ipcRenderer),
  updater: createUpdaterAPI(ipcRenderer),
};

// Expose once, typed, immutable
contextBridge.exposeInMainWorld('electronAPI', Object.freeze(api));

// Factory pattern for each domain
function createDocumentsAPI(ipc: typeof ipcRenderer) {
  return {
    save: (payload: DocumentsSaveRequest) =>
      ipc.invoke('documents:save:request', payload),
    delete: (payload: DocumentsDeleteRequest) =>
      ipc.invoke('documents:delete:request', payload),
    list: () => ipc.invoke('documents:list:request'),
    onSyncChange: (handler: (payload: SyncEvent) => void) => {
      const wrapped = (_event: IpcRendererEvent, data: SyncEvent) => handler(data);
      ipc.on('documents:sync:event', wrapped);
      return () => ipc.removeListener('documents:sync:event', wrapped);
    },
  };
}
```

### Process Communication Wiring

| From | To | Mechanism | Channel Pattern | Data Flow |
|------|----|-----------|----------------|-----------|
| Renderer → Main | Renderer | invoke/send | `domain:action:request` / `domain:action:notify` | User action triggers IPC call |
| Main → Renderer | Main | webContents.send | `domain:action:event` | Background service emits event |
| Main → All Renderers | Main | webContents.getAllWebContents().send | `domain:action:broadcast` | Global state change |
| Preload ↔ Renderer | Exposed API | Direct function call | N/A | Typed API surface via contextBridge |

### Service Registry — Singleton Factory Pattern

```typescript
export class ServiceRegistry {
  private static instances = new Map<string, Service>();
  private static factories = new Map<string, () => Service>();
  private static locked = false;  // Configuration lock — immutable post-operational

  static register<T extends Service>(name: string, factory: () => T): void {
    if (this.locked) throw new Error('Registry locked — cannot register after initialization');
    this.factories.set(name, factory);
  }

  static get<T extends Service>(name: string): T {
    let instance = this.instances.get(name) as T | undefined;
    if (!instance) {
      const factory = this.factories.get(name);
      if (!factory) throw new Error(`Service ${name} not registered`);
      instance = factory() as T;
      this.instances.set(name, instance);
      instance.onInit?.();
    }
    return instance;
  }

  static lock(): void {
    this.locked = true;
  }
}

// Usage
ServiceRegistry.register('vault', () => new VaultService());
ServiceRegistry.lock();  // After bootstrap, config is immutable
```

### Process Health Checks

```typescript
export async function performHealthCheck(services: ServiceMap): Promise<HealthReport> {
  const checks = await Promise.allSettled(
    Object.entries(services).map(async ([name, service]) => ({
      name,
      status: await service.ping?.() ?? true,
      latency: 0,  // measured per check
    }))
  );

  return {
    healthy: checks.every(c => c.status === 'fulfilled' && c.value.status),
    services: checks.map(c =>
      c.status === 'fulfilled' ? c.value : { name: 'unknown', status: false }
    ),
    timestamp: Date.now(),
  };
}
```

### Process Lifecycle State Machine

```text
INIT → LOADING → READY → ACTIVE → SUSPENDED → RESUMED → TERMINATING → TERMINATED
       ↑         ↓         ↓
     RETRY    RECOVER  REINIT
```

## Examples

**Correct:**
> Main process initializes services in dependency order: Logger → Config → Storage → Vault → Indexer → Sync → Search. Configuration lock activates after bootstrap — no service can register after `ServiceRegistry.lock()`. Preload exposes typed namespaces per domain via `contextBridge.exposeInMainWorld`. Renderer consumes `window.electronAPI.documents.save()` which delegates to `ipcRenderer.invoke('documents:save:request')`. Process health checks run on a 30-second interval; unhealthy services trigger recovery workflow with exponential backoff.

**Incorrect:**
> The renderer communicates with the main process through IPC. The preload script exposes APIs. Services are initialized in order.
> *Why wrong: no explicit service dependency tiers, no configuration lock mechanism, no contextBridge API surface definition, no health check strategy, no lifecycle state machine.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables + code blocks
- **Audience:** architect
- **Do:** Define explicit process model with entry points and lifetimes; document service initialization order with dependency tiers; provide contextBridge API surface organized by domain; wire process communication with channel patterns; include configuration lock mechanism; document health check and lifecycle state machine
- **Don't:** Omit service initialization order; skip contextBridge API surface; leave process communication unwired; forget lifecycle states

**Minimum content:** process model table + service initialization code + preload API + communication wiring table
**Length guidance:** detailed
**Required diagrams:** process architecture diagram showing process boundaries and communication paths
**Required cross-references:** IPC Implementation(18), Component Interactions(03), Communication Paths(08), QA Process Testing(11)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
