"""Versioned prompt contract for bounded GPT-5.6 semantic proposals."""

import copy
import json

from .validation import validate_case_bundle

PROMPT_VERSION = "scholartrace-gpt56-prompt-0.1.0"


def strict_proposal_schema(schema):
    """Return the accepted proposal schema as a strict model-output subset."""
    strict = copy.deepcopy(schema)
    strict.pop("$schema", None)
    strict.pop("$id", None)
    proposal = strict["$defs"]["proposal"]
    proposal["properties"].pop("suggested_final_verdict", None)
    strict["$defs"].pop("verdict", None)

    def require_all_properties(value):
        if isinstance(value, dict):
            if value.get("type") == "object" and "properties" in value:
                value["additionalProperties"] = False
                value["required"] = list(value["properties"])
            for child in value.values():
                require_all_properties(child)
        elif isinstance(value, list):
            for child in value:
                require_all_properties(child)

    require_all_properties(strict)
    return strict


def build_prompt(case_bundle):
    """Build the public instructions sent alongside one validated case."""
    validate_case_bundle(case_bundle)
    claim_ids = ", ".join(claim["claim_id"] for claim in case_bundle["claims"])
    source_ids = ", ".join(
        source["source_id"] for source in case_bundle["sources"]
    )
    return f"""ScholarTrace prompt version: {PROMPT_VERSION}

You are a bounded semantic proposal generator. You are not the final
adjudicator. A separate deterministic policy derives every final verdict.

Use only the supplied synthetic case bundle. Use no external knowledge,
browsing, retrieval, assumptions, or invented evidence. Analyze every supplied
claim_id exactly once and cite only supplied source_id values.

Allowed claim IDs: {claim_ids}
Allowed source IDs: {source_ids}

For each claim:
- split the claim into concise material components;
- map every component to the relevant supplied excerpts;
- distinguish correlation from causation;
- detect omitted or altered sample, period, geography, population, method,
  outcome, certainty, magnitude, generalization, and scope qualifiers;
- mark unsupported conclusions and contradictions explicitly;
- use ambiguity_or_conflict for unresolved supplied conflicts;
- use missing_required_context when required evidence context is absent;
- use separable_partial_support only for a supported component plus a distinct
  unsupported or incomplete component;
- set all_material_components_supported and
  all_material_qualifiers_supported only when coverage is complete;
- state uncertainty instead of guessing;
- provide a concise rationale candidate and unresolved questions.

The fact flags describe evidence conditions; they do not grant a final verdict.
Do not claim human_verified status, E3 promotion, citation eligibility,
grading authority, publication readiness, or any other academic authority.
Return only strict JSON conforming to the supplied schema.
"""


def build_case_input(case_bundle):
    """Serialize only the approved synthetic case as deterministic input."""
    validate_case_bundle(case_bundle)
    return json.dumps(
        case_bundle,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
