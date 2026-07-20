# Post-Rewrite Provenance and Rights Report

Date: 2026-07-21

## Phase A disposition

Eighteen of the authorized maximum twenty public GitHub searches were performed. No new exact source was found.

| Block | Final Phase A disposition | Rewrite treatment |
|---|---|---|
| MSB-010 | `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH` | Replaced by separated data-driven clean rewrite |
| MSB-012 | `EXACT_EXISTING_PERMISSION_SOURCE_CONFIRMED` | Embedded expression removed; template is runtime data only |
| MSB-013 | `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH` | Generator control replaced by neutral-ID renderer boundary |
| MSB-016 | `EXACT_EXISTING_PERMISSION_SOURCE_CONFIRMED` | Embedded expression removed; template is runtime data only |
| MSB-017 | `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH` | Generator control replaced by neutral-ID renderer boundary |
| MSB-026 | `NO_EXACT_SOURCE_AFTER_BOUNDED_SEARCH` | Replaced by standard-library-only metadata client |

No permissively licensed exact source was retained. No supplemental notice, third-party license file, README change, or author request is required.

## Final comparison

Comparison normalized Unicode with NFKC, normalized line endings and whitespace, removed blank lines, and used ordered `SequenceMatcher` line similarity. Long string constants of at least 30 characters and short ordered template expression were reviewed separately.

| Rewritten corpus | Baseline old-block similarity | Non-generic overlap |
|---|---:|---|
| MSB-010 | 0.0588 | None |
| MSB-012/013 | 0.1574 | None |
| MSB-016/017 | 0.1310 | None |
| MSB-026 | 0.2355 | None; official API endpoints only |

Maximum similarity for each accepted candidate:

```text
MSC-001 .0000  MSC-002 .0217  MSC-003 .0298  MSC-004 .0367
MSC-005 .0242  MSC-006 .0615  MSC-007 .0498  MSC-008 .0276
MSC-009 .0228  MSC-010 .0422  MSC-011 .0075  MSC-012 .0061
MSC-013 .0147  MSC-014 .0211  MSC-015 .0075  MSC-016 .0320
MSC-017 .0323  MSC-018 .0000  MSC-019 .0000  MSC-020 .0769
MSC-021 .0338  MSC-022 .0671  MSC-023 .0385  MSC-024 .0000
```

Only standard imports, public compatibility signatures, generic type/control-flow expression, and official Crossref/OpenAlex endpoint strings remain. The rewritten renderers contain no authorized template headings, table skeleton, internal prompts, or fallback body.

## Rights conclusion

- The five fixed cheneternity counterparts remain covered by the existing written permission and mixed-license boundary.
- No code or protected expression from cheneternity's historical scripts, `zbw0520`, `Enthoes1`, or another candidate is retained in the rewritten blocks.
- The authorized template remains separately licensed and is read at runtime; its expression is no longer duplicated into Python.
- No reciprocal, incompatible, no-license, or ambiguous external code remains in MSB-010, MSB-012/013, MSB-016/017, or MSB-026.
- Final determination: only generic/API/interface overlap remains.
