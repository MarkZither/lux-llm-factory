# Canonical Command Contract Versioning

**Status**: Accepted
**Date**: 2026-07-19

## Context

The deterministic environment feature introduces a single contributor command surface for setup, validation, and execution. Without a versioned command contract, documentation drift and hidden command variations can make setup behavior inconsistent across contributors and over time.

## Priorities and Requirements (ordered)

1. **Stable contributor experience** — Contributors must be able to rely on one documented command path.
2. **Safe evolution** — Command contract changes must be explicit and reviewable rather than implicit.
3. **Cross artifact consistency** — Docs, scripts, and feature contracts must remain aligned.

## Options Considered

### Option 1: Versioned canonical command contract with explicit compatibility rules

Treat the setup, validate, and run commands as a versioned contract and require updates to documentation and implementation artifacts together.

**Evaluation against priorities**:
- **Stable contributor experience**: Meets. One contract remains authoritative and changes are deliberate.
- **Safe evolution**: Meets. Versioning creates a clear change boundary and review point.
- **Cross artifact consistency**: Meets. The contract becomes a shared source of truth for docs and tooling.

### Option 2: Unversioned command surface with ad hoc updates

Allow command behavior to change without explicit contract versioning.

**Evaluation against priorities**:
- **Stable contributor experience**: Fails. Contributors cannot distinguish intended changes from accidental drift.
- **Safe evolution**: Fails. Breaking changes can be introduced silently.
- **Cross artifact consistency**: Fails. Docs and tool behavior diverge more easily.

## Decision

Choose Option 1. The project will maintain a versioned canonical command contract for setup, validation, and run entrypoints. Contract changes require documentation and implementation updates together so contributors always receive one authoritative path.

## Implementation Notes (optional)

- The contract version should be reflected in the feature documentation and any related command metadata.
- Breaking changes should be treated as a contract update and require review before the new behavior becomes canonical.

## References

* [Feature Spec: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/spec.md)
* [Feature Plan: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/plan.md)
