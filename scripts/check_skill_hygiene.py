#!/usr/bin/env python3
"""Read-only checks for active Codex skill hygiene."""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


CODEX_DIR = Path(os.environ.get("CODEX_DIR", Path.home() / ".codex")).expanduser()
ACTIVE_ROOT = Path(os.environ.get("CODEX_SKILLS_DIR", CODEX_DIR / "skills")).expanduser()
REPO_ROOT = Path(__file__).resolve().parents[1]

QUARANTINE_MARKERS = {
    "quarantine",
    "quarantined",
    "review",
    "disabled",
    "deprecated",
    "backup",
    "backups",
    "tmp",
}

SELECTED_REFS = {
    "academic-research-suite",
    "agent-sort",
    "agents-md",
    "api-design-principles",
    "api-endpoint-builder",
    "design-taste-frontend",
    "scientific-writing",
    "skillopt-skill-optimizer",
    "webwright",
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(Path.home())).replace(os.sep, "/")
    except ValueError:
        return str(path)


def iter_skill_files(root: Path):
    if not root.exists():
        return
    for path in sorted(root.rglob("SKILL.md")):
        if any(part in {".git", "node_modules", "__pycache__"} for part in path.parts):
            continue
        yield path


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    opening = re.match(r"^---[ \t]*\r?\n", text)
    if not opening:
        return None, "missing opening frontmatter fence"
    closing = re.search(r"(?m)^---[ \t]*$", text[opening.end() :])
    if not closing:
        return None, "missing closing frontmatter fence"
    frontmatter = text[opening.end() : opening.end() + closing.start()]
    match = re.search(r"(?m)^name:\s*['\"]?([^'\"\n#]+)['\"]?\s*(?:#.*)?$", frontmatter)
    if not match or not match.group(1).strip():
        return None, "missing frontmatter name"
    return match.group(1).strip(), None


def duplicate_values(items):
    groups = defaultdict(list)
    for key, value in items:
        groups[key].append(value)
    return {key: values for key, values in groups.items() if len(values) > 1}


def main() -> int:
    broken_frontmatter = []
    name_items = []
    folder_items = []
    active_quarantine_paths = []
    skill_files = list(iter_skill_files(ACTIVE_ROOT) or [])

    for skill_md in skill_files:
        skill_dir = skill_md.parent
        name, error = parse_frontmatter(skill_md)
        if error:
            broken_frontmatter.append({"path": rel(skill_md), "error": error})
        else:
            name_items.append((name.lower(), {"name": name, "path": rel(skill_md)}))

        folder_key = skill_dir.name.lower()
        folder_items.append((folder_key, {"folder": skill_dir.name, "path": rel(skill_dir)}))
        lowered_parts = {part.lower() for part in skill_dir.parts}
        if lowered_parts & QUARANTINE_MARKERS:
            active_quarantine_paths.append(rel(skill_dir))

    active_folder_names = {path.parent.name for path in skill_files}
    active_frontmatter_names = {item[1]["name"] for item in name_items}
    active_refs = active_folder_names | active_frontmatter_names
    selected_broken_refs = sorted(ref for ref in SELECTED_REFS if ref not in active_refs)

    duplicate_active_names = duplicate_values(name_items)
    duplicate_active_folders = duplicate_values(folder_items)

    result = {
        "active_root": str(ACTIVE_ROOT),
        "checked_skill_files": len(skill_files),
        "broken_frontmatter": broken_frontmatter,
        "duplicate_active_names": duplicate_active_names,
        "duplicate_active_folders": duplicate_active_folders,
        "active_quarantine_paths": sorted(active_quarantine_paths),
        "selected_broken_refs": selected_broken_refs,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    has_findings = any(
        result[key]
        for key in (
            "broken_frontmatter",
            "duplicate_active_names",
            "duplicate_active_folders",
            "active_quarantine_paths",
            "selected_broken_refs",
        )
    )
    return 1 if has_findings else 0


if __name__ == "__main__":
    sys.exit(main())
