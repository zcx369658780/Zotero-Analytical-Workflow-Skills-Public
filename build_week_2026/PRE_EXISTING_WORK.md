# Pre-Existing Work

## Evidence boundary

The authoritative pre-Build-Week boundary is the annotated tag:

`pre-build-week-2026-public-baseline`

It resolves to:

`e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`

That commit was authored on 2026-06-26. Everything in its tree is treated as
pre-existing work and must not be presented as a new judged Build Week
feature.

## Repository contents at the protected tag

The protected tree contains 16 tracked files:

| Category | Contents at the protected tag |
|---|---|
| Repository documents | `.gitignore`, `LICENSE`, `README.md` |
| Skills | Three `SKILL.md` files for collection management, data fetching, and analytical writing |
| Python utilities | Nine scripts: one Zotero fetcher and eight collection, import, deep-read, migration, and safety utilities |
| Template | `templates/论文精读模板.md` |

## Pre-existing capabilities

The following capabilities already existed and are not competition-period
product work:

- fetching Zotero metadata, annotations, and cached text;
- batch queue generation and resumable collection processing;
- initial note import and deep-read upgrade workflows;
- evidence-schema planning and sample-only migration execution;
- Obsidian literature-note formatting;
- evidence levels E0 through E3 and citation-eligibility metadata;
- dry-run planning, explicit write gates, no-overwrite defaults, backups, and
  diff summaries; and
- public-source metadata fallback and data-quality downgrade behavior.

## Pre-existing safety invariants

The protected baseline already required:

- read-only behavior unless writing is explicitly authorized;
- `--write` for actual output and `--overwrite` before replacing Markdown;
- `--dry-run` to override write intent;
- `human_verified: false` for machine-generated notes;
- no automatic E3 or `citation_eligible: true` promotion;
- sample-only and explicit vault-write gates for evidence migration;
- no fabricated methods, findings, locators, formulas, or missing details; and
- no unlicensed full-text acquisition.

ScholarTrace inherits these safety principles, but inheriting principles does
not make the ScholarTrace product feature pre-existing.

## Attribution and licensing

Five fixed upstream-derived counterparts in the protected baseline are
separately licensed under `UPSTREAM_PERMISSION_FINAL.md` and excluded from the
downstream MIT License:

- `README.md`;
- `skills/zotero-collection-manager/SKILL.md`;
- `skills/zotero-data-fetcher/SKILL.md`;
- `skills/zotero-analytical-writer/SKILL.md`; and
- `templates/论文精读模板.md`.

The protected baseline remains the provenance anchor for those file versions.
This scope gate neither changes their content nor claims them as new work.

## Explicit exclusion from the new judged feature

At the protected tag there was no ScholarTrace / Evidence Gate module, claim
verdict taxonomy, demonstration fixture set, deterministic claim-audit
pipeline, ScholarTrace CLI, or ScholarTrace evaluation suite. The existing
workflow is context and infrastructure; the independently developed
ScholarTrace extension is the proposed competition-period product work.
