#!/usr/bin/env python3
"""Shared write guards for Zotero analytical workflow scripts."""

from __future__ import annotations

import difflib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class WriteResult:
    path: str
    status: str
    action: str
    write: bool
    overwrite: bool
    backup_path: str | None = None
    diff_summary: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def summarize_diff(old_text: str, new_text: str, *, fromfile: str, tofile: str, max_lines: int = 60) -> str:
    if old_text == new_text:
        return "no content changes"
    diff_lines = list(
        difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            fromfile=fromfile,
            tofile=tofile,
            lineterm="",
        )
    )
    added = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))
    preview = "\n".join(diff_lines[:max_lines])
    if len(diff_lines) > max_lines:
        preview += f"\n... truncated {len(diff_lines) - max_lines} diff lines"
    return f"added={added}, removed={removed}\n{preview}"


def backup_path_for(path: Path) -> Path:
    return path.with_name(f"{path.name}.{timestamp()}.bak")


def guarded_write_text(
    path: Path,
    content: str,
    *,
    write: bool,
    overwrite: bool = False,
    backup: bool = True,
    backup_path: Path | None = None,
    diff: bool = True,
    create_parents: bool = True,
) -> WriteResult:
    exists = path.exists()
    old_text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
    diff_summary = ""
    if exists and diff:
        diff_summary = summarize_diff(old_text, content, fromfile=str(path), tofile=f"{path} (new)")
    elif not exists:
        diff_summary = "new file"

    if exists and not overwrite:
        return WriteResult(
            path=str(path),
            status="skipped_existing",
            action="skip",
            write=write,
            overwrite=overwrite,
            diff_summary=diff_summary,
        )

    if not write:
        return WriteResult(
            path=str(path),
            status="planned_update" if exists else "planned_create",
            action="plan",
            write=write,
            overwrite=overwrite,
            diff_summary=diff_summary,
        )

    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)

    resolved_backup_path: Path | None = None
    if exists and backup:
        resolved_backup_path = backup_path or backup_path_for(path)
        if resolved_backup_path.exists():
            raise FileExistsError(f"backup already exists: {resolved_backup_path}")
        resolved_backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, resolved_backup_path)

    path.write_text(content, encoding="utf-8")
    return WriteResult(
        path=str(path),
        status="updated" if exists else "created",
        action="write",
        write=write,
        overwrite=overwrite,
        backup_path=str(resolved_backup_path) if resolved_backup_path else None,
        diff_summary=diff_summary,
    )


def guarded_append_line(path: Path, line: str, *, write: bool, create_parents: bool = True) -> WriteResult:
    if not write:
        return WriteResult(
            path=str(path),
            status="planned_log_append",
            action="plan",
            write=write,
            overwrite=True,
            diff_summary=f"append: {line.rstrip()}",
        )
    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line)
    return WriteResult(
        path=str(path),
        status="log_appended",
        action="write",
        write=write,
        overwrite=True,
        diff_summary=f"append: {line.rstrip()}",
    )


def print_json_summary(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
