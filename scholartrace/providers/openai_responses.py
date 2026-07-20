"""Bounded official OpenAI Responses API adapter."""

import hashlib
import importlib.metadata
import json
import os
import time

from ..prompt import (
    PROMPT_VERSION,
    build_case_input,
    build_prompt,
    strict_proposal_schema,
)
from ..render import render_json
from ..validation import ValidationError, validate_analysis_proposal

DEFAULT_MODEL = "gpt-5.6-sol"
ALLOWED_MODELS = {
    "gpt-5.6",
    "gpt-5.6-sol",
    "gpt-5.6-terra",
    "gpt-5.6-luna",
}
DEFAULT_REASONING_EFFORT = "medium"
DEFAULT_MAX_OUTPUT_TOKENS = 8000
AUTHORIZED_LIVE_ATTEMPTS = 3


class ProviderError(RuntimeError):
    """Base class for sanitized provider failures."""


class MissingSDKError(ProviderError):
    """The optional official SDK is unavailable."""


class MissingCredentialError(ProviderError):
    """The authorized process credential is unavailable."""


class UnsupportedModelError(ProviderError):
    """The requested model is outside the frozen GPT-5.6 family."""


class ModelAPIError(ProviderError):
    """The bounded Responses API request failed."""


class ModelResponseError(ProviderError):
    """The model response failed strict local validation."""


def _sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest().upper()


def _load_sdk():
    from openai import OpenAI

    return OpenAI


def _sdk_version():
    try:
        return importlib.metadata.version("openai")
    except importlib.metadata.PackageNotFoundError as exc:
        raise MissingSDKError("Official OpenAI SDK is not installed") from exc


def credential_available():
    """Check only whether the one authorized environment variable is nonempty."""
    return bool(os.environ.get("OPENAI_API_KEY"))


def create_official_client():
    """Create an official client with SDK retries disabled."""
    if not credential_available():
        raise MissingCredentialError(
            "OPENAI_API_KEY is not present and non-empty"
        )
    try:
        client_class = _load_sdk()
    except (ImportError, ModuleNotFoundError) as exc:
        raise MissingSDKError("Official OpenAI SDK is not installed") from exc
    return client_class(max_retries=0, timeout=180.0)


def validate_model(model):
    if model not in ALLOWED_MODELS:
        raise UnsupportedModelError("Only the GPT-5.6 family is allowed")
    return model


def _returned_model_is_allowed(model):
    return isinstance(model, str) and (
        model in ALLOWED_MODELS or model.startswith("gpt-5.6-")
    )


def _usage_value(usage, name):
    value = getattr(usage, name, None) if usage is not None else None
    return value if isinstance(value, int) and value >= 0 else None


def describe_request(
    case_bundle,
    proposal_schema,
    *,
    model=DEFAULT_MODEL,
    reasoning_effort=DEFAULT_REASONING_EFFORT,
    max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS,
):
    """Return request metadata without importing the SDK or calling the API."""
    validate_model(model)
    case_input = build_case_input(case_bundle)
    prompt = build_prompt(case_bundle)
    strict_schema = strict_proposal_schema(proposal_schema)
    return {
        "model_requested": model,
        "prompt_version": PROMPT_VERSION,
        "input_sha256": _sha256_text(case_input),
        "prompt_sha256": _sha256_text(prompt),
        "strict_schema_sha256": _sha256_text(
            json.dumps(
                strict_schema,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        ),
        "request_configuration": {
            "api": "responses",
            "store": False,
            "background": False,
            "no_tools": True,
            "reasoning_effort": reasoning_effort,
            "max_output_tokens": max_output_tokens,
            "structured_output": "strict_json_schema",
            "automatic_retries": 0,
            "multi_turn": False,
            "file_uploads": False,
        },
    }


def generate_proposal(
    case_bundle,
    proposal_schema,
    *,
    model=DEFAULT_MODEL,
    reasoning_effort=DEFAULT_REASONING_EFFORT,
    max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS,
    attempt_number,
    client=None,
    sdk_version=None,
):
    """Make exactly one bounded request and return a validated proposal."""
    validate_model(model)
    if attempt_number not in range(1, AUTHORIZED_LIVE_ATTEMPTS + 1):
        raise ProviderError("Live attempt number must be between 1 and 3")

    description = describe_request(
        case_bundle,
        proposal_schema,
        model=model,
        reasoning_effort=reasoning_effort,
        max_output_tokens=max_output_tokens,
    )
    prompt = build_prompt(case_bundle)
    case_input = build_case_input(case_bundle)
    strict_schema = strict_proposal_schema(proposal_schema)
    if client is None:
        client = create_official_client()
    if sdk_version is None:
        sdk_version = _sdk_version()

    started = time.perf_counter()
    try:
        response = client.responses.create(
            model=model,
            instructions=prompt,
            input=case_input,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "scholartrace_analysis_proposal",
                    "strict": True,
                    "schema": strict_schema,
                }
            },
            reasoning={"effort": reasoning_effort},
            max_output_tokens=max_output_tokens,
            store=False,
            background=False,
        )
    except Exception as exc:
        status_code = getattr(exc, "status_code", None)
        label = type(exc).__name__
        detail = f"{label}"
        if isinstance(status_code, int):
            detail += f" (HTTP {status_code})"
        raise ModelAPIError(f"Responses API request failed: {detail}") from exc
    latency_ms = round((time.perf_counter() - started) * 1000, 3)

    returned_model = getattr(response, "model", None)
    if not _returned_model_is_allowed(returned_model):
        raise ModelResponseError("Returned model is outside GPT-5.6")
    output_text = getattr(response, "output_text", None)
    if not isinstance(output_text, str) or not output_text.strip():
        raise ModelResponseError("Response did not contain structured text")
    try:
        proposal = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise ModelResponseError("Response was not valid JSON") from exc
    try:
        validate_analysis_proposal(proposal, case_bundle)
    except ValidationError as exc:
        raise ModelResponseError(
            "Response violated the proposal contract"
        ) from exc

    usage = getattr(response, "usage", None)
    metadata = {
        **description,
        "model_returned": returned_model,
        "sdk_version": sdk_version,
        "attempt_number": attempt_number,
        "authorized_live_attempts": AUTHORIZED_LIVE_ATTEMPTS,
        "latency_ms": latency_ms,
        "created_at": getattr(response, "created_at", None),
        "response_id_retained": False,
        "usage": {
            "input_tokens": _usage_value(usage, "input_tokens"),
            "output_tokens": _usage_value(usage, "output_tokens"),
            "total_tokens": _usage_value(usage, "total_tokens"),
        },
        "raw_output_sha256": _sha256_text(output_text),
        "proposal_sha256": _sha256_text(render_json(proposal)),
        "schema_validation": True,
        "invented_identifier_check": True,
    }
    return proposal, metadata
