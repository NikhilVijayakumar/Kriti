use serde::{Deserialize, Serialize};

/// IPC Testing Determinist — validates mock transport, handler tests, integration tests
/// for desktop application IPC layer (Main ↔ Renderer ↔ Preload via contextBridge).
///
/// System: electron_dev
/// Domain: qa
/// Section: ipc_testing

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IpcTestingDeterminist {
    pub meta: DeterministMeta,
    pub rules: Vec<AuditRule>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeterministMeta {
    pub system_id: &'static str,
    pub domain: &'static str,
    pub section_type: &'static str,
    pub standard_id: &'static str,
    pub scope: &'static str,
    pub kind: &'static str,
}

impl Default for DeterministMeta {
    fn default() -> Self {
        Self {
            system_id: "samgraha-documentation",
            domain: "qa",
            section_type: "ipc_testing",
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
pub enum Severity {
    Error,
    Warning,
    Info,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Evidence {
    SectionPresence {
        semantic_type: &'static str,
    },
    ContentCheck {
        min_length: Option<usize>,
        keywords: Option<Vec<&'static str>>,
        patterns: Option<Vec<&'static str>>,
    },
    CrossReference {
        expected: Vec<CrossRef>,
    },
    StructureCheck {
        required_fields: Vec<&'static str>,
        required_subsections: Vec<&'static str>,
    },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CrossRef {
    pub domain: &'static str,
    pub direction: &'static str,
}

// ─── Validation Rules ───────────────────────────────────────────────────────

pub fn build_rules() -> Vec<AuditRule> {
    vec![
        // ── Section Presence ──
        AuditRule {
            id: "qa-sec-ipc_testing-001",
            description: "IPC Testing section exists",
            condition: "document has a section with semantic_type = 'ipc_testing'",
            message: "Missing required 'IPC Testing' section",
            severity: Severity::Error,
            weight: 1.5,
            mandatory: true,
            evidence: Evidence::SectionPresence {
                semantic_type: "ipc_testing",
            },
        },
        // ── Mock Transport Validation ──
        AuditRule {
            id: "qa-sec-ipc_testing-002",
            description: "IPC mock transport layer is defined",
            condition: "section defines a mock or fake IPC transport for unit-testing handlers without a live Electron runtime",
            message: "IPC testing section does not define a mock transport layer",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "mock",
                    "fake",
                    "stub",
                    "transport",
                    "ipc",
                    "channel",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-003",
            description: "Mock transport covers all three process contexts",
            condition: "mock transport supports Main process senders, Renderer process receivers, and Preload bridge proxies",
            message: "Mock transport does not cover Main/Renderer/Preload process contexts",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "main",
                    "renderer",
                    "preload",
                    "contextBridge",
                    "process",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-004",
            description: "Mock transport validates channel naming conventions",
            condition: "mock transport enforces channel naming patterns (e.g. domain:action format) and rejects unregistered channels",
            message: "Mock transport does not validate channel naming conventions",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "channel",
                    "naming",
                    "pattern",
                    "convention",
                    "register",
                    "reject",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-005",
            description: "Mock transport simulates serialization roundtrip",
            condition: "mock transport applies JSON serialization/deserialization to messages to catch structured-clone incompatibilities",
            message: "Mock transport does not simulate serialization roundtrip",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "serialize",
                    "deserialize",
                    "json",
                    "structured-clone",
                    "roundtrip",
                    "serialization",
                ]),
                patterns: None,
            },
        },
        // ── Handler Tests ──
        AuditRule {
            id: "qa-sec-ipc_testing-006",
            description: "IPC handler tests exist for every registered channel",
            condition: "each ipcMain.handle / ipcMain.on handler has at least one corresponding test that invokes it via the mock transport",
            message: "IPC handler tests do not cover all registered channels",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "handler",
                    "ipcMain",
                    "handle",
                    "on",
                    "channel",
                    "registered",
                    "coverage",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-007",
            description: "Handler tests validate input sanitization",
            condition: "tests verify that handlers reject or sanitize malformed, missing, or type-incorrect arguments from Renderer processes",
            message: "Handler tests do not validate input sanitization",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "sanitize",
                    "validate",
                    "malformed",
                    "input",
                    "type",
                    "reject",
                    "argument",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-008",
            description: "Handler tests validate error propagation",
            condition: "tests verify that handler errors are caught, wrapped, and propagated back to the Renderer process with a consistent error shape",
            message: "Handler tests do not validate error propagation across process boundary",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "error",
                    "propagation",
                    "catch",
                    "wrap",
                    "ipcRenderer",
                    "reject",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-009",
            description: "Handler tests validate async completion",
            condition: "tests verify that async handlers resolve or reject within a defined timeout and do not leave dangling promises",
            message: "Handler tests do not validate async completion or timeout behavior",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "async",
                    "await",
                    "timeout",
                    "promise",
                    "resolve",
                    "reject",
                    "completion",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-010",
            description: "Handler tests validate permission checks",
            condition: "tests verify that handlers enforce sender permission checks (webContents id validation, origin checks) before processing",
            message: "Handler tests do not validate sender permission checks",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "permission",
                    "sender",
                    "webContents",
                    "origin",
                    "authorize",
                    "check",
                ]),
                patterns: None,
            },
        },
        // ── contextBridge Integration Tests ──
        AuditRule {
            id: "qa-sec-ipc_testing-011",
            description: "contextBridge exposure tests exist",
            condition: "tests verify that preload scripts expose exactly the intended API surface through contextBridge.exposeInMainWorld",
            message: "contextBridge exposure tests are missing",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "contextBridge",
                    "exposeInMainWorld",
                    "preload",
                    "api",
                    "exposure",
                    "surface",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-012",
            description: "contextBridge tests validate API surface lockdown",
            condition: "tests verify that the exposed API does not leak internal Node.js modules, Electron internals, or prototype chain access",
            message: "contextBridge tests do not validate API surface lockdown",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "lockdown",
                    "leak",
                    "node",
                    "electron",
                    "internal",
                    "prototype",
                    "forbidden",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-013",
            description: "contextBridge tests validate argument cloning",
            condition: "tests verify that objects passed through contextBridge are deep-cloned and do not carry references to Renderer-side state",
            message: "contextBridge tests do not validate argument cloning behavior",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "clone",
                    "deep",
                    "structured-clone",
                    "reference",
                    "argument",
                    "copy",
                ]),
                patterns: None,
            },
        },
        // ── Service Registry & Channel Naming ──
        AuditRule {
            id: "qa-sec-ipc_testing-014",
            description: "Channel registry tests verify all declared channels",
            condition: "tests confirm that every channel in the service registry has a corresponding handler and every handler has a registered channel",
            message: "Channel registry tests do not verify bidirectional handler-channel mapping",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "registry",
                    "channel",
                    "handler",
                    "bidirectional",
                    "mapping",
                    "declare",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-015",
            description: "Channel naming convention tests enforce format",
            condition: "tests verify that all channels follow the project naming convention (e.g. domain:entity:action) and reject non-conforming names",
            message: "Channel naming convention tests are missing or incomplete",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "naming",
                    "convention",
                    "format",
                    "domain",
                    "action",
                    "conform",
                ]),
                patterns: None,
            },
        },
        // ── IPC Serialization & Data Integrity ──
        AuditRule {
            id: "qa-sec-ipc_testing-016",
            description: "IPC payload serialization tests exist",
            condition: "tests verify that complex payloads (Date, Map, Set, ArrayBuffer, typed arrays) survive the IPC serialization boundary without data loss",
            message: "IPC payload serialization tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "payload",
                    "serialization",
                    "Date",
                    "Map",
                    "ArrayBuffer",
                    "typed",
                    "data loss",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-017",
            description: "IPC large payload tests exist",
            condition: "tests verify that large payloads (multi-MB) transfer correctly without truncation or memory issues",
            message: "IPC large payload tests are missing",
            severity: Severity::Warning,
            weight: 0.6,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "large",
                    "payload",
                    "multi-mb",
                    "truncation",
                    "memory",
                    "transfer",
                ]),
                patterns: None,
            },
        },
        // ── Process Isolation Tests ──
        AuditRule {
            id: "qa-sec-ipc_testing-018",
            description: "Process isolation tests verify sandbox boundaries",
            condition: "tests confirm that Renderer process code cannot access Main process modules, filesystem, or native APIs outside the approved IPC surface",
            message: "Process isolation tests are missing or incomplete",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "isolation",
                    "sandbox",
                    "renderer",
                    "main",
                    "filesystem",
                    "native",
                    "boundary",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-019",
            description: "Preload script tests verify execution context",
            condition: "tests verify that preload scripts execute in the correct context with access to both Node.js APIs and theRenderer DOM",
            message: "Preload script execution context tests are missing",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "preload",
                    "context",
                    "node",
                    "dom",
                    "execution",
                    "sandbox",
                ]),
                patterns: None,
            },
        },
        // ── Event System Tests ──
        AuditRule {
            id: "qa-sec-ipc_testing-020",
            description: "IPC event subscription and unsubscription tests exist",
            condition: "tests verify that listeners can be registered and removed without leaking, and that removed listeners do not fire on subsequent messages",
            message: "IPC event subscription lifecycle tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "subscribe",
                    "unsubscribe",
                    "listener",
                    "remove",
                    "leak",
                    "event",
                    "lifecycle",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-021",
            description: "IPC broadcast and targeted send tests exist",
            condition: "tests verify that broadcast sends reach all Renderer windows and targeted sends reach only the specified webContents",
            message: "IPC broadcast vs targeted send tests are missing",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "broadcast",
                    "targeted",
                    "send",
                    "webContents",
                    "window",
                    "recipient",
                ]),
                patterns: None,
            },
        },
        // ── Background Job IPC Tests ──
        AuditRule {
            id: "qa-sec-ipc_testing-022",
            description: "Background job IPC tests exist",
            condition: "tests verify that background jobs (workers, utility processes) can communicate with the Main process via IPC and that results propagate to the Renderer",
            message: "Background job IPC tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "background",
                    "job",
                    "worker",
                    "utility",
                    "process",
                    "ipc",
                    "result",
                ]),
                patterns: None,
            },
        },
        // ── Configuration Lock Tests ──
        AuditRule {
            id: "qa-sec-ipc_testing-023",
            description: "Configuration lock IPC tests exist",
            condition: "tests verify that configuration mutations through IPC are serialized and do not produce race conditions when multiple Renderer windows write concurrently",
            message: "Configuration lock IPC tests are missing",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "configuration",
                    "lock",
                    "race",
                    "concurrent",
                    "serialize",
                    "mutation",
                ]),
                patterns: None,
            },
        },
        // ── Storage Domain Tests ──
        AuditRule {
            id: "qa-sec-ipc_testing-024",
            description: "Storage domain isolation tests exist",
            condition: "tests verify that IPC handlers enforce storage domain boundaries and prevent cross-domain data access",
            message: "Storage domain isolation IPC tests are missing",
            severity: Severity::Error,
            weight: 1.0,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "storage",
                    "domain",
                    "isolation",
                    "boundary",
                    "cross-domain",
                    "access",
                ]),
                patterns: None,
            },
        },
        // ── Cross-Reference Tests ──
        AuditRule {
            id: "qa-sec-ipc_testing-025",
            description: "IPC tests reference Architecture Documentation",
            condition: "section references Architecture Documentation communication paths and process model",
            message: "IPC tests do not reference Architecture Documentation",
            severity: Severity::Warning,
            weight: 0.5,
            mandatory: false,
            evidence: Evidence::CrossReference {
                expected: vec![CrossRef {
                    domain: "architecture",
                    direction: "derives_from",
                }],
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-026",
            description: "IPC tests reference Security Documentation",
            condition: "section references Security Documentation IPC threat model and process isolation requirements",
            message: "IPC tests do not reference Security Documentation",
            severity: Severity::Warning,
            weight: 0.5,
            mandatory: false,
            evidence: Evidence::CrossReference {
                expected: vec![CrossRef {
                    domain: "security",
                    direction: "derives_from",
                }],
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-027",
            description: "IPC tests reference Engineering Documentation",
            condition: "section references Engineering Documentation IPC channel standards and service registry conventions",
            message: "IPC tests do not reference Engineering Documentation",
            severity: Severity::Warning,
            weight: 0.5,
            mandatory: false,
            evidence: Evidence::CrossReference {
                expected: vec![CrossRef {
                    domain: "engineering",
                    direction: "derives_from",
                }],
            },
        },
        AuditRule {
            id: "qa-sec-ipc_testing-028",
            description: "IPC tests reference Feature Technical Documentation",
            condition: "section references Feature Technical Documentation component responsibilities for IPC-exposed services",
            message: "IPC tests do not reference Feature Technical Documentation",
            severity: Severity::Warning,
            weight: 0.5,
            mandatory: false,
            evidence: Evidence::CrossReference {
                expected: vec![CrossRef {
                    domain: "feature-technical",
                    direction: "derives_from",
                }],
            },
        },
    ]
}

// ─── Validation Engine ──────────────────────────────────────────────────────

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ValidationReport {
    pub total_rules: usize,
    pub passed: usize,
    pub warnings: usize,
    pub errors: usize,
    pub findings: Vec<Finding>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Finding {
    pub rule_id: String,
    pub severity: Severity,
    pub message: String,
    pub evidence_type: &'static str,
}

pub fn validate(doc_content: &str) -> ValidationReport {
    let rules = build_rules();
    let mut findings = Vec::new();
    let mut passed = 0usize;
    let mut warnings = 0usize;
    let mut errors = 0usize;

    for rule in &rules {
        let result = evaluate_rule(rule, doc_content);
        match result {
            RuleResult::Pass => {
                passed += 1;
            }
            RuleResult::Fail(msg) => {
                match rule.severity {
                    Severity::Error => errors += 1,
                    Severity::Warning => warnings += 1,
                    Severity::Info => {}
                }
                findings.push(Finding {
                    rule_id: rule.id.to_string(),
                    severity: rule.severity.clone(),
                    message: msg,
                    evidence_type: match &rule.evidence {
                        Evidence::SectionPresence { .. } => "section_presence",
                        Evidence::ContentCheck { .. } => "content_check",
                        Evidence::CrossReference { .. } => "cross_reference",
                        Evidence::StructureCheck { .. } => "structure_check",
                    },
                });
            }
        }
    }

    ValidationReport {
        total_rules: rules.len(),
        passed,
        warnings,
        errors,
        findings,
    }
}

enum RuleResult {
    Pass,
    Fail(String),
}

fn evaluate_rule(rule: &AuditRule, content: &str) -> RuleResult {
    match &rule.evidence {
        Evidence::SectionPresence { semantic_type } => {
            let heading_variants = vec![
                format!("## {}", sanitize_heading(semantic_type)),
                format!("### {}", sanitize_heading(semantic_type)),
                semantic_type.replace('_', " "),
            ];
            let found = heading_variants
                .iter()
                .any(|v| content.to_lowercase().contains(&v.to_lowercase()));
            if found {
                RuleResult::Pass
            } else {
                RuleResult::Fail(rule.message.to_string())
            }
        }
        Evidence::ContentCheck {
            min_length,
            keywords,
            patterns,
        } => {
            if let Some(min) = min_length {
                if content.len() < *min {
                    return RuleResult::Fail(rule.message.to_string());
                }
            }
            if let Some(kws) = keywords {
                let content_lower = content.to_lowercase();
                let keyword_hits = kws
                    .iter()
                    .filter(|kw| content_lower.contains(&kw.to_lowercase()))
                    .count();
                if keyword_hits == 0 {
                    return RuleResult::Fail(rule.message.to_string());
                }
            }
            if let Some(pats) = patterns {
                let content_lower = content.to_lowercase();
                let pattern_hits = pats
                    .iter()
                    .filter(|p| content_lower.contains(&p.to_lowercase()))
                    .count();
                if pattern_hits == 0 {
                    return RuleResult::Fail(rule.message.to_string());
                }
            }
            RuleResult::Pass
        }
        Evidence::CrossReference { expected } => {
            for cross_ref in expected {
                let ref_lower = cross_ref.domain.to_lowercase();
                if !content.to_lowercase().contains(&ref_lower) {
                    return RuleResult::Fail(rule.message.to_string());
                }
            }
            RuleResult::Pass
        }
        Evidence::StructureCheck {
            required_fields,
            required_subsections,
        } => {
            let content_lower = content.to_lowercase();
            for field in required_fields {
                if !content_lower.contains(&field.to_lowercase()) {
                    return RuleResult::Fail(rule.message.to_string());
                }
            }
            for sub in required_subsections {
                if !content_lower.contains(&sub.to_lowercase()) {
                    return RuleResult::Fail(rule.message.to_string());
                }
            }
            RuleResult::Pass
        }
    }
}

fn sanitize_heading(semantic_type: &str) -> String {
    semantic_type
        .replace('_', " ")
        .split(' ')
        .map(|word| {
            let mut chars = word.chars();
            match chars.next() {
                None => String::new(),
                Some(c) => {
                    let upper: String = c.to_uppercase().collect();
                    upper + &chars.as_str().to_lowercase()
                }
            }
        })
        .collect::<Vec<_>>()
        .join(" ")
}

// ─── Tests ──────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rule_count_matches_spec() {
        let rules = build_rules();
        assert!(rules.len() >= 28, "Expected at least 28 rules, got {}", rules.len());
    }

    #[test]
    fn all_rule_ids_are_unique() {
        let rules = build_rules();
        let mut ids: Vec<&str> = rules.iter().map(|r| r.id).collect();
        ids.sort();
        ids.dedup();
        assert_eq!(ids.len(), rules.len(), "Duplicate rule IDs found");
    }

    #[test]
    fn mandatory_rules_have_error_severity() {
        let rules = build_rules();
        for rule in &rules {
            if rule.mandatory {
                assert!(
                    matches!(rule.severity, Severity::Error),
                    "Rule {} is mandatory but severity is not Error",
                    rule.id
                );
            }
        }
    }

    #[test]
    fn weights_are_bounded() {
        let rules = build_rules();
        for rule in &rules {
            assert!(
                rule.weight > 0.0 && rule.weight <= 2.0,
                "Rule {} has out-of-bounds weight: {}",
                rule.id,
                rule.weight
            );
        }
    }

    #[test]
    fn validate_empty_doc_fails_all() {
        let report = validate("");
        assert!(report.errors > 0, "Empty doc should produce errors");
        assert_eq!(report.passed, 0, "Empty doc should pass no rules");
    }

    #[test]
    fn validate_comprehensive_doc_passes_section_presence() {
        let doc = r#"
## IPC Testing

This section defines the IPC testing strategy for the desktop application.

### Mock Transport

A mock IPC transport layer is implemented to enable unit testing of IPC handlers
without requiring a live Electron runtime. The mock transport supports all three
process contexts: Main process senders, Renderer process receivers, and Preload
bridge proxies via contextBridge.exposeInMainWorld.

The mock transport validates channel naming conventions using the domain:entity:action
pattern and rejects unregistered channels. It applies JSON serialization/deserialization
roundtrip to catch structured-clone incompatibilities in complex payloads.

### Handler Tests

Every registered ipcMain.handle and ipcMain.on handler has a corresponding test
that invokes it via the mock transport. Tests validate input sanitization by
supplying malformed, missing, and type-incorrect arguments. Error propagation is
verified by confirming that handler errors are caught, wrapped, and propagated
back to the Renderer process with a consistent error shape.

Async handlers are tested for resolution and rejection within defined timeouts.
Sender permission checks are validated by verifying webContents id validation
and origin checks before processing.

### contextBridge Integration Tests

Preload scripts are tested to verify that contextBridge.exposeInMainWorld exposes
exactly the intended API surface. Tests confirm that the exposed API does not leak
internal Node.js modules, Electron internals, or prototype chain access. Argument
cloning through contextBridge is validated to ensure objects are deep-cloned and
do not carry references to Renderer-side state.

### Channel Registry Tests

The service registry is tested for bidirectional handler-channel mapping. Every
channel in the registry has a corresponding handler and every handler has a
registered channel. Channel naming convention tests enforce the domain:entity:action
format and reject non-conforming names.

### Serialization Tests

IPC payload serialization tests verify that complex payloads including Date, Map,
Set, ArrayBuffer, and typed arrays survive the IPC serialization boundary without
data loss. Large payload tests verify multi-MB transfers without truncation or
memory issues.

### Process Isolation Tests

Process isolation tests confirm that Renderer process code cannot access Main
process modules, filesystem, or native APIs outside the approved IPC surface.
Preload script execution context is tested to verify correct context with access
to both Node.js APIs and the Renderer DOM.

### Event System Tests

IPC event subscription and unsubscription lifecycle tests verify that listeners
can be registered and removed without leaking. Broadcast vs targeted send tests
verify that broadcasts reach all Renderer windows and targeted sends reach only
the specified webContents.

### Background Job IPC Tests

Background job IPC tests verify that workers and utility processes can communicate
with the Main process via IPC and that results propagate to the Renderer.

### Configuration Lock Tests

Configuration lock IPC tests verify that configuration mutations through IPC are
serialized and do not produce race conditions when multiple Renderer windows write
concurrently.

### Storage Domain Tests

Storage domain isolation tests verify that IPC handlers enforce storage domain
boundaries and prevent cross-domain data access.

This section references Architecture Documentation for communication paths and
process model, Security Documentation for IPC threat model, Engineering
Documentation for channel standards, and Feature Technical Documentation for
service component responsibilities.
"#;
        let report = validate(doc);
        assert!(
            report.passed > 5,
            "Comprehensive doc should pass more than 5 rules; passed: {}, errors: {}, warnings: {}, findings: {:?}",
            report.passed,
            report.errors,
            report.warnings,
            report.findings,
        );
    }

    #[test]
    fn default_meta_is_correct() {
        let meta = DeterministMeta::default();
        assert_eq!(meta.system_id, "samgraha-documentation");
        assert_eq!(meta.domain, "qa");
        assert_eq!(meta.section_type, "ipc_testing");
        assert_eq!(meta.kind, "deterministic");
    }

    #[test]
    fn serialization_roundtrip() {
        let rules = build_rules();
        let json = serde_json::to_string(&rules).unwrap();
        let deserialized: Vec<AuditRule> = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.len(), rules.len());
        assert_eq!(deserialized[0].id, rules[0].id);
    }
}
