# Error Codes

## Policy and dependency validation

- `PolicyViolation`: The resolved environment or dependency state does not match the declared policy.
- `LockMismatch`: The generated lock identity does not match the expected manifest digest.
- `ProfileUnsupported`: The requested profile is not defined in the canonical profile catalog.
- `PreflightFailure`: The canonical entrypoint could not be executed because preflight validation failed.

## Version-boundary rule identifiers

- `DPR-001`: Torch must remain pinned to the baseline-tested version.
- `DPR-002`: Transformers must satisfy the minimum supported version constraint.
- `DPR-003`: Accelerate must satisfy the minimum supported version constraint.
