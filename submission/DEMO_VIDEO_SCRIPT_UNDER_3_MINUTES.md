# Demo Video Script Under Three Minutes

Target duration: 2 minutes 45 seconds. Use voiceover and screen capture only; do not add copyrighted music.

## 0:00-0:15 - Project Identity

**Shot:** Show the public GitHub repository title and the English README pitch. Keep browser notifications and account details hidden.

**Voiceover:** "This is Zotero Analytical Workflow Skills, a privacy-conscious Codex Skill bundle that connects Zotero reading material to structured, evidence-labeled Obsidian notes."

## 0:15-0:35 - Three-Skill Architecture

**Shot:** Scroll to the architecture table, then show the three public Skill directories.

**Voiceover:** "The workflow has three parts. The fetcher prepares source evidence, the analytical writer guides Codex's semantic reading, and the collection manager coordinates resumable batches, deep reading, and safe writes."

## 0:35-0:50 - Installation And Discoverability

**Shot:** Show the repository's `skills/` tree and the three public `agents/openai.yaml` files. Show only placeholders such as `<codex_home>`.

**Voiceover:** "Each directory installs as a Codex Skill with bundled scripts and agent metadata. The literature template is placed under the user's Codex template directory."

## 0:50-1:15 - Synthetic Daily Workflow

**Shot:** Use the README diagram and a synthetic item label such as `SYNTHETIC_ITEM`. Do not open Zotero, PDFs, Obsidian, or a real local path.

**Voiceover:** "In daily use, a researcher selects material they own in Zotero. The fetcher organizes metadata, annotations, or cached text. Codex reasons over that supplied evidence, and the writer produces a structured Chinese note. The manager repeats the process safely across a collection. No private research content is included in this demo or repository."

## 1:15-1:38 - Dry-Run And Safety

**Shot:** Show `--help`, a dry-run command with placeholders, and the README safety section.

**Voiceover:** "The scripts default to planning. A write requires an explicit flag, and overwriting existing Markdown needs separate authorization. Evidence labels remain conservative, missing content is not invented, and human review is required before citation."

## 1:38-1:58 - Offline Judge Test

**Shot:** Run `python -m unittest discover -s tests -v` and show the final `Ran 24 tests` and `OK` lines. Then open the Judge Testing Guide.

**Voiceover:** "Judges can verify the release offline with synthetic fixtures and mocked metadata responses. Twenty-four deterministic tests cover classifiers, template fail-closed behavior, rendering, and metadata normalization without a private Zotero library."

## 1:58-2:20 - Pre-Existing Versus Build Week Work

**Shot:** Show the Build Week evidence table and protected baseline reference.

**Voiceover:** "The core three Skills and daily workflow pre-existed Build Week. During the event, we integrated permission and mixed licensing, audited privacy and provenance, independently rewrote unresolved blocks, added safety tests and agent metadata, synchronized the real installation, and prepared this release candidate."

## 2:20-2:35 - Codex And GPT-5.6

**Shot:** Show the README collaboration section and clean-rewrite acceptance report. Do not show a Session ID or private transcript.

**Voiceover:** "Codex with GPT-5.6 helped plan bounded gates, inspect and refactor the workflow, test behavior, review provenance, synchronize the Skills, and document the final release. There is no separate runtime OpenAI API adapter."

## 2:35-2:45 - Attribution And Close

**Shot:** Show the upstream attribution and mixed-licensing links.

**Voiceover:** "Upstream attribution and the mixed-license boundary are preserved in the repository. Zotero Analytical Workflow Skills is ready for judges to test without exposing private research data."

## Recording Safety Check

- Use no private Zotero items, PDF content, annotations, vault paths, credentials, email, notifications, browser profiles, backup paths, or Session IDs.
- Use no copyrighted music or unlicensed media.
- Refer to Zotero, Codex, Obsidian, and GitHub descriptively without implying endorsement.
- Confirm the final public video is under three minutes and has audible English narration.
