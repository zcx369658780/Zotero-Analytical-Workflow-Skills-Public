import copy
import contextlib
import io
import json
import os
import tempfile
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from scholartrace.cli import main
from scholartrace.evaluation import (
    OutputCollisionError,
    build_evaluation,
    prepare_live_artifacts,
    write_live_artifacts,
)
from scholartrace.policy import adjudicate
from scholartrace.prompt import (
    PROMPT_VERSION,
    build_prompt,
    strict_proposal_schema,
)
from scholartrace.providers.openai_responses import (
    MissingCredentialError,
    MissingSDKError,
    ModelResponseError,
    UnsupportedModelError,
    create_official_client,
    generate_proposal,
)
from scholartrace.validation import load_json


FIXTURE_DIR = Path("examples/scholartrace")
CASE_PATH = FIXTURE_DIR / "education_claim_audit_case.json"
GOLD_PATH = FIXTURE_DIR / "education_claim_audit_gold.json"
SCHEMA_PATH = Path("schemas/scholartrace_analysis_proposal.schema.json")


class FakeResponses:
    def __init__(self, output_text, model="gpt-5.6-sol"):
        self.output_text = output_text
        self.model = model
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            output_text=self.output_text,
            model=self.model,
            id="resp_not_retained",
            created_at=1784510000,
            usage=SimpleNamespace(
                input_tokens=100,
                output_tokens=200,
                total_tokens=300,
            ),
        )


class FakeClient:
    def __init__(self, output_text, model="gpt-5.6-sol"):
        self.responses = FakeResponses(output_text, model=model)


def fixture_case():
    return load_json(CASE_PATH)


def fixture_proposal():
    return load_json(
        FIXTURE_DIR / "education_claim_audit_proposal.json"
    )


def proposal_schema():
    return load_json(SCHEMA_PATH)


class OpenAIProviderTests(unittest.TestCase):
    def test_prompt_and_request_are_bounded_and_strict(self):
        case_bundle = fixture_case()
        fake = FakeClient(json.dumps(fixture_proposal()))

        proposal, metadata = generate_proposal(
            case_bundle,
            proposal_schema(),
            model="gpt-5.6-sol",
            attempt_number=1,
            client=fake,
            sdk_version="test-sdk",
        )

        self.assertEqual(proposal["case_id"], case_bundle["case_id"])
        self.assertEqual(len(fake.responses.calls), 1)
        request = fake.responses.calls[0]
        self.assertEqual(request["model"], "gpt-5.6-sol")
        self.assertFalse(request["store"])
        self.assertFalse(request["background"])
        self.assertEqual(request["reasoning"], {"effort": "medium"})
        self.assertEqual(request["max_output_tokens"], 8000)
        self.assertNotIn("tools", request)
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertEqual(
            request["text"]["format"]["type"], "json_schema"
        )
        self.assertEqual(metadata["prompt_version"], PROMPT_VERSION)
        self.assertTrue(metadata["request_configuration"]["no_tools"])
        serialized = json.dumps(metadata, sort_keys=True)
        for forbidden in [
            "api_key",
            "authorization",
            "headers",
            "instructions",
            "client",
            "resp_not_retained",
        ]:
            self.assertNotIn(forbidden, serialized.lower())

    def test_strict_schema_removes_proposal_verdict_authority(self):
        strict = strict_proposal_schema(proposal_schema())

        proposal_properties = strict["$defs"]["proposal"]["properties"]
        self.assertNotIn("suggested_final_verdict", proposal_properties)
        self.assertEqual(
            set(proposal_properties),
            set(strict["$defs"]["proposal"]["required"]),
        )

    def test_missing_key_and_missing_sdk_fail_without_discovery(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(MissingCredentialError):
                create_official_client()

        with mock.patch.dict(
            os.environ, {"OPENAI_API_KEY": "opaque-test-only"}, clear=True
        ):
            with mock.patch(
                "scholartrace.providers.openai_responses._load_sdk",
                side_effect=ImportError,
            ):
                with self.assertRaises(MissingSDKError):
                    create_official_client()

    def test_non_gpt56_model_is_rejected_before_client_use(self):
        fake = FakeClient(json.dumps(fixture_proposal()))

        with self.assertRaises(UnsupportedModelError):
            generate_proposal(
                fixture_case(),
                proposal_schema(),
                model="gpt-5.5",
                attempt_number=1,
                client=fake,
                sdk_version="test-sdk",
            )
        self.assertEqual(fake.responses.calls, [])

    def test_malformed_and_invented_identifiers_fail_closed(self):
        malformed = FakeClient("{not-json")
        with self.assertRaises(ModelResponseError):
            generate_proposal(
                fixture_case(),
                proposal_schema(),
                model="gpt-5.6-sol",
                attempt_number=1,
                client=malformed,
                sdk_version="test-sdk",
            )

        invented = fixture_proposal()
        invented["proposals"][0]["cited_source_ids"] = ["source_invented"]
        fake = FakeClient(json.dumps(invented))
        with self.assertRaises(ModelResponseError):
            generate_proposal(
                fixture_case(),
                proposal_schema(),
                model="gpt-5.6-sol",
                attempt_number=1,
                client=fake,
                sdk_version="test-sdk",
            )

    def test_model_cannot_override_deterministic_downgrade_or_authority(self):
        proposal = fixture_proposal()
        causation = next(
            item
            for item in proposal["proposals"]
            if item["claim_id"] == "claim_causation"
        )
        causation["suggested_final_verdict"] = "supported"
        fake = FakeClient(json.dumps(proposal))

        generated, _ = generate_proposal(
            fixture_case(),
            proposal_schema(),
            model="gpt-5.6-sol",
            attempt_number=1,
            client=fake,
            sdk_version="test-sdk",
        )
        result = adjudicate(fixture_case(), generated)
        audited = next(
            item
            for item in result["claims"]
            if item["claim_id"] == "claim_causation"
        )
        self.assertEqual(audited["verdict"], "overstated")
        self.assertFalse(audited["human_verified"])
        self.assertNotIn("citation_eligible", result)

        unsafe = copy.deepcopy(fixture_proposal())
        unsafe["proposals"][0]["human_verified"] = True
        with self.assertRaises(ModelResponseError):
            generate_proposal(
                fixture_case(),
                proposal_schema(),
                model="gpt-5.6-sol",
                attempt_number=1,
                client=FakeClient(json.dumps(unsafe)),
                sdk_version="test-sdk",
            )


class LiveEvaluationTests(unittest.TestCase):
    def test_evaluation_and_five_file_write_are_no_overwrite(self):
        case_bundle = fixture_case()
        proposal = fixture_proposal()
        audit = adjudicate(case_bundle, proposal)
        evaluation = build_evaluation(
            case_bundle,
            proposal,
            audit,
            load_json(GOLD_PATH),
        )
        metadata = {
            "fixture_set_id": "scholartrace_education_claim_audit_v1",
            "model_requested": "gpt-5.6-sol",
            "model_returned": "gpt-5.6-sol",
            "prompt_version": PROMPT_VERSION,
            "attempt_number": 1,
            "authorized_live_attempts": 3,
            "request_configuration": {
                "store": False,
                "no_tools": True,
            },
            "schema_validation": True,
        }
        artifacts, finalized = prepare_live_artifacts(
            proposal, audit, metadata, evaluation
        )

        self.assertEqual(len(artifacts), 5)
        self.assertTrue(finalized["evaluation"]["gold_verdict_agreement"])
        self.assertTrue(finalized["evaluation"]["required_rule_agreement"])
        self.assertTrue(finalized["evaluation"]["no_e3"])
        self.assertTrue(finalized["evaluation"]["human_verified_false"])

        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary) / "gpt56-output"
            written = write_live_artifacts(output_dir, artifacts)
            before = {
                path.name: path.read_bytes() for path in output_dir.iterdir()
            }
            self.assertEqual(sorted(written), sorted(artifacts))
            with self.assertRaises(OutputCollisionError):
                write_live_artifacts(output_dir, artifacts)
            after = {
                path.name: path.read_bytes() for path in output_dir.iterdir()
            }
            self.assertEqual(before, after)

    def test_cli_dry_run_never_calls_provider_or_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary) / "unused"
            with mock.patch(
                "scholartrace.cli.generate_proposal",
                side_effect=AssertionError("provider must not be called"),
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    exit_code = main(
                        [
                            "propose",
                            "--case",
                            str(CASE_PATH),
                            "--schema",
                            str(SCHEMA_PATH),
                            "--gold",
                            str(GOLD_PATH),
                            "--dry-run",
                            "--out-dir",
                            str(output_dir),
                        ]
                    )
            self.assertEqual(exit_code, 0)
            self.assertFalse(output_dir.exists())

    def test_cli_collision_refuses_before_provider_call(self):
        with tempfile.TemporaryDirectory() as temporary:
            with mock.patch(
                "scholartrace.cli.generate_proposal",
                side_effect=AssertionError("provider must not be called"),
            ):
                with contextlib.redirect_stderr(io.StringIO()):
                    exit_code = main(
                        [
                            "propose",
                            "--case",
                            str(CASE_PATH),
                            "--schema",
                            str(SCHEMA_PATH),
                            "--gold",
                            str(GOLD_PATH),
                            "--live",
                            "--write",
                            "--out-dir",
                            temporary,
                        ]
                    )
            self.assertEqual(exit_code, 8)

    def test_packaging_keeps_offline_core_and_bounded_sdk_extra(self):
        with Path("pyproject.toml").open("rb") as handle:
            project = tomllib.load(handle)["project"]

        self.assertEqual(project["dependencies"], [])
        self.assertEqual(
            project["optional-dependencies"]["openai"],
            ["openai>=2.43.0,<3"],
        )
        with Path("pyproject.toml").open("rb") as handle:
            packaging = tomllib.load(handle)["tool"]["setuptools"]
        self.assertEqual(
            packaging["packages"],
            ["scholartrace", "scholartrace.providers"],
        )

    def test_prompt_is_public_and_contains_required_boundaries(self):
        prompt = build_prompt(fixture_case())
        normalized = " ".join(prompt.lower().split())
        for required in [
            "semantic proposal generator",
            "every supplied claim_id exactly once",
            "correlation",
            "causation",
            "sample",
            "period",
            "scope",
            "no external knowledge",
            "human_verified",
            "E3",
        ]:
            self.assertIn(required.lower(), normalized)


if __name__ == "__main__":
    unittest.main()
