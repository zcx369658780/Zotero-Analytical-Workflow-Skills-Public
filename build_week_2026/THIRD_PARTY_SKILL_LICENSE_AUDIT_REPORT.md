# Third-Party Skill Provenance and License Audit Report

Date: 2026-07-20

## Verdict

`BLOCKED_BY_UNRESOLVED_THIRD_PARTY_RIGHTS`

This is a provenance and compliance audit, not legal advice. The blocking result follows the task's conservative no-license and scope-ambiguity rules.

## Repository and scope

- Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`
- Branch: `build-week-2026-skill-release-prep`
- Accepted synchronization baseline: `521ef5d60c8b695a6b5c7bfa930511f0fdedf92a`
- Task-bearing start HEAD: `ae9b6a2a11b437fbdf0552d169134f01c38c7772`
- Public main baseline: `6c1c6caa93318f08cff666d94de26da42447ef59`
- Protected baseline tag: `e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`
- Reachable current-branch history inspected: `e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e..ae9b6a2a11b437fbdf0552d169134f01c38c7772`, including the root commit.

The complete 16-file submission product was inspected: three `SKILL.md` files, three `agents/openai.yaml` files, nine Python scripts, and `templates/论文精读模板.md`. The four authorized local daily-use locations were checked only for provenance indicators; no other `.codex` Skill, private repository, Zotero data, vault, PDF, research data, Downloads directory, browser data, or credential source was accessed.

## Fixed upstream evidence

The documented upstream repository is `cheneternity/Zotero-Analytical-Workflow-Skills`, owned by GitHub user `cheneternity`; the existing effective permission identifies the author/licensor as Eternity Chen.

Commit `81c624d37a114028dd49c63764694e30e5be13d4` contains the five already documented blobs:

- `README.md`: `868334953c93b49f666af700fed9d2e6edb464fd`
- `skills/zotero-collection-manager/SKILL.md`: `b32f2f26eebe47b111ad13c8cd72a4ff5de5af09`
- `skills/zotero-data-fetcher/SKILL.md`: `3b4f4409415d8886f678f058f4cc3dfa4d673372`
- `skills/zotero-analytical-writer/SKILL.md`: `858be0d998625824cbf362beda5f7ce0d80c39d5`
- `templates/论文精读模板.md`: `ee49e315d9e7a51a00bc256013e98f8713e82e58`

Those five downstream counterparts remain governed by the effective repository-limited written permission and are correctly excluded from downstream MIT scope.

The upstream repository reports no repository license. At historical commit `0888dc1a2e941979cf73d4575b89a40a5db22dd7`, its tree contained:

- `scripts/regenerate_template_notes.py`, blob `35ec0f85774488ada298116c31b4a7d1dfe0227f`
- `scripts/zotero_collection_manager_v2_pilot.py`, blob `ada0f997c60e9baaf0fa74130bae9769badb3e33`

Direct fixed-version probes for `LICENSE`, `LICENSE.md`, `COPYING`, and `NOTICE` all returned 404. The scripts were deleted in the next commit, `70dee34552b9ccd98882c4458aec81a27da77eb4`. The existing written permission expressly fixes five other upstream paths and five downstream counterparts; it does not list either historical script.

## Blocking findings

### Historical pilot adaptation

`skills/zotero-collection-manager/scripts/batch_import_collection.py:127-173` contains `infer_theme`, `infer_methodology`, and `infer_core_variable`. The fixed historical pilot has the same three non-generic names and responsibilities, matching or near-matching signatures, the same keyword-branch classification structure, and categorized return text. Function-body similarity scores were 0.4718, 0.4893, and 0.4591 after the domain-specific vocabulary was changed.

This is classified `MODIFIED_COPY` with high confidence. No public license or written permission covering these source and downstream paths was found. Attribution or a supplemental notice alone cannot create redistribution rights.

### Template expression embedded outside the fixed counterpart

`batch_import_collection.py:355-530` reproduces 28 literals from the fixed upstream template. `deep_read_collection.py:462-679` reproduces 30. Both include the ordered major headings and distinctive prompts used to generate complete notes.

This is classified `TEMPLATE_ADAPTATION` with high confidence. Although the template counterpart itself is authorized, these two Python files are not listed downstream counterparts. The narrow path scope in the existing permission does not clearly authorize separately MIT-claimed code files embedding the protected template expression.

### Historical regeneration-script relationship

The historical `regenerate_template_notes.py` performs the same template-note regeneration function. Comparison found short helper overlap and template-field correspondence, but not enough fixed expression to prove or exclude a further modified copy. Because the downstream public history begins with the completed scripts, no earlier authorship trail resolves the relationship.

This candidate is `UNRESOLVED`. Under the task's rule for no-license public repositories and uncertain provenance, it is independently blocking.

## Classification counts

- `DIRECT_COPY`: 0
- `MODIFIED_COPY`: 2
- `TEMPLATE_ADAPTATION`: 2
- `SKILL_INSTRUCTION_ADAPTATION`: 3
- `CODE_DEPENDENCY_NOT_VENDORED`: 0 third-party packages
- `VENDORED_DEPENDENCY`: 0
- `REFERENCE_OR_LINK_ONLY`: 0
- `CONCEPTUAL_INSPIRATION_ONLY`: 1
- `PLATFORM_OR_PRODUCT_REFERENCE`: 2
- `INDEPENDENTLY_AUTHORED`: 3 coherent groups
- `UNRESOLVED`: 1
- Total provenance candidates: 14

No GPL, AGPL, LGPL, MPL, Apache, BSD, ISC, Creative Commons, or other reciprocal/permissive package was found in the submission product. The critical finding is absence of an applicable public license or sufficiently broad written permission, not reciprocal-license incompatibility.

## Python dependencies

All product imports resolve either to the Python 3.11 standard library or repository-local modules. No PyPI or other non-standard Python distribution is required, imported, or vendored.

The observed interpreter was CPython 3.11.9. Standard-library modules are listed in the dependency manifest and are not treated as third-party packages bundled by this repository. Zotero Local API, Crossref, OpenAlex, and Unpaywall are interoperability/service references, not copied source dependencies.

## Supplemental notice decision

No `THIRD_PARTY_SKILL_NOTICES.md`, `third_party_licenses/`, or README link was created. A supplemental permissive-license notice cannot cure a no-license source or unclear written-permission scope. README remained unchanged.

Required remediation must occur in a separate authorized task:

1. obtain express written permission covering the two historical script blobs and all affected downstream paths; or
2. remove and independently rewrite the affected code and generated-template expression without consulting the unlicensed source; and
3. resolve the provenance of the historical regeneration-script relationship with reliable source history, permission, or a clean rewrite.

## Validation

- provenance CSV: 14 rows, all required columns present, duplicate candidate IDs 0, exit 0
- dependency CSV: 6 rows, all required columns present, duplicate dependency IDs 0, exit 0
- action-matrix coverage: 14 of 14 provenance candidate IDs, exit 0
- pinned-source rule: every direct, modified, template, Skill-instruction, or vendored classification has a fixed version and blob, exit 0
- Python AST parse: 9 of 9 scripts, exit 0
- safe script `--help`: 9 of 9 scripts, 0 failures
- agent YAML parse: 3 of 3 files, exit 0
- `git diff --check`: exit 0
- locked legal/permission hash mismatches: 0
- README changed: false
- supplemental notice/license files created: 0
- high-confidence credential/private-key findings in proposed additions: 0
- real private-path findings in proposed additions: 0
- private contact findings: 0; one phone-pattern heuristic hit was a numeric substring inside a Git blob SHA and was reviewed as a false positive

## Privacy and forbidden operations

No credential, API key, private key, real private path, private correspondence, or personal research content was needed or introduced. No model/API was invoked. No untrusted code was executed. No ScholarTrace branch content, private repository, Zotero database, PDF, annotation, vault, or research data was accessed. No product functionality was added.
