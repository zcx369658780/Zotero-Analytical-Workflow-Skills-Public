"""Command-line interface for deterministic ScholarTrace audits."""

import argparse
import sys
from pathlib import Path

from .evaluation import (
    LIVE_FILENAMES,
    OutputCollisionError,
    build_evaluation,
    prepare_live_artifacts,
    validate_new_output_directory,
    write_live_artifacts,
)
from .policy import adjudicate
from .provenance import verify_fixture_manifest
from .providers.openai_responses import (
    DEFAULT_MAX_OUTPUT_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_REASONING_EFFORT,
    MissingCredentialError,
    MissingSDKError,
    ModelAPIError,
    ModelResponseError,
    ProviderError,
    UnsupportedModelError,
    describe_request,
    generate_proposal,
)
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

    propose = subparsers.add_parser(
        "propose", help="Run the bounded GPT-5.6 proposal and audit path."
    )
    propose.add_argument("--case", required=True)
    propose.add_argument(
        "--schema",
        default="schemas/scholartrace_analysis_proposal.schema.json",
    )
    propose.add_argument(
        "--gold",
        default="examples/scholartrace/education_claim_audit_gold.json",
    )
    propose.add_argument("--model", default=DEFAULT_MODEL)
    propose.add_argument(
        "--reasoning-effort",
        default=DEFAULT_REASONING_EFFORT,
        choices=["none", "low", "medium", "high", "xhigh", "max"],
    )
    propose.add_argument(
        "--max-output-tokens",
        type=int,
        default=DEFAULT_MAX_OUTPUT_TOKENS,
    )
    propose.add_argument("--attempt", type=int, default=1)
    propose.add_argument("--dry-run", action="store_true")
    propose.add_argument("--live", action="store_true")
    propose.add_argument("--write", action="store_true")
    propose.add_argument("--out-dir")

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
        if args.command == "propose":
            if args.dry_run == args.live:
                raise ValidationError(
                    "Choose exactly one of --dry-run or --live"
                )
            case_bundle = validate_case_bundle(load_json(args.case))
            proposal_schema = load_json(args.schema)
            gold = load_json(args.gold)
            description = describe_request(
                case_bundle,
                proposal_schema,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                max_output_tokens=args.max_output_tokens,
            )
            if args.dry_run:
                sys.stdout.write(
                    render_json(
                        {
                            **description,
                            "dry_run": True,
                            "api_called": False,
                            "write_requested": args.write,
                            "output_directory_supplied": bool(args.out_dir),
                            "intended_files": list(LIVE_FILENAMES),
                        }
                    )
                )
                return 0
            if not args.write or not args.out_dir:
                raise ValidationError(
                    "--live requires --write and --out-dir"
                )
            validate_new_output_directory(args.out_dir)
            proposal, metadata = generate_proposal(
                case_bundle,
                proposal_schema,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                max_output_tokens=args.max_output_tokens,
                attempt_number=args.attempt,
            )
            result = adjudicate(case_bundle, proposal)
            evaluation = build_evaluation(
                case_bundle, proposal, result, gold
            )
            metadata["fixture_set_id"] = gold["fixture_set_id"]
            metadata["fixture_file_sha256"] = (
                verify_fixture_manifest(Path(args.case).parent)["hashes"][
                    Path(args.case).name
                ]
            )
            artifacts, finalized = prepare_live_artifacts(
                proposal, result, metadata, evaluation
            )
            write_live_artifacts(args.out_dir, artifacts)
            sys.stdout.write(
                render_json(
                    {
                        "status": (
                            "successful"
                            if evaluation["successful"]
                            else "failed_closed"
                        ),
                        "files": list(LIVE_FILENAMES),
                        "model_requested": finalized["model_requested"],
                        "model_returned": finalized["model_returned"],
                        "attempt_number": finalized["attempt_number"],
                        "gold_verdict_agreement": evaluation[
                            "gold_verdict_agreement"
                        ],
                        "required_rule_agreement": evaluation[
                            "required_rule_agreement"
                        ],
                    }
                )
            )
            return 0 if evaluation["successful"] else 7
    except MissingSDKError as exc:
        sys.stderr.write(f"scholartrace: missing SDK: {exc}\n")
        return 3
    except MissingCredentialError as exc:
        sys.stderr.write(f"scholartrace: missing credential: {exc}\n")
        return 4
    except ModelAPIError as exc:
        sys.stderr.write(f"scholartrace: model API failure: {exc}\n")
        return 5
    except ModelResponseError as exc:
        sys.stderr.write(f"scholartrace: model schema failure: {exc}\n")
        return 6
    except OutputCollisionError as exc:
        sys.stderr.write(f"scholartrace: output collision: {exc}\n")
        return 8
    except UnsupportedModelError as exc:
        sys.stderr.write(f"scholartrace: unsupported model: {exc}\n")
        return 2
    except ProviderError as exc:
        sys.stderr.write(f"scholartrace: provider failure: {exc}\n")
        return 5
    except ValidationError as exc:
        parser.exit(2, f"scholartrace: validation failed: {exc}\n")
    return 2
