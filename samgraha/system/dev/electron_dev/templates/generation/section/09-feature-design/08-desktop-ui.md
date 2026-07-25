# Desktop UI Feature Design — Generation Template

> **Domain:** feature-design
> **Section:** desktop_ui
> **Source:** `documentation-standards/09-feature-design-standards.md` §Desktop UI
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate the Desktop UI Feature Design section for a Feature Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Desktop UI must deliver the user experience defined in the Feature Specification |
| `uses` | architecture / window_management | UI layout governed by window lifecycle and multi-window coordination rules |
| `integrates` | engineering / ipc_pattern | All UI↔backend communication uses IPC abstraction layers |
| `respects` | engineering / keyboard_accessibility | All interactions must be keyboard-accessible |

## Template

```markdown
## Desktop UI Feature Design

> [metadata block]

[1 paragraph: this feature's desktop UI approach — native window management, platform integration, keyboard-first interaction model]

### Window Management

> **Generation note:** Every window is a `BrowserWindow` instance with explicit lifecycle management. No untracked windows.

#### Window Lifecycle

```
Window Lifecycle States:

  ┌─────────┐   show()    ┌─────────┐   blur/focus  ┌─────────┐
  │ CREATED │────────────▶│ VISIBLE │◀──────────────▶│ FOCUSED │
  └─────────┘             └─────────┘                └─────────┘
       │                       │                          │
       │ close()               │ close()                  │ close()
       ▼                       ▼                          ▼
  ┌─────────┐            ┌─────────┐                ┌─────────┐
  │ CLOSING │            │ CLOSING │                │ CLOSING │
  └─────────┘            └─────────┘                └─────────┘
       │                       │                          │
       ▼                       ▼                          ▼
  ┌─────────┐            ┌─────────┐                ┌─────────┐
  │ CLOSED  │            │ CLOSED  │                │ CLOSED  │
  └─────────┘            └─────────┘                └─────────┘
```

> **Window lifecycle rules:**
> - Every `BrowserWindow` must have a registered owner (Main process module)
> - Windows must set `close` event handler to confirm destructive actions before closing
> - Hidden windows (tray background) use `hide()` not `destroy()` — preserve state
> - All windows must have `title` set (no empty title bars)
> - Window bounds persisted to Local storage domain on resize/move
> - Maximum window count per feature: 1 (single-instance) or N (multi-document)

#### Window Configuration

| Window Type | Width | Height | Resizable | Minimizable | Always on Top | Frame |
|---|---|---|---|---|---|---|
| `{{main_window}}` | `{{width}}` | `{{height}}` | `{{resizable}}` | `{{minimizable}}` | `{{always_on_top}}` | `{{frame}}` |
| `{{secondary_window}}` | `{{width}}` | `{{height}}` | `{{resizable}}` | `{{minimizable}}` | `{{always_on_top}}` | `{{frame}}` |
| `{{dialog_window}}` | `{{width}}` | `{{height}}` | `false` | `false` | `true` | `false` |

> **Window configuration rules:**
> - Main window: `show: false` until ready (prevents white flash)
> - Secondary windows: positioned relative to parent window center
> - Dialog windows: frameless, centered on parent, modal (`parent` option)
> - All windows: `webPreferences.nodeIntegration: false`, `contextIsolation: true`

### Multi-Window Coordination

> **Generation note:** When a feature uses multiple windows, define explicit communication and state synchronization patterns.

```
Multi-Window Communication:

  ┌──────────────┐     IPC      ┌──────────────┐
  │  Main Window │◀────────────▶│  Settings    │
  │  (primary)   │              │  Window      │
  └──────┬───────┘              └──────────────┘
         │
         │ IPC
         ▼
  ┌──────────────┐
  │  Detail      │
  │  Window      │
  └──────────────┘

  Coordination Rules:
  1. Main window is source of truth for shared state
  2. Secondary windows subscribe to state changes via IPC
  3. State mutations only through Main window (or Main process)
  4. Secondary windows emit events, Main window applies mutations
  5. Window close does not affect other windows (no cascade)
  6. All windows receive `app:quit` signal on application exit
```

> **Multi-window patterns:**
> - **Primary/Secondary:** Main window owns state; secondary windows are views into subsets
> - **Inspector:** Detail window opens for selected item; bidirectional selection sync
> - **Modal:** Dialog window blocks parent interaction until dismissed; returns result via IPC
> - **Independent:** Each window is self-contained; no shared state beyond application config

### Native Dialog Integration

> **Generation note:** Use Electron's `dialog` module for all system dialogs. Never implement custom file pickers or message boxes.

| Dialog Type | API | When to Use | Returns |
|---|---|---|---|
| Open File | `dialog.showOpenDialog` | User selects file(s) to open | `{ filePaths[], canceled }` |
| Save File | `dialog.showSaveDialog` | User specifies output file path | `{ filePath, canceled }` |
| Message Box | `dialog.showMessageBox` | Confirm destructive actions, show errors | `{ response, checkboxChecked }` |
| Custom | `BrowserWindow` (dialog) | Complex selection (multi-step, preview) | Custom IPC result |

> **Dialog integration rules:**
> - All dialogs must be parented to the active window (prevents orphan dialogs)
> - File dialogs must filter by relevant extensions (`filters` option)
> - Destructive actions require confirmation dialog with explicit "Cancel" option
> - Dialog results must be checked for `canceled` before processing
> - Batch file operations: use file picker with `properties: ['multiSelections']`

### Tray Menu Design

> **Generation note:** System tray provides quick access to common actions when the app is minimized or backgrounded.

```
Tray Menu Structure:

  ┌─────────────────────────────┐
  │  {{App Name}}               │  ← always present
  │  ─────────────────────────  │
  │  Show Window                │  ← primary action
  │  ─────────────────────────  │
  │  {{Quick Action 1}}         │  ← feature-specific
  │  {{Quick Action 2}}         │
  │  ─────────────────────────  │
  │  Preferences...             │  ← always present
  │  ─────────────────────────  │
  │  Quit                       │  ← always present
  └─────────────────────────────┘
```

> **Tray menu rules:**
> - Tray icon visible when: window is closed/minimized, OR app runs in background
> - Double-click tray icon: show/restore main window
> - Menu rebuilt on each open (dynamic state: enabled/disabled items)
> - Tray tooltip shows app version and status
> - Quit from tray fully exits app (no background process unless explicitly designed)

### Notification System

> **Generation note:** Desktop notifications inform users of background events. Use Electron's `Notification` API.

| Notification Type | Priority | Auto-dismiss | Action |
|---|---|---|---|
| **Information** | Low | 5 seconds | None |
| **Success** | Low | 3 seconds | None |
| **Warning** | Medium | 10 seconds | Click to open relevant window |
| **Error** | High | Manual dismiss | Click to open error details |
| **Critical** | Maximum | Manual dismiss | Blocks until acknowledged |

> **Notification rules:**
> - Notifications must not appear when app is in foreground (show in-app banner instead)
> - Max 3 notifications queued — older ones replaced
> - Notification click opens/focuses relevant window
> - Notifications respect OS "Do Not Disturb" mode
> - Sensitive data never shown in notification body

### Keyboard Shortcuts

> **Generation note:** All features must have keyboard shortcuts. Shortcuts follow platform conventions.

| Shortcut | Action | Scope | Notes |
|---|---|---|---|
| `{{shortcut}}` | `{{action}}` | `{{global/window}}` | `{{notes}}` |

> **Keyboard shortcut rules:**
> - Windows/Linux: `Ctrl+{{key}}` | macOS: `Cmd+{{key}}`
> - Global shortcuts registered via `globalShortcut` module (only when app focused)
> - Window-scoped shortcuts via `Menu` accelerator (active when window focused)
> - Shortcut conflicts detected and warned at registration time
> - All shortcuts discoverable via Help > Keyboard Shortcuts menu
> - `Ctrl/Cmd+Q` always quits; `Ctrl/Cmd+W` always closes current window
> - Function keys reserved: F1=Help, F5=Refresh, F11=Fullscreen toggle

### Drag and Drop

> **Generation note:** Desktop apps support native drag-and-drop for files and data. Define drop zones and drag sources explicitly.

```
Drag-and-Drop Flow:

  Source (Renderer)              Target (Renderer/Window)
  ┌──────────────┐              ┌──────────────┐
  │ dragstart     │─── drag ───▶│ dragover      │
  │ → data payload│              │ → validate    │
  └──────────────┘              └──────────────┘
                                       │
                                       ▼ valid?
                                  ┌──────────┐
                                  │ drop      │
                                  │ → process │
                                  └──────────┘
```

> **Drag-and-drop rules:**
> - File drops: validate file types via extension AND MIME type
> - File drops: never trust filename — read file content for validation
> - Visual feedback: drop zone highlights on `dragover`, reverts on `dragleave`
> - Drag source provides data payload via `dataTransfer.setData`
> - Cross-window drops use IPC: Main process relays data between renderer processes
> - Maximum file count per drop: configurable, default 50

### Context Menus

> **Generation note:** Right-click context menus provide contextual actions. Use Electron's `Menu.buildFromTemplate`.

> **Context menu rules:**
> - Menu items are context-sensitive (enabled/disabled based on selection)
> - Separator lines between logical groups
> - Keyboard accelerators displayed in menu items
> - Destructive actions (delete, remove) shown in red or at bottom with separator
> - Context menu closed on: click outside, Escape key, action selected
> - Right-click on disabled element: show read-only context menu (copy, inspect)

### Accessibility

> **Generation note:** Desktop UI must meet WCAG 2.1 AA. Keyboard navigation is non-negotiable.

| Requirement | Implementation |
|---|---|
| Keyboard navigation | All interactive elements focusable via Tab/Shift+Tab |
| Focus indicators | Visible focus ring on all focusable elements |
| Screen reader support | ARIA labels on all interactive elements |
| High contrast | Respect OS high-contrast mode |
| Font scaling | UI scales with OS font size setting |
| Reduced motion | Respect `prefers-reduced-motion` media query |
| Color contrast | Minimum 4.5:1 ratio for text, 3:1 for large text |

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables, code blocks, diagrams
- **Audience:** UI engineer
- **Do:** Define window lifecycle explicitly; specify keyboard shortcuts for all actions; integrate native dialogs; respect platform conventions
- **Don't:** Implement custom dialogs when native ones exist; ignore keyboard accessibility; assume mouse-only interaction

**Required subsections:** Window Management, Native Dialog Integration, Keyboard Shortcuts
**Optional subsections:** Multi-Window Coordination, Tray Menu, Notifications, Drag-and-Drop, Context Menus, Accessibility
**Required diagrams:** Window lifecycle, Multi-window communication
**Required cross-references:** Architecture(05), IPC Pattern, Feature Specification, Accessibility Standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
