# OpenAI Build Week 2026 — Final YouTube Demo Video Production Gate

Date: 2026-07-21  
Executor: Codex CLI / Codex Desktop  
Repository: `zcx369658780/Zotero-Analytical-Workflow-Skills-Public`  
Working branch: `build-week-2026-video-production`  
Accepted release-candidate `main`: `a6bc117b12d91003691d57ba76e972621d356584`  
Accepted RC tag: `openai-build-week-2026-submission-rc1`  
Task type: external media production only; no product/repository release changes

## 0. Goal and user authorization

Create a complete, upload-ready English demo video for the OpenAI Build Week 2026 submission without requiring the user to record English narration or manually edit footage.

The user explicitly authorizes AI-generated English narration.

The final deliverable must be a clear, truthful, public-safe demo of the real daily-use Zotero + Codex + Obsidian Skill bundle already released on `main`. It must not add or imply new product functionality.

The video must satisfy the official submission requirements:

- total duration at or below 3 minutes, with a target of 2:35–2:50;
- English narration;
- clear demonstration of the working project;
- explanation of what was built;
- specific explanation of how Codex was used;
- specific explanation of how GPT-5.6 was used;
- suitable for upload as a **public YouTube video**;
- no copyrighted music, unlicensed images, private data, or misleading claims.

This gate produces the video package locally. It MUST NOT log in to YouTube, upload the video, change visibility, enter Devpost, submit the project, or publish a private `/feedback` Session ID.

## 1. Authoritative product boundary

The submission product is exactly:

1. `zotero-collection-manager`;
2. `zotero-data-fetcher`;
3. `zotero-analytical-writer`;
4. their bundled Python scripts/modules and `agents/openai.yaml` metadata; and
5. `templates/论文精读模板.md`.

The video must not present ScholarTrace, EvidenceGate, a runtime OpenAI API adapter, a hosted application, SaaS, or deployment as the submission product.

Normal use does not require `OPENAI_API_KEY`. GPT-5.6 is used through Codex for building and executing the Skill workflow, while the Python modules provide deterministic extraction, queuing, template rendering, safety gates, and scholarly metadata interoperability.

## 2. Repository and Git preflight

Before media work:

1. run `git fetch origin --tags`;
2. verify repository identity and accepted SSH/HTTPS origin;
3. verify `origin/main` and local `main` equal `a6bc117b12d91003691d57ba76e972621d356584`;
4. verify annotated tag `openai-build-week-2026-submission-rc1` peels to the same commit;
5. verify protected tag `pre-build-week-2026-public-baseline` peels to `e76fb0bb7f3523a608bd8abe231d7e7f8ffa678e`;
6. verify the current video branch descends directly from the accepted RC and contains only this governing task-file commit after it;
7. verify the working tree is clean;
8. stop on repository or history mismatch.

Do not modify or push `main`. Do not merge the video branch. Do not create a release or new product tag.

## 3. Required source materials

Read only the public release-candidate repository files needed to create the video:

- `README.md`;
- `submission/DEMO_VIDEO_SCRIPT_UNDER_3_MINUTES.md`;
- `submission/DEVPOST_SUBMISSION_COPY.md`;
- `submission/JUDGE_TESTING_GUIDE.md`;
- `submission/BUILD_WEEK_NEW_WORK_EVIDENCE.md`;
- `submission/ASSET_PRIVACY_AND_COPYRIGHT_CHECKLIST.md`;
- `build_week_2026/README.md`;
- `build_week_2026/FINAL_PROVENANCE_AND_RIGHTS_ACCEPTANCE_REPORT.md`;
- `build_week_2026/FINAL_SUBMISSION_READINESS_CHECKPOINT.md`;
- the three `SKILL.md` files;
- the three `agents/openai.yaml` files;
- the public directory tree and safe command outputs generated in this task.

Do not access:

- private Zotero databases, item titles, notes, annotations, PDFs, or attachments;
- Obsidian vaults or private research notes;
- private browser tabs, email, notifications, credentials, Downloads, backups, or private repositories;
- private Codex transcript content or `/feedback` Session ID;
- the ScholarTrace experimental branch;
- real scholarly metadata services or any model/API.

## 4. External working directory

Create one new external working directory outside the Git repository:

`%USERPROFILE%\Videos\OpenAI_Build_Week_2026_Zotero_Skills\`

If it already exists and is non-empty, create a new timestamped sibling rather than overwriting it.

All generated media, temporary frames, virtual environments, package caches, logs, audio, subtitles, scripts, and final deliverables must stay outside the Git repository.

Do not stage or commit video assets or production dependencies.

## 5. Tooling strategy

Use a fully automated, reproducible local production route.

Preferred stack:

- Python 3.11 or the available compatible Python;
- Pillow for generated visuals;
- FFmpeg for encoding, muxing, loudness normalization, and inspection;
- an AI text-to-speech engine usable without an API key, preferably `edge-tts`, for English narration;
- `imageio-ffmpeg` may be used to obtain a task-local FFmpeg binary if no system FFmpeg is available.

Tool rules:

1. First detect existing Python, FFmpeg, Pillow, and a usable TTS command.
2. If dependencies are missing, create an isolated virtual environment inside the external working directory.
3. Installing task-local PyPI packages in that external environment is authorized only for video production. Do not install globally and do not modify repository dependency files.
4. Record exact package names, versions, source URLs, and detected licenses in the private production report.
5. Do not download fonts, images, music, icons, video templates, or web assets.
6. Use only system fonts already present on the machine. Do not copy or redistribute font files.
7. Do not use background music.
8. Do not use OpenAI API or any paid/secret-key TTS service.
9. Do not use browser automation or desktop screen capture that could expose private UI.

Preferred narration voice:

- first choice: `en-US-JennyNeural`;
- fallback AI voice: another clear English neural voice available through the same tool;
- final fallback: an installed Windows English SAPI voice if online AI TTS is unavailable.

Use pronunciation-safe narration text, while subtitles retain correct written names. Examples:

- narration may pronounce Zotero as “zoh-TAIR-oh”;
- pronounce Codex clearly as “Co-dex”;
- pronounce GPT-5.6 as “G P T five point six”;
- pronounce YAML as “YAML” or “Yam-ul”.

If no usable narration engine or video encoder is available after the bounded task-local setup, stop with a precise blocker. Do not fabricate a completed video.

## 6. Visual strategy: generated and repository-grounded

Create a polished 1920×1080, 30 fps, text-and-diagram-led product demo using only public repository content and exact task-generated verification outputs.

Do not use third-party logos, screenshots, stock media, web images, copyrighted music, or screenshots of private interfaces.

Use generated visual components such as:

- project title cards;
- animated architecture flow: `Zotero → Codex / GPT-5.6 → Obsidian`;
- directory-tree panels for the three Skills;
- excerpts from public `agents/openai.yaml` metadata;
- safe generic installation paths with placeholders;
- terminal-style panels containing exact outputs from commands run in this task;
- diagrams for dry-run, explicit write, no-overwrite, evidence, and privacy gates;
- a pre-existing-versus-Build-Week comparison timeline;
- a Codex/GPT-5.6 collaboration panel;
- an attribution and mixed-license panel;
- a final repository URL and `Education` track card.

Do not show an actual Windows username or private absolute path. Use placeholders such as:

- `<codex_home>`;
- `<note_root>`;
- `<vault_root>`;
- `<zotero_data_dir>`.

## 7. Required real verification footage/evidence

The visual demo must include actual, freshly generated command evidence from accepted `main`, rendered as animated terminal-style panels rather than a private desktop capture.

Run and capture sanitized output for at least:

1. `git rev-parse HEAD`;
2. `git describe --tags --exact-match` or an equivalent tag verification;
3. `python -m unittest discover -s tests -v` with the expected `24/24` pass result;
4. representative safe `--help` output for:
   - `zotero_collection_queue.py`;
   - `batch_import_collection.py`;
   - `deep_read_collection.py`;
   - `zotero_fetch.py`;
5. a safe public directory tree showing the three Skills, agent metadata, scripts, and template;
6. static validation that normal use does not require an API key and the repository imports no OpenAI SDK.

Sanitize command prompts and paths before rendering. Do not alter substantive test results.

## 8. Required narrative content

Use `submission/DEMO_VIDEO_SCRIPT_UNDER_3_MINUTES.md` as the starting source, but produce a final narration optimized to the actual scene timing.

The final voiceover must accurately cover:

1. **Problem and audience** — researchers and students need a safe way to transform their own Zotero libraries into structured Obsidian notes without publishing their research data.
2. **Product** — three installable Codex Skills for fetching, analytical writing, and collection-level orchestration.
3. **Workflow** — Zotero supplies user-controlled source material, Codex executes the Skills with GPT-5.6 semantic reasoning, and Obsidian receives structured notes only after explicit write authorization.
4. **Safety** — dry-run by default, explicit `--write`, no-overwrite controls, evidence levels, `human_verified: false`, no automatic E3 promotion, and no private data in the public repository.
5. **Working evidence** — offline tests, safe CLI help, and repository structure.
6. **Pre-existing boundary** — the core three-Skill workflow pre-existed Build Week and must not be described as newly built during the event.
7. **Build Week additions** — permission and mixed-licensing integration, public/local synchronization, agent metadata, privacy and multi-source provenance audits, independent rewrites of unresolved blocks, 24 offline tests, final provenance acceptance, and release packaging.
8. **Codex usage** — Codex helped inspect the real installation, plan gates, compare local/public files, perform source audits, implement isolated rewrites, test, document, and safely synchronize the production Skills.
9. **GPT-5.6 usage** — GPT-5.6 was the reasoning model used inside the primary Codex build workflow for planning, code analysis, refactoring decisions, provenance reasoning, documentation, and Skill execution; the project does not require a second runtime API key.
10. **Attribution** — acknowledge Eternity Chen / `cheneternity` and state that five fixed counterparts remain separately licensed under the repository permission and mixed-licensing files.
11. **Closing** — identify the public repository, Education track, and no-private-data boundary.

Do not claim:

- that private research content is included;
- that an OpenAI runtime API integration exists;
- that ScholarTrace is part of the project;
- that all core functionality was built during Build Week;
- user counts, adoption, awards, performance metrics, or external validation not supported by evidence;
- that the project has already been submitted.

## 9. Scene and timing requirements

Target 10–12 scenes and a final duration between 155 and 170 seconds.

Recommended sequence:

1. title, user problem, and Education audience;
2. three-Skill architecture;
3. repository structure and installation;
4. safe daily workflow using synthetic/redacted diagrams;
5. dry-run, explicit write, no-overwrite, and evidence model;
6. actual test run showing `24/24`;
7. safe CLI and judge testing path;
8. pre-existing versus Build Week additions;
9. Codex workflow and key decisions;
10. GPT-5.6 role without runtime API key;
11. upstream attribution, mixed licensing, and privacy;
12. repository URL and closing.

Generate and preserve a scene timing CSV containing:

- scene number;
- title;
- narration start/end;
- visual start/end;
- narration text;
- on-screen text;
- source repository path or command evidence.

## 10. Narration and subtitles

Generate:

- the final English narration audio;
- a clean narration transcript;
- a pronunciation-adjusted TTS input file;
- an English `.srt` subtitle file;
- burned-in English captions using a safe readable font and high contrast.

Audio requirements:

- intelligible voice at normal playback speed;
- no clipping;
- no background music;
- normalize approximately to YouTube-appropriate spoken-word loudness using FFmpeg loudness normalization;
- avoid excessive silence;
- do not time-stretch narration so aggressively that it becomes unnatural.

Caption requirements:

- accurate spelling even when TTS input uses pronunciation hints;
- readable on a 1080p frame;
- placed inside title-safe margins;
- no more than two lines at a time where practical;
- synchronized to the narration.

## 11. Final video encoding

Create the upload-ready file:

`Zotero_Analytical_Workflow_Skills_OpenAI_Build_Week_2026.mp4`

Required properties:

- container: MP4;
- video: H.264;
- pixel format: `yuv420p`;
- resolution: 1920×1080;
- frame rate: 30 fps;
- audio: AAC, 48 kHz;
- duration: no more than 180.000 seconds;
- no missing audio stream;
- no copyrighted music;
- seekable and playable by FFprobe/FFmpeg;
- YouTube-compatible metadata and encoding.

Also create a 1280×720 thumbnail:

`Zotero_Analytical_Workflow_Skills_YouTube_Thumbnail.png`

The thumbnail must use only generated typography and shapes, contain no third-party logos, and stay below 2 MB where practical.

## 12. Final deliverable package

The external working directory must contain at least:

1. `Zotero_Analytical_Workflow_Skills_OpenAI_Build_Week_2026.mp4`;
2. `Zotero_Analytical_Workflow_Skills_OpenAI_Build_Week_2026.srt`;
3. `Zotero_Analytical_Workflow_Skills_YouTube_Thumbnail.png`;
4. `FINAL_NARRATION_TRANSCRIPT.md`;
5. `TTS_INPUT_PRONUNCIATION_ADJUSTED.txt`;
6. `SCENE_TIMING_AND_SOURCE_MANIFEST.csv`;
7. `YOUTUBE_UPLOAD_METADATA.md`;
8. `VIDEO_PRIVACY_COPYRIGHT_AND_TECHNICAL_QC_REPORT.md`;
9. `VIDEO_ASSET_SHA256_MANIFEST.csv`;
10. the private build scripts and dependency/version report needed to reproduce the video.

`YOUTUBE_UPLOAD_METADATA.md` must provide:

- recommended title;
- concise English description;
- repository URL;
- Education track statement;
- upstream attribution and mixed-license link summary;
- suggested tags;
- explicit instruction to choose **Public**, not Unlisted or Private;
- instruction to verify audio, captions, 1080p processing, and duration before using the URL in Devpost;
- no private `/feedback` Session ID.

## 13. Quality control

Before declaring success, verify and report:

### Technical

- FFprobe duration at or below 180 seconds;
- expected resolution, frame rate, codecs, pixel format, and audio sample rate;
- video and audio streams decode without errors;
- final MP4 file size and SHA256;
- subtitle parse and final cue time within video duration;
- thumbnail dimensions and size;
- narration duration and loudness normalization result.

### Content

- all required official topics are spoken: project, Codex, GPT-5.6;
- core pre-existing functionality is explicitly distinguished from Build Week additions;
- no runtime OpenAI API key is claimed or required;
- no ScholarTrace/API experiment appears;
- no unsupported metric or submission-complete claim appears;
- project name and repository URL are correct;
- track is Education.

### Privacy and copyright

- no credentials, API keys, private paths, emails, notifications, private item titles, PDF text, vault notes, purchased data, private Session ID, or backup path appears in video, subtitles, thumbnail, metadata, or transcript;
- no external image, logo, copyrighted music, downloaded font, or unlicensed media is used;
- all visuals are generated from public repository text, shapes, and sanitized command evidence;
- upstream attribution is accurate.

### Visual

Create contact-sheet images at representative timestamps and inspect them for:

- text clipping;
- unreadable contrast;
- caption overlap;
- private-path leakage;
- transition glitches;
- blank or corrupted frames.

Correct blocking defects and re-encode. Do not silently accept a broken or privacy-unsafe result.

## 14. Repository boundary

The video-production branch may contain only this task file. Do not commit:

- video files;
- narration audio;
- subtitles;
- thumbnails;
- production scripts;
- virtual environments;
- package lock files;
- TTS output;
- logs or command output;
- media manifests;
- private paths.

Do not push media to GitHub. Do not merge this branch to `main`.

## 15. Verdicts

Success:

`OPENAI_BUILD_WEEK_2026_FINAL_VIDEO_PRODUCTION_COMPLETE`

Success with Windows SAPI narration fallback rather than neural TTS:

`OPENAI_BUILD_WEEK_2026_FINAL_VIDEO_PRODUCTION_COMPLETE_WITH_SAPI_VOICE_FALLBACK`

Blocking verdicts:

- `VIDEO_PRODUCTION_BLOCKED_BY_TTS_OR_ENCODER_UNAVAILABLE`
- `VIDEO_PRODUCTION_BLOCKED_BY_PRIVACY_OR_COPYRIGHT_QC`
- `VIDEO_PRODUCTION_BLOCKED_BY_DURATION_OR_TECHNICAL_QC`
- `VIDEO_PRODUCTION_BLOCKED_BY_REPOSITORY_STATE`

## 16. Final response requirements

Report:

- exact verdict;
- repository, accepted main commit, tags, and task-bearing branch commit;
- external output directory;
- production tools, versions, and narration voice;
- final video path, size, SHA256, duration, codecs, resolution, frame rate, and audio properties;
- subtitle and thumbnail paths and hashes;
- narration word count and duration;
- scene count and timing range;
- all freshly generated command evidence used;
- privacy, copyright, factual, and technical QC results;
- confirmation that no media or private data was committed;
- confirmation that YouTube and Devpost were not accessed;
- exact remaining manual steps: upload as Public to YouTube, verify processing, run `/feedback`, and submit Devpost before the deadline.

Do not claim the video is uploaded or the project is submitted.