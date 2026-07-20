"""Deterministic ScholarTrace verdict policy."""

from . import __version__
from .validation import (
    validate_analysis_proposal,
    validate_audit_result,
    validate_case_bundle,
)

POLICY_VERSION = "scholartrace-policy-0.1.0"


def _derive_verdict(proposal):
    flags = proposal["fact_flags"]
    evidence_status = proposal["evidence_status"]
    triggered = [name for name, value in flags.items() if value]

    if (
        flags["missing_required_context"]
        or flags["ambiguity_or_conflict"]
        or evidence_status in {"conflicting", "insufficient_context"}
    ):
        return "unverifiable", triggered, ["unverifiable_safety_condition"]
    if (
        flags["contradiction_or_no_support"]
        or evidence_status == "no_support"
    ):
        return "unsupported", triggered, ["contradiction_or_no_support"]
    if (
        flags["causal_overreach"]
        or flags["scope_generalization"]
        or flags["certainty_magnitude_overreach"]
    ):
        return "overstated", triggered, ["strength_or_scope_overreach"]
    if (
        flags["separable_partial_support"]
        and evidence_status == "mixed_support"
    ):
        return "partially_supported", triggered, ["separable_mixed_support"]
    if (
        evidence_status == "full_support"
        and flags["all_material_components_supported"]
        and flags["all_material_qualifiers_supported"]
    ):
        return "supported", triggered, ["full_coverage_supported"]
    return "unverifiable", triggered, ["unclassified_fail_closed"]


def adjudicate(case_bundle, analysis_proposal):
    """Derive audit verdicts from supplied case and proposal data."""
    validate_case_bundle(case_bundle)
    validate_analysis_proposal(analysis_proposal, case_bundle)
    sources = {source["source_id"]: source for source in case_bundle["sources"]}
    proposals = {
        proposal["claim_id"]: proposal
        for proposal in analysis_proposal["proposals"]
    }
    claims = []
    for claim in case_bundle["claims"]:
        proposal = proposals[claim["claim_id"]]
        verdict, triggered, trace = _derive_verdict(proposal)
        claims.append(
            {
                "claim_id": claim["claim_id"],
                "fixture_id": claim["fixture_id"],
                "claim_text": claim["text"],
                "verdict": verdict,
                "cited_sources": [
                    {
                        "source_id": source_id,
                        "locator": sources[source_id]["locator"],
                    }
                    for source_id in proposal["cited_source_ids"]
                ],
                "rationale": proposal["rationale_candidate"],
                "missing_or_altered_qualifiers": proposal[
                    "missing_or_altered_qualifiers"
                ],
                "deterministic_rule_flags": triggered,
                "policy_trace": trace,
                "unresolved_questions": proposal["unresolved_questions"],
                "human_review_reason": (
                    "Human review is required before academic use."
                ),
                "human_verified": False,
            }
        )
    result = {
        "schema_version": "1.0.0",
        "tool_version": __version__,
        "case_id": case_bundle["case_id"],
        "deterministic_policy_version": POLICY_VERSION,
        "execution": {"read_only_inputs": True, "no_overwrite": True},
        "provenance_summary": {
            "synthetic_independently_written": case_bundle[
                "source_provenance"
            ]["synthetic_independently_written"]
        },
        "claims": claims,
    }
    return validate_audit_result(result)
