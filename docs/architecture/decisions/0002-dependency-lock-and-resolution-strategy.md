# Dependency Lock and Resolution Strategy

**Status**: Proposed
**Date**: 2026-07-18

## Context

The feature requires deterministic setup identity and intentional pin or constraint policy. The current project defines dependency constraints, but there is no canonical lock artifact and no single update governance path. A formal decision is needed for resolver behavior, lock scope, and policy validation.

## Priorities and Requirements (ordered)

1. **Deterministic dependency identity** — The same declared inputs must produce the same dependency identity.
2. **Controlled and auditable upgrades** — Dependency changes must be intentional, reviewable, and reversible.
3. **Contributor usability** — Setup commands must remain straightforward for first time contributors.

## Options Considered

### Option 1: Single canonical resolver and committed lock artifact with policy validation gate

Use one resolver path as canonical, commit lock artifacts, and require validation before setup success.

**Evaluation against priorities**:
- **Deterministic dependency identity**: Meets. A single resolver plus committed lock artifact provides repeatable resolution.
- **Controlled and auditable upgrades**: Meets. Lock updates become explicit change events with review history.
- **Contributor usability**: Meets. Contributors follow one setup flow without resolver choice ambiguity.

### Option 2: Constraint only policy without committed lock artifacts

Rely on version constraints and resolve dependencies at install time.

**Evaluation against priorities**:
- **Deterministic dependency identity**: Fails. Resolution can drift over time even when constraints are unchanged.
- **Controlled and auditable upgrades**: Partially meets. Constraint edits are reviewable, but transitive drift remains hard to audit.
- **Contributor usability**: Partially meets. Initial setup can appear simple, but drift creates inconsistent failures.

## Decision

Choose Option 1. The project will define one canonical resolver path, commit lock artifacts, and enforce policy validation before setup success is reported. This is the strongest match for deterministic identity and controlled upgrades while preserving a simple contributor flow.

## Implementation Notes (optional)

- Core dependency groups must be explicitly classified as pinned or intentionally constrained.
- Lock update procedures require documented review criteria and rollback guidance.

## References

* [Feature Spec: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/spec.md)
* [Feature Plan: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/plan.md)
