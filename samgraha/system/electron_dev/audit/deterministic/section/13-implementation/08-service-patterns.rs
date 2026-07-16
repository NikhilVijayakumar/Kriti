use serde::{Deserialize, Serialize};

/// Service Patterns Determinist — validates factory pattern, lifecycle, IPC wrapping
/// for desktop application service registry and dependency injection.
///
/// System: electron_dev
/// Domain: implementation
/// Section: service_patterns

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServicePatternsDeterminist {
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
            domain: "implementation",
            section_type: "service_patterns",
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
            id: "impl-sec-service_patterns-001",
            description: "Service Patterns section exists",
            condition: "document has a section with semantic_type = 'service_patterns'",
            message: "Missing required 'Service Patterns' section",
            severity: Severity::Error,
            weight: 1.5,
            mandatory: true,
            evidence: Evidence::SectionPresence {
                semantic_type: "service_patterns",
            },
        },
        // ── Factory Pattern ──
        AuditRule {
            id: "impl-sec-service_patterns-002",
            description: "Service factory pattern is defined",
            condition: "section defines a factory function or builder pattern for constructing service instances with dependency injection",
            message: "Service factory pattern is not defined",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "factory",
                    "builder",
                    "construct",
                    "dependency",
                    "inject",
                    "create",
                    "instance",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-003",
            description: "Factory validates dependencies before construction",
            condition: "factory pattern verifies that all required dependencies are available and initialized before constructing a service instance",
            message: "Factory pattern does not validate dependencies before construction",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "validate",
                    "dependency",
                    "available",
                    "initialized",
                    "before",
                    "construct",
                    "check",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-004",
            description: "Factory pattern supports lazy and eager initialization",
            condition: "factory supports both lazy initialization (on first use) and eager initialization (at startup) with explicit selection per service",
            message: "Factory pattern does not support lazy and eager initialization modes",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "lazy",
                    "eager",
                    "initialization",
                    "startup",
                    "first use",
                    "mode",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-005",
            description: "Factory supports singleton and transient lifetimes",
            condition: "factory supports singleton (shared instance) and transient (new instance per request) service lifetimes with explicit declaration per service",
            message: "Factory does not support singleton and transient service lifetimes",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "singleton",
                    "transient",
                    "lifetime",
                    "shared",
                    "instance",
                    "per-request",
                ]),
                patterns: None,
            },
        },
        // ── Service Lifecycle ──
        AuditRule {
            id: "impl-sec-service_patterns-006",
            description: "Service lifecycle phases are defined",
            condition: "section defines explicit lifecycle phases for services: registration, initialization, ready, degradation, shutdown",
            message: "Service lifecycle phases are not defined",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "lifecycle",
                    "registration",
                    "initialization",
                    "ready",
                    "degradation",
                    "shutdown",
                    "phase",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-007",
            description: "Service startup ordering is defined",
            condition: "section defines the order in which services are initialized during application startup, including dependency-driven ordering",
            message: "Service startup ordering is not defined",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "startup",
                    "ordering",
                    "initialize",
                    "dependency",
                    "sequence",
                    "order",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-008",
            description: "Service shutdown ordering is defined",
            condition: "section defines the order in which services are shut down during application exit, in reverse startup order with graceful drain",
            message: "Service shutdown ordering is not defined",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "shutdown",
                    "ordering",
                    "exit",
                    "reverse",
                    "drain",
                    "graceful",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-009",
            description: "Service health check mechanism is defined",
            condition: "section defines a health check protocol for services including readiness checks, liveness probes, and degraded state reporting",
            message: "Service health check mechanism is not defined",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "health",
                    "check",
                    "readiness",
                    "liveness",
                    "degraded",
                    "probe",
                    "protocol",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-010",
            description: "Service error recovery is defined",
            condition: "section defines how services recover from failures including retry strategies, circuit breakers, and fallback behavior",
            message: "Service error recovery is not defined",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "recovery",
                    "retry",
                    "circuit breaker",
                    "fallback",
                    "failure",
                    "strategy",
                ]),
                patterns: None,
            },
        },
        // ── IPC Wrapping ──
        AuditRule {
            id: "impl-sec-service_patterns-011",
            description: "IPC service wrapping pattern is defined",
            condition: "section defines how Main-process services are wrapped for Renderer-process consumption via IPC, with each service exposing a typed API surface",
            message: "IPC service wrapping pattern is not defined",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "ipc",
                    "wrap",
                    "service",
                    "typed",
                    "api",
                    "renderer",
                    "main",
                    "surface",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-012",
            description: "IPC wrapping uses contextBridge for preload exposure",
            condition: "IPC-wrapped services are exposed to Renderer processes through contextBridge.exposeInMainWorld in preload scripts, not through direct ipcRenderer access",
            message: "IPC wrapping does not use contextBridge for preload exposure",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "contextBridge",
                    "exposeInMainWorld",
                    "preload",
                    "ipc",
                    "wrap",
                    "exposure",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-013",
            description: "IPC wrapping validates input/output schemas",
            condition: "IPC wrappers validate input arguments and output return values against declared schemas at the process boundary before forwarding to the service",
            message: "IPC wrapping does not validate input/output schemas",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "validate",
                    "input",
                    "output",
                    "schema",
                    "boundary",
                    "forward",
                    "argument",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-014",
            description: "IPC wrapping handles service unavailability",
            condition: "IPC wrappers detect when the target service is not ready or has crashed and return a structured error to the Renderer process",
            message: "IPC wrapping does not handle service unavailability",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "unavailable",
                    "not ready",
                    "crashed",
                    "error",
                    "structured",
                    "detect",
                    "wrapper",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-015",
            description: "IPC channel naming follows project convention",
            condition: "IPC channels follow the project naming convention (e.g. domain:entity:action) and are registered in a central channel registry",
            message: "IPC channel naming does not follow project convention or is not centrally registered",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "channel",
                    "naming",
                    "convention",
                    "registry",
                    "central",
                    "register",
                ]),
                patterns: None,
            },
        },
        // ── Service Registry ──
        AuditRule {
            id: "impl-sec-service_patterns-016",
            description: "Service registry is defined",
            condition: "section defines a central service registry that tracks all registered services, their lifetimes, and their dependencies",
            message: "Service registry is not defined",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "registry",
                    "central",
                    "register",
                    "lifetime",
                    "dependency",
                    "track",
                    "service",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-017",
            description: "Service registry enforces dependency resolution",
            condition: "service registry resolves dependencies at registration time and detects circular dependencies before any service is initialized",
            message: "Service registry does not enforce dependency resolution",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "dependency",
                    "resolve",
                    "circular",
                    "detect",
                    "registration",
                    "initialize",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-018",
            description: "Service registry supports service lookup by name and interface",
            condition: "service registry allows lookup by service name and by interface/type, enabling loose coupling between consumers and providers",
            message: "Service registry does not support lookup by name and interface",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "lookup",
                    "name",
                    "interface",
                    "type",
                    "loose coupling",
                    "consumer",
                    "provider",
                ]),
                patterns: None,
            },
        },
        // ── Event System Integration ──
        AuditRule {
            id: "impl-sec-service_patterns-019",
            description: "Service event system integration is defined",
            condition: "section defines how services publish and subscribe to events through the application event system, including cross-process event forwarding",
            message: "Service event system integration is not defined",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "event",
                    "publish",
                    "subscribe",
                    "forward",
                    "cross-process",
                    "integration",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-020",
            description: "Service event lifecycle hooks are defined",
            condition: "section defines lifecycle event hooks (onInit, onReady, onShutdown, onError) that services can implement to participate in application lifecycle",
            message: "Service event lifecycle hooks are not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "lifecycle",
                    "hook",
                    "onInit",
                    "onReady",
                    "onShutdown",
                    "onError",
                ]),
                patterns: None,
            },
        },
        // ── Background Job Integration ──
        AuditRule {
            id: "impl-sec-service_patterns-021",
            description: "Background job service pattern is defined",
            condition: "section defines how background jobs are registered as services with the service registry, including scheduling, execution, and result delivery",
            message: "Background job service pattern is not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "background",
                    "job",
                    "schedule",
                    "execute",
                    "result",
                    "service",
                    "registry",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "impl-sec-service_patterns-022",
            description: "Background job retry and dead-letter handling is defined",
            condition: "section defines retry policies for failed background jobs and dead-letter queue handling for permanently failed jobs",
            message: "Background job retry and dead-letter handling is not defined",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "retry",
                    "dead-letter",
                    "failed",
                    "policy",
                    "permanent",
                    "queue",
                ]),
                patterns: None,
            },
        },
        // ── Configuration Lock Integration ──
        AuditRule {
            id: "impl-sec-service_patterns-023",
            description: "Configuration lock service integration is defined",
            condition: "section defines how services acquire and release configuration locks to prevent concurrent configuration mutations",
            message: "Configuration lock service integration is not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "configuration",
                    "lock",
                    "acquire",
                    "release",
                    "concurrent",
                    "mutation",
                ]),
                patterns: None,
            },
        },
        // ── Storage Domain Integration ──
        AuditRule {
            id: "impl-sec-service_patterns-024",
            description: "Storage domain service boundary is defined",
            condition: "section defines how services are assigned to storage domains and how cross-domain data access is controlled through the service layer",
            message: "Storage domain service boundary is not defined",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "storage",
                    "domain",
                    "boundary",
                    "access",
                    "control",
                    "cross-domain",
                    "service",
                ]),
                patterns: None,
            },
        },
        // ── Process Boundary Service Tests ──
        AuditRule {
            id: "impl-sec-service_patterns-025",
            description: "Service pattern tests verify process boundary behavior",
            condition: "section references tests that verify service instantiation, invocation, and error handling across Main/Renderer/Preload process boundaries",
            message: "Service pattern tests for process boundary behavior are not referenced",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "test",
                    "process",
                    "boundary",
                    "instantiation",
                    "invocation",
                    "error",
                    "main",
                    "renderer",
                ]),
                patterns: None,
            },
        },
        // ── Cross-References ──
        AuditRule {
            id: "impl-sec-service_patterns-026",
            description: "Service patterns reference Architecture Documentation",
            condition: "section references Architecture Documentation component model and service boundaries",
            message: "Service patterns do not reference Architecture Documentation",
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
            id: "impl-sec-service_patterns-027",
            description: "Service patterns reference Engineering Documentation",
            condition: "section references Engineering Documentation service conventions and IPC standards",
            message: "Service patterns do not reference Engineering Documentation",
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
            id: "impl-sec-service_patterns-028",
            description: "Service patterns reference Feature Technical Documentation",
            condition: "section references Feature Technical Documentation component responsibilities for each implemented service",
            message: "Service patterns do not reference Feature Technical Documentation",
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
        AuditRule {
            id: "impl-sec-service_patterns-029",
            description: "Service patterns reference Security Documentation",
            condition: "section references Security Documentation service-level security constraints and IPC security model",
            message: "Service patterns do not reference Security Documentation",
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
        assert!(rules.len() >= 29, "Expected at least 29 rules, got {}", rules.len());
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
        assert_eq!(meta.domain, "implementation");
        assert_eq!(meta.section_type, "service_patterns");
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
