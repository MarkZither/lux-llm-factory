# Handoff Envelope: Deterministic Python and Environment Foundation

- **Created on**: 2026-07-18
- **Status**: Ready for `devsquad.decompose`
- **Source feature**: [spec.md](./spec.md)

## Handoff Context

**Relevant artifacts**:
- [spec.md](./spec.md)
- [plan.md](./plan.md)
- [research.md](./research.md)
- [data-model.md](./data-model.md)
- [contracts/environment-foundation-contract.md](./contracts/environment-foundation-contract.md)
- [../../architecture/decisions/0001-python-runtime-and-platform-support.md](../../architecture/decisions/0001-python-runtime-and-platform-support.md)
- [../../architecture/decisions/0002-dependency-lock-and-resolution-strategy.md](../../architecture/decisions/0002-dependency-lock-and-resolution-strategy.md)
- [../../architecture/decisions/0003-training-stack-orchestration-contract.md](../../architecture/decisions/0003-training-stack-orchestration-contract.md)
- [../../architecture/decisions/0004-environment-profiles-and-progression.md](../../architecture/decisions/0004-environment-profiles-and-progression.md)

**Inherited assumptions**:
- Deterministic setup is defined by policy compliance plus lock identity validation.
- Local CPU is the baseline required profile for conformance.
- Free hosted profiles are optional and best effort but must still honor policy and lock governance.
- RunPod is an optional upgrade profile under the same governance contract.
- TRL `SFTTrainer` is the baseline orchestration path, while Axolotl and Unsloth are profile gated options.

**Pending decisions**:
- Exact supported OS matrix for baseline deterministic guarantee.
- Exact canonical lock artifact schema and digest rules.
- Exact toolchain choices for build, lint, and test commands currently marked as TBD in [plan.md](./plan.md).
- Criteria for promotion of optional profiles to baseline required support.
- Review and acceptance of Proposed ADRs by at least one additional team member.

**Discarded information**:
- Multi-flow setup approaches per environment were discarded because they violate one canonical setup requirement.
- Constraint-only dependency strategy without committed lock artifacts was discarded because it does not ensure deterministic identity.
- Unbounded framework interchangeability per run was discarded because it increases nondeterministic behavior and support complexity.

## Decompose Guidance

### Priority workstreams

1. Policy and support matrix foundation.
2. Dependency lock and resolution governance.
3. Canonical setup, validate, and run command contract.
4. Environment profile progression from local CPU to optional hosted and RunPod tiers.
5. Conformance validation for `CC-001` to `CC-004` and measurement protocol for `SC-001` to `SC-004`.

### Task decomposition rules

- Each task must trace to at least one requirement (`FR-*`) and one concrete artifact target.
- Task set must include ADR review tasks before implementation tasks depending on accepted decisions.
- Task set must include validation tasks for deterministic identity and safe failure behavior.
- Task set must keep one canonical contributor flow as a non-negotiable constraint.

## Ready Signal

This feature package is ready for decomposition into implementation tasks.
