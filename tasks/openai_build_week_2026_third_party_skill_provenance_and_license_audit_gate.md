# OpenAI Build Week 2026 — Third-Party Skill Provenance and License Audit Gate

Date: 2026-07-20  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Branch: `build-week-2026-skill-release-prep`  
Task type: source-provenance, third-party Skill reference, dependency-license, and notice-completeness audit

## 0. Goal and governing product boundary

Before preparing submission materials, determine whether the real daily-use Zotero + Codex + Obsidian Skill bundle incorporates, adapts, copies, invokes, depends on, or materially derives from any third-party Skill, repository, template, script, prompt, example, package, or other protected expression beyond the already documented upstream source.

The submission product remains only:

1. `skills/zotero-collection-manager/`;
2. `skills/zotero-data-fetcher/`;
3. `skills/zotero-analytical-writer/`;
4. their bundled scripts and `agents/openai.yaml` metadata; and
5. `templates/论文精读模板.md`.

Do not introduce ScholarTrace, EvidenceGate, API adapters, standalone applications, hosted services, deployment, or new product functionality.

A public GitHub repository MUST NOT be assumed to be MIT-licensed merely because it is publicly accessible. Confirm the actual license at a fixed commit or tag. If no applicable license or written permission exists for copied/adapted expression, classify it as unresolved and block submission until it is removed, independently rewritten, or separately authorized.

## 1. Accepted baseline

Accepted daily-use synchronization and privacy-audit commit:

`521ef5d60c8b695a6b5c7bfa930511f0fdedf92a`

Accepted public `main` baseline containing the existing upstream permission and mixed-licensing notices:

`6c1c6caa93318f08cff666d94de26da42447ef59`

Protected pre-Build-Week baseline tag:

`pre-build-week-2026-public-baseline`

Required tag target:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

The task-bearing commit that adds this file must immediately follow `521ef5d...` and add only this governing task file.

## 2. Existing documented upstream relationship

The following relationship is already documented and must remain intact:

- upstream repository: `cheneternity/Zotero-Analytical-Workflow-Skills`;
- author/licensor: Eternity Chen / GitHub `cheneternity`;
- fixed five-file mapping and written repository-limited permission;
- conceptual-inspiration acknowledgement for the specified Xiaohongshu post;
- mixed-licensing boundary recorded in the repository.

Treat this as an already documented relationship, but re-check that all references to it are internally consistent and that no additional upstream files beyond the five fixed mappings were silently copied or adapted.

`UPSTREAM_PERMISSION_FINAL.md` is immutable and MUST NOT be edited.

The following previously hash-recorded legal/notice files must also remain unchanged in this audit gate:

- `THIRD_PARTY_NOTICES.md`;
- `LICENSE_SCOPE.md`;
- `ACKNOWLEDGEMENTS.md`;
- `FILE_MAPPING_AND_HASH_MANIFEST.md`;
- `UPSTREAM_PERMISSION_CONFIRMATION_RECORD.md`;
- root `LICENSE`.

If additional notices are required, create supplemental files rather than editing these locked records. README may receive a narrowly additive supplemental-notice link only after the audit establishes that such an update is required.

## 3. Git and repository preflight

Before audit work:

1. run `git fetch origin --tags`;
2. verify the exact repository identity and accepted SSH/HTTPS origin;
3. verify branch `build-week-2026-skill-release-prep`;
4. verify the task-bearing start HEAD descends immediately from `521ef5d...` and adds only this task file;
5. verify `origin/main` remains at or contains `6c1c6caa...` and is not changed by this gate;
6. verify the protected tag target exactly;
7. run `git status --short --untracked-files=all`;
8. stop if unrelated tracked or untracked project changes exist.

Use explicit-path staging only. Never use `git add .` or `git add -A`. Never force-push.

## 4. Authorized evidence scope

Inspect the complete tracked tree and reachable Git history of the public repository, limited to evidence needed for provenance and licensing.

Also inspect the already authorized daily-use local sources, read-only, only when necessary to determine whether the synchronized public files came from or refer to another Skill/source:

- `C:\Users\zcxve\.codex\skills\zotero-collection-manager\`;
- `C:\Users\zcxve\.codex\skills\zotero-data-fetcher\`;
- `C:\Users\zcxve\.codex\skills\zotero-analytical-writer\`;
- `C:\Users\zcxve\.codex\templates\论文精读模板.md`.

Do not inspect other `.codex` Skills, private repositories, Zotero data, Obsidian vaults, PDFs, research data, Downloads, browser data, credential stores, or unrelated project directories.

Public-network access is authorized only for provenance verification through:

- public GitHub repositories, commits, tags, blobs, releases, LICENSE files, NOTICE files, and repository metadata;
- official package metadata or an installed package's own license metadata when a third-party Python dependency is identified.

Do not download or execute untrusted third-party code. Do not clone broad unrelated repositories. Prefer `gh`, GitHub API, raw file fetch, `git ls-remote`, and fixed-commit file reads.

## 5. Phase A — Discover all external-source indicators

Search every tracked submission-product file and relevant reachable history for:

- GitHub URLs and repository names;
- `source`, `upstream`, `fork`, `adapted from`, `based on`, `inspired by`, `copied from`, `derived from`, `reference`, `template`, and equivalent Chinese wording;
- copyright headers and author names;
- SPDX identifiers and license names;
- code comments naming a source;
- distinctive prompt, Skill, template, or script phrases that indicate adaptation;
- vendored code, copied helper functions, or near-verbatim blocks;
- references to other Skill names or Skill collections;
- package imports and optional dependencies;
- copied `agents/openai.yaml` conventions or metadata that may originate from another public Skill;
- historical files that were later renamed, removed, or rewritten but remain relevant to the current tree's provenance.

Use targeted repository searches and Git history tools, including where useful:

- `git log --all --name-status`;
- `git log -S` and `git log -G`;
- `git blame`;
- exact-string searches;
- normalized line/block comparisons against candidate upstream files;
- file-level and block-level hashes.

Do not claim derivation solely from generic wording, common Python patterns, standard library usage, public API names, or general workflow ideas. Record the evidence and confidence level.

## 6. Phase B — Build the provenance classification

For every external candidate, classify the relationship as exactly one of:

- `DIRECT_COPY` — complete or substantial verbatim reproduction;
- `MODIFIED_COPY` — identifiable copied expression with modifications;
- `TEMPLATE_ADAPTATION` — structure or protected template expression adapted;
- `SKILL_INSTRUCTION_ADAPTATION` — Skill/prompt instructions materially adapted;
- `CODE_DEPENDENCY_NOT_VENDORED` — imported package used but not copied into this repository;
- `VENDORED_DEPENDENCY` — third-party source included in this repository;
- `REFERENCE_OR_LINK_ONLY` — cited or linked without copying protected expression;
- `CONCEPTUAL_INSPIRATION_ONLY` — general idea/workflow inspiration without identifiable copied expression;
- `PLATFORM_OR_PRODUCT_REFERENCE` — descriptive reference to Zotero, Obsidian, OpenAI, Codex, GitHub, or another platform;
- `INDEPENDENTLY_AUTHORED` — no material third-party expression identified;
- `UNRESOLVED` — evidence is insufficient to reach a defensible conclusion.

For each candidate, record:

- stable candidate ID;
- downstream path and line/block range;
- upstream owner/repository/path;
- upstream fixed commit/tag and Git blob SHA where available;
- author/copyright holder;
- relationship classification;
- evidence summary and confidence level;
- applicable license and exact license source path;
- whether the license applies at the pinned version;
- notice, attribution, source-disclosure, modification-disclosure, or redistribution obligations;
- compatibility with the repository's current mixed-licensing boundary;
- required action and blocker status.

## 7. Phase C — Verify licenses; never infer them

For every candidate involving copied/adapted/vendored expression:

1. pin the exact upstream commit, tag, or file version;
2. read the actual LICENSE/COPYING/NOTICE or per-file license at that version;
3. record the SPDX identifier only when supported by the source;
4. capture the copyright notice that must be preserved;
5. verify whether the referenced file is covered by the repository-level license or has a different per-file license;
6. verify whether attribution, NOTICE preservation, source disclosure, modification notices, reciprocal licensing, or other conditions apply.

Apply these conservative decision rules:

- MIT / BSD / ISC: generally usable when the exact copyright and license notice are preserved; do not merely write "MIT" without the notice required by the license.
- Apache-2.0: preserve the license and any applicable NOTICE; identify modification and patent-related obligations where relevant.
- MPL-2.0 / LGPL / GPL / AGPL / other reciprocal licenses: do not assume compatibility with the current distribution; classify for separate review and block submission if included source has not been handled correctly.
- Creative Commons or documentation licenses: verify whether software/Skill text use is permitted and satisfy attribution/share-alike/noncommercial restrictions as applicable.
- Public repository with no license: default classification is `NO_LICENSE_FOUND`; copied or adapted protected expression is a blocker unless separately authorized or independently rewritten.
- Unknown, custom, or ambiguous license: blocker pending resolution.
- Mere reference/link, conceptual inspiration, platform name, or standard API use: record accurately but do not falsely characterize it as copied licensed code.

This gate is a provenance and compliance audit, not legal advice. Use precise evidence and conservative classifications; do not fabricate ownership or permission.

## 8. Phase D — Python and tool dependency audit

For every non-standard-library Python import used by the submission-product scripts:

- identify package/distribution name;
- distinguish required, optional, development-only, operating-system-provided, and undeclared dependencies;
- record installed version if locally available without broad environment inspection;
- record official project URL and license metadata;
- determine whether any package source is vendored in the repository;
- record whether redistribution notices are required for the repository itself;
- flag missing installation documentation or undeclared required dependencies.

Do not install new packages in this gate. Do not inspect unrelated packages. Standard-library modules should be recorded as standard library, not third-party components.

Descriptive product/API references such as Zotero Local API, Obsidian, SQLite, Crossref, OpenAlex, Semantic Scholar, Unpaywall, and similar services must be distinguished from copied source code. Record their terms/documentation relevance only if the repository redistributes protected code or a required notice; do not turn normal API interoperability into a false source-code dependency claim.

## 9. Phase E — Notice remediation policy

If the audit finds no additional copied/adapted/vendored third-party expression beyond the already documented upstream permission:

- do not alter README or existing notices;
- create audit reports confirming the negative result with evidence.

If an additional source is permissively licensed and obligations can be satisfied without changing product behavior:

- create `THIRD_PARTY_SKILL_NOTICES.md` containing the exact source, fixed version, relationship, copyright notice, applicable license text or durable license reference as required, and modification/attribution statements;
- create `third_party_licenses/` files when preservation of full license text is required or clearer;
- update README only with a concise additive link to `THIRD_PARTY_SKILL_NOTICES.md` and a statement that additional third-party components retain their own licenses;
- do not weaken, replace, or reinterpret the existing upstream permission and mixed-licensing section.

If a source has no license, incompatible/reciprocal terms, uncertain authorship, incomplete NOTICE obligations, or unresolved copying evidence:

- do not silently remove or rewrite it in this gate;
- record the exact affected path and required remediation;
- conclude `BLOCKED_BY_UNRESOLVED_THIRD_PARTY_RIGHTS`;
- do not proceed to submission materials.

Any actual code/text removal, independent rewrite, or request for permission requires a separately authorized remediation task.

## 10. Required outputs

Always create:

1. `build_week_2026/THIRD_PARTY_SKILL_PROVENANCE_MANIFEST.csv`
2. `build_week_2026/THIRD_PARTY_DEPENDENCY_LICENSE_MANIFEST.csv`
3. `build_week_2026/THIRD_PARTY_SKILL_LICENSE_AUDIT_REPORT.md`
4. `build_week_2026/THIRD_PARTY_NOTICE_ACTION_MATRIX.md`
5. `build_week_2026/THIRD_PARTY_PROVENANCE_READINESS_CHECKPOINT.md`

Create only when required by identified obligations:

6. `THIRD_PARTY_SKILL_NOTICES.md`
7. files under `third_party_licenses/`
8. a narrowly additive README update linking the supplemental notice

The provenance manifest must contain one row for every identified candidate, including already documented upstream material, conceptual-inspiration-only items, dependencies, platform references requiring clarification, and independently authored submission-product files or coherent file groups.

## 11. Required validation

At minimum, run and report:

- CSV parse and required-column validation;
- duplicate candidate-ID check;
- every direct/adapted/vendored candidate has a pinned source or explicit unresolved status;
- every claimed license has a fetched/recorded license source;
- every required notice action appears in the action matrix;
- exact hashes of any newly added license/notice files;
- README link validation if README is changed;
- re-run the prior secret/private-path scan on all proposed additions;
- Python AST and safe `--help` checks remain passing for the existing nine scripts;
- all three `agents/openai.yaml` remain valid;
- all locked legal/permission files remain byte-identical;
- `git diff --check`;
- exact staged-path review.

Do not run real Zotero operations, access a vault, invoke a model/API, or execute downloaded third-party code.

## 12. Verdicts and readiness

Success with no additional notice obligations:

`OPENAI_BUILD_WEEK_2026_THIRD_PARTY_SKILL_PROVENANCE_AND_LICENSE_AUDIT_COMPLETE_NO_ADDITIONAL_NOTICE_REQUIRED`

Success with permissive-license notices added:

`OPENAI_BUILD_WEEK_2026_THIRD_PARTY_SKILL_PROVENANCE_AND_LICENSE_AUDIT_COMPLETE_NOTICES_ADDED`

Blocking verdict:

`BLOCKED_BY_UNRESOLVED_THIRD_PARTY_RIGHTS`

The readiness checkpoint must conclude exactly one:

- `READY_FOR_SUBMISSION_MATERIALS_GATE`;
- `READY_AFTER_SUPPLEMENTAL_NOTICE_GPT_ACCEPTANCE`;
- `BLOCKED_PENDING_THIRD_PARTY_RIGHTS_REMEDIATION`.

Only the first two permit the next gate after GPT GitHub acceptance:

`OPENAI_BUILD_WEEK_2026_SUBMISSION_MATERIALS_AND_DEVPOST_PACKAGE_GATE`

Do not start the next gate automatically.

## 13. Allowed commit and push

Commit and push only to:

`build-week-2026-skill-release-prep`

Suggested commit message when no supplemental notices are required:

`docs: audit third-party skill provenance and licenses`

Suggested commit message when notices are added:

`docs: add third-party skill license notices`

Explicitly stage only the task-authorized report/manifest/notice paths and any narrowly authorized README addition. Do not stage unrelated files.

Do not modify or push `main`. Do not create a PR, release, deployment, video, or Devpost submission.

## 14. Forbidden operations

- no `OPENAI_API_KEY` or model/API invocation;
- no ScholarTrace/API branch content;
- no broad filesystem or unrelated `.codex` Skill search;
- no private repository or private research access;
- no Zotero database, PDF, attachment, annotation, Obsidian vault, or research-data access;
- no untrusted third-party code execution;
- no assumption that public GitHub content is MIT;
- no fabrication of license, authorship, provenance, or permission;
- no modification of locked legal/permission files;
- no wildcard staging;
- no force-push;
- no submission-material creation in this gate.

## 15. Final report requirements

Report:

- exact verdict and readiness checkpoint;
- repository, branch, baseline, task-bearing HEAD, final commit, push, and final status;
- files and history ranges inspected;
- all external candidates and classification counts;
- all direct/adapted/vendored findings with fixed upstream versions and blob SHAs;
- all license identities, license-source paths, copyright notices, and obligations;
- all no-license, ambiguous, reciprocal, or unresolved findings;
- Python dependency inventory and license summary;
- supplemental notices created or reason none were required;
- README change or confirmation it remained unchanged;
- locked-file hash preservation;
- privacy/secret scan result;
- validation commands and exit codes;
- exact staged paths;
- forbidden-operation check;
- recommended next gate.
