# Process Testing Strategy — Generation Template

> **Domain:** qa
> **Section:** process_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Process Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Process Testing Strategy section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / process_architecture | Process tests must cover every process type defined in Process Architecture |
| `derives_from` | qa / test_strategy | Process test types must align with the overall test strategy |
| `derives_from` | qa / ipc_testing | Process communication tests must complement IPC channel tests |

## Template

```markdown
## Process Testing Strategy

### Process Isolation Tests

| Test Scope | Target Process | Verification | Isolation Mechanism |
|------------|---------------|-------------|-------------------|
| Service lifecycle | Main | Init → Ready → Terminate sequence | Mock service registry, isolate each service |
| UI rendering | Renderer | Component mount, interaction, unmount | jsdom + React Testing Library |
| Bridge surface | Preload | contextBridge API shape, type correctness | Preload script in isolated Node.js context |
| Crash recovery | Main | Service crash → detect → restart → health check | Process crash mock, recovery handler test |

### Service Lifecycle Testing

```typescript
// test-utils/service-lifecycle-mock.ts
export function createMockServiceLifecycle() {
  const states = new Map<string, ServiceState>();
  const initOrder: string[] = [];

  return {
    registerService: (name: string, factory: () => MockService) => {
      ServiceRegistry.register(name, factory);
    },

    initialize: async (services: string[]) => {
      for (const name of services) {
        const svc = ServiceRegistry.get<MockService>(name);
        svc.onInit?.();
        states.set(name, 'INIT');
        initOrder.push(name);
        await svc.onReady?.();
        states.set(name, 'READY');
      }
      ServiceRegistry.lock();
    },

    crashService: async (name: string) => {
      const svc = ServiceRegistry.get<MockService>(name);
      states.set(name, 'CRASHED');
      await svc.onCrash?.();
    },

    recoverService: async (name: string) => {
      const svc = ServiceRegistry.get<MockService>(name);
      await svc.onRecover?.();
      states.set(name, 'RECOVERED');
    },

    getState: (name: string) => states.get(name),
    getInitOrder: () => [...initOrder],
    isLocked: () => (ServiceRegistry as any).locked === true,
    reset: () => {
      states.clear();
      initOrder.length = 0;
      ServiceRegistry.reset();
    },
  };
}
```

#### Service Lifecycle Unit Tests

```typescript
describe('Main process service lifecycle', () => {
  const lifecycle = createMockServiceLifecycle();

  beforeEach(() => {
    lifecycle.reset();
    // Register services with dependency order
    lifecycle.registerService('logger', () => new MockLogger());
    lifecycle.registerService('config', () => new MockConfig());
    lifecycle.registerService('storage', () => new MockStorage());
  });

  it('initializes services in correct dependency order', async () => {
    await lifecycle.initialize(['logger', 'config', 'storage']);
    expect(lifecycle.getInitOrder()).toEqual(['logger', 'config', 'storage']);
  });

  it('locks service registry after initialization', async () => {
    await lifecycle.initialize(['logger', 'config']);
    expect(lifecycle.isLocked()).toBe(true);
  });

  it('prevents registration after lock', async () => {
    await lifecycle.initialize(['logger']);
    ServiceRegistry.register('vault', () => new MockVault());
    expect(() => ServiceRegistry.get('vault')).toThrow('Registry locked');
  });

  it('tracks INIT → READY state transitions', async () => {
    await lifecycle.initialize(['logger']);
    expect(lifecycle.getState('logger')).toBe('READY');
  });

  it('handles service crash and recovery', async () => {
    await lifecycle.initialize(['logger', 'config']);
    await lifecycle.crashService('config');
    expect(lifecycle.getState('config')).toBe('CRASHED');
    await lifecycle.recoverService('config');
    expect(lifecycle.getState('config')).toBe('RECOVERED');
  });
});
```

### Process Crash Recovery Tests

```typescript
describe('process crash recovery', () => {
  const lifecycle = createMockServiceLifecycle();

  it('detects crashed service via health check', async () => {
    await lifecycle.initialize(['logger', 'storage']);
    await lifecycle.crashService('storage');
    const health = await performHealthCheck();
    expect(health.services.find(s => s.name === 'storage')?.status).toBe(false);
    expect(health.healthy).toBe(false);
  });

  it('re-initializes service with exponential backoff', async () => {
    await lifecycle.initialize(['logger', 'storage']);
    await lifecycle.crashService('storage');
    const recovery = await attemptRecovery('storage', {
      maxRetries: 3,
      baseDelay: 100,
      strategy: 'exponential',
    });
    expect(recovery.success).toBe(true);
    expect(recovery.attempts).toBeLessThanOrEqual(3);
    expect(recovery.backoffDelays).toEqual([100, 200, 400]);
  });

  it('escalates to user notification after max retries', async () => {
    await lifecycle.initialize(['logger', 'config']);
    await lifecycle.crashService('config');
    const recovery = await attemptRecovery('config', {
      maxRetries: 2,
      baseDelay: 10,
      strategy: 'exponential',
    });
    expect(recovery.success).toBe(false);
    expect(recovery.escalated).toBe(true);
  });

  it('preserves state of healthy services during crash of another', async () => {
    await lifecycle.initialize(['logger', 'storage']);
    await lifecycle.crashService('storage');
    expect(lifecycle.getState('logger')).toBe('READY');
  });
});
```

### Preload Script Testing

```typescript
// preload.spec.ts — test contextBridge API shape without Electron
describe('preload API surface', () => {
  let api: ReturnType<typeof createPreloadAPI>;

  beforeEach(() => {
    // Create preload API using mock ipcRenderer
    const mockIpcRenderer = createMockIpcRenderer();
    api = createPreloadAPI(mockIpcRenderer);
  });

  it('exposes documents namespace with correct methods', () => {
    expect(api.documents).toBeDefined();
    expect(typeof api.documents.save).toBe('function');
    expect(typeof api.documents.delete).toBe('function');
    expect(typeof api.documents.onSyncChange).toBe('function');
  });

  it('exposes vault namespace with read and write', () => {
    expect(api.vault).toBeDefined();
    expect(typeof api.vault.read).toBe('function');
    expect(typeof api.vault.write).toBe('function');
  });

  it('returns unsubscribe function from event listeners', () => {
    const unsubscribe = api.documents.onSyncChange(() => {});
    expect(typeof unsubscribe).toBe('function');
    unsubscribe();
    // Verify listener was removed
    expect(api.getListenerCount?.('documents:sync:event')).toBe(0);
  });

  it('preserves immutability of exposed API', () => {
    expect(() => { (api as any).documents = {}; }).toThrow();
    expect(() => { (api as any).newProp = 'test'; }).toThrow();
  });
});
```

### Renderer Process Testing

```typescript
// renderer.spec.ts — component tests with mocked preload API
describe('Renderer process integration', () => {
  beforeEach(() => {
    // Inject mock electronAPI into window
    (window as any).electronAPI = createMockElectronAPI();
  });

  it('renders application shell', () => {
    render(<App />);
    expect(screen.getByTestId('app-shell')).toBeInTheDocument();
  });

  it('invokes document save on form submit', async () => {
    render(<DocumentEditor documentId="doc-1" />);
    fireEvent.click(screen.getByText('Save'));
    await waitFor(() => {
      expect(window.electronAPI.documents.save).toHaveBeenCalledWith({
        id: 'doc-1', content: expect.any(String), format: 'md',
      });
    });
  });

  it('responds to main-process sync events', () => {
    render(<DocumentList />);
    window.electronAPI.documents.onSyncChange.mock.calls[0][0]({
      changedIds: ['doc-2'],
      syncStatus: 'completed',
    });
    expect(screen.getByText('doc-2')).toBeInTheDocument();
  });
});
```

### Process Communication Integration Tests

| Test Scenario | Sender | Receiver | Mechanism | Verification |
|---------------|--------|----------|-----------|--------------|
| User saves document | Renderer | Main | invoke | Handler receives correct payload, returns result |
| Background sync completes | Main | Renderer | webContents.send | Renderer receives event, updates UI |
| Vault lock changes | Main | All Renderers | broadcast | All windows receive event |
| Application quit signal | Main | Renderer | webContents.send | Renderer shows confirmation dialog |
| Service initialized | Main | Preload | — | contextBridge API ready before renderer mounts |

### Process Health Check Tests

```typescript
describe('process health checks', () => {
  it('reports all services healthy when ping succeeds', async () => {
    const report = await performHealthCheck({
      logger: { ping: () => Promise.resolve(true) },
      storage: { ping: () => Promise.resolve(true) },
    });
    expect(report.healthy).toBe(true);
    expect(report.services.every(s => s.status)).toBe(true);
  });

  it('reports unhealthy when any service ping fails', async () => {
    const report = await performHealthCheck({
      logger: { ping: () => Promise.resolve(true) },
      storage: { ping: () => Promise.reject(new Error('Storage down')) },
    });
    expect(report.healthy).toBe(false);
    expect(report.services.find(s => s.name === 'storage')?.status).toBe(false);
  });

  it('handles ping timeout gracefully', async () => {
    const report = await performHealthCheck({
      logger: { ping: () => new Promise(resolve => setTimeout(resolve, 5000)) },
    }, { timeout: 1000 });
    expect(report.services.find(s => s.name === 'logger')?.status).toBe(false);
  });
});
```

## Examples

**Correct:**
> Process testing covers three process types independently. Main process tests use `createMockServiceLifecycle` to verify service initialization order, state transitions (INIT→LOADING→READY→CRASHED→RECOVERED), and configuration lock enforcement. Renderer tests inject a mock `window.electronAPI` and test components against it without Electron. Preload tests run in isolation to verify the contextBridge API surface shape, type correctness, and immutability. Crash recovery tests verify exponential backoff, service isolation (healthy services unaffected), and escalation after max retries. Process communication tests at the integration level verify invoke/send/event/broadcast patterns between processes.

**Incorrect:**
> We test processes by starting the full Electron application and clicking through the UI. If a process crashes, we see it in the logs.
> *Why wrong: process testing requires isolation per process type (Main/Renderer/Preload), testable lifecycle state machines, crash recovery verification with backoff assertions, and health check testing with controlled ping responses.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables + code blocks
- **Audience:** engineer
- **Do:** Test each process type in isolation (Main/Renderer/Preload); provide mock lifecycle harness for service init/state/recovery; verify crash recovery with backoff assertions; test contextBridge API shape and immutability; test process health checks with controlled ping responses; verify process communication integration
- **Don't:** Require full Electron startup for process tests; skip crash recovery scenarios; test process communication without isolation mocks; omit health check verification

**Required subsections:** Process Isolation Tests table, Service Lifecycle Tests, Crash Recovery Tests, Preload API Tests, Process Communication Integration table
**Optional subsections:** Renderer Process Tests, Health Check Tests
**Required diagrams:** none
**Required cross-references:** Process Architecture(19), IPC Testing(10), Service Registry pattern

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
