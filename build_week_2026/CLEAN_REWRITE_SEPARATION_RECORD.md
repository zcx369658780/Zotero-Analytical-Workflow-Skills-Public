# Clean Rewrite Separation Record

Date: 2026-07-21

## Result

`SEPARATION_MAINTAINED`

The gate used separate Codex subagent contexts. No private session identifier or transcript is recorded here.

## Roles and boundaries

### Source-discovery role

- Read only the governing task and accepted provenance records.
- Performed 18 public GitHub searches and wrote only `UNRESOLVED_SOURCE_DISCOVERY_LOG.md`.
- Did not read or modify product implementation and did not communicate candidate source text to the implementation role.

### Behavior-analyst role

- Could read the affected downstream baseline blocks, public interfaces, authorized template, and caller-visible behavior.
- Wrote only the neutral behavior contract and synthetic tests.
- Did not write replacement implementation or read candidate GitHub code.
- Final frozen implementation inputs:
  - `UNRESOLVED_BLOCK_BEHAVIOR_CONTRACT.md`: SHA256 `A30A62D3F6B850A187F7A7C2A7B2FC9E0FDEFDAD80E4815A49EF05BF32BB4263`
  - `tests/test_unresolved_block_behavior.py`: SHA256 `6BBD093A299EAAFE597B32F228E342C38B58AD459A0BBA118689D4C116C75F2E`
- After implementation and review, two Markdown hard-break trailing spaces were removed from the contract solely for `git diff --check`; committed contract SHA256 is `0F4CF7177AA9EBEE7F2C598E533807C8D85760FA7E37253CB507A93F9727596D`. No wording or implementation input changed.

### Implementation role

- Started without parent-thread context.
- Received only the frozen neutral contract, frozen synthetic tests, public signatures and non-prohibited call-site context, the authorized runtime template contract, and official Crossref, OpenAlex, Unpaywall, DOI, and Python standard-library documentation.
- Could write only the three affected scripts and three new helper modules.
- Did not receive or open candidate repositories, candidate blobs, provenance reports, source-discovery output, local daily-use implementation, private data, or the old unresolved source-range text.
- Old AST nodes were located mechanically by name and boundary for wholesale replacement; their bodies were not displayed or supplied as implementation input.
- Did not modify the frozen contract, tests, template, README, legal files, Skills, agent metadata, or unrelated scripts.

### Review role

- Began only after implementation.
- Read the final rewrite, baseline blocks, accepted candidate manifest, and fixed public candidates for comparison.
- Was read-only and made no implementation, staging, or commit change.
- Identified and verified remediation of template-expression, behavior-regression, and OpenAlex mismatch-reporting issues.

## Prohibited-source controls

The implementation context was explicitly prohibited from reading:

- `cheneternity/Zotero-Analytical-Workflow-Skills` historical script bodies;
- `zbw0520/zotero-codex-skills`;
- `Enthoes1/doi-zotero-skills`;
- all other candidate repositories and blobs;
- old unresolved line ranges after contract freeze;
- provenance and source-discovery reports;
- the authorized local daily-use affected scripts;
- private repositories, Zotero data, PDFs, vaults, research data, credentials, Downloads, browser data, or ScholarTrace.

No candidate expression was transmitted between roles. No external model API or live metadata service was invoked.
