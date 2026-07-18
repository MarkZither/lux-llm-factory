from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

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
        lines = handle.readlines()

    payload: dict[str, Any] = {}
    current_section: str | None = None
    for raw_line in lines:
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("\t"):
            if current_section is None:
                continue
            if ":" in line:
                key, value = line.strip().split(":", 1)
                payload.setdefault(current_section, {})[key.strip()] = value.strip().strip('"\'')
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            current_section = key
            payload[key] = {}
            continue
        payload[key] = value.strip('"\'')
        current_section = None

    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping content in {resolved_path}")
    return payload


def load_environment_policy(path: Path | str | None = None) -> dict[str, Any]:
    return _load_yaml(path, DEFAULT_POLICY_PATH)


def load_profiles(path: Path | str | None = None) -> dict[str, Any]:
    return _load_yaml(path, DEFAULT_PROFILES_PATH)


def run_setup(profile_id: str = "local-cpu", policy_path: Path | str | None = None, profiles_path: Path | str | None = None) -> dict[str, Any]:
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

    virtual_env = policy.get("virtual_environment", {}).get("expectation", ".venv")
    return {
        "ok": True,
        "status": "ready",
        "profile_id": profile_id,
        "policy_version": expected_policy_version,
        "venv": virtual_env,
        "setup_command": "uv venv --python 3.14 && uv sync",
        "message": "Environment policy matched the local-cpu profile and setup is ready.",
    }


def validate_environment(profile_id: str = "local-cpu", policy_path: Path | str | None = None, profiles_path: Path | str | None = None) -> dict[str, Any]:
    outcome = run_setup(profile_id=profile_id, policy_path=policy_path, profiles_path=profiles_path)
    if outcome["ok"]:
        return {
            **outcome,
            "status": "validated",
            "message": "Policy and profile checks passed without mutation.",
        }
    return outcome


def run_entrypoint(profile_id: str = "local-cpu", policy_path: Path | str | None = None, profiles_path: Path | str | None = None) -> dict[str, Any]:
    validation = validate_environment(profile_id=profile_id, policy_path=policy_path, profiles_path=profiles_path)
    if not validation["ok"]:
        return {
            **validation,
            "status": "preflight-failed",
            "command": "python scripts/train_first_sft.py --config training/configs/first-run-cpu.yaml",
        }
    return {
        **validation,
        "status": "ready",
        "command": "python scripts/train_first_sft.py --config training/configs/first-run-cpu.yaml",
        "message": "Preflight checks passed and the canonical training entrypoint can be invoked.",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Canonical environment setup and execution contract")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", help="Initialize the environment under the canonical policy")
    setup_parser.add_argument("--profile", default="local-cpu")

    validate_parser = subparsers.add_parser("validate", help="Validate policy and profile expectations")
    validate_parser.add_argument("--profile", default="local-cpu")

    run_parser = subparsers.add_parser("run", help="Run the canonical training entrypoint after preflight validation")
    run_parser.add_argument("--profile", default="local-cpu")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "setup":
        result = run_setup(profile_id=args.profile)
    elif args.command == "validate":
        result = validate_environment(profile_id=args.profile)
    elif args.command == "run":
        result = run_entrypoint(profile_id=args.profile)
    else:
        parser.error("Unsupported command")
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
