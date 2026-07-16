use serde::{Deserialize, Serialize};

/// Desktop caching deterministic audit.
///
/// Validates cache strategy, storage domain usage, cache coherence
/// protocols, and cross-process cache consistency. Each Electron process
/// has different caching capabilities and constraints: Main process has
/// full access to memory, disk, and database caches; Renderer is
/// sandboxed with IndexedDB, sessionStorage, and Service Worker caches;
/// Preload must not cache sensitive data. This audit verifies that cache
/// behavior respects storage domain boundaries (Local, Vault, Document),
/// that cross-process coherence is maintained via explicit invalidation
/// protocols, and that cache sizes are bounded with pressure responses.

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
    pub const fn caching() -> Self {
        Self {
            system_id: "electron_dev",
            domain: "engineering",
            section_type: "caching",
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
    #[serde(rename = "content_check")]
    ContentCheck { keywords: Vec<String> },
    #[serde(rename = "keyword_absence")]
    KeywordAbsence { categories: Vec<String> },
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
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FieldPresenceConfig {
    pub field: &'static str,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub allowed_values: Option<Vec<&'static str>>,
}

// ---------------------------------------------------------------------------
// Rule definitions: cache architecture by process
// ---------------------------------------------------------------------------

pub const RULE_CACHE_ARCHITECTURE_EXISTS: AuditRule = AuditRule {
    id: "cache-001",
    description: "Cache Architecture by Process subsection exists with separate Main and Renderer definitions",
    condition: "section contains a Cache Architecture by Process subsection with Main Process Caches and Renderer Process Caches",
    message: "Cache Architecture by Process subsection is missing or does not cover all processes",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::SubsectionPresence {
        required: vec![
            "Cache Architecture by Process",
            "Main Process Caches",
            "Renderer Process Caches",
        ],
    },
};

pub const RULE_MAIN_CACHE_DEFINITIONS: AuditRule = AuditRule {
    id: "cache-002",
    description: "Main process caches define name, storage type, TTL, max size, and eviction policy",
    condition: "Main Process Caches table includes Cache Name, Storage, TTL, Max Size, and Eviction columns for every entry",
    message: "Main process cache definitions are incomplete - missing required columns",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::FieldPresence {
        per_entry: FieldPresenceConfig {
            field: "Eviction",
            allowed_values: Some(vec!["LRU", "LFU", "TTL", "Manual"]),
        },
    },
};

pub const RULE_RENDERER_CACHE_MECHANISMS: AuditRule = AuditRule {
    id: "cache-003",
    description: "Renderer caches use only browser-native storage (IndexedDB, sessionStorage, DOM, Service Worker)",
    condition: "Renderer Process Caches table references only browser-native storage mechanisms",
    message: "Renderer cache definitions reference Node.js storage mechanisms (filesystem, SQLite)",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::KeywordAbsence {
        categories: vec![
            "filesystem_cache",
            "sqlite_in_renderer",
            "node_fs_in_renderer",
        ],
    },
};

pub const RULE_MAIN_CACHE_LIFECYCLE: AuditRule = AuditRule {
    id: "cache-004",
    description: "Main process cache lifecycle follows documented memory -> disk -> source pattern",
    condition: "Main Process Caches includes lifecycle description covering memory check, disk fallback, source fetch, and memory pressure eviction",
    message: "Main process cache lifecycle is not documented",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "memory check",
            "disk fallback",
            "source fetch",
            "memory pressure",
            "eviction",
        ],
    },
};

pub const RULE_PRELOAD_NO_SENSITIVE_CACHE: AuditRule = AuditRule {
    id: "cache-005",
    description: "Preload bridge does not cache sensitive data; freshness validation on bridge returns",
    condition: "Preload Cache Pattern specifies no sensitive data caching and includes staleness indicator on returns",
    message: "Preload bridge cache pattern caches sensitive data or lacks freshness validation",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "no sensitive data",
            "staleness indicator",
            "freshness",
            "timestamp",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: storage domain cache mapping
// ---------------------------------------------------------------------------

pub const RULE_STORAGE_DOMAIN_MAPPING: AuditRule = AuditRule {
    id: "cache-006",
    description: "Storage Domain Cache Mapping table maps Local, Vault, and Document domains to cache locations and invalidation triggers",
    condition: "Storage Domain Cache Mapping table defines Domain, Cache Location, Invalidation Trigger, and Encryption for Local, Vault, and Document",
    message: "Storage domain cache mapping is missing or incomplete",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Local",
            "Vault",
            "Document",
            "Cache Location",
            "Invalidation Trigger",
            "Encryption",
        ],
    },
};

pub const RULE_VAULT_CACHE_RESTRICTIONS: AuditRule = AuditRule {
    id: "cache-007",
    description: "Vault domain caches are minimal-TTL, memory-only, never disk-persistent unencrypted",
    condition: "Vault domain cache rules specify short TTL (session duration or less), memory-only storage, and no unencrypted disk persistence",
    message: "Vault domain cache does not meet security requirements (TTL too long, disk persistence, no encryption)",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "short TTL",
            "memory only",
            "no disk persistence",
            "AES-256",
            "session duration",
        ],
    },
};

pub const RULE_LOCAL_DOMAIN_TTL: AuditRule = AuditRule {
    id: "cache-008",
    description: "Local domain caches use aggressive TTL (hours/days) and survive app restart",
    condition: "Local domain cache rules specify long TTL and persistence across app restarts",
    message: "Local domain cache TTL or persistence is not documented",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "hours",
            "days",
            "survive restart",
            "aggressive caching",
        ],
    },
};

pub const RULE_DOCUMENT_DOMAIN_FRESHNESS: AuditRule = AuditRule {
    id: "cache-009",
    description: "Document domain caches validate freshness on every access with file watcher invalidation",
    condition: "Document domain cache rules specify freshness validation and file watcher-based invalidation",
    message: "Document domain cache does not validate freshness or lacks file watcher invalidation",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "freshness validation",
            "file watcher",
            "every access",
            "fs.watch",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: cross-process cache coherence
// ---------------------------------------------------------------------------

pub const RULE_COHERENCE_PROTOCOL: AuditRule = AuditRule {
    id: "cache-010",
    description: "Cross-process cache coherence protocol is defined with Main as source of truth",
    condition: "Coherence Protocol subsection defines Main as source of truth, Renderer as read-only mirror, and invalidation broadcast via IPC",
    message: "Cross-process cache coherence protocol is not documented",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "source of truth",
            "read-only mirror",
            "invalidation broadcast",
            "IPC",
        ],
    },
};

pub const RULE_INVALIDATION_CHANNELS: AuditRule = AuditRule {
    id: "cache-011",
    description: "Cache invalidation IPC channel (cache:invalidate) defined with domain, keys, and reason payload",
    condition: "cache:invalidate channel definition includes domain, keys, and reason fields in payload",
    message: "Cache invalidation IPC channel is not defined or lacks payload specification",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "cache:invalidate",
            "domain",
            "keys",
            "reason",
        ],
    },
};

pub const RULE_INVALIDATION_TRIGGERS: AuditRule = AuditRule {
    id: "cache-012",
    description: "Invalidation triggers documented for all five types: file change, config update, user logout, DB migration, TTL expiry",
    condition: "invalidation triggers table covers file changed, config updated, user logout, database migrated, and timer expiry",
    message: "Cache invalidation triggers do not cover all required scenarios",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "file changed",
            "config updated",
            "user logout",
            "database migrated",
            "timer expiry",
            "TTL",
        ],
    },
};

pub const RULE_RENDERER_LISTENS_INVALIDATION: AuditRule = AuditRule {
    id: "cache-013",
    description: "Renderer listens for invalidation events and purges local cache entries",
    condition: "coherence protocol specifies Renderer-side invalidation listener that purges local entries and requests fresh data",
    message: "Renderer does not listen for cache invalidation events",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Renderer listens",
            "purge local",
            "request fresh data",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: invalidation strategy
// ---------------------------------------------------------------------------

pub const RULE_INVALIDATION_STRATEGY_TABLE: AuditRule = AuditRule {
    id: "cache-014",
    description: "Cache Invalidation Strategy table defines time-based, event-based, version-based, manual, and LRU eviction",
    condition: "Invalidation Strategy table covers TTL, event-based IPC broadcast, version-based ETag, manual delete, and LRU eviction",
    message: "Cache invalidation strategy does not cover all required invalidation types",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "TTL",
            "event-based",
            "version-based",
            "ETag",
            "manual",
            "LRU",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: cache size management
// ---------------------------------------------------------------------------

pub const RULE_CACHE_SIZE_LIMITS: AuditRule = AuditRule {
    id: "cache-015",
    description: "Cache size management defines default max, growth policy, and pressure response for each cache type",
    condition: "Cache Size Management table includes Default Max, Growth Policy, and Pressure Response for in-memory, disk, IndexedDB, and Service Worker caches",
    message: "Cache size management is missing or does not cover all cache types",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Default Max",
            "Growth Policy",
            "Pressure Response",
            "in-memory",
            "disk",
            "IndexedDB",
            "Service Worker",
        ],
    },
};

pub const RULE_CACHE_PRESSURE_LEVELS: AuditRule = AuditRule {
    id: "cache-016",
    description: "Cache pressure response defines four levels: 70% warning, 85% aggressive eviction, 95% LRU eviction, 100% emergency purge",
    condition: "pressure response defines four escalation levels with specific thresholds and actions",
    message: "Cache pressure response does not define escalation levels",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Level 1",
            "Level 2",
            "Level 3",
            "Level 4",
            "emergency purge",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: offline cache strategy
// ---------------------------------------------------------------------------

pub const RULE_OFFLINE_STRATEGY: AuditRule = AuditRule {
    id: "cache-017",
    description: "Offline cache strategy defines asset type, offline strategy, and pre-cache status for each asset category",
    condition: "Offline Cache Strategy table covers app shell, static assets, API responses, user documents, and real-time data",
    message: "Offline cache strategy does not cover all required asset categories",
    severity: Severity::Warning,
    weight: 1.0,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "app shell",
            "static assets",
            "API responses",
            "user documents",
            "real-time data",
            "cache-first",
            "network-first",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: cache monitoring
// ---------------------------------------------------------------------------

pub const RULE_CACHE_MONITORING: AuditRule = AuditRule {
    id: "cache-018",
    description: "Cache monitoring defines metrics: hit rate, memory usage, disk usage, invalidation lag with thresholds",
    condition: "Cache Monitoring table defines metric, source, threshold, and action for hit rate, memory usage, disk usage, and invalidation lag",
    message: "Cache monitoring is missing or does not cover all required metrics",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "hit rate",
            "memory usage",
            "disk usage",
            "invalidation lag",
            "threshold",
        ],
    },
};

pub const RULE_CACHE_METRICS_REPORTED_VIA_IPC: AuditRule = AuditRule {
    id: "cache-019",
    description: "Cache health metrics are reported to Main process via IPC for diagnostics",
    condition: "cache monitoring includes IPC-based reporting from Renderer to Main for diagnostics",
    message: "Cache health metrics are not reported to Main process",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "IPC report",
            "Main process diagnostics",
            "cache health",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: coherence edge cases
// ---------------------------------------------------------------------------

pub const RULE_MAIN_UNAVAILABLE_FALLBACK: AuditRule = AuditRule {
    id: "cache-020",
    description: "Renderer uses cached data with staleness flag when Main process is unavailable",
    condition: "coherence protocol specifies fallback behavior when Main process is unavailable: use cached data with staleness indicator",
    message: "No fallback behavior defined for Main process unavailability",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Main unavailable",
            "cached data",
            "staleness flag",
            "fallback",
        ],
    },
};

pub const RULE_CACHE_DOMAIN_ISOLATION: AuditRule = AuditRule {
    id: "cache-021",
    description: "Cache entries are isolated by storage domain - no cross-domain cache leakage",
    condition: "cache architecture ensures Local, Vault, and Document cache entries are isolated and cannot leak across domains",
    message: "Cache entries are not isolated by storage domain",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "domain isolation",
            "no cross-domain",
            "cache boundary",
        ],
    },
};

pub const RULE_CACHE_INVALIDATION_ATOMICITY: AuditRule = AuditRule {
    id: "cache-022",
    description: "Cache invalidation is atomic - either all affected entries are purged or none",
    condition: "invalidation protocol guarantees atomic purge of all affected entries within a domain",
    message: "Cache invalidation is not atomic across affected entries",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "atomic purge",
            "all affected entries",
            "consistent state",
        ],
    },
};

pub const RULE_VAULT_CACHE_CLEAR_ON_LOCK: AuditRule = AuditRule {
    id: "cache-023",
    description: "Vault domain cache is cleared on app lock and sleep events",
    condition: "Vault domain cache rules specify clearing on lock event and system sleep",
    message: "Vault domain cache is not cleared on lock or sleep events",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "clear on lock",
            "clear on sleep",
            "vault cache clear",
        ],
    },
};

pub const RULE_CACHE_COHERENCE_TESTED: AuditRule = AuditRule {
    id: "cache-024",
    description: "Cross-process cache coherence is tested with stale-read and invalidation race scenarios",
    condition: "cache tests cover stale-read scenarios, invalidation race conditions, and Main-process-unavailable fallback",
    message: "Cross-process cache coherence lacks test coverage",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "stale-read test",
            "invalidation race",
            "Main unavailable test",
        ],
    },
};

// ---------------------------------------------------------------------------
// Full audit rule set
// ---------------------------------------------------------------------------

pub fn all_rules() -> Vec<&'static AuditRule> {
    vec![
        &RULE_CACHE_ARCHITECTURE_EXISTS,
        &RULE_MAIN_CACHE_DEFINITIONS,
        &RULE_RENDERER_CACHE_MECHANISMS,
        &RULE_MAIN_CACHE_LIFECYCLE,
        &RULE_PRELOAD_NO_SENSITIVE_CACHE,
        &RULE_STORAGE_DOMAIN_MAPPING,
        &RULE_VAULT_CACHE_RESTRICTIONS,
        &RULE_LOCAL_DOMAIN_TTL,
        &RULE_DOCUMENT_DOMAIN_FRESHNESS,
        &RULE_COHERENCE_PROTOCOL,
        &RULE_INVALIDATION_CHANNELS,
        &RULE_INVALIDATION_TRIGGERS,
        &RULE_RENDERER_LISTENS_INVALIDATION,
        &RULE_INVALIDATION_STRATEGY_TABLE,
        &RULE_CACHE_SIZE_LIMITS,
        &RULE_CACHE_PRESSURE_LEVELS,
        &RULE_OFFLINE_STRATEGY,
        &RULE_CACHE_MONITORING,
        &RULE_CACHE_METRICS_REPORTED_VIA_IPC,
        &RULE_MAIN_UNAVAILABLE_FALLBACK,
        &RULE_CACHE_DOMAIN_ISOLATION,
        &RULE_CACHE_INVALIDATION_ATOMICITY,
        &RULE_VAULT_CACHE_CLEAR_ON_LOCK,
        &RULE_CACHE_COHERENCE_TESTED,
    ]
}

pub fn mandatory_rules() -> Vec<&'static AuditRule> {
    all_rules().into_iter().filter(|r| r.mandatory).collect()
}

pub fn recommended_rules() -> Vec<&'static AuditRule> {
    all_rules().into_iter().filter(|r| !r.mandatory).collect()
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
        let meta = AuditMetadata::caching();
        assert_eq!(meta.system_id, "electron_dev");
        assert_eq!(meta.domain, "engineering");
        assert_eq!(meta.section_type, "caching");
        assert_eq!(meta.kind, "deterministic");
    }

    #[test]
    fn serde_roundtrip() {
        let rule = &RULE_CACHE_ARCHITECTURE_EXISTS;
        let json = serde_json::to_string(rule).expect("serialize");
        let deserialized: AuditRule = serde_json::from_str(&json).expect("deserialize");
        assert_eq!(deserialized.id, rule.id);
    }
}