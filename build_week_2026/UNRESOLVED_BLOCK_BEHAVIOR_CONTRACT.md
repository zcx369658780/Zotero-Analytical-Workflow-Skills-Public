# Unresolved Block Behavior Contract

Date: 2026-07-21
Role: behavior analyst
Scope: MSB-010, MSB-012/013, MSB-016/017, and MSB-026

## 1. Purpose and boundary

This document records public interfaces and externally observable behavior needed for an independent rewrite. It does not prescribe algorithms, internal organization, helper names, or control flow. All examples are synthetic and fictional.

The covered code must remain standard-library-only, must not contact a network during tests, must not read or write Zotero, vault, PDF, credential, or private-path data unless an existing caller explicitly supplies such data, and must not add machine-specific defaults.

## 2. MSB-010: inference helpers

### Public interfaces

| Function | Accepted inputs | Output |
| --- | --- | --- |
| `infer_theme(title: str) -> str` | A title string. Matching is case-insensitive. | One non-empty Chinese category label. |
| `infer_methodology(title: str, abstract: str, fulltext: str) -> str` | Three strings. Matching is case-insensitive. | One non-empty Chinese method label. |
| `infer_core_variable(title: str, abstract: str) -> str` | Two strings. Matching is case-insensitive. | One non-empty Chinese variable label. |

The functions are pure: they perform no I/O, do not mutate inputs, and return the same result for repeated equal inputs. Matching is case-insensitive substring matching. When more than one recognized concept is present, the first matching row in the tables below wins. Unrecognized text returns the established general fallback rather than an empty value or exception.

### Complete theme matrix and precedence

| Priority | Trigger keyword(s) in title | Exact established label |
| --- | --- | --- |
| 1 | `hank` | `异质主体宏观模型与政策传导` |
| 2 | `migration` or `commuting` | `人口迁移与空间劳动力配置` |
| 3 | `housing` | `住房约束与空间资源错配` |
| 4 | `spatial` or `geography` | `空间结构与宏观经济政策` |
| 5 | `monetary` | `货币政策传导与区域异质性` |
| 6 | `climate` | `气候冲击与宏观经济` |
| 7 | no trigger | `空间宏观经济与异质性分析` |

Synthetic alias cases use titles such as `Commuting in Fictional Harbor` and `Geography of Northwind`. A title containing all branch keywords returns the priority-1 label. More generally, a title containing a row's keyword plus any lower-priority keywords returns that row's label.

### Complete methodology matrix, precedence, and text boundary

The search text is the title, abstract, and only the first 8,000 characters of full text, joined and lowercased. Keywords beginning at full-text offset 8,000 or later are not observable to this classifier.

| Priority | Trigger keyword(s) | Exact established label |
| --- | --- | --- |
| 1 | `gravity` | `引力模型与迁移流估计` |
| 2 | `hank` | `HANK模型与政策冲击分析` |
| 3 | `dynamic spatial` or `spatial general equilibrium` | `动态空间一般均衡模型` |
| 4 | `deep learning` or `neural` | `深度学习近似动态规划` |
| 5 | `difference-in-differences` or `instrument` | `准实验识别与计量估计` |
| 6 | `model` | `结构模型与数值模拟` |
| 7 | no trigger | `文献综述或理论分析` |

Synthetic cases may place a trigger in any accepted field. A search text containing all branch keywords returns the priority-1 label; a row's trigger plus lower-priority triggers returns that row's label. A fictional full text with `gravity` ending exactly at offset 8,000 returns the gravity label, while the same keyword beginning at offset 8,000 returns the fallback when title and abstract contain no trigger.

### Complete core-variable matrix and precedence

| Priority | Trigger keyword in title or abstract | Exact established label |
| --- | --- | --- |
| 1 | `migration` | `迁移流、城市便利性和就业机会` |
| 2 | `commuting` | `通勤联系、本地就业弹性和福利` |
| 3 | `housing` | `住房供给、价格约束和就业增长` |
| 4 | `monetary` | `货币政策冲击、收入分布和消费响应` |
| 5 | `hank` | `家庭异质性、资产分布和政策传导` |
| 6 | no trigger | `空间分布、异质性和政策响应` |

Synthetic cases use fictional places and studies. A title/abstract containing all branch keywords returns the priority-1 label; a row's trigger plus lower-priority triggers returns that row's label.

Safety-permitted change: invalid non-string inputs may be rejected with `TypeError` instead of being coerced. Such validation must not alter results for valid string inputs.

## 3. MSB-012/013: first-pass note generation

### Public interface and inputs

`make_note(payload: dict[str, Any], collection: str) -> str`

`payload` requires an `item` mapping. The established shape accepts `item.key`, `item.data`, and optional `attachments`, `online_supplements`, and `raw_data_quality`. Missing optional collections behave as empty collections. Missing title falls back to `Untitled`. `collection` is rendered as caller-supplied data.

### Observable output contract

- Return UTF-8-compatible Markdown as `str`, ending in exactly one newline.
- Produce YAML frontmatter followed by a title and the authorized template's major sections in stable order: basic information, one-sentence summary, research object, method, data source, conclusions, and analyst judgment. A workflow-status section may follow.
- Preserve stable frontmatter keys for Zotero identity, workflow tags, reading stage, evidence level, citation eligibility/status, usable purposes, evidence sources, research fields, and human-verification state.
- Use `reading_stage` value `初录入`; never represent automated output as human verified or E3 evidence.
- Preserve `zotero://select/library/items/<key>` when an item key is supplied and a PDF page link when a PDF key is available.
- Keep conclusion findings paired with their evidence indication. If evidence is insufficient, state the limitation instead of inventing a finding or page.
- HTML entities in metadata titles are decoded for display.
- Given equal inputs and an equal clock value, output is byte-for-byte deterministic.

The function performs no network access and no filesystem writes. The rewrite must obtain section order, headings, and template expression from the separately authorized template through an explicit runtime template boundary. Product Python must not reproduce the authorized template's headings, internal table rows, subheading skeleton, or instructional prompt skeleton. Output headings come only from the runtime template. A missing or structurally invalid template must fail closed with a clear exception before any write. No full-template fallback may be embedded in Python.

### Synthetic golden case

For a fictional item with key `FIC1001`, title `Migration in Fictional Harbor`, a 2025 date, one fictional author, no PDF, and metadata-only quality:

- output begins with frontmatter and ends with a newline;
- the display heading contains the fictional title;
- `reading_stage` is `初录入`;
- `evidence_level` is `E0` and `citation_eligible` is false;
- the Zotero select URI ends in `FIC1001`;
- major sections appear in template order;
- the output contains no asserted PDF page evidence.

## 4. MSB-016/017: deep-read note generation

### Public interface and inputs

`make_deep_note(payload: dict[str, Any], collection: str) -> str`

The input shape is the same general item payload. Deep-read callers normally supply a PDF attachment with cached full text. Missing optional collections remain safe. The function returns Markdown and does not itself write a file or contact a network.

### Observable output contract

- Preserve the same template-derived major-section order and stable frontmatter families as first-pass generation. Section headings must come only from the runtime template; product Python must not reproduce the authorized template's internal table, subheading, or prompt skeleton.
- Use `reading_stage` value `二次精读` and the `deep-read` workflow tag.
- Automated deep reading remains at most E2 candidate evidence and `human_verified: false`.
- Prefer supplied full-text evidence, but do not invent formulas, exact samples, exact page numbers, or strong conclusions when extraction is incomplete.
- Preserve evidence pairs for generated findings and expose limitations when stable page information is unavailable.
- Given equal inputs and an equal clock value, output is byte-for-byte deterministic.
- Machine-specific paths must never be introduced by defaults. A future safety rewrite may omit or redact an attachment path supplied by a caller; tests must not require disclosure of such paths.
- Missing or malformed authorized template data fails closed before any write, with no embedded full-template fallback.

### Synthetic golden case

For fictional item `FIC2002`, title `Housing Constraints in Northwind`, and a fictional PDF cache containing introduction, method, data, results, and conclusion prose:

- output contains the fictional title and Zotero item/PDF links;
- `reading_stage` is `二次精读`, evidence is no stronger than E2 candidate, and `human_verified` remains false;
- major sections occur in template order;
- a conclusion is accompanied by an evidence link or an explicit page-availability limitation;
- repeated generation under a frozen clock is identical.

## 5. MSB-026: online metadata helpers

### Pure normalization interfaces

The following signatures and return families are public compatibility surfaces:

- `clean_doi(value: str | None) -> str | None`: remove a leading DOI resolver URL or `doi:` label, surrounding whitespace, and a final period; return `None` for empty input.
- `abstract_from_openalex(index: dict[str, list[int]] | None) -> str`: reconstruct words in ascending position order; return an empty string when absent.
- `publication_year_from_crossref(message: dict[str, Any]) -> int | None`: use the first available year in established print, online, published, then issued priority.
- `normalize_title(value: str | None) -> str`: remove markup, lowercase ASCII alphanumerics, collapse separators, and return an empty string when absent.
- `title_similarity(left, right) -> float`: return deterministic set-token Jaccard similarity in `[0.0, 1.0]`, or `0.0` if either token set is empty.
- `title_matches(expected, found, threshold=0.5) -> bool`: preserve established containment-or-threshold matching for present titles. A rewrite may change missing-title handling from permissive to false when required to fail closed.
- `collect_oa_locations(payload) -> list[dict[str, str]]`: return Unpaywall locations before OpenAlex locations, normalize stable keys, and deduplicate by PDF/landing URL while retaining first occurrence.

### Network lookup interfaces

| Function | Required input | Success output | Failure output |
| --- | --- | --- | --- |
| `crossref_lookup(doi, email)` | DOI | Normalized mapping with DOI, title, venue/publisher/type/year/abstract/URL keys | `None` |
| `crossref_title_search(title, email)` | Title | Same normalized core plus `match_score` | `None` |
| `openalex_lookup(doi, title, email)` | DOI or title | Normalized mapping with identity, title/year/type/OA/abstract/location keys | `None` |
| `unpaywall_lookup(doi, email)` | DOI and email | Normalized DOI/OA/location mapping | `None` |

Lookups URL-encode caller data and use HTTPS service endpoints. The shared HTTP JSON boundary uses an explicit finite timeout (baseline default: 8 seconds), a non-empty user agent, JSON accept headers, and standard-library HTTP/JSON facilities. Network, decoding, malformed-shape, and empty-result failures return `None` from service lookups rather than leaking transport exceptions. Tests inject or mock the HTTP boundary; they never perform live requests.

`add_online_supplements(payload, email, skip_unpaywall=False) -> dict[str, Any]` mutates and returns the supplied payload for compatibility. It adds stable `online_supplements`, `raw_data_quality`, and `raw_data_buffer` keys. The supplement mapping contains `doi`, `title`, `warnings`, `crossref`, `openalex`, `unpaywall`, and `oa_locations`. Title mismatches are warned about and untrusted results are rejected or retried by title. `skip_unpaywall=True` prevents Unpaywall lookup. Partial or unavailable services yield explicit `None`/empty fields without fabricating metadata.

For OpenAlex aggregation specifically, a DOI lookup result whose title does not match the Zotero title must append an explicit OpenAlex mismatch warning and trigger exactly one title-search retry using no DOI. A retry result that validates against the Zotero title may be retained. A missing or still-mismatched retry is discarded. This aggregate behavior is deterministic and is tested with mocked service functions only.

When the input payload has a title but no DOI, the initial OpenAlex request is already a title search. If that result's title does not match the payload title, aggregation must append an explicit non-empty warning, reject the result, and stop. It must not repeat the same title search. This case is tested through the real lookup helper with only the shared HTTP JSON boundary mocked.

### Synthetic golden cases

| Input | Expected observable result |
| --- | --- |
| `clean_doi(" https://doi.org/10.5555/FICTION.7. ")` | `10.5555/FICTION.7` |
| OpenAlex inverted index `{"Northwind": [1], "Trade": [0]}` | `Trade Northwind` |
| Titles `"Northwind: Trade!"` and `"Northwind Trade"` | exact normalized match |
| Crossref mocked message for DOI `10.5555/fiction.7` | stable normalized mapping; markup removed from abstract |
| Any service mock raising a timeout | `None`; no retry loop at the service wrapper |
| Aggregate enrichment with all service results absent | supplement keys remain present with `None` results and an empty OA-location list |
| OpenAlex DOI result titled `Southern Health` for Zotero title `Northwind Trade`, followed by title-search result `Northwind Trade` | one explicit warning, one retry without DOI, and validated retry retained |
| No DOI, Zotero title `Northwind Trade`, and mocked OpenAlex title-search result `Southern Health` | one HTTP lookup, one explicit warning, mismatched OpenAlex result rejected, and no repeated title search |

## 6. Ordering, privacy, and intentional changes

All mapping/list ordering described above is deterministic. Covered functions do not write files. Only the service lookup layer may access the network in production, with finite timeout and public scholarly endpoints; test execution is offline.

Permitted safety/licensing changes are limited to template-driven rendering, clear failure for missing/malformed templates, stricter rejection when identity cannot be title-validated, redaction/omission of supplied local paths, and clearer warnings for partial metadata. These changes must preserve the public call signatures unless a separately documented compatibility decision is made.
