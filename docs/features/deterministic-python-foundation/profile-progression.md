# Profile Progression Criteria

- **Created on**: 2026-07-19
- **Status**: Draft
- **Related spec**: [spec.md](./spec.md)

## Purpose

Define when an optional environment profile can move from best effort support to a baseline support tier without weakening the one canonical contributor workflow.

## Current Profile Model

| Profile | Support level | Status |
|---------|---------------|--------|
| local-cpu | Baseline required | The canonical onboarding path and the reference deterministic guarantee. |
| colab-free | Optional best effort | Supported for experimentation when the platform can honor policy and lock checks. |
| kaggle-free | Optional best effort | Supported for experimentation when the platform can honor policy and lock checks. |
| hf-free | Optional best effort | Supported for experimentation when the platform can honor policy and lock checks. |
| runpod | Optional upgrade | Supported for scaled execution when the same governance contract applies. |

## Promotion Criteria

A profile may move from optional to baseline only when all of the following conditions are met:

1. The profile can run the canonical setup, validate, and run commands from the repository root without undocumented workarounds.
2. The profile honors the same policy and lock governance rules as the baseline profile.
3. The profile produces reproducible evidence artifacts that can be compared with the local-cpu baseline.
4. Known limitations, support boundaries, and fallback behavior are documented for contributors.
5. A maintainer review confirms that the profile is stable enough to be treated as a first class support path.

## Decision Rule

Promotion should be a deliberate decision, not an automatic outcome of initial availability. If any criterion is not met, the profile stays optional and should remain labeled as best effort or upgrade tier.

## Evidence Required for Review

Before a promotion decision, collect:

- the validation transcript for setup and run commands
- the generated identity or lock evidence artifact
- the contributor-facing documentation for the profile
- a short note describing the profile-specific limitations and support boundary
