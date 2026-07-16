# Feature Technical Design Document — Generation Template

> **Domain:** feature-technical
> **Source standard:** `documentation-standards/10-feature-technical-standards.md`
> **Coherence source:** `audit/semantic/document/10-feature-technical.md`
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate a complete Feature Technical Design document for a system feature. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | ✓ | Definition of Feature Technical Design; one-to-one relationship with Feature; boundary with Architecture |
| 2 | Participating Components | `participating_components` | ✓ | List of components with brief purpose for each |
| 3 | Component Interactions | `component_interactions` | ✓ | Each interaction with triggering condition, nature of exchange, and expected outcome |
| 4 | Data Ownership | `data_ownership` | ✓ | Ownership assignment, read/write access, and access constraints per data element |
| 5 | Feature Specification | `feature_specification` | | Reference to exactly one Feature Specification by name |
| 6 | Component Responsibilities | `component_responsibilities` | | Primary responsibility per participating component |
| 7 | Runtime Behavior | `runtime_behavior` | | Runtime lifecycle: initialization, execution flow, state transitions, shutdown |
| 8 | Communication Paths | `communication_paths` | | Direction, nature, and architectural protocol for each path |
| 9 | Integration Points | `integration_points` | | Each integration point with systems involved, nature, and boundary type |
| 10 | External Dependency Integration | `external_dependencies` | | Dependency name, role in feature, nature of integration, constraints imposed |
| 11 | Runtime Constraints | `runtime_constraints` | | Operational constraints: concurrency limits, resource boundaries, requirements |
| 12 | Architectural Constraints | `architectural_constraints` | | Architecture source principle and application to this feature |
| 13 | Security Considerations | `security_considerations` | | Security boundaries, authentication requirements, authorization rules |
| 14 | Performance Considerations | `performance_considerations` | | Performance expectations, throughput, latency constraints at architectural level |
| 15 | Failure Handling | `failure_handling` | | Failure modes per interaction, error propagation paths, recovery strategies |
| 16 | Extension Points | `extension_points` | | Extension points with type and constraints on extensions |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/10-feature-technical.md` Engineering Intent.

Participating Components, Component Interactions, Data Ownership, and Runtime Behavior must describe the same feature realization without contradicting each other. Specifically:

- Every component in Component Interactions must be defined in Participating Components
- Every data element owner in Data Ownership must be a component from Participating Components
- Every interaction in Runtime Behavior must trace to a Component Interaction
- Communication Paths must connect components that Participating Components defines as adjacent
- Component names must be used identically everywhere they appear across all sections
- The collection as a whole must read as one technical design, not several independent descriptions

If any section would introduce a component, data path, or interaction not present in another section, reconcile before outputting.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

> **Feature Technical Design purpose:** [1-2 sentences: what this Feature Technical Design defines — how the system architecture realizes this specific feature]

> **Scope boundaries:**
> - **In scope:** [architectural concerns this document covers for this feature]
> - **Out of scope:** [concerns explicitly excluded, with the owning standard identified]

> **One-to-one relationship:** This Feature Technical Design corresponds to exactly one Feature Specification: [Feature name].
```

> **Generation note:** When generating for a specific system, fill this template with *that feature's* technical design purpose: how the architecture realizes this feature and what it intentionally excludes. The meta-level "This document defines the standard for Feature Technical Design Documentation..." language belongs in the standard itself, not in a generated document.

**Correct example:**
> **Feature Technical Design purpose:** This Feature Technical Design defines how the Authentication Feature is realized architecturally — credential validation, session management, and security boundary enforcement across the Identity, Session, and API Gateway components.
>
> **Scope boundaries:**
> - **In scope:** Component responsibilities, interaction patterns, data ownership, security boundaries for authentication
> - **Out of scope:** User login UX (Feature Design), password storage algorithms (Engineering), OAuth provider selection (Architecture)
>
> **One-to-one relationship:** This Feature Technical Design corresponds to exactly one Feature Specification: User Authentication.

**Incorrect example:**
> Feature Technical Design covers all features in the system, including User Authentication, Order Processing, Payment Handling, and Notification Delivery. It combines shared architecture with feature-specific requirements into a single comprehensive document.
> *Why wrong: violates the one-to-one relationship principle — must correspond to exactly one Feature Specification.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Define Feature Technical Design in relation to the documentation ecosystem; explicitly state what it is not; maintain the one-to-one mapping constraint throughout
- **Don't:** Drift into implementation specifics; conflate with Architecture or Feature Design; list features or technologies

---

### 2. Participating Components

**Template:**

```markdown
## Participating Components

[Component list or table: each participating component with a brief statement of why it is involved]

| Component | Reason for Participation |
|---|---|
| [Component Name from Architecture] | [why this component is involved in this feature] |
| ... | ... |

[Optional paragraph: relationship to Architecture component model]

### Component Diagram
[Diagram showing participating components and their relationships]
```

**Correct example:**
> | Component | Reason for Participation |
> |---|---|
> | Authentication Component | Validates user credentials and manages session lifecycle for the login feature |
> | Data Component | Stores and retrieves user account data required for authentication |
> | Notification Component | Delivers security alerts triggered by authentication events |
> | UI Component | Presents the login interface and communicates user input to the Authentication Component |

**Incorrect example:**
> | Component | Technology |
> |---|---|
> | AuthService | Node.js microservice using Express framework |
> | UserDatabase | PostgreSQL 15 with TypeORM |
> | EmailSender | Nodemailer with SMTP transport |
> | LoginView | React 18 with TypeScript |
> *Why wrong: lists implementation technologies rather than architectural components with their purpose for participation.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Use component names from Architecture Documentation; state the reason each component participates; include a component diagram
- **Don't:** List technologies, frameworks, or library names; describe component internals; include components not directly involved in the feature

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** component diagram showing participating components
**Required cross-references:** Architecture component model, Feature Specification

---

### 3. Component Interactions

**Template:**

```markdown
## Component Interactions

[Interaction list: each interaction with triggering condition, nature of exchange, and expected outcome]

### [Interaction Name]
- **Triggering condition:** [what initiates this interaction]
- **Nature of exchange:** [synchronous request, asynchronous event, etc.]
- **Expected outcome:** [what happens as a result]

### [Interaction Name]
- **Triggering condition:** [what initiates this interaction]
- **Nature of exchange:** [synchronous request, asynchronous event, etc.]
- **Expected outcome:** [what happens as a result]

### Interaction Diagram
[Sequence diagram showing component interactions]
```

**Correct example:**
> **Interaction: Order Submission**
> - Triggering condition: User submits an order through the UI Component
> - Nature of exchange: UI Component sends a synchronous request to the Order Component; Order Component validates and delegates payment to the Payment Component
> - Expected outcome: Order is created in Submitted state; payment is initiated; user receives confirmation or rejection

**Incorrect example:**
> **Interaction: Order Submission**
> - The React `OrderForm` component calls `POST /api/orders` using axios
> - Express router passes to `OrderController.submit()` which calls `OrderService.process()`
> *Why wrong: describes implementation-level details rather than architectural component interactions.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** State the triggering condition, nature of exchange, and expected outcome for each interaction; trace every interaction to a Feature Specification behavior; include a sequence diagram
- **Don't:** Name specific classes, methods, or API endpoints; describe serialization formats or protocols; use implementation-level communication details

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** sequence diagram showing component interactions
**Required cross-references:** Participating Components, Feature Specification, Architecture communication model

---

### 4. Data Ownership

**Template:**

```markdown
## Data Ownership

[Data ownership table: each data element with owner component, read access, write access, and constraints]

| Data Element | Owner | Read Access | Write Access | Constraints |
|---|---|---|---|---|
| [element] | [owning component] | [who can read] | [who can write] | [architectural constraints] |
| ... | ... | ... | ... | ... |

### Data Ownership Diagram
[ER diagram showing data ownership boundaries]
```

**Correct example:**
> | Data Element | Owner | Read Access | Write Access | Constraints |
> |---|---|---|---|---|
> | User Credentials | Authentication Component | Authentication Component only | Authentication Component only | Must not be exposed outside security boundary |
> | Order Records | Order Component | Order Component, Notification Component (read-only) | Order Component only | Order state transitions follow the lifecycle defined in Runtime Behavior |

**Incorrect example:**
> | Data Element | Table | Column | Type |
> |---|---|---|---|
> | User Credentials | users | password_hash | VARCHAR(255) |
> *Why wrong: describes database schema details rather than component ownership and access boundaries.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Assign one owning component per data element; define read and write access boundaries explicitly; reference Architecture ownership rules; include an ER diagram
- **Don't:** Describe database schemas, column types, or ORM mappings; allow multiple owners for the same data element; use implementation-specific storage details

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** ER diagram showing data ownership boundaries
**Required cross-references:** Architecture ownership rules, Participating Components

---

### 5. Feature Specification

**Template:**

```markdown
## Feature Specification

[Feature reference: name of the Feature Specification and brief confirmation that scope matches]

This Feature Technical Design realizes the **[Feature Name]** Feature Specification. The scope of this design covers [scope summary] — matching the Feature's defined scope. No additional features are addressed in this document.
```

**Correct example:**
> This Feature Technical Design realizes the **User Authentication** Feature Specification. The scope of this design covers credential validation, session management, and secure access — matching the Feature's defined scope. No additional features are addressed in this document.

**Incorrect example:**
> This Feature Technical Design realizes the **User Authentication** Feature Specification, which requires: users must be able to log in with email and password, reset passwords via email link, enable two-factor authentication, and manage session devices. The login form must validate input in real time and show inline error messages.
> *Why wrong: duplicates Feature Specification content rather than referencing the Feature by name and confirming scope alignment.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Reference the Feature by exact name; confirm scope alignment; state that no additional features are addressed
- **Don't:** Duplicate Feature requirements, acceptance criteria, or user stories; paraphrase Feature content; list multiple Feature Specifications

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Feature(04)

---

### 6. Component Responsibilities

**Template:**

```markdown
## Component Responsibilities

[Responsibility list: each participating component with its primary responsibility and alignment with Architecture]

### [Component Name]
- **Primary responsibility:** [what this component is responsible for in this feature]
- **Alignment with Architecture:** [how this responsibility aligns with Architecture ownership rules]
- **Boundary:** [what this component must not do]

### [Component Name]
- **Primary responsibility:** [what this component is responsible for in this feature]
- **Alignment with Architecture:** [how this responsibility aligns with Architecture ownership rules]
- **Boundary:** [what this component must not do]

### Responsibility Diagram
[Component diagram showing responsibility assignments]
```

**Correct example:**
> **Authentication Component:**
> - Primary responsibility: Validating user credentials and issuing session tokens
> - Alignment with Architecture: Operates within the security boundary defined in Architecture
> - Boundary: Must not store user profile data — that belongs to the Data Component
>
> **Data Component:**
> - Primary responsibility: Storing and retrieving user account information
> - Alignment with Architecture: Owns all account data per Architecture ownership rules
> - Boundary: No other component may write account data directly

**Incorrect example:**
> **Authentication Component:** The `AuthService` class extends `BaseAuth` and implements the `login()` method using bcrypt.compare() for password verification.
> *Why wrong: describes class hierarchies and specific method implementations rather than architectural responsibilities and ownership boundaries.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Assign a primary responsibility to every participating component; ensure responsibilities do not overlap; align each responsibility with Architecture ownership rules; include a component diagram
- **Don't:** Describe class hierarchies, method signatures, or library usage; assign shared ownership; leave any participating component without a defined responsibility

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** component diagram showing responsibility assignments
**Required cross-references:** Participating Components, Architecture component model

---

### 7. Runtime Behavior

**Template:**

```markdown
## Runtime Behavior

[Lifecycle description: initialization, execution flow, state transitions, and shutdown at the architectural level]

### Initialization
[How components start and register with the system]

### Execution Flow
[How components process requests and produce responses]

### State Transitions
[How component states change during feature execution]

### Shutdown
[How components gracefully stop]

### Runtime Lifecycle Diagram
[Flowchart showing runtime lifecycle and state transitions]
```

**Correct example:**
> **Lifecycle: Order Processing**
> 1. **Initialization:** The Order Component starts and registers with the Event Bus. It subscribes to order submission events.
> 2. **Execution Flow:** When an order submission event arrives, the Order Component validates the request, delegates payment to the Payment Component, and updates order state.
> 3. **State Transitions:** An order moves through states: Submitted → Validated → PaymentPending → Confirmed → Completed (or Failed).
> 4. **Shutdown:** The Order Component unsubscribes from the Event Bus and completes any in-flight order processing before terminating.

**Incorrect example:**
> 1. Initialize Spring Boot application context and connect to RabbitMQ using `amqp://guest:guest@localhost:5672`.
> 2. `OrderService.processOrder()` method validates input, calls `PaymentClient.charge()`, then `OrderRepository.save()`.
> *Why wrong: describes Spring Boot initialization, connection strings, and specific method names rather than architectural runtime lifecycle.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Describe the full lifecycle — initialization, execution flow, state transitions, and shutdown — at the architectural level; define each state and valid transitions; include a flowchart
- **Don't:** Name specific runtime frameworks, connection strings, or configuration files; describe threading or process models; use implementation-level lifecycle hooks

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** flowchart showing runtime lifecycle and state transitions
**Required cross-references:** Component Interactions, Architecture runtime boundaries

---

### 8. Communication Paths

**Template:**

```markdown
## Communication Paths

[Communication path list: each path with direction, nature, and architectural protocol]

### [Source Component] → [Destination Component]
- **Direction:** [outbound/inbound]
- **Nature:** [synchronous request, asynchronous event, etc.]
- **Architectural protocol:** [reference to Architecture communication model]

### [Source Component] → [Destination Component]
- **Direction:** [outbound/inbound]
- **Nature:** [synchronous request, asynchronous event, etc.]
- **Architectural protocol:** [reference to Architecture communication model]

### Communication Diagram
[Sequence diagram showing communication paths]
```

**Correct example:**
> **Order Component → Notification Component**
> - Direction: Outbound from Order to Notification
> - Nature: Asynchronous event publication — order completion triggers notification delivery
> - Architectural protocol: Event Bus (as defined in Architecture communication model)
>
> **UI Component → Order Component**
> - Direction: Inbound request from UI to Order
> - Nature: Synchronous request — UI submits order and awaits confirmation
> - Architectural protocol: REST Gateway (as defined in Architecture communication model)

**Incorrect example:**
> **Order Component → Notification Component**
> - Direction: POST request to `https://notification-service/internal/events`
> - Nature: JSON payload with order ID and status fields
> *Why wrong: describes HTTP methods, URLs, and payload formats rather than architectural communication path direction, nature, and protocol reference.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Define direction, nature, and architectural protocol for every communication path; trace each path to a Component Interaction; reference the Architecture communication model
- **Don't:** Specify HTTP methods, URLs, or payload schemas; describe serialization or wire formats; use library-specific communication patterns

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** sequence diagram showing communication paths
**Required cross-references:** Component Interactions, Architecture communication model

---

### 9. Integration Points

**Template:**

```markdown
## Integration Points

[Integration list: each integration point with systems involved, nature, and boundary type]

### [Integration Name]
- **Systems involved:** [component(s) and external system]
- **Nature:** [synchronous request-response, asynchronous event, etc.]
- **Boundary type:** [Internal, External, Third-party]

### [Integration Name]
- **Systems involved:** [component(s) and external system]
- **Nature:** [synchronous request-response, asynchronous event, etc.]
- **Boundary type:** [Internal, External, Third-party]

### Integration Diagram
[Component diagram showing integration boundaries]
```

**Correct example:**
> **Integration Point: Payment Processing**
> - Systems involved: Order Component and external Payment Processor
> - Nature: Synchronous request-response for transaction authorization
> - Boundary type: External — crosses the system boundary to a third-party service

**Incorrect example:**
> **Integration Point: Payment Processing**
> - Call `POST https://api.paymentprocessor.com/v2/charge` with API key in `Authorization: Bearer` header
> *Why wrong: describes API endpoint URLs and HTTP headers rather than the architectural integration boundary.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Identify every integration point with systems involved, nature of integration, and boundary type; classify each as internal, external, or third-party; include a component diagram
- **Don't:** Describe API endpoints, authentication token formats, or request/response schemas; specify retry logic; name client libraries

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** component diagram showing integration boundaries
**Required cross-references:** Feature Specification, Architecture boundaries

---

### 10. External Dependency Integration

**Template:**

```markdown
## External Dependency Integration

[Dependency list: each external dependency with name, role in feature, nature of integration, and constraints imposed]

### [Dependency Name] (reference: [External Context document])
- **Role in feature:** [what this dependency does for the feature]
- **Nature of integration:** [how the system interacts with it]
- **Constraints:** [what constraints this dependency imposes]

### Dependency Diagram
[Component diagram showing external dependencies]
```

**Correct example:**
> **Dependency: Identity Provider** (reference: External Context identity services)
> - Role in feature: Authenticates user credentials during login flow; provides identity verification for protected operations
> - Nature of integration: The Authentication Component delegates credential verification to the Identity Provider
> - Constraints: The Identity Provider requires network connectivity; authentication is unavailable if the provider is unreachable (see Failure Handling)

**Incorrect example:**
> **Dependency: Identity Provider**
> - Use Auth0 SDK v4.2.1 to call the `/oauth/token` endpoint
> - Store refresh tokens in memory using the `auth0-spa-js` library
> *Why wrong: describes SDK versions and library APIs rather than the architectural role of the external dependency.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Reference External Context documents by name; state the role of each dependency in the feature; describe constraints imposed without duplicating External Context content; include a component diagram
- **Don't:** Duplicate External Context content; describe SDK versions or library APIs; specify implementation-level integration patterns

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** component diagram showing external dependencies
**Required cross-references:** External Context, Integration Points

---

### 11. Runtime Constraints

**Template:**

```markdown
## Runtime Constraints

[Constraint list: each operational constraint with source (Architecture or External Context) and application to this feature]

### [Constraint Name] (source: [Architecture or External Context])
[How this constraint applies to this specific feature]

### [Constraint Name] (source: [Architecture or External Context])
[How this constraint applies to this specific feature]
```

**Correct example:**
> **Constraint: Concurrency Limit** (source: Architecture runtime boundaries)
> The Order Processing Component must handle concurrent order submissions without data corruption. The architectural model limits concurrent processing to the resource allocation defined for this component class.
>
> **Constraint: Resource Boundary** (source: External Context platform constraints)
> The feature must operate within the memory and compute boundaries defined by the hosting platform. Component lifecycle must respect the platform's resource management model.

**Incorrect example:**
> **Constraint: Concurrency Limit**
> Use `java.util.concurrent.Semaphore` with permits=10 in the OrderService. Configure Tomcat max threads to 200.
> *Why wrong: specifies implementation-level concurrency tools and server configuration rather than architectural operational constraints.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each constraint as a clear operational limitation; cite the source from Architecture or External Context; explain how the constraint applies to this specific feature
- **Don't:** Specify implementation tools, frameworks, or configuration files; provide performance benchmarks; describe deployment or infrastructure details

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture runtime boundaries, External Context

---

### 12. Architectural Constraints

**Template:**

```markdown
## Architectural Constraints

[Constraint list: each architectural constraint with Architecture source principle and application to this feature]

### [Constraint Name] (source: [Architecture principle])
[How this constraint applies to this specific feature]
```

**Correct example:**
> **Constraint: Component Ownership** (source: Architecture ownership rules)
> Each data element must have exactly one owning component. The Authentication Component owns credential data; no other component may write to it directly.
>
> **Constraint: Communication Model** (source: Architecture communication model)
> All inter-component communication must use the event bus defined in Architecture. Direct component-to-component calls are not permitted.

**Incorrect example:**
> **Constraint: Component Ownership**
> Use a single PostgreSQL database for all component data. Each component writes to its own schema using TypeORM repositories.
> *Why wrong: specifies technology choices and implementation patterns rather than architectural ownership principles.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Reference each architectural constraint by its Architecture source principle; state how the constraint applies to this feature; avoid redefining architectural principles
- **Don't:** Redefine or paraphrase Architecture principles; introduce implementation-level constraints; name technologies or frameworks as constraints

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture principles and constraints

---

### 13. Security Considerations

**Template:**

```markdown
## Security Considerations

[Security list: security boundaries, authentication requirements, authorization rules, and sensitive data identification]

### Security Boundary
[Where trust changes in this feature]

### Authentication
[Authentication requirements for this feature]

### Authorization
[What each component can and cannot access]

### Sensitive Data
[What data is classified as sensitive and how it is protected]
```

**Correct example:**
> **Security Boundary:** The Authentication Component operates within the security boundary defined by Architecture. Only authenticated requests may access the Data Component.
> **Authentication:** Requests from external systems must be validated against the identity provider defined in External Context.
> **Authorization:** The Notification Component may read user preferences but may not modify account data.
> **Sensitive Data:** User credentials and session tokens are classified as sensitive; they must not appear in communication paths that cross the external boundary.

**Incorrect example:**
> Use bcrypt for password hashing with 12 salt rounds. Implement JWT tokens using the jsonwebtoken npm library with RS256 algorithm.
> *Why wrong: specifies implementation-level security details rather than architectural security boundaries and authorization rules.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Define security boundaries, authentication requirements, and authorization rules at the architectural level; identify sensitive data; reference Architecture security boundaries and External Context security constraints
- **Don't:** Name specific encryption algorithms, libraries, or token formats; describe code-level security patterns; specify cookie or header configurations

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture security boundaries, External Context, Security Documentation

---

### 14. Performance Considerations

**Template:**

```markdown
## Performance Considerations

[Performance list: performance expectations, throughput requirements, latency constraints, and resource limitations at the architectural level]

### [Performance Expectation Name]
- **Throughput:** [throughput requirement]
- **Latency constraint:** [latency expectation]
- **Resource limitation:** [resource boundary]
```

**Correct example:**
> **Performance Expectation: Search Response**
> - Throughput: The search component must support concurrent queries from multiple client components without degrading response times
> - Latency constraint: Search results must be available to the UI component within the time expected for interactive use
> - Resource limitation: Search indexing must not consume more than the resource allocation defined in Architecture runtime boundaries

**Incorrect example:**
> Elasticsearch query must complete in under 200ms. Node.js event loop must not be blocked for more than 50ms. Use Redis caching with TTL of 300 seconds.
> *Why wrong: specifies technology-specific benchmarks and implementation details rather than architectural performance expectations.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State performance expectations as architectural constraints traceable to Feature Specification; define throughput, latency, and resource expectations at the system level; reference Architecture performance patterns
- **Don't:** Provide specific latency numbers or benchmarks; name profiling tools or caching libraries; describe optimization techniques or implementation strategies

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Feature Specification, Architecture performance patterns

---

### 15. Failure Handling

**Template:**

```markdown
## Failure Handling

[Failure list: failure modes per interaction, error propagation paths, recovery strategies, and resilience boundaries]

### [Failure Mode Name]
- **Interaction affected:** [which component interaction fails]
- **Propagation:** [how the failure propagates across components]
- **Recovery:** [what happens and how the system recovers]
- **Resilience boundary:** [where failure propagation stops]

### Failure Diagram
[Flowchart showing error propagation and recovery paths]
```

**Correct example:**
> **Failure Mode: External Service Unavailable**
> - Interaction affected: Order Service queries Payment Gateway
> - Propagation: Failure propagates from Payment Gateway to Order Service to Notification Service
> - Recovery: Order Service queues the order for retry; Notification Service informs the user that processing is delayed
> - Resilience boundary: Failure does not propagate beyond Order Service to the User Interface layer

**Incorrect example:**
> Catch `PaymentTimeoutException` in `OrderService.java` line 142. Retry 3 times with exponential backoff using Spring Retry `@Retryable`.
> *Why wrong: describes implementation-level error handling rather than architectural failure modes and recovery strategies.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Define failure modes for every component interaction; trace error propagation paths across architectural boundaries; state recovery strategies and resilience boundaries; include a flowchart
- **Don't:** Name specific exception types, error codes, or try/catch patterns; describe retry implementations or logging frameworks; reference code locations

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** flowchart showing error propagation and recovery paths
**Required cross-references:** Component Interactions, Architecture error boundaries, Component Responsibilities

---

### 16. Extension Points

**Template:**

```markdown
## Extension Points

[Extension list: each extension point with type (plugin, hook, event, configuration) and constraints on extensions]

### [Extension Point Name]
- **Type:** [plugin, hook, event, configuration]
- **Constraint:** [what extensions must or must not do]

### Extension Diagram
[Component diagram showing extension points]
```

**Correct example:**
> **Extension Point: Notification Dispatch**
> - Type: Event hook
> - Constraint: Extensions must implement the notification dispatch contract defined in Architecture plugin model; extensions cannot modify core notification routing

**Incorrect example:**
> **Extension Point: Notification Dispatch**
> - Type: Custom JavaScript class extending BaseNotifier
> - Constraint: Must override onSend() method using the EventEmitter library API
> *Why wrong: specifies implementation-level details rather than architectural extension type and constraints.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Identify extension points with type (plugin, hook, event, configuration) and constraints; reference the Architecture plugin model; ensure extension points are architecturally sound
- **Don't:** Name specific programming languages, class hierarchies, or library APIs; describe callback implementations; define extension mechanisms not present in Architecture

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** component diagram showing extension points
**Required cross-references:** Architecture plugin architecture, Component Responsibilities

## Output Contract

Output a single complete markdown document containing all 16 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
