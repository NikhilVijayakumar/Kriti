# Security Hardening — Generation Template

> **Domain:** engineering
> **Section:** security_hardening
> **Source:** `documentation-standards/07-engineering-standards.md` §Security Hardening
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Security Hardening section for a Desktop Application Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `enforced_by` | architecture / process_isolation | Security hardening must respect process boundaries (Main/Renderer/Preload) |
| `derives_from` | security / threat_model | Hardening measures must map to identified threat vectors |
| `constrains` | engineering / code_standards | Security requirements override convenience patterns |

## Template

```markdown
## Security Hardening

> [metadata block]

[1 paragraph: overall security posture — defense-in-depth across all three Electron processes]

### Process Security Checklist

> **Generation note:** Every process (Main, Renderer, Preload) must have its own security checklist. These are not suggestions — they are hard requirements that gate deployment.

#### Main Process

| Requirement | Status | Rationale |
|---|---|---|
| `nodeIntegration: false` in all `BrowserWindow` configs | `[ ]` | Prevents renderer process from accessing Node.js APIs directly |
| `sandbox: true` on all renderer-hosting windows | `[ ]` | Enforces OS-level sandbox restricting filesystem/network access |
| `contextIsolation: true` on all `BrowserWindow` instances | `[ ]` | Isolates preload scripts from renderer JavaScript context |
| `webviewTag: false` unless explicitly required | `[ ]` | `<webview>` is a major attack surface — disable by default |
| `nodeIntegrationInWorker: false` | `[ ]` | Workers must not have Node.js access unless absolutely required |
| `allowRunningInsecureContent: false` | `[ ]` | Blocks HTTP-served scripts in HTTPS contexts |
| `experimentalFeatures: false` | `[ ]` | Disables Chrome experimental features that bypass security checks |
| All `webContents` use `session.setPermissionRequestHandler` | `[ ]` | Centralizes permission decisions (camera, microphone, notifications) |
| IPC handlers validate channel names against allowlist | `[ ]` | Prevents arbitrary IPC channel invocation |
| Native module loading restricted to `app.getPath('userData')` | `[ ]` | Limits native module search path |

#### Preload Script

| Requirement | Status | Rationale |
|---|---|---|
| Only `contextBridge.exposeInMainWorld` used | `[ ]` | Single sanctioned bridge mechanism — no direct `window` property assignment |
| Exposed API surface is minimal per feature | `[ ]` | Each feature exposes only the methods it needs — no `ipcRenderer.send` passthrough |
| No sensitive data in bridge API return values | `[ ]` | Renderer process is untrusted — never return tokens, keys, or paths |
| All exposed functions use named channel strings | `[ ]` | No dynamic channel construction — channels are static constants |
| Preload script has no network, filesystem, or `child_process` imports | `[ ]` | Preload executes in sandboxed context — respect the boundary |

#### Renderer Process

| Requirement | Status | Rationale |
|---|---|---|
| No `require()`, `process`, or `Buffer` globals | `[ ]` | Validates that `nodeIntegration` is truly disabled |
| Content Security Policy header set | `[ ]` | See CSP Configuration below |
| No `eval()`, `new Function()`, or inline script execution | `[ ]` | Prevents script injection via CSP bypass |
| All external links use `shell.openExternal()` via preload bridge | `[ ]` | Prevents renderer from navigating to arbitrary URLs |
| No `<meta http-equiv="refresh">` tags | `[ ]` | Prevents redirect-based phishing |

### Content Security Policy Configuration

> **Generation note:** CSP is your first line of defense against XSS. Define a strict policy per window type and enforce it.

```csp
default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
font-src 'self';
connect-src 'self' https://api.yourdomain.com;
object-src 'none';
base-uri 'self';
form-action 'self';
frame-src 'none';
worker-src 'self';
```

> **CSP deployment notes:**
> - Set via `session.defaultSession.webRequest.onHeadersReceived` in Main process
> - Different windows may need different CSP (admin windows may allow `connect-src` to internal APIs)
> - Log CSP violations via `report-uri` or `report-to` directive for monitoring
> - Test with `Content-Security-Policy-Report-Only` header before enforcing

### Code Signing Setup

> **Generation note:** Code signing is mandatory for production desktop applications. Unsigned executables trigger OS warnings and block installation.

| Platform | Tool | Key Storage | Build Integration |
|---|---|---|---|
| Windows | `electron-builder` with `win.certificateFile` | CI secret / HSM | `CSC_LINK` env var |
| macOS | `electron-notarize` with Apple Developer ID | Keychain / CI secret | `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD` env vars |
| Linux | GPG signing (optional) | GPG keyring | `GPG_PRIVATE_KEY` env var |

> **Code signing checklist:**
> - [ ] Certificate stored in CI secrets, never in repository
> - [ ] Certificate expiration monitored (renew 30 days before expiry)
> - [ ] macOS notarization runs as part of release pipeline
> - [ ] Windows SmartScreen reputation built via repeated signing
> - [ ] Update server serves only signed packages
> - [ ] Auto-update verifies signature before applying patch

### IPC Input Validation

> **Generation note:** Every IPC handler must validate its inputs. Renderer is untrusted — treat every message as potentially malicious.

```
IPC Validation Pattern:
1. Validate channel name is in allowed list
2. Validate payload type matches expected schema
3. Validate all string fields for length bounds
4. Validate numeric fields for range bounds
5. Reject unknown fields (strict schema)
6. Sanitize paths (resolve against known roots, reject traversal)
7. Log validation failures for security monitoring
```

> **Validation rules by data type:**
> - **Strings:** Max length, character whitelist, no control characters, no path traversal sequences (`..`, `~`)
> - **Paths:** Must resolve to allowed directories, use `path.resolve()` then prefix check
> - **Numbers:** Min/max bounds, no `NaN`, no `Infinity`
> - **Booleans:** Strict type check — reject `0`, `1`, `"true"`, `"false"`
> - **Arrays:** Max length, element type validation, no nested objects unless explicitly allowed
> - **Objects:** Schema validation (allowlist keys), reject prototype pollution (`__proto__`, `constructor`)

### Process Privilege Restrictions

| Process | Filesystem | Network | IPC Scope | Native Modules |
|---|---|---|---|---|
| Main | Full (rooted at `app.getPath`) | Full | All handlers | Yes |
| Preload | None | None | Restricted bridge only | No |
| Renderer | None (via sandbox) | Via `fetch` under CSP | Bridge methods only | No |

> **Privilege escalation prevention:**
> - Renderer must never receive `ipcRenderer` — only `contextBridge`-wrapped methods
> - Preload must not re-expose `ipcRenderer.send` or `ipcRenderer.invoke` directly
> - Main process IPC handlers must not forward raw input to other handlers
> - Database access only from Main process — renderer queries go through IPC
> - File I/O only from Main process — renderer triggers via `dialog.showOpenDialog`

### Auto-Update Security

> **Generation note:** Auto-update is a critical attack vector. Compromise the update channel and you compromise every installation.

| Requirement | Implementation |
|---|---|
| HTTPS-only update server | Hardcode `https://` — no `http://` fallback |
| Signature verification | Verify code signature before applying update |
| Staged rollouts | 5% → 25% → 100% with 24h soak between stages |
| Rollback capability | Keep previous version available for emergency rollback |
| Integrity checks | SHA-256 hash verification of downloaded package |

### Security Audit Checklist

> **Generation note:** Run this checklist before every major release. Document findings in engineering document.

- [ ] All `BrowserWindow` instances created with secure defaults
- [ ] No `nodeIntegration: true` anywhere in codebase (grep audit)
- [ ] All IPC channels registered and validated
- [ ] CSP headers set for all window types
- [ ] Code signing certificates valid and not expired
- [ ] Auto-update channel uses HTTPS and verifies signatures
- [ ] No hardcoded secrets, tokens, or credentials in source
- [ ] Dependencies scanned for known vulnerabilities (`npm audit`)
- [ ] Native modules rebuilt for target platform (no cross-platform binary leaks)
- [ ] Crash reporter does not send sensitive user data
- [ ] `shell.openExternal` called only with validated URLs
- [ ] No `webview` tags without explicit security review

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** checklists, tables, code blocks
- **Audience:** security engineer
- **Do:** Provide actionable checklists with rationale; define concrete validation patterns; specify per-process security boundaries
- **Don't:** Use vague security language; omit rationale for requirements; treat all processes as equally privileged

**Required subsections:** Process Security Checklist, CSP Configuration, Code Signing, IPC Input Validation
**Optional subsections:** Auto-Update Security, Security Audit Checklist
**Required diagrams:** none
**Required cross-references:** Architecture(05), Security(03), Code Standards(06)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
