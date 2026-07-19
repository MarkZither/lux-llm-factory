import tempfile
import tomllib
import unittest
from pathlib import Path

from scripts import envctl
from scripts import env_policy
from scripts import lock_identity


class EnvctlCliTests(unittest.TestCase):
    def test_policy_and_profiles_are_loaded_from_feature_documents(self) -> None:
        policy = envctl.load_environment_policy(
            Path("docs/features/deterministic-python-foundation/policy/environment-policy.yaml")
        )
        profiles = envctl.load_profiles(
            Path("docs/features/deterministic-python-foundation/policy/profiles.yaml")
        )

        self.assertEqual(policy["policy_version"], "1.0")
        self.assertIn("local-cpu", profiles)
        self.assertEqual(profiles["local-cpu"]["support_level"], "baseline")

    def test_setup_command_returns_deterministic_outcome(self) -> None:
        outcome = envctl.run_setup(profile_id="local-cpu")
        self.assertTrue(outcome["ok"])
        self.assertEqual(outcome["profile_id"], "local-cpu")
        self.assertEqual(outcome["status"], "ready")
        self.assertIn("uv", outcome["setup_command"])

    def test_optional_dependency_groups_are_resolvable(self) -> None:
        with Path("pyproject.toml").open("rb") as handle:
            metadata = tomllib.load(handle)

        groups = metadata.get("dependency-groups", {})
        self.assertIn("qlora", groups)
        self.assertNotIn("axolotl", groups)

    def test_setup_reports_structured_outcome_and_writes_lock_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            outcome = envctl.run_setup(profile_id="local-cpu", state_dir=Path(tmpdir))

            self.assertTrue(outcome["ok"])
            self.assertEqual(outcome["status"], "ready")
            self.assertEqual(outcome["setup_outcome"]["status"], "ready")
            self.assertEqual(outcome["setup_outcome"]["policy_check"], "passed")
            self.assertEqual(outcome["setup_outcome"]["lock_check"], "verified")
            self.assertTrue((Path(tmpdir) / "lock-manifest.json").exists())

    def test_policy_evaluation_rejects_unsupported_profiles(self) -> None:
        result = env_policy.evaluate_policy(profile_id="unsupported", policy_path=Path("docs/features/deterministic-python-foundation/policy/environment-policy.yaml"), profiles_path=Path("docs/features/deterministic-python-foundation/policy/profiles.yaml"))

        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "ProfileUnsupported")

    def test_lock_identity_is_deterministic_for_same_inputs(self) -> None:
        manifest_a = lock_identity.build_lock_manifest(
            policy_version="1.0",
            profile_id="local-cpu",
            package_entries=[{"name": "torch", "version": "2.4.0", "source": "pypi"}],
        )
        manifest_b = lock_identity.build_lock_manifest(
            policy_version="1.0",
            profile_id="local-cpu",
            package_entries=[{"name": "torch", "version": "2.4.0", "source": "pypi"}],
        )

        self.assertEqual(manifest_a["manifest_digest"], manifest_b["manifest_digest"])
        self.assertEqual(manifest_a["source_digest"], manifest_b["source_digest"])


if __name__ == "__main__":
    unittest.main()
