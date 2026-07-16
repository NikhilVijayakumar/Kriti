use serde::{Deserialize, Serialize};

/// Desktop service architecture deterministic audit.
///
/// Validates three-process model compliance (Main, Renderer, Preload),
/// IPC channel design, service registry patterns, and process isolation
/// guarantees. A desktop application built on Electron relies on strict
/// separation of concerns across its process boundaries: the Main process
/// owns OS integration, lifecycle, and privileged operations; the Renderer
/// process owns UI rendering and user interaction; the Preload process
/// serves as the trusted bridge between the two via contextBridge.

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
    pub const fn desktop_service_architecture() -> Self {
        Self {
            system_id: "electron_dev",
            domain: "architecture",
            section_type: "desktop_service_architecture",
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
    #[serde(rename = "cross_section_check")]
    CrossSectionCheck {
        requires_section: String,
        coverage: String,
    },
    #[serde(rename = "keyword_absence")]
    KeywordAbsence { categories: Vec<String> },
    #[serde(rename = "diagram_presence")]
    DiagramPresence { kinds: Vec<String> },
    #[serde(rename = "structural_check")]
    StructuralCheck {
        min_paragraphs: Option<usize>,
        min_diagrams: Option<usize>,
        required_subsections: Option<Vec<String>>,
    },
    #[serde(rename = "content_check")]
    ContentCheck { keywords: Vec<String> },
    #[serde(rename = "content_deduplication")]
    ContentDeduplication { scope: String, field: String },
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
// Rule definitions: three-process model
// ---------------------------------------------------------------------------

/// Rule: Three-process model (Main, Renderer, Preload) is explicitly
/// documented with ownership boundaries for each process.
pub const RULE_PROCESS_MODEL_DOCUMENTED: AuditRule = AuditRule {
    id: "arch-micro-001",
    description: "Three-process model is documented with explicit ownership for Main, Renderer, and Preload",
    condition: "section contains a Process Model subsection defining Main, Renderer, and Preload with ownership boundaries",
    message: "Desktop Service Architecture is missing the three-process model definition with ownership boundaries",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::SubsectionPresence {
        required: vec![
            "Process Model",
            "Main Process Services",
            "Renderer Process Services",
            "Preload Script Services",
        ],
    },
};

/// Rule: Each process declares what it owns and what it is forbidden from
/// doing. No process can perform operations outside its privilege boundary.
pub const RULE_PROCESS_ISOLATION_BOUNDARIES: AuditRule = AuditRule {
    id: "arch-micro-002",
    description: "Each process declares responsibility boundary with explicit exclusions",
    condition: "every process entry has Responsibility, Isolation Boundary, and Interfaces fields",
    message: "One or more process entries lack responsibility boundaries or exclusion declarations",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::FieldPresence {
        per_entry: FieldPresenceConfig {
            field: "Isolation Boundary",
            allowed_values: None,
        },
    },
};

/// Rule: Main process is documented as owning system access, OS integration,
/// lifecycle management, file system, network, and native modules.
pub const RULE_MAIN_PROCESS_PRIVILEGES: AuditRule = AuditRule {
    id: "arch-micro-003",
    description: "Main process ownership covers OS integration, lifecycle, file system, network, native modules",
    condition: "Main Process Services entry includes OS integration, lifecycle, and privileged operations in its responsibility",
    message: "Main process responsibility boundary does not cover all required privileged operations",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "system access",
            "OS integration",
            "lifecycle",
            "file system",
            "network",
            "native modules",
        ],
    },
};

/// Rule: Renderer process is documented as owning UI rendering and user
/// interaction, with NO direct system access (sandboxed execution).
pub const RULE_RENDERER_SANDBOX: AuditRule = AuditRule {
    id: "arch-micro-004",
    description: "Renderer process responsibility covers UI rendering and user interaction with no direct system access",
    condition: "Renderer Process Services entry explicitly excludes file system, network, and native module access",
    message: "Renderer process does not explicitly exclude privileged operations from its scope",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "UI rendering",
            "user interaction",
            "no direct system access",
            "sandboxed",
        ],
    },
};

/// Rule: Preload script is documented as owning contextBridge API surface
/// and secure channel exposure, with no business logic.
pub const RULE_PRELOAD_BRIDGE_ONLY: AuditRule = AuditRule {
    id: "arch-micro-005",
    description: "Preload script responsibility covers contextBridge API surface and secure channel exposure",
    condition: "Preload Script Services entry defines contextBridge usage and excludes business logic",
    message: "Preload script responsibility does not define its bridge-only role",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "contextBridge",
            "secure channel",
            "API surface",
            "ipcRenderer",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: IPC channel design
// ---------------------------------------------------------------------------

/// Rule: IPC channel naming convention is defined with domain:action pattern,
/// specifying direction (Main->Renderer, Renderer->Main, bidirectional),
/// serialization format, error handling, and timeout.
pub const RULE_IPC_NAMING_CONVENTION: AuditRule = AuditRule {
    id: "arch-micro-006",
    description: "IPC channel design follows documented naming convention (domain:action) with directionality",
    condition: "IPC Channel Design subsection defines naming pattern with domain:action format and direction classification",
    message: "IPC channels lack a documented naming convention with direction classification",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "domain:action",
            "direction",
            "request-response",
            "broadcast",
            "fire-and-forget",
        ],
    },
};

/// Rule: Every IPC channel has a defined pattern (request-response, broadcast,
/// fire-and-forget) with payload type, response type, error type, and timeout.
pub const RULE_IPC_CHANNEL_CONTRACT: AuditRule = AuditRule {
    id: "arch-micro-007",
    description: "Every IPC channel specifies pattern, payload contract, response type, and error handling",
    condition: "IPC Channel Inventory table includes Pattern, Payload Contract, Response Type for every entry",
    message: "One or more IPC channels lack complete contract specification",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::FieldPresence {
        per_entry: FieldPresenceConfig {
            field: "Payload Contract",
            allowed_values: None,
        },
    },
};

/// Rule: No IPC channels use arbitrary naming — all channels follow the
/// domain:action convention with consistent casing.
pub const RULE_NO_ARBITRARY_CHANNELS: AuditRule = AuditRule {
    id: "arch-micro-008",
    description: "No IPC channels use arbitrary naming outside the domain:action convention",
    condition: "all channel names in the inventory match the documented naming pattern",
    message: "IPC channel inventory contains channels that do not follow the naming convention",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::PatternMatch {
        pattern: "^[a-z][a-z0-9-]*:[a-z][a-z0-9-]*$",
        allowed_values: None,
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: service registry
// ---------------------------------------------------------------------------

/// Rule: Service registry exists as a structured artifact enumerating all
/// services, their host process, exposed IPC interface, and lifecycle state.
pub const RULE_SERVICE_REGISTRY_EXISTS: AuditRule = AuditRule {
    id: "arch-micro-009",
    description: "Service registry exists as a structured artifact enumerating all services",
    condition: "Service Registry subsection contains a registered services table with Service Name, Factory, Dependencies, and Lifecycle Scope",
    message: "Service registry is missing or does not enumerate all services",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "register",
            "resolve",
            "dispose",
            "singleton",
            "factory",
        ],
    },
};

/// Rule: Each registered service declares its host process, dependencies,
/// and lifecycle scope (process / window / app).
pub const RULE_SERVICE_METADATA: AuditRule = AuditRule {
    id: "arch-micro-010",
    description: "Each registered service declares host process, dependencies, and lifecycle scope",
    condition: "every service entry in the registry has Factory, Dependencies, and Lifecycle Scope fields",
    message: "One or more registered services lack dependency or lifecycle scope declarations",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::FieldPresence {
        per_entry: FieldPresenceConfig {
            field: "Lifecycle Scope",
            allowed_values: Some(vec!["process", "window", "app"]),
        },
    },
};

/// Rule: Service lifecycle is documented with four phases: INIT, LOADING,
/// COMPLETED, DISPOSED, including triggers, behavior, and failure modes.
pub const RULE_SERVICE_LIFECYCLE: AuditRule = AuditRule {
    id: "arch-micro-011",
    description: "Service lifecycle defines INIT, LOADING, COMPLETED, DISPOSED phases with failure modes",
    condition: "Service Lifecycle table includes all four lifecycle phases with Trigger, Behavior, and Failure Mode columns",
    message: "Service lifecycle does not define all required phases or is missing failure modes",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "INIT",
            "LOADING",
            "COMPLETED",
            "DISPOSED",
            "Failure Mode",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: process isolation validation
// ---------------------------------------------------------------------------

/// Rule: No Renderer code imports Node.js modules directly — all privileged
/// operations are confined to the Main process.
pub const RULE_RENDERER_NO_NODE: AuditRule = AuditRule {
    id: "arch-micro-012",
    description: "Renderer process does not directly import Node.js modules",
    condition: "Process isolation boundary confirms Renderer has zero file system, network, and native module access",
    message: "Process isolation boundary does not confirm Renderer exclusion from Node.js APIs",
    severity: Severity::Error,
    weight: 2.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "no direct file system",
            "no network",
            "no native modules",
            "sandboxed execution",
        ],
    },
};

/// Rule: All cross-process data flow is traceable through documented IPC
/// channels only — no undocumented backdoor channels, no direct shared
/// state, no electron.remote usage.
pub const RULE_NO_UNDOCUMENTED_CHANNELS: AuditRule = AuditRule {
    id: "arch-micro-013",
    description: "All cross-process data flow is traceable through documented IPC channels only",
    condition: "no references to electron.remote, direct state sharing, or undocumented IPC channels exist",
    message: "Cross-process data flow includes undocumented channels or direct state sharing",
    severity: Severity::Error,
    weight: 1.5,
    mandatory: true,
    evidence: Evidence::KeywordAbsence {
        categories: vec![
            "electron.remote",
            "direct state sharing",
            "undocumented channels",
        ],
    },
};

/// Rule: Configuration lock is documented — configuration is loaded once at
/// INIT and becomes immutable for the service lifetime, preventing runtime
/// state drift between processes.
pub const RULE_CONFIGURATION_LOCK: AuditRule = AuditRule {
    id: "arch-micro-014",
    description: "Configuration lock prevents runtime state drift between processes",
    condition: "Configuration Lock subsection defines load-once, freeze, and no-mutation semantics",
    message: "Configuration lock mechanism is not documented",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "load once",
            "frozen",
            "immutable",
            "no runtime mutation",
            "restart required",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: storage domains
// ---------------------------------------------------------------------------

/// Rule: Storage domains are defined (Local, Vault, Document) with process
/// ownership, purpose, and persistence strategy for each.
pub const RULE_STORAGE_DOMAINS: AuditRule = AuditRule {
    id: "arch-micro-015",
    description: "Storage domains defined with process ownership and persistence strategy",
    condition: "Storage Domains table defines Local, Vault, and Document domains with Process, Purpose, and Persistence columns",
    message: "Storage domains are not defined or are missing process ownership boundaries",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Local",
            "Vault",
            "Document",
            "sessionStorage",
            "encrypted",
            "file system",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: health monitoring and recovery
// ---------------------------------------------------------------------------

/// Rule: Process health monitoring is documented with health check protocol
/// covering Renderer heartbeat, Main responsiveness, and service readiness.
pub const RULE_HEALTH_MONITORING: AuditRule = AuditRule {
    id: "arch-micro-016",
    description: "Process health monitoring covers Renderer heartbeat, Main responsiveness, and service readiness",
    condition: "Health Check Protocol table defines check type, interval, scope, and failure action for each process",
    message: "Process health monitoring is missing or does not cover all process types",
    severity: Severity::Warning,
    weight: 1.0,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Renderer heartbeat",
            "Main responsiveness",
            "service readiness",
            "failure action",
        ],
    },
};

/// Rule: Recovery strategies are defined for Renderer crash, Main hang,
/// IPC channel timeout, and service initialization failure.
pub const RULE_RECOVERY_STRATEGIES: AuditRule = AuditRule {
    id: "arch-micro-017",
    description: "Recovery strategies defined for Renderer crash, Main hang, IPC timeout, and service init failure",
    condition: "Recovery Strategies table covers all four failure scenarios with detection and recovery columns",
    message: "Recovery strategies do not cover all critical failure scenarios",
    severity: Severity::Warning,
    weight: 1.0,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Renderer crash",
            "Main hang",
            "IPC timeout",
            "initialization failure",
            "recovery",
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: process health monitoring ordering
// ---------------------------------------------------------------------------

/// Rule: Initialization order is documented: Main ready -> BrowserWindow
/// created -> Preload loaded -> Renderer hydrated.
pub const RULE_INIT_ORDER: AuditRule = AuditRule {
    id: "arch-micro-018",
    description: "Initialization order documented: Main ready -> BrowserWindow created -> Preload loaded -> Renderer hydrated",
    condition: "service lifecycle or process model defines the sequential initialization order across all three processes",
    message: "Initialization order across Main, Preload, and Renderer is not documented",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Main ready",
            "BrowserWindow created",
            "Preload loaded",
            "Renderer hydrated",
        ],
    },
};

/// Rule: Shutdown order is documented: Renderer teardown -> Preload cleanup
/// -> Main termination.
pub const RULE_SHUTDOWN_ORDER: AuditRule = AuditRule {
    id: "arch-micro-019",
    description: "Shutdown order documented: Renderer teardown -> Preload cleanup -> Main termination",
    condition: "service lifecycle defines the reverse-order shutdown sequence across all three processes",
    message: "Shutdown order across Renderer, Preload, and Main is not documented",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "Renderer teardown",
            "Preload cleanup",
            "Main termination",
            "shutdown",
        ],
    },
};

/// Rule: Service diagram is present showing three processes, service
/// registry in Main, contextBridge boundary, and IPC channels.
pub const RULE_SERVICE_DIAGRAM: AuditRule = AuditRule {
    id: "arch-micro-020",
    description: "Service architecture diagram present showing three processes and IPC channels",
    condition: "section contains or references an architecture diagram depicting process boundaries and IPC channels",
    message: "Desktop Service Architecture lacks a process boundary and IPC channel diagram",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::DiagramPresence {
        kinds: vec![
            "architecture".to_string(),
            "process_boundary".to_string(),
        ],
    },
};

// ---------------------------------------------------------------------------
// Rule definitions: edge cases and advanced patterns
// ---------------------------------------------------------------------------

/// Rule: Native Node addons loaded in Main are documented with their
/// IPC-callable functions and security implications.
pub const RULE_NATIVE_ADDON_DOCS: AuditRule = AuditRule {
    id: "arch-micro-021",
    description: "Native Node addons in Main process are documented with IPC surface and security implications",
    condition: "if native addons exist, they are listed with their IPC-callable functions and isolation guarantees",
    message: "Native Node addons are not documented or lack security review",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "native addon",
            "IPC-callable",
            "security implications",
        ],
    },
};

/// Rule: UtilityProcess usage (Electron 22+) for compute-heavy tasks is
/// documented as a separate process boundary requiring audit.
pub const RULE_UTILITY_PROCESS_BOUNDARY: AuditRule = AuditRule {
    id: "arch-micro-022",
    description: "UtilityProcess for compute-heavy tasks documented as a separate process boundary",
    condition: "if UtilityProcess is used, it is documented with its own responsibility, isolation boundary, and IPC interface",
    message: "UtilityProcess usage is not documented as a separate process boundary",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "UtilityProcess",
            "process boundary",
            "compute",
        ],
    },
};

/// Rule: Services spanning multiple processes have their cross-boundary
/// interface explicitly defined with data serialization boundaries.
pub const RULE_CROSS_PROCESS_INTERFACES: AuditRule = AuditRule {
    id: "arch-micro-023",
    description: "Services spanning multiple processes define cross-boundary interface explicitly",
    condition: "every cross-process service has its interface defined with data serialization boundaries",
    message: "Cross-process services lack explicit interface definitions at process boundaries",
    severity: Severity::Error,
    weight: 1.0,
    mandatory: true,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "cross-boundary",
            "interface",
            "serialization",
            "data boundary",
        ],
    },
};

/// Rule: Service registry includes versioning or compatibility notes for
/// each registered service.
pub const RULE_SERVICE_VERSIONING: AuditRule = AuditRule {
    id: "arch-micro-024",
    description: "Service registry includes versioning or compatibility notes for each registered service",
    condition: "registered services table includes a version or compatibility column",
    message: "Service registry does not include versioning or compatibility information",
    severity: Severity::Warning,
    weight: 0.5,
    mandatory: false,
    evidence: Evidence::ContentCheck {
        keywords: vec![
            "version",
            "compatibility",
            "semver",
            "breaking change",
        ],
    },
};

// ---------------------------------------------------------------------------
// Full audit rule set
// ---------------------------------------------------------------------------

pub fn all_rules() -> Vec<&'static AuditRule> {
    vec![
        &RULE_PROCESS_MODEL_DOCUMENTED,
        &RULE_PROCESS_ISOLATION_BOUNDARIES,
        &RULE_MAIN_PROCESS_PRIVILEGES,
        &RULE_RENDERER_SANDBOX,
        &RULE_PRELOAD_BRIDGE_ONLY,
        &RULE_IPC_NAMING_CONVENTION,
        &RULE_IPC_CHANNEL_CONTRACT,
        &RULE_NO_ARBITRARY_CHANNELS,
        &RULE_SERVICE_REGISTRY_EXISTS,
        &RULE_SERVICE_METADATA,
        &RULE_SERVICE_LIFECYCLE,
        &RULE_RENDERER_NO_NODE,
        &RULE_NO_UNDOCUMENTED_CHANNELS,
        &RULE_CONFIGURATION_LOCK,
        &RULE_STORAGE_DOMAINS,
        &RULE_HEALTH_MONITORING,
        &RULE_RECOVERY_STRATEGIES,
        &RULE_INIT_ORDER,
        &RULE_SHUTDOWN_ORDER,
        &RULE_SERVICE_DIAGRAM,
        &RULE_NATIVE_ADDON_DOCS,
        &RULE_UTILITY_PROCESS_BOUNDARY,
        &RULE_CROSS_PROCESS_INTERFACES,
        &RULE_SERVICE_VERSIONING,
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
        let meta = AuditMetadata::desktop_service_architecture();
        assert_eq!(meta.system_id, "electron_dev");
        assert_eq!(meta.domain, "architecture");
        assert_eq!(meta.section_type, "desktop_service_architecture");
        assert_eq!(meta.kind, "deterministic");
    }

    #[test]
    fn serde_roundtrip() {
        let rule = &RULE_PROCESS_MODEL_DOCUMENTED;
        let json = serde_json::to_string(rule).expect("serialize");
        let deserialized: AuditRule = serde_json::from_str(&json).expect("deserialize");
        assert_eq!(deserialized.id, rule.id);
    }
}
