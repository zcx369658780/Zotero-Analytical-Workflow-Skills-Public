"""Fail-closed renderer for the authorized literature-note template."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Mapping, Sequence


TEMPLATE_NAME = "论文精读模板.md"
SECTION_IDS = (
    "metadata",
    "summary",
    "subject",
    "method",
    "data",
    "findings",
    "assessment",
    "evidence_status",
)
REQUIRED_FRONTMATTER_KEYS = (
    "zotero:",
    "obsidian_workflow_tags:",
    "reading_stage:",
    "evidence_level:",
    "citation_eligible:",
    "citation_status:",
    "usable_for:",
    "evidence_sources:",
    "research_tags:",
    "human_verified:",
)


class TemplateContractError(ValueError):
    """Raised when the runtime template cannot satisfy the note contract."""


def discover_template(script_file: str | Path, explicit_path: str | Path | None = None) -> Path:
    configured = explicit_path or os.environ.get("ZOTERO_NOTE_TEMPLATE")
    if configured:
        path = Path(configured).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Authorized note template not found: {path}")
        return path

    origin = Path(script_file).resolve()
    for parent in origin.parents:
        candidate = parent / "templates" / TEMPLATE_NAME
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Authorized note template not found: {TEMPLATE_NAME}")


def _load_contract(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 4 or lines[0].strip() != "---":
        raise TemplateContractError("Authorized note template has invalid frontmatter")
    try:
        frontmatter_end = lines.index("---", 1)
    except ValueError as exc:
        raise TemplateContractError("Authorized note template frontmatter is not closed") from exc

    frontmatter = "\n".join(lines[1:frontmatter_end])
    missing_keys = [key for key in REQUIRED_FRONTMATTER_KEYS if key not in frontmatter]
    if missing_keys:
        raise TemplateContractError(
            "Authorized note template is missing required frontmatter keys: "
            + ", ".join(missing_keys)
        )

    body = lines[frontmatter_end + 1 :]
    title_positions = [
        index
        for index, line in enumerate(body)
        if re.fullmatch(r"#\s+\{\{title\}\}\s*", line)
    ]
    if len(title_positions) != 1:
        raise TemplateContractError("Authorized note template is missing the title expression")
    heading_entries = [
        (index, match.group(1).strip())
        for index, line in enumerate(body)
        if (match := re.fullmatch(r"##\s+(.+?)\s*", line))
    ]
    if len(heading_entries) != len(SECTION_IDS):
        raise TemplateContractError(
            f"Authorized note template requires exactly {len(SECTION_IDS)} top-level sections"
        )
    if any(index <= title_positions[0] for index, _heading in heading_entries):
        raise TemplateContractError("Authorized note template sections must follow its title")
    headings = [heading for _index, heading in heading_entries]
    if len(set(headings)) != len(headings):
        raise TemplateContractError("Authorized note template section headings must be unique")
    return dict(zip(SECTION_IDS, headings))


def render_note(
    *,
    template_path: str | Path,
    frontmatter: Sequence[str],
    title: str,
    sections: Mapping[str, str],
) -> str:
    heading_by_id = _load_contract(Path(template_path))
    if not frontmatter or frontmatter[0] != "---" or frontmatter[-1] != "---":
        raise ValueError("Rendered frontmatter must be delimited by ---")
    missing = [section_id for section_id in SECTION_IDS if section_id not in sections]
    if missing:
        raise ValueError("Missing rendered sections: " + ", ".join(missing))
    unknown = sorted(set(sections) - set(SECTION_IDS))
    if unknown:
        raise ValueError("Unknown rendered sections: " + ", ".join(unknown))

    output = [*frontmatter, "", f"# {title}", ""]
    for section_id in SECTION_IDS:
        output.extend(
            (
                f"## {heading_by_id[section_id]}",
                "",
                sections[section_id].strip(),
                "",
            )
        )
    return "\n".join(output).rstrip("\n") + "\n"
