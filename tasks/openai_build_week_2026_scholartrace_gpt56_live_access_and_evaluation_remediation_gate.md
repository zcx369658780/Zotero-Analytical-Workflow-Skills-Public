# OpenAI Build Week 2026 — ScholarTrace GPT-5.6 Live Access and Evaluation Remediation Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-scholartrace`  
Task type: credential-availability preflight, bounded live GPT-5.6 evaluation, and evidence remediation

## 0. Goal

Resolve the sole remaining blocker from the accepted GPT-5.6 adapter gate by performing a real, narrowly bounded GPT-5.6 Sol evaluation on the frozen synthetic education fixture.

This gate must:

1. preserve the accepted adapter, fixture, schemas, deterministic policy, privacy, copyright, no-overwrite, and human-review boundaries;
2. repeat the complete offline test and fixture suite before any model request;
3. use only the official OpenAI Python SDK and Responses API;
4. make no more than three live requests in this gate;
5. send only the frozen synthetic case and public semantic-proposal contract;
6. validate every returned identifier, locator, schema field, authority field, verdict, rule flag, and evidence mapping locally;
7. keep the deterministic policy as the sole authority for final verdicts;
8. generate and preserve sanitized live-evaluation artifacts and hashes if a request succeeds;
9. update offline tests when a bounded adapter or prompt correction is required by the current official API surface;
10. produce a clear `GO`, `CONDITIONAL_GO`, or `NO_GO` decision for demo productization.

This gate is not a general model experiment. It does not authorize real research content, broader prompt tuning, deployment, submission, or user-facing product expansion.

## 1. Accepted baseline

Accepted bounded adapter commit:

`f8fa1c9f23f5c3e222aea529d3299c91792df246`

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

The task-bearing commit that adds this task file is expected immediately after `f8fa1c9f...` and must be identified separately.

## 2. Official model and API boundary

Use only official OpenAI interfaces.

Required live model:

`gpt-5.6-sol`

The `gpt-5.6` alias MAY be used only if the exact model ID `gpt-5.6-sol` is rejected by the official service while the alias is officially documented to route to GPT-5.6 Sol. Such use counts as a live attempt and must be explicitly reported. No other model, including Terra, Luna, GPT-5.5, GPT-5.4, or a non-OpenAI model, is authorized.

Use the official OpenAI Python SDK and Responses API with strict Structured Outputs.

Required request properties:

- `store=False`;
- `background=False`;
- no tools;
- no web search, file search, computer use, code interpreter, hosted shell, apply-patch tool, MCP, skill invocation, or retrieval;
- no uploaded file;
- no conversation, previous-response, or multi-turn persistence;
- `reasoning.effort=medium` unless the installed official SDK requires a documented equivalent;
- `max_output_tokens=8000` unless one narrowly documented reduction is required to address a quota or request-size error;
- SDK automatic retries disabled;
- no application retry loop;
- no fallback to another model family;
- request input limited to the canonicalized frozen case and semantic-proposal contract;
- output restricted to the accepted strict proposal schema.

Official current references for implementation review:

- `https://developers.openai.com/api/docs/models/gpt-5.6-sol`
- `https://developers.openai.com/api/docs/guides/latest-model`
- `https://platform.openai.com/docs/api-reference/responses`

Do not use undocumented private endpoints or reverse-engineered ChatGPT endpoints.

## 3. Required context to read

Read before any change or live request:

- `tasks/openai_build_week_2026_scholartrace_gpt56_bounded_integration_and_evaluation_gate.md`
- `build_week_2026/SCHOLARTRACE_GPT56_BOUNDED_INTEGRATION_AND_EVALUATION_REPORT.md`
- `build_week_2026/SCHOLARTRACE_GPT56_INTEGRATION_USAGE.md`
- `build_week_2026/SCHOLARTRACE_FIXTURES_SCHEMA_AND_DETERMINISTIC_PIPELINE_REPORT.md`
- `build_week_2026/SCHOLARTRACE_MVP_SCOPE.md`
- `build_week_2026/SCHOLARTRACE_FIXTURE_AND_EVALUATION_PLAN.md`
- `build_week_2026/CODEX_GPT56_USAGE_PLAN.md`
- `examples/scholartrace/fixture_provenance_manifest.json`
- `examples/scholartrace/education_claim_audit_case.json`
- `examples/scholartrace/education_claim_audit_gold.json`
- the three ScholarTrace schemas;
- `scholartrace/prompt.py`;
- `scholartrace/providers/openai_responses.py`;
- `scholartrace/evaluation.py`;
- `scholartrace/policy.py`;
- `scholartrace/cli.py`;
- `tests/test_scholartrace_pipeline.py`;
- `tests/test_scholartrace_openai.py`;
- `LICENSE_SCOPE.md`;
- `THIRD_PARTY_NOTICES.md`;
- `UPSTREAM_PERMISSION_FINAL.md`.

Do not read private email evidence, Zotero files, Obsidian files, PDFs, or unrelated project content.

## 4. Repository and Git preflight

Before writing or calling the API:

1. run `git fetch origin --tags`;
2. confirm the exact repository and accepted SSH/HTTPS origin;
3. confirm the current branch is `build-week-2026-scholartrace`;
4. confirm the task-bearing start HEAD descends immediately from `f8fa1c9f...` and adds only this task file;
5. confirm `origin/main` remains at or contains `6c1c6caa...` and is not modified;
6. confirm the protected tag target exactly;
7. run `git status --short --untracked-files=all`;
8. stop if unrelated tracked or untracked project changes exist.

Use explicit-path staging only. Never use `git add .` or `git add -A`.

## 5. Credential and billing boundary

The only authorized credential source is the current process environment variable:

`OPENAI_API_KEY`

Codex MUST:

- check only whether the variable is present and non-empty;
- never print, echo, hash, truncate, partially reveal, serialize, persist, or commit the value;
- never search `.env`, shell history, PowerShell history, browser storage, credential managers, registry entries, config files, notebooks, logs, or other secret sources;
- never ask the user to paste the key into chat or a repository file;
- never add a GitHub Actions secret or run a live request in CI;
- never infer billing status from ChatGPT subscription status.

If the environment variable is absent or empty, stop before changing implementation files and report:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_LIVE_EVALUATION_BLOCKED_CREDENTIAL_UNAVAILABLE`

If the API returns authentication, account, billing, quota, rate-tier, organization, or model-access denial, preserve a sanitized error category and stop unless the task's bounded alias rule applies. Do not expose raw headers, request IDs, account identifiers, organization identifiers, or credential fragments.

## 6. Frozen live input and prohibited content

The only source case that may be sent is:

`examples/scholartrace/education_claim_audit_case.json`

Required frozen SHA256:

`653FEA5B5B507B8258C620B9AFFE0D125AA9CC3D1884F69D97B7A119EDD55B1C`

The gold file is local evaluation authority only and MUST NOT be sent to the model:

`examples/scholartrace/education_claim_audit_gold.json`

The following MUST NOT be sent:

- the human-authored proposal;
- gold verdicts or expected rule flags;
- repository source code;
- tests;
- reports;
- legal or licensing files;
- private paths;
- Zotero or Obsidian content;
- PDF content;
- purchased, private, unpublished, or real research material;
- Xiaohongshu or external article content;
- Codex transcript or Session ID;
- credentials or account metadata.

Before the first request, recalculate and verify the frozen case hash, canonical-input hash, prompt hash, and strict-schema hash. Stop on drift.

## 7. Mandatory offline preflight

Before any live attempt, run and require exit code `0` for:

1. install the local package with the already accepted optional OpenAI extra, without changing dependency declarations;
2. `python -m scholartrace verify-fixtures --fixture-dir examples/scholartrace`;
3. `python -m unittest discover -s tests -v`;
4. the existing validation command for the frozen case and human-authored proposal;
5. the existing deterministic offline audit;
6. the existing GPT-5.6 `propose --dry-run` command;
7. a no-key isolated-process test confirming exit `4` and zero output;
8. a non-GPT-5.6 test confirming rejection and zero provider call;
9. `git diff --check`;
10. locked-file identity checks.

Require at least `24/24 PASS` before the first request. If offline checks fail, make no live request and report a blocked verdict.

Do not change the frozen case, gold, provenance manifest, accepted schemas, or deterministic policy to make a live result pass.

## 8. Live-attempt budget and order

Maximum live attempts in this gate: `3`.

An API request counts as an attempt once submitted to the official client, regardless of success, refusal, malformed output, timeout, or account error.

### Attempt 1

Use the accepted adapter and prompt without implementation modification:

- model: `gpt-5.6-sol`;
- reasoning effort: `medium`;
- max output tokens: `8000`;
- a new task-specific output directory outside the repository;
- attempt number `1`;
- live + explicit write.

The output directory must be checked before the request. A collision must fail without consuming an API attempt.

### Attempt 2 — only if justified

Attempt 2 is allowed only after one of these bounded conditions:

1. the exact model ID is rejected while the officially documented `gpt-5.6` alias remains available; or
2. the official SDK/API rejects the request shape and a minimal adapter-only compatibility correction is required; or
3. the model returns schema-invalid output and one minimal prompt-contract clarification is justified; or
4. the proposal is schema-valid but fails required local identifier, locator, authority, or deterministic-evaluation checks, and one minimal prompt clarification can address the observed failure without exposing gold labels.

Before Attempt 2:

- preserve Attempt 1 artifacts or sanitized failure metadata in a no-overwrite evidence directory;
- add or update an offline regression test reproducing the issue with a fake client where possible;
- rerun the complete offline suite;
- increment the prompt version if prompt wording changes;
- do not change the frozen case, gold, schemas, policy, or verdict taxonomy.

### Attempt 3 — exceptional final attempt

Attempt 3 is allowed only if Attempt 2 demonstrates clear progress but one narrow schema/compatibility defect remains. Repeat the same regression-test and full-offline-suite requirements.

No fourth request is authorized. Do not retry automatically.

## 9. Permitted bounded implementation changes

Prefer a no-code live evaluation. If the official API or observed bounded output requires a correction, this task authorizes changes only to:

- `scholartrace/providers/openai_responses.py`;
- `scholartrace/prompt.py`;
- `scholartrace/evaluation.py`;
- `scholartrace/cli.py` only when required for sanitized error handling or attempt evidence;
- `tests/test_scholartrace_openai.py`;
- `pyproject.toml` only if the already declared official SDK range is technically incompatible and an exact evidence-backed minimum adjustment is required;
- new sanitized live-evaluation documentation and evidence paths specified below;
- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`.

Do not refactor unrelated deterministic code or broaden product scope.

Any prompt change must receive a new version and hash. Never silently mutate a versioned prompt.

## 10. Required local validation of every successful response

A successful provider response is not accepted until all checks pass:

1. returned model identity is GPT-5.6 Sol or the authorized `gpt-5.6` alias path;
2. structured output parses as JSON;
3. strict proposal schema passes;
4. every `claim_id` exists in the frozen case;
5. every `source_id` exists in the frozen case;
6. every locator is one of the supplied locators for the cited source;
7. no invented evidence excerpt, source, claim, citation, URL, path, or external fact exists;
8. no final-verdict authority is supplied by the model;
9. no E3, citation approval, `human_verified: true`, grading, publication, or legal authority is introduced;
10. deterministic adjudication produces seven final claim results;
11. all five verdict labels remain represented;
12. the three required teaching cases match gold verdicts;
13. all seven final verdicts match the frozen gold record;
14. required deterministic rule flags match gold;
15. required evidence links and qualifier flags match gold;
16. final results remain `human_verified: false`;
17. no output overwrite occurs;
18. output and report schemas pass;
19. sanitized metadata contains no credential, raw response object, request headers, private account data, private path, or prompt text beyond approved public version/hash references.

Rationale prose may differ within the accepted rubric. The model must not be rewarded for parroting undisclosed gold wording.

If the semantic proposal is useful but final agreement is below target after the third attempt, report the exact failure and retain productization as blocked. Do not edit gold labels to match the model.

## 11. Live evidence output and repository publication

For every submitted attempt, create a new no-overwrite local evidence directory.

For a successful accepted attempt, copy only sanitized, synthetic-data artifacts into:

`build_week_2026/live_evaluation/gpt56_sol_accepted/`

Required public files:

- `gpt56_analysis_proposal.json`;
- `gpt56_claim_evidence_map.json`;
- `gpt56_audit_report.md`;
- `gpt56_run_metadata.json`;
- `gpt56_evaluation_summary.md`;
- `LIVE_EVALUATION_ARTIFACT_MANIFEST.json`.

The public metadata file may include:

- date in UTC;
- requested and returned model IDs;
- official SDK version;
- prompt/schema/tool/policy versions;
- reasoning effort;
- max output token limit;
- `store` and `background` values;
- tools enabled: none;
- attempt number;
- input and output token counts when returned;
- latency in milliseconds;
- sanitized finish/status category;
- canonical input, prompt, schema, proposal, final-map, report, metadata, summary, and manifest hashes;
- test and evaluation counts;
- `human_verified: false`;
- credential source category: process environment only, without any credential value.

The public files MUST NOT include:

- API key material;
- request or response headers;
- organization/project/account identifiers;
- raw SDK object dumps;
- private response or request IDs;
- billing details;
- private paths;
- Codex Session ID;
- private timestamps that expose unrelated user activity;
- content outside the frozen synthetic fixture and approved public prompt contract.

If all attempts fail, do not publish raw failures. Create only a sanitized failure summary in the completion report.

## 12. Required reports

Create or update:

- `build_week_2026/SCHOLARTRACE_GPT56_LIVE_ACCESS_AND_EVALUATION_REMEDIATION_REPORT.md`;
- `build_week_2026/SCHOLARTRACE_GPT56_INTEGRATION_USAGE.md` only if actual usage instructions or verified API behavior changed;
- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`;
- successful public live-evaluation artifacts under the fixed directory in Section 11.

The remediation report must include:

- repository, branch, baselines, and task-bearing start HEAD;
- credential availability category only;
- official SDK version;
- requested and returned model identity;
- exact sanitized request configuration;
- attempt ledger for attempts 1–3;
- issue, correction, prompt version, and regression-test ledger;
- all frozen and generated artifact hashes;
- token usage and latency when returned;
- schema, identifier, locator, authority, evidence, qualifier, rule, verdict, no-E3, human-verification, and no-overwrite results;
- all offline commands, exit codes, and test counts;
- privacy, copyright, credential, and locked-file checks;
- exact staged paths;
- commit and push result;
- GitHub Actions result;
- final readiness decision;
- recommended next gate.

Do not include private credentials, raw API error bodies, private IDs, or private Codex session data.

## 13. GitHub Actions boundary

GitHub Actions must remain offline and secret-free.

Do not add `OPENAI_API_KEY` or any other secret to GitHub Actions. Do not add a live model test. The existing workflow should run the complete offline suite automatically if its path filters already cover the modified implementation and tests.

A successful local live run does not replace CI. After commit and push, require the offline GitHub Actions workflow to pass on the final commit.

## 14. Locked and forbidden modifications

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
- `examples/scholartrace/education_claim_audit_case.json`;
- `examples/scholartrace/education_claim_audit_proposal.json`;
- `examples/scholartrace/education_claim_audit_gold.json`;
- `examples/scholartrace/fixture_provenance_manifest.json`;
- the three accepted schema files;
- `scholartrace/policy.py`;
- the accepted deterministic test file except to add no live behavior; prefer leaving it unchanged.

MUST NOT:

- access Zotero, Obsidian, PDFs, private research, purchased data, unpublished material, external article text, or other repositories;
- modify or push `main`;
- create a PR, release, deployment, video, Devpost submission, or public hosted service;
- use model tools, retrieval, browsing, uploads, background mode, or multi-turn state;
- add secrets to repository or CI;
- publish raw API errors or response objects;
- change fixtures or gold expectations to improve agreement;
- make more than three live requests;
- use wildcard staging;
- force-push;
- start the next gate automatically.

## 15. Allowed commit and push

After local checks and live evaluation are complete, explicitly stage only authorized paths.

Suggested commit message on full success:

`test: record bounded GPT-5.6 live evaluation`

Suggested commit message if live access remains blocked after a valid credential check:

`docs: record GPT-5.6 live access blocker`

Push only to:

`origin/build-week-2026-scholartrace`

Do not merge to `main`.

## 16. Expected verdicts

### Full success

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_LIVE_EVALUATION_COMPLETE`

Requires:

- at least one real authorized GPT-5.6 Sol request;
- schema-valid proposal;
- all local safety and authority checks pass;
- `7/7` final verdict agreement;
- all required rule, evidence, and qualifier checks pass;
- accepted sanitized artifacts and manifest committed;
- full offline tests pass locally and in GitHub Actions.

### Credential unavailable before request

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_LIVE_EVALUATION_BLOCKED_CREDENTIAL_UNAVAILABLE`

### Account, billing, quota, tier, organization, or model access blocked

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_LIVE_EVALUATION_BLOCKED_PLATFORM_ACCESS`

### Adapter or API compatibility unresolved

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_LIVE_EVALUATION_BLOCKED_API_COMPATIBILITY`

### Model output quality or deterministic agreement unresolved after bounded attempts

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_LIVE_EVALUATION_BLOCKED_EVALUATION`

### Safety or provenance violation

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_GPT56_LIVE_EVALUATION_NO_GO`

## 17. Acceptance and next gate

Codex must self-report local evidence and remote CI status but must not claim GPT GitHub acceptance.

Expected GPT acceptance target on full success:

`GITHUB_ACCEPTANCE_L4_CI_OR_TEST_VERIFIED`

Only after GPT verifies the live artifacts, commit diff, report, and final offline CI should the next task be created:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_DEMO_PRODUCTIZATION_AND_SUBMISSION_ASSETS_GATE`

End the session after this gate.