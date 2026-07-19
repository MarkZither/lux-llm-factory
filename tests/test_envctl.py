import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import dependency_policy
from scripts import envctl
from scripts import env_policy
from scripts import lock_identity
from scripts import train_first_sft


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

    def test_dependency_rules_are_loaded_and_can_report_rule_ids(self) -> None:
        result = dependency_policy.evaluate_dependency_policy(
            artifacts=[{"name": "torch", "version": "2.4.0", "requirement": ">=2.4.0"}],
            rules_path=Path("docs/features/deterministic-python-foundation/policy/dependency-rules.yaml"),
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["evaluated_rules"], 1)

    def test_environment_validation_reports_dependency_rule_violations(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            outcome = envctl.validate_environment(
                profile_id="local-cpu",
                dependency_artifacts=[{"name": "transformers", "version": "4.43.0", "requirement": ">=4.44.0"}],
                state_dir=Path(tmpdir),
            )

            self.assertFalse(outcome["ok"])
            self.assertEqual(outcome["setup_outcome"]["dependency_check"], "failed")
            self.assertEqual(outcome["rule_id"], "DPR-002")

    def test_default_validation_path_evaluates_dependency_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            outcome = envctl.validate_environment(profile_id="local-cpu", state_dir=Path(tmpdir))

            self.assertIn("dependency_policy", outcome)
            self.assertGreater(outcome["dependency_policy"]["evaluated_rules"], 0)

    def test_run_entrypoint_executes_canonical_training_command_after_preflight(self) -> None:
        calls: list[tuple[list[str], Path]] = []

        def runner(command: list[str], cwd: Path) -> int:
            calls.append((command, cwd))
            return 0

        with tempfile.TemporaryDirectory() as tmpdir:
            outcome = envctl.run_entrypoint(profile_id="local-cpu", state_dir=Path(tmpdir), runner=runner)

        self.assertTrue(outcome["ok"])
        self.assertEqual(outcome["status"], "ready")
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0][0], sys.executable)
        self.assertTrue(calls[0][0][1].endswith("scripts/train_first_sft.py"))
        self.assertEqual(calls[0][0][2], "--config")

    def test_run_entrypoint_marks_non_local_profiles_as_future_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            outcome = envctl.run_entrypoint(profile_id="runpod", state_dir=Path(tmpdir))

        self.assertFalse(outcome["ok"])
        self.assertEqual(outcome["status"], "preflight-failed")
        self.assertIn("future work", outcome["message"])

    def test_training_entrypoint_uses_processing_class_for_current_trl_api(self) -> None:
        kwargs = train_first_sft.build_sft_trainer_kwargs(
            model=object(),
            args=object(),
            train_dataset=object(),
            eval_dataset=None,
            tokenizer=object(),
            dataset_text_field="text",
            max_seq_length=128,
            peft_config=None,
        )

        self.assertIn("processing_class", kwargs)
        self.assertNotIn("tokenizer", kwargs)

    def test_training_entrypoint_uses_formatting_func_for_current_trl_api(self) -> None:
        kwargs = train_first_sft.build_sft_trainer_kwargs(
            model=object(),
            args=object(),
            train_dataset=object(),
            eval_dataset=None,
            tokenizer=object(),
            dataset_text_field="text",
            max_seq_length=128,
            peft_config=None,
        )

        self.assertIn("formatting_func", kwargs)
        self.assertNotIn("dataset_text_field", kwargs)


if __name__ == "__main__":
    unittest.main()
