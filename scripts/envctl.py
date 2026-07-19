from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import dependency_policy, env_policy, lock_identity
from scripts.env_errors import PolicyViolation, ProfileUnsupported, PreflightFailure, to_error_payload
from scripts.runtime_profiles import build_runtime_command
DEFAULT_POLICY_PATH = REPO_ROOT / "docs/features/deterministic-python-foundation/policy/environment-policy.yaml"
DEFAULT_PROFILES_PATH = REPO_ROOT / "docs/features/deterministic-python-foundation/policy/profiles.yaml"
DEFAULT_DEPENDENCY_RULES_PATH = REPO_ROOT / "docs/features/deterministic-python-foundation/policy/dependency-rules.yaml"
DEFAULT_STATE_DIR = REPO_ROOT / ".setup-state"


def load_environment_policy(path: Path | str | None = None) -> dict[str, Any]:
    return env_policy.load_environment_policy(path)


def load_profiles(path: Path | str | None = None) -> dict[str, Any]:
    return env_policy.load_profiles(path)


def _resolve_state_dir(state_dir: Path | str | None) -> Path:
    if state_dir is None:
        state_dir = DEFAULT_STATE_DIR
    resolved_path = Path(state_dir)
    if not resolved_path.is_absolute():
        resolved_path = REPO_ROOT / resolved_path
    resolved_path.mkdir(parents=True, exist_ok=True)
    return resolved_path


def _parse_dependency_artifacts(raw_value: str | None) -> list[dict[str, Any]] | None:
    if raw_value is None:
        return None
    parsed = json.loads(raw_value)
    if not isinstance(parsed, list):
        raise ValueError("--dependency-artifacts expects a JSON array")
    return [item for item in parsed if isinstance(item, dict)]


def _extract_dependency_version(requirement: str) -> str:
    requirement = requirement.strip()
    if not requirement:
        return ""
    version_match = re.search(r"(\d+(?:\.\d+)*)", requirement)
    return version_match.group(1) if version_match else ""


def _load_dependency_artifacts_from_pyproject(pyproject_path: Path | str | None = None) -> list[dict[str, Any]]:
    resolved_path = Path(pyproject_path or REPO_ROOT / "pyproject.toml")
    if not resolved_path.is_absolute():
        resolved_path = REPO_ROOT / resolved_path
    with resolved_path.open("rb") as handle:
        metadata = tomllib.load(handle)

    project_dependencies: list[str] = metadata.get("project", {}).get("dependencies", []) or []
    dependency_groups: dict[str, list[str]] = metadata.get("dependency-groups", {}) or {}

    artifacts: list[dict[str, Any]] = []
    for dependency_spec in project_dependencies:
        dependency_spec = dependency_spec.split(";", 1)[0].strip()
        match = re.match(r"^([A-Za-z0-9_.-]+)(?:\[[^\]]+\])?\s*(.*)$", dependency_spec)
        if not match:
            continue
        requirement = match.group(2).strip()
        name = match.group(1)
        artifacts.append({
            "name": name,
            "version": _extract_dependency_version(requirement),
            "requirement": requirement,
        })

    for group_dependencies in dependency_groups.values():
        for dependency_spec in group_dependencies:
            dependency_spec = dependency_spec.split(";", 1)[0].strip()
            match = re.match(r"^([A-Za-z0-9_.-]+)(?:\[[^\]]+\])?\s*(.*)$", dependency_spec)
            if not match:
                continue
            requirement = match.group(2).strip()
            name = match.group(1)
            artifacts.append({
                "name": name,
                "version": _extract_dependency_version(requirement),
                "requirement": requirement,
            })

    return artifacts


def _build_failure_payload(
    error: Exception,
    profile_id: str,
    *,
    lock_check: str = "not_run",
    dependency_check: str = "not_run",
    rule_id: str | None = None,
) -> dict[str, Any]:
    payload = to_error_payload(error) if hasattr(error, "details") else {
        "ok": False,
        "error": error.__class__.__name__,
        "message": str(error),
        "code": getattr(error, "code", "EnvironmentError"),
    }
    if rule_id:
        payload["rule_id"] = rule_id
    payload.update({
        "status": "failed",
        "profile_id": profile_id,
        "setup_outcome": {
            "status": "failed",
            "policy_check": "failed",
            "lock_check": lock_check,
            "dependency_check": dependency_check,
            "error": payload.get("code", "EnvironmentError"),
        },
    })
    return payload


def run_setup(
    profile_id: str = "local-cpu",
    policy_path: Path | str | None = None,
    profiles_path: Path | str | None = None,
    state_dir: Path | str | None = None,
    dependency_artifacts: list[dict[str, Any]] | None = None,
    dependency_rules_path: Path | str | None = None,
) -> dict[str, Any]:
    policy_result = env_policy.evaluate_policy(profile_id=profile_id, policy_path=policy_path, profiles_path=profiles_path)
    if not policy_result["ok"]:
        error_type = ProfileUnsupported if policy_result["error"] == "ProfileUnsupported" else PolicyViolation
        return _build_failure_payload(error_type(policy_result["message"]), profile_id)

    effective_dependency_artifacts = dependency_artifacts
    if effective_dependency_artifacts is None:
        effective_dependency_artifacts = _load_dependency_artifacts_from_pyproject()

    dependency_result = dependency_policy.evaluate_dependency_policy(
        artifacts=effective_dependency_artifacts,
        rules_path=dependency_rules_path or DEFAULT_DEPENDENCY_RULES_PATH,
    )
    if not dependency_result["ok"]:
        return _build_failure_payload(
            PolicyViolation(dependency_result["message"]),
            profile_id,
            dependency_check="failed",
            rule_id=dependency_result.get("rule_id"),
        )

    state_path = _resolve_state_dir(state_dir)
    policy = load_environment_policy(policy_path)
    virtual_env = policy.get("virtual_environment", {}).get("expectation", ".venv")
    package_entries = [
        {
            "name": "python",
            "version": policy_result.get("python_version", policy.get("python_baseline", {}).get("version", "3.14")),
            "source": policy.get("source_policy", {}).get("default_source", "pypi"),
        }
    ]
    manifest = lock_identity.build_lock_manifest(
        policy_version=policy_result["policy_version"],
        profile_id=profile_id,
        package_entries=package_entries,
        source_context={
            "default_source": policy.get("source_policy", {}).get("default_source", "pypi"),
            "virtual_environment": virtual_env,
        },
    )
    lock_identity.write_lock_manifest(state_path / "lock-manifest.json", manifest)

    return {
        "ok": True,
        "status": "ready",
        "profile_id": profile_id,
        "policy_version": policy_result["policy_version"],
        "venv": virtual_env,
        "setup_command": "uv venv --python 3.14 && uv sync",
        "message": "Environment policy matched the requested profile and setup is ready.",
        "setup_outcome": {
            "status": "ready",
            "policy_check": "passed",
            "lock_check": "verified",
            "dependency_check": "passed",
            "state_dir": str(state_path),
        },
        "dependency_policy": dependency_result,
        "lock_manifest": manifest,
    }


def validate_environment(
    profile_id: str = "local-cpu",
    policy_path: Path | str | None = None,
    profiles_path: Path | str | None = None,
    state_dir: Path | str | None = None,
    dependency_artifacts: list[dict[str, Any]] | None = None,
    dependency_rules_path: Path | str | None = None,
) -> dict[str, Any]:
    outcome = run_setup(
        profile_id=profile_id,
        policy_path=policy_path,
        profiles_path=profiles_path,
        state_dir=state_dir,
        dependency_artifacts=dependency_artifacts,
        dependency_rules_path=dependency_rules_path,
    )
    if outcome["ok"]:
        return {
            **outcome,
            "status": "validated",
            "message": "Policy and profile checks passed without mutation.",
        }
    return outcome


def run_entrypoint(
    profile_id: str = "local-cpu",
    policy_path: Path | str | None = None,
    profiles_path: Path | str | None = None,
    state_dir: Path | str | None = None,
    dependency_artifacts: list[dict[str, Any]] | None = None,
    dependency_rules_path: Path | str | None = None,
    runner: Any | None = None,
) -> dict[str, Any]:
    validation = validate_environment(
        profile_id=profile_id,
        policy_path=policy_path,
        profiles_path=profiles_path,
        state_dir=state_dir,
        dependency_artifacts=dependency_artifacts,
        dependency_rules_path=dependency_rules_path,
    )
    if not validation["ok"]:
        return {
            **validation,
            "status": "preflight-failed",
            "command": "python scripts/train_first_sft.py --config training/configs/first-run-cpu.yaml",
        }

    if profile_id != "local-cpu":
        return {
            **validation,
            "ok": False,
            "status": "preflight-failed",
            "message": f"Profile '{profile_id}' is not currently supported for execution. Only the local-cpu profile is validated in this implementation; other profiles are future work.",
            "command": "python scripts/train_first_sft.py --config training/configs/first-run-cpu.yaml",
        }

    runtime_plan = build_runtime_command(profile_id=profile_id, repo_root=REPO_ROOT)
    command = runtime_plan["command"]
    if runner is None:
        import subprocess

        completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
        if completed.returncode != 0:
            raise PreflightFailure(
                f"Canonical runtime entrypoint exited with code {completed.returncode}"
            )
    else:
        exit_code = runner(command, REPO_ROOT)
        if exit_code != 0:
            raise PreflightFailure(f"Canonical runtime entrypoint exited with code {exit_code}")

    return {
        **validation,
        "status": "ready",
        "command": " ".join(command),
        "runtime_profile": runtime_plan,
        "message": "Preflight checks passed and the canonical training entrypoint was invoked.",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Canonical environment setup and execution contract")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", help="Initialize the environment under the canonical policy")
    setup_parser.add_argument("--profile", default="local-cpu")
    setup_parser.add_argument("--state-dir", default=None)
    setup_parser.add_argument("--dependency-artifacts", default=None)
    setup_parser.add_argument("--dependency-rules-path", default=None)

    validate_parser = subparsers.add_parser("validate", help="Validate policy and profile expectations")
    validate_parser.add_argument("--profile", default="local-cpu")
    validate_parser.add_argument("--state-dir", default=None)
    validate_parser.add_argument("--dependency-artifacts", default=None)
    validate_parser.add_argument("--dependency-rules-path", default=None)

    run_parser = subparsers.add_parser("run", help="Run the canonical training entrypoint after preflight validation")
    run_parser.add_argument("--profile", default="local-cpu")
    run_parser.add_argument("--state-dir", default=None)
    run_parser.add_argument("--dependency-artifacts", default=None)
    run_parser.add_argument("--dependency-rules-path", default=None)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        dependency_artifacts = _parse_dependency_artifacts(getattr(args, "dependency_artifacts", None))
    except json.JSONDecodeError as exc:
        parser.error(str(exc))
        return 2
    if args.command == "setup":
        result = run_setup(
            profile_id=args.profile,
            state_dir=args.state_dir,
            dependency_artifacts=dependency_artifacts,
            dependency_rules_path=args.dependency_rules_path,
        )
    elif args.command == "validate":
        result = validate_environment(
            profile_id=args.profile,
            state_dir=args.state_dir,
            dependency_artifacts=dependency_artifacts,
            dependency_rules_path=args.dependency_rules_path,
        )
    elif args.command == "run":
        result = run_entrypoint(
            profile_id=args.profile,
            state_dir=args.state_dir,
            dependency_artifacts=dependency_artifacts,
            dependency_rules_path=args.dependency_rules_path,
        )
    else:
        parser.error("Unsupported command")
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
