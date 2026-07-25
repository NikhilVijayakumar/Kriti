use serde::{Deserialize, Serialize};

/// Desktop Packaging Determinist — validates electron-builder config, platform packaging,
/// code signing for desktop application distribution.
///
/// System: electron_dev
/// Domain: build
/// Section: packaging

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PackagingDeterminist {
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
            domain: "build",
            section_type: "packaging",
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
            id: "build-sec-packaging-001",
            description: "Packaging section exists",
            condition: "document has a section with semantic_type = 'packaging'",
            message: "Missing required 'Packaging' section",
            severity: Severity::Error,
            weight: 1.5,
            mandatory: true,
            evidence: Evidence::SectionPresence {
                semantic_type: "packaging",
            },
        },
        // ── electron-builder Configuration ──
        AuditRule {
            id: "build-sec-packaging-002",
            description: "electron-builder configuration is defined",
            condition: "section defines or references the electron-builder configuration (electron-builder.yml, package.json build key, or JS config) with all required fields",
            message: "electron-builder configuration is not defined",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "electron-builder",
                    "config",
                    "configuration",
                    "build",
                    "yml",
                    "yaml",
                    "json",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-003",
            description: "electron-builder appId is defined",
            condition: "electron-builder configuration specifies a reverse-domain appId (e.g. com.company.appname) used for all platform identifiers",
            message: "electron-builder appId is not defined",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "appid",
                    "app-id",
                    "com.",
                    "reverse-domain",
                    "identifier",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-004",
            description: "electron-builder productName is defined",
            condition: "electron-builder configuration specifies a human-readable productName used in installer titles, window titles, and system notifications",
            message: "electron-builder productName is not defined",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(60),
                keywords: Some(vec![
                    "productname",
                    "product-name",
                    "product name",
                    "display",
                    "installer",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-005",
            description: "electron-builder files glob is defined",
            condition: "electron-builder configuration specifies the files glob pattern to include/exclude in the asar archive, excluding development-only files",
            message: "electron-builder files glob is not defined",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "files",
                    "glob",
                    "include",
                    "exclude",
                    "asar",
                    "archive",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-006",
            description: "electron-builder asar packaging is configured",
            condition: "electron-builder configuration defines asar packaging settings (asar: true/false, unpacked resources, smart unpacking for native modules)",
            message: "electron-builder asar packaging is not configured",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "asar",
                    "unpack",
                    "smart",
                    "native",
                    "module",
                    "archive",
                ]),
                patterns: None,
            },
        },
        // ── Platform-Specific Packaging ──
        AuditRule {
            id: "build-sec-packaging-007",
            description: "Windows packaging configuration is defined",
            condition: "section defines Windows packaging: target format (NSIS, MSI, portable), icon format (.ico), publisher name, requested execution level, and file associations",
            message: "Windows packaging configuration is not defined",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "windows",
                    "nsis",
                    "msi",
                    "ico",
                    "publisher",
                    "execution level",
                    "file association",
                    "portable",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-008",
            description: "macOS packaging configuration is defined",
            condition: "section defines macOS packaging: target format (DMG, PKG, ZIP), icon format (.icns), entitlements plist, category (UTI), minimum deployment target",
            message: "macOS packaging configuration is not defined",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "macos",
                    "dmg",
                    "pkg",
                    "icns",
                    "entitlements",
                    "category",
                    "uti",
                    "deployment target",
                    "zip",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-009",
            description: "Linux packaging configuration is defined",
            condition: "section defines Linux packaging: target formats (DEB, RPM, AppImage, Snap), desktop file, icon format (PNG), category, dependencies, and maintained permissions",
            message: "Linux packaging configuration is not defined",
            severity: Severity::Error,
            weight: 1.3,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "linux",
                    "deb",
                    "rpm",
                    "appimage",
                    "snap",
                    "desktop",
                    "png",
                    "dependency",
                    "category",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-010",
            description: "Platform icon assets are defined",
            condition: "section defines the source icon assets for each platform: PNG (512x512 minimum) for Linux, ICO for Windows, ICNS for macOS, and the generation pipeline from a single source",
            message: "Platform icon assets are not defined",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "icon",
                    "png",
                    "ico",
                    "icns",
                    "512",
                    "source",
                    "generate",
                    "pipeline",
                ]),
                patterns: None,
            },
        },
        // ── Code Signing ──
        AuditRule {
            id: "build-sec-packaging-011",
            description: "macOS code signing configuration is defined",
            condition: "section defines macOS code signing: Apple Developer ID certificate, team ID, entitlements for hardened runtime, notarization via notarytool, and staple process",
            message: "macOS code signing configuration is not defined",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "code signing",
                    "developer id",
                    "team id",
                    "entitlements",
                    "hardened runtime",
                    "notarization",
                    "notarytool",
                    "staple",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-012",
            description: "Windows code signing configuration is defined",
            condition: "section defines Windows code signing: Authenticode certificate, timestamp server, signtool or osslsigncode configuration, and EV certificate requirements",
            message: "Windows code signing configuration is not defined",
            severity: Severity::Error,
            weight: 1.4,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(150),
                keywords: Some(vec![
                    "authenticode",
                    "certificate",
                    "timestamp",
                    "signtool",
                    "osslsigncode",
                    "ev certificate",
                    "sign",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-013",
            description: "Linux package signing is defined",
            condition: "section defines Linux package signing: GPG key for DEB/RPM packages, repository signing, and package verification instructions",
            message: "Linux package signing is not defined",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "gpg",
                    "sign",
                    "deb",
                    "rpm",
                    "repository",
                    "verify",
                    "key",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-014",
            description: "Code signing secret management is defined",
            condition: "section defines how code signing certificates and keys are stored (CI secrets vault, HSM, notarization API key) and accessed during builds without exposing them in source",
            message: "Code signing secret management is not defined",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "secret",
                    "vault",
                    "hsm",
                    "certificate",
                    "key",
                    "ci",
                    "environment",
                    "expose",
                ]),
                patterns: None,
            },
        },
        // ── Artifact Naming & Versioning ──
        AuditRule {
            id: "build-sec-packaging-015",
            description: "Artifact naming convention is defined",
            condition: "section defines the artifact naming convention for each platform including version, platform, and architecture in the filename (e.g. appName-1.2.3-x64.exe)",
            message: "Artifact naming convention is not defined",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "naming",
                    "convention",
                    "artifact",
                    "version",
                    "platform",
                    "architecture",
                    "filename",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-016",
            description: "Artifact checksum generation is defined",
            condition: "section defines that SHA-256 checksums are generated for all release artifacts and published alongside the binaries",
            message: "Artifact checksum generation is not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "checksum",
                    "sha-256",
                    "sha256",
                    "hash",
                    "artifact",
                    "generate",
                    "publish",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-017",
            description: "Auto-update manifest generation is defined",
            condition: "section defines how the auto-update manifest (latest.yml, latest-mac.yml, latest-linux.yml) is generated and published for each platform",
            message: "Auto-update manifest generation is not defined",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "auto-update",
                    "manifest",
                    "latest.yml",
                    "latest-mac",
                    "latest-linux",
                    "generate",
                    "publish",
                ]),
                patterns: None,
            },
        },
        // ── Platform-Specific Packaging Details ──
        AuditRule {
            id: "build-sec-packaging-018",
            description: "Windows installer options are defined",
            condition: "section defines NSIS/MSI installer options: installation directory, per-user vs machine install, uninstaller, Start Menu shortcuts, file associations, protocol handlers",
            message: "Windows installer options are not defined",
            severity: Severity::Warning,
            weight: 0.9,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "installer",
                    "nsis",
                    "msi",
                    "directory",
                    "per-user",
                    "machine",
                    "uninstall",
                    "shortcut",
                    "protocol",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-019",
            description: "macOS DMG layout is defined",
            condition: "section defines DMG layout: background image, icon positioning, symlink to Applications folder, window size, and license file",
            message: "macOS DMG layout is not defined",
            severity: Severity::Warning,
            weight: 0.7,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "dmg",
                    "background",
                    "icon",
                    "applications",
                    "symlink",
                    "window",
                    "license",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-020",
            description: "Linux desktop integration is defined",
            condition: "section defines Linux desktop integration: .desktop file with correct categories, MIME type associations, icon theme integration, and session autostart options",
            message: "Linux desktop integration is not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "desktop",
                    "file",
                    "mime",
                    "icon theme",
                    "autostart",
                    "category",
                    "session",
                ]),
                patterns: None,
            },
        },
        // ── Bundle Size & Optimization ──
        AuditRule {
            id: "build-sec-packaging-021",
            description: "Bundle size limits are defined",
            condition: "section defines maximum bundle size per platform with enforcement thresholds and blocking behavior when limits are exceeded",
            message: "Bundle size limits are not defined",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "bundle",
                    "size",
                    "limit",
                    "threshold",
                    "block",
                    "enforce",
                    "megabyte",
                    "mb",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-022",
            description: "Dependency tree analysis is defined",
            condition: "section defines dependency tree analysis to detect unnecessary large dependencies, native module duplication, and duplicate Electron runtime copies",
            message: "Dependency tree analysis is not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "dependency",
                    "tree",
                    "analyze",
                    "duplicate",
                    "native",
                    "unnecessary",
                    "large",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-023",
            description: "Native module prebuild strategy is defined",
            condition: "section defines the prebuild or prebuildify strategy for native modules to avoid compiling from source during packaging on each target platform",
            message: "Native module prebuild strategy is not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(80),
                keywords: Some(vec![
                    "prebuild",
                    "prebuildify",
                    "native",
                    "module",
                    "compile",
                    "binary",
                    "strategy",
                ]),
                patterns: None,
            },
        },
        // ── Build Pipeline Integration ──
        AuditRule {
            id: "build-sec-packaging-024",
            description: "Packaging CI pipeline is defined",
            condition: "section defines the CI pipeline for packaging including build triggers, matrix builds per platform, artifact upload, and release publication",
            message: "Packaging CI pipeline is not defined",
            severity: Severity::Error,
            weight: 1.2,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "ci",
                    "pipeline",
                    "trigger",
                    "matrix",
                    "artifact",
                    "upload",
                    "release",
                    "publish",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-025",
            description: "Packaging build reproducibility is defined",
            condition: "section defines how builds are made reproducible: locked dependency versions, deterministic Electron version, pinned toolchain, and reproducibility verification",
            message: "Packaging build reproducibility is not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "reproducible",
                    "locked",
                    "dependency",
                    "pinned",
                    "toolchain",
                    "deterministic",
                    "verify",
                ]),
                patterns: None,
            },
        },
        AuditRule {
            id: "build-sec-packaging-026",
            description: "Packaging test verification is defined",
            condition: "section defines post-packaging verification: install/uninstall test, launch test, basic functionality smoke test, and signature verification on each platform",
            message: "Packaging test verification is not defined",
            severity: Severity::Error,
            weight: 1.1,
            mandatory: true,
            evidence: Evidence::ContentCheck {
                min_length: Some(120),
                keywords: Some(vec![
                    "verify",
                    "install",
                    "uninstall",
                    "launch",
                    "smoke",
                    "signature",
                    "test",
                    "platform",
                ]),
                patterns: None,
            },
        },
        // ── Storage Domain Packaging ──
        AuditRule {
            id: "build-sec-packaging-027",
            description: "Storage domain directory packaging is defined",
            condition: "section defines how storage domain directories are initialized on first launch with correct platform-specific paths and default data",
            message: "Storage domain directory packaging is not defined",
            severity: Severity::Warning,
            weight: 0.8,
            mandatory: false,
            evidence: Evidence::ContentCheck {
                min_length: Some(100),
                keywords: Some(vec![
                    "storage",
                    "domain",
                    "directory",
                    "initialize",
                    "first launch",
                    "platform",
                    "default",
                ]),
                patterns: None,
            },
        },
        // ── Cross-References ──
        AuditRule {
            id: "build-sec-packaging-028",
            description: "Packaging references Engineering Documentation",
            condition: "section references Engineering Documentation build standards and CI/CD configuration",
            message: "Packaging does not reference Engineering Documentation",
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
            id: "build-sec-packaging-029",
            description: "Packaging references Security Documentation",
            condition: "section references Security Documentation code signing and supply chain security requirements",
            message: "Packaging does not reference Security Documentation",
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
            id: "build-sec-packaging-030",
            description: "Packaging references External Context Documentation",
            condition: "section references External Context Documentation platform distribution requirements and store guidelines",
            message: "Packaging does not reference External Context Documentation",
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
        assert!(rules.len() >= 30, "Expected at least 30 rules, got {}", rules.len());
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
        assert_eq!(meta.domain, "build");
        assert_eq!(meta.section_type, "packaging");
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
