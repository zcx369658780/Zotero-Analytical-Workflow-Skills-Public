# ScholarTrace Deterministic Pipeline Usage

## Requirements

- Python 3.11 or later
- repository-local files only
- no model, API key, account, network retrieval, Zotero, Obsidian, or PDF
  access

The package has no runtime dependencies outside the Python standard library.

## Optional local installation

```text
python -m pip install --no-deps --no-build-isolation .
```

The repository commands below also work directly with `python -m scholartrace`
from the repository root.

## Validate inputs and fixture provenance

```text
python -m scholartrace validate \
  --case examples/scholartrace/education_claim_audit_case.json \
  --proposal examples/scholartrace/education_claim_audit_proposal.json
```

Expected behavior:

- validates the strict case and proposal contracts;
- verifies the fixture manifest declarations and SHA256 values;
- runs the deterministic audit validation path;
- prints a small JSON success record; and
- writes no files.

## Verify frozen fixture hashes

```text
python -m scholartrace verify-fixtures \
  --fixture-dir examples/scholartrace
```

Expected behavior: prints the fixture-set identifier, version, and the three
verified file hashes. Missing, changed, or prohibited content fails with a
nonzero exit.

## Audit dry-run

```text
python -m scholartrace audit \
  --case examples/scholartrace/education_claim_audit_case.json \
  --proposal examples/scholartrace/education_claim_audit_proposal.json
```

This is the default mode. It prints deterministic JSON to stdout and creates no
file or directory. Repeated identical runs produce byte-stable JSON and stable
claim ordering.

## Explicit write

Choose a new output directory that does not exist:

```text
python -m scholartrace audit \
  --case examples/scholartrace/education_claim_audit_case.json \
  --proposal examples/scholartrace/education_claim_audit_proposal.json \
  --write \
  --out-dir <new_output_directory>
```

Exactly two files are created:

- `<new_output_directory>/claim_evidence_map.json`
- `<new_output_directory>/audit_report.md`

`--write` requires `--out-dir`. The target directory must be new. A second
attempt with the same path exits nonzero before modifying anything. There is no
`--overwrite` option.

No input path is copied into either output. The CLI never infers a Zotero or
Obsidian destination and must not be pointed at a real vault or research-data
location.

## Run tests

```text
python -m unittest discover -s tests -v
```

The tests cover schema/runtime contracts, all seven fixture verdicts, all five
labels, policy priority, proposal authority rejection, provenance tampering,
privacy and credential rejection, deterministic output, dry-run, explicit
write, Markdown safety notices, and byte-preserving no-overwrite refusal.

## Output authority

Every result includes:

- tool version `0.1.0`;
- schema version `1.0.0`;
- deterministic policy version `scholartrace-policy-0.1.0`;
- source IDs and only supplied synthetic locators;
- triggered deterministic rules and policy trace; and
- `human_verified: false`.

Outputs cannot grant E3, citation eligibility, grading authority, or
publication readiness. Human review remains separate and mandatory before any
academic use.

## Current limitations

- only the frozen synthetic JSON contract is supported;
- no PDF parsing, source retrieval, model invocation, or real research data;
- no automatic evidence discovery or missing-context repair;
- no human-review writeback;
- no overwrite or update-in-place workflow;
- no direct writing to Zotero or Obsidian; and
- no deployment, hosted interface, submission integration, or public demo
  claim.
