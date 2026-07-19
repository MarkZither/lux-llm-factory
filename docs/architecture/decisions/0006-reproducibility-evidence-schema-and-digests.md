# Reproducibility Evidence Schema and Digest Policy

**Status**: Accepted
**Date**: 2026-07-19

## Context

The deterministic environment foundation needs an explicit evidence model so setup success can be verified and audited. Without a shared schema and digest policy, contributors and reviewers cannot tell whether a setup run produced the same identity or whether evidence is trustworthy.

## Priorities and Requirements (ordered)

1. **Deterministic evidence** — Reproducibility evidence must be stable for the same declared inputs.
2. **Actionable validation** — Setup and validation results must expose enough information to diagnose mismatches.
3. **Operational simplicity** — The evidence format must be lightweight and easy to generate.

## Options Considered

### Option 1: Standardized evidence payload with canonical digest fields

Define a lightweight schema containing policy version, lock digest, profile identifier, and a manifest digest so each run can be compared deterministically.

**Evaluation against priorities**:
- **Deterministic evidence**: Meets. The schema creates a stable identity model for each setup outcome.
- **Actionable validation**: Meets. The payload exposes the inputs necessary to explain that a run passed or failed.
- **Operational simplicity**: Meets. The format remains small and easy to emit from CLI tooling.

### Option 2: Ad hoc evidence notes without schema or digest policy

Record whatever text or logs are available without a shared structure.

**Evaluation against priorities**:
- **Deterministic evidence**: Fails. Evidence cannot be compared reliably across runs.
- **Actionable validation**: Partially meets. Logs may explain behavior but are not machine-checked.
- **Operational simplicity**: Partially meets. It is easy to start but poor for long term audits.

## Decision

Choose Option 1. The project will use a standardized reproducibility evidence payload with a stable manifest digest and explicit policy and lock identity fields. This creates a consistent audit trail for setup and validation outcomes.

## Implementation Notes (optional)

- Evidence payloads should include the policy version, resolved profile, and lock digest used during setup.
- Digest generation should be deterministic and derived from stable manifest content rather than timestamps or transient environment values.

## References

* [Feature Spec: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/spec.md)
* [Feature Plan: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/plan.md)
