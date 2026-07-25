# IPC Testing Strategy — Generation Template

> **Domain:** qa
> **Section:** ipc_testing
> **Source:** `documentation-standards/12-qa-standards.md` §IPC Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the IPC Testing Strategy section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | features-technical / ipc_implementation | IPC tests must cover every defined IPC channel |
| `derives_from` | security / channel_security | IPC tests must verify security boundaries and channel isolation |
| `derives_from` | qa / test_strategy | IPC test types must align with the overall test strategy |

## Template

```markdown
## IPC Testing Strategy

### IPC Channel Test Coverage

| Channel | Priority | Unit Test | Integration Test | Error Test | Security Test |
|---------|----------|-----------|-----------------|------------|--------------|
| `[domain:action:request]` | Critical | Handler logic | Cross-process flow | Invalid payloads | Unauthorized access |
| `[domain:action:notify]` | High | Handler logic | — | — | Channel spoofing |
| `[domain:action:event]` | High | Event emission | Delivery to renderer | Timeout | — |
| `[domain:action:broadcast]` | Medium | — | Multi-window delivery | — | — |

### Mock IPC Transport Layer

```typescript
// test-utils/ipc-transport-mock.ts
import { z } from 'zod';
import type { ChannelMap } from '../src/ipc/channels';

type HandlerEntry = {
  handler: (event: MockIpcEvent, payload: unknown) => unknown;
  schema: z.ZodSchema;
};

type MockIpcEvent = {
  senderFrame: { id: number };
  processId: number;
};

export function createMockIpcTransport() {
  const handlers = new Map<string, HandlerEntry>();
  const eventListeners = new Map<string, Set<(payload: unknown) => void>>();

  return {
    // Simulate Main process handler registration
    registerHandler: <C extends keyof ChannelMap>(
      channel: C,
      schema: z.ZodSchema<ChannelMap[C]['request']>,
      handler: (event: MockIpcEvent, payload: ChannelMap[C]['request']) =>
        Promise<ChannelMap[C]['response']>
    ) => {
      handlers.set(channel as string, { handler, schema });
    },

    // Simulate Renderer invoking a handler
    invoke: async <C extends keyof ChannelMap>(
      channel: C,
      payload: ChannelMap[C]['request']
    ): Promise<ChannelMap[C]['response']> => {
      const entry = handlers.get(channel as string);
      if (!entry) throw new Error(`No handler registered for channel: ${channel}`);
      const validated = entry.schema.parse(payload);
      return entry.handler(
        { senderFrame: { id: 1 }, processId: 2 },
        validated
      ) as Promise<ChannelMap[C]['response']>;
    },

    // Simulate Main sending event to Renderer
    simulateEvent: <C extends keyof ChannelMap>(
      channel: C,
      payload: ChannelMap[C]['response']
    ) => {
      const listeners = eventListeners.get(channel as string);
      if (listeners) listeners.forEach(fn => fn(payload));
    },

    // Simulate Renderer listening for events
    onEvent: <C extends keyof ChannelMap>(
      channel: C,
      handler: (payload: ChannelMap[C]['response']) => void
    ): (() => void) => {
      if (!eventListeners.has(channel as string)) {
        eventListeners.set(channel as string, new Set());
      }
      eventListeners.get(channel as string)!.add(handler);
      return () => eventListeners.get(channel as string)!.delete(handler);
    },

    // Simulate Renderer sending fire-and-forget
    send: <C extends keyof ChannelMap>(
      channel: C,
      payload: ChannelMap[C]['request']
    ): void => {
      const entry = handlers.get(channel as string);
      if (entry) entry.handler(
        { senderFrame: { id: 1 }, processId: 2 },
        entry.schema.parse(payload)
      );
    },

    reset: () => {
      handlers.clear();
      eventListeners.clear();
    },

    getRegisteredChannels: (): string[] => [...handlers.keys()],
    getListenerCount: (channel: string): number =>
      eventListeners.get(channel)?.size ?? 0,
  };
}
```

### Handler Unit Tests

```typescript
// documents:save:request handler tests
describe('documents:save:request IPC handler', () => {
  const ipc = createMockIpcTransport();
  const mockDocumentService = { save: jest.fn() };

  beforeEach(() => {
    ipc.reset();
    registerDocumentsHandlers(ipc as any, mockDocumentService);
  });

  it('returns revision on successful save', async () => {
    mockDocumentService.save.mockResolvedValue({ version: 3 });
    const result = await ipc.invoke('documents:save:request', {
      id: 'doc-1',
      content: '# Hello',
      format: 'md',
    });
    expect(result).toEqual({ revision: 3, timestamp: expect.any(Number) });
  });

  it('rejects with VALIDATION error for missing fields', async () => {
    await expect(
      ipc.invoke('documents:save:request', { id: 'doc-1' } as any)
    ).rejects.toMatchObject({ code: 'VALIDATION' });
  });

  it('rejects with LOCKED error when document is in use', async () => {
    mockDocumentService.save.mockRejectedValue(new DocumentLockError('doc-1'));
    await expect(
      ipc.invoke('documents:save:request', { id: 'doc-1', content: 'x', format: 'md' })
    ).rejects.toMatchObject({ code: 'LOCKED' });
  });
});
```

### Cross-Process Integration Tests

```typescript
// Full integration: Renderer invokes → Main handles → event emitted back
describe('document sync integration', () => {
  const ipc = createMockIpcTransport();
  const syncEvents: SyncEventPayload[] = [];

  beforeAll(async () => {
    // Bootstrap full service chain on mock transport
    await initializeServices(ipc as any);
    ipc.onEvent('documents:sync:event', (payload) => {
      syncEvents.push(payload);
    });
  });

  it('emits sync event after document save', async () => {
    await ipc.invoke('documents:save:request', {
      id: 'doc-1', content: 'update', format: 'md',
    });
    expect(syncEvents.length).toBe(1);
    expect(syncEvents[0].changedIds).toContain('doc-1');
  });

  it('does not emit event on failed save', async () => {
    syncEvents.length = 0;
    await expect(
      ipc.invoke('documents:save:request', { id: 'locked-doc', content: 'x', format: 'md' })
    ).rejects.toBeDefined();
    expect(syncEvents.length).toBe(0);
  });
});
```

### IPC Error Testing

| Error Scenario | Channel | Expected Behavior | Assertion |
|----------------|---------|-------------------|-----------|
| Invalid payload schema | invoke channels | Reject with `VALIDATION` + field path | `toMatchObject({ code: 'VALIDATION' })` |
| Service throws | invoke channels | Reject with typed error code | `toMatchObject({ code: 'SERVICE_ERROR' })` |
| Handler timeout | invoke channels | Reject with `TIMEOUT` after 30s | `toMatchObject({ code: 'TIMEOUT' })` |
| Unregistered channel | invoke channels | Reject with channel error | `toThrow('No handler registered')` |
| Renderer disconnected | event channels | Queue or drop event | `expect(sent).toBe(false)` |

### Channel Isolation Tests

```typescript
describe('IPC channel isolation', () => {
  const ipc = createMockIpcTransport();

  it('does not allow invoke on send-only channels', async () => {
    ipc.registerHandler('indexing:complete:notify', ...);
    await expect(
      ipc.invoke('indexing:complete:notify', { jobId: '1', duration: 100 })
    ).rejects.toThrow('Not an invoke channel');
  });

  it('prevents event listener on request channels', () => {
    expect(() =>
      ipc.onEvent('documents:save:request', () => {})
    ).toThrow('Not an event channel');
  });

  it('isolates handler state per channel', () => {
    ipc.registerHandler('documents:save:request', ...);
    ipc.registerHandler('documents:delete:request', ...);
    // Deleting one should not affect the other
    handlers.delete('documents:save:request');
    expect(ipc.getRegisteredChannels()).not.toContain('documents:save:request');
    expect(ipc.getRegisteredChannels()).toContain('documents:delete:request');
  });
});
```

### Test Fixture — Preload API Mock

```typescript
// test-utils/mock-electron-api.ts
export function createMockElectronAPI(): ElectronAPI {
  const ipc = createMockIpcTransport();
  return {
    documents: {
      save: (p) => ipc.invoke('documents:save:request', p),
      delete: (p) => ipc.invoke('documents:delete:request', p),
      onSyncChange: (h) => ipc.onEvent('documents:sync:event', h),
    },
    vault: {
      read: (p) => ipc.invoke('vault:read:request', p),
      write: (p) => ipc.invoke('vault:write:request', p),
    },
    // wire remaining domains...
  };
}
```

## Examples

**Correct:**
> IPC testing uses a `createMockIpcTransport` that simulates both invoke/send (Renderer→Main) and event (Main→Renderer) patterns without Electron runtime. Every channel in the channel map has corresponding unit tests for handler logic, payload validation, and error propagation. Integration tests verify cross-process flows — e.g., document save triggers sync event. Channel isolation tests ensure channels cannot be invoked on wrong pattern types. The mock transport exposes `getRegisteredChannels` and `getListenerCount` for introspection.

**Incorrect:**
> We test IPC by actually starting Electron and calling `ipcRenderer.invoke` in integration tests.
> *Why wrong: IPC tests should use a mock transport layer to avoid Electron runtime dependency, enable fast unit tests, and allow deterministic error simulation. Tests must cover error propagation, channel isolation, and the full type-safety contract.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables + code blocks
- **Audience:** engineer
- **Do:** Provide mock IPC transport as test utility; test every channel defined in IPC Implementation(18); include handler unit tests, error propagation tests, channel isolation tests; provide preload API mock fixture; document error scenarios table
- **Don't:** Require Electron runtime for unit tests; skip channel isolation tests; omit error scenario coverage; test without type-safe mock transport

**Required subsections:** IPC Channel Test Coverage table, Mock Transport code, Handler Unit Tests, Error Testing, Channel Isolation Tests
**Optional subsections:** Integration Tests, Preload API Mock fixture
**Required diagrams:** none
**Required cross-references:** IPC Implementation(18), Process Architecture(19), Process Testing(11)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
