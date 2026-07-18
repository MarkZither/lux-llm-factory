# Environment Profiles and Progression

**Status**: Accepted
**Date**: 2026-07-18

## Context

The feature requires local CPU as the initial training baseline, optional free alternatives, and a possible upgrade path to RunPod. A decision is needed on how environments are modeled so the project keeps one canonical flow while accommodating different compute contexts.

## Priorities and Requirements (ordered)

1. **Canonical flow consistency** — Contributors must use one documented setup and execution pattern.
2. **Deterministic policy continuity across environments** — Environment changes must not bypass policy and lock governance.
3. **Incremental scalability** — The project must support progression from local CPU to stronger compute when needed.

## Options Considered

### Option 1: Tiered environment profiles under one canonical command contract

Define required baseline profile for local CPU, optional best effort free profiles, and optional RunPod upgrade profile, all under one policy and command contract.

**Evaluation against priorities**:
- **Canonical flow consistency**: Meets. One command contract remains authoritative across profiles.
- **Deterministic policy continuity across environments**: Meets. Policy and lock checks remain mandatory for each profile.
- **Incremental scalability**: Meets. The model supports staged progression without redesigning the workflow.

### Option 2: Separate setup and execution flows per environment

Allow each environment to define its own commands and policy interpretation.

**Evaluation against priorities**:
- **Canonical flow consistency**: Fails. Multiple official flows increase onboarding ambiguity.
- **Deterministic policy continuity across environments**: Partially meets. Independent flows can diverge in policy enforcement.
- **Incremental scalability**: Partially meets. It can scale technically but increases governance fragmentation.

## Decision

Choose Option 1. The project will use tiered environment profiles under one canonical command and policy contract, with local CPU as required baseline, free alternatives as optional best effort profiles, and RunPod as optional upgrade profile. Every profile remains reachable through the same uv-based setup and validation workflow, which preserves canonical setup consistency, deterministic governance continuity, and staged scalability.

## Implementation Notes (optional)

- Profiles must declare compliance level and known limitations.
- Promotion from optional profile to baseline support requires explicit review and plan update.
- uv remains the canonical command entry for setup, validation, and execution across profiles.

## References

* [Feature Spec: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/spec.md)
* [Feature Plan: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/plan.md)
