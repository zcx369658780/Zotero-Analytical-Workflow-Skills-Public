"""Deterministic ScholarTrace output rendering."""

import json
from collections import Counter


def render_json(audit_result):
    return json.dumps(
        audit_result,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def _list_or_none(values):
    return ", ".join(values) if values else "none"


def render_markdown(audit_result):
    counts = Counter(item["verdict"] for item in audit_result["claims"])
    verdict_order = [
        "supported",
        "partially_supported",
        "unsupported",
        "overstated",
        "unverifiable",
    ]
    lines = [
        "# ScholarTrace Audit Report",
        "",
        f"- Case: `{audit_result['case_id']}`",
        (
            "- Deterministic policy: "
            f"`{audit_result['deterministic_policy_version']}`"
        ),
        "- Provenance: independently written synthetic demonstration content",
        "- Input mode: read-only",
        "- Output policy: no-overwrite",
        "",
        "## Verdict counts",
        "",
    ]
    lines.extend(
        f"- `{verdict}`: {counts.get(verdict, 0)}"
        for verdict in verdict_order
    )
    for claim in audit_result["claims"]:
        cited = [
            f"`{item['source_id']}` ({item['locator']})"
            for item in claim["cited_sources"]
        ]
        lines.extend(
            [
                "",
                f"## {claim['fixture_id']}",
                "",
                f"- Claim ID: `{claim['claim_id']}`",
                f"- Claim: {claim['claim_text']}",
                f"- Verdict: `{claim['verdict']}`",
                (
                    "- Triggered rules: "
                    + _list_or_none(claim["deterministic_rule_flags"])
                ),
                "- Policy trace: " + _list_or_none(claim["policy_trace"]),
                "- Sources: " + _list_or_none(cited),
                (
                    "- Missing or altered qualifiers: "
                    + _list_or_none(
                        claim["missing_or_altered_qualifiers"]
                    )
                ),
                f"- Rationale: {claim['rationale']}",
                (
                    "- Unresolved questions: "
                    + _list_or_none(claim["unresolved_questions"])
                ),
                (
                    "- Human review: "
                    f"{claim['human_review_reason']}"
                ),
                "- `human_verified: false`",
            ]
        )
    lines.extend(
        [
            "",
            "## Safety notice",
            "",
            "These machine-generated results remain `human_verified: false` "
            "and cannot grant E3, citation eligibility, grading authority, "
            "or publication readiness.",
            "",
        ]
    )
    return "\n".join(lines)
