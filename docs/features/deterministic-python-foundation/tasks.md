# Tasks: Deterministic Python and Environment Foundation

## Phase 1: Setup

- [x] Define deterministic environment policy skeleton in docs/features/deterministic-python-foundation/policy/environment-policy.yaml for FR-001, FR-002, and FR-003.
- [x] [P] Create profile definition stubs for local-cpu, colab-free, kaggle-free, hf-free, and runpod in docs/features/deterministic-python-foundation/policy/profiles.yaml for FR-001 and FR-003.
- [x] [P] Add canonical command surface scaffold in scripts/envctl.py with setup, validate, and run command groups mapped to CLI-SETUP-001, CLI-VALIDATE-001, and CLI-RUN-001.
- [x] Add contributor-facing setup entry section in README.md pointing to one canonical flow for FR-006 and FR-007.

## Phase 2: Foundational

- [x] Complete ADR review and status update for docs/architecture/decisions/0001-python-runtime-and-platform-support.md before implementation tasks that depend on baseline support tiers.
- [x] Complete ADR review and status update for docs/architecture/decisions/0002-dependency-lock-and-resolution-strategy.md before implementation tasks that depend on lock governance.
- [x] Complete ADR review and status update for docs/architecture/decisions/0003-training-stack-orchestration-contract.md before implementation tasks that depend on profile-gated stack behavior.
- [x] Complete ADR review and status update for docs/architecture/decisions/0004-environment-profiles-and-progression.md before implementation tasks that depend on profile progression.
- [x] Create missing cross-cutting ADR for canonical command contract versioning in docs/architecture/decisions/0005-canonical-command-contract-versioning.md.
- [x] Create missing cross-cutting ADR for reproducibility evidence schema and digest policy in docs/architecture/decisions/0006-reproducibility-evidence-schema-and-digests.md.
- [x] Define lock manifest schema and digest generation contract in docs/features/deterministic-python-foundation/contracts/lock-manifest-schema.md for FR-004 and FR-008.

## Phase 3: User Story 1 - Deterministic First Time Setup (P1)

- [x] Implement tracer bullet vertical slice for deterministic setup in scripts/envctl.py that executes setup, validates policy plus lock identity, and reports SetupOutcome for CC-001.
- [x] Implement local-cpu baseline policy enforcement in scripts/env_policy.py using docs/features/deterministic-python-foundation/policy/environment-policy.yaml for FR-001, FR-002, and FR-003.
- [x] [P] Implement lock identity generation and verification in scripts/lock_identity.py using docs/features/deterministic-python-foundation/contracts/lock-manifest-schema.md for FR-004 and FR-008.
- [x] [P] Implement safe failure taxonomy mapping in scripts/env_errors.py for PolicyViolation, LockMismatch, ProfileUnsupported, and PreflightFailure to satisfy FR-008 and CC-002.
- [x] Implement interrupted setup convergence behavior in scripts/envctl.py to satisfy CC-003 and deterministic rerun requirements.
- [x] Update canonical setup documentation in docs/features/deterministic-python-foundation/setup.md with one official setup sequence and no alternate hidden path for FR-007 and CC-004.

## Phase 4: User Story 2 - Intentional Version Boundaries (P2)

- [x] Implement tracer bullet for version-boundary governance in scripts/envctl.py validate command to prove pin-versus-constraint checks against one dependency group for FR-005.
- [x] Implement dependency rule catalog in docs/features/deterministic-python-foundation/policy/dependency-rules.yaml covering all core dependency groups for FR-005.
- [x] [P] Implement policy rule evaluator in scripts/dependency_policy.py to enforce pinned or constrained declarations against resolved artifacts for FR-004 and FR-005.
- [x] [P] Implement lock update workflow documentation in docs/features/deterministic-python-foundation/lock-governance.md including review gate and rollback steps for FR-004.
- [x] Implement policy violation reporting with explicit rule identifiers in scripts/envctl.py and docs/features/deterministic-python-foundation/contracts/error-codes.md for CC-002.

## Phase 5: User Story 3 - Canonical Execution Entry (P3)

- [x] Implement tracer bullet for canonical execution entry in scripts/envctl.py run command that enforces preflight validation before invoking scripts/train_first_sft.py for FR-006.
- [x] [P] Implement canonical command documentation source in docs/features/deterministic-python-foundation/commands.md for setup, validate, and run entrypoints mapped to DOC-CMD-001.
- [x] [P] Add profile-aware runtime invocation adapter in scripts/runtime_profiles.py for local-cpu baseline and deferred future-work handling for hosted or runpod profiles under one command contract.
- [x] Implement command discoverability links in README.md and docs/features/deterministic-python-foundation/setup.md so contributors find one authoritative command path for FR-007 and CC-004.

## Phase 6: Polish and Cross-Cutting

- [x] [P] Add conformance validation playbook for CC-001 through CC-004 in docs/features/deterministic-python-foundation/conformance.md with expected evidence artifacts.
- [x] [P] Add measurement protocol for SC-001 through SC-004 in docs/features/deterministic-python-foundation/measurement-protocol.md including onboarding timing and identity match checks.
- [x] Define profile promotion criteria from optional to baseline in docs/features/deterministic-python-foundation/profile-progression.md to close handoff pending decision.
- [x] Add implementation handoff summary and traceability matrix update in docs/features/deterministic-python-foundation/handoff-envelope.md linking completed tasks to FR, CC, and SC coverage.