# OpenAI Build Week 2026 — Multi-Source Skill Provenance Reconstruction Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-skill-release-prep`  
Task type: provenance reconstruction before any additional permission request or submission work

## 0. Authoritative correction and supersession

The user has provided an authoritative provenance correction:

> Eternity Chen can grant permission only for files originating from
> `cheneternity/Zotero-Analytical-Workflow-Skills`. Other Skill material was
> gradually found and added by Codex from other GitHub repositories during
> real use.

Therefore:

1. `tasks/openai_build_week_2026_upstream_permission_supplement_preparation_gate.md`
   is **superseded before execution**;
2. do not prepare, send, or activate any supplemental permission request yet;
3. do not assume the three currently reported blockers all belong to Eternity
   Chen merely because similar historical files exist in that repository;
4. reconstruct the actual source chain for every externally derived part of the
   submission bundle before deciding which author, license, notice, rewrite, or
   permission route applies;
5. no author may be asked to authorize material outside that author's own
   repository or rights.

The superseded task file remains in Git history as an audit record. Do not
execute it and do not delete or rewrite history in this gate.

## 1. Goal

Reconstruct, as far as reasonably possible from repository evidence and public
fixed-version GitHub evidence, the actual multi-source provenance of the real
daily-use Zotero + Codex + Obsidian Skill bundle.

The submission product remains only:

- `skills/zotero-collection-manager/`;
- `skills/zotero-data-fetcher/`;
- `skills/zotero-analytical-writer/`;
- their bundled scripts and `agents/openai.yaml` metadata; and
- `templates/论文精读模板.md`.

This gate must determine, for every material code, Skill-instruction, template,
prompt, metadata, or helper block:

- whether it is independently authored;
- whether it came from Eternity Chen's repository;
- whether it came from another public GitHub Skill/repository;
- whether it is only a generic/common implementation pattern;
- whether its origin remains unresolved;
- what exact license or permission route applies.

Do not add product functionality. Do not prepare submission materials.

## 2. Accepted baseline

Accepted third-party provenance-audit commit:

`2d4f81014e656f07ae6d22297a3785f8a0f55926`

Superseded supplemental-permission task commit:

`763c0c14f5854fe373e7d1113e36ccbf66b003cd`

Accepted daily-use synchronization commit:

`521ef5d60c8b695a6b5c7bfa930511f0fdedf92a`

Accepted public `main` permission baseline:

`6c1c6caa93318f08cff666d94de26da42447ef59`

Protected pre-Build-Week baseline tag:

`pre-build-week-2026-public-baseline`

Required tag target:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-bearing commit adding this file must immediately follow `763c0c14...`
and add only this governing task file.

## 3. Repository preflight

Before provenance work:

1. run `git fetch origin --tags`;
2. verify the exact public repository and accepted SSH/HTTPS origin;
3. verify branch `build-week-2026-skill-release-prep`;
4. verify the task-bearing start HEAD immediately follows `763c0c14...` and
   adds only this task file;
5. verify `origin/main` remains at or contains `6c1c6caa...` and is not modified;
6. verify the protected tag target;
7. verify the working tree is clean;
8. stop on unrelated tracked or untracked project changes.

Use explicit-path staging only. Never use `git add .` or `git add -A`. Never
force-push.

## 4. Authorized evidence scope

Inspect:

- the complete tracked submission-product tree;
- reachable Git history, commit messages, task files, reports, and deleted or
  renamed files relevant to the product;
- the four already authorized local daily-use paths, read-only:
  - `C:\Users\zcxve\.codex\skills\zotero-collection-manager\`;
  - `C:\Users\zcxve\.codex\skills\zotero-data-fetcher\`;
  - `C:\Users\zcxve\.codex\skills\zotero-analytical-writer\`;
  - `C:\Users\zcxve\.codex\templates\论文精读模板.md`;
- public GitHub search and fixed-version file reads needed to identify candidate
  source repositories and licenses.

Do not inspect:

- unrelated local `.codex` Skills;
- private repositories;
- Zotero databases, attachments, or annotations;
- Obsidian vaults or private notes;
- PDFs, research data, Downloads, browser data, credential stores, or unrelated
  directories;
- the ScholarTrace/API experimental branch.

Do not download or execute untrusted third-party code. Prefer GitHub code search,
GitHub API, raw fixed-version file reads, `git log`, `git blame`, `git show`,
`git -S`, `git -G`, and normalized offline comparisons.

## 5. Phase A — Reconstruct candidate source families

For each of the 16 submission-product files, identify coherent blocks that may
have different origins. Do not treat a whole file as single-source when evidence
suggests mixed authorship.

Search for:

- exact and near-exact distinctive function names;
- distinctive ordered headings, prompt text, return strings, data-field names,
  comments, help text, and error wording;
- GitHub URLs, repository names, authors, copyright headers, SPDX markers, and
  source comments;
- historical commit messages or task reports naming source Skills;
- structural similarity that combines multiple non-generic choices;
- earlier local/public versions that reveal when a block appeared;
- exact phrases from `agents/openai.yaml` that may originate from published
  Skill conventions;
- source-specific tests, schemas, naming conventions, or helper patterns.

Use public GitHub exact-string/code search for distinctive fragments. For each
credible candidate repository, pin the exact candidate commit/tag/path/blob.

Do not infer copying from:

- standard Python library use;
- generic CLI patterns;
- common `argparse`, JSON, CSV, HTTP, SQLite, Markdown, or YAML idioms;
- product/API names;
- generic research-workflow concepts;
- short common phrases lacking distinctive expression.

## 6. Phase B — Re-evaluate prior TP-006, TP-007, and TP-008

The prior audit findings are evidence inputs, not final source ownership
conclusions.

For each:

### TP-006

Re-evaluate the source of `infer_theme`, `infer_methodology`, and
`infer_core_variable` in
`skills/zotero-collection-manager/scripts/batch_import_collection.py`.

Determine whether the best-supported source is:

- Eternity Chen's historical pilot script;
- another GitHub Skill/repository;
- multiple sources;
- independent implementation after generic conceptual exposure; or
- unresolved.

### TP-007

Re-evaluate the embedded note/template expression in:

- `skills/zotero-collection-manager/scripts/batch_import_collection.py`;
- `skills/zotero-collection-manager/scripts/deep_read_collection.py`.

Determine which expression derives from the already authorized Eternity Chen
template and whether any additional headings/prompts came from other GitHub
Skills.

### TP-008

Re-evaluate the historical regeneration-script relationship. Do not ask
Eternity Chen to authorize this relationship unless the evidence supports that
his repository is the actual source.

For every re-evaluated item, report:

- prior conclusion;
- new evidence;
- revised or retained classification;
- actual likely source owner/repository;
- confidence;
- permission/license route.

## 7. Phase C — License and permission routing by actual source

For every identified external source:

1. pin exact repository, commit/tag, path, and blob SHA;
2. read the actual applicable `LICENSE`, `COPYING`, `NOTICE`, or per-file header
   at that fixed version;
3. record author/copyright notice;
4. verify the license applies to the specific source file;
5. classify the required route:
   - `EXISTING_ETERNITY_PERMISSION_COVERS`;
   - `ETERNITY_SUPPLEMENT_NEEDED`;
   - `PERMISSIVE_LICENSE_NOTICE_NEEDED`;
   - `OTHER_AUTHOR_PERMISSION_NEEDED`;
   - `INDEPENDENT_REWRITE_NEEDED`;
   - `REFERENCE_ONLY_NO_PERMISSION_NEEDED`;
   - `CONCEPTUAL_ONLY_ACKNOWLEDGEMENT`;
   - `UNRESOLVED_SOURCE_BLOCKER`.

No author may be assigned responsibility for another repository's material.

Apply conservative rules:

- MIT/BSD/ISC: preserve exact copyright and license notice;
- Apache-2.0: preserve license and applicable NOTICE/modification statements;
- GPL/AGPL/LGPL/MPL/other reciprocal terms: flag for separate compatibility
  review before submission;
- no license or ambiguous custom terms: copied/adapted expression remains a
  blocker unless the actual author grants permission or the content is removed
  and independently rewritten;
- public GitHub availability alone grants no redistribution license.

## 8. Phase D — Source-completeness challenge

Because the user knows Codex added material from multiple GitHub sources, a
negative result requires stronger evidence than the prior audit.

Before declaring no additional source:

- run exact-string searches on multiple distinctive fragments per material
  block;
- inspect relevant commit/task history for provenance clues;
- compare at least the strongest plausible candidate repositories;
- document search queries and result counts;
- identify what evidence remains unavailable;
- assign confidence honestly.

Do not claim certainty where only absence of search results exists.

## 9. Required outputs

Create:

1. `build_week_2026/MULTI_SOURCE_SKILL_PROVENANCE_BLOCK_MANIFEST.csv`
2. `build_week_2026/MULTI_SOURCE_GITHUB_ORIGIN_CANDIDATE_MANIFEST.csv`
3. `build_week_2026/MULTI_SOURCE_LICENSE_AND_PERMISSION_ROUTE_MATRIX.md`
4. `build_week_2026/MULTI_SOURCE_PROVENANCE_RECONSTRUCTION_REPORT.md`
5. `build_week_2026/MULTI_SOURCE_PROVENANCE_READINESS_CHECKPOINT.md`
6. `build_week_2026/SUPERSEDED_PERMISSION_SUPPLEMENT_TASK_RECORD.md`

The supersession record must state that
`tasks/openai_build_week_2026_upstream_permission_supplement_preparation_gate.md`
was not executed because its single-source assumption was corrected by the
user before execution.

Do not create an author email, permission draft, license notice, README change,
or code rewrite in this gate.

## 10. Validation

At minimum verify:

- every submission-product file/block has a provenance row;
- every external candidate has a pinned source or explicit unresolved status;
- every claimed license has a fixed-version license source;
- every permission route maps to the actual source owner;
- TP-006, TP-007, and TP-008 each have a documented re-evaluation;
- duplicate candidate and block IDs are zero;
- CSV files parse and required columns exist;
- all nine Python scripts still pass AST parsing and safe `--help` checks;
- all three `agents/openai.yaml` parse;
- prior privacy/secret scan remains clean for proposed additions;
- locked legal/permission files remain byte-identical;
- README, Skills, template, and product code remain unchanged;
- `git diff --check` passes;
- staged paths are exactly the six required documents.

## 11. Forbidden operations

Do not:

- execute the superseded supplement-preparation task;
- contact or draft an email to any author;
- claim any new permission is effective;
- modify product code, README, Skills, template, root LICENSE, or existing legal
  and notice files;
- add license notices before the actual source is established;
- invoke OpenAI API or another model/API;
- access private data or unrelated local Skills;
- merge or push `main`;
- create a PR, release, deployment, video, Devpost submission, or hosted service;
- use wildcard staging;
- force-push;
- start the next gate automatically.

## 12. Verdicts

Success with actionable source routing:

`OPENAI_BUILD_WEEK_2026_MULTI_SOURCE_SKILL_PROVENANCE_RECONSTRUCTION_COMPLETE`

Blocking verdict when material source remains insufficiently traceable:

`BLOCKED_BY_UNRESOLVED_MULTI_SOURCE_PROVENANCE`

Repository-state blocker:

`MULTI_SOURCE_PROVENANCE_RECONSTRUCTION_BLOCKED_BY_REPOSITORY_STATE`

The readiness checkpoint must conclude exactly one:

- `READY_FOR_SOURCE_SPECIFIC_RIGHTS_REMEDIATION_GATE`;
- `BLOCKED_PENDING_ADDITIONAL_SOURCE_DISCOVERY`.

No submission-material gate is allowed until source-specific rights remediation
is completed and accepted.

## 13. Commit and push

Commit and push only to:

`build-week-2026-skill-release-prep`

Suggested commit message:

`docs: reconstruct multi-source Skill provenance`

Use explicit-path staging only. End the session after this gate.
