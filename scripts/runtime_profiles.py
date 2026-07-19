from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRAINING_SCRIPT = REPO_ROOT / "scripts" / "train_first_sft.py"
DEFAULT_TRAINING_CONFIG = REPO_ROOT / "training" / "configs" / "first-run-cpu.yaml"


def build_runtime_command(
    profile_id: str = "local-cpu",
    *,
    repo_root: Path | str | None = None,
    python_executable: str | None = None,
) -> dict[str, Any]:
    resolved_root = Path(repo_root or REPO_ROOT)
    if not resolved_root.is_absolute():
        resolved_root = REPO_ROOT / resolved_root

    if profile_id == "local-cpu":
        mode = "local"
    elif profile_id in {"colab-free", "kaggle-free", "hf-free", "runpod"}:
        mode = "hosted"
    else:
        raise ValueError(f"Unsupported runtime profile: {profile_id}")

    command = [
        python_executable or sys.executable,
        "scripts/train_first_sft.py",
        "--config",
        "training/configs/first-run-cpu.yaml",
    ]
    return {
        "profile_id": profile_id,
        "mode": mode,
        "script": "scripts/train_first_sft.py",
        "config": "training/configs/first-run-cpu.yaml",
        "command": command,
    }
