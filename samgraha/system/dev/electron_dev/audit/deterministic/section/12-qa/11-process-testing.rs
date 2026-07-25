use serde::{Deserialize, Serialize};

/// Process Testing Determinist — validates isolation tests, lifecycle tests, crash recovery
/// for desktop application multi-process architecture (Main/Renderer/Preload/Utility).
///
/// System: electron_dev
/// Domain: qa
/// Section: process_testing

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessTestingDeterminist {
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
            section_type: "process_testing",
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
            id: "qa-sec-process_testing-001",
            description: "Process Testing section exists",
            condition: "document has a section with semantic_type = 'process_testing'",
            message: "Missing required 'Process Testing' section",
            severity: Severity::Error,
            weight: 1.5,
            mandatory: true,
            evidence: Evidence::SectionPresence {
                semantic_type: "process_testing",
            },
        },
        // ── Main Process Lifecycle ──
        AuditRule {
            id: "qa-sec-process_testing-002",
            description: "Main process lifecycle tests exist",
            condition: "tests verify Main process startup, ready-state, graceful shutdown, and signal handling (SIGINT, SIGTERM, SIGHUP on Unix)",
            message: "Main process lifecycle tests are missing",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "main",
                    "process",
                    "lifecycle",
                    "startup",
                    "shutdown",
                    "graceful",
                    "signal",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-003",
            description: "Main process ready-state detection tests",
            condition: "tests verify that the Main process signals readiness only after all services are initialized and the primary window is loaded",
            message: "Main process ready-state detection tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "ready",
                    "ready-state",
                    "initialized",
                    "service",
                    "window",
                    "loaded",
                    "signal",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-004",
            description: "Main process single-instance lock tests",
            condition: "tests verify that the single-instance lock prevents duplicate Main process launches and routes activation requests to the existing instance",
            message: "Main process single-instance lock tests are missing",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "single-instance",
                    "lock",
                    "duplicate",
                    "activation",
                    "request",
                    "existing",
                ]),
                patterns: None,
            },
        },
        // ── Renderer Process Lifecycle ──
        AuditRule {
            id: "qa-sec-process_testing-005",
            description: "Renderer process lifecycle tests exist",
            condition: "tests verify Renderer process creation, page load, DOM ready, navigation, and destruction for each application window",
            message: "Renderer process lifecycle tests are missing",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "renderer",
                    "process",
                    "lifecycle",
                    "creation",
                    "page load",
                    "dom",
                    "destruction",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-006",
            description: "Renderer process crash recovery tests exist",
            condition: "tests verify that Renderer process crashes are detected by Main, the window is recreated or an error state is displayed, and IPC channels are re-established",
            message: "Renderer process crash recovery tests are missing",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "crash",
                    "recovery",
                    "renderer",
                    "recreate",
                    "error",
                    "ipc",
                    "re-establish",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-007",
            description: "Renderer process unresponsive detection tests",
            condition: "tests verify that unresponsive Renderer processes are detected within a configurable timeout and trigger recovery actions",
            message: "Renderer process unresponsive detection tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "unresponsive",
                    "timeout",
                    "detection",
                    "recovery",
                    "renderer",
                    "hang",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-008",
            description: "Renderer process memory pressure tests",
            condition: "tests verify behavior under memory pressure including garbage collection pressure, heap size limits, and memory leak detection",
            message: "Renderer process memory pressure tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "memory",
                    "pressure",
                    "heap",
                    "garbage collection",
                    "leak",
                    "limit",
                ]),
                patterns: None,
            },
        },
        // ── Preload Process Tests ──
        AuditRule {
            id: "qa-sec-process_testing-009",
            description: "Preload script execution isolation tests",
            condition: "tests verify that preload scripts run in an isolated context with access to both Node.js APIs and the Renderer DOM but not to arbitrary Main process modules",
            message: "Preload script execution isolation tests are missing",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "preload",
                    "isolation",
                    "context",
                    "node",
                    "dom",
                    "main",
                    "module",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-010",
            description: "Preload injection timing tests",
            condition: "tests verify that preload scripts execute before DOMContentLoaded and after the renderer world is created, in the correct sequence",
            message: "Preload injection timing tests are missing",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "preload",
                    "timing",
                    "DOMContentLoaded",
                    "sequence",
                    "injection",
                    "execute",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-011",
            description: "Preload API surface boundary tests",
            condition: "tests verify that preload scripts cannot extend the exposed API surface at runtime and that the API surface matches the declared contract",
            message: "Preload API surface boundary tests are missing",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "preload",
                    "api",
                    "surface",
                    "boundary",
                    "runtime",
                    "contract",
                    "extend",
                ]),
                patterns: None,
            },
        },
        // ── Utility Process Tests ──
        AuditRule {
            id: "qa-sec-process_testing-012",
            description: "Utility process lifecycle tests exist",
            condition: "tests verify utility process (worker) creation, message passing, error handling, and termination",
            message: "Utility process lifecycle tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "utility",
                    "process",
                    "worker",
                    "lifecycle",
                    "creation",
                    "termination",
                    "message",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-013",
            description: "Utility process crash isolation tests",
            condition: "tests verify that utility process crashes do not propagate to the Main process and that the Main process can detect and restart failed workers",
            message: "Utility process crash isolation tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "utility",
                    "crash",
                    "isolation",
                    "main",
                    "propagate",
                    "restart",
                    "worker",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-014",
            description: "Utility process resource limit tests",
            condition: "tests verify that utility processes enforce CPU and memory limits and are terminated when limits are exceeded",
            message: "Utility process resource limit tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "utility",
                    "resource",
                    "limit",
                    "cpu",
                    "memory",
                    "terminate",
                    "exceed",
                ]),
                patterns: None,
            },
        },
        // ── Cross-Process Communication Tests ──
        AuditRule {
            id: "qa-sec-process_testing-015",
            description: "Cross-process message ordering tests",
            condition: "tests verify that messages between Main and Renderer processes maintain ordering guarantees and do not arrive out of sequence under load",
            message: "Cross-process message ordering tests are missing",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "message",
                    "ordering",
                    "sequence",
                    "cross-process",
                    "main",
                    "renderer",
                    "guarantee",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-016",
            description: "Cross-process error propagation tests",
            condition: "tests verify that unhandled exceptions in Renderer processes do not crash the Main process and are caught and logged appropriately",
            message: "Cross-process error propagation tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "error",
                    "propagation",
                    "exception",
                    "crash",
                    "main",
                    "renderer",
                    "catch",
                    "log",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-017",
            description: "Cross-process state synchronization tests",
            condition: "tests verify that shared state between Main and Renderer processes is synchronized correctly and does not diverge under concurrent updates",
            message: "Cross-process state synchronization tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "state",
                    "synchronization",
                    "shared",
                    "concurrent",
                    "diverge",
                    "update",
                ]),
                patterns: None,
            },
        },
        // ── Process Spawn & Supervision Tests ──
        AuditRule {
            id: "qa-sec-process_testing-018",
            description: "Process spawn failure handling tests",
            condition: "tests verify that failures to spawn child processes (Renderer or Utility) are handled gracefully with user feedback and retry logic",
            message: "Process spawn failure handling tests are missing",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "spawn",
                    "failure",
                    "graceful",
                    "retry",
                    "feedback",
                    "child process",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-019",
            description: "Process supervision restart tests",
            condition: "tests verify that the Main process can detect failed child processes and restart them within configurable retry limits",
            message: "Process supervision restart tests are missing",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "supervision",
                    "restart",
                    "detect",
                    "failed",
                    "retry",
                    "limit",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-020",
            description: "Process watchdog timer tests",
            condition: "tests verify that a watchdog monitors Main process health and triggers recovery if the process becomes unresponsive",
            message: "Process watchdog timer tests are missing",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "watchdog",
                    "health",
                    "monitor",
                    "unresponsive",
                    "recovery",
                    "timer",
                ]),
                patterns: None,
            },
        },
        // ── Graceful Degradation Tests ──
        AuditRule {
            id: "qa-sec-process_testing-021",
            description: "Graceful degradation under resource exhaustion tests",
            condition: "tests verify that the application degrades gracefully when system resources (CPU, memory, file descriptors) are exhausted",
            message: "Graceful degradation under resource exhaustion tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "graceful",
                    "degradation",
                    "resource",
                    "exhaustion",
                    "cpu",
                    "memory",
                    "file descriptor",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-022",
            description: "Process cleanup on exit tests",
            condition: "tests verify that all child processes, file handles, sockets, and temporary files are cleaned up on application exit",
            message: "Process cleanup on exit tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "cleanup",
                    "exit",
                    "child process",
                    "file handle",
                    "socket",
                    "temporary",
                    "resource",
                ]),
                patterns: None,
            },
        },
        // ── Event System Process Tests ──
        AuditRule {
            id: "qa-sec-process_testing-023",
            description: "Event system process dispatch tests",
            condition: "tests verify that the event system dispatches events to the correct process context and that events do not leak across process boundaries",
            message: "Event system process dispatch tests are missing",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "event",
                    "dispatch",
                    "process",
                    "context",
                    "leak",
                    "boundary",
                    "handler",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-process_testing-024",
            description: "Background job process isolation tests",
            condition: "tests verify that background jobs run in isolated utility processes and do not share memory or state with the Main process except through defined IPC channels",
            message: "Background job process isolation tests are missing",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "background",
                    "job",
                    "isolation",
                    "utility",
                    "process",
                    "memory",
                    "ipc",
                ]),
                patterns: None,
            },
        },
        // ── Configuration Lock Process Tests ──
        AuditRule {
            id: "qa-sec-process_testing-025",
            description: "Configuration lock cross-process tests",
            condition: "tests verify that configuration locks are enforced across processes and that concurrent configuration reads and writes from different processes do not produce stale data",
            message: "Configuration lock cross-process tests are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "configuration",
                    "lock",
                    "cross-process",
                    "concurrent",
                    "read",
                    "write",
                    "stale",
                ]),
                patterns: None,
            },
        },
        // ── Cross-Reference Tests ──
        AuditRule {
            id: "qa-sec-process_testing-026",
            description: "Process tests reference Architecture Documentation",
            condition: "section references Architecture Documentation process model and component boundaries",
            message: "Process tests do not reference Architecture Documentation",
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
            id: "qa-sec-process_testing-027",
            description: "Process tests reference Security Documentation",
            condition: "section references Security Documentation process isolation and sandbox requirements",
            message: "Process tests do not reference Security Documentation",
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
            id: "qa-sec-process_testing-028",
            description: "Process tests reference Engineering Documentation",
            condition: "section references Engineering Documentation process management conventions and error handling standards",
            message: "Process tests do not reference Engineering Documentation",
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
            RuleResult::Pass => passed += 1,
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
    fn default_meta_is_correct() {
        let meta = DeterministMeta::default();
        assert_eq!(meta.system_id, "samgraha-documentation");
        assert_eq!(meta.domain, "qa");
        assert_eq!(meta.section_type, "process_testing");
        assert_eq!(meta.kind, "deterministic");
    }

    #[test]
    fn serialization_roundtrip() {
        let rules = build_rules();
        let json = serde_json::to_string(&rules).unwrap();
        let deserialized: Vec<AuditRule> = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.len(), rules.len());
    }
}
