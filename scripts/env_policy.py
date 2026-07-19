from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY_PATH = REPO_ROOT / "docs/features/deterministic-python-foundation/policy/environment-policy.yaml"
DEFAULT_PROFILES_PATH = REPO_ROOT / "docs/features/deterministic-python-foundation/policy/profiles.yaml"


def _resolve_path(path: Path | str | None, default: Path) -> Path:
    if path is None:
        return default
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    return candidate


def _load_yaml(path: Path | str | None, default: Path) -> dict[str, Any]:
    resolved_path = _resolve_path(path, default)
    with resolved_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}

    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping content in {resolved_path}")
    return payload


def load_environment_policy(path: Path | str | None = None) -> dict[str, Any]:
    return _load_yaml(path, DEFAULT_POLICY_PATH)


def load_profiles(path: Path | str | None = None) -> dict[str, Any]:
    return _load_yaml(path, DEFAULT_PROFILES_PATH)


def evaluate_policy(profile_id: str = "local-cpu", policy_path: Path | str | None = None, profiles_path: Path | str | None = None) -> dict[str, Any]:
    policy = load_environment_policy(policy_path)
    profiles = load_profiles(profiles_path)
    profile = profiles.get(profile_id)
    if profile is None:
        return {
            "ok": False,
            "status": "failed",
            "profile_id": profile_id,
            "error": "ProfileUnsupported",
            "message": f"Profile '{profile_id}' is not defined in the canonical policy file.",
        }

    expected_policy_version = policy.get("policy_version")
    actual_profile_policy_version = profile.get("policy_version")
    if expected_policy_version != actual_profile_policy_version:
        return {
            "ok": False,
            "status": "failed",
            "profile_id": profile_id,
            "error": "PolicyViolation",
            "message": "Profile policy version does not match the current environment policy.",
        }

    python_baseline = policy.get("python_baseline", {}).get("version")
    profile_python = profile.get("constraints", {}).get("python")
    if python_baseline and profile_python and python_baseline != profile_python:
        return {
            "ok": False,
            "status": "failed",
            "profile_id": profile_id,
            "error": "PolicyViolation",
            "message": "Profile python constraint does not match the declared baseline policy.",
        }

    expected_virtual_env = policy.get("virtual_environment", {}).get("expectation", ".venv")
    profile_virtual_env = profile.get("constraints", {}).get("virtual_environment")
    if profile_virtual_env and expected_virtual_env and profile_virtual_env != expected_virtual_env:
        return {
            "ok": False,
            "status": "failed",
            "profile_id": profile_id,
            "error": "PolicyViolation",
            "message": "Profile virtual environment expectation does not match the declared policy.",
        }

    return {
        "ok": True,
        "status": "passed",
        "profile_id": profile_id,
        "policy_version": expected_policy_version,
        "python_version": python_baseline,
        "virtual_environment": expected_virtual_env,
        "message": "Environment policy matched the requested profile.",
    }
