"""Command-line interface for deterministic ScholarTrace audits."""

import argparse
import sys
from pathlib import Path

from .policy import adjudicate
from .provenance import verify_fixture_manifest
from .render import render_json, render_markdown
from .validation import (
    ValidationError,
    load_json,
    validate_analysis_proposal,
    validate_case_bundle,
)


def _build_parser():
    parser = argparse.ArgumentParser(prog="scholartrace")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate", help="Validate case, proposal, and fixture provenance."
    )
    validate.add_argument("--case", required=True)
    validate.add_argument("--proposal", required=True)

    audit = subparsers.add_parser(
        "audit", help="Run a deterministic claim-evidence audit."
    )
    audit.add_argument("--case", required=True)
    audit.add_argument("--proposal", required=True)
    audit.add_argument("--write", action="store_true")
    audit.add_argument("--out-dir")

    verify = subparsers.add_parser(
        "verify-fixtures", help="Verify frozen synthetic fixture hashes."
    )
    verify.add_argument("--fixture-dir", required=True)
    return parser


def _write_new_output(output_dir, result):
    output_dir = Path(output_dir)
    if output_dir.exists():
        raise ValidationError("Output directory already exists; overwrite refused")
    output_dir.mkdir(parents=True)
    json_path = output_dir / "claim_evidence_map.json"
    report_path = output_dir / "audit_report.md"
    with json_path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(render_json(result))
    with report_path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(render_markdown(result))
    return [json_path.name, report_path.name]


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "verify-fixtures":
            sys.stdout.write(
                render_json(verify_fixture_manifest(args.fixture_dir))
            )
            return 0
        if args.command == "validate":
            case_path = Path(args.case)
            proposal_path = Path(args.proposal)
            if case_path.parent.resolve() != proposal_path.parent.resolve():
                raise ValidationError(
                    "Case and proposal must share a fixture directory"
                )
            case_bundle = validate_case_bundle(load_json(case_path))
            proposal = validate_analysis_proposal(
                load_json(proposal_path), case_bundle
            )
            verification = verify_fixture_manifest(case_path.parent)
            adjudicate(case_bundle, proposal)
            sys.stdout.write(
                render_json(
                    {
                        "valid": True,
                        "case_id": case_bundle["case_id"],
                        "fixture_set_id": verification["fixture_set_id"],
                        "fixture_hashes_valid": True,
                    }
                )
            )
            return 0
        if args.command == "audit":
            case_bundle = load_json(args.case)
            proposal = load_json(args.proposal)
            result = adjudicate(case_bundle, proposal)
            if args.write:
                if not args.out_dir:
                    raise ValidationError("--write requires --out-dir")
                written = _write_new_output(args.out_dir, result)
                sys.stdout.write(
                    render_json(
                        {
                            "status": "written",
                            "files": sorted(written),
                            "no_overwrite": True,
                        }
                    )
                )
            else:
                if args.out_dir:
                    raise ValidationError("--out-dir requires --write")
                sys.stdout.write(render_json(result))
            return 0
    except ValidationError as exc:
        parser.exit(2, f"scholartrace: validation failed: {exc}\n")
    return 2
