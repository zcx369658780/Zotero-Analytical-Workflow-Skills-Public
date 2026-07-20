# OpenAI Build Week 2026 - Public Repository Baseline and ScholarTrace Scope Gate

Date: 2026-07-20
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`
Branch: `build-week-2026-scholartrace`
Task type: planning, provenance boundary, and scope freeze only

## 0. Governing status

This task freezes the scope of a proposed independently developed Build Week
extension called ScholarTrace / Evidence Gate. It does not authorize product
implementation, model execution, fixture creation, or access to private
research materials.

The accepted upstream-permission integration baseline is:

`6c1c6caa93318f08cff666d94de26da42447ef59`

The protected pre-Build-Week public baseline tag is:

`pre-build-week-2026-public-baseline`

and must resolve to:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

## 1. Required preflight

Before writing, the executor must:

1. run `git fetch origin --tags`;
2. confirm the repository identity and accepted SSH or HTTPS origin;
3. confirm a clean working tree;
4. confirm `origin/main` contains the accepted permission baseline;
5. check out `build-week-2026-scholartrace`;
6. verify the branch begins exactly at the accepted permission baseline;
7. synchronize only by a fast-forward-only operation; and
8. stop on unexpected commits, files, divergence, or repository identity.

## 2. Required deliverables

Create only:

- `build_week_2026/PRE_EXISTING_WORK.md`;
- `build_week_2026/NEW_WORK_SINCE_2026_07_13.md`;
- `build_week_2026/SCHOLARTRACE_MVP_SCOPE.md`;
- `build_week_2026/SCHOLARTRACE_FIXTURE_AND_EVALUATION_PLAN.md`;
- `build_week_2026/CODEX_GPT56_USAGE_PLAN.md`;
- `build_week_2026/BUILD_WEEK_READINESS_DECISION.md`; and
- `build_week_2026/PUBLIC_REPO_BASELINE_AND_SCHOLARTRACE_SCOPE_GATE_REPORT.md`.

Together with this task file, these documents must:

- separate work present at the protected tag from all later additions;
- classify commit `6c1c6caa...` as permission/licensing integration, not a
  judged feature;
- define ScholarTrace as an independently developed extension;
- freeze target users, Education-track narrative, contracts, verdict taxonomy,
  fail-closed rules, human review, privacy/copyright rules, tests, demo path,
  and non-goals;
- require `supported`, `partially_supported`, `unsupported`, `overstated`, and
  `unverifiable`;
- plan fixtures for unsupported conclusions, correlation presented as
  causation, and omitted limiting conditions;
- use only independently written or lawfully reusable demonstration sources;
- define meaningful GPT-5.6 and Codex responsibilities;
- preserve the primary Codex session and later `/feedback` Session ID;
- preserve read-only defaults, no-overwrite output, `human_verified: false`,
  no automatic E3 promotion, and no direct real-vault writes; and
- end in `GO`, `CONDITIONAL_GO`, or `NO_GO` with remaining blockers.

## 3. Scope frozen by this gate

ScholarTrace is an educational claim-evidence audit workflow. It will accept a
bounded, structured demonstration bundle containing claims, supplied source
excerpts, locators, and provenance metadata. It will return a machine-readable
audit and a human-readable report without modifying the source bundle.

The MVP is limited to the five required verdicts and deterministic policy
checks over supplied materials. It is not a literature-discovery system, PDF
parser, citation manager replacement, autonomous verifier, or automated
publisher.

## 4. Allowed operations

Only the following operations are authorized:

- repository, branch, tag, commit, and status inspection;
- read-only inspection of public repository files and Git history;
- creation of this task file and the seven planning deliverables;
- documentation-only consistency and sensitive-content checks;
- explicit-path staging of exactly those eight files;
- one focused documentation commit; and
- push of that commit only to `origin/build-week-2026-scholartrace`.

## 5. Forbidden operations

The executor must not:

- implement ScholarTrace, Evidence Gate, or any other feature;
- create or modify Python, schemas, tests, fixtures, or CLI code;
- invoke GPT-5.6 or any API;
- inspect credentials or authentication material beyond ordinary GitHub CLI
  status required for the authorized push;
- access Zotero databases, attachments, or local APIs;
- access or modify an Obsidian vault;
- parse PDFs or include copyrighted sample papers;
- include private Zotero content, purchased data, Xiaohongshu screenshots, or
  unpublished research;
- modify any locked permission, notice, mapping, confirmation, Skill, template,
  or root license file;
- merge to `main`;
- create a release, deployment, Devpost submission, or video upload;
- use `git add .`, `git add -A`, force-push, or destructive Git recovery.

## 6. Required checks

Before commit:

1. confirm the protected tag target and permission baseline;
2. confirm the eight-path change set exactly;
3. confirm all locked files have no diff;
4. confirm no implementation-like extension was added;
5. confirm the five verdicts and three required fixture cases are present;
6. confirm every planning document preserves the safety invariants;
7. search staged content for credentials, email addresses, private paths,
   private research content, or copied paper text;
8. inspect the complete staged diff; and
9. stage only explicit paths.

After push:

1. confirm local HEAD, upstream branch, and remote branch match;
2. confirm the final working tree is clean;
3. confirm the protected tag still resolves to the protected baseline; and
4. stop without starting the next gate.

## 7. Commit and verdict

Suggested commit message:

`docs: freeze ScholarTrace Build Week scope`

Expected success verdict:

`OPENAI_BUILD_WEEK_2026_PUBLIC_REPO_BASELINE_AND_SCHOLARTRACE_SCOPE_GATE_COMPLETE`

Recommended next gate, only after GPT GitHub acceptance:

`OPENAI_BUILD_WEEK_2026_SCHOLARTRACE_FIXTURES_SCHEMA_AND_DETERMINISTIC_PIPELINE_GATE`
