use serde::{Deserialize, Serialize};

/// Cross-Platform Testing Determinist — validates platform matrix, native tests, CI config
/// for desktop application targeting Windows, macOS, and Linux.
///
/// System: electron_dev
/// Domain: qa
/// Section: cross_platform_testing

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CrossPlatformTestingDeterminist {
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
            section_type: "cross_platform_testing",
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
            id: "qa-sec-cross_platform_testing-001",
            description: "Cross-Platform Testing section exists",
            condition: "document has a section with semantic_type = 'cross_platform_testing'",
            message: "Missing required 'Cross-Platform Testing' section",
            severity: Severity::Error,
            weight: 1.5,
            mandatory: true,
            evidence: Evidence::SectionPresence {
                semantic_type: "cross_platform_testing",
            },
        },
        // ── Platform Matrix ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-002",
            description: "Platform matrix defines all target operating systems",
            condition: "section defines a platform matrix covering Windows (x64, ARM64), macOS (x64, ARM64/Apple Silicon), and Linux (x64, ARM64) with explicit OS version ranges",
            message: "Platform matrix does not define all target operating systems with version ranges",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "windows",
                    "macos",
                    "linux",
                    "x64",
                    "arm64",
                    "apple silicon",
                    "version",
                    "platform",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-003",
            description: "Platform matrix defines minimum supported versions",
            condition: "section specifies the minimum supported OS version for each platform (e.g. Windows 10 1903, macOS 11, Ubuntu 20.04)",
            message: "Platform matrix does not define minimum supported OS versions",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "minimum",
                    "supported",
                    "version",
                    "windows 10",
                    "macos 11",
                    "ubuntu",
                    "baseline",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-004",
            description: "Platform matrix defines CI runner specifications",
            condition: "section specifies the CI runner or build agent configuration for each platform (e.g. GitHub Actions runner images, self-hosted runners)",
            message: "Platform matrix does not define CI runner specifications",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "ci",
                    "runner",
                    "build",
                    "agent",
                    "github actions",
                    "self-hosted",
                    "image",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-005",
            description: "Platform matrix defines Electron version per platform",
            condition: "section specifies which Electron version is tested on each platform and whether platform-specific Electron patches are applied",
            message: "Platform matrix does not define Electron version per platform",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "electron",
                    "version",
                    "platform",
                    "patch",
                    "chromium",
                    "node",
                ]),
                patterns: None,
            },
        },
        // ── Native Module Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-006",
            description: "Native module compilation tests exist for each platform",
            condition: "tests verify that native Node.js addons (node-gyp, prebuild) compile and link correctly on each target platform and architecture",
            message: "Native module compilation tests per platform are missing",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "native",
                    "module",
                    "compile",
                    "link",
                    "node-gyp",
                    "prebuild",
                    "addon",
                    "platform",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-007",
            description: "Native module runtime tests exist for each platform",
            condition: "tests verify that native modules load, initialize, and function correctly at runtime on each target platform",
            message: "Native module runtime tests per platform are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "native",
                    "runtime",
                    "load",
                    "initialize",
                    "function",
                    "platform",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-008",
            description: "Native module ABI compatibility tests exist",
            condition: "tests verify that prebuilt binaries are ABI-compatible with the target Electron/Node.js version on each platform",
            message: "Native module ABI compatibility tests are missing",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "abi",
                    "compatibility",
                    "prebuilt",
                    "binary",
                    "electron",
                    "node",
                ]),
                patterns: None,
            },
        },
        // ── Platform-Specific Feature Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-009",
            description: "Platform-specific API usage tests exist",
            condition: "tests verify that platform-specific APIs (e.g. Windows registry, macOS notification center, Linux D-Bus) are only invoked on their target platform",
            message: "Platform-specific API usage tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "platform-specific",
                    "api",
                    "registry",
                    "notification",
                    "d-bus",
                    "guard",
                    "conditional",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-010",
            description: "Filesystem path handling tests exist",
            condition: "tests verify correct handling of platform-specific path separators, case sensitivity, extended-length paths (Windows), and symlinks",
            message: "Filesystem path handling tests are missing",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "path",
                    "separator",
                    "case sensitivity",
                    "symlink",
                    "extended-length",
                    "filesystem",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-011",
            description: "Process priority and scheduling tests exist",
            condition: "tests verify that process priority, CPU affinity, and scheduling behave correctly on each platform (e.g. nice values on Linux, priority class on Windows)",
            message: "Process priority and scheduling tests are missing",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "priority",
                    "scheduling",
                    "nice",
                    "affinity",
                    "cpu",
                    "platform",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-012",
            description: "Auto-updater platform tests exist",
            condition: "tests verify that the auto-updater works on each platform including code signature validation (macOS notarization, Windows Authenticode, Linux GPG)",
            message: "Auto-updater platform tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "auto-updater",
                    "code signature",
                    "notarization",
                    "authenticode",
                    "gpg",
                    "platform",
                ]),
                patterns: None,
            },
        },
        // ── UI Rendering Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-013",
            description: "UI rendering parity tests exist across platforms",
            condition: "tests verify that the application UI renders correctly on each platform accounting for DPI scaling, font rendering differences, and window chrome variations",
            message: "UI rendering parity tests across platforms are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "ui",
                    "rendering",
                    "parity",
                    "dpi",
                    "scaling",
                    "font",
                    "window chrome",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-014",
            description: "High-DPI and multi-monitor tests exist",
            condition: "tests verify correct behavior on high-DPI displays and multi-monitor setups with different scaling factors on each platform",
            message: "High-DPI and multi-monitor tests are missing",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "high-dpi",
                    "multi-monitor",
                    "scaling",
                    "retina",
                    "display",
                    "factor",
                ]),
                patterns: None,
            },
        },
        // ── Platform-Specific Packaging Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-015",
            description: "Platform installer tests exist",
            condition: "tests verify that platform-specific installers (NSIS/MSI for Windows, DMG/PKG for macOS, DEB/RPM/AppImage for Linux) install, uninstall, and update correctly",
            message: "Platform installer tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "installer",
                    "nsis",
                    "msi",
                    "dmg",
                    "pkg",
                    "deb",
                    "rpm",
                    "appimage",
                    "uninstall",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-016",
            description: "Portable app tests exist",
            condition: "tests verify that portable/standalone builds (no installer) run correctly on each platform without requiring elevated privileges",
            message: "Portable app tests are missing",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "portable",
                    "standalone",
                    "no installer",
                    "elevated",
                    "privilege",
                    "run",
                ]),
                patterns: None,
            },
        },
        // ── CI Configuration Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-017",
            description: "CI pipeline tests run on all target platforms",
            condition: "CI configuration includes a build and test job for each platform in the matrix, and the pipeline blocks release if any platform fails",
            message: "CI pipeline does not test on all target platforms",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "ci",
                    "pipeline",
                    "build",
                    "test",
                    "platform",
                    "matrix",
                    "release",
                    "block",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-018",
            description: "CI configuration includes platform-specific test flags",
            condition: "CI jobs pass platform-appropriate test flags, environment variables, and runtime configurations to the test suite",
            message: "CI configuration does not include platform-specific test flags",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "flag",
                    "environment",
                    "variable",
                    "platform",
                    "configuration",
                    "runtime",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-019",
            description: "CI cross-compilation tests exist",
            condition: "CI configuration tests cross-compilation scenarios (e.g. building Windows on Linux CI, building ARM64 on x64 CI) where applicable",
            message: "CI cross-compilation tests are missing",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "cross-compilation",
                    "cross-compile",
                    "build",
                    "arm64",
                    "x64",
                    "ci",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-020",
            description: "CI artifact caching tests exist",
            condition: "CI configuration caches platform-specific build artifacts (node_modules, native modules, Electron binaries) and verifies cache validity",
            message: "CI artifact caching tests are missing",
            severity: Severity::Warning,
            weight: 0.6,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "cache",
                    "artifact",
                    "node_modules",
                    "native",
                    "electron",
                    "ci",
                ]),
                patterns: None,
            },
        },
        // ── Storage Domain Platform Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-021",
            description: "Storage domain path tests per platform",
            condition: "tests verify that storage domains use platform-appropriate paths (AppData on Windows, ~/Library/Application Support on macOS, ~/.config on Linux)",
            message: "Storage domain path tests per platform are missing",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "storage",
                    "domain",
                    "path",
                    "appdata",
                    "application support",
                    ".config",
                    "platform",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-022",
            description: "Storage domain permission tests per platform",
            condition: "tests verify that storage directories are created with correct permissions on each platform (e.g. 0700 on Linux, NTFS ACLs on Windows)",
            message: "Storage domain permission tests per platform are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "storage",
                    "permission",
                    "0700",
                    "acl",
                    "ntfs",
                    "platform",
                    "directory",
                ]),
                patterns: None,
            },
        },
        // ── Platform-Specific IPC Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-023",
            description: "IPC behavior parity tests across platforms",
            condition: "tests verify that IPC channels behave identically on all platforms including message ordering, serialization, and error handling",
            message: "IPC behavior parity tests across platforms are missing",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "ipc",
                    "parity",
                    "behavior",
                    "platform",
                    "message",
                    "serialization",
                ]),
                patterns: None,
            },
        },
        // ── Platform Release Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-024",
            description: "Platform release artifact tests exist",
            condition: "tests verify that release artifacts for each platform are correctly signed, notarized (macOS), and contain the expected file structure",
            message: "Platform release artifact tests are missing",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "release",
                    "artifact",
                    "signed",
                    "notarized",
                    "structure",
                    "platform",
                ]),
                patterns: None,
            },
        },
        // ── Cross-Reference Tests ──
        AuditRule {
            id: "qa-sec-cross_platform_testing-025",
            description: "Cross-platform tests reference Architecture Documentation",
            condition: "section references Architecture Documentation platform constraints and process model",
            message: "Cross-platform tests do not reference Architecture Documentation",
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
            id: "qa-sec-cross_platform_testing-026",
            description: "Cross-platform tests reference External Context Documentation",
            condition: "section references External Context Documentation platform-specific constraints and dependencies",
            message: "Cross-platform tests do not reference External Context Documentation",
            severity: Severity::Warning,
            weight: 0.5,
            mandatory: false,
            evidence: Evidence::CrossReference {
                expected: vec![CrossRef {
                    domain: "external-context",
                    direction: "derives_from",
                }],
            },
        },
        AuditRule {
            id: "qa-sec-cross_platform_testing-027",
            description: "Cross-platform tests reference Engineering Documentation",
            condition: "section references Engineering Documentation cross-platform build standards and tooling",
            message: "Cross-platform tests do not reference Engineering Documentation",
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
        assert!(rules.len() >= 27, "Expected at least 27 rules, got {}", rules.len());
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
        assert_eq!(meta.section_type, "cross_platform_testing");
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
