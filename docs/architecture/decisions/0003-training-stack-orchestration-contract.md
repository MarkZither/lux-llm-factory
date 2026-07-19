# Training Stack Orchestration Contract

**Status**: Accepted
**Date**: 2026-07-18

## Context

The project intends to build with PyTorch, Axolotl, Unsloth, and Hugging Face TRL `SFTTrainer`. Without a clear orchestration contract, contributors can select incompatible paths or duplicate configuration logic, which undermines deterministic execution and maintainability.

## Priorities and Requirements (ordered)

1. **Deterministic training behavior by profile** — Each supported profile must map to one clear orchestration contract.
2. **Compatibility and upgrade safety** — Framework interactions must be explicit to reduce breakage from upstream changes.
3. **Practical maintainability** — The stack contract must be manageable for a small team.

## Options Considered

### Option 1: Profile based contract with TRL `SFTTrainer` baseline and Axolotl or Unsloth as optional policy gated profiles

Define TRL `SFTTrainer` as baseline training contract and allow Axolotl or Unsloth under explicit profile rules.

**Evaluation against priorities**:
- **Deterministic training behavior by profile**: Meets. Each profile has one declared orchestration path.
- **Compatibility and upgrade safety**: Meets. Optional profiles are gated and versioned, reducing accidental stack mixing.
- **Practical maintainability**: Meets. One baseline path limits complexity while preserving expansion paths.

### Option 2: Fully interchangeable framework choice per run

Allow contributors to choose Axolotl, Unsloth, or TRL workflow at run time without profile governance.

**Evaluation against priorities**:
- **Deterministic training behavior by profile**: Fails. Run level framework switching introduces inconsistent behavior.
- **Compatibility and upgrade safety**: Fails. Implicit combinations increase risk of version conflicts and nondeterministic failures.
- **Practical maintainability**: Fails. Support and debugging cost grows quickly.

## Decision

Choose Option 1. The project will treat TRL `SFTTrainer` as the baseline orchestration contract and allow Axolotl and Unsloth through explicit, policy gated profiles. This preserves deterministic profile behavior, improves upgrade safety, and keeps maintenance realistic.

## Implementation Notes (optional)

- Profile documentation must state required dependencies and unsupported combinations.
- Changes to baseline orchestration contract require ADR update or supersession.

## References

* [Feature Spec: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/spec.md)
* [Feature Plan: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/plan.md)
