# OpenAI Build Week 2026 — Upstream Permission and Mixed-Licensing Integration Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Task type: authorization-record and repository-notice integration only

## 0. Governing status

The upstream author has provided the required final written confirmation for:

- filename: `UPSTREAM_PERMISSION_FINAL.md`;
- document date: `2026-07-20`;
- SHA256: `0384E8256235C3371FFDD1EA0E017571AABD2B78D66C51FD60661EC6DE797E3E`;
- applicable downstream repository baseline commit:
  `e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`.

The downstream repository owner, GitHub user `zcx369658780`, has subsequently sent the exact written acceptance required by Section 10 and committed to comply with the same final document.

Therefore the limited upstream permission is effective for the specified repository, subject to all scope, attribution, MIT-boundary, maintenance, breach, and notice requirements in the final permission document.

This task records that effective permission in the repository. It does not adjudicate general OpenAI Build Week eligibility and does not start the Build Week product implementation.

## 1. Baseline and preflight

The pre-task public repository baseline is:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-file commit added after that baseline is expected and must be identified separately.

Before writing anything, Codex MUST:

1. run `git fetch origin`;
2. record current branch, current HEAD, `origin/main`, and the task-bearing commit;
3. run `git status --short --untracked-files=all`;
4. verify there are no unrelated tracked modifications;
5. compare the current task-bearing start HEAD against baseline commit `e76fb0bb...`;
6. verify that any post-baseline repository change before execution is limited to this task file;
7. stop if unrelated tracked changes or unexpected remote divergence exist.

Do not use `git add .` or `git add -A`.

## 2. Required source package

Use the exact locally supplied authorization package:

`OPENAI_BUILD_WEEK_FINAL_AUTHORIZATION_REVIEW_PACKAGE_2026_07_20.zip`

Expected ZIP SHA256:

`0ED30019BBD6C8671875CACAC23E72B7285954B4963700D81B3443427117E450`

Codex MAY search read-only for this exact filename only in:

1. the repository root;
2. the repository parent directory;
3. the current user's `Downloads` directory; or
4. a path supplied through environment variable `BUILD_WEEK_AUTH_PACKAGE`.

Do not perform a broad filesystem search.

If the exact ZIP cannot be found or its SHA256 does not match, stop with:

`AUTHORIZATION_SOURCE_PACKAGE_NOT_FOUND_OR_HASH_MISMATCH`

Do not recreate the legal texts from memory, chat history, summaries, or approximate wording.

Extract the ZIP only to a new task-specific temporary or staging directory outside any Zotero database, Obsidian vault, or private research-data directory. No overwrite is allowed.

## 3. Authoritative files and hashes

The following package files are authoritative and MUST be copied byte-for-byte to the repository root:

| Repository path | Required SHA256 |
|---|---|
| `UPSTREAM_PERMISSION_FINAL.md` | `0384E8256235C3371FFDD1EA0E017571AABD2B78D66C51FD60661EC6DE797E3E` |
| `THIRD_PARTY_NOTICES.md` | `903891E34649319AED4CFEAFBE1AA9A5CEFED75D37C085FEABD731AAC04794DE` |
| `LICENSE_SCOPE.md` | `477355A9687EE1F21DA857D0E18DCBEA3155F5808C2811E7D490001FC80F3941` |
| `ACKNOWLEDGEMENTS.md` | `94841D8676F034A7B16616AD3B3748777BE84EF15A47050EBB855125AB908B31` |
| `FILE_MAPPING_AND_HASH_MANIFEST.md` | `CE5CCF071AADC70E09D895058D14A0841959A9C801763B6D26AC1F6F09D111D3` |

Before copying, verify every source-file hash. After copying, verify every repository-file hash again.

The exact legal text of the first four files MUST NOT be edited, reformatted, normalized, translated, line-wrapped, or regenerated.

`FILE_MAPPING_AND_HASH_MANIFEST.md` also MUST be copied unchanged in this gate.

## 4. Required repository baseline identity verification

Verify that commit `e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e` contains the following downstream counterpart paths and blob identities:

| Downstream counterpart path | Required baseline Git blob SHA |
|---|---|
| `README.md` | `6ecfec2a87919f18f9eb8be077339747646b330d` |
| `skills/zotero-collection-manager/SKILL.md` | `5826dacff6fe382295c8d34520b707a50a5713a1` |
| `skills/zotero-data-fetcher/SKILL.md` | `31ade3273b9e179c996e4ae7e6be51b9494ddc92` |
| `skills/zotero-analytical-writer/SKILL.md` | `2a68954ae627981a5859661288f6506762d02979` |
| `templates/论文精读模板.md` | `25216c059b007719847a69dd228c82dc89238cfb` |

Also verify that `FILE_MAPPING_AND_HASH_MANIFEST.md` contains the same upstream/downstream mapping and baseline commit.

The three Skill files and the template MUST remain byte-identical to the current task start in this gate.

`README.md` is the only one of the five downstream counterparts authorized for a bounded update in this task.

## 5. Required README update

Update `README.md` conservatively. Preserve the existing project description, commands, structure, and acknowledgements already present.

Add a clearly visible section titled substantially:

`## Upstream attribution and mixed licensing`

The new README section MUST state all of the following:

1. the project adapts and extends `cheneternity/Zotero-Analytical-Workflow-Skills`;
2. the upstream author is Eternity Chen / GitHub `cheneternity`;
3. five fixed upstream file versions and their downstream counterparts are governed by `UPSTREAM_PERMISSION_FINAL.md`;
4. those complete downstream counterpart files are separately licensed and excluded from the downstream MIT License;
5. independently created downstream content may be MIT-licensed only where the repository owner has the right to do so;
6. readers must consult:
   - `UPSTREAM_PERMISSION_FINAL.md`;
   - `THIRD_PARTY_NOTICES.md`;
   - `LICENSE_SCOPE.md`;
   - `ACKNOWLEDGEMENTS.md`; and
   - `FILE_MAPPING_AND_HASH_MANIFEST.md`;
7. public repository access does not make the separately licensed upstream-derived materials MIT-licensed.

The README MUST retain prominent upstream attribution after the update.

Do not claim that the upstream repository, five files, or their identifiable adaptations are MIT-licensed.

Do not include the upstream author's email address, legal name from private correspondence, private-message content, screenshots, or raw email text.

## 6. Public confirmation record

Create:

`UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`

This new file MUST be a sanitized public record only. It MUST include:

- specified repository;
- final permission filename, date, SHA256, and baseline commit;
- public Licensor identity: Eternity Chen / GitHub `cheneternity`;
- public Licensee identity: GitHub `zcx369658780`;
- statement that the Licensor confirmed the exact final document in writing;
- statement that the Licensee subsequently accepted and committed to comply with the same exact document;
- statement that the permission became effective after both confirmations;
- hashes of `THIRD_PARTY_NOTICES.md`, `LICENSE_SCOPE.md`, and `ACKNOWLEDGEMENTS.md`;
- a statement that original email evidence is retained privately and is not published in the repository;
- a placeholder for the final notice-files integration commit, to be replaced before commit once the commit strategy is resolved.

Do not quote full private emails. Do not include email addresses or unpublished personal identifiers.

Because a commit cannot contain its own final commit SHA in advance, use this two-step rule:

1. In the committed confirmation record, write:
   `Notice-files integration commit: recorded in the completion report and Git history.`
2. Record the actual final commit SHA in the completion report after commit.

Do not amend or create a second metadata-only commit solely to insert a self-referential commit SHA unless explicitly required by a later task.

## 7. Build Week baseline tag

Check whether the tag below already exists locally or remotely:

`pre-build-week-2026-public-baseline`

If it does not exist, create an annotated tag pointing exactly to:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

Suggested annotation:

`Pre-Build-Week public repository baseline before permission notices and 2026 competition additions.`

If the tag exists, verify it points to the exact baseline commit and do not recreate it.

Push the tag only if this task reaches the commit-and-push stage successfully.

Stop if the existing tag points elsewhere.

## 8. Completion report

Create:

`build_week_2026/UPSTREAM_PERMISSION_AND_MIXED_LICENSING_INTEGRATION_REPORT.md`

The report MUST include:

- task title and date;
- repository and branch;
- pre-task baseline commit;
- task-bearing start HEAD;
- source ZIP path used and ZIP SHA256;
- source-file and repository-file SHA256 verification table;
- five upstream/downstream mapping verification result;
- README change summary;
- confirmation-record privacy check;
- whether `LICENSE` was unchanged;
- whether the three Skill files and template were unchanged;
- baseline-tag status and target;
- exact staged file list;
- commit hash;
- push result;
- final HEAD and `origin/main`;
- final `git status --short --untracked-files=all`;
- forbidden-operation check;
- known caveats;
- recommended next gate.

Do not place raw email contents in the report.

## 9. Allowed operations

This task explicitly authorizes only:

- repository and Git preflight checks;
- read-only lookup of the exact source ZIP in the bounded locations listed above;
- SHA256 and Git blob identity checks;
- extraction to a new staging directory;
- creation of the five authoritative root files listed in Section 3;
- bounded modification of `README.md` for mandatory attribution and mixed-license disclosure;
- creation of `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- creation of the completion report;
- creation or verification of the one baseline tag;
- explicit-path staging;
- one focused commit;
- push of that commit to `origin/main`;
- push of the baseline tag if newly created.

Suggested commit message:

`docs: integrate upstream permission and mixed licensing notices`

## 10. Forbidden operations

Codex MUST NOT:

- start ScholarTrace, EvidenceGate, Claim–Evidence Map, or other Build Week feature implementation;
- modify any Python script, test, schema, template, or Skill file;
- modify the root `LICENSE` text;
- rename or relocate the five downstream counterpart files;
- alter any legal-text byte in the four final legal/notice files;
- copy private email messages, email addresses, screenshots, or unpublished personal identities into GitHub;
- upload the ZIP package itself;
- upload `REPLY_EMAIL_TO_AUTHOR.md`, `BILATERAL_CONFIRMATION_TEXT.md`, or private correspondence;
- access or modify Zotero SQLite, Zotero attachments, PDFs, Obsidian vaults, ResearchVault, or private research data;
- introduce external paper content, Xiaohongshu screenshots, or copyrighted sample material;
- modify another repository;
- create a release, Devpost submission, YouTube upload, deployment, or production service;
- use `git add .` or `git add -A`;
- force-push;
- overwrite an existing tag that points elsewhere.

## 11. Required checks

At minimum run:

1. source ZIP SHA256 verification;
2. source-file SHA256 verification for all five authoritative files;
3. post-copy SHA256 verification for all five repository files;
4. `git cat-file` or equivalent baseline blob verification for the five downstream counterparts;
5. exact check that the three Skill files and template have no diff;
6. exact check that root `LICENSE` has no diff;
7. search for accidental email addresses, raw private-email phrases, secrets, tokens, SQLite, PDF, or private local paths in staged changes;
8. verify README contains mandatory attribution and links to all five notice/manifest files;
9. verify `THIRD_PARTY_NOTICES.md` and `LICENSE_SCOPE.md` contain the five downstream counterpart paths;
10. verify `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md` contains no private email address or full private correspondence;
11. inspect staged diff before commit;
12. explicit staged-file list before commit;
13. final clean-status check after push.

## 12. Expected staged paths

The intended staged paths are exactly:

- `README.md`
- `UPSTREAM_PERMISSION_FINAL.md`
- `THIRD_PARTY_NOTICES.md`
- `LICENSE_SCOPE.md`
- `ACKNOWLEDGEMENTS.md`
- `FILE_MAPPING_AND_HASH_MANIFEST.md`
- `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`
- `build_week_2026/UPSTREAM_PERMISSION_AND_MIXED_LICENSING_INTEGRATION_REPORT.md`

The task file itself is already present in the task-bearing start commit and should not be restaged unless it is unexpectedly uncommitted locally.

Stop if any unrelated path would be staged.

## 13. Expected verdict

On complete success, report exactly:

`OPENAI_BUILD_WEEK_2026_UPSTREAM_PERMISSION_AND_MIXED_LICENSING_INTEGRATION_COMPLETE`

If the source package or hashes fail:

`AUTHORIZATION_SOURCE_PACKAGE_NOT_FOUND_OR_HASH_MISMATCH`

If repository preflight or scope is unsafe:

`UPSTREAM_PERMISSION_INTEGRATION_BLOCKED_BY_REPOSITORY_STATE`

## 14. Acceptance level and next gate

Codex should self-report local evidence and commit/push status, but must not claim GPT GitHub acceptance.

Expected next GPT acceptance target:

`GITHUB_ACCEPTANCE_L3_COMMIT_OR_PR_VERIFIED`

Only after GPT verifies the repository files, commit diff, tag target, and required notices should the next task be created:

`OPENAI_BUILD_WEEK_2026_PUBLIC_REPO_BASELINE_AND_SCHOLARTRACE_SCOPE_GATE`

End the Codex session after this gate. Do not auto-start the next task.