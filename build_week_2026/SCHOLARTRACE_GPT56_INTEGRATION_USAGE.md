# ScholarTrace GPT-5.6 Integration Usage

## Boundary

The optional GPT-5.6 path generates a non-authoritative semantic proposal from
the frozen synthetic case. The existing deterministic policy remains the only
authority for final verdicts.

The live path:

- uses the official OpenAI Python SDK and Responses API;
- defaults to `gpt-5.6-sol`;
- sets `store=False` and `background=False`;
- uses reasoning effort `medium`;
- supplies a strict JSON Schema response format;
- provides no tools and performs no browsing, retrieval, upload, or fallback;
- disables SDK automatic retries; and
- accepts only the frozen synthetic case in this gate.

## Optional dependency

Deterministic offline use has no OpenAI dependency. Install the bounded live
extra only when live evaluation is authorized:

```text
python -m pip install -e ".[openai]"
```

The declared compatible range is `openai>=2.43.0,<3`.

## Credential

The only supported credential source is the current process environment
variable `OPENAI_API_KEY`. Configure it through the operating system or an
approved secret-management workflow before launching the process.

Do not place a key in a command example, repository file, `.env` file, shell
history, test, report, or chat. The CLI checks only whether the variable is
present and non-empty.

API billing and quota are separate from a ChatGPT subscription.

## Dry run

This command validates the case and request contract, prints sanitized request
configuration and intended filenames, calls no API, and writes nothing:

```text
python -m scholartrace propose \
  --case examples/scholartrace/education_claim_audit_case.json \
  --schema schemas/scholartrace_analysis_proposal.schema.json \
  --gold examples/scholartrace/education_claim_audit_gold.json \
  --dry-run \
  --out-dir <new_output_directory>
```

The default model is `gpt-5.6-sol`. Other model families are rejected.

## Authorized live run

Use a new output directory. The attempt number must reflect the bounded gate
attempt, from 1 through 3:

```text
python -m scholartrace propose \
  --case examples/scholartrace/education_claim_audit_case.json \
  --schema schemas/scholartrace_analysis_proposal.schema.json \
  --gold examples/scholartrace/education_claim_audit_gold.json \
  --model gpt-5.6-sol \
  --reasoning-effort medium \
  --max-output-tokens 8000 \
  --attempt 1 \
  --live \
  --write \
  --out-dir <new_output_directory>
```

Exactly five files are written:

- `gpt56_analysis_proposal.json`
- `gpt56_claim_evidence_map.json`
- `gpt56_audit_report.md`
- `gpt56_run_metadata.json`
- `gpt56_evaluation_summary.md`

The output directory is checked before the API request. Existing directories
are refused, so an output collision does not consume a model request.
There is no overwrite option.

## Offline replay

The accepted human-authored proposal remains available for deterministic,
secret-free replay:

```text
python -m scholartrace audit \
  --case examples/scholartrace/education_claim_audit_case.json \
  --proposal examples/scholartrace/education_claim_audit_proposal.json
```

Run all offline tests with:

```text
python -m unittest discover -s tests -v
```

Verify frozen fixture provenance with:

```text
python -m scholartrace verify-fixtures \
  --fixture-dir examples/scholartrace
```

## Exit codes

- `0`: successful dry-run or successful bounded live evaluation
- `2`: validation or model-family rejection
- `3`: optional official SDK unavailable
- `4`: `OPENAI_API_KEY` absent or empty
- `5`: sanitized model/API or provider failure
- `6`: malformed or schema-invalid model response
- `7`: deterministic evaluation failed closed
- `8`: output collision or prohibited output destination

There is no automatic model fallback and no automatic retry loop.

## Privacy and authority

Only the approved synthetic case is sent. Gold labels, repository source,
legal files, private paths, Zotero, Obsidian, PDFs, private research, and
external articles are not sent.

`store=False` requests no stored response for this call, but API processing and
retention remain governed by the applicable OpenAI API data controls and
account policy. Review the current official policy before using any new data.

Model output cannot grant E3, citation eligibility, grading authority,
publication readiness, or human verification. Every generated proposal must
pass strict local validation and the deterministic policy. Human review
remains required.
