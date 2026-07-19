# Lock Governance

## Review gate

1. Review the declared dependency policy and the current lock manifest before approving an environment update.
2. Ensure every dependency group covered by the policy either remains pinned or satisfies an explicit constraint.
3. Confirm the manifest digest and the source context reflect the same declared inputs.

## Rollback steps

1. Revert the dependency declaration change that introduced the drift.
2. Re-run the canonical validation flow to confirm the prior dependency identity is restored.
3. Rebuild the lock manifest from the restored policy inputs before continuing.
