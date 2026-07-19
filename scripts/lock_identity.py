from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def _canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def build_lock_manifest(
    policy_version: str,
    profile_id: str,
    package_entries: list[dict[str, Any]],
    resolver_identity: str = "uv-sync",
    source_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    normalized_entries = []
    for entry in sorted(package_entries, key=lambda item: (item.get("name", ""), item.get("version", ""), item.get("source", ""))):
        normalized_entries.append(
            {
                "name": entry.get("name", ""),
                "version": entry.get("version", ""),
                "source": entry.get("source", ""),
                "extra": entry.get("extra"),
            }
        )

    source_payload = {
        "policy_version": policy_version,
        "profile_id": profile_id,
        "resolver_identity": resolver_identity,
        "package_entries": normalized_entries,
        "source_context": source_context or {},
    }
    manifest = {
        "lock_version": "1.0",
        "resolver_identity": resolver_identity,
        "policy_version": policy_version,
        "profile_id": profile_id,
        "package_entries": normalized_entries,
        "source_digest": _digest(source_payload),
    }
    manifest["manifest_digest"] = _digest({key: value for key, value in manifest.items() if key != "manifest_digest"})
    return manifest


def validate_lock_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    expected_digest = _digest({key: value for key, value in manifest.items() if key != "manifest_digest"})
    actual_digest = manifest.get("manifest_digest")
    return {
        "ok": actual_digest == expected_digest,
        "expected_manifest_digest": expected_digest,
        "actual_manifest_digest": actual_digest,
    }


def write_lock_manifest(path: Path | str, manifest: dict[str, Any]) -> Path:
    resolved_path = Path(path)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return resolved_path


def load_lock_manifest(path: Path | str) -> dict[str, Any]:
    resolved_path = Path(path)
    with resolved_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
