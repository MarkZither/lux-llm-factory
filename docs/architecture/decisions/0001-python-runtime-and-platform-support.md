# Python Runtime and Platform Support

**Status**: Proposed
**Date**: 2026-07-18

## Context

The project needs deterministic contributor setup before training work can proceed. The specification requires one canonical setup flow and deterministic environment identity. Without a fixed runtime baseline and explicit platform support policy, lock behavior and reproducibility checks can diverge between contributors and hosting environments.

## Priorities and Requirements (ordered)

1. **Deterministic contributor setup** — Contributors must reach the same runtime baseline from the same documented inputs.
2. **Cross environment continuity** — The same project policy must remain valid for local CPU and optional hosted profiles.
3. **Operational simplicity for a small team** — The support burden must stay low during the first project phase.

## Options Considered

### Option 1: Single Python minor baseline with explicit support tiers

Define one required Python minor baseline for canonical support and classify environments by support tier.

**Evaluation against priorities**:
- **Deterministic contributor setup**: Meets. One required minor baseline removes interpreter ambiguity and improves lock reproducibility.
- **Cross environment continuity**: Meets. Tiered support allows the same policy to apply across local and hosted profiles while documenting known differences.
- **Operational simplicity for a small team**: Meets. One canonical baseline reduces troubleshooting permutations.

### Option 2: Python version range policy across all environments

Allow a bounded version range for the baseline and rely on compatibility rules.

**Evaluation against priorities**:
- **Deterministic contributor setup**: Partially meets. A range increases interpreter variability and can change resolution outcomes.
- **Cross environment continuity**: Partially meets. It increases the chance that local and hosted runtimes choose different minor versions.
- **Operational simplicity for a small team**: Fails. Broader version support increases test and support overhead.

## Decision

Choose Option 1. The project will use a single Python minor baseline for canonical deterministic support and define explicit support tiers for local CPU, free hosted alternatives, and RunPod. This best satisfies deterministic setup first, keeps continuity across environments, and minimizes support burden for the current team size.

## Implementation Notes (optional)

- Baseline runtime policy is recorded in the feature implementation artifacts and contributor setup documentation.
- Tier labels are required in environment profile definitions.

## References

* [Feature Spec: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/spec.md)
* [Feature Plan: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/plan.md)
