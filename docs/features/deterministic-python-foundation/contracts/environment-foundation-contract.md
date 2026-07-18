# Contracts: Deterministic Environment Foundation

- **Created on**: 2026-07-18
- **Status**: Draft
- **Related spec**: [../spec.md](../spec.md)
- **Related plan**: [../plan.md](../plan.md)

## Contract Scope

This document defines contract surfaces for setup, validation, and execution behavior and their required inputs and outputs.

## CLI Contracts

### CLI-SETUP-001

| Attribute | Value |
|-----------|-------|
| Purpose | Initialize a contributor environment under policy control |
| Inputs | profile identifier, policy reference, optional clean setup intent |
| Outputs | setup result, policy compliance result, lock identity confirmation |
| Success condition | Environment is ready and policy and lock checks pass |
| Failure condition | Any policy or lock mismatch must return failed setup outcome |
| Invariants | Must not declare success on validation failure |
| Conformance mapping | CC-001, CC-002, CC-003 |

### CLI-VALIDATE-001

| Attribute | Value |
|-----------|-------|
| Purpose | Verify environment conformance without mutating environment state |
| Inputs | existing environment context, policy reference, lock manifest reference |
| Outputs | deterministic pass or fail report with violations |
| Success condition | Environment matches policy and lock expectations |
| Failure condition | Any mismatch produces explicit violation output |
| Invariants | Validation is read-only |
| Conformance mapping | CC-002 |

### CLI-RUN-001

| Attribute | Value |
|-----------|-------|
| Purpose | Execute documented runtime entrypoint after preflight checks |
| Inputs | validated environment and canonical run intent |
| Outputs | runtime invocation result and preflight report |
| Success condition | Runtime starts using validated environment |
| Failure condition | Preflight mismatch blocks execution |
| Invariants | Must enforce preflight checks before run |
| Conformance mapping | CC-004 |

## Configuration Contracts

### CFG-POLICY-001

| Attribute | Value |
|-----------|-------|
| Purpose | Define the canonical environment and dependency governance rules |
| Required keys | policy_version, python_baseline, supported_profiles, dependency_policy, source_policy |
| Validation requirement | Missing required keys is invalid configuration |
| Conformance mapping | FR-002, FR-004, FR-005 |

### CFG-PROFILE-001

| Attribute | Value |
|-----------|-------|
| Purpose | Define an environment profile under one policy contract |
| Required keys | profile_id, support_level, compute_class, constraints, policy_version |
| Validation requirement | profile policy version must exist and be active |
| Conformance mapping | FR-001, FR-003 |

### CFG-LOCK-001

| Attribute | Value |
|-----------|-------|
| Purpose | Capture deterministic dependency identity for setup validation |
| Required keys | lock_version, resolver_identity, package_entries, manifest_digest |
| Validation requirement | Digest mismatch is hard failure |
| Conformance mapping | FR-004, FR-008 |

## Documentation Contracts

### DOC-SETUP-001

| Attribute | Value |
|-----------|-------|
| Purpose | Guarantee one canonical setup flow in contributor documentation |
| Requirement | Documentation presents one official setup sequence |
| Prohibited behavior | Hidden or alternate undocumented setup path |
| Conformance mapping | CC-001, CC-004 |

### DOC-CMD-001

| Attribute | Value |
|-----------|-------|
| Purpose | Guarantee stable command discoverability for setup and run |
| Requirement | Commands documented in one authoritative location |
| Validation | Command references in docs match supported command contract |
| Conformance mapping | FR-006, FR-007 |

## Error Contract

| Error category | Trigger | Required response |
|---------------|---------|-------------------|
| PolicyViolation | Environment does not satisfy policy contract | Fail setup or validation with explicit rule identifier |
| LockMismatch | Lock digest does not match expected identity | Fail setup or validation and mark environment not ready |
| ProfileUnsupported | Profile is not in supported profile list | Fail before setup mutation |
| PreflightFailure | Runtime preflight checks fail | Block runtime entry and report actionable next step |

## Compatibility Contract

- All profile tiers must use the same policy and lock governance model.
- Optional profile support does not allow bypass of canonical setup and validation contracts.
- Changes to contract IDs require explicit update of conformance traceability in the feature artifacts.

## Traceability Matrix

| Contract ID | Requirements | Conformance cases |
|-------------|--------------|-------------------|
| CLI-SETUP-001 | FR-001, FR-004, FR-008 | CC-001, CC-002, CC-003 |
| CLI-VALIDATE-001 | FR-004, FR-005, FR-008 | CC-002 |
| CLI-RUN-001 | FR-006, FR-007 | CC-004 |
| CFG-POLICY-001 | FR-002, FR-004, FR-005 | CC-001, CC-002 |
| CFG-PROFILE-001 | FR-001, FR-003 | CC-001 |
| CFG-LOCK-001 | FR-004, FR-008 | CC-001, CC-002 |
| DOC-SETUP-001 | FR-007 | CC-001, CC-004 |
| DOC-CMD-001 | FR-006, FR-007 | CC-004 |
