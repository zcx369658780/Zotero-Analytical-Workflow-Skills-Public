# Zotero Analytical Workflow Skills

**A privacy-conscious Codex Skill bundle that turns a Zotero reading library into structured, evidence-labeled Obsidian literature notes.**

## Overview

Zotero Analytical Workflow Skills connects three reusable Codex Skills into one daily literature workflow: retrieve source material from Zotero, reason over it with Codex, and organize the result as structured Obsidian notes. Deterministic Python scripts handle extraction, resumable queues, template rendering, evidence labels, dry-run planning, guarded writes, and metadata interoperability. Final semantic analysis and writing happen when Codex executes the Skills.

Normal use does not require a separate OpenAI API key. GPT-5.6 is used through the user's Codex environment rather than through an additional runtime API client in this repository.

## 中文概览

这是一个连接 Zotero、Codex 和 Obsidian 的三 Skill 文献工作流：先提取文献语料，再由 Codex 完成语义分析和中文逻辑重构，最后生成带证据等级的结构化笔记。Python 脚本负责队列、断点续跑、模板渲染、默认 dry-run、安全写入和元数据互操作；公开仓库不包含私人研究资料或机器路径。

## Architecture And Data Flow

```text
Zotero library owned by the user
  -> zotero-data-fetcher
     metadata, annotations, cached full text, evidence quality
  -> zotero-analytical-writer
     Codex/GPT-5.6 semantic analysis and structured Chinese writing
  -> zotero-collection-manager
     collection queue, resumable batch flow, deep-read upgrade, safety gates
  -> Obsidian literature notes owned by the user
```

| Skill | Responsibility | Deterministic support |
|---|---|---|
| `zotero-data-fetcher` | Retrieve one item's source corpus without translating or inventing content | Local API/SQLite fallback, attachment and annotation extraction, metadata normalization |
| `zotero-analytical-writer` | Restructure supplied evidence into the authorized literature-note format | Evidence and human-review rules defined in the Skill and template |
| `zotero-collection-manager` | Coordinate collections, resumable imports, deep-read upgrades, and migration audits | Queues, logs, dry-run plans, guarded writes, backups, diff summaries |

## Features

| Feature | Behavior |
|---|---|
| Resumable collection processing | Builds queues by Zotero collection and skips completed item keys |
| Evidence-aware notes | Distinguishes metadata, online abstract, annotation, and local full-text evidence |
| Two-stage reading | Supports first-pass import and a deeper pass only when local full-text evidence exists |
| Runtime template contract | Loads the separately licensed template as data and fails closed when it is missing or malformed |
| Safe writes | Defaults to dry-run; writing and overwriting require explicit flags |
| Migration audit | Plans existing-note evidence updates without writing, with a separately gated sample-only executor |
| Public sanitization | Uses placeholders instead of private paths, collections, credentials, logs, or research records |

## Installation

Clone or download the repository. Copy the three directories under `skills/` into the Codex Skill directory, preserving their names and bundled files:

```text
<codex_home>/skills/zotero-collection-manager/
<codex_home>/skills/zotero-data-fetcher/
<codex_home>/skills/zotero-analytical-writer/
```

Copy the template to:

```text
<codex_home>/templates/论文精读模板.md
```

On a standard Windows Codex installation, `<codex_home>` is commonly `%USERPROFILE%\.codex`. Use your own installation location and replace every public placeholder such as `<note_root>`, `<vault_root>`, `<zotero_data_dir>`, and `<workflow_root>` with a path you control.

## Supported Platforms And Prerequisites

- Windows-oriented and tested with CPython 3.11.
- Codex with Skill support; GPT-5.6 is used inside that environment.
- Zotero and Obsidian are needed only for an optional personal end-to-end trial.
- Other operating systems may require path and Zotero-profile adjustments.
- No separate OpenAI API key or hosted service is required for normal use.

## Quick Start

Inspect the available commands first:

```bash
python skills/zotero-collection-manager/scripts/zotero_collection_queue.py --help
python skills/zotero-collection-manager/scripts/batch_import_collection.py --help
python skills/zotero-collection-manager/scripts/deep_read_collection.py --help
python skills/zotero-data-fetcher/scripts/zotero_fetch.py --help
```

Build a collection queue and preview a first-pass import. Both examples remain read-only without `--write`:

```bash
python skills/zotero-collection-manager/scripts/zotero_collection_queue.py --collection "<collection_name>" --recursive --note-root "<note_root>"
python skills/zotero-collection-manager/scripts/batch_import_collection.py --collection "<collection_name>" --recursive --note-root "<note_root>"
```

Only after reviewing the plan should a user authorize a write:

```bash
python skills/zotero-collection-manager/scripts/batch_import_collection.py --collection "<collection_name>" --recursive --note-root "<note_root>" --write
```

Overwriting an existing Markdown note additionally requires `--overwrite`. Evidence migration has stricter sample-only and vault-write gates documented in the collection-manager Skill.

## Judge Testing Without Private Data

Judges can validate the release without Zotero, Obsidian, PDFs, or private research files:

```bash
python -m unittest discover -s tests -v
```

The expected minimum is `24/24` passing offline tests. The tests use synthetic fixtures and mocked metadata responses. Safe `--help` commands above also exercise CLI imports without opening a Zotero database or writing a note. The complete reproducible path is in the [Judge Testing Guide](submission/JUDGE_TESTING_GUIDE.md).

## Safety Model

- **Privacy:** no Zotero database, PDF, annotation, Obsidian vault, research note, purchased data, credential, processing log, or private backup is included.
- **No overwrite by default:** scripts plan first; `--write` is explicit, and existing Markdown requires `--overwrite`.
- **Evidence limits:** scripts do not promote records to human-verified evidence or invent missing methods, conclusions, page numbers, or formulas.
- **Human review:** generated notes remain review candidates. Users are responsible for checking source evidence before citation.
- **No hidden runtime API:** public metadata interoperability is optional; Codex/GPT-5.6 semantic work occurs in Codex, not through a bundled OpenAI API adapter.

## Pre-Existing Work And Build Week 2026 Additions

The core three Skills and their daily Zotero-to-Obsidian capabilities pre-existed OpenAI Build Week 2026. They must not be evaluated as newly created during the submission period.

Build Week work meaningfully extended and prepared the real bundle by integrating upstream permission and mixed licensing, synchronizing a sanitized public/local Skill identity, adding `agents/openai.yaml` discovery metadata, auditing privacy and source provenance, independently rewriting unresolved functional blocks, adding deterministic safety tests, completing final provenance acceptance, and packaging judge and submission materials. See [Build Week New Work Evidence](submission/BUILD_WEEK_NEW_WORK_EVIDENCE.md).

## How Codex And GPT-5.6 Were Used

Codex with GPT-5.6 was used to plan bounded gates, inspect the existing workflow, reconstruct provenance, refactor unresolved blocks under clean separation, test deterministic behavior, review privacy and licensing, safely synchronize the installed Skills, and prepare this release candidate. The work improved auditability, safety, and release readiness without presenting pre-existing workflow capabilities as new.

During normal use, Codex executes the three Skills and performs the semantic reading and writing. The bundled Python code provides deterministic extraction, queuing, rendering, safety gates, and metadata interoperability.

## Repository Structure

```text
skills/                 three installable Codex Skills and bundled scripts
templates/              authorized literature-reading template
tests/                  offline deterministic behavior and safety tests
build_week_2026/        audit evidence, not a separate product
submission/             judge, video, Devpost, and manual-submission materials
```

## Upstream Attribution And Mixed Licensing

This project adapts and extends [cheneternity/Zotero-Analytical-Workflow-Skills](https://github.com/cheneternity/Zotero-Analytical-Workflow-Skills) by Eternity Chen (`cheneternity`).

The five fixed upstream-derived counterparts are `README.md`, the three `SKILL.md` files, and `templates/论文精读模板.md`. They are governed by the repository-limited permission in [UPSTREAM_PERMISSION_FINAL.md](UPSTREAM_PERMISSION_FINAL.md) and are separately licensed; they are not covered by the downstream MIT License. The root `LICENSE` applies only to independently authored downstream material that the repository owner may license under MIT.

Read the complete boundary in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), [LICENSE_SCOPE.md](LICENSE_SCOPE.md), [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md), and [FILE_MAPPING_AND_HASH_MANIFEST.md](FILE_MAPPING_AND_HASH_MANIFEST.md).

## Judge And Submission Links

- [Judge Testing Guide](submission/JUDGE_TESTING_GUIDE.md)
- [Build Week Evidence Index](build_week_2026/README.md)
- [Final Provenance and Rights Acceptance Report](build_week_2026/FINAL_PROVENANCE_AND_RIGHTS_ACCEPTANCE_REPORT.md)
- [Devpost Submission Copy](submission/DEVPOST_SUBMISSION_COPY.md)
- [Under-Three-Minute Demo Script](submission/DEMO_VIDEO_SCRIPT_UNDER_3_MINUTES.md)
- [Manual Submission Checklist](submission/MANUAL_SUBMISSION_CHECKLIST.md)
