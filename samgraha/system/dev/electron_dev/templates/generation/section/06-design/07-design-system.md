# Desktop Design System — Generation Template

> **Domain:** design
> **Section:** desktop_design_system
> **Source:** `documentation-standards/06-design-standards.md` §Desktop Design System
> **Relationships:** `audit/deterministic/document/06-design-relationships.yaml`

Generate the Desktop Design System section for a Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / guiding_principles | Design System must embody the product's guiding philosophy through visual language and interaction patterns |
| `constrains` | feature-design / states | Design System defines the component states and transitions that Feature Design documents reference |
| `guided_by` | design / ux_principles | Design System implements the UX principles through concrete tokens, components, and patterns |

## Template

```markdown
## Desktop Design System

### Design Token Structure

[1 paragraph: how design tokens encode the visual language of the application — colors, typography, spacing, and motion — as a structured, themeable system]

#### Color Tokens

| Token Name | Light Value | Dark Value | Usage |
|-----------|-------------|------------|-------|
| `--color-bg-primary` | `[hex]` | `[hex]` | Main background surface |
| `--color-bg-secondary` | `[hex]` | `[hex]` | Sidebar, panel backgrounds |
| `--color-bg-tertiary` | `[hex]` | `[hex]` | Card, modal backgrounds |
| `--color-text-primary` | `[hex]` | `[hex]` | Headings, primary body text |
| `--color-text-secondary` | `[hex]` | `[hex]` | Captions, metadata, timestamps |
| `--color-text-disabled` | `[hex]` | `[hex]` | Inactive labels, placeholders |
| `--color-accent` | `[hex]` | `[hex]` | Primary action buttons, links |
| `--color-accent-hover` | `[hex]` | `[hex]` | Hover state of accent elements |
| `--color-border` | `[hex]` | `[hex]` | Dividers, input borders, card outlines |
| `--color-error` | `[hex]` | `[hex]` | Error messages, destructive actions |
| `--color-success` | `[hex]` | `[hex]` | Success feedback, positive states |
| `--color-warning` | `[hex]` | `[hex]` | Caution states, deprecation notices |

#### Typography Tokens

| Token Name | Value | Usage |
|-----------|-------|-------|
| `--font-family-sans` | `[font stack]` | Primary UI text |
| `--font-family-mono` | `[font stack]` | Code blocks, technical data |
| `--font-size-xs` | `[size]` | Captions, fine print |
| `--font-size-sm` | `[size]` | Secondary text, labels |
| `--font-size-base` | `[size]` | Body text, paragraphs |
| `--font-size-lg` | `[size]` | Section headings |
| `--font-size-xl` | `[size]` | Page titles |
| `--font-weight-normal` | `[weight]` | Regular body text |
| `--font-weight-semibold` | `[weight]` | Emphasis, labels |
| `--font-weight-bold` | `[weight]` | Headings |
| `--line-height` | `[value]` | Body text line height |

#### Spacing Tokens

| Token Name | Value | Usage |
|-----------|-------|-------|
| `--space-xs` | `[size]` | Tight gaps within components |
| `--space-sm` | `[size]` | Gap between related elements |
| `--space-md` | `[size]` | Standard padding, margins |
| `--space-lg` | `[size]` | Section separation |
| `--space-xl` | `[size]` | Page-level margins |

#### Motion Tokens

| Token Name | Value | Usage |
|-----------|-------|-------|
| `--duration-fast` | `[ms]` | Micro-interactions (hover, focus) |
| `--duration-normal` | `[ms]` | Panel transitions, dropdowns |
| `--duration-slow` | `[ms]` | Page transitions, modals |
| `--easing-default` | `[cubic-bezier]` | Standard easing |
| `--easing-enter` | `[cubic-bezier]` | Elements entering the viewport |
| `--easing-exit` | `[cubic-bezier]` | Elements leaving the viewport |

### Platform-Specific Styling

[1 paragraph: how the design system adapts to Windows, macOS, and Linux — respecting native conventions while maintaining brand consistency]

#### Native Chrome Integration

| Platform | Title Bar Style | Window Controls | Font Stack |
|---------|----------------|----------------|-----------|
| **Windows** | [standard / custom] | [minimize, maximize, close] | `[Segoe UI, ...]` |
| **macOS** | [standard / custom] | [close, minimize, maximize — traffic lights] | `[SF Pro, system-ui, ...]` |
| **Linux** | [standard / custom] | [minimize, maximize, close — varies by DE] | `[system-ui, ...]` |

#### Platform Adaptation Rules

| Rule | Description |
|------|-------------|
| **Window controls** | macOS traffic lights require left-side positioning; Windows/Linux controls are right-side |
| **Font rendering** | macOS uses subpixel antialiasing; Windows uses ClearType; Linux varies by toolkit |
| **Scroll behavior** | macOS scroll direction is "natural" by default; Windows/Linux use traditional scroll |
| **Context menus** | macOS uses Ctrl+Click for secondary click; Windows/Linux use right-click |
| **Keyboard shortcuts** | macOS uses Cmd; Windows/Linux use Ctrl — token system must map accordingly |

### Title Bar Customization

[1 paragraph: when and how to implement custom title bars vs. native title bars — tradeoffs between brand control and platform compliance]

#### Custom Title Bar Configuration

| Element | Behavior |
|---------|----------|
| **Drag region** | [-webkit-app-region: drag] applied to title bar area |
| **Double-click** | [toggle maximize on title bar double-click] |
| **Window controls overlay** | [macOS: traffic lights remain native; Windows: custom or native] |
| **Content below title bar** | [offset content by title bar height to prevent occlusion] |
| **Minimum height** | [title bar must meet minimum height for platform interaction targets] |

### Theme Switching

[1 paragraph: how themes are managed — light, dark, and system-preference modes — and how token values resolve at runtime]

#### Theme Modes

| Mode | Behavior | Token Resolution |
|------|----------|-----------------|
| **Light** | Forces light theme tokens | `[light values]` |
| **Dark** | Forces dark theme tokens | `[dark values]` |
| **System** | Follows OS preference via `prefers-color-scheme` media query | [dynamic resolution] |

#### Theme Application Mechanism

```
1. Configuration Service loads theme preference from Vault storage
2. CSS custom properties set on document root via [mechanism]
3. Token values cascade to all components via CSS inheritance
4. System preference change triggers token update without restart
5. Theme preference persists across app restarts
```

#### Theme-Aware Component Patterns

| Pattern | Implementation |
|---------|---------------|
| **SVG icons** | Use `currentColor` or theme-aware fill classes |
| **Shadows** | Define shadow tokens per theme — light uses subtle shadows, dark uses glow |
| **Borders** | Border color tokens adapt to theme — higher contrast in dark mode |
| **Images** | Provide light/dark variants or use CSS filters for theme adaptation |

### Accessibility in Desktop Context

[1 paragraph: how the design system addresses accessibility specific to desktop applications — native OS accessibility, keyboard navigation, and screen reader support]

#### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Move focus to next interactive element |
| `Shift+Tab` | Move focus to previous interactive element |
| `Enter` / `Space` | Activate focused button or link |
| `Escape` | Close modal, cancel operation, dismiss popup |
| `Arrow keys` | Navigate within lists, tabs, menus |
| `Cmd/Ctrl+K` | [global shortcut — command palette or search] |

#### Focus Management

| Rule | Description |
|------|-------------|
| **Visible focus ring** | All interactive elements must show a visible focus indicator — never `outline: none` without replacement |
| **Focus trapping** | Modal dialogs must trap focus — Tab cycles within the modal only |
| **Focus restoration** | When a modal closes, focus returns to the element that opened it |
| **Initial focus** | On window open or modal open, the primary action or first input receives focus |

#### Screen Reader Support

| Attribute | Usage |
|-----------|-------|
| `aria-label` | Label for icon-only buttons and controls |
| `aria-describedby` | Link form inputs to helper text or error messages |
| `aria-live` | Announce dynamic content changes (status updates, error messages) |
| `role` | Semantic roles for custom components (dialog, tablist, tree) |

#### Color and Contrast

| Criterion | Requirement |
|-----------|-------------|
| **Text contrast** | Minimum 4.5:1 ratio for normal text; 3:1 for large text |
| **Interactive contrast** | Minimum 3:1 for buttons, links, form controls against background |
| **Focus indicator** | Minimum 2:1 contrast against adjacent colors |
| **Error indication** | Never rely solely on color to convey error state — combine with icon or text |

### Component Library

[1 paragraph: the set of shared UI components that implement the design tokens — buttons, inputs, modals, navigation, data display]

| Component | Variants | States | Platform Behavior |
|-----------|----------|--------|-------------------|
| `[ComponentName]` | `[variant list]` | `[state list]` | `[platform-specific behavior]` |

### Design System Diagram

[Diagram showing token hierarchy, theme resolution, platform adaptation, and component rendering pipeline]
```

## Examples

**Correct:**
> **Color Token: --color-accent**
> - Light value: `#0066CC` — high-contrast blue for primary actions
> - Dark value: `#4DA3FF` — lighter blue compensating for dark background luminance
> - Usage: Primary action buttons, active tab indicators, selected sidebar items
> - Accessibility: Both values maintain ≥4.5:1 contrast ratio against their respective backgrounds
>
> **Platform Adaptation:**
> - Windows: Title bar uses native Windows chrome; custom content sits below the 32px title bar
> - macOS: Title bar uses native traffic lights; content uses `-webkit-app-region: drag` for the 28px bar area; `titleBarStyle: 'hiddenInset'` leaves traffic light space
> - Linux: Title bar follows GNOME/GTK conventions; fallback to standard chrome if detection fails

**Incorrect:**
> The design system uses CSS variables for theming. We have `--primary-color`, `--bg-color`, and `--text-color`. Dark mode changes these values. We use a React component library with buttons, inputs, and modals. Platform-specific styles use media queries.
> *Why wrong: describes implementation without design system structure — missing token hierarchy, platform adaptation rules, accessibility requirements, and theme resolution mechanism. CSS variables are implementation; design tokens are architectural decisions.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables and structured lists
- **Audience:** designer and frontend engineer
- **Do:** Define complete token hierarchy with light/dark values; specify platform-specific adaptation rules for Windows, macOS, and Linux; address accessibility requirements specific to desktop applications; document theme switching mechanism and persistence
- **Don't:** Use framework-specific syntax (React, Vue, Angular) in token definitions; skip platform-specific behavior — desktop design must address all three platforms; conflate design tokens with CSS implementation; omit accessibility requirements — they are mandatory, not optional

**Required subsections:** Design Token Structure, Platform-Specific Styling, Theme Switching, Accessibility in Desktop Context
**Optional subsections:** Title Bar Customization, Component Library, Motion System
**Required diagrams:** token hierarchy and theme resolution diagram
**Required cross-references:** Design Principles, UX Principles, Accessibility, Component Model (for UI component architecture)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
