# IPC Channel Implementation — Generation Template

> **Domain:** feature-technical
> **Section:** ipc_implementation
> **Source:** `documentation-standards/10-feature-technical-standards.md` §IPC Implementation
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the IPC Channel Implementation section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / process_architecture | IPC patterns must use the process architecture's communication model |
| `derives_from` | feature-technical / component_interactions | Each IPC channel must trace to a defined Component Interaction |
| `derives_from` | security / channel_security | IPC channel definitions must respect security boundaries |

## Template

```markdown
## IPC Channel Implementation

### Channel Naming Convention

| Pattern | Format | Example |
|---------|--------|---------|
| Invoke (request/response) | `[domain]:[action]:request` | `documents:save:request` |
| Send (fire-and-forget) | `[domain]:[action]:notify` | `indexing:complete:notify` |
| Receive (main-to-renderer) | `[domain]:[action]:event` | `sync:status-change:event` |
| Broadcast (all windows) | `[domain]:[action]:broadcast` | `update:available:broadcast` |

**Domain prefixes:** `app`, `documents`, `sync`, `indexing`, `search`, `vault`, `settings`, `updater`, `window`, `workspace`

### Channel Definitions

| Channel | Direction | Pattern | Payload Type | Error Type |
|---------|-----------|---------|-------------|-----------|
| `[domain:action:request]` | Renderer → Main | invoke | `[RequestPayload]` | `[ErrorResponse]` |
| `[domain:action:notify]` | Renderer → Main | send | `[NotificationPayload]` | — |
| `[domain:action:event]` | Main → Renderer | receive | `[EventPayload]` | — |
| `[domain:action:broadcast]` | Main → All Renderers | broadcast | `[BroadcastPayload]` | — |

### Handler Implementation

```typescript
// Main process handler registration
import { ipcMain } from 'electron';
import { registerHandler, invokeChannel, sendChannel } from './ipc/registry';

// Type-safe channel definition
export const DOCUMENTS_SAVE_CHANNEL = 'documents:save:request' as const;
type DocumentsSaveRequest = { id: string; content: string; format: 'md' | 'json' };
type DocumentsSaveResponse = { revision: number; timestamp: number };

// Handler with validation and error propagation
registerHandler<DocumentsSaveRequest, DocumentsSaveResponse>(
  DOCUMENTS_SAVE_CHANNEL,
  {
    schema: documentsSaveSchema,      // Zod/JSON schema validation
    handler: async (event, payload) => {
      // event.senderFrame for sender identity
      const result = await documentService.save(payload.id, payload.content);
      return { revision: result.version, timestamp: Date.now() };
    },
    errorPolicy: 'propagate',         // propagate | swallow | fallback
    timeout: 30_000,                  // ms
  }
);
```

### Type Definitions

```typescript
// Channel descriptor — one file per domain
export interface ChannelMap {
  'documents:save:request': {
    request: { id: string; content: string };
    response: { revision: number; timestamp: number };
    error: { code: 'LOCKED' | 'NOT_FOUND' | 'VALIDATION'; message: string };
  };
  'documents:delete:request': {
    request: { id: string; permanent: boolean };
    response: { success: boolean };
    error: { code: 'LOCKED' | 'NOT_FOUND'; message: string };
  };
  // ...
}

// Type-safe invoke wrapper
type TypedIpc = {
  invoke<C extends keyof ChannelMap>(
    channel: C,
    payload: ChannelMap[C]['request']
  ): Promise<ChannelMap[C]['response']>;

  send<C extends keyof ChannelMap>(
    channel: C extends `${string}:notify` ? C : never,
    payload: ChannelMap[C]['request']
  ): void;

  on<C extends keyof ChannelMap>(
    channel: C extends `${string}:event` ? C : never,
    handler: (payload: ChannelMap[C]['response']) => void
  ): () => void; // returns unsubscribe
};
```

### Error Propagation Strategy

| Error Category | Channel Behavior | Renderer Experience |
|----------------|-----------------|---------------------|
| Validation | Reject with typed error code | Show field-level validation |
| Service | Reject with error code + retry hint | Show retry dialog or toast |
| Timeout | Reject with `TIMEOUT` (30s default) | Show timeout message |
| Crash | Channel handler crash caught; logged; fallback response | Show graceful error state |

### Preload API Surface

```typescript
// preload.ts — exposed via contextBridge
contextBridge.exposeInMainWorld('electronAPI', {
  documents: {
    save: (payload) => ipcRenderer.invoke('documents:save:request', payload),
    delete: (payload) => ipcRenderer.invoke('documents:delete:request', payload),
    onSyncChange: (handler) => {
      const cb = (_event, payload) => handler(payload);
      ipcRenderer.on('documents:sync:event', cb);
      return () => ipcRenderer.removeListener('documents:sync:event', cb);
    },
  },
  vault: {
    read: (payload) => ipcRenderer.invoke('vault:read:request', payload),
    write: (payload) => ipcRenderer.invoke('vault:write:request', payload),
  },
});
```

### IPC Testing Hooks

```typescript
// Test injector for Main process handlers
export function createTestIpcTransport() {
  const handlers = new Map<string, { handler: Function; schema: AnySchema }>();

  return {
    registerHandler: (channel, config) => handlers.set(channel, config),
    invoke: async (channel, payload) => {
      const entry = handlers.get(channel);
      if (!entry) throw new Error(`No handler for ${channel}`);
      const validated = entry.schema.parse(payload);
      return entry.handler({ senderFrame: { id: 1 } }, validated);
    },
    reset: () => handlers.clear(),
    getRegisteredChannels: () => [...handlers.keys()],
  };
}

// Usage
const ipc = createTestIpcTransport();
ipc.registerHandler('documents:save:request', { ... });
const result = await ipc.invoke('documents:save:request', validPayload);
```

## Examples

**Correct:**
> | Channel | Direction | Pattern | Payload Type | Error Type |
> |---------|-----------|---------|-------------|-----------|
> | `documents:save:request` | Renderer → Main | invoke | `{ id, content, format }` | `{ code: 'LOCKED' \| 'NOT_FOUND' \| 'VALIDATION', message }` |
> | `documents:sync:event` | Main → Renderer | receive | `{ changedIds[], syncStatus }` | — |
> | `indexing:complete:notify` | Renderer → Main | send | `{ jobId, duration }` | — |
>
> Handler implementation uses `registerHandler` with Zod schema validation. Errors propagate as typed responses with `errorPolicy: 'propagate'`. The `documents:save:request` handler validates the payload, acquires a document lock via the service registry's singleton factory, and returns the new revision number.

**Incorrect:**
> We use IPC to communicate between main and renderer. The renderer calls `ipcRenderer.invoke('save', data)` and the main process handles it with `ipcMain.handle('save', handler)`.
> *Why wrong: no channel naming convention, no type definitions, no error propagation strategy, no preload API surface, no testing hooks.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables + code blocks
- **Audience:** engineer
- **Do:** Define channel naming convention with domain:action:pattern; provide explicit type definitions per channel; document handler registration, error handling, and timeout strategy; include preload API surface; provide test injector patterns
- **Don't:** Use generic channel names without domain prefixes; omit type safety for invoke/send/receive; skip error propagation strategy; forget testing hooks

**Minimum content:** channel naming convention table + channel definitions table + handler implementation snippet + preload API
**Length guidance:** detailed
**Required diagrams:** none
**Required cross-references:** Process Architecture(19), Component Interactions(03), Communication Paths(08), QA IPC Testing(10)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
