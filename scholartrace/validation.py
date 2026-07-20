"""Strict runtime validation for ScholarTrace's normative contracts."""

import json
import re
from pathlib import Path

SCHEMA_VERSION = "1.0.0"
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]{2,63}$")
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
TOKEN_PATTERN = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{12,}|gh[oprsu]_[A-Za-z0-9_]{12,})\b",
    re.IGNORECASE,
)
WINDOWS_ABSOLUTE_PATTERN = re.compile(
    r"(?:^|[\s\"'(])(?:[A-Za-z]:[\\/]|\\\\)"
)
POSIX_PRIVATE_PATTERN = re.compile(
    r"(?:^|[\s\"'(])/(?:Users|home|private|mnt|var|tmp)/",
    re.IGNORECASE,
)
PRIVATE_SCHEME_PATTERN = re.compile(
    r"\b(?:file|zotero|obsidian)://", re.IGNORECASE
)
PDF_PATH_PATTERN = re.compile(r"(?:^|[\\/])[^/\\\s]+\.pdf\b", re.IGNORECASE)
SYNTHETIC_LOCATOR_PATTERN = re.compile(r"^synthetic://[a-z0-9_/]+$")
VERDICTS = {
    "supported",
    "partially_supported",
    "unsupported",
    "overstated",
    "unverifiable",
}


class ValidationError(ValueError):
    """Raised when ScholarTrace input fails closed."""


def load_json(path):
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"Cannot load valid JSON from {path}") from exc


def _require_fields(value, fields, label):
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    missing = sorted(set(fields) - set(value))
    if missing:
        raise ValidationError(f"{label} missing fields: {', '.join(missing)}")


def _require_exact_fields(value, required, label, optional=()):
    _require_fields(value, required, label)
    unexpected = sorted(set(value) - set(required) - set(optional))
    if unexpected:
        raise ValidationError(
            f"{label} has unexpected fields: {', '.join(unexpected)}"
        )


def _validate_id(value, label):
    if not isinstance(value, str) or not ID_PATTERN.fullmatch(value):
        raise ValidationError(f"{label} must be a stable lowercase identifier")


def _require_nonempty_string(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")


def _require_list(value, label, allow_empty=True):
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ValidationError(f"{label} must be a list")


def _require_string_list(value, label, allow_empty=True):
    _require_list(value, label, allow_empty=allow_empty)
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValidationError(f"{label} must contain non-empty strings")


def _unique_ids(items, key, label):
    values = [item.get(key) for item in items]
    if len(values) != len(set(values)):
        raise ValidationError(f"{label} identifiers must be unique")


def _scan_sensitive_values(value, label):
    if isinstance(value, dict):
        for child in value.values():
            _scan_sensitive_values(child, label)
    elif isinstance(value, list):
        for child in value:
            _scan_sensitive_values(child, label)
    elif isinstance(value, str):
        if EMAIL_PATTERN.search(value):
            raise ValidationError(f"{label} contains a personal contact detail")
        if TOKEN_PATTERN.search(value):
            raise ValidationError(f"{label} contains a credential-like value")
        if (
            WINDOWS_ABSOLUTE_PATTERN.search(value)
            or POSIX_PRIVATE_PATTERN.search(value)
            or PRIVATE_SCHEME_PATTERN.search(value)
            or PDF_PATH_PATTERN.search(value)
        ):
            raise ValidationError(f"{label} contains a private or prohibited path")


def validate_case_bundle(case_bundle):
    _scan_sensitive_values(case_bundle, "case bundle")
    _require_exact_fields(
        case_bundle,
        [
            "schema_version",
            "case_id",
            "title",
            "educational_scenario",
            "source_provenance",
            "sources",
            "claims",
        ],
        "case bundle",
    )
    if case_bundle["schema_version"] != SCHEMA_VERSION:
        raise ValidationError("Unsupported case schema_version")
    _validate_id(case_bundle["case_id"], "case_id")
    _require_nonempty_string(case_bundle["title"], "case title")
    _require_nonempty_string(
        case_bundle["educational_scenario"], "educational scenario"
    )
    _require_list(case_bundle["sources"], "sources", allow_empty=False)
    _require_list(case_bundle["claims"], "claims", allow_empty=False)
    if not case_bundle["sources"] or not case_bundle["claims"]:
        raise ValidationError("Case bundle requires sources and claims")
    provenance = case_bundle["source_provenance"]
    provenance_fields = [
        "synthetic_independently_written",
        "reuse_status",
        "authoring_method",
        "creation_date",
        "license_reuse_note",
        "prohibited_content_review",
    ]
    _require_exact_fields(provenance, provenance_fields, "source provenance")
    if provenance["synthetic_independently_written"] is not True:
        raise ValidationError("Case sources must be independently written")
    if provenance["reuse_status"] != "project-authored-synthetic":
        raise ValidationError("MVP case reuse_status is not permitted")
    for field in [
        "reuse_status",
        "authoring_method",
        "creation_date",
        "license_reuse_note",
    ]:
        _require_nonempty_string(provenance[field], f"provenance {field}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", provenance["creation_date"]):
        raise ValidationError("Provenance creation_date must use YYYY-MM-DD")
    review_fields = [
        "copied_source_passages",
        "private_zotero_content",
        "copyrighted_pdf_content",
        "purchased_data",
        "unpublished_research",
        "personal_data",
    ]
    review = provenance["prohibited_content_review"]
    _require_exact_fields(review, review_fields, "prohibited-content review")
    if any(value is not False for value in review.values()):
        raise ValidationError("Case declares prohibited source content")
    _unique_ids(case_bundle["sources"], "source_id", "source")
    _unique_ids(case_bundle["claims"], "claim_id", "claim")
    for source in case_bundle["sources"]:
        _require_exact_fields(
            source,
            ["source_id", "text", "locator", "limitations"],
            "source",
        )
        _validate_id(source["source_id"], "source_id")
        _require_nonempty_string(source["text"], "source text")
        _require_string_list(source["limitations"], "source limitations")
        if (
            not isinstance(source["locator"], str)
            or not SYNTHETIC_LOCATOR_PATTERN.fullmatch(source["locator"])
        ):
            raise ValidationError("Source locator must be public-safe synthetic")
    for claim in case_bundle["claims"]:
        _require_exact_fields(
            claim,
            ["claim_id", "fixture_id", "text"],
            "claim",
            optional=["claim_type"],
        )
        _validate_id(claim["claim_id"], "claim_id")
        _validate_id(claim["fixture_id"], "fixture_id")
        _require_nonempty_string(claim["text"], "claim text")
        if "claim_type" in claim:
            _require_nonempty_string(claim["claim_type"], "claim_type")
    return case_bundle


def validate_analysis_proposal(analysis_proposal, case_bundle):
    _scan_sensitive_values(analysis_proposal, "analysis proposal")
    _require_exact_fields(
        analysis_proposal,
        ["schema_version", "case_id", "proposals"],
        "analysis proposal",
    )
    if analysis_proposal["schema_version"] != SCHEMA_VERSION:
        raise ValidationError("Unsupported proposal schema_version")
    if analysis_proposal["case_id"] != case_bundle["case_id"]:
        raise ValidationError("Proposal case_id does not match case bundle")
    _require_list(
        analysis_proposal["proposals"], "proposals", allow_empty=False
    )
    _unique_ids(analysis_proposal["proposals"], "claim_id", "proposal")
    claim_ids = {claim["claim_id"] for claim in case_bundle["claims"]}
    source_ids = {source["source_id"] for source in case_bundle["sources"]}
    proposal_ids = {
        proposal["claim_id"] for proposal in analysis_proposal["proposals"]
    }
    if proposal_ids != claim_ids:
        raise ValidationError("Proposal must contain exactly one item per claim")
    for proposal in analysis_proposal["proposals"]:
        _require_exact_fields(
            proposal,
            [
                "claim_id",
                "cited_source_ids",
                "evidence_status",
                "material_components",
                "missing_or_altered_qualifiers",
                "fact_flags",
                "rationale_candidate",
                "unresolved_questions",
            ],
            "proposal item",
            optional=["suggested_final_verdict"],
        )
        if proposal["evidence_status"] not in {
            "full_support",
            "mixed_support",
            "no_support",
            "conflicting",
            "insufficient_context",
        }:
            raise ValidationError("Invalid proposal evidence_status")
        _require_list(
            proposal["cited_source_ids"], "cited_source_ids"
        )
        if len(proposal["cited_source_ids"]) != len(
            set(proposal["cited_source_ids"])
        ):
            raise ValidationError("cited_source_ids must be unique")
        for source_id in proposal["cited_source_ids"]:
            _validate_id(source_id, "cited source_id")
        _require_string_list(
            proposal["missing_or_altered_qualifiers"],
            "missing_or_altered_qualifiers",
        )
        _require_nonempty_string(
            proposal["rationale_candidate"], "rationale_candidate"
        )
        _require_string_list(
            proposal["unresolved_questions"], "unresolved_questions"
        )
        if (
            "suggested_final_verdict" in proposal
            and proposal["suggested_final_verdict"] not in VERDICTS
        ):
            raise ValidationError("Invalid suggested_final_verdict")
        components = proposal["material_components"]
        if not isinstance(components, list) or not components:
            raise ValidationError("Proposal requires material components")
        for component in components:
            _require_exact_fields(
                component,
                ["component_id", "text", "support_status"],
                "material component",
            )
            _validate_id(component["component_id"], "component_id")
            _require_nonempty_string(component["text"], "component text")
            if component["support_status"] not in {
                "supported",
                "unsupported",
                "unknown",
            }:
                raise ValidationError("Invalid component support_status")
        flag_fields = [
            "causal_overreach",
            "scope_generalization",
            "certainty_magnitude_overreach",
            "contradiction_or_no_support",
            "separable_partial_support",
            "ambiguity_or_conflict",
            "missing_required_context",
            "all_material_components_supported",
            "all_material_qualifiers_supported",
        ]
        _require_exact_fields(
            proposal["fact_flags"], flag_fields, "proposal fact_flags"
        )
        if any(
            not isinstance(value, bool)
            for value in proposal["fact_flags"].values()
        ):
            raise ValidationError("Proposal fact flags must be boolean")
        unknown_sources = set(proposal["cited_source_ids"]) - source_ids
        if unknown_sources:
            raise ValidationError(
                "Proposal cites unknown source IDs: "
                + ", ".join(sorted(unknown_sources))
            )
    return analysis_proposal


def validate_audit_result(audit_result):
    _scan_sensitive_values(audit_result, "audit result")
    _require_exact_fields(
        audit_result,
        [
            "schema_version",
            "tool_version",
            "case_id",
            "deterministic_policy_version",
            "execution",
            "provenance_summary",
            "claims",
        ],
        "audit result",
    )
    if audit_result["schema_version"] != SCHEMA_VERSION:
        raise ValidationError("Unsupported audit schema_version")
    _validate_id(audit_result["case_id"], "audit case_id")
    _require_nonempty_string(audit_result["tool_version"], "tool_version")
    if (
        audit_result["deterministic_policy_version"]
        != "scholartrace-policy-0.1.0"
    ):
        raise ValidationError("Unsupported deterministic policy version")
    _require_exact_fields(
        audit_result["execution"],
        ["read_only_inputs", "no_overwrite"],
        "audit execution",
    )
    if audit_result["execution"] != {
        "read_only_inputs": True,
        "no_overwrite": True,
    }:
        raise ValidationError("Audit result must preserve read-only/no-overwrite")
    _require_exact_fields(
        audit_result["provenance_summary"],
        ["synthetic_independently_written"],
        "audit provenance summary",
    )
    if (
        audit_result["provenance_summary"]["synthetic_independently_written"]
        is not True
    ):
        raise ValidationError("Audit provenance must remain synthetic")
    if not audit_result["claims"]:
        raise ValidationError("Audit result requires claims")
    _unique_ids(audit_result["claims"], "claim_id", "audit claim")
    claim_fields = [
        "claim_id",
        "fixture_id",
        "claim_text",
        "verdict",
        "cited_sources",
        "rationale",
        "missing_or_altered_qualifiers",
        "deterministic_rule_flags",
        "policy_trace",
        "unresolved_questions",
        "human_review_reason",
        "human_verified",
    ]
    for claim in audit_result["claims"]:
        _require_exact_fields(claim, claim_fields, "audit claim")
        _validate_id(claim["claim_id"], "audit claim_id")
        _validate_id(claim["fixture_id"], "audit fixture_id")
        _require_nonempty_string(claim["claim_text"], "audit claim text")
        _require_nonempty_string(claim["rationale"], "audit rationale")
        _require_nonempty_string(
            claim["human_review_reason"], "human_review_reason"
        )
        if claim["verdict"] not in VERDICTS:
            raise ValidationError("Invalid audit verdict")
        if claim["human_verified"] is not False:
            raise ValidationError("Machine audit cannot be human verified")
        if not claim["policy_trace"]:
            raise ValidationError("Audit claim requires a policy trace")
        _require_list(claim["cited_sources"], "audit cited_sources")
        _require_string_list(
            claim["missing_or_altered_qualifiers"],
            "audit missing_or_altered_qualifiers",
        )
        _require_string_list(
            claim["deterministic_rule_flags"],
            "audit deterministic_rule_flags",
        )
        _require_string_list(
            claim["policy_trace"], "audit policy_trace", allow_empty=False
        )
        _require_string_list(
            claim["unresolved_questions"], "audit unresolved_questions"
        )
        for cited in claim["cited_sources"]:
            _require_exact_fields(
                cited, ["source_id", "locator"], "audit cited source"
            )
            _validate_id(cited["source_id"], "audit source_id")
            if (
                not isinstance(cited["locator"], str)
                or not SYNTHETIC_LOCATOR_PATTERN.fullmatch(cited["locator"])
            ):
                raise ValidationError(
                    "Audit source locator must be public-safe synthetic"
                )
    return audit_result
