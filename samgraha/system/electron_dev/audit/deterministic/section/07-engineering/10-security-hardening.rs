use serde::{Deserialize, Serialize};

/// Electron security hardening deterministic audit.
///
/// Validates defense-in-depth posture across every process boundary and
/// runtime surface. Electron applications embed a full Chromium browser
/// and Node.js runtime, creating a large attack surface where web content
/// meets native system access. This audit verifies that context isolation
/// is enforced, nodeIntegration is disabled, Content Security Policy (CSP)
/// is configured, code signing is implemented for all distributable
/// artifacts, the Chromium sandbox is active, and every IPC input is
/// validated and sanitized at the trust boundary.

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditMetadata {
    pub system_id: &'static str,
    pub domain: &'static str,
    pub section_type: &'static str,
    pub standard_id: &'static str,
    pub scope: &'static str,
    pub kind: &'static str,
}

impl AuditMetadata {
    pub const fn security_hardening() -> Self {
        Self {
            system_id: "electron_dev",
            domain: "engineering",
            section_type: "security_hardening",
            standard_id: "documentation-standards",
            scope: "section",
            kind: "deterministic",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditRule {
    pub id: &'static str,
    pub description: &'static str,
    pub condition: &'static str,
    pub message: &'static str,
    pub severity: Severity,
    pub weight: f64,
    pub mandatory: bool,
    pub evidence: Evidence,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Severity {
    Error,
    Warning,
    Info,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum Evidence {
    #[serde(rename = "section_presence")]
    SectionPresence { semantic_type: String },
    #[serde(rename = "subsection_presence")]
    SubsectionPresence { required: Vec<String> },
    #[serde(rename = "field_presence")]
    FieldPresence {
        per_entry: FieldPresenceConfig,
    },
    #[serde(rename = "keyword_absence")]
    KeywordAbsence { categories: Vec<String> },
    #[serde(rename = "content_check")]
    ContentCheck { keywords: Vec<String> },
    #[serde(rename = "cross_section_check")]
    CrossSectionCheck {
        requires_section: String,
        coverage: String,
    },
    #[serde(rename = "structural_check")]
    StructuralCheck {
        min_paragraphs: Option<usize>,
        min_diagrams: Option<usize>,
        required_subsections: Option<Vec<String>>,
    },
    #[serde(rename = "pattern_match")]
    PatternMatch {
        pattern: String,
        allowed_values: Option<Vec<String>>,
    },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FieldPresenceConfig {
    pub field: &'static str,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allowed_values: Option<Vec<&'static str>>,
}

// ---------------------------------------------------------------------------
// Rule definitions: context isolation and node integration
// ---------------------------------------------------------------------------

/// Rule: contextIsolation is enabled in all BrowserWindow and WebContents
/// configurations. No exceptions without documented justification and
/// compensating controls.
pub const RULE_CONTEXT_ISOLATION: AuditRule = AuditRule {
    id: "sec-hard-001",
    description: "contextIsolation is enabled in all BrowserWindow and WebContents configurations",
    condition: "all BrowserWindow creation sites set contextIsolation: true with no documented exceptions",
    message: "contextIsolation is not enabled in all BrowserWindow configurations",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "contextIsolation: true",
            "context isolation enabled",
            "all BrowserWindow",
        ],
    },
};

/// Rule: nodeIntegration is explicitly set to false in every web-creation
/// site. No exceptions without documented justification and compensating
/// controls.
pub const RULE_NO_NODE_INTEGRATION: AuditRule = AuditRule {
    id: "sec-hard-002",
    description: "nodeIntegration is explicitly set to false in every BrowserWindow",
    condition: "all BrowserWindow creation sites set nodeIntegration: false",
    message: "nodeIntegration is not disabled in all BrowserWindow configurations",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "nodeIntegration: false",
            "nodeIntegration disabled",
        ],
    },
};

/// Rule: nodeIntegrationInWorker is disabled unless a documented, justified
/// exception exists with compensating controls.
pub const RULE_NO_WORKER_NODE_INTEGRATION: AuditRule = AuditRule {
    id: "sec-hard-003",
    description: "nodeIntegrationInWorker is disabled unless documented exception with compensating controls exists",
    condition: "nodeIntegrationInWorker is set to false or any exception is documented with security justification",
    message: "nodeIntegrationInWorker is enabled without documented justification",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "nodeIntegrationInWorker: false",
            "worker node integration",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: Content Security Policy
// ---------------------------------------------------------------------------

/// Rule: CSP is defined with restrictive directives — no unsafe-inline
/// or unsafe-eval in script-src. CSP violations are reported via
/// report-uri or report-to.
pub const RULE_CSP_DEFINED: AuditRule = AuditRule {
    id: "sec-hard-004",
    description: "Content Security Policy is defined with restrictive directives and violation reporting",
    condition: "CSP configuration includes default-src, script-src without unsafe-inline/unsafe-eval, and report-uri or report-to",
    message: "Content Security Policy is not defined or contains unsafe directives",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "default-src",
            "script-src",
            "no unsafe-inline",
            "no unsafe-eval",
            "report-uri",
            "report-to",
        ],
    },
};

/// Rule: CSP directives include default-src, script-src, style-src, and
/// connect-src at minimum.
pub const RULE_CSP_MINIMUM_DIRECTIVES: AuditRule = AuditRule {
    id: "sec-hard-005",
    description: "CSP includes minimum directives: default-src, script-src, style-src, connect-src",
    condition: "CSP configuration defines at least default-src, script-src, style-src, and connect-src directives",
    message: "CSP is missing required minimum directives (default-src, script-src, style-src, connect-src)",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "default-src",
            "script-src",
            "style-src",
            "connect-src",
        ],
    },
};

/// Rule: CSP violations are logged and monitored — report-uri or report-to
/// directive is present.
pub const RULE_CSP_VIOLATION_REPORTING: AuditRule = AuditRule {
    id: "sec-hard-006",
    description: "CSP violations are logged via report-uri or report-to directive",
    condition: "CSP configuration includes a report-uri or report-to directive for violation monitoring",
    message: "CSP violation reporting is not configured",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "report-uri",
            "report-to",
            "CSP violations",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: code signing
// ---------------------------------------------------------------------------

/// Rule: Code signing is configured for all distributable targets (Windows
/// Authenticode, macOS codesign/notarize). Auto-update signature verification
/// is enforced.
pub const RULE_CODE_SIGNING: AuditRule = AuditRule {
    id: "sec-hard-007",
    description: "Code signing is configured for all distributable targets (Windows, macOS, auto-update)",
    condition: "code signing setup covers Windows Authenticode, macOS codesign/notarize, and update server signature verification",
    message: "Code signing is not configured for all distributable targets",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Windows Authenticode",
            "macOS codesign",
            "notarize",
            "auto-update signature",
        ],
    },
};

/// Rule: Code signing certificates are stored in secure key management
/// (CI secret / HSM), never in the repository filesystem.
pub const RULE_CERT_STORAGE: AuditRule = AuditRule {
    id: "sec-hard-008",
    description: "Code signing certificates stored in secure key management, never in repository",
    condition: "certificate storage references CI secrets, HSM, or keychain — no filesystem paths for certificate files",
    message: "Code signing certificates may be stored insecurely",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::KeywordAbsence {
        categories: vec![
            "certificate_file_path",
            "hardcoded_cert",
            "filesystem_cert_storage",
        ],
    },
};

/// Rule: Auto-update serves only signed packages — unsigned updates are
/// rejected.
pub const RULE_UPDATE_SIGNATURE_VERIFICATION: AuditRule = AuditRule {
    id: "sec-hard-009",
    description: "Auto-update enforces signature verification — unsigned updates rejected",
    condition: "auto-update configuration verifies code signature before applying update",
    message: "Auto-update does not enforce signature verification",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "signature verification",
            "unsigned update rejected",
            "verify signature",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: sandbox and web security
// ---------------------------------------------------------------------------

/// Rule: Chromium sandbox is enabled (sandbox: true). webSecurity is not
/// disabled. remote module is not used. DevTools are disabled in production.
pub const RULE_SANDBOX_ENABLED: AuditRule = AuditRule {
    id: "sec-hard-010",
    description: "Chromium sandbox enabled, webSecurity not disabled, remote module not used, DevTools disabled in production",
    condition: "BrowserWindow config has sandbox: true, webSecurity not false, no electron.remote, DevTools disabled in production",
    message: "Chromium sandbox or web security configuration is insufficient",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "sandbox: true",
            "webSecurity not disabled",
            "no electron.remote",
            "DevTools disabled",
        ],
    },
};

/// Rule: allowRunningInsecureContent is false — blocks HTTP-served scripts
/// in HTTPS contexts.
pub const RULE_NO_INSECURE_CONTENT: AuditRule = AuditRule {
    id: "sec-hard-011",
    description: "allowRunningInsecureContent is false in all BrowserWindow configurations",
    condition: "no BrowserWindow configuration sets allowRunningInsecureContent: true",
    message: "allowRunningInsecureContent is enabled in BrowserWindow configuration",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::KeywordAbsence {
        categories: vec![
            "allowRunningInsecureContent: true",
            "insecure content",
        ],
    },
};

/// Rule: webviewTag is disabled unless explicitly required and documented
/// with security review.
pub const RULE_WEBVIEW_DISABLED: AuditRule = AuditRule {
    id: "sec-hard-012",
    description: "webviewTag is disabled unless documented exception with security review exists",
    condition: "webviewTag is set to false or any exception has documented security justification",
    message: "webviewTag is enabled without documented security justification",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "webviewTag: false",
            "webview disabled",
            "webview exception",
        ],
    },
};

/// Rule: experimentalFeatures is false — Chrome experimental features
/// that bypass security checks are disabled.
pub const RULE_NO_EXPERIMENTAL_FEATURES: AuditRule = AuditRule {
    id: "sec-hard-013",
    description: "experimentalFeatures is false in all BrowserWindow configurations",
    condition: "no BrowserWindow configuration enables experimental Chrome features",
    message: "experimentalFeatures is enabled, potentially bypassing security checks",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::KeywordAbsence {
        categories: vec![
            "experimentalFeatures: true",
            "chrome experimental",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: IPC input validation
// ---------------------------------------------------------------------------

/// Rule: All IPC input is validated at the handler boundary. Payload schema
/// validation occurs before any business logic. Sender identity (webContents
/// ID) is verified for privileged channels.
pub const RULE_IPC_INPUT_VALIDATION: AuditRule = AuditRule {
    id: "sec-hard-014",
    description: "All IPC input validated at handler boundary with schema validation before business logic",
    condition: "IPC handlers validate payload type against schema before executing business logic",
    message: "IPC handlers accept payloads without schema validation",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "validate payload",
            "schema validation",
            "before business logic",
            "sender validation",
        ],
    },
};

/// Rule: IPC handlers validate channel names against an allowlist —
/// prevents arbitrary IPC channel invocation.
pub const RULE_CHANNEL_ALLOWLIST: AuditRule = AuditRule {
    id: "sec-hard-015",
    description: "IPC handlers validate channel names against an allowlist",
    condition: "IPC handler registration uses an allowlist pattern to reject unknown channels",
    message: "IPC handlers do not validate channel names against an allowlist",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "channel allowlist",
            "channel validation",
            "reject unknown channels",
        ],
    },
};

/// Rule: IPC validation rules cover strings (max length, character
/// whitelist, no control characters, no path traversal), paths (resolve
/// against allowed roots), numbers (min/max bounds), booleans (strict
/// type), and objects (allowlist keys, reject prototype pollution).
pub const RULE_IPC_VALIDATION_COVERAGE: AuditRule = AuditRule {
    id: "sec-hard-016",
    description: "IPC validation covers strings, paths, numbers, booleans, and objects with type-specific rules",
    condition: "validation rules define checks for all five data types (string, path, number, boolean, object)",
    message: "IPC validation does not cover all required data types",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "string validation",
            "path traversal",
            "number bounds",
            "boolean type check",
            "prototype pollution",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: process privilege restrictions
// ---------------------------------------------------------------------------

/// Rule: Process privilege table defines filesystem, network, IPC scope,
/// and native module access for Main, Preload, and Renderer.
pub const RULE_PRIVILEGE_TABLE: AuditRule = AuditRule {
    id: "sec-hard-017",
    description: "Process privilege restrictions table covers filesystem, network, IPC scope, native modules for all processes",
    condition: "privilege restrictions table defines access levels for Main, Preload, and Renderer across all four dimensions",
    message: "Process privilege restrictions are not fully documented for all processes",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "filesystem",
            "network",
            "IPC scope",
            "native modules",
            "Main",
            "Preload",
            "Renderer",
        ],
    },
};

/// Rule: Privilege escalation prevention is documented — Renderer must
/// never receive ipcRenderer, Preload must not re-expose ipcRenderer
/// directly, Main must not forward raw input.
pub const RULE_ESCALATION_PREVENTION: AuditRule = AuditRule {
    id: "sec-hard-018",
    description: "Privilege escalation prevention rules documented for all process boundaries",
    condition: "document defines rules preventing Renderer from accessing ipcRenderer directly, Preload from re-exposing raw IPC, and Main from forwarding unvalidated input",
    message: "Privilege escalation prevention rules are not documented",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Renderer must never receive ipcRenderer",
            "Preload must not re-expose",
            "Main must not forward raw",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: preload API surface
// ---------------------------------------------------------------------------

/// Rule: Preload scripts expose minimum API surface via contextBridge.
/// Permission requests default to deny. Session cookie attributes
/// (secure, httpOnly, sameSite) are configured.
pub const RULE_PRELOAD_MINIMAL_SURFACE: AuditRule = AuditRule {
    id: "sec-hard-019",
    description: "Preload scripts expose minimum API surface via contextBridge with permission-deny defaults",
    condition: "preload configuration shows minimal API surface, permission deny defaults, and secure cookie attributes",
    message: "Preload scripts expose excessive API surface or lack security defaults",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "minimum API surface",
            "contextBridge",
            "permission deny",
            "secure cookie",
            "httpOnly",
            "sameSite",
        ],
    },
};

/// Rule: Navigation and new-window events are restricted to trusted origins
/// only — no arbitrary URL navigation.
pub const RULE_NAVIGATION_RESTRICTION: AuditRule = AuditRule {
    id: "sec-hard-020",
    description: "Navigation and new-window events restricted to trusted origins",
    condition: "navigation event handlers validate target URLs against a trusted origin allowlist",
    message: "Navigation events are not restricted to trusted origins",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "trusted origins",
            "navigation restriction",
            "new-window validation",
            "origin allowlist",
        ],
    },
};

/// Rule: Permissions API, clipboard, notifications, and media access are
/// restricted per origin via session.setPermissionRequestHandler.
pub const RULE_PERMISSION_RESTRICTIONS: AuditRule = AuditRule {
    id: "sec-hard-021",
    description: "Permissions API, clipboard, notifications, and media access restricted per origin",
    condition: "session.setPermissionRequestHandler is configured to restrict camera, microphone, notifications, clipboard per origin",
    message: "Permission requests are not restricted per origin",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "setPermissionRequestHandler",
            "camera",
            "microphone",
            "notifications",
            "clipboard",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: auto-update security
// ---------------------------------------------------------------------------

/// Rule: Auto-update server uses HTTPS-only — no HTTP fallback.
pub const RULE_UPDATE_HTTPS_ONLY: AuditRule = AuditRule {
    id: "sec-hard-022",
    description: "Auto-update server uses HTTPS-only with no HTTP fallback",
    condition: "update server URL uses https:// protocol with no http:// alternative",
    message: "Auto-update server allows HTTP or has HTTP fallback",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::KeywordAbsence {
        categories: vec![
            "http://update",
            "http fallback",
        ],
    },
};

/// Rule: Auto-update includes staged rollouts (5% -> 25% -> 100%) with
/// 24-hour soak between stages.
pub const RULE_STAGED_ROLLOUTS: AuditRule = AuditRule {
    id: "sec-hard-023",
    description: "Auto-update includes staged rollouts with soak period between stages",
    condition: "update strategy defines staged rollout percentages with time-based soak between stages",
    message: "Auto-update does not use staged rollouts",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "staged rollout",
            "soak period",
            "5%",
            "25%",
            "100%",
        ],
    },
};

/// Rule: SHA-256 integrity checks verify downloaded update packages.
pub const RULE_UPDATE_INTEGRITY: AuditRule = AuditRule {
    id: "sec-hard-024",
    description: "SHA-256 integrity verification of downloaded update packages",
    condition: "auto-update process includes hash verification of downloaded packages before applying",
    message: "Auto-update does not verify package integrity",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "SHA-256",
            "hash verification",
            "integrity check",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: native modules and dependencies
// ---------------------------------------------------------------------------

/// Rule: Native module usage is audited — only necessary native addons
/// with up-to-date binaries are loaded.
pub const RULE_NATIVE_MODULE_AUDIT: AuditRule = AuditRule {
    id: "sec-hard-025",
    description: "Native module usage is audited with only necessary, up-to-date addons",
    condition: "native module list exists with security justification and binary freshness verification",
    message: "Native module usage is not audited for security",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "native module audit",
            "up-to-date binaries",
            "security justification",
        ],
    },
};

/// Rule: Dependency vulnerability scanning covers both npm and native addon
/// dependencies. Known CVEs are tracked and resolved.
pub const RULE_DEPENDENCY_SCANNING: AuditRule = AuditRule {
    id: "sec-hard-026",
    description: "Dependency vulnerability scanning covers npm packages and native addons",
    condition: "dependency scanning process covers both npm and native dependencies with CVE tracking",
    message: "Dependency vulnerability scanning does not cover all dependency types",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "npm audit",
            "native addon scan",
            "CVE tracking",
            "known vulnerabilities",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: security audit checklist
// ---------------------------------------------------------------------------

/// Rule: Security configuration is centralized in a hardening module, not
/// scattered across files.
pub const RULE_CENTRALIZED_SECURITY: AuditRule = AuditRule {
    id: "sec-hard-027",
    description: "Security configuration centralized in a hardening module",
    condition: "security settings are defined in a single hardening module or configuration file",
    message: "Security configuration is scattered across multiple files",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "hardening module",
            "centralized security",
            "single configuration",
        ],
    },
};

/// Rule: No hardcoded secrets, tokens, or credentials in source code.
pub const RULE_NO_HARDCODED_SECRETS: AuditRule = AuditRule {
    id: "sec-hard-028",
    description: "No hardcoded secrets, tokens, or credentials in source code",
    condition: "no API keys, tokens, passwords, or secrets are embedded in source files",
    message: "Hardcoded secrets detected in source code",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::KeywordAbsence {
        categories: vec![
            "hardcoded_api_key",
            "hardcoded_token",
            "hardcoded_password",
            "embedded_secret",
        ],
    },
};

/// Rule: Crash reporter does not send sensitive user data.
pub const RULE_CRASH_REPORTER_PRIVACY: AuditRule = AuditRule {
    id: "sec-hard-029",
    description: "Crash reporter does not send sensitive user data",
    condition: "crash reporter configuration excludes PII, credentials, and file contents from reports",
    message: "Crash reporter may transmit sensitive user data",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "crash reporter",
            "no PII",
            "exclude sensitive",
            "privacy-safe",
        ],
    },
};

/// Rule: shell.openExternal is called only with validated URLs — prevents
/// renderer from navigating to arbitrary URLs.
pub const RULE_OPEN_EXTERNAL_VALIDATION: AuditRule = AuditRule {
    id: "sec-hard-030",
    description: "shell.openExternal called only with validated URLs",
    condition: "all shell.openExternal calls validate URLs against a scheme and domain allowlist",
    message: "shell.openExternal may accept unvalidated URLs",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "shell.openExternal",
            "URL validation",
            "scheme allowlist",
        ],
    },
};

/// Rule: DevTools are disabled or restricted in production builds.
pub const RULE_DEVTOOLS_DISABLED: AuditRule = AuditRule {
    id: "sec-hard-031",
    description: "DevTools disabled or restricted in production builds",
    condition: "DevTools are gated behind development-only condition or disabled in production configuration",
    message: "DevTools are accessible in production builds",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "DevTools disabled",
            "production build",
            "development only",
        ],
    },
};

// ---------------------------------------------------------------------------
// Full audit rule set
// ---------------------------------------------------------------------------

pub fn all_rules() -> Vec<&'static AuditRule> {
    vec![
        &RULE_CONTEXT_ISOLATION,
        &RULE_NO_NODE_INTEGRATION,
        &RULE_NO_WORKER_NODE_INTEGRATION,
        &RULE_CSP_DEFINED,
        &RULE_CSP_MINIMUM_DIRECTIVES,
        &RULE_CSP_VIOLATION_REPORTING,
        &RULE_CODE_SIGNING,
        &RULE_CERT_STORAGE,
        &RULE_UPDATE_SIGNATURE_VERIFICATION,
        &RULE_SANDBOX_ENABLED,
        &RULE_NO_INSECURE_CONTENT,
        &RULE_WEBVIEW_DISABLED,
        &RULE_NO_EXPERIMENTAL_FEATURES,
        &RULE_IPC_INPUT_VALIDATION,
        &RULE_CHANNEL_ALLOWLIST,
        &RULE_IPC_VALIDATION_COVERAGE,
        &RULE_PRIVILEGE_TABLE,
        &RULE_ESCALATION_PREVENTION,
        &RULE_PRELOAD_MINIMAL_SURFACE,
        &RULE_NAVIGATION_RESTRICTION,
        &RULE_PERMISSION_RESTRICTIONS,
        &RULE_UPDATE_HTTPS_ONLY,
        &RULE_STAGED_ROLLOUTS,
        &RULE_UPDATE_INTEGRITY,
        &RULE_NATIVE_MODULE_AUDIT,
        &RULE_DEPENDENCY_SCANNING,
        &RULE_CENTRALIZED_SECURITY,
        &RULE_NO_HARDCODED_SECRETS,
        &RULE_CRASH_REPORTER_PRIVACY,
        &RULE_OPEN_EXTERNAL_VALIDATION,
        &RULE_DEVTOOLS_DISABLED,
    ]
}

pub fn mandatory_rules() -> Vec<&'static AuditRule> {
    all_rules().into_iter().filter(|r| r.mandatory).collect()
}

pub fn recommended_rules() -> Vec<&'static AuditRule> {
    all_rules()
        .into_iter()
        .filter(|r| !r.mandatory)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn all_rules_have_unique_ids() {
        let rules = all_rules();
        let mut ids: Vec<&str> = rules.iter().map(|r| r.id).collect();
        ids.sort();
        ids.dedup();
        assert_eq!(ids.len(), rules.len(), "duplicate rule IDs found");
    }

    #[test]
    fn mandatory_rules_are_error_severity() {
        for rule in mandatory_rules() {
            assert!(
                matches!(rule.severity, Severity::Error),
                "mandatory rule {} must have error severity",
                rule.id
            );
        }
    }

    #[test]
    fn weights_are_positive() {
        for rule in all_rules() {
            assert!(rule.weight > 0.0, "rule {} has non-positive weight", rule.id);
        }
    }

    #[test]
    fn metadata_is_correct() {
        let meta = AuditMetadata::security_hardening();
        assert_eq!(meta.system_id, "electron_dev");
        assert_eq!(meta.domain, "engineering");
        assert_eq!(meta.section_type, "security_hardening");
        assert_eq!(meta.kind, "deterministic");
    }

    #[test]
    fn serde_roundtrip() {
        let rule = &RULE_CONTEXT_ISOLATION;
        let json = serde_json::to_string(rule).expect("serialize");
        let deserialized: AuditRule = serde_json::from_str(&json).expect("deserialize");
        assert_eq!(deserialized.id, rule.id);
    }
}
