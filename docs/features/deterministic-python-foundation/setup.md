# Canonical setup flow

Use this sequence as the one supported setup path for contributors.

1. Create a Python 3.14 virtual environment in the repository root.
2. Activate the environment and install the pinned project dependencies.
3. Run the canonical validation command to confirm policy and profile expectations.
4. Use the canonical run command when you are ready to start training.

## Supported commands

```powershell
uv python install 3.14
uv venv --python 3.14
uv sync
uv run python scripts/envctl.py setup --profile local-cpu
uv run python scripts/envctl.py validate --profile local-cpu
uv run python scripts/envctl.py run --profile local-cpu
```

This document is the authoritative setup path. Do not rely on alternate hidden workflows.
