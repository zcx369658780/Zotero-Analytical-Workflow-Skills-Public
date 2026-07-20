# Devpost Submission Copy

## Project Title

Zotero Analytical Workflow Skills

## Tagline

A privacy-conscious Codex Skill bundle for turning Zotero research material into structured, evidence-labeled Obsidian literature notes.

## Recommended Track

Education

Education is the strongest fit because the project helps students and researchers practice repeatable literature reading, evidence labeling, source-aware writing, and human verification while keeping their learning and research materials under their own control.

## Project Overview

Researchers and students often collect papers in Zotero but still move manually between metadata, PDF notes, analytical reading, and an Obsidian knowledge base. Zotero Analytical Workflow Skills connects that work through three installable Codex Skills. It retrieves source material, guides evidence-aware semantic analysis, and coordinates safe, resumable note production.

The project is a real daily-use developer tool rather than a hosted application. Codex executes the Skills, while deterministic Python scripts handle extraction, queueing, template rendering, evidence labels, dry-run plans, write gates, and optional public metadata interoperability.

## Problem And Target Users

The target users are students, researchers, and knowledge workers who use Zotero and Obsidian and want a repeatable literature-reading workflow without uploading a private library to a new hosted service. The project addresses fragmented tooling, accidental overwrites, weak evidence labeling, and the difficulty of processing a collection consistently over multiple sessions.

## What The Project Does

- Retrieves a Zotero item by item key or title and organizes metadata, annotations, cached full text, and evidence quality.
- Uses Codex to transform supplied source material into structured Chinese analytical notes.
- Builds resumable collection queues and supports first-pass import and evidence-bounded deep reading.
- Loads an authorized note template at runtime and fails closed if the template contract is missing or malformed.
- Defaults to dry-run and requires explicit authorization for writes and overwrites.
- Provides offline synthetic tests so judges can verify the release without private Zotero or Obsidian data.

## How The Three Skills Work Together

`zotero-data-fetcher` prepares the source corpus without translating or inventing content. `zotero-analytical-writer` tells Codex how to reason over that corpus and produce the structured note. `zotero-collection-manager` coordinates collections, progress, safe writes, deep-read upgrades, and evidence migration audits.

## Privacy And Safety Design

The public repository contains no private Zotero database, PDF, annotation, Obsidian vault, research note, purchased data, credential, processing log, or machine-specific path. Public placeholders must be replaced by paths owned by the user. Scripts plan before writing, require `--write` for changes, and require `--overwrite` for existing Markdown. Evidence labels never imply automatic human verification.

## Pre-Existing Work

The three core Skills and their daily Zotero-to-Obsidian capabilities existed before OpenAI Build Week 2026. Those capabilities are not claimed as newly built during the submission period.

## Meaningful Build Week Extensions

Build Week work integrated upstream permission and mixed licensing, synchronized a sanitized public and installed Skill identity, added agent discovery metadata, audited privacy and multi-source provenance, independently rewrote unresolved functional blocks, added deterministic safety tests, completed final provenance acceptance, and prepared a judge-ready release package.

## How Codex And GPT-5.6 Were Used

Codex with GPT-5.6 was used to plan bounded implementation gates, inspect the existing workflow, reconstruct provenance, perform separated clean rewrites, test deterministic behavior, review privacy and licensing, synchronize the real installed Skills, and curate the final release. In normal use, GPT-5.6 operates through Codex while executing the Skills; this repository does not add a separate OpenAI runtime API client.

## Repository And Testing

Repository: `https://github.com/zcx369658780/Zotero-Analytical-Workflow-Skills-Public`

Clone or download the repository and run:

```bash
python -m unittest discover -s tests -v
```

The expected minimum is 24 passing offline tests. The repository also provides safe CLI `--help` checks and a complete judge guide. No Zotero database, Obsidian vault, or API key is needed for offline verification.

## Third-Party And Licensing Disclosure

The project adapts and extends `cheneternity/Zotero-Analytical-Workflow-Skills` by Eternity Chen. Five fixed upstream-derived counterparts are covered by written repository-limited permission and are separately licensed. Independently authored downstream material may be covered by the root MIT License. Full attribution, permission, notices, scope, and file mapping are linked from the repository README.

## Limitations And Supported Environment

The workflow is Windows-oriented and tested with CPython 3.11. Other systems may need path and Zotero-profile adjustments. A personal end-to-end trial requires the user's own Zotero and Obsidian installations and should begin in dry-run mode. Generated analytical notes require human review before citation.
