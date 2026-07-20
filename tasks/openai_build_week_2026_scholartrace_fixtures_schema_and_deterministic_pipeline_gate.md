# OpenAI Build Week 2026 — ScholarTrace Fixtures, Schema, and Deterministic Pipeline Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-scholartrace`  
Task type: first bounded Build Week implementation gate

## 0. Goal

Implement and validate the first independently developed ScholarTrace / Evidence Gate MVP slice:

1. one lawful, independently written synthetic education case bundle covering all five frozen verdicts and the required teaching mistakes;
2. normative JSON schemas for the case bundle, semantic-analysis proposal, and final audit result;
3. a deterministic fail-closed adjudication pipeline;
4. a read-only-by-default, no-overwrite CLI;
5. structured `claim_evidence_map.json` and human-readable `audit_report.md` outputs;
6. focused automated tests and a no-secret GitHub Actions workflow; and
7. a reproducible implementation report.

This gate MUST NOT invoke GPT-5.6 or any other model. The semantic-analysis proposal used here is a synthetic, human-authored fixture that exercises the same bounded interface a later GPT-5.6 gate may use.

## 1. Accepted baseline

The accepted scope-freeze commit is:

`341b30951cac04903960e6f8a6c3cd6fd58bda75`

The accepted permission/licensing baseline on `main` is:

`6c1c6caa93318f08cff666d94de26da42447ef59`

The protected pre-Build-Week tag is:

`pre-build-week-2026-public-baseline`

and MUST resolve to:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-bearing commit that adds this task file is expected after `341b3095...` and must be identified separately.

## 2. Required context to read

Read before implementation:

- `build_week_2026/PRE_EXISTING_WORK.md`
- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`
- `build_week_2026/SCHOLARTRACE_MVP_SCOPE.md`
- `build_week_2026/SCHOLARTRACE_FIXTURE_AND_EVALUATION_PLAN.md`
- `build_week_2026/CODEX_GPT56_USAGE_PLAN.md`
- `build_week_2026/BUILD_WEEK_READINESS_DECISION.md`
- `build_week_2026/PUBLIC_REPO_BASELINE_AND_SCHOLARTRACE_SCOPE_GATE_REPORT.md`
- `LICENSE_SCOPE.md`
- `THIRD_PARTY_NOTICES.md`
- `UPSTREAM_PERMISSION_FINAL.md`

Treat the scope-freeze documents as authoritative. If implementation would require changing the frozen taxonomy, safety boundary, input/output contract, or non-goals, stop and report rather than broadening scope.

## 3. Repository and Git preflight

Before writing:

1. run `git fetch origin --tags`;
2. verify the repository identity and accepted SSH/HTTPS origin;
3. verify the current branch is `build-week-2026-scholartrace`;
4. verify the task-bearing start HEAD descends directly from `341b3095...` with only this task-file commit added after it;
5. verify `origin/main` remains at or contains `6c1c6caa...` and is not modified by this task;
6. verify the protected tag target exactly;
7. run `git status --short --untracked-files=all`;
8. stop if unrelated tracked or untracked project changes exist.

Use explicit-path staging only. Never use `git add .` or `git add -A`.

## 4. Primary Codex session evidence

This is the first implementation gate. Continue using this Codex session as the primary ScholarTrace Build Week development session if possible.

In the final response, state whether the user has been reminded to retain the current Codex Session ID privately for later `/feedback` evidence. Do not place a private Session ID or transcript in the public repository.

## 5. Implementation architecture

Create a new, independently authored Python package at repository root:

```text
scholartrace/
  __init__.py
  __main__.py
  cli.py
  policy.py
  validation.py
  render.py
  provenance.py
```

A small deviation in internal module names is allowed only when documented in the report and the public CLI contract remains unchanged.

Create a minimal `pyproject.toml` with:

- Python `>=3.11`;
- no runtime network/model dependency;
- no secret or account configuration;
- a console entry point equivalent to `scholartrace = scholartrace.cli:main`;
- a package version beginning at `0.1.0`.

Prefer Python standard-library implementation. Do not add an external runtime dependency merely for convenience. If a dependency is genuinely necessary, stop and request a separate dependency decision rather than silently adding it.

## 6. Normative schemas

Create exactly these normative JSON Schema files using JSON Schema Draft 2020-12:

- `schemas/scholartrace_case_bundle.schema.json`
- `schemas/scholartrace_analysis_proposal.schema.json`
- `schemas/scholartrace_audit_result.schema.json`

The schemas and runtime validators MUST enforce the frozen contracts.

### 6.1 Case bundle minimum fields

The case bundle must include:

- `schema_version`;
- stable `case_id`;
- title and educational scenario;
- `source_provenance` with synthetic/reuse status, authoring method, creation date, license/reuse note, and prohibited-content review status;
- one or more source excerpts with stable `source_id`, text, public-safe locator, and material limitations/qualifiers;
- one or more claims with stable `claim_id`, `fixture_id`, text, and optional claim type;
- no local absolute path, credential, private contact detail, PDF path, Zotero key, or real-vault locator.

### 6.2 Analysis proposal minimum fields

The analysis proposal is a non-authoritative semantic proposal. It must include:

- matching `schema_version` and `case_id`;
- one proposal per `claim_id`;
- cited source IDs;
- a bounded evidence status;
- material component/support assessment;
- missing or altered qualifiers;
- deterministic fact flags for causality, scope/generalization, certainty/magnitude, contradiction/no-support, separable partial support, ambiguity/conflict, and missing required context;
- concise rationale candidate;
- unresolved questions;
- no final human verification, E3, publication-readiness, grading, or citation-eligibility authority.

The proposal MUST NOT directly control the final verdict. Runtime policy derives the verdict.

### 6.3 Audit result minimum fields

The final result must include:

- schema and tool version;
- `case_id`;
- deterministic-policy version;
- read-only/no-overwrite status;
- provenance summary;
- stable claim ordering;
- for every claim:
  - `claim_id` and `fixture_id`;
  - exactly one of `supported`, `partially_supported`, `unsupported`, `overstated`, `unverifiable`;
  - cited source IDs and public-safe supplied locators;
  - concise rationale;
  - missing or altered qualifiers;
  - deterministic rule flags;
  - unresolved questions;
  - human-review reason when applicable;
  - `human_verified: false`;
- no E3 promotion and no `citation_eligible: true`.

Runtime validation may be purpose-built for these normative schemas rather than a general JSON Schema engine, but it must be strict, deterministic, documented, and tested against the schema contracts.

## 7. Synthetic fixture bundle

Create:

```text
examples/scholartrace/
  README.md
  education_claim_audit_case.json
  education_claim_audit_proposal.json
  education_claim_audit_gold.json
  fixture_provenance_manifest.json
```

The entire source text, claims, proposal, and gold expectations must be independently written for this project. Do not paraphrase or adapt a real paper, private research material, textbook passage, course assessment, or online article.

The case bundle must contain stable fixtures/claims covering at least:

1. `fixture_supported` — fully aligned claim, expected `supported`;
2. `fixture_partially_supported` — separable compound claim, expected `partially_supported`;
3. `fixture_unsupported_conclusion` — no support or contradiction, expected `unsupported`;
4. `fixture_correlation_as_causation` — observational association written as causation, expected `overstated`;
5. `fixture_omitted_limitations` — sample/period/population/geography/scope materially broadened, expected `overstated`;
6. `fixture_unverifiable_missing_context` — required context/evidence link absent or insufficient in a schema-valid representation, expected `unverifiable`;
7. `fixture_conflicting_evidence` — unresolved conflict/ambiguity, expected `unverifiable`.

The synthetic scenario should be coherent enough for a three-minute Education-track demonstration and should not use sensitive, medical, legal, political, personal, or high-stakes subject matter.

### 7.1 Gold record

The gold record must be human-authored and contain:

- expected verdict for every fixture;
- required evidence IDs;
- required qualifier/rule flags;
- acceptable rationale elements;
- prohibited inventions/upgrades;
- human-review requirement;
- `human_verified: false` and `review_status: unreviewed` until a later human-review gate.

### 7.2 Provenance manifest

The provenance manifest must include:

- stable fixture-set ID and version;
- creation date;
- `synthetic_independently_written: true`;
- authoring method;
- statement of no copied source passage;
- prohibited-content checklist;
- SHA256 for the case, proposal, and gold files after freeze;
- no self-hash requirement for the manifest itself.

Provide a command that revalidates the manifest hashes.

## 8. Deterministic policy

Implement a documented policy version such as `scholartrace-policy-0.1.0`.

The mandatory verdict priority is:

1. **Unverifiable safety conditions first:** missing required context/evidence link, unresolved ambiguity, or conflicting evidence -> `unverifiable`.
2. **No support or contradiction:** relevant evidence exists but does not support, or contradicts, the material conclusion -> `unsupported`.
3. **Strength/scope overreach:** causal overreach, materially broadened scope, or certainty/magnitude/generalization stronger than evidence -> `overstated`.
4. **Separable mixed support:** a supported core plus a separable unsupported/incomplete component, without a stronger overstatement condition -> `partially_supported`.
5. **Full coverage only:** all material components and qualifiers supported, with no higher-priority condition -> `supported`.
6. Any unclassified or internally inconsistent proposal -> fail closed as `unverifiable` or a validation error; never guess.

The policy MUST:

- ignore any attempted proposal-level final verdict that conflicts with policy;
- reject or override attempted `human_verified: true`, E3, or citation approval;
- verify cited source IDs exist in the case bundle;
- resolve locators only from supplied source records;
- produce stable ordering and repeatable output;
- expose rule flags and a concise policy trace;
- never retrieve missing evidence or use network access.

## 9. CLI contract

Required commands or equivalent subcommands:

### 9.1 Validate

```text
python -m scholartrace validate \
  --case examples/scholartrace/education_claim_audit_case.json \
  --proposal examples/scholartrace/education_claim_audit_proposal.json
```

This validates inputs and fixture provenance without writing outputs.

### 9.2 Audit dry-run

```text
python -m scholartrace audit \
  --case examples/scholartrace/education_claim_audit_case.json \
  --proposal examples/scholartrace/education_claim_audit_proposal.json
```

Default behavior must be read-only and write no file. It should print a concise result or JSON to stdout.

### 9.3 Explicit write

```text
python -m scholartrace audit \
  --case examples/scholartrace/education_claim_audit_case.json \
  --proposal examples/scholartrace/education_claim_audit_proposal.json \
  --write \
  --out-dir <new_output_directory>
```

Explicit write must create exactly:

- `<new_output_directory>/claim_evidence_map.json`
- `<new_output_directory>/audit_report.md`

Requirements:

- `--write` requires `--out-dir`;
- output directory must not already contain either output file;
- no `--overwrite` option is permitted in this MVP;
- existing output causes safe nonzero refusal without modification;
- output must not include absolute private input paths;
- no writing to a Zotero or Obsidian location is inferred or performed.

### 9.4 Manifest verification

Provide a command such as:

```text
python -m scholartrace verify-fixtures --fixture-dir examples/scholartrace
```

It must verify the frozen file hashes and provenance declarations.

## 10. Human-readable report

`audit_report.md` must be generated deterministically and include:

- case and provenance summary;
- verdict counts;
- one section per claim in stable order;
- claim text;
- verdict and triggered rules;
- cited source IDs and supplied locators;
- missing/altered qualifiers;
- rationale and unresolved questions;
- explicit `human_verified: false` statement;
- explicit notice that results cannot grant E3, citation eligibility, grading authority, or publication readiness.

Do not include lengthy source reproduction. Use only the bounded synthetic excerpts needed for traceability.

## 11. Tests

Use the standard-library `unittest` framework unless a pre-existing repository test framework is clearly available. Tests must run with:

```text
python -m unittest discover -s tests -v
```

Create focused tests covering at least:

1. all three schemas are valid JSON and required contract fields are enforced;
2. fixture manifest hashes pass and tampering fails;
3. all seven fixtures produce their expected verdicts;
4. all five verdict labels are covered;
5. causal overreach and scope broadening deterministically downgrade to `overstated`;
6. contradiction/no-support produces `unsupported`;
7. conflict or unresolved ambiguity produces `unverifiable`;
8. partial support is allowed only when separable and no stronger rule applies;
9. `supported` requires every material component and qualifier;
10. proposal attempts to set a final verdict cannot override policy;
11. attempted E3, citation approval, or `human_verified: true` is rejected or forced false;
12. invalid/missing source references fail closed;
13. stable ordering and byte-stable JSON output across repeated identical runs;
14. dry-run creates no files;
15. explicit write creates exactly two output files;
16. existing output refuses safely and preserves original bytes;
17. Windows and POSIX absolute private paths are rejected;
18. obvious credentials/tokens and personal contact fields are rejected;
19. prohibited source declarations are rejected;
20. generated Markdown contains the required safety notices and all fixture IDs.

Aim for clear, fast tests. Do not add meaningless test count inflation.

## 12. GitHub Actions

Create:

`.github/workflows/scholartrace-tests.yml`

Requirements:

- run on push and pull request for the ScholarTrace branch/path scope;
- use Python 3.11;
- install the local package without model/API dependencies;
- run fixture verification;
- run the full unittest suite;
- run the dry-run CLI smoke test;
- contain no secrets, tokens, network calls to external model APIs, or deployment step.

Normal GitHub checkout and Python setup actions are allowed. Do not add third-party application integrations.

## 13. Documentation and report

Create:

- `build_week_2026/SCHOLARTRACE_DETERMINISTIC_PIPELINE_USAGE.md`
- `build_week_2026/SCHOLARTRACE_FIXTURES_SCHEMA_AND_DETERMINISTIC_PIPELINE_REPORT.md`

Update only the competition-period implementation section of:

- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`

The usage document must give exact local commands, expected outputs, no-overwrite behavior, and current limitations.

The report must include:

- repository, branch, start HEAD, task-bearing HEAD, and protected-tag target;
- architecture and file inventory;
- synthetic fixture provenance and hashes;
- schema versions;
- deterministic policy and tie-break summary;
- commands run and exit codes;
- test names/counts and results;
- CLI dry-run result;
- explicit-write smoke result in a new temporary directory;
- no-overwrite refusal test and before/after hashes;
- GitHub Actions workflow summary;
- privacy/copyright/secret scan result;
- exact staged paths;
- commit and push result;
- final HEAD, upstream, `origin/main`, and git status;
- forbidden-operation check;
- unresolved caveats;
- readiness recommendation and next gate.

Do not include a private Codex Session ID, credentials, private local paths, or temporary file contents in the repository report.

## 14. Allowed operations

This task authorizes only:

- the repository/Git checks above;
- creation of the new ScholarTrace package, schemas, synthetic example bundle, tests, workflow, usage document, report, and minimal packaging metadata;
- bounded update of `NEW_WORK_SINCE_2026_07_13.md`;
- local execution of the new deterministic Python code and tests;
- local use of new task-specific temporary directories;
- explicit-path staging;
- one focused implementation commit;
- push only to `origin/build-week-2026-scholartrace`.

## 15. Forbidden operations

Codex MUST NOT:

- invoke GPT-5.6, OpenAI API, ChatGPT API, Codex model endpoints, or any other model;
- search for API keys, tokens, credentials, or account configuration;
- use network access to retrieve content or evidence;
- access Zotero Local API, Zotero SQLite, Zotero attachments, PDFs, Obsidian, ResearchVault, purchased data, private research files, or unpublished material;
- modify the five separately licensed downstream counterpart files:
  - `README.md`;
  - the three existing `SKILL.md` files;
  - `templates/论文精读模板.md`;
- modify:
  - root `LICENSE`;
  - `UPSTREAM_PERMISSION_FINAL.md`;
  - `THIRD_PARTY_NOTICES.md`;
  - `LICENSE_SCOPE.md`;
  - `ACKNOWLEDGEMENTS.md`;
  - `FILE_MAPPING_AND_HASH_MANIFEST.md`;
  - `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- add real paper text, copyrighted PDF excerpts, Xiaohongshu material, private notes, or externally copied teaching content;
- write to an existing real output directory or provide an overwrite flag;
- merge or push to `main`;
- create a release, deployment, Devpost submission, video, or public demo claim;
- use `git add .`, `git add -A`, force-push, or destructive Git cleanup;
- silently change the frozen verdict taxonomy or safety policy.

## 16. Staging boundary

Expected staged paths must be limited to:

- this task file if it is not already committed locally;
- `pyproject.toml`;
- `.github/workflows/scholartrace-tests.yml`;
- `scholartrace/**`;
- `schemas/scholartrace_*.schema.json`;
- `examples/scholartrace/**`;
- `tests/test_scholartrace_*.py`;
- `build_week_2026/SCHOLARTRACE_DETERMINISTIC_PIPELINE_USAGE.md`;
- `build_week_2026/SCHOLARTRACE_FIXTURES_SCHEMA_AND_DETERMINISTIC_PIPELINE_REPORT.md`;
- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`.

Stop if any unrelated or locked path would be staged.

Suggested commit message:

`feat: add ScholarTrace deterministic evidence gate`

## 17. Success criteria

Success requires all of the following:

- lawful synthetic fixture provenance passes;
- schemas and runtime validators pass;
- seven fixture expectations pass;
- all five verdicts covered;
- 100% deterministic downgrade enforcement on required cases;
- zero automatic E3, citation approval, or human verification;
- zero overwrite;
- zero prohibited/private source leakage;
- repeatable stable structured output;
- CLI dry-run and explicit-write behavior pass;
- full unittest suite passes;
- GitHub Actions workflow is created without secret/model integration;
- one scoped commit is pushed only to the ScholarTrace branch;
- final working tree is clean.

## 18. Expected verdict and next gate

On complete success, report exactly:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_FIXTURES_SCHEMA_AND_DETERMINISTIC_PIPELINE_COMPLETE`

If a frozen-scope, licensing, fixture-provenance, privacy, deterministic-policy, no-overwrite, or repository-state blocker occurs, stop and report a specific fail-closed verdict rather than weakening requirements.

Expected next GPT acceptance target:

- `GITHUB_ACCEPTANCE_L4_CI_OR_TEST_VERIFIED` when the workflow/check evidence is available;
- otherwise `GITHUB_ACCEPTANCE_L3_COMMIT_OR_PR_VERIFIED` with an explicit CI caveat.

Only after GPT acceptance should the next task be created:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_BOUNDED_INTEGRATION_AND_EVALUATION_GATE`

End the session after this gate. Do not invoke a model or auto-start the next task.