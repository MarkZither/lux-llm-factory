# Conformance Validation Playbook

- **Created on**: 2026-07-19
- **Status**: Draft
- **Related spec**: [spec.md](./spec.md)

## Objective

Validate the canonical deterministic setup foundation against conformance cases CC-001 through CC-004 using the documented local-cpu baseline flow.

## Validation Scope

This playbook covers the contributor experience for:

- deterministic first setup
- safe policy violation handling
- interrupted setup recovery
- canonical onboarding without alternate hidden paths

The baseline validation path is the documented flow in [setup.md](./setup.md) and [commands.md](./commands.md).

## Required Evidence

Collect the following artifacts for each validation run:

| Artifact | Purpose |
|----------|---------|
| setup command output | Proves whether setup succeeded or failed in a deterministic way |
| validate command output | Confirms policy and lock checks passed or failed as expected |
| run command output | Confirms the canonical execution entrypoint works from the repository root |
| lock identity or manifest output | Provides dependency identity evidence for repeatability |
| notes from the contributor run | Captures onboarding friction and unexpected steps |

## Validation Procedure

1. Start from a clean supported machine or a disposable environment snapshot.
2. Follow the canonical setup sequence exactly as written in [setup.md](./setup.md).
3. Record the command output and any environment identity artifacts.
4. Repeat the validation for each conformance case below.

## Conformance Cases

| ID | Scenario | Validation steps | Expected result |
|----|----------|------------------|-----------------|
| CC-001 | Deterministic first setup happy path | Run the documented setup, validate, and run commands from the repository root using the local-cpu profile. | Setup completes, the environment is reported ready, and the dependency identity matches the declared policy and lock state. |
| CC-002 | Policy violation error path | Use a controlled policy or lock deviation in a disposable copy of the workspace or a temporary override to trigger a validation failure. | Setup fails safely, reports the policy violation clearly, and does not claim readiness. |
| CC-003 | Interrupted setup recovery edge case | Interrupt setup after partial progress, then rerun the canonical setup flow. | The rerun converges to the same deterministic ready state without requiring manual cleanup steps. |
| CC-004 | Must not require ambiguous onboarding paths | Follow only the official setup and command documentation and record whether any alternate path is needed. | The contributor reaches a ready state without hidden manual commands, alternate entrypoints, or undocumented workarounds. |

## Completion Criteria

A validation pass is complete when all required evidence is captured and each conformance case meets its expected result. If a case fails, the issue should be recorded with the implicated requirement, the observed output, and the corrective action before the feature is marked ready for broader rollout.
