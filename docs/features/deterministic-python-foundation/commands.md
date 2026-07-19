# Canonical commands

This document is the authoritative command reference for the deterministic Python foundation feature.

## Setup

```powershell
uv run python scripts/envctl.py setup --profile local-cpu
```

## Validate

```powershell
uv run python scripts/envctl.py validate --profile local-cpu
```

## Run

```powershell
uv run python scripts/envctl.py run --profile local-cpu
```

Use these commands from the repository root. They are the only supported entrypoints for setup, validation, and execution.
