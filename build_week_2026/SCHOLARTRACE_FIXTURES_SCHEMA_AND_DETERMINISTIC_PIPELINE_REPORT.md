# ScholarTrace Fixtures, Schema, and Deterministic Pipeline Report

Date: 2026-07-20
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`
Branch: `build-week-2026-scholartrace`

## Git and provenance baseline

- Accepted scope-freeze commit:
  `341b30951cac04903960e6f8a6c3cd6fd58bda75`
- Task-bearing start HEAD:
  `8d9f6fb58818abb7fa52a88c14b772f96f0d1e56`
- Accepted permission/licensing baseline on `origin/main`:
  `6c1c6caa93318f08cff666d94de26da42447ef59`
- Protected tag target:
  `e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`
- The task-bearing commit directly follows the accepted scope freeze and adds
  only the governing task file.

## Architecture and file inventory

The independently authored implementation contains:

- `scholartrace/`: seven standard-library modules for CLI, validation,
  provenance, policy, and deterministic rendering;
- `schemas/`: three normative JSON Schema Draft 2020-12 contracts;
- `examples/scholartrace/`: seven-claim synthetic education bundle, proposal,
  gold record, manifest, and public explanation;
- `tests/test_scholartrace_pipeline.py`: focused integration-style unittest
  coverage;
- `pyproject.toml`: Python 3.11 package metadata and console entry point;
- `.github/workflows/scholartrace-tests.yml`: local-package CI checks;
- a deterministic-pipeline usage document; and
- this implementation report plus the bounded competition-period update.

No external runtime dependency, network/model client, account configuration,
or secret integration was added.

## Synthetic fixture provenance

Fixture set: `scholartrace_education_claim_audit_v1`

- creation date: 2026-07-20;
- independently written for this repository: yes;
- source and claim text: human-authored from scratch for a fictional,
  low-stakes education scenario;
- copied source passage: none;
- private Zotero, PDF, purchased data, Xiaohongshu, unpublished research,
  personal data, or external teaching content: none;
- gold status: `review_status: unreviewed`;
- gold authority: `human_verified: false`.

Frozen content hashes:

| File | SHA256 |
|---|---|
| `education_claim_audit_case.json` | `653FEA5B5B507B8258C620B9AFFE0D125AA9CC3D1884F69D97B7A119EDD55B1C` |
| `education_claim_audit_proposal.json` | `EEB53DE25B204820AD67B4D61F4E07BF4219A08A10E663222DF22D41376CE0B0` |
| `education_claim_audit_gold.json` | `12569B669B6FC2D5597EE0269DCDDD1BF720152B950E3D8034BFD399F15142B0` |
| `fixture_provenance_manifest.json` | `2A4BD60DCD54BD805BCD02A853B46088F4361CCF1104A9E95E54E5A3FD278176` |

Revalidation command:

```text
python -m scholartrace verify-fixtures --fixture-dir examples/scholartrace
```

## Contract and policy versions

- package/tool version: `0.1.0`;
- case schema version: `1.0.0`;
- analysis proposal schema version: `1.0.0`;
- audit result schema version: `1.0.0`;
- JSON Schema dialect: Draft 2020-12;
- deterministic policy: `scholartrace-policy-0.1.0`.

The policy priority is:

1. missing context, ambiguity, or conflict -> `unverifiable`;
2. no support or contradiction -> `unsupported`;
3. causal, scope, certainty, magnitude, or generalization overreach ->
   `overstated`;
4. separable mixed support without a stronger condition ->
   `partially_supported`;
5. complete component and qualifier coverage only -> `supported`;
6. unclassified input -> fail closed as `unverifiable` or validation error.

Suggested proposal verdicts cannot override policy. Proposal or output attempts
to grant E3, citation approval, or human verification are rejected.

## Commands and exit codes

| Command or check | Exit | Result |
|---|---:|---|
| `git fetch origin --tags` | 0 | Repository refs fetched |
| `git merge --ff-only origin/build-week-2026-scholartrace` | 0 | Fast-forwarded to task-bearing HEAD |
| Individual TDD RED tests | 1 | Expected failures before each behavior existed |
| `python -m unittest discover -s tests -v` | 0 | 13 tests passed |
| `python -m scholartrace verify-fixtures --fixture-dir examples/scholartrace` | 0 | Manifest declarations and three frozen hashes valid |
| `python -m scholartrace validate --case ... --proposal ...` | 0 | Case, proposal, provenance, and audit path valid |
| `python -m scholartrace audit --case ... --proposal ...` | 0 | Read-only stdout audit; seven claims |
| `python -m scholartrace audit ... --write --out-dir <new>` | 0 | Exactly two output files created |
| Repeat explicit-write command with same output directory | 2 | Safe no-overwrite refusal |
| Standard-library AST parse of package and tests | 0 | Eight Python files parsed |
| GitHub Actions workflow static requirement check | 0 | Required local checks present; no model/deploy integration |
| `git diff --check` | 0 | No whitespace errors |

## Unittest result

`13/13 PASS` in approximately 0.53 seconds:

- `test_supported_requires_full_component_and_qualifier_coverage`
- `test_policy_applies_frozen_fail_closed_priority`
- `test_unknown_source_reference_fails_closed`
- `test_frozen_fixture_set_matches_all_gold_verdicts`
- `test_fixture_manifest_detects_content_tampering`
- `test_normative_schemas_are_draft_2020_12_and_runtime_is_strict`
- `test_runtime_rejects_wrong_contract_value_types`
- `test_proposal_cannot_override_policy_or_grant_human_authority`
- `test_private_paths_credentials_contacts_and_prohibited_sources_reject`
- `test_packaging_declares_local_standard_library_cli`
- `test_audit_defaults_to_read_only_byte_stable_stdout`
- `test_explicit_write_creates_two_files_and_never_overwrites`
- `test_validate_and_verify_fixtures_are_read_only`

The seven fixtures matched all gold verdicts. Label distribution was:
`supported=1`, `partially_supported=1`, `unsupported=1`, `overstated=2`,
and `unverifiable=2`.

## CLI smoke results

Default audit:

- exit 0;
- seven claims in stable case order;
- deterministic stdout JSON;
- no output directory or file created.

Explicit write in a new task-specific system temporary directory:

- exit 0;
- created exactly `claim_evidence_map.json` and `audit_report.md`;
- JSON SHA256:
  `6C715FFE57F2D763993D548D2F2D79AB8FA129DFF61F8E82D65851C387A07541`;
- Markdown SHA256:
  `6CF1916CC6943BA4A9E3D810584FBFECE6CB3D5B12170A2B5BC3068B60FBE278`.

Second write:

- exit 2;
- refusal reason: output directory already exists;
- both before/after hashes were identical;
- no `--overwrite` option exists.

## GitHub Actions workflow

The workflow:

- runs on ScholarTrace-scoped pushes and path-scoped pull requests;
- uses Python 3.11;
- installs only the local package without runtime dependencies;
- verifies frozen fixtures;
- runs the full unittest suite;
- runs the read-only CLI smoke test;
- requests only `contents: read`; and
- contains no model/API, secret, deployment, release, or submission step.

Local workflow structure check passed. Remote workflow status is recorded in
the final gate output after the implementation commit is pushed.

## Privacy, copyright, and secret checks

Runtime and tests reject:

- Windows and POSIX private absolute paths;
- Zotero, Obsidian, file, and PDF locators;
- credential-like values and personal email addresses;
- prohibited source declarations;
- unknown source IDs;
- E3, citation approval, or human-verification authority; and
- overwrite attempts.

Repository scans found no actual credential, private contact detail, private
path, copied source passage, external evidence, or prohibited fixture content.
The synthetic forbidden-value test strings are assembled only at runtime.

## Exact intended staged paths

- `.github/workflows/scholartrace-tests.yml`
- `pyproject.toml`
- `scholartrace/__init__.py`
- `scholartrace/__main__.py`
- `scholartrace/cli.py`
- `scholartrace/policy.py`
- `scholartrace/provenance.py`
- `scholartrace/render.py`
- `scholartrace/validation.py`
- `schemas/scholartrace_case_bundle.schema.json`
- `schemas/scholartrace_analysis_proposal.schema.json`
- `schemas/scholartrace_audit_result.schema.json`
- `examples/scholartrace/README.md`
- `examples/scholartrace/education_claim_audit_case.json`
- `examples/scholartrace/education_claim_audit_proposal.json`
- `examples/scholartrace/education_claim_audit_gold.json`
- `examples/scholartrace/fixture_provenance_manifest.json`
- `tests/test_scholartrace_pipeline.py`
- `build_week_2026/SCHOLARTRACE_DETERMINISTIC_PIPELINE_USAGE.md`
- `build_week_2026/SCHOLARTRACE_FIXTURES_SCHEMA_AND_DETERMINISTIC_PIPELINE_REPORT.md`
- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`

No task file is restaged because the governing task is already committed in
the task-bearing start HEAD.

## Commit, push, and final state

The single implementation commit containing this report is identified by Git
history. Its exact SHA, push result, remote workflow result, final HEAD,
upstream, `origin/main`, and final status are recorded in the final gate
output because a commit cannot contain its own final SHA.

The only authorized push target is:

`origin/build-week-2026-scholartrace`

## Forbidden-operation check

PASS:

- no model or model API was invoked;
- no credential or account source was inspected;
- no external content or evidence was retrieved;
- no Zotero, Obsidian, PDF, private research, purchased data, or unpublished
  material was accessed;
- no locked permission, notice, README, Skill, template, or root `LICENSE`
  file was modified;
- no output overwrite was allowed;
- no merge or push to `main` occurred;
- no release, deployment, submission, video, or public demo claim was made;
- no wildcard staging, force-push, or destructive Git recovery was used; and
- the frozen taxonomy and safety policy were preserved.

## Caveats and readiness

- The gold record remains unreviewed and `human_verified: false`.
- No GPT-5.6 or other model behavior has been evaluated.
- The host blocked automated deletion of the task-specific system-temp smoke
  directory. It is outside the repository and contains only the two synthetic
  generated outputs.
- GitHub Actions status is available only after push.
- GPT GitHub acceptance has not been claimed.

Local implementation readiness: `GO_FOR_GITHUB_ACCEPTANCE`.

Expected next acceptance target:

- `GITHUB_ACCEPTANCE_L4_CI_OR_TEST_VERIFIED` if remote workflow evidence is
  available;
- otherwise `GITHUB_ACCEPTANCE_L3_COMMIT_OR_PR_VERIFIED` with a CI caveat.

Only after acceptance should the next task be created:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_BOUNDED_INTEGRATION_AND_EVALUATION_GATE`
