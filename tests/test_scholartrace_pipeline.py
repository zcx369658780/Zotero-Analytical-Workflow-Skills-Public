import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

from scholartrace.policy import adjudicate
from scholartrace.provenance import verify_fixture_manifest
from scholartrace.validation import (
    ValidationError,
    load_json,
    validate_audit_result,
)


def minimal_case():
    return {
        "schema_version": "1.0.0",
        "case_id": "case_demo",
        "title": "Synthetic learning case",
        "educational_scenario": "A bounded fictional classroom exercise.",
        "source_provenance": {
            "synthetic_independently_written": True,
            "reuse_status": "project-authored-synthetic",
            "authoring_method": "Human-authored for ScholarTrace tests.",
            "creation_date": "2026-07-20",
            "license_reuse_note": "Independently written for this repository.",
            "prohibited_content_review": {
                "copied_source_passages": False,
                "private_zotero_content": False,
                "copyrighted_pdf_content": False,
                "purchased_data": False,
                "unpublished_research": False,
                "personal_data": False,
            },
        },
        "sources": [
            {
                "source_id": "source_one",
                "text": "The fictional workshop ran for six weeks with 24 volunteers.",
                "locator": "synthetic://case_demo/source_one",
                "limitations": ["six weeks", "24 volunteers"],
            }
        ],
        "claims": [
            {
                "claim_id": "claim_one",
                "fixture_id": "fixture_supported",
                "text": "The fictional workshop ran for six weeks with 24 volunteers.",
                "claim_type": "descriptive",
            }
        ],
    }


def minimal_proposal():
    return {
        "schema_version": "1.0.0",
        "case_id": "case_demo",
        "proposals": [
            {
                "claim_id": "claim_one",
                "cited_source_ids": ["source_one"],
                "evidence_status": "full_support",
                "material_components": [
                    {
                        "component_id": "component_one",
                        "text": "The workshop duration and sample are stated.",
                        "support_status": "supported",
                    }
                ],
                "missing_or_altered_qualifiers": [],
                "fact_flags": {
                    "causal_overreach": False,
                    "scope_generalization": False,
                    "certainty_magnitude_overreach": False,
                    "contradiction_or_no_support": False,
                    "separable_partial_support": False,
                    "ambiguity_or_conflict": False,
                    "missing_required_context": False,
                    "all_material_components_supported": True,
                    "all_material_qualifiers_supported": True,
                },
                "rationale_candidate": "The claim matches the supplied source.",
                "unresolved_questions": [],
            }
        ],
    }


class ScholarTracePolicyTests(unittest.TestCase):
    def test_supported_requires_full_component_and_qualifier_coverage(self):
        result = adjudicate(minimal_case(), minimal_proposal())

        self.assertEqual(result["claims"][0]["verdict"], "supported")
        self.assertFalse(result["claims"][0]["human_verified"])

        incomplete = minimal_proposal()
        incomplete["proposals"][0]["fact_flags"][
            "all_material_qualifiers_supported"
        ] = False
        result = adjudicate(minimal_case(), incomplete)
        self.assertEqual(result["claims"][0]["verdict"], "unverifiable")

    def test_policy_applies_frozen_fail_closed_priority(self):
        scenarios = [
            (
                {
                    "missing_required_context": True,
                    "contradiction_or_no_support": True,
                },
                "unverifiable",
            ),
            ({"contradiction_or_no_support": True}, "unsupported"),
            ({"causal_overreach": True}, "overstated"),
            (
                {
                    "separable_partial_support": True,
                    "all_material_components_supported": False,
                    "all_material_qualifiers_supported": False,
                },
                "partially_supported",
            ),
        ]

        for flag_changes, expected in scenarios:
            with self.subTest(expected=expected):
                proposal = copy.deepcopy(minimal_proposal())
                proposal_item = proposal["proposals"][0]
                proposal_item["fact_flags"].update(flag_changes)
                if expected == "partially_supported":
                    proposal_item["evidence_status"] = "mixed_support"
                result = adjudicate(minimal_case(), proposal)
                self.assertEqual(result["claims"][0]["verdict"], expected)

    def test_unknown_source_reference_fails_closed(self):
        proposal = minimal_proposal()
        proposal["proposals"][0]["cited_source_ids"] = ["source_missing"]

        with self.assertRaises(ValidationError):
            adjudicate(minimal_case(), proposal)


class ScholarTraceFixtureTests(unittest.TestCase):
    fixture_dir = Path("examples/scholartrace")

    def test_frozen_fixture_set_matches_all_gold_verdicts(self):
        verification = verify_fixture_manifest(self.fixture_dir)
        case_bundle = load_json(
            self.fixture_dir / "education_claim_audit_case.json"
        )
        proposal = load_json(
            self.fixture_dir / "education_claim_audit_proposal.json"
        )
        gold = load_json(
            self.fixture_dir / "education_claim_audit_gold.json"
        )

        result = adjudicate(case_bundle, proposal)
        expected = {
            item["claim_id"]: item["expected_verdict"]
            for item in gold["expectations"]
        }
        actual = {
            item["claim_id"]: item["verdict"] for item in result["claims"]
        }
        result_by_claim = {
            item["claim_id"]: item for item in result["claims"]
        }

        self.assertTrue(verification["valid"])
        self.assertEqual(actual, expected)
        self.assertEqual(
            [item["claim_id"] for item in result["claims"]],
            [item["claim_id"] for item in case_bundle["claims"]],
        )
        for expectation in gold["expectations"]:
            actual_item = result_by_claim[expectation["claim_id"]]
            self.assertEqual(
                [item["source_id"] for item in actual_item["cited_sources"]],
                expectation["required_evidence_ids"],
            )
            self.assertTrue(
                set(expectation["required_rule_flags"])
                <= set(actual_item["deterministic_rule_flags"])
            )
            self.assertFalse(actual_item["human_verified"])
        self.assertEqual(
            set(actual.values()),
            {
                "supported",
                "partially_supported",
                "unsupported",
                "overstated",
                "unverifiable",
            },
        )

    def test_fixture_manifest_detects_content_tampering(self):
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / "scholartrace"
            shutil.copytree(self.fixture_dir, copied)
            self.assertTrue(verify_fixture_manifest(copied)["valid"])

            case_path = copied / "education_claim_audit_case.json"
            case_path.write_bytes(case_path.read_bytes() + b"\n")
            with self.assertRaises(ValidationError):
                verify_fixture_manifest(copied)

    def test_normative_schemas_are_draft_2020_12_and_runtime_is_strict(self):
        schema_names = [
            "scholartrace_case_bundle.schema.json",
            "scholartrace_analysis_proposal.schema.json",
            "scholartrace_audit_result.schema.json",
        ]
        for name in schema_names:
            with self.subTest(schema=name):
                schema = load_json(Path("schemas") / name)
                self.assertEqual(
                    schema["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )
                self.assertEqual(schema["type"], "object")
                self.assertFalse(schema["additionalProperties"])

        invalid_case = minimal_case()
        del invalid_case["title"]
        with self.assertRaises(ValidationError):
            adjudicate(invalid_case, minimal_proposal())

        invalid_proposal = minimal_proposal()
        del invalid_proposal["proposals"][0]["evidence_status"]
        with self.assertRaises(ValidationError):
            adjudicate(minimal_case(), invalid_proposal)

    def test_runtime_rejects_wrong_contract_value_types(self):
        invalid_case = minimal_case()
        invalid_case["sources"][0]["text"] = ["not", "source", "text"]
        with self.assertRaises(ValidationError):
            adjudicate(invalid_case, minimal_proposal())

        invalid_proposal = minimal_proposal()
        invalid_proposal["proposals"][0]["rationale_candidate"] = 42
        with self.assertRaises(ValidationError):
            adjudicate(minimal_case(), invalid_proposal)

    def test_proposal_cannot_override_policy_or_grant_human_authority(self):
        case_bundle = load_json(
            self.fixture_dir / "education_claim_audit_case.json"
        )
        proposal = load_json(
            self.fixture_dir / "education_claim_audit_proposal.json"
        )
        result = adjudicate(case_bundle, proposal)
        causation = next(
            item for item in result["claims"]
            if item["claim_id"] == "claim_causation"
        )

        self.assertEqual(causation["verdict"], "overstated")
        validate_audit_result(result)

        unsafe = copy.deepcopy(result)
        unsafe["claims"][0]["human_verified"] = True
        with self.assertRaises(ValidationError):
            validate_audit_result(unsafe)

        unsafe = copy.deepcopy(result)
        unsafe["claims"][0]["citation_eligible"] = True
        with self.assertRaises(ValidationError):
            validate_audit_result(unsafe)

    def test_private_paths_credentials_contacts_and_prohibited_sources_reject(self):
        mutations = [
            lambda case: case["sources"][0].update(
                {"locator": "C:" + "\\Users\\student\\private-note.md"}
            ),
            lambda case: case["sources"][0].update(
                {"locator": "/" + "home/student/private-note.md"}
            ),
            lambda case: case["sources"][0].update(
                {"locator": "zotero" + "://select/library/items/FAKE1234"}
            ),
            lambda case: case["sources"][0].update(
                {"locator": "synthetic://case_demo/source_one?private=1"}
            ),
            lambda case: case["sources"][0].update(
                {
                    "text": (
                        "Fake test credential "
                        + "sk-"
                        + "TESTONLY000000000000"
                    )
                }
            ),
            lambda case: case["sources"][0].update(
                {
                    "text": (
                        "Contact a fictional person at "
                        + "student"
                        + "@"
                        + "example.invalid"
                    )
                }
            ),
            lambda case: case["source_provenance"][
                "prohibited_content_review"
            ].update({"private_zotero_content": True}),
        ]

        for mutate in mutations:
            with self.subTest(mutation=repr(mutate)):
                case_bundle = minimal_case()
                mutate(case_bundle)
                with self.assertRaises(ValidationError):
                    adjudicate(case_bundle, minimal_proposal())

    def test_packaging_declares_local_standard_library_cli(self):
        with Path("pyproject.toml").open("rb") as handle:
            project = tomllib.load(handle)["project"]

        self.assertEqual(project["version"], "0.1.0")
        self.assertEqual(project["requires-python"], ">=3.11")
        self.assertEqual(project.get("dependencies", []), [])
        self.assertEqual(
            project["scripts"]["scholartrace"],
            "scholartrace.cli:main",
        )


class ScholarTraceCliTests(unittest.TestCase):
    repo_root = Path(__file__).resolve().parents[1]
    fixture_dir = repo_root / "examples" / "scholartrace"

    def test_audit_defaults_to_read_only_byte_stable_stdout(self):
        command = [
            sys.executable,
            "-m",
            "scholartrace",
            "audit",
            "--case",
            str(self.fixture_dir / "education_claim_audit_case.json"),
            "--proposal",
            str(self.fixture_dir / "education_claim_audit_proposal.json"),
        ]
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(self.repo_root)

        with tempfile.TemporaryDirectory() as temporary:
            first = subprocess.run(
                command,
                cwd=temporary,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            second = subprocess.run(
                command,
                cwd=temporary,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(list(Path(temporary).iterdir()), [])
            self.assertEqual(
                len(json.loads(first.stdout)["claims"]),
                7,
            )

    def test_explicit_write_creates_two_files_and_never_overwrites(self):
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(self.repo_root)
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary) / "audit-output"
            command = [
                sys.executable,
                "-m",
                "scholartrace",
                "audit",
                "--case",
                str(self.fixture_dir / "education_claim_audit_case.json"),
                "--proposal",
                str(self.fixture_dir / "education_claim_audit_proposal.json"),
                "--write",
                "--out-dir",
                str(output_dir),
            ]
            first = subprocess.run(
                command,
                cwd=self.repo_root,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(
                sorted(path.name for path in output_dir.iterdir()),
                ["audit_report.md", "claim_evidence_map.json"],
            )
            original = {
                path.name: path.read_bytes() for path in output_dir.iterdir()
            }
            report = (output_dir / "audit_report.md").read_text(
                encoding="utf-8"
            )
            for fixture_id in [
                "fixture_supported",
                "fixture_partially_supported",
                "fixture_unsupported_conclusion",
                "fixture_correlation_as_causation",
                "fixture_omitted_limitations",
                "fixture_unverifiable_missing_context",
                "fixture_conflicting_evidence",
            ]:
                self.assertIn(fixture_id, report)
            self.assertIn("human_verified: false", report)
            self.assertIn("cannot grant E3", report)

            second = subprocess.run(
                command,
                cwd=self.repo_root,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(
                original,
                {
                    path.name: path.read_bytes()
                    for path in output_dir.iterdir()
                },
            )

            missing_out_dir = subprocess.run(
                command[:-2],
                cwd=self.repo_root,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(missing_out_dir.returncode, 0)

            overwrite_attempt = subprocess.run(
                command + ["--overwrite"],
                cwd=self.repo_root,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(overwrite_attempt.returncode, 0)

    def test_validate_and_verify_fixtures_are_read_only(self):
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(self.repo_root)
        commands = [
            [
                sys.executable,
                "-m",
                "scholartrace",
                "validate",
                "--case",
                str(self.fixture_dir / "education_claim_audit_case.json"),
                "--proposal",
                str(
                    self.fixture_dir
                    / "education_claim_audit_proposal.json"
                ),
            ],
            [
                sys.executable,
                "-m",
                "scholartrace",
                "verify-fixtures",
                "--fixture-dir",
                str(self.fixture_dir),
            ],
        ]

        with tempfile.TemporaryDirectory() as temporary:
            for command in commands:
                with self.subTest(command=command[3]):
                    completed = subprocess.run(
                        command,
                        cwd=temporary,
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(
                        completed.returncode, 0, completed.stderr
                    )
                    self.assertTrue(json.loads(completed.stdout)["valid"])
            self.assertEqual(list(Path(temporary).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
