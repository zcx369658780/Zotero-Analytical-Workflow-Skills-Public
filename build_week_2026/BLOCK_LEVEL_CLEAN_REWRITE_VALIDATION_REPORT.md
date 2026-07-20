# Block-Level Clean Rewrite Validation Report

Date: 2026-07-21

## Verdict

`OPENAI_BUILD_WEEK_2026_UNRESOLVED_SOURCE_DISCOVERY_AND_BLOCK_LEVEL_CLEAN_REWRITE_COMPLETE`

## Architecture

- `classification.py`: shared ordered rule tables and one classifier boundary preserve all public infer signatures, labels, precedence, and the 8,000-character full-text limit.
- `template_renderer.py`: discovers the separately authorized template, validates frontmatter and eight unique ordered top-level sections, maps neutral section IDs to runtime headings, and fails closed without an embedded fallback.
- `metadata_client.py`: standard-library-only request builders, normalizers, title matching, DOI cleanup, OA-location collection, and injectable HTTP boundary for Crossref, OpenAlex, and Unpaywall.
- The three existing scripts retain public wrappers and orchestration while delegating rewritten behavior to these modules.

## Synthetic tests

Command:

`python -m unittest -v tests.test_unresolved_block_behavior tests.test_clean_rewrite_safety`

Result: 24 tests run, 24 passed, exit code 0. All HTTP interactions were mocked; no live external request occurred.

Coverage includes:

- complete infer keyword and precedence matrices plus 8,000-character boundary;
- first-pass and deep-read deterministic rendering;
- missing and malformed template failure;
- dynamic proof that runtime template headings/skeleton are absent from product Python;
- Crossref, OpenAlex, and Unpaywall success/failure normalization;
- DOI and title normalization, OA ordering/deduplication, partial-result behavior;
- DOI and title-only OpenAlex mismatch warnings and bounded retry behavior;
- HTTP timeout, User-Agent, and JSON Accept headers.

## Structural checks

- Python AST: 12 of 12 product scripts/modules passed, exit code 0.
- Safe `--help`: 9 of 9 original product scripts passed, each exit code 0.
- Agent YAML: 3 of 3 parsed as mappings with an `interface` mapping, exit code 0.
- `git diff --check`: exit code 0.
- Authorized template SHA256 remained `F9E56E7EFC3E2E699AC39388292F39A9DAD03D59AB7CAC0C3C3A2901E958C8FB`.

## Privacy, secrets, and locked files

- Private-key and credential-token patterns: no matches (`rg` exit code 1).
- Credential-value assignments: no matches (`rg` exit code 1).
- Corrected Windows/POSIX private-path patterns: no matches (`rg` exit code 1).
- Email-address scan found only synthetic `example.invalid` test/User-Agent values; no real contact address was introduced.
- All six locked legal/permission files matched their accepted SHA256 values.
- README, root LICENSE, three Skills, authorized template, three agent YAML files, and all locked legal/permission files had no diff from task-bearing HEAD (`git diff --quiet` exit code 0).
- No `OPENAI_API_KEY`, model API, Zotero database, PDF, vault, private research, credential source, private repository, Downloads, browser data, or ScholarTrace content was accessed.

## Local comparison

After all public tests passed, only the three authorized local affected paths were hashed read-only. All existed and all differed from the public rewrite:

| Affected file | Local SHA256 | Public SHA256 | Identical |
|---|---|---|---|
| `batch_import_collection.py` | `28E2027855A7D9344C40E90393B3E12005C5D594CF81D5C96E43C895D2193A0E` | `AAE9EF11A2CF79CA23DD16511DA62F5DDCEB789C5E804BD1674B0C772AADCC30` | No |
| `deep_read_collection.py` | `7817755FD044DADEA1CC4E80B4221D1AC7FC0C9F538ED3439BC778DBFFF9C4E7` | `59AC4548A785B626D4903EB2384F1C1D72B64C628FF0056F19DD1FF6945EB7A4` | No |
| `zotero_fetch.py` | `03711AF89296F6B0373CC93A50B0CE8DF398CA0C75698821B13AF44B887FA15D` | `FFBE9B1B1747069AAD6C4FEA19B78459CF671F7B0C388EFD4E065A6C82B0D568` | No |

A separate local-install synchronization gate is required and must include the three new helper modules. No local file was modified.
