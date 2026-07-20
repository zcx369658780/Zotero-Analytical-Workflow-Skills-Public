"""Local deterministic evaluation and no-overwrite artifact writing."""

import hashlib
from pathlib import Path

from . import __version__
from .policy import POLICY_VERSION
from .render import render_json, render_markdown
from .validation import SCHEMA_VERSION

LIVE_FILENAMES = (
    "gpt56_analysis_proposal.json",
    "gpt56_claim_evidence_map.json",
    "gpt56_audit_report.md",
    "gpt56_run_metadata.json",
    "gpt56_evaluation_summary.md",
)


class OutputCollisionError(RuntimeError):
    """A live output target already exists."""


def _sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest().upper()


def validate_new_output_directory(output_dir):
    output_dir = Path(output_dir)
    lowered_parts = {part.lower() for part in output_dir.parts}
    prohibited = {"zotero", "obsidian", ".obsidian", "researchvault"}
    if lowered_parts & prohibited:
        raise OutputCollisionError("Real research-data destinations are refused")
    if output_dir.exists():
        raise OutputCollisionError("Output directory already exists")
    return output_dir


def build_evaluation(case_bundle, proposal, audit_result, gold):
    """Compare deterministic output with frozen local gold expectations."""
    expected = {
        item["claim_id"]: item for item in gold["expectations"]
    }
    actual = {
        item["claim_id"]: item for item in audit_result["claims"]
    }
    source_ids = {item["source_id"] for item in case_bundle["sources"]}
    source_locators = {
        item["source_id"]: item["locator"] for item in case_bundle["sources"]
    }
    proposal_claim_ids = [item["claim_id"] for item in proposal["proposals"]]
    case_claim_ids = [item["claim_id"] for item in case_bundle["claims"]]

    verdict_matches = {}
    rule_matches = {}
    evidence_matches = {}
    for claim_id, expectation in expected.items():
        audited = actual.get(claim_id, {})
        verdict_matches[claim_id] = (
            audited.get("verdict") == expectation["expected_verdict"]
        )
        rule_matches[claim_id] = set(
            expectation["required_rule_flags"]
        ) <= set(audited.get("deterministic_rule_flags", []))
        evidence_matches[claim_id] = [
            item["source_id"] for item in audited.get("cited_sources", [])
        ] == expectation["required_evidence_ids"]

    cited = [
        source_id
        for item in proposal["proposals"]
        for source_id in item["cited_source_ids"]
    ]
    locators_valid = all(
        source_locators.get(item["source_id"]) == item["locator"]
        for claim in audit_result["claims"]
        for item in claim["cited_sources"]
    )
    authority_keys = {
        "e3",
        "citation_eligible",
        "publication_ready",
        "grading_authority",
    }
    authority_present = any(
        key.lower() in authority_keys
        for claim in audit_result["claims"]
        for key in claim
    )
    human_verified_false = all(
        item["human_verified"] is False for item in audit_result["claims"]
    )
    return {
        "claims_evaluated": len(actual),
        "proposal_claims_exact": proposal_claim_ids == case_claim_ids,
        "source_identifiers_valid": set(cited) <= source_ids,
        "locators_from_supplied_case_only": locators_valid,
        "gold_verdict_agreement": all(verdict_matches.values()),
        "gold_verdict_matches": verdict_matches,
        "required_rule_agreement": all(rule_matches.values()),
        "required_rule_matches": rule_matches,
        "required_evidence_agreement": all(evidence_matches.values()),
        "required_evidence_matches": evidence_matches,
        "human_verified_false": human_verified_false,
        "no_e3": not authority_present,
        "successful": all(
            [
                proposal_claim_ids == case_claim_ids,
                set(cited) <= source_ids,
                locators_valid,
                all(verdict_matches.values()),
                all(rule_matches.values()),
                all(evidence_matches.values()),
                human_verified_false,
                not authority_present,
            ]
        ),
    }


def _render_evaluation_summary(metadata):
    evaluation = metadata["evaluation"]
    usage = metadata.get("usage", {})
    return "\n".join(
        [
            "# ScholarTrace GPT-5.6 Evaluation Summary",
            "",
            f"- Fixture: `{metadata['fixture_set_id']}`",
            f"- Requested model: `{metadata['model_requested']}`",
            f"- Returned model: `{metadata['model_returned']}`",
            f"- Prompt version: `{metadata['prompt_version']}`",
            f"- Attempt: `{metadata['attempt_number']}` of "
            f"`{metadata['authorized_live_attempts']}` authorized",
            f"- Input tokens: `{usage.get('input_tokens')}`",
            f"- Output tokens: `{usage.get('output_tokens')}`",
            f"- Latency ms: `{metadata.get('latency_ms')}`",
            "",
            "## Deterministic evaluation",
            "",
            f"- Schema valid: `{metadata['schema_validation']}`",
            f"- Gold verdict agreement: "
            f"`{evaluation['gold_verdict_agreement']}`",
            f"- Required rule agreement: "
            f"`{evaluation['required_rule_agreement']}`",
            f"- Required evidence agreement: "
            f"`{evaluation['required_evidence_agreement']}`",
            f"- Invented identifiers absent: "
            f"`{evaluation['source_identifiers_valid']}`",
            f"- Supplied locators only: "
            f"`{evaluation['locators_from_supplied_case_only']}`",
            f"- `human_verified: false`: "
            f"`{evaluation['human_verified_false']}`",
            f"- No E3 authority: `{evaluation['no_e3']}`",
            f"- Selected run successful: `{evaluation['successful']}`",
            "",
            "GPT-5.6 generated only the semantic proposal. The frozen "
            "deterministic policy produced all final verdicts. Human review "
            "remains required.",
            "",
        ]
    )


def prepare_live_artifacts(proposal, audit_result, metadata, evaluation):
    proposal_text = render_json(proposal)
    audit_text = render_json(audit_result)
    report_text = render_markdown(audit_result)
    finalized = {
        **metadata,
        "schema_version": SCHEMA_VERSION,
        "tool_version": __version__,
        "deterministic_policy_version": POLICY_VERSION,
        "evaluation": evaluation,
        "artifacts": {
            "gpt56_analysis_proposal.json": _sha256_text(proposal_text),
            "gpt56_claim_evidence_map.json": _sha256_text(audit_text),
            "gpt56_audit_report.md": _sha256_text(report_text),
        },
        "human_verified": False,
        "e3_promoted": False,
    }
    summary_text = _render_evaluation_summary(finalized)
    artifacts = {
        "gpt56_analysis_proposal.json": proposal_text,
        "gpt56_claim_evidence_map.json": audit_text,
        "gpt56_audit_report.md": report_text,
        "gpt56_run_metadata.json": render_json(finalized),
        "gpt56_evaluation_summary.md": summary_text,
    }
    return artifacts, finalized


def write_live_artifacts(output_dir, artifacts):
    output_dir = validate_new_output_directory(output_dir)
    if set(artifacts) != set(LIVE_FILENAMES):
        raise ValueError("Live artifact set must contain exactly five files")
    output_dir.mkdir(parents=True)
    for filename in LIVE_FILENAMES:
        path = output_dir / filename
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(artifacts[filename])
    return list(LIVE_FILENAMES)
