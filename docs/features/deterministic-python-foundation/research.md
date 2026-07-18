# Research: Deterministic Python and Environment Foundation

- **Created on**: 2026-07-18
- **Status**: Draft
- **Related spec**: [spec.md](./spec.md)
- **Related plan**: [plan.md](./plan.md)

## Objective

Capture the decision context that supports deterministic contributor setup and controlled progression from local CPU to optional free hosted alternatives and optional RunPod upgrade.

## Inputs Considered

- [spec.md](./spec.md)
- [plan.md](./plan.md)
- [0001-python-runtime-and-platform-support](../../architecture/decisions/0001-python-runtime-and-platform-support.md)
- [0002-dependency-lock-and-resolution-strategy](../../architecture/decisions/0002-dependency-lock-and-resolution-strategy.md)
- [0003-training-stack-orchestration-contract](../../architecture/decisions/0003-training-stack-orchestration-contract.md)
- [0004-environment-profiles-and-progression](../../architecture/decisions/0004-environment-profiles-and-progression.md)

## Decision Synthesis

| Topic | Chosen direction | Why it was selected | Spec mapping |
|------|------------------|---------------------|--------------|
| Runtime baseline | Single Python minor baseline with explicit support tiers | Reduces interpreter drift and contributor ambiguity | FR-001, FR-002, CC-001 |
| Dependency identity | One canonical resolver and committed lock artifacts | Enables repeatable dependency identity and auditable changes | FR-004, FR-005, CC-001, CC-002 |
| Training orchestration | TRL `SFTTrainer` baseline with Axolotl and Unsloth as profile gated options | Prevents stack mixing while preserving advanced paths | FR-006, CC-004 |
| Environment progression | Tiered profiles under one command and policy contract | Keeps one canonical flow while enabling staged scale | FR-001, FR-007, CC-001 |

## Alternatives Reviewed

| Alternative | Reason not selected |
|-------------|---------------------|
| Python version range as baseline | Increases setup variability and support burden |
| Constraint only dependency model with no lock files | Cannot guarantee deterministic dependency identity |
| Fully interchangeable run-time framework selection | Causes orchestration ambiguity and upgrade risk |
| Separate setup flows for each environment | Breaks canonical contributor path requirement |

## Profile Progression Model

| Profile | Support level | Purpose | Determinism expectation |
|---------|---------------|---------|-------------------------|
| local-cpu | Baseline required | Canonical onboarding and first deterministic run | Strict conformance required |
| colab-free | Optional best effort | Free hosted experimentation | Policy and lock checks required, environment limits documented |
| kaggle-free | Optional best effort | Free hosted experimentation | Policy and lock checks required, environment limits documented |
| hf-free | Optional best effort | Free Hugging Face hosted experimentation | Policy and lock checks required, environment limits documented |
| runpod | Optional upgrade | Scaled execution when required | Same policy and lock governance as baseline |

## Controlled Unknowns

| Unknown | Current handling | Closure owner |
|---------|------------------|---------------|
| Exact supported OS matrix | Track as policy decision in implementation workstream | Feature implementer and reviewer |
| Exact lock artifact format | Track as contract detail in dependency workstream | Feature implementer and reviewer |
| Baseline command tool selection for build and lint | Keep as explicit TBD in plan commands | Feature implementer and reviewer |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hosted platform package variance | Setup and run drift | Enforce policy checks before declaring readiness |
| Upstream dependency churn | Breaks setup reproducibility | Use lock governance and controlled update workflow |
| Documentation drift from command surface | Contributor confusion | Keep one canonical command contract and validation step |

## Conformance Traceability

| Conformance case | Supporting decision or artifact |
|------------------|-------------------------------|
| CC-001 | Runtime baseline, lock strategy, profile model |
| CC-002 | Lock policy validation gate |
| CC-003 | Canonical rerun behavior and safe convergence expectation |
| CC-004 | Single command and documentation contract |

## Implementation Readiness Summary

This research confirms that deterministic setup is feasible under one governance model if the team keeps a strict baseline profile, committed lock strategy, and profile based orchestration boundaries.
