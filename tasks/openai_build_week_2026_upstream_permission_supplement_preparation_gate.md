# OpenAI Build Week 2026 — Upstream Permission Supplement Preparation Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-skill-release-prep`  
Task type: exact supplemental-permission drafting and author-contact package preparation

## 0. Goal

Prepare, but do not send and do not activate, a narrowly scoped written-permission supplement that resolves the three blockers recorded in:

- `build_week_2026/THIRD_PARTY_SKILL_LICENSE_AUDIT_REPORT.md`;
- `build_week_2026/THIRD_PARTY_SKILL_PROVENANCE_MANIFEST.csv`;
- `build_week_2026/THIRD_PARTY_NOTICE_ACTION_MATRIX.md`;
- `build_week_2026/THIRD_PARTY_PROVENANCE_READINESS_CHECKPOINT.md`.

The preferred remediation is a supplemental written permission from Eternity Chen / GitHub `cheneternity`, because:

1. the identified upstream historical scripts have no public repository license;
2. the existing effective permission covers five fixed files but not the historical scripts or the two affected downstream Python files;
3. the affected Python files are part of the user's real daily-use Skill bundle;
4. hurried replacement would change production behavior and would not provide a strong clean-room record after prior source inspection; and
5. a narrow addendum can resolve all identified blockers without expanding the product or changing daily-use code.

This gate MUST NOT modify any product code, existing legal/permission file, README, Skill, template, or submission material. It only prepares an exact review package for the user to send manually to the author.

## 1. Accepted baseline and findings

Accepted provenance-audit commit:

`2d4f81014e656f07ae6d22297a3785f8a0f55926`

Accepted daily-use synchronization commit:

`521ef5d60c8b695a6b5c7bfa930511f0fdedf92a`

Accepted public `main` permission baseline:

`6c1c6caa93318f08cff666d94de26da42447ef59`

Protected pre-Build-Week baseline tag:

`pre-build-week-2026-public-baseline`

Required tag target:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-bearing commit that adds this file must immediately follow `2d4f810...` and add only this governing task file.

The supplement must address exactly these unresolved relationships:

### A. Historical pilot script

- upstream repository: `cheneternity/Zotero-Analytical-Workflow-Skills`;
- upstream commit: `0888dc1a2e941979cf73d4575b89a40a5db22dd7`;
- upstream path: `scripts/zotero_collection_manager_v2_pilot.py`;
- upstream Git blob: `ada0f997c60e9baaf0fa74130bae9769badb3e33`;
- affected downstream path: `skills/zotero-collection-manager/scripts/batch_import_collection.py`;
- current downstream Git blob at accepted provenance-audit commit: `e4de17dd8bfce5310feb941b0f4882b98da2bf45`.

### B. Historical regeneration script

- upstream repository: `cheneternity/Zotero-Analytical-Workflow-Skills`;
- upstream commit: `0888dc1a2e941979cf73d4575b89a40a5db22dd7`;
- upstream path: `scripts/regenerate_template_notes.py`;
- upstream Git blob: `35ec0f85774488ada298116c31b4a7d1dfe0227f`;
- affected downstream note-generation paths:
  - `skills/zotero-collection-manager/scripts/batch_import_collection.py`, blob `e4de17dd8bfce5310feb941b0f4882b98da2bf45`;
  - `skills/zotero-collection-manager/scripts/deep_read_collection.py`, blob `21b81dd14ef0bc72c2ca73b08efec68586ebc34f`.

### C. Template expression embedded in downstream scripts

Existing authorized upstream template:

- upstream commit: `81c624d37a114028dd49c63764694e30e5be13d4`;
- upstream path: `templates/论文精读模板.md`;
- upstream Git blob: `ee49e315d9e7a51a00bc256013e98f8713e82e58`.

Existing permission covers the complete downstream template counterpart but does not clearly cover identifiable template expression embedded in the two downstream scripts. The supplement must expressly clarify and authorize that use within the specified repository and specified downstream paths.

## 2. Repository preflight

Before drafting:

1. run `git fetch origin --tags`;
2. verify the exact public repository and accepted SSH/HTTPS origin;
3. verify branch `build-week-2026-skill-release-prep`;
4. verify the task-bearing start HEAD immediately follows `2d4f810...` and adds only this task file;
5. verify `origin/main` remains at or contains `6c1c6caa...` and is not modified;
6. verify the protected tag target;
7. verify the working tree is clean;
8. stop on unrelated tracked or untracked project changes.

Use explicit-path staging only. Never use `git add .` or `git add -A`. Never force-push.

## 3. Required context

Read only the repository files needed to draft the supplement:

- `UPSTREAM_PERMISSION_FINAL.md`;
- `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- `THIRD_PARTY_NOTICES.md`;
- `LICENSE_SCOPE.md`;
- `ACKNOWLEDGEMENTS.md`;
- `FILE_MAPPING_AND_HASH_MANIFEST.md`;
- `build_week_2026/THIRD_PARTY_SKILL_LICENSE_AUDIT_REPORT.md`;
- `build_week_2026/THIRD_PARTY_SKILL_PROVENANCE_MANIFEST.csv`;
- `build_week_2026/THIRD_PARTY_NOTICE_ACTION_MATRIX.md`;
- `build_week_2026/THIRD_PARTY_PROVENANCE_READINESS_CHECKPOINT.md`.

Fixed-version public GitHub reads are allowed only to re-confirm the listed upstream commits, paths, and blobs. Do not inspect new unrelated sources. Do not access private correspondence, Zotero, Obsidian, PDFs, research content, credentials, other repositories, or the ScholarTrace branch.

## 4. Required supplement scope

Draft `UPSTREAM_PERMISSION_SUPPLEMENT_DRAFT.md` as a standalone supplement to, not a replacement for, `UPSTREAM_PERMISSION_FINAL.md`.

The draft must:

1. identify the existing permission document by filename, date, SHA256, repository, and original baseline commit;
2. state that all original limitations and requirements remain effective except where the supplement expressly adds fixed materials and downstream paths;
3. identify the two historical upstream script paths, fixed commit, and blob SHAs exactly;
4. identify the two affected downstream Python paths and current blob SHAs exactly;
5. expressly authorize, within the same specified public repository, reproduction, modification, adaptation, maintenance, public distribution, release inclusion, testing, demonstration, and OpenAI Build Week submission use of:
   - the two fixed historical upstream script versions;
   - their identifiable adaptations in the specified downstream Python files;
   - identifiable expression from the already authorized template when embedded in the two specified downstream Python files;
6. cover normal future maintenance of the two specified downstream Python files within this repository, subject to attribution and license-boundary requirements;
7. remain non-exclusive, worldwide, and royalty-free;
8. remain repository-limited and not automatically extend to other repositories, products, services, or separately distributed projects;
9. clarify that the two complete downstream Python files, to the extent they contain identifiable upstream expression, are separately licensed and excluded from downstream MIT unless a future written separation is confirmed;
10. require preservation of attribution and supplemental notice in README plus a new supplemental notice file after effectiveness;
11. retain the same breach, cure, prospective-termination, ownership, no-endorsement, responsibility, and third-party-rights boundaries as the original permission;
12. state that the supplement becomes effective only after exact written confirmation by the Licensor and subsequent exact acceptance by the Licensee;
13. provide exact suggested confirmation text for both parties, naming the supplement filename, date, SHA256, repository, original permission SHA256, and accepted downstream baseline commit;
14. avoid private legal names, email addresses, private correspondence, and unpublished identifiers; use only public identities Eternity Chen / GitHub `cheneternity` and GitHub `zcx369658780`;
15. state clearly that this is a draft pending exact bilateral written confirmation.

Do not claim that the author owns rights beyond what the author is authorized to license. Use the same conservative ownership qualifier as the original permission.

## 5. Exact baseline for the supplement

Use the accepted provenance-audit commit as the downstream supplement baseline:

`2d4f81014e656f07ae6d22297a3785f8a0f55926`

Record that product-code blobs at this baseline are:

- `skills/zotero-collection-manager/scripts/batch_import_collection.py`:
  `e4de17dd8bfce5310feb941b0f4882b98da2bf45`;
- `skills/zotero-collection-manager/scripts/deep_read_collection.py`:
  `21b81dd14ef0bc72c2ca73b08efec68586ebc34f`.

The supplement must not silently authorize unrelated files or future repositories.

## 6. Required author-contact package

Create:

1. `build_week_2026/UPSTREAM_PERMISSION_SUPPLEMENT_DRAFT.md`
2. `build_week_2026/UPSTREAM_PERMISSION_SUPPLEMENT_MAPPING_AND_HASH_MANIFEST.md`
3. `build_week_2026/UPSTREAM_PERMISSION_SUPPLEMENT_AUTHOR_REVIEW_EMAIL.md`
4. `build_week_2026/UPSTREAM_PERMISSION_SUPPLEMENT_BILATERAL_CONFIRMATION_TEXT.md`
5. `build_week_2026/UPSTREAM_PERMISSION_SUPPLEMENT_PREPARATION_REPORT.md`

The author-review email must be concise, respectful, and explain:

- the prior permission remains appreciated and unchanged;
- a later fixed-version provenance audit found two historical scripts and template expression embedded in two downstream scripts outside the original five-file mapping;
- the public upstream repository has no license at those fixed versions;
- the requested supplement is narrow, repository-limited, and intended only to close those identified path-scope gaps;
- no additional repository, product, commercial service, or unrelated source is requested;
- the author should review the attached exact draft and, only if accurate, reply with the exact Licensor confirmation text;
- the author may request corrections instead of confirming.

The bilateral-confirmation file must contain separate exact text for:

- Licensor confirmation; and
- subsequent Licensee acceptance.

Do not send email. Do not create a Gmail draft. The user will review and manually send the package after GPT acceptance.

## 7. Hashing and package

After all five files are finalized:

1. compute SHA256 and byte size for each file;
2. place those values in the mapping/hash manifest and preparation report;
3. re-compute all hashes after the manifest is finalized;
4. if a manifest self-reference is impossible, exclude the manifest's own hash from its body and record it in the preparation report/final response;
5. create a ZIP in a task-specific temporary directory or repository-external location named:
   `OPENAI_BUILD_WEEK_UPSTREAM_PERMISSION_SUPPLEMENT_REVIEW_PACKAGE_2026_07_20.zip`;
6. include only the five required files;
7. compute the ZIP SHA256;
8. do not add or stage the ZIP in Git;
9. do not include private email evidence or the previous private correspondence.

The draft supplement must remain byte-stable after its SHA256 is presented for author review. Any author-requested textual change requires a new hash and another exact review cycle.

## 8. Validation

At minimum verify:

- every listed upstream path, commit, and blob exists;
- both downstream paths and blobs match baseline `2d4f810...`;
- original permission filename/date/SHA256/baseline references are exact;
- the supplement does not alter or contradict the original five-file permission;
- all three blockers TP-006, TP-007, and TP-008 are expressly addressed;
- no unrelated upstream or downstream path is added;
- no private identity, email address, credential, private path, or correspondence appears;
- the ZIP contains exactly five files;
- all reported hashes re-compute;
- all locked repository files remain byte-identical;
- README and product code remain unchanged;
- `git diff --check` passes;
- staged paths are exactly the five repository documents plus the preparation report if the report is among those five as specified above.

## 9. Forbidden operations

Do not:

- claim the supplement is effective;
- send or draft an email in Gmail;
- modify product code, README, existing permission/notice files, Skills, template, or root LICENSE;
- access private correspondence or private author identity details;
- invoke a model/API;
- access Zotero, Obsidian, PDFs, research data, credentials, or other repositories;
- inspect or use the ScholarTrace branch;
- merge or push `main`;
- create a PR, release, deployment, video, or submission;
- stage the ZIP;
- use wildcard staging;
- force-push;
- start the next gate automatically.

## 10. Commit and push

Commit and push only the five required repository documents to:

`build-week-2026-skill-release-prep`

Suggested commit message:

`docs: prepare upstream permission supplement review package`

Use explicit-path staging only.

## 11. Verdicts

Success verdict:

`OPENAI_BUILD_WEEK_2026_UPSTREAM_PERMISSION_SUPPLEMENT_PREPARATION_COMPLETE`

Blocking verdicts:

- `SUPPLEMENT_SCOPE_OR_FIXED_VERSION_VERIFICATION_FAILED`
- `SUPPLEMENT_PACKAGE_PRIVACY_OR_HASH_VALIDATION_FAILED`
- `SUPPLEMENT_PREPARATION_BLOCKED_BY_REPOSITORY_STATE`

Readiness after success:

`AWAITING_AUTHOR_SUPPLEMENT_CONFIRMATION`

Recommended next step is a human action, not an automatic Codex gate:

1. GPT verifies the preparation commit and package;
2. user sends the exact author-review email and attached draft/package;
3. author confirms or requests changes;
4. user returns the exact response to GPT;
5. only after author confirmation and user acceptance may a repository-integration and blocker-clearance gate be created.

## 12. Final report

Report:

- verdict and readiness;
- repository, branch, accepted baseline, task-bearing HEAD, final commit, push, and status;
- exact original permission identity;
- all upstream and downstream fixed mappings;
- how TP-006, TP-007, and TP-008 are addressed;
- files created;
- each file's SHA256 and byte size;
- ZIP path, contents, byte size, and SHA256;
- validation commands and exit codes;
- privacy and locked-file checks;
- exact staged paths;
- forbidden-operation check;
- next human action.

Do not start another task.