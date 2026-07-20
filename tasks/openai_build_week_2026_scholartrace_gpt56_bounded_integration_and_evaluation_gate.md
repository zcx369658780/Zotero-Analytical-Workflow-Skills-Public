# OpenAI Build Week 2026 — ScholarTrace GPT-5.6 Bounded Integration and Evaluation Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-scholartrace`  
Task type: bounded model integration, live synthetic evaluation, and evidence gate

## 0. Goal

Integrate GPT-5.6 into the already accepted ScholarTrace deterministic evidence gate without weakening any deterministic, privacy, copyright, no-overwrite, or human-review boundary.

This gate must:

1. add a bounded OpenAI Responses API adapter that converts an approved synthetic case bundle into a schema-valid ScholarTrace semantic-analysis proposal;
2. use GPT-5.6 meaningfully for semantic claim decomposition, evidence mapping, qualifier detection, and rationale proposals;
3. keep the existing deterministic policy as the only authority for final verdicts and safety downgrades;
4. perform a narrowly bounded live evaluation on the frozen synthetic education fixture when authorized API access is available;
5. record sanitized model, input-hash, output-hash, usage, latency, schema, policy, and evaluation evidence without exposing credentials or private account data;
6. add offline adapter tests and update GitHub Actions without requiring an API secret; and
7. produce a reproducible completion report and a clear readiness decision for the demo-productization gate.

The live model call is limited to the existing independently written synthetic fixture. No private, purchased, unpublished, or externally copied research material may be sent to the model.

## 1. Accepted baseline

Accepted deterministic implementation commit:

`2fca61f61dcf5218290a101f15e5b6a2f142c6a2`

Accepted scope-freeze commit:

`341b30951cac04903960e6f8a6c3cd6fd58bda75`

Accepted permission/licensing baseline on `main`:

`6c1c6caa93318f08cff666d94de26da42447ef59`

Protected pre-Build-Week tag:

`pre-build-week-2026-public-baseline`

Required tag target:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-bearing commit that adds this task file is expected after `2fca61f...` and must be identified separately.

## 2. Official model and API boundary

Use only official OpenAI interfaces.

Required default live model:

`gpt-5.6-sol`

The implementation may accept `gpt-5.6` as an alias and may permit `gpt-5.6-terra` or `gpt-5.6-luna` only through an explicit CLI option, but it MUST reject non-GPT-5.6 models in this gate.

Use the OpenAI Responses API through the official Python SDK. Use Structured Outputs or an equivalent strict JSON-schema response format supported by the Responses API.

Required request properties:

- `store=False`;
- no web search, file search, computer use, code interpreter, hosted shell, MCP, or other tools;
- input limited to the approved synthetic case bundle and the frozen semantic-proposal contract;
- bounded output token limit appropriate to the seven-claim fixture;
- reasoning effort explicitly set, with `medium` as the default unless the current SDK requires a documented equivalent;
- no background mode;
- no multi-turn persistence;
- no upload of files to the API;
- no fallback to another model family;
- no silent retry loop.

If the currently installed SDK surface differs from the documented request shape, implement the closest official supported equivalent and document the exact SDK version and request fields used. Do not use undocumented private endpoints.

## 3. Required context to read

Read before implementation:

- `tasks/openai_build_week_2026_scholartrace_fixtures_schema_and_deterministic_pipeline_gate.md`
- `build_week_2026/SCHOLARTRACE_MVP_SCOPE.md`
- `build_week_2026/SCHOLARTRACE_FIXTURE_AND_EVALUATION_PLAN.md`
- `build_week_2026/CODEX_GPT56_USAGE_PLAN.md`
- `build_week_2026/BUILD_WEEK_READINESS_DECISION.md`
- `build_week_2026/SCHOLARTRACE_DETERMINISTIC_PIPELINE_USAGE.md`
- `build_week_2026/SCHOLARTRACE_FIXTURES_SCHEMA_AND_DETERMINISTIC_PIPELINE_REPORT.md`
- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`
- `schemas/scholartrace_case_bundle.schema.json`
- `schemas/scholartrace_analysis_proposal.schema.json`
- `schemas/scholartrace_audit_result.schema.json`
- `scholartrace/cli.py`
- `scholartrace/policy.py`
- `scholartrace/provenance.py`
- `scholartrace/render.py`
- `scholartrace/validation.py`
- `tests/test_scholartrace_pipeline.py`
- `.github/workflows/scholartrace-tests.yml`
- `LICENSE_SCOPE.md`
- `THIRD_PARTY_NOTICES.md`

Treat the accepted schemas, five-verdict taxonomy, deterministic rules, synthetic fixture identities, and safety boundaries as authoritative. If model integration would require changing those semantics, stop and report rather than broadening scope.

## 4. Repository and Git preflight

Before writing:

1. run `git fetch origin --tags`;
2. verify the exact public repository identity and accepted SSH/HTTPS origin;
3. verify the current branch is `build-week-2026-scholartrace`;
4. verify the task-bearing start HEAD descends directly from `2fca61f...` with only this task-file commit added after it;
5. verify `origin/main` remains at or contains `6c1c6caa...` and will not be modified;
6. verify the protected tag target exactly;
7. run `git status --short --untracked-files=all`;
8. stop if unrelated tracked or untracked project changes exist.

Use explicit-path staging only. Never use `git add .` or `git add -A`.

## 5. Credential and account safety

The only authorized credential source is the process environment variable:

`OPENAI_API_KEY`

Codex MUST NOT:

- print, echo, hash, count characters of, partially reveal, or otherwise inspect the key value;
- search for `.env` files, key stores, shell history, browser storage, config files, credentials, or tokens;
- create an API key;
- modify account billing or organization settings;
- write the key to code, tests, logs, reports, subprocess arguments, GitHub Actions, or repository files.

It may check only whether `OPENAI_API_KEY` is present and non-empty.

Optional organization or project environment variables may be passed through only if the official SDK reads them normally; their values must not be printed or persisted.

GitHub Actions MUST remain secret-free and MUST NOT execute live model calls.

## 6. Required implementation

### 6.1 Official SDK dependency

Add the official `openai` Python SDK as an optional dependency group suitable for live model use. Preserve installation and execution of the deterministic package without the optional model dependency.

Document the exact dependency extra, for example:

`pip install -e ".[openai]"`

Use a bounded compatible version range. Record the actually installed SDK version in the live evaluation report.

### 6.2 Provider abstraction

Add a small provider boundary, for example:

- `scholartrace/providers/__init__.py`
- `scholartrace/providers/openai_responses.py`

The adapter MUST:

- accept an already validated case bundle;
- build a deterministic, reviewable prompt from only the supplied source excerpts, locators, limitations, and claims;
- request output conforming to `scholartrace_analysis_proposal.schema.json`;
- reject missing, additional, malformed, or invented identifiers;
- reject citations to source IDs or claim IDs not present in the input;
- reject any returned `human_verified: true`, E3 promotion, or final-verdict authority if such fields appear;
- return only a semantic-analysis proposal to the deterministic pipeline;
- expose a sanitized metadata object containing model requested, model returned, response identifier if safe, creation time if supplied, usage token counts, latency, SDK version, request configuration, and input/output SHA256 values;
- never persist hidden reasoning, chain of thought, credentials, request headers, or full private SDK objects.

### 6.3 Prompt contract

Create a public, versioned prompt template or prompt-builder module. It must state that GPT-5.6 is a semantic proposal generator, not the final adjudicator.

The prompt must require:

- analysis of every supplied `claim_id` exactly once;
- use only supplied source excerpts;
- stable source and claim identifiers;
- detection of unsupported material components;
- correlation-versus-causation distinction;
- sample, period, geography, population, method, and scope qualifiers;
- explicit uncertainty rather than guessing;
- concise rationale candidates;
- no human-verification claim;
- no E3 or citation-eligibility promotion;
- no external knowledge or browsing;
- strict schema output.

Create a prompt version identifier, initially such as:

`scholartrace-gpt56-prompt-0.1.0`

### 6.4 CLI integration

Extend the CLI with a clear bounded live-model path. Acceptable design:

- a `propose` command that writes a proposal and sanitized run metadata; and
- the existing deterministic command consumes that proposal to produce the final map and report;

or one `audit --provider openai` path with explicit intermediate-output recording.

Required CLI properties:

- deterministic/offline behavior remains the default;
- live use requires an explicit flag or command;
- model default is `gpt-5.6-sol`;
- non-GPT-5.6 models are rejected;
- `--dry-run` or equivalent must show intended paths and request configuration without calling the API;
- actual API invocation requires an explicit live flag;
- actual file writing requires an explicit write flag;
- outputs are no-overwrite;
- output directory is explicit and must not be a real Zotero or Obsidian location;
- model proposal, final audit, report, and sanitized metadata have stable filenames;
- exit codes distinguish missing SDK, missing key, model/API failure, schema failure, deterministic evaluation failure, and output collision;
- failure never falls back to the human-authored proposal while claiming live GPT-5.6 success.

### 6.5 Live-run evidence files

For a successful bounded run, write to a new no-overwrite directory under a task-specific local output root first.

After validation, copy only the sanitized selected-run evidence into a new repository path such as:

`examples/scholartrace/gpt56_evaluation/`

Required committed evidence:

- `gpt56_analysis_proposal.json`
- `gpt56_claim_evidence_map.json`
- `gpt56_audit_report.md`
- `gpt56_run_metadata.json`
- `gpt56_evaluation_summary.md`

Do not commit raw SDK response dumps, request headers, credentials, private paths, hidden reasoning, or failed-attempt payloads containing sensitive data.

The metadata must include:

- fixture identifier and hashes;
- requested and returned model identity;
- prompt version;
- schema, tool, and policy versions;
- `store: false` status;
- no-tools status;
- reasoning effort;
- max output setting;
- SDK version;
- sanitized response ID if retained;
- input/output token usage when returned;
- latency;
- proposal and final-output hashes;
- deterministic rule outcomes;
- gold-verdict agreement;
- `human_verified: false` and no-E3 checks;
- attempt number and total authorized live attempts used.

### 6.6 Offline tests

Add tests using a fake or monkeypatched official-client boundary. They MUST cover:

- correct model and request configuration;
- `store=False`;
- no tools;
- strict structured-output request;
- missing optional SDK;
- missing `OPENAI_API_KEY` without revealing or searching for credentials;
- non-GPT-5.6 model rejection;
- malformed model response rejection;
- unknown source/claim identifier rejection;
- model output unable to override deterministic downgrades;
- no automatic E3 or human verification;
- live-write no-overwrite behavior;
- sanitized metadata excludes key, headers, prompts containing secrets, and private SDK objects;
- deterministic existing tests remain unchanged in behavior.

## 7. Bounded live-evaluation policy

A live call may occur only after all offline tests pass.

Approved input:

`examples/scholartrace/education_claim_audit_case.json`

No other live input is authorized.

Maximum live attempts:

- up to three total model requests in this gate;
- each attempt must use the same frozen fixture and GPT-5.6 family;
- transient transport failure may consume an attempt;
- no unbounded automatic retry;
- every attempt number and sanitized outcome must be recorded locally;
- only the selected final successful sanitized result may be committed.

Prompt or adapter corrections between attempts are permitted only when they remain within the frozen scope and are documented in the report. Do not edit the fixture or gold labels merely to make the model pass.

Live evaluation success requires:

1. returned proposal passes the proposal schema;
2. every input claim appears exactly once;
3. every referenced source ID exists;
4. deterministic pipeline completes;
5. final verdict distribution covers the frozen fixture as expected;
6. 100% final-verdict agreement with the gold record;
7. all required causality and qualifier downgrade flags are enforced;
8. zero invented evidence identifiers or locators;
9. zero automatic E3 or `human_verified: true` values;
10. repeated file writing is safely refused and existing bytes remain unchanged;
11. no credential, private path, external source, or prohibited content appears in committed evidence.

If live access is unavailable, do not fabricate a live result. The gate may still commit a fully tested adapter with the blocked verdict defined below, but the next gate must remain blocked until an actual GPT-5.6 run is completed.

## 8. Required documentation and reports

Create or update:

- `build_week_2026/SCHOLARTRACE_GPT56_INTEGRATION_USAGE.md`
- `build_week_2026/SCHOLARTRACE_GPT56_BOUNDED_INTEGRATION_AND_EVALUATION_REPORT.md`
- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`

The usage document must include:

- optional dependency installation;
- environment-variable setup without showing a key;
- dry-run command;
- live proposal/audit command;
- no-overwrite behavior;
- offline fixture replay command;
- explicit statement that API billing is separate from a ChatGPT subscription;
- privacy and data-retention caveat;
- deterministic-policy authority;
- human-review boundary.

The report must include:

- repository, branch, accepted baseline, task-bearing HEAD;
- implementation summary;
- exact files changed;
- official SDK version;
- request configuration;
- live-attempt count and sanitized outcomes;
- fixture, prompt, proposal, map, report, and metadata hashes;
- token usage and latency if returned;
- schema and deterministic evaluation results;
- gold agreement and rule-flag agreement;
- no-overwrite verification;
- offline unit-test results;
- GitHub Actions status if available before final response;
- secret/privacy/copyright scan;
- locked-file preservation;
- staged paths, commit, push, final status;
- known caveats;
- readiness verdict and recommended next gate.

Do not include the API key, private account IDs, billing details, organization identifiers, private Codex Session ID, or private transcript.

## 9. GitHub Actions

Update `.github/workflows/scholartrace-tests.yml` only as necessary to run the expanded offline test suite.

Requirements:

- no OpenAI API call;
- no API secret requirement;
- read-only GitHub token permissions;
- deterministic fixtures and fake-client tests only;
- existing fixture verification, unittest, and CLI smoke tests remain;
- optional OpenAI dependency may be installed only if needed for import/interface tests and must not trigger network model calls.

## 10. Locked and protected files

MUST NOT modify:

- `README.md`;
- `UPSTREAM_PERMISSION_FINAL.md`;
- `THIRD_PARTY_NOTICES.md`;
- `LICENSE_SCOPE.md`;
- `ACKNOWLEDGEMENTS.md`;
- `FILE_MAPPING_AND_HASH_MANIFEST.md`;
- `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- root `LICENSE`;
- the three pre-existing `SKILL.md` files;
- `templates/论文精读模板.md`;
- the frozen synthetic case, proposal, gold, or provenance manifest from commit `2fca61f...`, except that no change to them is expected or authorized in this gate;
- the accepted three JSON schemas, unless a clear implementation defect makes a backward-compatible correction essential. Any schema modification requires a stop-and-report recommendation rather than an automatic change in this gate.

Do not modify `origin/main`.

## 11. Forbidden operations

Codex MUST NOT:

- access Zotero, Obsidian, PDFs, private research files, purchased data, private messages, or external article content;
- search for credentials or API keys;
- print or persist credential values;
- use any model outside the GPT-5.6 family;
- invoke web search, file search, computer use, code interpreter, hosted shell, MCP, or other model tools;
- send repository source code, legal files, private paths, or unrelated content to the API;
- use the live API from GitHub Actions;
- alter gold labels or fixtures to improve the result;
- weaken deterministic rules;
- make model output final academic authority;
- set E3, `citation_eligible: true`, or `human_verified: true`;
- overwrite output;
- merge or push to `main`;
- create a release, deployment, public service, Devpost submission, or video;
- create or publish the final `/feedback` Session ID in the repository;
- use `git add .` or `git add -A`;
- force-push.

## 12. Required checks

At minimum run:

1. all existing deterministic fixture checks;
2. full unittest suite;
3. new fake-client/provider tests;
4. CLI dry-run proving no API request occurs;
5. missing-key and missing-SDK tests;
6. non-GPT-5.6 rejection test;
7. structured-output and identifier-validation tests;
8. deterministic-override prevention tests;
9. secret/privacy scan over changed and generated files;
10. locked-file diff check;
11. live evaluation when `OPENAI_API_KEY` is present;
12. schema validation of live proposal and final output;
13. gold and rule-flag comparison;
14. explicit-write and repeated-write no-overwrite test;
15. workflow syntax and local reproduction of CI commands;
16. staged-diff inspection;
17. final clean-status check after push.

## 13. Commit and push policy

Commit and push only to:

`build-week-2026-scholartrace`

Use explicit-path staging only.

Suggested commit message on complete live success:

`feat: integrate GPT-5.6 with ScholarTrace evidence gate`

If adapter implementation is complete but live access is blocked, use:

`feat: add bounded GPT-5.6 adapter pending live evaluation`

Do not merge to `main`.

## 14. Expected verdicts

On full implementation, successful bounded live GPT-5.6 evaluation, local checks, and push:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_BOUNDED_INTEGRATION_AND_EVALUATION_COMPLETE`

If implementation and offline tests pass but no authorized live API access is available:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_ADAPTER_COMPLETE_LIVE_EVALUATION_BLOCKED`

If model access exists but the bounded evaluation cannot pass without violating scope or changing frozen fixtures/gold:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_EVALUATION_FAILED_CLOSED`

If repository, privacy, credential, licensing, or locked-file safety fails:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_INTEGRATION_BLOCKED_BY_SAFETY_STATE`

## 15. Acceptance target and next gate

Codex must self-report local checks, live-run status, commit, push, and known caveats. It must not claim GPT GitHub acceptance.

Expected GPT acceptance target:

`GITHUB_ACCEPTANCE_L4_CI_OR_TEST_VERIFIED`

Only after GPT verifies the implementation diff, sanitized live evidence, deterministic evaluation, CI, and locked-file preservation should the next task be created:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_DEMO_PRODUCTIZATION_AND_SUBMISSION_ASSET_GATE`

If live evaluation is blocked or failed closed, the next task must be a narrow access or evaluation remediation gate instead.

End the Codex session after this gate. Do not auto-start the next task.

## 16. Primary Codex session reminder

Continue using the same primary ScholarTrace Codex session if possible.

In the final response, remind the user to retain privately:

- the current primary Codex Session ID;
- the exact live-run date and model identity;
- the later `/feedback` Session ID.

Do not commit those private identifiers or transcripts to the public repository.