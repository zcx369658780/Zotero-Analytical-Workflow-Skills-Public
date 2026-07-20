# Multi-Source Skill Provenance Reconstruction Report

Date: 2026-07-20

## Verdict

`BLOCKED_BY_UNRESOLVED_MULTI_SOURCE_PROVENANCE`

The user's correction is controlling: material outside the five fixed cheneternity mappings cannot be assigned to Eternity Chen merely because his historical repository contains similar code.

## Repository and evidence scope

- Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`
- Branch: `build-week-2026-skill-release-prep`
- Accepted provenance-audit commit: `2d4f81014e656f07ae6d22297a3785f8a0f55926`
- Superseded task commit: `763c0c14f5854fe373e7d1113e36ccbf66b003cd`
- Task-bearing start HEAD: `9b10aec1f8560356d527fd546190246c8dd8c170`
- Public main baseline: `6c1c6caa93318f08cff666d94de26da42447ef59`
- Protected baseline tag: `e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

All 16 submission files were covered by 28 block rows. Current-branch reachable history from the root commit through task HEAD, relevant reports/tasks, fixed public GitHub trees, and the four authorized local daily-use paths were inspected. The superseded supplement task was not executed.

## Search method and evidence

The audit used:

- exact function signatures and names;
- ordered Markdown headings and distinctive Chinese prompts;
- error strings, return strings, evidence fields and migration-stage names;
- filenames and agent metadata wording;
- fixed GitHub trees, blobs, commit dates, repository license metadata and license-file reads;
- normalized ordered-line, AST function-name and long string-constant comparisons.

More than 50 GitHub code-search queries were run in rate-limited batches. Key zero-result searches included the three infer signatures, all distinctive infer return strings, `zotero_notes_or_annotations`, `Stage2E_sample_migration`, `_EvidenceMigrationLog_EvidenceSchema.md`, template prompt pairs, online-metadata warnings, all three agent default prompts, and unique backup/write-gate errors.

Repository-family screening covered 22 public candidate repositories. Five separate public files named `zotero_fetch.py` were compared and none shared a non-generic function, constant or continuous block with the downstream fetcher. Stronger candidate details are in the origin manifest.

Evidence unavailable:

- pre-public development history for the scripts;
- original Codex browsing/install logs naming source repositories;
- reliable source comments in the authorized local installation;
- deleted history in unknown external repositories.

The authorized local installation had no GitHub/source/SPDX/copyright indicators. Data-fetcher, analytical-writer and template files matched public counterparts; collection-manager contained the already documented machine-path drift but no source marker.

## Re-evaluation of prior findings

### TP-006

Prior conclusion: high-confidence modified copy from cheneternity's historical pilot.

New evidence: the historical pilot remains structurally similar, but GitHub search found no exact signature or return-string copy. A second repository matched only the generic function name `infer_core_variable` with unrelated stock logic. The user's correction establishes that other repositories were used.

Revised conclusion: `UNRESOLVED`, not assignable to Eternity Chen. Route: `UNRESOLVED_SOURCE_BLOCKER`; do not prepare an Eternity supplement for these functions.

### TP-007

Prior conclusion: template adaptation outside the five listed counterparts.

New evidence: 28 literals in `make_note` and 30 in `make_deep_note` map directly to the fixed cheneternity template. Broad Skill/template repository comparison found no competing source for those exact ordered headings. Additional deep-read prompts had no external match.

Revised conclusion: retain `TEMPLATE_ADAPTATION` for the exact template-derived literals, source owner Eternity Chen, route `ETERNITY_SUPPLEMENT_NEEDED` if retained. Surrounding generator logic and extra prompts are separate blocks; unresolved parts must not be folded into that request.

### TP-008

Prior conclusion: unresolved relationship to cheneternity's historical regeneration script.

New evidence: fixed comparison still shows functional-domain similarity but no material non-generic code block outside already explained template expression. No public evidence establishes that this historical script was the actual source.

Revised conclusion: remain `UNRESOLVED`, but remove the implied Eternity ownership route. Route: source discovery or independent rewrite, not an Eternity request.

## Candidate counts

- Confirmed source repository: cheneternity, 5 fixed counterpart blocks plus 2 embedded-template blocks.
- Plausible but unestablished source repositories: cheneternity historical scripts, `zbw0520/zotero-codex-skills`, and `Enthoes1/doi-zotero-skills`.
- Platform-schema reference: `openai/skills`.
- Rejected source candidates after comparison: 18 repository entries/groups.
- Block classifications: 5 authorized upstream counterparts, 2 additional template adaptations needing narrower scope, 4 unresolved blocks, 7 independently authored blocks, 7 generic blocks, and 3 platform-schema/custom-metadata blocks. Some line ranges contain separate template and generator rows, so classification totals exceed unique files.

## Rights routing

No author is assigned material from another repository:

- existing Eternity permission: only the five mapped counterparts;
- possible Eternity supplement: only exact fixed-template expression embedded in two named scripts;
- TP-006, TP-008 and online-metadata uncertainty: no author request; source discovery or clean rewrite;
- no permissive notice route was activated;
- no AGPL or other reciprocal code was confirmed as incorporated;
- generic platform/API/CLI patterns require no source permission.

## Output boundary

No email, permission supplement, license notice, README update, product-code change or rewrite was created. This report does not claim any new permission is effective.

## Validation

- Both CSV files parsed successfully with all required columns present.
- The block manifest contains 28 unique block IDs; the candidate manifest contains 24 unique candidate IDs.
- All 16 submission-product files are covered, all candidate references resolve, and all routes use the authorized route vocabulary.
- TP-006, TP-007, and TP-008 each have a documented re-evaluation.
- All nine Python scripts passed AST parsing and safe `--help` checks with exit code 0.
- All three `agents/openai.yaml` files parsed as mappings with an `interface` mapping.
- Secret-token, private-path, email-address, and credential-value scans over only the six additions returned no matches.
- The six locked legal/permission files matched their accepted SHA256 values. README, root LICENSE, the submission product, and those locked files had no tracked diff from task-bearing HEAD.
- The protected annotated tag peeled to `e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`.
