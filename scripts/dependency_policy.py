from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES_PATH = REPO_ROOT / "docs/features/deterministic-python-foundation/policy/dependency-rules.yaml"


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


def load_dependency_rules(path: Path | str | None = None) -> dict[str, Any]:
    return _load_yaml(path, DEFAULT_RULES_PATH)


def _normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")


def _parse_version(value: str) -> tuple[int, ...]:
    parts = []
    for part in re.split(r"[^0-9]+", value.strip()):
        if part:
            parts.append(int(part))
    return tuple(parts) if parts else (0,)


def _compare_versions(left: str, right: str) -> int:
    left_parts = _parse_version(left)
    right_parts = _parse_version(right)
    max_length = max(len(left_parts), len(right_parts))
    padded_left = left_parts + (0,) * (max_length - len(left_parts))
    padded_right = right_parts + (0,) * (max_length - len(right_parts))
    if padded_left < padded_right:
        return -1
    if padded_left > padded_right:
        return 1
    return 0


def _satisfies_requirement(version: str, requirement: str) -> bool:
    requirement = (requirement or "").strip()
    if not requirement:
        return True

    if requirement.startswith(">="):
        return _compare_versions(version, requirement[2:].strip()) >= 0
    if requirement.startswith("<="):
        return _compare_versions(version, requirement[2:].strip()) <= 0
    if requirement.startswith(">"):
        return _compare_versions(version, requirement[1:].strip()) > 0
    if requirement.startswith("<"):
        return _compare_versions(version, requirement[1:].strip()) < 0
    if requirement.startswith("=="):
        return _compare_versions(version, requirement[2:].strip()) == 0
    if requirement.startswith("="):
        return _compare_versions(version, requirement[1:].strip()) == 0
    return version == requirement


def evaluate_dependency_policy(
    artifacts: list[dict[str, Any]] | None = None,
    rules_path: Path | str | None = None,
) -> dict[str, Any]:
    rules_payload = load_dependency_rules(rules_path)
    rules = rules_payload.get("rules", [])
    artifacts = artifacts or []

    normalized_artifacts = {
        _normalize_name(str(artifact.get("name", ""))): artifact
        for artifact in artifacts
        if artifact.get("name")
    }

    violations: list[dict[str, Any]] = []
    evaluated_rules = 0
    for rule in rules:
        dependency_name = rule.get("dependency")
        if not dependency_name:
            continue

        normalized_dependency_name = _normalize_name(str(dependency_name))
        artifact = normalized_artifacts.get(normalized_dependency_name)
        if artifact is None:
            continue

        evaluated_rules += 1
        rule_policy = str(rule.get("policy", "constraint")).lower()
        artifact_version = str(artifact.get("version") or "")
        requirement = str(artifact.get("requirement") or rule.get("requirement") or rule.get("expected_requirement") or "")
        expected_version = str(rule.get("expected_version") or rule.get("version") or "")

        if rule_policy == "pin":
            if not expected_version or artifact_version != expected_version:
                violations.append({
                    "rule_id": rule.get("rule_id", "DPR-000"),
                    "dependency": dependency_name,
                    "expected_version": expected_version,
                    "actual_version": artifact_version,
                    "message": f"{dependency_name} is expected to be pinned to {expected_version}, but resolved to {artifact_version}.",
                })
        elif rule_policy == "constraint":
            if not _satisfies_requirement(artifact_version, requirement):
                violations.append({
                    "rule_id": rule.get("rule_id", "DPR-000"),
                    "dependency": dependency_name,
                    "requirement": requirement,
                    "actual_version": artifact_version,
                    "message": f"{dependency_name} resolved to {artifact_version}, which violates the declared constraint {requirement}.",
                })

    if violations:
        first_violation = violations[0]
        return {
            "ok": False,
            "status": "failed",
            "error": "PolicyViolation",
            "message": first_violation["message"],
            "rule_id": first_violation["rule_id"],
            "dependency": first_violation["dependency"],
            "violations": violations,
            "evaluated_rules": evaluated_rules,
        }

    return {
        "ok": True,
        "status": "passed",
        "message": "Dependency policy matched the declared version boundaries.",
        "evaluated_rules": evaluated_rules,
    }
