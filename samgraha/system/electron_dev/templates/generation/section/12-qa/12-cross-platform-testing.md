# Cross-Platform Testing — Generation Template

> **Domain:** qa
> **Section:** cross_platform_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Cross-Platform Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Cross-Platform Testing section for a QA document in a desktop application.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / component_model | Platform test matrix must cover all process isolation boundaries (Main/Renderer/Preload) |
| `derives_from` | architecture / communication_paths | IPC channel behavior must be verified across every target OS |
| `derives_from` | feature / purpose | Platform-specific feature behavior must trace to Feature requirements |

## Template

```markdown
## Cross-Platform Testing

### Platform Test Matrix

| OS | Version Range | Architecture | Electron Channel | Test Runner | Status |
|----|--------------|--------------|------------------|-------------|--------|
| Windows | 10 (1903+), 11 | x64, arm64 | Stable | [runner] | [status] |
| macOS | 12+ (Monterey) | x64, arm64 (Apple Silicon) | Stable | [runner] | [status] |
| Linux | Ubuntu 20.04+, Fedora 38+, Debian 12+ | x64 | Stable | [runner] | [status] |

### Platform-Specific Behavior Tests

| Behavior | Windows | macOS | Linux | Verification Method |
|----------|---------|-------|-------|-------------------|
| [Behavior 1] | [Windows-specific expectation] | [macOS-specific expectation] | [Linux-specific expectation] | [Test approach] |
| [Behavior 2] | [Windows-specific expectation] | [macOS-specific expectation] | [Linux-specific expectation] | [Test approach] |

### Native Integration Tests

| Integration | Windows | macOS | Linux | Test Strategy |
|-------------|---------|-------|-------|---------------|
| File system paths | NTFS conventions, UNC paths, drive letters | APFS, case-insensitive, `/Users/` | ext4/btrfs, case-sensitive, `/home/` | Path normalization assertions |
| Native dialogs | Win32 Common Dialogs via `dialog.showOpenDialog` | Cocoa NSOpenPanel via `dialog.showOpenDialog` | GTK via `dialog.showOpenDialog` | Screenshot assertion + Playwright click |
| System notifications | Windows Toast via `Notification` API | macOS Notification Center via `Notification` API | libnotify via `Notification` API | Notification delivery assertion |
| Auto-launch / startup | Registry `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | `~/Library/LaunchAgents/` plist | `~/.config/autostart/` .desktop file | Registry/plist/desktop-file existence assertion |
| Tray icon | Win32 `Tray` with `NativeImage` | Cocoa `Tray` with `NativeImage` | AppIndicator or `Tray` with `NativeImage` | Tray presence assertion via screen reader |
| Window decorations | Native Win32 frame, snap layouts (Win11) | Traffic light buttons, full-screen menu bar | GTK window decorations, tiling WM hints | Visual regression assertion |
| File associations | Windows Registry file association + `HKEY_CLASSES_ROOT` | macOS `Info.plist` `CFBundleDocumentTypes` | XDG `mimeapps.list` + desktop entry | Open-with-default-app assertion |
| Certificate store | Windows certificate store via `app.getPath('certificateStore')` | macOS Keychain via `security` CLI | NSS/`/etc/ssl/certs` | Certificate trust assertion |

### Platform Edge Cases

| Edge Case | Platform | Expected Behavior | Test Method |
|-----------|----------|-------------------|-------------|
| High DPI / scaling > 200% | All | UI renders without clipping or misalignment | Automated screenshot at 150%, 200%, 300% |
| Non-ASCII paths (CJK, Arabic, Cyrillic) | All | Files open/save correctly without mojibake | Create temp dir with Unicode name, verify round-trip |
| Deeply nested paths (> 260 chars) | Windows | Long path support enabled or graceful error | Attempt open of 300-char path |
| Symbolic links | All | Symlinks followed correctly, no permission errors | Create symlink to config, verify read/write |
| Read-only filesystem | macOS (SIP), Linux (immutable mount) | Graceful error, no crash | Mount read-only, attempt write |
| Multiple monitors with different DPI | All | Window renders correctly on each monitor | Move window between monitors, screenshot each |
| System sleep/wake cycle | All | IPC connections survive sleep/wake, no data loss | Sleep 5s, wake, verify state |
| GPU process crash | All | App recovers, renderer reloads | Kill GPU process, verify recovery |
| Locale change mid-session | All | Date/number formatting updates, no crash | Change system locale, verify rendering |

### CI Matrix Configuration

```yaml
platform_matrix:
  os: [windows-latest, macos-latest, ubuntu-latest]
  electron_channel: [stable]
  architecture: [x64]
  include:
    - os: macos-latest
      architecture: arm64
    - os: windows-latest
      architecture: arm64
  test_types:
    - unit
    - integration
    - e2e
    - native_dialog
    - ipc
  exclude:
    - os: ubuntu-latest
      test_types: [native_dialog]

  failure_policy: any_failure_blocks
  retry:
    max_attempts: 2
    backoff: exponential

  artifacts:
    screenshots: true
    logs: true
    crash_reports: true
    platform_diagnostics:
      windows: [event_logs, gpu_info]
      macos: [console_logs, system_profiler]
      linux: [dmesg, journalctl]
```

### Platform-Specific CI Steps

| CI Step | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Install dependencies | `npm ci` | `npm ci` | `npm ci` |
| Build native modules | `node-gyp rebuild` (MSVC) | `node-gyp rebuild` (Xcode) | `node-gyp rebuild` (gcc) |
| Code signing test | Verify signing config (no actual sign in CI) | Verify entitlements plist | N/A (not required) |
| Package test build | `electron-builder --win --dir` (portable) | `electron-builder --mac --dir` | `electron-builder --linux --dir` |
| E2E test | Playwright on Windows runner | Playwright on macOS runner | Playwright on Ubuntu runner |
| Artifact upload | Screenshot diffs, logs, .dmp crash files | Screenshot diffs, logs, .ips crash files | Screenshot diffs, logs, core dumps |

### Platform Compatibility Assertions

| Assertion | Condition | Severity | Blocking |
|-----------|-----------|----------|----------|
| All unit tests pass on target OS | `test_results.passed === test_results.total` | critical | yes |
| IPC channels functional across processes | All `invoke`/`send`/`on` pairs succeed | critical | yes |
| Native dialog renders and returns | Dialog opens, selection captured | high | yes |
| No native module segfaults | Zero SIGSEGV / EXC_BAD_ACCESS / access violation | critical | yes |
| Window manages correct geometry | Window bounds match requested dimensions | medium | no |
| Tray icon visible in system tray | Icon present after `Tray` instantiation | medium | no |
| Auto-update check completes | Update check returns valid response or "no update" | high | no |
| Performance within threshold | Startup < 3s, IPC round-trip < 50ms, memory < 500MB | medium | no |
| Accessibility tree complete | All interactive elements exposed to screen reader | high | no |
```

## Examples

**Correct:**
> ### Platform Test Matrix
>
> | OS | Version Range | Architecture | Electron Channel | Test Runner | Status |
> |----|--------------|--------------|------------------|-------------|--------|
> | Windows | 10 (1903+), 11 | x64, arm64 | Stable | GitHub Actions `windows-latest` | active |
> | macOS | 12+ (Monterey) | x64, arm64 | Stable | GitHub Actions `macos-latest` | active |
> | Linux | Ubuntu 20.04+, Fedora 38+ | x64 | Stable | GitHub Actions `ubuntu-latest` | active |
>
> ### Platform-Specific Behavior Tests
>
> | Behavior | Windows | macOS | Linux | Verification Method |
> |----------|---------|-------|-------|-------------------|
> | Window snapping | Snap to left/right, Win11 snap layouts | Green maximize button, Split View | Tiling WM hints | Window position assertion after snap |
> | Context menu | Native Win32 context menu | Native Cocoa context menu | GTK context menu | Menu item count assertion |

**Incorrect:**
> We test on Windows, Mac, and Linux. Each platform gets the same tests and they should all work the same way.
> *Why wrong: cross-platform testing must define a platform test matrix with explicit version ranges, architectures, and runner configurations; platform-specific behavior must be listed with per-OS expectations; native integration tests must verify OS-specific behavior patterns.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Define the platform test matrix with OS versions, architectures, and CI runners; list platform-specific behaviors with per-OS expectations; include native integration tests for file system, dialogs, notifications, tray, window management, file associations, and certificate store; define platform edge cases (high DPI, non-ASCII paths, deep nesting, symlinks, sleep/wake, GPU crash); provide CI matrix YAML configuration; specify platform-specific CI steps; define compatibility assertions with severity and blocking status
- **Don't:** Assume identical behavior across platforms; omit platform-specific version ranges or architecture variants; skip native integration test coverage; leave platform edge cases undefined; omit CI matrix configuration

**Required subsections:** Platform Test Matrix, Platform-Specific Behavior Tests, Native Integration Tests, Platform Edge Cases, CI Matrix Configuration
**Optional subsections:** Platform-Specific CI Steps, Platform Compatibility Assertions
**Required diagrams:** none
**Required cross-references:** Architecture(05), Feature(04), Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
