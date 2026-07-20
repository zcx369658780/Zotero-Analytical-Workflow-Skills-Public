# OpenAI Build Week 2026 — Unresolved Source Discovery and Block-Level Clean Rewrite Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-skill-release-prep`  
Task type: bounded source discovery, source-specific rights remediation, and behavior-preserving block-level independent rewrite

## 0. Goal and product boundary

Resolve the four remaining multi-source provenance blockers without changing the submission product into a new application and without attributing material to the wrong author.

The submission product remains the real daily-use bundle only:

- `skills/zotero-collection-manager/`;
- `skills/zotero-data-fetcher/`;
- `skills/zotero-analytical-writer/`;
- their bundled scripts and `agents/openai.yaml` files; and
- `templates/论文精读模板.md`.

This gate has two ordered phases:

1. perform one final bounded, high-signal source-discovery pass for the unresolved blocks;
2. for every block still unresolved or covered by no/ambiguous/incompatible permission, replace only that block through a documented behavior-contract and separated independent-rewrite process.

Do not add ScholarTrace, an API adapter, a hosted service, deployment, or unrelated functionality. Do not require `OPENAI_API_KEY` and do not invoke the OpenAI API or any external model API.

## 1. Accepted baseline

Accepted multi-source provenance reconstruction commit:

`1a9b18981f3c4ddaf864064822ac94e50fa21760`

Accepted prior provenance-audit commit:

`2d4f81014e656f07ae6d22297a3785f8a0f55926`

Accepted daily-use synchronization commit:

`521ef5d60c8b695a6b5c7bfa930511f0fdedf92a`

Accepted public `main` permission baseline:

`6c1c6caa93318f08cff666d94de26da42447ef59`

Protected pre-Build-Week baseline tag:

`pre-build-week-2026-public-baseline`

Required peeled target:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-bearing commit that adds this file must immediately follow `1a9b189...` and add only this governing task file.

## 2. Authoritative unresolved blocks

Use the accepted block manifest as the governing blocker list.

### MSB-010 — infer helpers

Path and range at baseline:

- `skills/zotero-collection-manager/scripts/batch_import_collection.py:127-173`
- functions: `infer_theme`, `infer_methodology`, `infer_core_variable`
- current file blob at baseline: `e4de17dd8bfce5310feb941b0f4882b98da2bf45`

Current route: `UNRESOLVED_SOURCE_BLOCKER`.

### MSB-012 and MSB-013 — first-pass note renderer

Path and range at baseline:

- `skills/zotero-collection-manager/scripts/batch_import_collection.py:355-530`
- current file blob: `e4de17dd8bfce5310feb941b0f4882b98da2bf45`

MSB-012 is exact expression from the already authorized Eternity Chen template, but embedded in an additional Python path outside the five-file permission mapping.

MSB-013 is the surrounding generator control logic with unresolved source history.

### MSB-016 and MSB-017 — deep-read note renderer

Path and range at baseline:

- `skills/zotero-collection-manager/scripts/deep_read_collection.py:462-679`
- current file blob: `21b81dd14ef0bc72c2ca73b08efec68586ebc34f`

MSB-016 is exact expression from the already authorized template embedded in an additional Python path.

MSB-017 is the surrounding deep-read generator logic with incomplete source history.

### MSB-026 — online metadata helpers

Path and range at baseline:

- `skills/zotero-data-fetcher/scripts/zotero_fetch.py:308-579`
- current file blob: `da25d5f421080a589f56d8b2390e163504283306`

Plausible but unestablished candidates include:

- `zbw0520/zotero-codex-skills`;
- `Enthoes1/doi-zotero-skills`.

Current route: `UNRESOLVED_SOURCE_BLOCKER`.

Do not expand the rewrite to blocks already classified as authorized, independently authored, generic, platform-reference-only, or reference-only unless a necessary import or call-site adjustment is minimal and documented.

## 3. Repository preflight

Before any discovery or write:

1. run `git fetch origin --tags`;
2. verify the exact repository identity and accepted SSH/HTTPS origin;
3. verify branch `build-week-2026-skill-release-prep`;
4. verify the task-bearing start HEAD immediately follows `1a9b189...` and adds only this task file;
5. verify `origin/main` remains at or contains `6c1c6caa...` and is not modified;
6. verify the protected tag target exactly;
7. run `git status --short --untracked-files=all`;
8. stop on unrelated tracked or untracked project changes.

Never use `git add .` or `git add -A`. Never force-push.

## 4. Required context

Read:

- `build_week_2026/MULTI_SOURCE_SKILL_PROVENANCE_BLOCK_MANIFEST.csv`;
- `build_week_2026/MULTI_SOURCE_GITHUB_ORIGIN_CANDIDATE_MANIFEST.csv`;
- `build_week_2026/MULTI_SOURCE_LICENSE_AND_PERMISSION_ROUTE_MATRIX.md`;
- `build_week_2026/MULTI_SOURCE_PROVENANCE_RECONSTRUCTION_REPORT.md`;
- `build_week_2026/MULTI_SOURCE_PROVENANCE_READINESS_CHECKPOINT.md`;
- `build_week_2026/THIRD_PARTY_SKILL_LICENSE_AUDIT_REPORT.md`;
- the current affected public scripts;
- existing `SKILL.md` instructions and the authorized public template only as needed to preserve interfaces and behavior.

Do not inspect other `.codex` Skills, private repositories, Zotero databases, Obsidian vaults, PDFs, research data, Downloads, browser data, credential stores, or the ScholarTrace/API branch.

The authorized local daily-use paths may be read only after the public rewrite passes, and only for the bounded post-rewrite identity comparison specified in Section 12. Do not use local affected implementation code as a rewrite source.

## 5. Phase A — final bounded source discovery

Perform no more than 20 additional high-signal GitHub code or repository searches total.

Search only for:

- exact full function signatures;
- distinctive return strings or warnings;
- ordered combinations of two or more non-generic strings;
- uncommon API field/error combinations;
- exact note-rendering helper names or marker sequences;
- exact historical filenames when tied to an unresolved block.

For every credible new candidate:

- identify owner/repository;
- pin commit/tag/path/blob;
- read the actual applicable license file at that version;
- compare the exact relevant block;
- classify confidence and rights route.

Do not download or execute candidate code. Do not treat shared API endpoint names, standard JSON fields, common headings, generic Python control flow, or public service documentation as proof of copying.

### Phase A disposition

For each unresolved block, choose exactly one:

- `EXACT_PERMISSIVE_SOURCE_CONFIRMED`;
- `EXACT_EXISTING_PERMISSION_SOURCE_CONFIRMED`;
- `EXACT_NO_LICENSE_OR_INCOMPATIBLE_SOURCE_CONFIRMED`;
- `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH`.

If an exact permissively licensed source is confirmed, preserve the block only when all copyright and license obligations can be satisfied through a supplemental notice without changing the established mixed-license boundary. Create the notice artifacts authorized in Section 11.

If an exact no-license, incompatible, ambiguous, or still-unresolved source remains, proceed to the separated rewrite process below.

## 6. Phase B — behavior-contract capture

Before replacing any unresolved block, create a neutral behavior contract that describes only observable requirements and interfaces, not the old implementation's expression.

Create:

`build_week_2026/UNRESOLVED_BLOCK_BEHAVIOR_CONTRACT.md`

For each block record:

- accepted input types and required fields;
- output type and stable keys;
- expected error/fail-closed behavior;
- relevant CLI compatibility;
- ordering and determinism requirements;
- read-only/write behavior;
- network behavior and timeouts where applicable;
- privacy and no-private-path constraints;
- representative synthetic cases and expected outputs;
- behavior that may intentionally change for safety or licensing reasons.

Use synthetic, fictional, non-private examples only.

Capture golden behavior through tests before replacement. Tests may assert public interfaces and representative outputs, but must not copy large internal string blocks or implementation structure from an unresolved candidate source.

## 7. Phase C — separated independent rewrite process

Use role separation if Codex subagents are available.

### Behavior analyst role

The behavior analyst may read the current affected downstream blocks to produce the neutral contract and tests. It must not write replacement implementation.

### Implementation role

Use a separate implementation subagent/context when available. The implementation role:

- must receive only the neutral behavior contract, tests, public function signatures, allowed standard-library interfaces, official public API documentation, and the authorized template path/contract;
- must not open candidate third-party repositories or blobs;
- must not open the old unresolved line ranges after the contract is frozen;
- must not use the previous provenance reports as implementation guidance beyond the list of prohibited source candidates;
- must create materially new organization, naming, data structures, and control flow rather than paraphrasing the old block.

If true subagent/context separation is unavailable, stop with:

`CLEAN_REWRITE_SEPARATION_NOT_AVAILABLE`

Do not falsely claim a clean rewrite.

Create:

`build_week_2026/CLEAN_REWRITE_SEPARATION_RECORD.md`

Record roles, file-access boundaries, inputs supplied to the implementation role, prohibited sources, and whether the separation was successfully maintained. Do not publish private session IDs or transcripts.

## 8. Required rewrite architecture

### 8.1 Template-expression remediation

Do not duplicate the distinctive authorized template headings and prompts inside Python code.

Replace embedded template expression in `batch_import_collection.py` and `deep_read_collection.py` with a template-driven rendering boundary that reads the separately authorized installed/public template at runtime or through an explicitly supplied template path.

Preferred approach:

- add an independently authored repository-local renderer module under `skills/zotero-collection-manager/scripts/`;
- parse the authorized template as data;
- fill or replace defined sections through neutral section identifiers and values;
- preserve heading order from the template file itself;
- fail closed with a clear error if the template is missing or structurally invalid;
- do not include a copied full-template fallback in code;
- do not alter `templates/论文精读模板.md`.

A concise generic marker or section-mapping contract is allowed when independently authored. Do not copy the template's distinctive prose into Python tests beyond the minimum needed to verify parsing of the actual authorized template file.

### 8.2 Infer-helper remediation

Replace MSB-010 with an independently organized, data-driven classifier or other materially distinct implementation.

Preserve externally used function signatures only where compatibility requires them. Prefer neutral rule tables, normalized tokens, and a shared classification helper rather than the prior branch layout.

Use synthetic tests to verify representative outputs. Do not consult candidate implementations during the implementation role.

### 8.3 Generator-control remediation

Replace the unresolved generator logic in MSB-013 and MSB-017 with the new template-driven renderer and independently organized data preparation.

Preserve:

- output note format as defined by the authorized template;
- required frontmatter and evidence fields;
- deterministic ordering;
- existing dry-run/write/no-overwrite safety behavior;
- public placeholders rather than local private paths.

Do not rewrite unrelated extraction, logging, migration, or CLI blocks.

### 8.4 Online-metadata remediation

Replace MSB-026 through a new standard-library-only metadata client boundary built from official Crossref, OpenAlex, Unpaywall, DOI, and HTTP interface documentation rather than candidate GitHub code.

Preferred approach:

- one generic request/JSON helper;
- service-specific request builders and response normalizers;
- explicit timeout and user-agent behavior;
- deterministic title normalization/matching;
- fail-closed partial-result reporting;
- dependency injection or mocking boundary for offline tests;
- no external package dependency.

Do not run live network requests in tests. Use mocked HTTP responses containing synthetic metadata.

## 9. Tests and validation

Add focused standard-library `unittest` coverage. A repository workflow is not required in this gate.

At minimum test:

- all three infer-helper public functions on representative synthetic titles/abstracts;
- template-driven first-pass note generation;
- template-driven deep-read note generation;
- missing or malformed template failure;
- no distinctive template fallback text embedded in affected Python files;
- deterministic output on repeated runs;
- mocked Crossref success/failure;
- mocked OpenAlex success/failure;
- mocked Unpaywall success/failure;
- DOI cleanup and title matching;
- unknown/partial online metadata fail-closed behavior;
- existing CLI `--help` for all nine product scripts;
- AST parse for all product scripts;
- three `agents/openai.yaml` parse;
- prior privacy/secret/private-path scan;
- locked legal/permission file hash preservation;
- root README, Skills, template, and root LICENSE unchanged;
- `git diff --check`.

Run the previous nine safe `--help` checks and any new tests. Do not perform real Zotero operations, real vault writes, or live external API calls.

## 10. Post-rewrite provenance comparison

After implementation, compare the rewritten blocks against:

- the prior unresolved block text;
- every candidate source already listed in the accepted candidate manifest;
- any exact candidate found in Phase A.

The comparison is a review check only. The implementation role must not use candidate source text during creation.

Record:

- normalized line similarity;
- function/control-flow organization differences;
- distinctive long-string overlap;
- remaining copied-expression findings;
- whether only generic/API/interface overlap remains.

Any remaining non-generic copied expression from an unlicensed or unresolved source is a blocker.

## 11. Notice route when a permissive exact source is confirmed

Only when Phase A confirms an exact permissively licensed source and the affected block is retained, create:

- `THIRD_PARTY_SKILL_NOTICES.md`;
- required full license text under `third_party_licenses/`;
- a narrowly additive README link.

Preserve exact copyright and license notices. Do not alter the locked original permission files.

If no permissive retained block exists after rewrite, do not create empty notices.

## 12. Daily-use local comparison boundary

After all public tests pass, compare the rewritten public affected files against the corresponding authorized local daily-use files only to determine follow-up synchronization needs:

- `C:\Users\zcxve\.codex\skills\zotero-collection-manager\scripts\batch_import_collection.py`;
- `C:\Users\zcxve\.codex\skills\zotero-collection-manager\scripts\deep_read_collection.py`;
- `C:\Users\zcxve\.codex\skills\zotero-data-fetcher\scripts\zotero_fetch.py`.

Read-only comparison only. Do not modify local files in this gate.

Record whether a separate local-install synchronization gate is required. Do not copy machine-specific paths back into the public repository.

## 13. Required outputs

Always create:

1. `build_week_2026/UNRESOLVED_SOURCE_DISCOVERY_LOG.md`
2. `build_week_2026/UNRESOLVED_BLOCK_BEHAVIOR_CONTRACT.md`
3. `build_week_2026/CLEAN_REWRITE_SEPARATION_RECORD.md`
4. `build_week_2026/BLOCK_LEVEL_CLEAN_REWRITE_VALIDATION_REPORT.md`
5. `build_week_2026/POST_REWRITE_PROVENANCE_AND_RIGHTS_REPORT.md`
6. `build_week_2026/POST_REWRITE_SUBMISSION_READINESS_CHECKPOINT.md`

Update:

7. `build_week_2026/MULTI_SOURCE_SKILL_PROVENANCE_BLOCK_MANIFEST.csv`
8. `build_week_2026/MULTI_SOURCE_GITHUB_ORIGIN_CANDIDATE_MANIFEST.csv`
9. `build_week_2026/MULTI_SOURCE_LICENSE_AND_PERMISSION_ROUTE_MATRIX.md`
10. `build_week_2026/MULTI_SOURCE_PROVENANCE_READINESS_CHECKPOINT.md`

Product changes are limited to the affected scripts, a narrowly necessary new renderer/metadata helper module, and focused tests.

## 14. Locked and forbidden modifications

MUST NOT modify:

- `UPSTREAM_PERMISSION_FINAL.md`;
- `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- `THIRD_PARTY_NOTICES.md`;
- `LICENSE_SCOPE.md`;
- `ACKNOWLEDGEMENTS.md`;
- `FILE_MAPPING_AND_HASH_MANIFEST.md`;
- root `LICENSE`;
- the three `SKILL.md` files;
- `templates/论文精读模板.md`;
- the three `agents/openai.yaml` files;
- unrelated scripts;
- `origin/main`.

README may change only under the exact permissive-notice condition in Section 11.

MUST NOT:

- execute the superseded single-source permission task;
- contact any author;
- claim any new permission;
- use candidate source code as rewrite input;
- invoke OpenAI API or any model API;
- use `OPENAI_API_KEY`;
- access Zotero databases, PDFs, vaults, private research, credentials, private repositories, or the ScholarTrace branch;
- create a release, PR, deployment, video, Devpost submission, or hosted service;
- use wildcard staging;
- force-push;
- start the next gate automatically.

## 15. Commit and push

Commit and push only to:

`build-week-2026-skill-release-prep`

Use one focused implementation/remediation commit after all checks pass.

Suggested commit message:

`refactor: independently rewrite unresolved skill blocks`

Explicit-path staging only.

## 16. Verdicts

Full success with rewrite and no new retained permissive source:

`OPENAI_BUILD_WEEK_2026_UNRESOLVED_SOURCE_DISCOVERY_AND_BLOCK_LEVEL_CLEAN_REWRITE_COMPLETE`

Success with an exact permissive source retained and notices added:

`OPENAI_BUILD_WEEK_2026_UNRESOLVED_SOURCE_REMEDIATION_COMPLETE_NOTICES_ADDED`

Blocking verdicts:

- `CLEAN_REWRITE_SEPARATION_NOT_AVAILABLE`
- `BLOCKED_BY_REMAINING_UNRESOLVED_RIGHTS_OR_BEHAVIOR_REGRESSION`
- `BLOCKED_BY_REPOSITORY_STATE_OR_LOCKED_FILE_CHANGE`

The readiness checkpoint must conclude exactly one:

- `READY_FOR_LOCAL_INSTALL_SYNC_AND_FINAL_PROVENANCE_GATE`;
- `READY_AFTER_NOTICE_GPT_ACCEPTANCE`;
- `BLOCKED_PENDING_ADDITIONAL_RIGHTS_OR_REWRITE_REMEDIATION`.

Recommended next gate after GPT GitHub acceptance of a successful result:

`OPENAI_BUILD_WEEK_2026_POST_REWRITE_LOCAL_SYNC_AND_FINAL_PROVENANCE_GATE`

Do not start it automatically.

## 17. Final response requirements

Report:

- exact verdict and readiness;
- repository, branch, baselines, task-bearing HEAD, final commit and push;
- Phase A search count, queries/categories, candidates, pinned sources and licenses;
- disposition for MSB-010, MSB-012, MSB-013, MSB-016, MSB-017 and MSB-026;
- behavior contract and synthetic golden cases;
- role/context separation and exact prohibited-source controls;
- files created and modified;
- new module architecture;
- test commands, counts and exit codes;
- AST, `--help`, YAML, secret/privacy, locked-file and diff checks;
- post-rewrite similarity and copied-expression results;
- local/public affected-file comparison and whether local sync is required;
- exact staged paths;
- forbidden-operation check;
- final git status;
- recommended next gate.

Do not start the next gate automatically.
