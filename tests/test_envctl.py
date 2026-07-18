import tomllib
import unittest
from pathlib import Path

from scripts import envctl


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


if __name__ == "__main__":
    unittest.main()
