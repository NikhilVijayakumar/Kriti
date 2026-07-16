# Caching — Generation Template

> **Domain:** engineering
> **Section:** caching
> **Source:** `documentation-standards/07-engineering-standards.md` §Caching Strategy
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Caching Strategy section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `governed_by` | architecture / storage_domains | Cache strategy must respect Local/Vault/Document domain boundaries |
| `uses` | engineering / background_processing | Cache invalidation jobs run as background processes |
| `constrained_by` | security / threat_model | Cached data must respect encryption-at-rest and access control |

## Template

```markdown
## Caching Strategy

> [metadata block]

[1 paragraph: overall caching philosophy — reduce IPC round-trips, minimize redundant computation, respect storage domain boundaries]

### Cache Architecture by Process

> **Generation note:** Each Electron process has different caching capabilities and constraints. Main process has full access; Renderer is sandboxed. Design caches accordingly.

#### Main Process Caches

| Cache Name | Storage | TTL | Max Size | Eviction |
|---|---|---|---|---|
| `{{cache_name}}` | `[Memory / Disk / Both]` | `[duration]` | `[size]` | `[LRU / LFU / TTL]` |

> **Main process caching patterns:**
> - **In-memory cache:** Fastest access. Use for hot data queried frequently (config, feature flags, session state). Size-limited — evict on memory pressure.
> - **Disk cache:** Persisted to `app.getPath('userData')/cache/`. Use for large read-heavy data (documents, templates, offline assets). Survives restart.
> - **Database cache:** SQLite-backed for query-heavy data. Indexed for fast lookup. Use when in-memory is too small and disk-file access is too slow.

```
Main Process Cache Lifecycle:
  INIT → (check memory) → HIT: return cached
                        → MISS → (check disk) → HIT: load to memory, return
                                               → MISS → (fetch from source) → store → return
  MEMORY_PRESSURE → evict LRU entries → persist dirty entries to disk
```

#### Renderer Process Caches

| Cache Name | Storage | TTL | Max Size | Eviction |
|---|---|---|---|---|
| `{{cache_name}}` | `[IndexedDB / sessionStorage / DOM]` | `[duration]` | `[size]` | `[TTL / LRU / Manual]` |

> **Renderer process caching patterns:**
> - **IndexedDB:** Structured data cache. Use for query results, user preferences, UI state. Async API — no blocking.
> - **sessionStorage:** Transient UI state. Page-scoped, cleared on navigation. Use for form drafts, scroll positions.
> - **DOM cache:** Component-level memoization. React `memo()`, `useMemo()`. Avoids re-render cost.
> - **Service Worker cache:** Offline asset cache. Pre-cache critical assets, network-first for dynamic content.

#### Preload Bridge Cache Passthrough

> **Generation note:** Preload scripts must not cache sensitive data. Bridge methods that return cached Main-process data must validate freshness.

```
Preload Cache Pattern:
  renderer calls bridge.getCachedData(key)
  → preload invokes ipcRenderer.invoke('cache:get', key)
  → main process returns cached value with timestamp
  → preload returns data + metadata (staleness indicator)
  → renderer decides whether to use stale data or request refresh
```

### Storage Domain Cache Mapping

> **Generation note:** Each storage domain has different cache requirements. Map caches to domains explicitly.

| Domain | Cache Location | Invalidation Trigger | Encryption |
|---|---|---|---|
| **Local** (preferences, UI state) | Renderer IndexedDB + Main memory | User action, config change | Optional (user preference) |
| **Vault** (secrets, credentials) | Main process only (memory, short TTL) | Session end, explicit revocation | Required (AES-256-GCM) |
| **Document** (user files, data) | Main process disk cache + Service Worker | File change, sync event | Required (at-rest) |

> **Domain-specific rules:**
> - **Local:** Aggressive caching OK. TTL can be long (hours/days). Cache survives app restart.
> - **Vault:** Minimal caching. TTL ≤ session duration. Never persist to disk unencrypted. Clear on lock/sleep.
> - **Document:** Cache aggressively but validate freshness on every access. File watcher triggers invalidation.

### Cross-Process Cache Coherence

> **Generation note:** When Main and Renderer both cache the same data, stale reads are possible. Define explicit coherence protocol.

```
Coherence Protocol:
  1. Main process is source of truth for all cached data
  2. Renderer caches are read-only mirrors (never write-through)
  3. Main process broadcasts invalidation via IPC:
     - Channel: cache:invalidate
     - Payload: { domain: string, keys: string[], reason: string }
  4. Renderer listens for invalidations, purges local cache entries
  5. Renderer requests fresh data on next access
  6. If Main process is unavailable, Renderer uses cached data with staleness flag
```

> **Invalidation triggers:**
> - File changed (Document domain) → `fs.watch` in Main → IPC broadcast
> - Config updated (Local domain) → Main writes → IPC broadcast
> - User logout (Vault domain) → Main clears vault cache → IPC broadcast
> - Database migrated → Main invalidates all affected caches → IPC broadcast
> - Timer expiry (TTL) → Local invalidation only, no IPC broadcast needed

### Cache Invalidation Strategy

| Invalidation Type | Implementation | When to Use |
|---|---|---|
| **Time-based (TTL)** | `setTimeout` per entry, auto-expire | Data that degrades slowly (config, feature flags) |
| **Event-based** | IPC `cache:invalidate` broadcast | Data that changes via external action (file edit, config save) |
| **Version-based** | ETag / hash comparison on fetch | Network-sourced data with server-side versioning |
| **Manual** | Explicit `cache.delete(key)` call | User-initiated refresh, destructive actions |
| **LRU eviction** | Access-time tracking, evict oldest | Memory-bounded caches where capacity > completeness |

### Cache Size Management

> **Generation note:** Desktop apps run on constrained hardware. Cache size must be bounded and monitored.

| Cache Type | Default Max | Growth Policy | Pressure Response |
|---|---|---|---|
| In-memory (Main) | `{{max_memory_mb}}` MB | Fixed | Evict LRU → warn at 80% |
| Disk (Main) | `{{max_disk_mb}}` MB | Fixed | Evict oldest → warn at 90% |
| IndexedDB (Renderer) | `{{max_idb_mb}}` MB | Configurable | `quota` API → evict by domain |
| Service Worker | `{{max_sw_mb}}` MB | Cache-first | `caches.delete()` oldest entries |

```
Cache Pressure Response:
  Level 1 (70%): Log warning, stop caching optional data
  Level 2 (85%): Evict TTL-expired entries aggressively
  Level 3 (95%): Evict LRU entries, notify renderer of reduced cache
  Level 4 (100%): Emergency purge — clear all non-essential caches
```

### Offline Cache Strategy

> **Generation note:** Desktop apps must handle offline gracefully. Pre-cache critical assets, defer non-essential.

| Asset Type | Offline Strategy | Pre-cache |
|---|---|---|
| App shell (HTML/CSS/JS) | Service Worker cache-first | Yes |
| Static assets (images, fonts) | Service Worker cache-first | Yes |
| API responses | Network-first, fallback to cache | No (cache on first access) |
| User documents | Read from local disk | N/A (already local) |
| Real-time data | Queue for sync when online | No |

### Cache Monitoring

> **Generation note:** Cache health is observable through standard metrics. Report via IPC to Main process for diagnostics.

| Metric | Source | Threshold | Action |
|---|---|---|---|
| Hit rate | Per-cache counter | `< 60%` | Review TTL / cache size |
| Memory usage | `process.memoryUsage()` | `> 80%` of max | Trigger eviction |
| Disk usage | `fs.statSync(cacheDir)` | `> 90%` of max | Emergency purge |
| Invalidation lag | Timestamp delta | `> 30s` | Check IPC channel health |

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables, code blocks, diagrams
- **Audience:** engineer
- **Do:** Define cache behavior per process and storage domain; specify invalidation and coherence protocol; set explicit size limits
- **Don't:** Assume unlimited memory; skip cross-process coherence; treat all data with same cache policy

**Required subsections:** Cache Architecture by Process, Storage Domain Mapping, Cross-Process Coherence, Invalidation Strategy
**Optional subsections:** Offline Strategy, Cache Monitoring, Size Management
**Required diagrams:** none
**Required cross-references:** Architecture(05), Storage Domains, Background Processing(12)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
