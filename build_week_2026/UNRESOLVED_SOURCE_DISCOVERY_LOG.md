# Unresolved Source Discovery Log

Date: 2026-07-21
Role: Phase A source-discovery only
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`
Branch: `build-week-2026-skill-release-prep`
Task-bearing HEAD: `7736467d1532e6c41fbcba9b3285b18927434cc5`
Accepted parent: `1a9b18981f3c4ddaf864064822ac94e50fa21760`

## Scope and method

This pass followed Section 5 of the governing task. It used public GitHub code or repository search only. No candidate code was downloaded or executed, no private repository or local daily-use file was accessed, no author was contacted, and no product code was read or modified.

Search result counts below are the exact number of results returned by the GitHub search connector. A count of 20 means the configured 20-result return cap was reached and is not represented as a complete global total. Returned paths were screened only for a credible connection to the unresolved material; generic helper names, API endpoints, standard fields, and ordinary control flow were not treated as copying evidence.

## Numbered search ledger

1. Query: `def infer_theme`. Category: function-signature prefix for MSB-010. Result count: 10. Outcome: unrelated theme-inference and rendering paths; no Zotero or matching three-helper candidate.
2. Query: `"def infer_theme("`. Category: exact function-signature prefix for MSB-010. Result count: 20 (return cap). Outcome: unrelated repositories and paths; no credible Zotero source candidate.
3. Query: `"def infer_methodology("`. Category: exact function-signature prefix for MSB-010. Result count: 3. Outcome: unrelated research-corpus and analysis paths; no credible Zotero source candidate.
4. Query: `"def infer_core_variable("`. Category: exact function-signature prefix for MSB-010. Result count: 2. Outcome: both hits were the already screened `SPUERSAIYAN/Stock-Agent-Arena` stock-analysis implementation at commit `91019f87babeb64db61adce81752e6568e3f2a53`; no new candidate.
5. Query: `"infer_theme" "infer_methodology" "infer_core_variable"`. Category: ordered three-helper combination for MSB-010. Result count: 0. Outcome: no candidate.
6. Query: `zotero_collection_manager_v2_pilot.py`. Category: exact historical filename tied to MSB-010. Result count: 0. Outcome: no additional indexed copy or candidate.
7. Query: `"def make_note(" zotero`. Category: exact note-rendering helper name tied to MSB-012/013. Result count: 0. Outcome: no candidate.
8. Query: `"def make_deep_note("`. Category: exact note-rendering helper name tied to MSB-016/017. Result count: 0. Outcome: no candidate.
9. Query: `"make_note" "make_deep_note" zotero`. Category: ordered note-renderer marker sequence tied to MSB-012/013 and MSB-016/017. Result count: 0. Outcome: no candidate.
10. Query: `regenerate_template_notes.py`. Category: exact historical filename tied to MSB-013/017. Result count: 0. Outcome: no additional indexed copy or candidate.
11. Query: `"clean_doi" "title_similarity"`. Category: ordered metadata-helper combination for MSB-026. Result count: 20 (return cap). Outcome: generic citation, DOI-verification, and metadata utilities; one Zotero bot path was present, but the query exposed only common helper roles and supplied no exact unresolved-block evidence. No credible exact-source candidate.
12. Query: `"http_json" "clean_doi" "title_similarity"`. Category: ordered three-helper combination for MSB-026. Result count: 4. Outcome: citation verification/resolution utilities (`Aperivue/medsci-skills`, `Tw6249/scholarly-deep-research`, `fengwm64/skills`, and `maedoc/tvb-wiki`); none was Zotero-specific or an exact-block result. No credible candidate.
13. Query: `Crossref OpenAlex Unpaywall title_similarity`. Category: uncommon multi-service/helper combination for MSB-026. Result count: 20 (return cap). Outcome: generic scholarly-metadata integrations and documentation; shared services and helper role are not copying evidence. No credible candidate.
14. Query: `"def clean_doi(" Zotero`. Category: exact helper-signature prefix plus product domain for MSB-026. Result count: 15. Outcome: generic DOI cleanup in Zotero-related tools, including the already screened `zbw0520/zotero-codex-skills`; no exact unresolved-block evidence and no new credible candidate.
15. Query: `zotero_fetch.py clean_doi title_similarity`. Category: exact historical filename plus ordered helper combination for MSB-026. Result count: 0. Outcome: no candidate.
16. Query: `api.crossref.org api.openalex.org api.unpaywall.org`. Category: uncommon three-endpoint combination for MSB-026. Result count: 20 (return cap). Outcome: generic API cookbooks, configuration, retrieval utilities, and documentation; endpoint co-occurrence alone is not copying evidence. No credible candidate.
17. Query: repository search `zotero Crossref OpenAlex Unpaywall`. Category: repository-level multi-service/product combination for MSB-026. Result count: 1. Outcome: `roomi-fields/paper-trail`; repository-level topical overlap only, with no exact helper, filename, warning, or block evidence. Not a credible exact-source candidate.
18. Query: repository search `zotero infer_theme infer_methodology`. Category: repository-level helper/product combination for MSB-010. Result count: 0. Outcome: no candidate.

**Total public GitHub code/repository searches: 18.** The Section 5 maximum was 20; two searches remained unused.

## Candidate and license evidence

No new credible candidate was fixed by this pass, so no new owner/repository, commit, path, blob, or license record is added.

The following fixed evidence from the accepted multi-source manifests remains controlling:

- `cheneternity/Zotero-Analytical-Workflow-Skills`, commit `81c624d37a114028dd49c63764694e30e5be13d4`, `templates/论文精读模板.md`, blob `ee49e315d9e7a51a00bc256013e98f8713e82e58`: exact source for the template expression in MSB-012 and MSB-016. The repository has no public license. Existing written permission identifies and covers only the five fixed mapped counterparts, not either additional Python embedding path.
- `cheneternity/Zotero-Analytical-Workflow-Skills`, commit `0888dc1a2e941979cf73d4575b89a40a5db22dd7`, `scripts/zotero_collection_manager_v2_pilot.py`, blob `ada0f997c60e9baaf0fa74130bae9769badb3e33`: plausible parallel for MSB-010, not an exact established source. No `LICENSE`, `LICENSE.md`, `COPYING`, or `NOTICE` was present at the fixed version.
- The same repository and commit, `scripts/regenerate_template_notes.py`, blob `35ec0f85774488ada298116c31b4a7d1dfe0227f`: plausible parallel for MSB-013/017, not an exact established source outside the already confirmed template expression. No license file was present at the fixed version.
- `zbw0520/zotero-codex-skills`, fixed commits `0811ef944010abc0d4d2bce1588bc1652b47f363`, `c9d20891bfce120e200f7cad0731eb1c8ecbab4b`, and `b154fc72f7915e9c0439c68e5c98ac3d119899ff`: generic helper-name overlap relevant to MSB-010/MSB-026, with materially different bodies in the accepted comparison. No license files or per-file copyright headers were present at those fixed versions.
- `Enthoes1/doi-zotero-skills`, commit `f07bb61178162cb7e32ca88ed1f1172d51c1da58`, `skills/doi-to-zotero-word/scripts/doi_to_zotero_word.py`, blob `86476a01a791892addfbf76ef5499942f556f8f2`: shared public-service concepts/constants but no non-generic block match for MSB-026. No license file or per-file copyright header was present at the fixed version.
- `SPUERSAIYAN/Stock-Agent-Arena`, commit `91019f87babeb64db61adce81752e6568e3f2a53`, `agents/information_workflow.py`, blob `3540b691f1c58c9a835e750042aaa655ea028a3a`: generic `infer_core_variable` name only and unrelated stock-analysis logic. No license was found in the accepted repository metadata.

No permissively licensed exact source was confirmed. No supplemental notice route is activated by Phase A.

## Required dispositions

1. **MSB-010:** `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH`. The exact three-helper combination and historical filename produced no result; individual-name results were unrelated or already rejected.
2. **MSB-012:** `EXACT_EXISTING_PERMISSION_SOURCE_CONFIRMED`. The fixed cheneternity template blob is the exact expression source. This disposition confirms source identity only: existing written permission does not cover expression embedded in `batch_import_collection.py`, so retention is not authorized by the current mapping.
3. **MSB-013:** `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH`. No exact `make_note` or regeneration-source result established the surrounding generator logic.
4. **MSB-016:** `EXACT_EXISTING_PERMISSION_SOURCE_CONFIRMED`. The fixed cheneternity template blob is the exact expression source. This disposition confirms source identity only: existing written permission does not cover expression embedded in `deep_read_collection.py`, so retention is not authorized by the current mapping.
5. **MSB-017:** `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH`. No exact `make_deep_note`, paired-renderer, or regeneration-source result established the surrounding deep-read generator logic.
6. **MSB-026:** `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH`. Metadata-helper, filename/helper, and multi-service searches found only generic API/helper overlap or topical repositories; none established an exact source.

## Phase A closeout

Phase A found no new exact permissive, incompatible, or no-license source. The only exact source remains the previously fixed cheneternity template expression for MSB-012 and MSB-016, with the previously documented permission-scope gap. All other listed blocks remain unresolved after the bounded search and require the later separated remediation route defined by the governing task. This role did not begin Phase B, implement a rewrite, create notices, or contact any author.
