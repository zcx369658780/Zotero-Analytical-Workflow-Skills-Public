# OpenAI Build Week 2026 — Release Candidate Main Merge and Submission Materials Gate

Date: 2026-07-21  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Source branch: `build-week-2026-skill-release-prep`  
Target branch: `main`  
Task type: final release-candidate curation, judge-facing documentation, fast-forward main merge, and manual-submission package preparation

## 0. Goal and authoritative product decision

Prepare the real daily-use Zotero + Codex + Obsidian Skill bundle as the final OpenAI Build Week 2026 release candidate, merge the accepted release-preparation history to `main` by fast-forward only, and create complete English submission materials for the user's final manual YouTube and Devpost steps.

The submitted product is exactly the real daily-use Skill bundle:

1. `zotero-collection-manager`;
2. `zotero-data-fetcher`;
3. `zotero-analytical-writer`;
4. their bundled scripts and `agents/openai.yaml` metadata; and
5. `templates/论文精读模板.md`.

The product is NOT ScholarTrace, EvidenceGate, an independent OpenAI API client, a hosted application, SaaS, deployment, or standalone compilation project.

Normal use MUST NOT require `OPENAI_API_KEY`. GPT-5.6 is used through the user's Codex build and execution environment, not through an additional runtime API call in this submission.

Do not add new product functionality in this gate.

## 1. Accepted baselines

Accepted post-rewrite local synchronization and final provenance commit:

`bf82c8a4d82655fdd6b36534f4194456457df137`

Accepted clean-rewrite implementation commit:

`7bee5d5d7a5f7d8d625a483148993d4f4b8141bd`

Accepted public `main` permission and mixed-licensing baseline:

`6c1c6caa93318f08cff666d94de26da42447ef59`

Protected pre-Build-Week tag:

`pre-build-week-2026-public-baseline`

Required peeled target:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-bearing commit adding this file must immediately follow `bf82c8a4...` and add only this task file.

## 2. Official submission requirements and deadline

Use the official OpenAI Build Week / Devpost requirements as the governing external checklist:

- submission deadline: July 21, 2026 at 5:00 PM Pacific Daylight Time, equivalent to July 22, 2026 at 8:00 AM Asia/Singapore;
- project must be built with Codex and GPT-5.6;
- an existing project must clearly separate pre-existing work from meaningful work added during the submission period;
- choose exactly one track;
- include a text description of features and functionality;
- include a public YouTube demonstration video under three minutes, with audio explaining what was built and how Codex and GPT-5.6 were used;
- provide a repository URL for judging and testing;
- README must include setup instructions, testing guidance, and a clear account of Codex/GPT-5.6 collaboration;
- a Plugin or Developer Tool must state installation instructions, supported platforms, and a way for judges to test it without rebuilding from scratch;
- provide the `/feedback` Codex Session ID from the primary build thread in the Devpost submission form;
- submission materials must be English or include English translations;
- third-party content, trademarks, music, and integrations must be lawfully used.

This gate prepares materials but MUST NOT upload a YouTube video, enter a private Session ID into a public file, log in to Devpost, click final submission, or claim that submission is complete.

## 3. Repository and Git preflight

Before writing:

1. run `git fetch origin --tags`;
2. verify the exact repository and accepted SSH/HTTPS origin;
3. verify the current branch is `build-week-2026-skill-release-prep`;
4. verify the task-bearing start HEAD immediately follows `bf82c8a4...` and adds only this task file;
5. verify the working tree is clean;
6. verify `origin/main` remains exactly `6c1c6caa93318f08cff666d94de26da42447ef59` unless the user has separately authorized and documented a later accepted main commit;
7. verify the source branch is a strict descendant of `origin/main`, is not behind it, and can be fast-forwarded without merge conflict;
8. verify the protected tag peels to the required target;
9. stop if unrelated tracked or untracked changes exist.

Never use `git add .` or `git add -A`. Never force-push. Never use a non-fast-forward merge to `main`.

## 4. Required repository context

Read:

- `README.md`;
- the three `SKILL.md` files;
- the three `agents/openai.yaml` files;
- the public template;
- the final 12 product Python scripts/modules;
- `UPSTREAM_PERMISSION_FINAL.md`;
- `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- `THIRD_PARTY_NOTICES.md`;
- `LICENSE_SCOPE.md`;
- `ACKNOWLEDGEMENTS.md`;
- `FILE_MAPPING_AND_HASH_MANIFEST.md`;
- `build_week_2026/FINAL_DAILY_SKILL_BUNDLE_IDENTITY_AND_PROVENANCE_MANIFEST.csv`;
- `build_week_2026/FINAL_PROVENANCE_AND_RIGHTS_ACCEPTANCE_REPORT.md`;
- `build_week_2026/FINAL_SUBMISSION_READINESS_CHECKPOINT.md`;
- `build_week_2026/POST_REWRITE_PROVENANCE_AND_RIGHTS_REPORT.md`;
- `build_week_2026/CLEAN_REWRITE_SEPARATION_RECORD.md`;
- relevant Git history from the protected tag through the task-bearing HEAD.

Do not inspect private Zotero data, Obsidian vaults, PDFs, purchased/unpublished research data, credentials, browser data, private repositories, other local Skills, or the ScholarTrace experimental branch.

Do not invoke OpenAI API, another model API, or live scholarly metadata APIs.

## 5. Release-candidate tree curation

The final public working tree must be judge-friendly while retaining a transparent audit trail.

### 5.1 Keep product and legal files

Preserve:

- the complete real submission product;
- all existing effective permission, attribution, mixed-licensing, acknowledgement, and mapping files;
- final provenance/readiness records;
- tests needed for offline judge verification;
- the protected tag and Git history.

### 5.2 Build Week evidence index

Create:

`build_week_2026/README.md`

It must:

- explain that `build_week_2026/` is evidence and audit documentation, not a separate product;
- identify the final accepted product commit and final acceptance reports;
- distinguish current final evidence from historical intermediate/blocking reports;
- explain that intermediate reports are retained for transparency and are superseded by the final accepted reports where applicable;
- link the concise final evidence path first;
- state that ScholarTrace/API experiments were developed on a separate unmerged branch and are not part of this submission.

### 5.3 Remove task-specification clutter from the final working tree

After the task has been fully read and all required evidence is recorded, remove the following Build Week governing task files from the final working tree. Their commit history remains available and MUST NOT be rewritten:

- `tasks/openai_build_week_2026_upstream_permission_and_mixed_licensing_integration_gate.md`;
- `tasks/openai_build_week_2026_daily_skill_bundle_sync_privacy_and_release_readiness_gate.md`;
- `tasks/openai_build_week_2026_third_party_skill_provenance_and_license_audit_gate.md`;
- `tasks/openai_build_week_2026_upstream_permission_supplement_preparation_gate.md`;
- `tasks/openai_build_week_2026_multi_source_skill_provenance_reconstruction_gate.md`;
- `tasks/openai_build_week_2026_unresolved_source_discovery_and_block_level_clean_rewrite_gate.md`;
- `tasks/openai_build_week_2026_post_rewrite_local_sync_and_final_provenance_gate.md`;
- `tasks/openai_build_week_2026_release_candidate_main_merge_and_submission_materials_gate.md`.

Do not remove non-Build-Week project files. Do not rewrite history.

## 6. README release-candidate revision

Revise `README.md` as an English-first bilingual release-candidate README. Normal maintenance is authorized by the existing repository-limited permission, but README remains a separately licensed fixed counterpart and must retain the mixed-licensing boundary.

Required top-level structure:

1. project title and one-sentence English pitch;
2. concise English overview, followed by a shorter Chinese overview;
3. three-Skill architecture and data flow;
4. feature table;
5. installation instructions for Codex Skill directories and template placement;
6. supported platforms and prerequisites;
7. quick start and safe dry-run examples;
8. judge testing path without private Zotero or Obsidian data;
9. privacy, no-overwrite, evidence, and human-review safety model;
10. pre-existing work versus Build Week 2026 additions;
11. how Codex and GPT-5.6 were used;
12. repository structure;
13. upstream attribution and mixed licensing;
14. links to judge guide, Build Week evidence index, final provenance report, and submission materials.

README must accurately state:

- the core three Skills pre-existed Build Week;
- Build Week additions include permission/licensing integration, public/local synchronization, agent metadata, privacy and source audits, independent block-level rewrites, safety tests, final provenance acceptance, and release packaging;
- evaluation must not treat pre-existing capabilities as newly built during the submission period;
- normal use does not require a separate OpenAI API key;
- Codex with GPT-5.6 was used to plan, inspect, refactor, test, document, and safely synchronize the real Skill bundle;
- final semantic writing behavior occurs through Codex executing the Skills, while Python scripts provide deterministic extraction, queuing, rendering, safety gates, and metadata interoperability;
- no private Zotero database, PDF, Obsidian vault, credential, processing log, purchased data, or research note is included;
- public placeholders must be replaced by a user's own local paths;
- the repository is Windows-oriented and tested with CPython 3.11; other platforms may require path adjustments;
- the repository uses mixed licensing and the five fixed upstream-derived counterparts are separately licensed.

Do not add ScholarTrace, EvidenceGate, runtime Responses API, API-key setup, deployment, or hosted-service language.

## 7. Required submission-material files

Create directory `submission/` and these files:

### 7.1 `submission/DEVPOST_SUBMISSION_COPY.md`

English, ready to paste, containing:

- final project title: `Zotero Analytical Workflow Skills`;
- one-line tagline;
- recommended track: `Education`;
- project overview;
- problem and target users;
- what the project does;
- how the three Skills work together;
- privacy/safety design;
- what was pre-existing;
- what was meaningfully extended during Build Week;
- how Codex and GPT-5.6 were used;
- repository and testing instructions summary;
- third-party/licensing disclosure;
- limitations and supported environment;
- no claim that the submission or video is already live.

Do not fabricate metrics, users, awards, runtime API use, or deployment.

### 7.2 `submission/DEMO_VIDEO_SCRIPT_UNDER_3_MINUTES.md`

English voiceover plus shot list, targeted at 2:35–2:50 total duration.

The demo must show:

1. project/repository identity;
2. the three Skills and workflow architecture;
3. installation path and `agents/openai.yaml` discoverability;
4. a safe, synthetic/redacted explanation of the daily Zotero → Codex → Obsidian workflow;
5. default dry-run/no-overwrite and privacy protections;
6. offline tests and judge testing guide;
7. pre-existing versus Build Week additions;
8. how Codex and GPT-5.6 were used;
9. upstream attribution and mixed licensing;
10. final callout that no private research data is included.

Do not instruct the user to display private Zotero items, PDF content, vault paths, credentials, email, browser tabs, notifications, or local backup paths. Do not use copyrighted music. Product names may be referenced descriptively without logos implying endorsement.

### 7.3 `submission/JUDGE_TESTING_GUIDE.md`

English and executable without rebuilding from scratch. Include:

- supported environment;
- clone/download instructions;
- offline verification path that requires no Zotero database or Obsidian vault;
- `python -m unittest discover -s tests -v` and expected minimum `24/24`;
- AST/import and safe `--help` checks or a concise tested command sequence;
- how to inspect the three Skill files and agent metadata;
- optional full local trial using the judge's own Zotero/Obsidian data, with explicit privacy warnings and dry-run first;
- expected output behavior;
- no API key requirement;
- known Windows/path limitations;
- mixed-license links.

Do not include actual private paths. Use placeholders.

### 7.4 `submission/BUILD_WEEK_NEW_WORK_EVIDENCE.md`

English, with:

- protected pre-Build-Week tag and commit;
- accepted main permission baseline;
- final release-candidate commit placeholder to be filled after commit/merge by using Git history references rather than self-referential content where necessary;
- clear table of pre-existing capabilities versus submission-period additions;
- dated commit sequence summary;
- Codex/GPT-5.6 collaboration evidence categories;
- statement that the `/feedback` Session ID is retained privately and submitted only through Devpost;
- statement that experimental ScholarTrace/API work is excluded from `main` and the submission.

### 7.5 `submission/MANUAL_SUBMISSION_CHECKLIST.md`

English checklist for the user, containing:

- record or edit the public YouTube video under three minutes;
- verify audio and public visibility;
- run `/feedback` in the primary Codex build thread and privately retain the exact Session ID;
- do not put the Session ID in GitHub;
- open the Devpost submission page;
- choose Education;
- paste the prepared description;
- provide the public GitHub repository URL;
- provide the public YouTube URL;
- enter the private `/feedback` Session ID;
- verify all required fields;
- submit before July 21, 2026 5:00 PM PDT / July 22, 2026 8:00 AM Singapore;
- capture a private submission confirmation screenshot/receipt;
- do not add private confirmation evidence to the public repository.

Use visible placeholders for URLs and Session ID, never private values.

### 7.6 `submission/ASSET_PRIVACY_AND_COPYRIGHT_CHECKLIST.md`

English checklist covering:

- no credentials, private paths, Zotero items, annotations, PDFs, vault notes, emails, notifications, or purchased data in the video or repository;
- no copyrighted music or unlicensed images/screenshots;
- lawful descriptive use of product names;
- required upstream attribution and mixed-license links;
- YouTube visibility and audio check;
- no Session ID or private Devpost receipt in public assets.

## 8. Final release validation before commit

Run and require:

1. `python -m unittest discover -s tests -v`, minimum `24/24` pass;
2. AST parsing of all 12 product Python files;
3. safe `--help` checks for all nine public CLI scripts;
4. parse all three `agents/openai.yaml` files;
5. validate every Markdown link added to README and submission files;
6. validate README contains all required sections and no API-key requirement;
7. validate Devpost copy and video script are English and internally consistent;
8. verify video script timing estimate is under three minutes;
9. scan the complete proposed tree for credentials, private keys, authorization values, unredacted private paths, private contact details, Zotero item data, PDF/database/vault artifacts, and prohibited binaries;
10. verify the seven locked legal/permission files retain their accepted hashes;
11. verify the three Skill files and template remain unchanged except README, which may receive authorized maintenance;
12. verify no ScholarTrace or experimental API-adapter files are present in the source branch or proposed `main` tree;
13. verify the final product file set and tests match the accepted provenance manifest;
14. `git diff --check`;
15. exact staged-path review.

No live Zotero, Obsidian, scholarly metadata, OpenAI API, or model request is allowed.

## 9. Release-candidate commit on source branch

Create one focused release-candidate documentation/curation commit on `build-week-2026-skill-release-prep`.

Suggested commit message:

`docs: prepare Build Week release candidate and submission package`

Stage only explicit authorized paths:

- `README.md`;
- `build_week_2026/README.md`;
- the six required `submission/` files;
- exact task-file deletions listed in Section 5.3.

Do not restage unchanged product or legal files.

Push only to `origin/build-week-2026-skill-release-prep` first. Verify remote branch equality and clean status before touching `main`.

## 10. Fast-forward merge to main

Only after the release-candidate commit and all checks pass:

1. fetch origin again;
2. verify `origin/main` is still the accepted pre-merge commit;
3. verify the source branch is strictly ahead and not behind;
4. switch to local `main` with a clean working tree;
5. fast-forward local `main` to `origin/main` if necessary;
6. merge `origin/build-week-2026-skill-release-prep` using `--ff-only`;
7. re-run the complete final validation on the resulting local `main` tree;
8. push `main` normally without force;
9. verify GitHub `main`, local `main`, and final release-candidate commit are identical;
10. create and push one annotated tag:

`openai-build-week-2026-submission-rc1`

The tag must point to the final `main` commit. Do not move or recreate the tag if it already exists; stop and report.

Do not create a GitHub Release in this gate.

## 11. Final post-merge evidence

Create no additional self-referential metadata-only commit after merging.

The exact final commit SHA, push result, tag object/peeled target, final tests, and final status must be recorded in the Codex gate response and Git history. Submission documents may say “see `main` and tag `openai-build-week-2026-submission-rc1`” rather than trying to embed the commit's own SHA inside itself.

Final required repository state:

- default branch remains `main`;
- `origin/main` equals the final release-candidate commit;
- source branch may remain for audit history;
- working tree and index are clean;
- protected pre-Build-Week tag remains unchanged;
- submission RC tag points to final `main`;
- no ScholarTrace/API experiment is merged;
- no private `/feedback` Session ID, YouTube draft URL, or Devpost receipt is committed.

## 12. Forbidden operations

Do not:

- add product functionality;
- merge or copy anything from `build-week-2026-scholartrace`;
- use `OPENAI_API_KEY`;
- invoke OpenAI API, another model API, or live metadata services;
- access real Zotero/Obsidian/private research content;
- modify the effective permission or locked legal/notice files;
- weaken attribution or mixed licensing;
- upload YouTube video;
- log in to or submit through Devpost;
- publish the `/feedback` Session ID;
- create a GitHub Release;
- use wildcard staging;
- use `git add .` or `git add -A`;
- create a merge commit;
- rebase or rewrite published history;
- force-push;
- delete protected tags;
- start another gate automatically.

## 13. Verdicts

Full success:

`OPENAI_BUILD_WEEK_2026_RELEASE_CANDIDATE_MAIN_MERGE_AND_SUBMISSION_MATERIALS_COMPLETE`

Readiness:

`READY_FOR_MANUAL_VIDEO_UPLOAD_FEEDBACK_ID_AND_DEVPOST_SUBMISSION`

Blocking verdicts:

- `BLOCKED_BY_RELEASE_CANDIDATE_VALIDATION_FAILURE`
- `BLOCKED_BY_MAIN_DIVERGENCE_OR_NON_FAST_FORWARD_STATE`
- `BLOCKED_BY_SUBMISSION_MATERIAL_PRIVACY_OR_LICENSE_FINDING`
- `BLOCKED_BY_SUBMISSION_RC_TAG_CONFLICT`
- `BLOCKED_BY_DEADLINE_OR_REQUIRED_MANUAL_ASSET_UNAVAILABILITY`

## 14. Required final response

Report:

- exact verdict and readiness;
- repository, source branch, target branch, accepted baseline, task-bearing HEAD, release-candidate commit, and final main commit;
- official deadline in PDT and Singapore time;
- README changes and final structure;
- submission files created;
- pre-existing versus Build Week contribution summary;
- recommended track and rationale;
- complete validation commands, counts, and exit codes;
- privacy, credential, copyright, provenance, and locked-file checks;
- exact staged paths and deleted task paths;
- source-branch commit and push result;
- fast-forward merge and main push result;
- submission RC tag object and peeled target;
- confirmation that ScholarTrace/API experiments were not merged;
- final Git status;
- exact remaining manual actions: record/upload public YouTube video, run `/feedback`, privately retain Session ID, complete Devpost form, and submit before deadline;
- reminder not to put the Session ID or private submission receipt in the public repository.

Do not claim that the project has been submitted until the user manually confirms Devpost submission.