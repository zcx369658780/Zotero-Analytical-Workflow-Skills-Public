# OpenAI Build Week 2026 — Daily Skill Bundle Sync, Privacy, and Release-Readiness Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-skill-release-prep`  
Task type: actual daily-use Skill bundle synchronization, privacy/security audit, and submission-readiness checkpoint

## 0. Authoritative product decision

The submission product is the user's real, daily-use Zotero + Codex + Obsidian Skill bundle stored in the public GitHub repository.

The submission is NOT an independently hosted application, SaaS, standalone GPT-5.6 API client, or ScholarTrace compilation project.

Do not merge, cherry-pick, copy, or depend on the experimental branch:

`build-week-2026-scholartrace`

Do not require or use `OPENAI_API_KEY`. Do not invoke the OpenAI API or any other model/API in this gate.

The actual bundle consists of:

1. `zotero-collection-manager`;
2. `zotero-data-fetcher`;
3. `zotero-analytical-writer`; and
4. the daily-use literature-reading template and the scripts bundled under those Skills.

The repository must represent what the user actually uses locally, subject to public-repository sanitization, licensing, privacy, no-secret, and no-private-data boundaries.

## 1. Accepted repository baseline

Accepted public main baseline with effective upstream permission and mixed-licensing notices:

`6c1c6caa93318f08cff666d94de26da42447ef59`

Protected pre-Build-Week baseline tag:

`pre-build-week-2026-public-baseline`

Required tag target:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

This branch must begin exactly from `6c1c6caa...`, plus only this governing task-file commit.

## 2. Mandatory local sources to inspect

Inspect only the following expected daily-use installation paths, read-only at first:

- `C:\Users\zcxve\.codex\skills\zotero-collection-manager\`
- `C:\Users\zcxve\.codex\skills\zotero-data-fetcher\`
- `C:\Users\zcxve\.codex\skills\zotero-analytical-writer\`
- `C:\Users\zcxve\.codex\templates\论文精读模板.md`

Also inspect the public checkout:

- `D:\Zotero-Analytical-Workflow-Skills-Public\`

Do not broadly search the filesystem. Do not inspect other `.codex` skills, private repositories, Zotero data directories, Obsidian vaults, ResearchVault, PDFs, databases, Downloads, browser data, credential stores, or research-data directories.

If an expected path is absent, record it as absent. Do not guess or search elsewhere.

## 3. Git and repository preflight

Before any file comparison or write:

1. run `git fetch origin --tags`;
2. confirm repository identity and accepted SSH/HTTPS origin;
3. confirm branch `build-week-2026-skill-release-prep`;
4. confirm the task-bearing start HEAD descends directly from `6c1c6caa...` and adds only this task file;
5. confirm `origin/main` remains at or contains `6c1c6caa...` and is not changed by this gate;
6. confirm the protected tag target;
7. run `git status --short --untracked-files=all`;
8. stop on unrelated tracked or untracked project changes.

Never use `git add .` or `git add -A`.

## 4. Phase A — Exact local/public Skill identity audit

Build a complete manifest for the expected daily-use files under the three local Skill directories and the one local template.

For every local file, record:

- local relative path;
- corresponding public-repository path, if any;
- file type;
- byte size;
- SHA256;
- UTF-8/text readability status;
- public counterpart existence;
- public counterpart SHA256;
- identity verdict:
  - `IDENTICAL`;
  - `LOCAL_NEWER_CANDIDATE`;
  - `PUBLIC_ONLY_PACKAGING`;
  - `LOCAL_ONLY_RUNTIME_OR_PRIVATE_EXCLUDED`;
  - `MISSING_LOCAL`;
  - `MISSING_PUBLIC`;
  - `REVIEW_REQUIRED`.

Expected public mappings include:

- local `zotero-collection-manager/**` -> public `skills/zotero-collection-manager/**`;
- local `zotero-data-fetcher/**` -> public `skills/zotero-data-fetcher/**`;
- local `zotero-analytical-writer/**` -> public `skills/zotero-analytical-writer/**`;
- local template -> public `templates/论文精读模板.md`.

Ignore only clearly generated/runtime artifacts such as:

- `__pycache__/`;
- `*.pyc`;
- temporary logs;
- `.bak` files;
- `.env`;
- SQLite files;
- PDFs;
- local reports and processing logs;
- user-specific cache files.

Do not silently ignore an unfamiliar file. Classify it.

## 5. Phase B — Privacy, credential, API, and public-safety audit

Audit both:

1. the current tracked public-repository tree on this branch; and
2. any local file proposed for synchronization.

Required checks:

### 5.1 Credential and token patterns

Search for actual or likely:

- OpenAI/API keys;
- GitHub tokens;
- bearer tokens;
- passwords;
- cookies;
- authorization headers;
- private keys;
- `.env` content;
- cloud credentials;
- database credentials.

Do not print a detected secret value. If a credible secret is found, record only file path, line number, category, and a redacted fingerprint. Stop before commit.

### 5.2 Private/local path exposure

Identify hardcoded or embedded user-specific paths, including:

- `C:\Users\zcxve`;
- `D:\ResearchVault`;
- `D:\ResearchData`;
- Zotero profile/data paths;
- private repository paths;
- private note/vault paths;
- personal Downloads/Desktop paths.

Public documentation may contain generic placeholders such as `<note_root>`, `<vault_root>`, `<zotero_data_dir>`, and `<workflow_root>`. Actual private paths must not be newly synchronized.

### 5.3 Personal and private information

Check for:

- private email addresses not intentionally approved for public project contact;
- phone numbers;
- private usernames/account identifiers;
- raw correspondence;
- unpublished personal information;
- private research-note content;
- Zotero item titles or annotations from the user's library;
- purchased or unpublished data excerpts.

### 5.4 Forbidden/binary artifacts

Ensure no tracked or proposed file includes:

- Zotero SQLite/databases;
- PDF attachments;
- Obsidian vault notes;
- raw or purchased data;
- model outputs;
- large binary/log/cache artifacts;
- screenshots containing private data;
- API response dumps.

### 5.5 Repository history review

Inspect reachable history for forbidden filenames and obvious secret/private-path indicators. Do not rewrite history in this gate.

If a historical issue is discovered, stop and report a separate remediation requirement.

## 6. Phase C — Bounded synchronization of actual daily-use Skills

Synchronization is authorized only for a local/public difference that meets ALL conditions:

1. the file belongs to one of the three expected daily-use Skill directories or the expected template;
2. it is plain text/source content needed for actual daily use;
3. it is user-created or already covered by the repository's established upstream permission and mixed-licensing boundary;
4. it contains no secret, private data, private note, raw research content, or prohibited path;
5. any machine-specific default can be safely replaced with an existing public placeholder without changing functional intent;
6. the resulting public file accurately represents the installed daily-use behavior;
7. the file does not introduce ScholarTrace, API adapter, independent API-key requirements, hosted-service behavior, deployment, or unrelated project functionality.

Allowed public synchronization targets are limited to:

- `skills/zotero-collection-manager/**`;
- `skills/zotero-data-fetcher/**`;
- `skills/zotero-analytical-writer/**`;
- `templates/论文精读模板.md`.

Do not modify a file merely to reformat it.

For the five separately licensed downstream counterpart files—`README.md`, three `SKILL.md` files, and the template—preserve the mixed-licensing treatment. Normal maintenance within this specified repository is permitted, but the files remain separately licensed and excluded from MIT.

### Stop conditions for synchronization

Do not synchronize a candidate if:

- authorship or licensing is uncertain;
- sanitization would materially change behavior and requires a product decision;
- the local version appears older than the public version;
- the local file includes private research content or actual user paths that cannot be safely generalized;
- the difference is an experimental or unused local file;
- it belongs to ScholarTrace/API work.

Record the candidate in the report instead.

## 7. Phase D — Actual-use and judge-path review

Without invoking a model or touching real Zotero/Obsidian data, verify that the public repository provides a truthful, usable path for a judge or user to understand and install the daily-use bundle.

Check:

- the three Skill directory structures;
- relative template references;
- referenced bundled scripts exist;
- README installation instructions match the public files;
- README clearly identifies Windows-oriented defaults/placeholders;
- dry-run/write/overwrite behavior is accurately described;
- upstream attribution and mixed licensing remain prominent;
- no API key is stated as required for normal use;
- no ScholarTrace/API adapter is presented as the product;
- repository default branch remains the intended submission branch after later merge.

Do not run real Zotero operations or write to a vault. Static checks and safe command-help/import checks are allowed only if they do not access local data.

## 8. Required outputs

Create:

1. `build_week_2026/DAILY_SKILL_BUNDLE_LOCAL_PUBLIC_IDENTITY_MANIFEST.csv`
2. `build_week_2026/DAILY_SKILL_BUNDLE_SYNC_AND_PRIVACY_AUDIT_REPORT.md`
3. `build_week_2026/PUBLIC_REPOSITORY_SECRET_AND_PRIVACY_SCAN_REPORT.md`
4. `build_week_2026/DAILY_SKILL_BUNDLE_SUBMISSION_READINESS_CHECKPOINT.md`

The readiness checkpoint must conclude exactly one:

- `READY_FOR_SUBMISSION_MATERIALS_GATE`
- `READY_AFTER_BOUNDED_SYNC_GPT_ACCEPTANCE`
- `BLOCKED_BY_LOCAL_PUBLIC_DRIFT`
- `BLOCKED_BY_PRIVACY_OR_SECRET_RISK`
- `BLOCKED_BY_LICENSING_OR_PROVENANCE_RISK`

It must distinguish:

- pre-existing functional Skills;
- competition-period licensing/public-release hardening;
- any competition-period synchronization of actual daily-use improvements;
- experimental ScholarTrace/API work that is explicitly excluded from the submission.

## 9. README boundary

The permission and copyright notices already exist on `main` and must remain.

In this gate, modify `README.md` only if required to correct a demonstrably false installation path, missing actual daily-use file, or false API requirement discovered by the audit.

Any README modification must preserve:

- upstream author and repository attribution;
- links to `UPSTREAM_PERMISSION_FINAL.md`, `THIRD_PARTY_NOTICES.md`, `LICENSE_SCOPE.md`, `ACKNOWLEDGEMENTS.md`, and `FILE_MAPPING_AND_HASH_MANIFEST.md`;
- explicit mixed-licensing language;
- the fact that public access does not make upstream-derived files MIT-licensed.

Do not add ScholarTrace or an API-key requirement.

## 10. GitHub and commit policy

If no safe synchronization or README correction is required, commit only the task and four audit/readiness outputs.

If bounded synchronization is required and passes every check, include only the exact approved Skill/template paths plus the four outputs.

Suggested commit message:

`chore: synchronize and audit public daily-use skill bundle`

Push only to:

`origin/build-week-2026-skill-release-prep`

Do not merge to or push `main` in this gate.

Use explicit-path staging only.

## 11. Forbidden operations

MUST NOT:

- use `OPENAI_API_KEY`;
- invoke OpenAI API or another model/API;
- modify, copy from, merge, or cherry-pick `build-week-2026-scholartrace`;
- add ScholarTrace, EvidenceGate, schemas, fixtures, API adapters, tests, or CLI product code;
- access Zotero databases, attachments, PDFs, annotations, or Local API;
- access or modify Obsidian/ResearchVault notes;
- access private research data or unpublished materials;
- modify the locked legal text in `UPSTREAM_PERMISSION_FINAL.md`, `THIRD_PARTY_NOTICES.md`, `LICENSE_SCOPE.md`, `ACKNOWLEDGEMENTS.md`, `FILE_MAPPING_AND_HASH_MANIFEST.md`, or `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- alter root `LICENSE`;
- publish private email evidence;
- create PR, release, deployment, Devpost submission, or video in this gate;
- rewrite Git history;
- delete branches;
- force-push;
- use wildcard staging;
- start the next gate automatically.

## 12. Required final response

Report:

- exact verdict;
- repository, branch, baseline, and task-bearing start HEAD;
- exact local paths inspected and existence status;
- local/public file counts;
- identity counts by verdict;
- each synchronized or intentionally excluded path;
- privacy/secret scan summary;
- historical-risk scan summary;
- licensing and attribution preservation result;
- actual-use/judge-path result;
- files written or modified;
- commands/checks and exit codes;
- exact staged paths;
- commit and push result;
- forbidden-operation check;
- final git status;
- readiness checkpoint verdict;
- recommended next gate.

Expected success verdict:

`OPENAI_BUILD_WEEK_2026_DAILY_SKILL_BUNDLE_SYNC_PRIVACY_AND_RELEASE_READINESS_COMPLETE`

Recommended next gate after GPT GitHub acceptance:

`OPENAI_BUILD_WEEK_2026_SUBMISSION_MATERIALS_AND_DEVPOST_PACKAGE_GATE`

End the session after this gate.