# Lock Manifest Schema and Digest Contract

- **Created on**: 2026-07-19
- **Status**: Draft
- **Related spec**: [../spec.md](../spec.md)
- **Related plan**: [../plan.md](../plan.md)

## Purpose

Define the canonical lock manifest structure used to record deterministic dependency identity for setup and validation. The manifest is the authoritative artifact for comparing resolved dependency state across runs.

## Schema

The lock manifest MUST use the following top-level fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| lock_version | string | Yes | Schema version for the manifest format |
| resolver_identity | string | Yes | Canonical resolver identity, such as `uv-sync` |
| policy_version | string | Yes | Policy version used to produce the manifest |
| profile_id | string | Yes | Environment profile used to generate the manifest |
| package_entries | array | Yes | Resolved package entries for the environment |
| source_digest | string | Yes | Stable digest of the declared source context |
| manifest_digest | string | Yes | Stable digest of the manifest content |

## Package Entry Schema

Each entry in `package_entries` MUST contain:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Package name |
| version | string | Yes | Resolved version |
| source | string | Yes | Source identifier such as `pypi` |
| extra | string | No | Optional classifier for dependency group |

## Digest Rules

1. `source_digest` MUST be derived from the declared input context, including policy version, profile identifier, and dependency source declarations.
2. `manifest_digest` MUST be computed from the canonical manifest content after normalization so equivalent manifests yield the same digest.
3. Digest generation MUST be deterministic and MUST NOT include timestamps or local filesystem paths.
4. A manifest is invalid if `manifest_digest` does not match the digest of the normalized manifest content.

## Validation Contract

- Setup MUST fail if the computed manifest digest does not match the declared `manifest_digest`.
- Validation MUST report a lock mismatch when the current environment identity does not match the expected manifest digest.
- The canonical setup flow MUST use this schema for lock identity checks.

## Traceability

- FR-004: Canonical resolver and lock contract
- FR-008: Safe failure on lock mismatch
