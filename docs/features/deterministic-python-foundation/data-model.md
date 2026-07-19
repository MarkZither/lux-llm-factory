# Data Model: Deterministic Python and Environment Foundation

- **Created on**: 2026-07-18
- **Status**: Draft
- **Related spec**: [spec.md](./spec.md)
- **Related plan**: [plan.md](./plan.md)

## Purpose

Define the conceptual entities needed to enforce deterministic setup, dependency identity, and canonical execution behavior.

## Entities

### EnvironmentPolicy

Defines authoritative policy for runtime, virtual environment, dependency governance, and source constraints.

| Field | Type | Required | Description |
|------|------|----------|-------------|
| policy_version | string | Yes | Version identifier for policy lifecycle |
| python_baseline | string | Yes | Required Python baseline declaration |
| supported_profiles | list | Yes | Allowed environment profiles and support tier |
| dependency_policy | object | Yes | Pin or constraint rules by dependency group |
| source_policy | object | Yes | Allowed dependency sources and trust rules |
| change_control | object | Yes | Rules for policy updates and review |

### EnvironmentProfile

Represents an execution context under the common policy contract.

| Field | Type | Required | Description |
|------|------|----------|-------------|
| profile_id | string | Yes | Unique profile key such as local-cpu or runpod |
| support_level | enum | Yes | Baseline required or optional |
| compute_class | string | Yes | High level compute capability descriptor |
| constraints | list | Yes | Platform limitations and expected caveats |
| policy_version | string | Yes | Linked policy version |

### DependencyRule

Describes version intent and governance for a dependency group.

| Field | Type | Required | Description |
|------|------|----------|-------------|
| group_name | string | Yes | Logical dependency group identifier |
| rule_type | enum | Yes | Pinned or constrained |
| version_expression | string | Yes | Version declaration |
| rationale | string | Yes | Why this rule type was chosen |
| criticality | enum | Yes | Core or optional |

### LockManifest

Captures resolved dependency identity for deterministic setup.

| Field | Type | Required | Description |
|------|------|----------|-------------|
| lock_version | string | Yes | Lock schema version |
| resolver_identity | string | Yes | Canonical resolver identity |
| package_entries | list | Yes | Resolved package set |
| source_digest | string | Yes | Digest of source context |
| manifest_digest | string | Yes | Stable identity digest |

### SetupOutcome

Records the result of a setup attempt and its conformance state.

| Field | Type | Required | Description |
|------|------|----------|-------------|
| run_id | string | Yes | Unique setup attempt identifier |
| timestamp | datetime | Yes | Setup completion timestamp |
| profile_id | string | Yes | Applied environment profile |
| policy_version | string | Yes | Applied policy version |
| lock_digest | string | Yes | Used lock identity digest |
| conformance_result | enum | Yes | Pass or fail |
| violations | list | No | Detected rule violations |

## Relationships

| Source entity | Relationship | Target entity | Rule |
|---------------|--------------|---------------|------|
| EnvironmentPolicy | governs | EnvironmentProfile | A profile must reference exactly one policy version |
| EnvironmentPolicy | defines | DependencyRule | All core dependency groups must have a rule |
| DependencyRule | constrains | LockManifest | Lock entries must satisfy declared rules |
| EnvironmentProfile | scopes | SetupOutcome | Setup outcome is produced under one profile |
| LockManifest | proves | SetupOutcome | Successful setup must include a matching lock digest |

## Lifecycle States

### EnvironmentPolicy state

- Draft
- Approved
- Superseded

### LockManifest state

- Generated
- Validated
- Replaced

### SetupOutcome state

- InProgress
- Success
- Failed

## Integrity Rules

1. A successful setup outcome requires both policy compliance and lock digest validation.
2. A profile cannot be baseline required unless it has documented constraints and policy linkage.
3. A core dependency group cannot exist without a declared dependency rule.
4. Any policy version change requires an explicit version increment.

## Traceability to Requirements

| Requirement | Data model support |
|-------------|--------------------|
| FR-001 | EnvironmentProfile, SetupOutcome |
| FR-002 | EnvironmentPolicy |
| FR-003 | EnvironmentPolicy, EnvironmentProfile |
| FR-004 | DependencyRule, LockManifest |
| FR-005 | DependencyRule |
| FR-006 | SetupOutcome with command-linked execution record |
| FR-007 | Policy and profile entities exposed through canonical documentation |
| FR-008 | SetupOutcome failure state and violations |

## Open Model Decisions

| Topic | Decision needed |
|------|------------------|
| lock manifest schema detail | Exact package entry fields and hash strategy |
| setup outcome retention | How long setup outcomes are retained in project workflow |
| profile constraints taxonomy | Standard vocabulary for environment limits |
