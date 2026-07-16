# Desktop Packaging Strategy — Generation Template

> **Domain:** build
> **Section:** packaging
> **Source:** `documentation-standards/14-build-standards.md` §Packaging
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the Desktop Packaging Strategy section for a Build Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / build_standards | Packaging the requires:. |89699 |.0o43.. 7468 | | |1.5 | | |18 |

 |        <14-build-relationships.yaml` |

## Template

```markdown
## Desktop Packaging Strategy

### electron-builder Configuration

| Property | Windows | macOS | Linux |
|----------|---------|-------|-------|
| `appId` | `{appId}` | `{appId}` | `{appId}` |
| `productName` | `{productName}` | `{productName}` | `{productName}` |
| `outputDir` | `dist/win` | `dist/mac` | `dist/linux` |
| `asar` | `true` | `true` | `true` |
| `asarUnpack` | `[native modules]` | `[native modules]` | `[native modules]` |
| `files` | `[include patterns]` | `[include patterns]` | `[include patterns]` |
| `extraResources` | `[resource files]` | `[resource files]` | `[resource files]` |
| `compression` | `maximum` | `maximum` | `maximum` |
| `artifactName` | `${productName}-${version}-setup.${ext}` | `${productName}-${version}.${ext}` | `${productName}-${version}.${ext}` |

### Platform Packaging

| Format | Target OS | File Extension | Install Mechanism | File Size Estimate |
|--------|----------|---------------|-------------------|-------------------|
| NSIS Installer | Windows 10+ | `.exe` | User-guided wizard, per-user or per-machine | [size] |
| MSI Installer | Windows 10+ | `.msi` | Group Policy deployment, silent install | [size] |
| Portable | Windows 10+ | `.exe` | No install, single executable | [size] |
| DMG | macOS 12+ | `.dmg` | Drag-to-Applications | [size] |
| ZIP | macOS 12+ | `.zip` | Manual extraction | [size] |
| AppImage | Linux (universal) | `.AppImage` | `chmod +x && ./run` | [size] |
| DEB | Debian/Ubuntu | `.deb` | `dpkg -i` or Software Center | [size] |
| RPM | Fedora/RHEL | `.rpm` | `rpm -i` or DNF | [size] |

### NSIS Installer Customization

| Setting | Value | Purpose |
|---------|-------|---------|
| `oneClick` | `false` | Allow user to choose install directory |
| `perMachine` | `true` | Available to all users (requires admin) |
| `allowToChangeInstallationDirectory` | `true` | User selects custom install path |
| `installerIcon` | `build/icon.ico` | Custom installer icon |
| `uninstallerIcon` | `build/icon.ico` | Custom uninstaller icon |
| `installerHeaderIcon` | `build/icon.ico` | Header icon in wizard |
| `createDesktopShortcut` | `true` | Desktop shortcut option |
| `createStartMenuShortcut` | `true` | Start Menu entry |
| `shortcutName` | `{productName}` | Shortcut display name |
| `runAfterFinish` | `true` | Launch app after install |
| `deleteAppDataOnUninstall` | `false` | Preserve user data on uninstall |
| `script` | `build/installer.nsh` | Custom NSIS script for advanced behavior |

### DMG Configuration

| Setting | Value | Purpose |
|---------|-------|---------|
| `background` | `build/dmg-background.png` | Background image (1024×640 @2x) |
| `iconSize` | 80 | Icon size in DMG window |
| `contents` | Array of `{x, y, type, path}` | Icon positioning in DMG window |
| `window` | `{width: 560, height: 400}` | DMG window dimensions |
| `format` | `ULFO` | Compression format (best ratio) |
| `sign` | `true` | Sign the DMG itself |

### Linux Desktop Integration

| Property | Value | Purpose |
|----------|-------|---------|
| `desktop` | `{name: '{productName}', exec: '{appName}', icon: 'build/icon', Categories: '{categories}'}` | `.desktop` file for app launcher |
| `mimeTypes` | `['{mimeTypes}']` | File type associations |
| `maintainer` | `{maintainer}` | Package maintainer field |
| `homepage` | `{homepage}` | Package homepage |
| `fpm` | Array of flags | Custom FPM packaging flags |

### Code Signing

| Platform | Signing Type | Certificate Source | Verification |
|----------|-------------|-------------------|-------------|
| Windows | Authenticode (EV or Standard) | `CSC_LINK` env var (PFX) or `CSC_KEY_PASSWORD` | `signtool verify /pa` |
| macOS | Apple Developer ID | `CSC_LINK` (p12) + `CSC_KEY_PASSWORD` | `codesign --verify --deep` |
| macOS (notarization) | Apple Notarization | `APPLE_ID` + `APPLE_APP_SPECIFIC_PASSWORD` + `APPLE_TEAM_ID` | `stapler validate` |
| Linux | N/A (no signing) | N/A | N/A |

**Code signing verification steps:**

```bash
# Windows
signtool verify /pa /v dist/win/${productName}-${version}-setup.exe

# macOS
codesign --verify --deep --strict dist/mac/${productName}.app
xcrun notarytool submit dist/mac/${productName}.dmg --apple-id $APPLE_ID --team-id $APPLE_TEAM_ID
xcrun stapler staple dist/mac/${productName}.dmg
```

### Asset Optimization

| Asset | Optimization | Target Size | Format |
|-------|-------------|-------------|--------|
| App icon (ICO) | Multi-size (16,32,48,256) | < 100KB | `.ico` |
| App icon (ICNS) | Multi-size + @2x variants | < 200KB | `.icns` |
| App icon (PNG) | 512×512 + 1024×1024 @2x | < 300KB | `.png` |
| DMG background | @2x Retina, 1024×640 | < 500KB | `.png` |
| Installer header | 164×314 NSIS header | < 50KB | `.bmp` |
| Tray icon | 22×22 (Win), 22×22 (Mac), 22×22 (Linux) | < 10KB each | `.png` |

### Installer Design

| Element | Windows (NSIS) | macOS (DMG) | Linux (AppImage) |
|---------|---------------|-------------|------------------|
| Welcome page | Custom header + app name | Background image + icon grid | Default AppImage UI |
| License page | `LICENSE.txt` displayed | License in DMG window | N/A |
| Install directory | `Program Files\{productName}` or user-selected | `/Applications` | N/A (portable) |
| Progress bar | Standard NSIS progress | N/A (drag-to-install) | N/A |
| Completion | Launch checkbox + desktop shortcut | Eject + open Applications | Desktop entry created |
| Uninstaller | Start Menu entry + registry clean | Move to Trash | `AppImage --appimage-remove` |

### Auto-Update Integration

| Property | Value | Purpose |
|----------|-------|---------|
| `provider` | `generic` or `github` or `s3` | Update server type |
| `channel` | `latest` | Default update channel |
| `updaterCacheDirName` | `{appName}-updater` | Cache directory for downloaded updates |
| `autoDownload` | `true` | Download updates automatically |
| `autoInstallOnAppQuit` | `true` | Install pending updates on quit |
| `allowDowngrade` | `false` | Prevent version downgrade |
| `forceDevUpdate` | `false` | Use dev update URL in development |

### Package Verification Checklist

| Check | Windows | macOS | Linux | Blocking |
|-------|---------|-------|-------|----------|
| Installer launches without error | ✓ | ✓ | ✓ | yes |
| Silent install succeeds | `msiexec /i` | N/A | `dpkg -i` | yes |
| App launches post-install | ✓ | ✓ | ✓ | yes |
| Uninstall removes all files | ✓ | ✓ | ✓ | yes |
| Code signature valid | ✓ | ✓ | N/A | yes |
| Notarization complete | N/A | ✓ | N/A | yes |
| File associations registered | ✓ | ✓ | ✓ | no |
| Desktop shortcut created | ✓ | ✓ (DMG drag) | ✓ (.desktop) | no |
| Start Menu entry created | ✓ | ✓ (Applications) | N/A | no |
| Auto-update check passes | ✓ | ✓ | ✓ | yes |
| Package size within threshold | ✓ | ✓ | ✓ | yes |
| Native modules architecture-correct | x64/arm64 | x64/arm64 | x64 | yes |
```

## Examples

**Correct:**
> ### electron-builder Configuration
>
> | Property | Windows | macOS | Linux |
> |----------|---------|-------|-------|
> | `appId` | `com.example.myapp` | `com.example.myapp` | `com.example.myapp` |
> | `productName` | `My App` | `My App` | `My App` |
> | `outputDir` | `dist/win` | `dist/mac` | `dist/linux` |
> | `asar` | `true` | `true` | `true` |
> | `compression` | `maximum` | `maximum` | `maximum` |
>
> Windows: NSIS installer (`.exe`) with per-machine install, custom directory selection, and desktop shortcut. macOS: DMG with `@2x` background, drag-to-Applications layout, code signed + notarized. Linux: AppImage for universal compatibility, DEB for Debian/Ubuntu, RPM for Fedora.
>
> ### Code Signing
>
> | Platform | Signing Type | Certificate Source | Verification |
> |----------|-------------|-------------------|-------------|
> | Windows | Authenticode EV | `CSC_LINK` env (PFX) | `signtool verify /pa` |
> | macOS | Apple Developer ID | `CSC_LINK` (p12) | `codesign --verify --deep` |
> | macOS (notarization) | Apple Notarization | `APPLE_ID` + `APPLE_APP_SPECIFIC_PASSWORD` | `stapler validate` |

**Incorrect:**
> Package the app for Windows, Mac, and Linux. Use electron-builder with default settings. Sign the macOS build. Make sure the installer looks good.
> *Why wrong: packaging strategy must define per-platform format choices with explicit electron-builder configuration, code signing details with certificate sources and verification steps, installer customization (NSIS settings, DMG layout, Linux desktop integration), asset optimization targets, and a package verification checklist.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables, code blocks
- **Audience:** engineer
- **Do:** Define electron-builder configuration per platform with all critical properties; specify packaging formats with OS targets and file extensions; detail NSIS/DMG/Linux desktop customization; describe code signing with certificate sources and verification commands; list asset optimization targets; define installer design per platform; include auto-update integration config; provide a package verification checklist with blocking status
- **Don't:** Use default electron-builder settings without explicit configuration; omit platform-specific installer customization; skip code signing verification steps; leave asset optimization targets undefined; omit the package verification checklist

**Required subsections:** electron-builder Configuration, Platform Packaging, Code Signing, Package Verification Checklist
**Optional subsections:** NSIS Installer Customization, DMG Configuration, Linux Desktop Integration, Asset Optimization, Installer Design, Auto-Update Integration
**Required diagrams:** none
**Required cross-references:** Engineering(07), QA(12), Auto-Update section

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
