# Judge Testing Guide

## Supported Environment

- Windows-oriented release tested with CPython 3.11.
- Git is useful for cloning but not required when using a downloaded archive.
- No Zotero database, Obsidian vault, OpenAI API key, or external service is required for offline verification.
- Other platforms may require path or Zotero-profile adjustments for an optional full local trial.

## Get The Release

```bash
git clone https://github.com/zcx369658780/Zotero-Analytical-Workflow-Skills-Public.git
cd Zotero-Analytical-Workflow-Skills-Public
git checkout openai-build-week-2026-submission-rc1
```

Alternatively, download the public source archive for the same tag and open a terminal in its root directory.

## Offline Verification

Run the complete accepted unit-test suite:

```bash
python -m unittest discover -s tests -v
```

Expected minimum: `24/24` tests pass and the command exits 0. Tests use synthetic publication records and mocked metadata responses; they do not open Zotero or Obsidian data.

Parse every product Python file:

```bash
python -c "import ast,pathlib; p=list(pathlib.Path('skills').glob('*/scripts/*.py')); assert len(p)==12; [ast.parse(x.read_text(encoding='utf-8')) for x in p]; print('AST 12/12 PASS')"
```

Run safe help checks for the nine script paths that are not helper modules:

```bash
python -c "import os,pathlib,subprocess,sys; h={'classification.py','template_renderer.py','metadata_client.py'}; p=[x for x in pathlib.Path('skills').glob('*/scripts/*.py') if x.name not in h]; assert len(p)==9; r=[(x,subprocess.run([sys.executable,str(x),'--help'],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}).returncode) for x in p]; assert all(c==0 for _,c in r),r; print('CLI help 9/9 PASS')"
```

These commands only parse source and request command help. They do not write notes or contact scholarly metadata services.

## Inspect The Installable Skills

Review:

- `skills/zotero-collection-manager/SKILL.md`
- `skills/zotero-data-fetcher/SKILL.md`
- `skills/zotero-analytical-writer/SKILL.md`
- each Skill's `agents/openai.yaml`
- `templates/论文精读模板.md`

The Skill files describe the orchestration and evidence rules. Agent metadata makes the installed Skills discoverable. The template is separately licensed runtime data and is not duplicated into the rewritten Python renderers.

## Expected Behavior

- Queue and import commands are read-only unless `--write` is supplied.
- Existing Markdown is not replaced unless `--overwrite` is also supplied.
- Missing or malformed runtime templates fail closed.
- Low-evidence records remain labeled for triage or human review rather than being promoted to verified citations.
- Test output contains only synthetic identifiers and reserved `example.invalid` addresses.

## Optional Personal Local Trial

Only use data and directories you own or are authorized to process. Install the three Skill directories under `<codex_home>/skills/` and the template under `<codex_home>/templates/`. Replace placeholders with your own paths and begin with `--help` and dry-run commands. Do not point a judge test at an existing vault until the plan has been reviewed. Keep `--write` and `--overwrite` absent for the first run.

The optional workflow may read the judge's own Zotero Local API or SQLite database and write to the judge's own Obsidian directory only after explicit authorization. Public scholarly metadata lookup is optional and is not part of the offline judge test.

## Licensing

Review [Upstream Permission](../UPSTREAM_PERMISSION_FINAL.md), [Third-Party Notices](../THIRD_PARTY_NOTICES.md), [License Scope](../LICENSE_SCOPE.md), and the [Final Provenance Report](../build_week_2026/FINAL_PROVENANCE_AND_RIGHTS_ACCEPTANCE_REPORT.md). Five fixed upstream-derived counterparts are separately licensed; eligible independently authored downstream files may use the root MIT License.
