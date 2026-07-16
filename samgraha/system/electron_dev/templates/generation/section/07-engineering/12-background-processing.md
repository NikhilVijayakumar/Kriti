# Background Processing — Generation Template

> **Domain:** engineering
> **Section:** background_processing
> **Source:** `documentation-standards/07-engineering-standards.md` §Background Processing
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Background Processing section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `uses` | architecture / process_isolation | Background jobs execute in Main process or dedicated workers — never in Renderer |
| `communicates_via` | architecture / ipc_pattern | Job progress and results flow through IPC channels |
| `governed_by` | engineering / caching | Job results may be cached per storage domain rules |
| `persists_via` | architecture / storage_domains | Job state persisted to Document or Local domain |

## Template

```markdown
## Background Processing

> [metadata block]

[1 paragraph: overall approach — background jobs handle long-running work off the UI thread, communicate via IPC, persist state for crash recovery]

### Job State Machine

> **Generation note:** Every background job follows a deterministic state machine. States are: `INIT → LOADING → PROCESSING → COMPLETED | FAILED`. No implicit states.

```
Job State Machine:

  ┌──────┐    start     ┌─────────┐    data ready   ┌────────────┐
  │ INIT │──────────────▶│ LOADING │────────────────▶│ PROCESSING │
  └──────┘               └─────────┘                 └────────────┘
                             │                            │
                             │ error                      │ done
                             ▼                            ▼
                        ┌─────────┐                ┌───────────┐
                        │ FAILED  │                │ COMPLETED │
                        └─────────┘                └───────────┘

  Additional transitions:
    LOADING → CANCELLED    (user cancels during load)
    PROCESSING → CANCELLED (user cancels during processing)
    FAILED → RETRY         (retry policy allows re-attempt)
    COMPLETED → STALE      (result invalidated by external change)
```

> **State definitions:**
> - `INIT`: Job created, not yet started. Awaiting resource allocation or user trigger.
> - `LOADING`: Fetching input data (reading files, querying API, loading config). I/O bound.
> - `PROCESSING`: Executing core logic (parsing, transforming, generating). CPU bound.
> - `COMPLETED`: Job finished successfully. Result available for retrieval.
> - `FAILED`: Job failed with error. Error details recorded. May be retryable.
> - `CANCELLED`: User-initiated cancellation. Cleanup performed, resources released.
> - `STALE`: Result invalidated by external change. May need re-processing.

### Job Manager

> **Generation note:** Central job manager coordinates all background work. Single instance in Main process.

```typescript
interface Job<TInput, TOutput> {
  id: string;
  type: string;
  state: JobState;
  input: TInput;
  result?: TOutput;
  error?: JobError;
  progress: { current: number; total: number; message?: string };
  createdAt: number;
  startedAt?: number;
  completedAt?: number;
  retryCount: number;
  maxRetries: number;
}

interface JobManager {
  submit<TInput, TOutput>(type: string, input: TInput, options?: JobOptions): string;
  cancel(jobId: string): boolean;
  getStatus(jobId: string): JobState;
  getResult<TOutput>(jobId: string): TOutput | undefined;
  onProgress(jobId: string, callback: (progress: JobProgress) => void): void;
  onStateChange(jobId: string, callback: (state: JobState) => void): void;
  list(filter?: JobFilter): JobSummary[];
}
```

### Worker Thread Patterns

> **Generation note:** CPU-intensive jobs must run in worker threads to avoid blocking the Main process event loop. Use `worker_threads` module.

```
Worker Thread Architecture:

  Main Process                          Worker Thread
  ┌──────────────┐                     ┌──────────────┐
  │ JobManager   │──── postMessage ───▶│ JobHandler   │
  │              │◀─── postMessage ────│              │
  │ State Track  │    (progress)       │ Execute Job  │
  │ IPC Bridge   │                     │ Report State │
  └──────────────┘                     └──────────────┘

  Communication protocol:
    Main → Worker: { type: 'start', jobId, input }
    Worker → Main: { type: 'progress', jobId, current, total, message }
    Worker → Main: { type: 'complete', jobId, result }
    Worker → Main: { type: 'failed', jobId, error }
    Main → Worker: { type: 'cancel', jobId }
```

> **Worker thread rules:**
> - Worker threads have no access to Electron APIs (no `ipcRenderer`, no `BrowserWindow`)
> - Worker threads communicate only via `postMessage` and `SharedArrayBuffer`
> - Each worker thread handles one job at a time — no concurrent job execution within a worker
> - Worker thread pool size = `Math.min(os.cpus().length - 1, MAX_WORKERS)` (leave one core for Main)
> - Worker threads must not import renderer-process code or browser globals
> - Timeout per job: configurable, default 300 seconds. Kill worker on timeout.

### IPC Job Communication

> **Generation note:** Job progress and results flow through defined IPC channels. Channel naming follows `domain:action` convention.

| Channel | Direction | Purpose | Payload |
|---|---|---|---|
| `jobs:submit` | Renderer → Main | Submit new job | `{ type, input, options }` |
| `jobs:status` | Renderer → Main | Query job state | `{ jobId }` → `{ state, progress }` |
| `jobs:cancel` | Renderer → Main | Cancel running job | `{ jobId }` → `{ success }` |
| `jobs:result` | Renderer → Main | Retrieve completed result | `{ jobId }` → `{ result }` |
| `jobs:progress` | Main → Renderer | Push progress update | `{ jobId, current, total, message }` |
| `jobs:state-change` | Main → Renderer | Push state transition | `{ jobId, from, to, error? }` |
| `jobs:list` | Renderer → Main | List all jobs | `{ filter? }` → `{ jobs[] }` |

> **IPC job communication rules:**
> - Progress updates are throttled: max 1 per second per job (avoid flooding)
> - Result retrieval is one-shot: `jobs:result` returns and clears the result from memory
> - Failed jobs retain error info for 24 hours, then auto-purge
> - Large results (>1MB) use file reference pattern: return path, not payload

### Job Persistence and Recovery

> **Generation note:** Jobs must survive app crashes and restarts. Persist job state to disk at every state transition.

```
Persistence Strategy:
  State Transition → Write to disk (JSON) → Proceed
  Disk Write Pattern:
    app.getPath('userData')/jobs/{jobId}.json
    {
      id, type, state, input, result?, error?,
      progress, createdAt, startedAt, completedAt,
      retryCount, maxRetries, lastTransitionAt
    }

  Recovery Pattern (on app start):
    1. Scan jobs/ directory for all .json files
    2. For jobs in COMPLETED state: load result, make available
    3. For jobs in INIT/LOADING/PROCESSING: mark as FAILED (crash recovery)
    4. For jobs with retryCount < maxRetries: auto-resubmit to queue
    5. For jobs in CANCELLED/STALE: clean up file
    6. Report recovery summary via IPC to any connected renderer
```

> **Persistence rules:**
> - Write at every state transition (not batched, not debounced)
> - Use atomic write: write to `.tmp` file, then rename (prevents corruption)
> - Input data persisted as reference (file path), not copy (avoid duplication)
> - Results persisted only if below size threshold (1MB); larger results use file reference
> - Job files cleaned up 7 days after COMPLETED/FAILED state

### Retry Policy

| Failure Type | Max Retries | Backoff | Conditions |
|---|---|---|---|
| Network error | 3 | Exponential (1s, 2s, 4s) | Non-transient errors excluded |
| Timeout | 2 | Fixed (5s) | Only if job type is idempotent |
| File not found | 0 | None | User must resolve |
| Permission denied | 0 | None | User must resolve |
| Worker crash | 1 | Fixed (10s) | Investigate root cause |
| Validation error | 0 | None | Fix input, resubmit |

### Progress Reporting

> **Generation note:** Long-running jobs must report progress. Progress data flows from worker → Main → Renderer via IPC.

```
Progress Reporting Pattern:

  Worker Thread:
    self.postMessage({
      type: 'progress',
      jobId: job.id,
      current: processedItems,
      total: totalItems,
      message: `Processing item ${processedItems}/${totalItems}`
    });

  Main Process (JobManager):
    on worker message → update job.progress → emit to IPC listeners

  Renderer Process:
    ipcRenderer.on('jobs:progress', (event, { jobId, current, total, message }) => {
      updateProgressBar(current / total);
      updateStatusText(message);
    });
```

> **Progress reporting rules:**
> - Progress percentage = `current / total * 100` (integer, 0–100)
> - Progress messages are human-readable, not technical
> - If total is unknown, use indeterminate mode: `{ current: 0, total: -1, message: 'Processing...' }`
> - Progress updates throttled to 1/second minimum interval
> - Renderer must handle missing progress gracefully (job may complete before first update)

### Job Queue Priority

| Priority | Job Types | Max Concurrent | Preemptible |
|---|---|---|---|
| **Critical** | Auto-update, crash recovery | 1 | No |
| **High** | User-triggered export, save | 2 | No |
| **Normal** | Background sync, indexing | 3 | Yes |
| **Low** | Analytics, diagnostics | 1 | Yes |

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables, code blocks, state diagrams
- **Audience:** engineer
- **Do:** Define explicit state machine; specify IPC channels for all job communication; enforce persistence at every state transition; provide retry policies per failure type
- **Don't:** Assume jobs always complete; skip crash recovery; allow unbounded concurrent jobs; use fire-and-forget pattern

**Required subsections:** Job State Machine, Worker Thread Patterns, IPC Communication, Persistence and Recovery
**Optional subsections:** Retry Policy, Progress Reporting, Job Queue Priority
**Required diagrams:** State machine, Worker communication diagram
**Required cross-references:** Architecture(05), IPC Pattern, Caching(11)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
