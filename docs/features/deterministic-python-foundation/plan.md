# Plan: Deterministic Python and Environment Foundation

- **Created on**: 2026-07-18
- **Status**: Draft
- **Feature spec**: [Deterministic Python and Environment Foundation](./spec.md)

## Plan Objective

Deliver one canonical, deterministic setup and execution foundation for contributors using a PyTorch centered stack with Axolotl, Unsloth, and Hugging Face TRL `SFTTrainer`, starting with local CPU execution and defined progression to free hosted alternatives and RunPod when needed.

## Confirmed Inputs

- Current dependency declarations exist in [pyproject.toml](../../../pyproject.toml) with Python `>=3.11` and core libraries (`torch`, `transformers`, `trl`, `datasets`, `peft`, `pyyaml`, `sentencepiece`, `evaluate`, `accelerate`).
- Current runnable training script is [scripts/train_first_sft.py](../../../scripts/train_first_sft.py) and current sample config is [training/configs/first-run-cpu.yaml](../../../training/configs/first-run-cpu.yaml).
- Repository strategy requires reproducibility from setup through execution.

## Planning Artifacts

- Research: [research.md](./research.md)
- Data model: [data-model.md](./data-model.md)
- Contracts: [contracts/environment-foundation-contract.md](./contracts/environment-foundation-contract.md)
- Handoff envelope: [handoff-envelope.md](./handoff-envelope.md)

## Architecture Decisions for This Plan

| Decision | Type | Current status | Action in this plan |
|----------|------|----------------|---------------------|
| Python baseline and supported OS matrix | Architecture significant | Proposed in [0001-python-runtime-and-platform-support](../../architecture/decisions/0001-python-runtime-and-platform-support.md) | Implement and validate against ADR priorities |
| Dependency lock and resolution strategy | Architecture significant | Proposed in [0002-dependency-lock-and-resolution-strategy](../../architecture/decisions/0002-dependency-lock-and-resolution-strategy.md) | Implement canonical resolver, lock artifacts, and policy checks |
| Framework ownership contract across Axolotl, Unsloth, TRL `SFTTrainer` | Architecture significant | Proposed in [0003-training-stack-orchestration-contract](../../architecture/decisions/0003-training-stack-orchestration-contract.md) | Implement profile based usage contract |
| Environment progression model (local, free hosted, RunPod) | Architecture significant | Proposed in [0004-environment-profiles-and-progression](../../architecture/decisions/0004-environment-profiles-and-progression.md) | Implement profile tiers and progression criteria |
| Canonical command surface for setup and execution | Convention | Not decided | Implement as stable command contract |
| Reproducibility evidence artifacts | Architecture significant | Not decided | Define deterministic identity and validation checks |

## Engineering Practices

| Practice | Decision | Reference |
|----------|----------|-----------|
| Branch Strategy | Trunk based with short lived feature branches and pull request review | Defined by the team |
| CI/CD | Lightweight CI focused on environment validation, lock integrity checks, and smoke run | Defined by the team |
| Code Review | Minimum one reviewer for docs and policy updates; two reviewers for lock policy changes | Defined by the team |
| Observability | Per run reproducibility manifest and setup outcome record stored as build artifacts | [0003-training-stack-orchestration-contract](../../architecture/decisions/0003-training-stack-orchestration-contract.md) |
| IaC | Deferred for this feature; environment profiles are documented and versioned first | Defined by the team |

## Implementation Workstreams

### Workstream 1: Policy and Support Matrix Foundation

**Goal**: Define explicit environment policy boundaries that remove ambiguity for contributors.

**Deliverables**:
- Python baseline policy (minor version target and upgrade rule)
- Supported OS matrix for deterministic guarantee
- Virtual environment standard policy
- Dependency source policy

**Definition of done**:
- Policy is documented in one canonical location.
- All setup instructions reference this policy directly.
- Spec requirements `FR-001`, `FR-002`, and `FR-003` are mapped to policy sections.

### Workstream 2: Dependency Identity and Lock Governance

**Goal**: Make dependency identity deterministic and auditable.

**Deliverables**:
- Canonical lock strategy and lock artifact format
- Pin versus constraint classification policy for all core dependency groups
- Lock update workflow with review gate and rollback rule
- Validation rule set that blocks setup success on policy mismatch

**Definition of done**:
- Dependency identity can be reproduced from declared inputs.
- Setup fails safely on lock drift or policy violation.
- Spec requirements `FR-004`, `FR-005`, and `FR-008` are satisfied.

### Workstream 3: Canonical Command Contract

**Goal**: Provide one stable contributor command surface for setup, validation, and execution.

**Deliverables**:
- Canonical setup command contract
- Canonical validation command contract
- Canonical execution command contract
- Error outcome taxonomy for actionable failure messages

**Definition of done**:
- Contributors can complete setup and first execution without undocumented commands.
- Command contract covers local CPU first workflow.
- Spec requirements `FR-006` and `FR-007` are satisfied.

### Workstream 4: Runtime Progression Profiles

**Goal**: Keep one canonical flow while supporting progression across compute environments.

**Profiles in scope**:
- `local-cpu` (baseline, required)
- `colab-free` (optional, best effort)
- `kaggle-free` (optional, best effort)
- `hf-space-notebook` or equivalent Hugging Face free path (optional, best effort)
- `runpod` (upgrade tier, optional)

**Deliverables**:
- Profile definitions with required invariants and known limitations
- Compatibility matrix for policy and lock behavior by profile
- Migration triggers from optional free tier to RunPod tier

**Definition of done**:
- Local CPU profile is fully compliant with deterministic guarantees.
- Optional profiles declare parity expectations and known deviations.
- Upgrade path to RunPod is documented with no change to canonical governance rules.

### Workstream 5: Conformance and Onboarding Validation

**Goal**: Validate the feature against the conformance and success criteria in the spec.

**Deliverables**:
- End to end setup conformance checks for `CC-001` through `CC-004`
- Onboarding dry run script or checklist for first time contributors
- Reproducibility evidence collection template
- Measurement protocol for `SC-001` through `SC-004`

**Definition of done**:
- Conformance cases pass in defined baseline conditions.
- First time setup flow can be validated by a non-author contributor.
- Deterministic identity checks are repeatable across validation runs.

## Stack Usage Contract

| Component | Planned role | Boundary in this phase |
|----------|--------------|------------------------|
| PyTorch | Core runtime and tensor backend | Required in all profiles |
| TRL `SFTTrainer` | Baseline supervised fine tuning path | Required for baseline training path |
| Axolotl | Optional orchestration profile for advanced training workflows | Optional, policy gated |
| Unsloth | Optional optimization profile where platform support exists | Optional, policy gated |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Dependency drift between local and hosted profiles | Breaks reproducibility claims | Lock governance plus profile compatibility checks |
| Toolchain incompatibility between Axolotl, Unsloth, and TRL releases | Setup failures and hidden behavior changes | Explicit compatibility matrix and controlled upgrade workflow |
| Undocumented command variation by contributors | Onboarding inconsistency | One canonical command contract and docs validation |
| Hosted free environment limitations | Unstable parity expectations | Mark optional profiles as best effort with explicit constraints |

## Milestones

1. Finalize policy and support matrix decisions.
2. Implement dependency lock governance and validation.
3. Publish canonical setup, validate, and run command contract.
4. Add profile progression documentation for free alternatives and RunPod.
5. Execute conformance validation and publish readiness report.

## Commands

Executable commands for this project (copy and run directly):

### Build
```powershell
[TBD]
```

### Tests
```powershell
[TBD]
```

### Lint/Formatting
```powershell
[TBD]
```

### Local Execution
```powershell
python scripts/train_first_sft.py --config training/configs/first-run-cpu.yaml
```

### Environment Setup Baseline (current repository state)
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install "torch>=2.4.0" "transformers>=4.44.0" "trl>=0.10.1" "datasets>=2.20.0" "peft>=0.12.0" "pyyaml>=6.0.2" "sentencepiece>=0.2.0" "evaluate>=0.4.2" "accelerate>=0.33.0"
```

## ADR Follow Up

Proposed ADRs have been created for this feature and must be reviewed by at least one additional team member before moving to Accepted status:

1. [0001-python-runtime-and-platform-support](../../architecture/decisions/0001-python-runtime-and-platform-support.md)
2. [0002-dependency-lock-and-resolution-strategy](../../architecture/decisions/0002-dependency-lock-and-resolution-strategy.md)
3. [0003-training-stack-orchestration-contract](../../architecture/decisions/0003-training-stack-orchestration-contract.md)
4. [0004-environment-profiles-and-progression](../../architecture/decisions/0004-environment-profiles-and-progression.md)
