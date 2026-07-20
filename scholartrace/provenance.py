"""Fixture provenance and frozen-hash verification."""

import hashlib
from pathlib import Path

from .validation import ValidationError, load_json

FIXTURE_FILES = (
    "education_claim_audit_case.json",
    "education_claim_audit_proposal.json",
    "education_claim_audit_gold.json",
)


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def verify_fixture_manifest(fixture_dir):
    fixture_dir = Path(fixture_dir)
    manifest = load_json(fixture_dir / "fixture_provenance_manifest.json")
    required = {
        "fixture_set_id",
        "version",
        "creation_date",
        "synthetic_independently_written",
        "authoring_method",
        "no_copied_source_passage",
        "prohibited_content_checklist",
        "files",
    }
    missing = sorted(required - set(manifest))
    if missing:
        raise ValidationError(
            "Fixture manifest missing fields: " + ", ".join(missing)
        )
    if manifest["synthetic_independently_written"] is not True:
        raise ValidationError("Fixture set must be independently written")
    if manifest["no_copied_source_passage"] is not True:
        raise ValidationError("Fixture set must declare no copied passages")
    checklist = manifest["prohibited_content_checklist"]
    if not isinstance(checklist, dict) or not checklist:
        raise ValidationError("Fixture prohibited-content checklist is required")
    if any(value is not False for value in checklist.values()):
        raise ValidationError("Fixture manifest declares prohibited content")
    if set(manifest["files"]) != set(FIXTURE_FILES):
        raise ValidationError("Fixture manifest file set is not exact")

    hashes = {}
    for filename in FIXTURE_FILES:
        expected = manifest["files"][filename]["sha256"].upper()
        actual = sha256_file(fixture_dir / filename)
        if actual != expected:
            raise ValidationError(f"Fixture hash mismatch: {filename}")
        hashes[filename] = actual

    gold = load_json(fixture_dir / "education_claim_audit_gold.json")
    if gold.get("human_verified") is not False:
        raise ValidationError("Gold record must remain human_verified: false")
    if gold.get("review_status") != "unreviewed":
        raise ValidationError("Gold record must remain unreviewed")
    return {
        "valid": True,
        "fixture_set_id": manifest["fixture_set_id"],
        "version": manifest["version"],
        "hashes": hashes,
    }
