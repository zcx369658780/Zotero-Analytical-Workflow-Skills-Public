# ScholarTrace Synthetic Education Fixtures

This directory contains one independently written, fully synthetic teaching
bundle for the ScholarTrace deterministic Evidence Gate. It does not reproduce
or adapt a real paper, course assessment, textbook passage, online article,
private research record, Zotero item, Obsidian note, PDF, or purchased dataset.

## Fixture coverage

The bundle provides seven stable fixtures:

- `fixture_supported`
- `fixture_partially_supported`
- `fixture_unsupported_conclusion`
- `fixture_correlation_as_causation`
- `fixture_omitted_limitations`
- `fixture_unverifiable_missing_context`
- `fixture_conflicting_evidence`

Together they cover all five frozen verdicts:

- `supported`
- `partially_supported`
- `unsupported`
- `overstated`
- `unverifiable`

## Files

- `education_claim_audit_case.json`: synthetic excerpts and audited claims
- `education_claim_audit_proposal.json`: human-authored, non-authoritative
  semantic proposal
- `education_claim_audit_gold.json`: unreviewed gold expectations with
  `human_verified: false`
- `fixture_provenance_manifest.json`: source declarations and frozen SHA256
  values

The proposal cannot control final verdicts. The deterministic policy applies
the frozen fail-closed priority and ignores a conflicting suggested verdict.

## Verify frozen content

From the repository root:

```text
python -m scholartrace verify-fixtures --fixture-dir examples/scholartrace
```

The command exits nonzero if a declaration is unsafe, a required file is
missing, or any frozen content hash differs.

## Safety boundary

These fixtures are for low-stakes educational demonstration only. Machine
outputs remain `human_verified: false`, cannot promote evidence to E3, and
cannot grant citation eligibility, grading authority, or publication
readiness.
