# OpenAI Build Week 2026 — Post-Rewrite Local Install Sync and Final Provenance Gate

Date: 2026-07-21  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-skill-release-prep`  
Task type: bounded local Skill installation update, backup/rollback evidence, final public/local identity audit, and final provenance acceptance

## 0. Goal and authoritative product boundary

Safely install the accepted, independently rewritten public implementation into the user's real daily-use Codex Skill installation, verify that the local installation remains functional and contains no superseded unresolved-source code, and issue the final provenance/readiness decision before release-candidate merge and submission-material preparation.

The submission product remains only the real daily-use Zotero + Codex + Obsidian Skill bundle:

1. `zotero-collection-manager`;
2. `zotero-data-fetcher`;
3. `zotero-analytical-writer`;
4. their bundled scripts and `agents/openai.yaml` metadata; and
5. `templates/论文精读模板.md`.

This gate does not authorize new product functionality, ScholarTrace, an API adapter, a hosted service, deployment, submission, video production, or a model/API invocation.

## 1. Accepted baselines

Accepted clean-rewrite implementation commit:

`7bee5d5d7a5f7d8d625a483148993d4f4b8141bd`

Accepted multi-source provenance reconstruction commit:

`1a9b18981f3c4ddaf864064822ac94e50fa21760`

Accepted daily-use synchronization commit:

`521ef5d60c8b695a6b5c7bfa930511f0fdedf92a`

Accepted public `main` permission baseline:

`6c1c6caa93318f08cff666d94de26da42447ef59`

Protected pre-Build-Week tag:

`pre-build-week-2026-public-baseline`

Required peeled target:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-bearing commit adding this file must immediately follow `7bee5d5d...` and add only this governing task file.

## 2. Governing safety rules

Read and follow:

- `project_rules/PROJECT_RULE_INDEX_CURRENT.md` if present;
- `project_rules/PROJECT_RULE_LOCAL_FILE_SAFETY_CURRENT.md` if present;
- `project_rules/PROJECT_RULE_CODEX_GITHUB_WORKFLOW_CURRENT.md` if present;
- `project_rules/PROJECT_RULE_ACCEPTANCE_LEVELS_CURRENT.md` if present;
- otherwise use the corresponding project rules supplied in the current project context.

Local paths are read-only unless this task expressly authorizes a specific write below. Authorization to write one path does not authorize another path.

No-overwrite is the default. This task authorizes replacement of only the exact local target files in Section 5, and only after a verified task-specific backup and pre-write checks pass.

## 3. Git and repository preflight

Before reading or writing local Skill files:

1. run `git fetch origin --tags`;
2. verify the exact repository and accepted SSH/HTTPS origin;
3. verify branch `build-week-2026-skill-release-prep`;
4. verify the task-bearing start HEAD immediately follows `7bee5d5d...` and adds only this task file;
5. verify `origin/main` remains at or contains `6c1c6caa...` and is not modified by this gate;
6. verify the protected tag peels to the required target;
7. run `git status --short --untracked-files=all`;
8. stop if unrelated tracked or untracked project changes exist.

Never use `git add .` or `git add -A`. Never force-push.

## 4. Required repository context

Read before local synchronization:

- `build_week_2026/UNRESOLVED_BLOCK_BEHAVIOR_CONTRACT.md`;
- `build_week_2026/CLEAN_REWRITE_SEPARATION_RECORD.md`;
- `build_week_2026/BLOCK_LEVEL_CLEAN_REWRITE_VALIDATION_REPORT.md`;
- `build_week_2026/POST_REWRITE_PROVENANCE_AND_RIGHTS_REPORT.md`;
- `build_week_2026/POST_REWRITE_SUBMISSION_READINESS_CHECKPOINT.md`;
- `build_week_2026/MULTI_SOURCE_SKILL_PROVENANCE_BLOCK_MANIFEST.csv`;
- `build_week_2026/MULTI_SOURCE_GITHUB_ORIGIN_CANDIDATE_MANIFEST.csv`;
- `build_week_2026/MULTI_SOURCE_LICENSE_AND_PERMISSION_ROUTE_MATRIX.md`;
- the six public source files named in Section 5;
- the public template `templates/论文精读模板.md`;
- the existing upstream permission and mixed-licensing notice files only as needed for hash preservation.

Do not reopen candidate third-party repositories or historical unlicensed source blobs. Provenance discovery and clean rewrite are complete. This gate verifies the accepted result; it does not resume source research.

## 5. Exact authorized local paths and write scope

The only local installation root paths authorized for inspection and bounded write are:

### Collection-manager scripts

- `C:\Users\zcxve\.codex\skills\zotero-collection-manager\scripts\batch_import_collection.py`
- `C:\Users\zcxve\.codex\skills\zotero-collection-manager\scripts\deep_read_collection.py`
- `C:\Users\zcxve\.codex\skills\zotero-collection-manager\scripts\classification.py`
- `C:\Users\zcxve\.codex\skills\zotero-collection-manager\scripts\template_renderer.py`

### Data-fetcher scripts

- `C:\Users\zcxve\.codex\skills\zotero-data-fetcher\scripts\zotero_fetch.py`
- `C:\Users\zcxve\.codex\skills\zotero-data-fetcher\scripts\metadata_client.py`

The corresponding accepted public sources are:

- `skills/zotero-collection-manager/scripts/batch_import_collection.py`
- `skills/zotero-collection-manager/scripts/deep_read_collection.py`
- `skills/zotero-collection-manager/scripts/classification.py`
- `skills/zotero-collection-manager/scripts/template_renderer.py`
- `skills/zotero-data-fetcher/scripts/zotero_fetch.py`
- `skills/zotero-data-fetcher/scripts/metadata_client.py`

This task authorizes creating the three helper modules locally if absent and replacing the three existing affected scripts only after backup.

Do not modify any other `.codex` Skill, template, agent metadata, local configuration file, cache, log, project rule, or repository.

Do not modify:

- any local `SKILL.md`;
- any local `agents/openai.yaml`;
- `C:\Users\zcxve\.codex\templates\论文精读模板.md`;
- any `__pycache__` or `.pyc` file;
- any Zotero, Obsidian, ResearchVault, PDF, database, research-data, credential, browser, Downloads, or private-repository path.

## 6. Phase A — Pre-write local/public manifest and configuration-drift decision

For all six target paths:

1. record existence, byte size, SHA256, UTF-8 readability, and AST status when present;
2. record the accepted public source size and SHA256;
3. classify the pre-write local state as one of:
   - `IDENTICAL_TO_ACCEPTED_PUBLIC`;
   - `EXPECTED_PRE_REWRITE_LOCAL_VERSION`;
   - `ABSENT_EXPECTED_NEW_HELPER`;
   - `LOCAL_CONFIGURATION_OVERLAY_PRESENT`;
   - `UNEXPECTED_LOCAL_CONTENT_REVIEW_REQUIRED`.

For the three existing local scripts, compare against both:

- the accepted public clean-rewrite version; and
- the pre-rewrite public version at task baseline `1a9b1898...` or the recorded prior local hash where available.

Determine whether the local file contains configuration-only differences needed for real daily use, such as private machine paths, local collection names, or defaults. Do not copy any old unresolved function body, renderer body, online-metadata body, template expression, or candidate-source expression into the new implementation.

Preferred outcome: install the accepted public files byte-for-byte.

A local-only configuration overlay is allowed only if ALL conditions hold:

1. it is outside the rewritten functional blocks;
2. it consists only of literal configuration/default values or local path/name constants;
3. it is necessary for the user's existing daily-use behavior;
4. it contains no credential or private research content;
5. it does not reintroduce template expression or unresolved code;
6. it is listed line-by-line in the report;
7. the resulting local file passes the full local verification in Section 9.

If an unexpected local helper file already exists with content different from the accepted public helper, stop before modifying that file and return the repository-state blocking verdict.

## 7. Phase B — Task-specific backup and rollback package

Before any local write, create one new timestamped backup directory outside the repository under:

`C:\Users\zcxve\.codex\skill_sync_backups\openai_build_week_2026_post_rewrite_<YYYYMMDD_HHMMSS>\`

The directory must not already exist.

Back up every existing target file while preserving its relative Skill path. Do not back up absent files as empty placeholders; record them as absent in the manifest.

Create in the backup directory:

- `LOCAL_INSTALL_PREWRITE_BACKUP_MANIFEST.csv`;
- `RESTORE_INSTRUCTIONS.md`.

The backup manifest must record:

- source local path;
- backup path;
- existence before write;
- byte size;
- SHA256;
- backup SHA256;
- verification result;
- intended post-write source path;
- whether rollback would restore or remove the target.

Verify every backup byte-for-byte before continuing.

Do not delete the backup directory after success. Do not stage or commit backup contents.

## 8. Phase C — Atomic local synchronization

For each authorized target:

1. prepare the final local content in a task-specific temporary file;
2. run UTF-8, AST, forbidden-string, private-data, and unresolved-block checks on the temporary file;
3. verify the expected destination parent directory;
4. write atomically using temporary-file replacement where supported;
5. re-read the destination and verify final SHA256;
6. stop immediately on any mismatch.

When no local overlay is required, the installed local SHA256 must equal the accepted public SHA256.

When an approved configuration-only overlay is required, record:

- accepted public SHA256;
- final local SHA256;
- exact changed lines or keys;
- reason;
- proof that no rewritten block or protected expression differs.

Do not create an overwrite switch or generalized synchronization tool. This is a one-time bounded installation update.

## 9. Phase D — Local functional and safety verification

After all six files are synchronized, run without accessing real Zotero or Obsidian data:

### Repository tests

- `python -m unittest discover -s tests -v` from the public checkout;
- require at least the previously accepted 24 tests to pass.

### Public source checks

- AST parse all twelve public product Python files;
- safe `--help` checks for the nine public CLI scripts;
- parse all three public `agents/openai.yaml` files;
- `git diff --check`.

### Local installation checks

- AST parse the six synchronized local target files;
- import `classification.py`, `template_renderer.py`, and `metadata_client.py` from their local installed paths using an isolated import harness;
- run safe `--help` for the three synchronized local entry scripts:
  - `batch_import_collection.py`;
  - `deep_read_collection.py`;
  - `zotero_fetch.py`;
- run a task-specific synthetic local-install harness that exercises:
  - all preserved classifier labels and precedence;
  - runtime template parsing against the authorized local template path, read-only;
  - fail-closed behavior for a missing/malformed temporary synthetic template;
  - mocked Crossref/OpenAlex/Unpaywall responses with no network;
  - no unresolved old functions, embedded template headings, or old metadata-helper bodies.

The local template may be read only for structure/hash validation. Do not modify it and do not generate or write a real Obsidian note.

No live Zotero Local API, SQLite, Crossref, OpenAlex, Unpaywall, DOI resolver, network, model, or OpenAI API request is allowed.

If public tests pass but local installed verification fails, restore all modified local targets from the verified backup, remove only newly created helper targets that were absent before write, verify rollback hashes, and return the rollback verdict.

## 10. Phase E — Final provenance, identity, and privacy acceptance

Rebuild a final manifest covering the complete daily-use submission product:

- three `SKILL.md` files;
- three `agents/openai.yaml` files;
- twelve Python scripts after the three helper additions;
- `templates/论文精读模板.md`.

For every file record:

- public path and Git blob/SHA256;
- local path and SHA256 where installed;
- identity status;
- local-overlay status;
- license/provenance route;
- privacy status;
- submission inclusion status.

Final allowed identity states:

- `IDENTICAL_PUBLIC_AND_LOCAL`;
- `SANITIZED_PUBLIC_LOCAL_CONFIGURATION_OVERLAY`;
- `PUBLIC_ONLY_AUDIT_OR_PACKAGING_FILE`;
- `SEPARATELY_LICENSED_FIXED_COUNTERPART`.

No product file may remain `MISSING_LOCAL`, `MISSING_PUBLIC`, `UNRESOLVED_SOURCE_BLOCKER`, `NO_LICENSE_FOUND`, `INCOMPATIBLE_LICENSE`, or `REVIEW_REQUIRED`.

Reconfirm:

- the five fixed Eternity Chen counterparts remain under the existing written permission;
- no historical-script expression or unresolved candidate expression remains in the rewritten product code;
- authorized template expression exists only in the separately licensed template file and is loaded as runtime data;
- all other product scripts are independently rewritten, generic implementation, platform/API interoperability, or repository-local engineering as recorded;
- no supplemental permission or new third-party notice is required;
- no credential, API key, private key, email, phone number, private research content, Zotero item data, annotation, PDF, database, vault content, or prohibited binary is present in tracked submission files;
- local private path/configuration values, if retained locally, do not appear in the public repository or committed reports except as approved redacted placeholders.

Do not include actual private local configuration values in committed reports. Describe overlays by category and redacted location only.

## 11. Required repository outputs

Create:

1. `build_week_2026/POST_REWRITE_LOCAL_INSTALL_SYNC_MANIFEST.csv`
2. `build_week_2026/POST_REWRITE_LOCAL_INSTALL_SYNC_REPORT.md`
3. `build_week_2026/FINAL_DAILY_SKILL_BUNDLE_IDENTITY_AND_PROVENANCE_MANIFEST.csv`
4. `build_week_2026/FINAL_PROVENANCE_AND_RIGHTS_ACCEPTANCE_REPORT.md`
5. `build_week_2026/FINAL_SUBMISSION_READINESS_CHECKPOINT.md`

Do not commit the backup manifest or restore instructions from the private backup directory. The repository report may record only the backup directory category, creation status, file count, and manifest hash; do not publish the full private path if it exposes more than the already authorized user profile path, and do not publish private configuration values.

The final readiness checkpoint must conclude exactly one:

- `READY_FOR_RELEASE_CANDIDATE_MAIN_MERGE_AND_SUBMISSION_MATERIALS_GATE`;
- `BLOCKED_BY_LOCAL_INSTALL_SYNC_OR_FUNCTIONAL_REGRESSION`;
- `BLOCKED_BY_FINAL_PROVENANCE_OR_PRIVACY_FINDING`.

## 12. Locked and forbidden modifications

MUST NOT modify repository product or legal files in this gate, including:

- `README.md`;
- `UPSTREAM_PERMISSION_FINAL.md`;
- `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- `THIRD_PARTY_NOTICES.md`;
- `LICENSE_SCOPE.md`;
- `ACKNOWLEDGEMENTS.md`;
- `FILE_MAPPING_AND_HASH_MANIFEST.md`;
- root `LICENSE`;
- all three repository `SKILL.md` files;
- repository `templates/论文精读模板.md`;
- all repository product Python files;
- all three repository `agents/openai.yaml` files;
- prior audit reports and manifests except where the task explicitly requires a new final output rather than rewriting history.

MUST NOT:

- access real Zotero data, SQLite, attachments, annotations, or PDFs;
- access or modify an Obsidian vault or ResearchVault;
- access research data, private repositories, Downloads, browser data, credential stores, or unrelated `.codex` Skills;
- use or require `OPENAI_API_KEY`;
- invoke OpenAI API, another model/API, or live scholarly metadata services;
- inspect candidate third-party source code again;
- modify or push `main`;
- create a PR, release, deployment, video, Devpost submission, or hosted service;
- delete the backup directory;
- use wildcard staging;
- force-push;
- start the next gate automatically.

## 13. Validation and staging

At minimum validate:

- all five required output files parse/read successfully;
- both CSVs have required columns and unique IDs/paths;
- complete 19-file product coverage: three Skills + three agents + twelve scripts + one template;
- all final routes are non-blocking;
- local/public target hashes and overlay classifications are internally consistent;
- backup manifest hash is recorded and backup verification succeeded;
- no private configuration value appears in committed outputs;
- all locked repository files remain byte-identical;
- repository product code remains byte-identical to `7bee5d5d...`;
- secret/private-path/privacy scan passes;
- `git diff --check` passes;
- staged paths are exactly the five required repository outputs.

Use explicit-path staging only.

## 14. Commit and push

Commit and push only to:

`build-week-2026-skill-release-prep`

Suggested commit message:

`chore: sync local Skill install and finalize provenance`

One focused commit only. Do not modify or push `main`.

## 15. Verdicts

Full success:

`OPENAI_BUILD_WEEK_2026_POST_REWRITE_LOCAL_SYNC_AND_FINAL_PROVENANCE_COMPLETE`

Local synchronization or verification failed but rollback completed and verified:

`LOCAL_INSTALL_SYNC_FAILED_ROLLBACK_COMPLETE`

Unexpected local content or backup/preflight blocker before write:

`LOCAL_INSTALL_SYNC_BLOCKED_BY_UNEXPECTED_LOCAL_STATE`

Final provenance or privacy blocker:

`BLOCKED_BY_FINAL_PROVENANCE_OR_PRIVACY_FINDING`

Repository-state blocker:

`POST_REWRITE_LOCAL_SYNC_BLOCKED_BY_REPOSITORY_STATE`

Only full success may recommend:

`OPENAI_BUILD_WEEK_2026_RELEASE_CANDIDATE_MAIN_MERGE_AND_SUBMISSION_MATERIALS_GATE`

End the session after this gate. Do not start the next gate automatically.

## 16. Final response requirements

Report:

- exact verdict and readiness checkpoint;
- repository, branch, accepted baseline, task-bearing HEAD, final commit and push;
- exact authorized local targets inspected;
- pre-write local/public classifications and hashes;
- configuration-overlay decision without publishing private values;
- backup directory category, backed-up file count, backup-manifest hash, and verification result;
- every local file created or replaced;
- final local/public identity status for all six targets;
- repository tests, AST, `--help`, YAML, synthetic local harness, no-network, and rollback checks with exit codes;
- final 19-file identity/provenance summary;
- remaining third-party rights, license, or notice findings;
- privacy, credential, private-path, and prohibited-artifact results;
- locked-file and repository-product hash preservation;
- exact repository files created;
- exact staged paths;
- commit and push result;
- forbidden-operation check;
- final local and Git status;
- recommended next gate.
