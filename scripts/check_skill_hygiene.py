#!/usr/bin/env python3
"""Check Codex skill hygiene and optionally write deletion manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REVIEW = ROOT / "skills.review"
GATED = ROOT / "skills.gated"
FRONTMATTER_NAME = re.compile(r"^name:\s*['\"]?([^'\"\n]+)['\"]?\s*$", re.MULTILINE)
LEGACY_SKILL_ROOT = re.compile(r"(\$HOME|~|/home/[^\s]+)\s*/?\.agents/skills|\.agents/skills", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(item.relative_to(path)).encode())
        digest.update(b"\0")
        digest.update(sha256_file(item).encode())
        digest.update(b"\0")
    return digest.hexdigest()


def skill_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def all_skill_dirs() -> list[Path]:
    dirs = []
    dirs.extend(skill_dirs(SKILLS))
    dirs.extend(skill_dirs(SKILLS / ".system"))
    dirs.extend(skill_dirs(REVIEW))
    dirs.extend(skill_dirs(GATED / "security-offensive"))
    return dirs


def read_name(skill_file: Path) -> str | None:
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_NAME.search(text)
    return match.group(1).strip() if match else None


def build_manifest(paths: list[Path]) -> dict[str, object]:
    entries = []
    for path in sorted(paths):
        if not path.exists():
            continue
        skill_file = path / "SKILL.md"
        entries.append(
            {
                "path": str(path.relative_to(ROOT)),
                "has_skill_md": skill_file.exists(),
                "name": read_name(skill_file) if skill_file.exists() else None,
                "skill_md_sha256": sha256_file(skill_file) if skill_file.exists() else None,
                "tree_sha256": tree_hash(path),
                "reason": "redundant inactive/gated skill or broken active helper; deleted after user-approved hard prune",
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "codex_root": str(ROOT),
        "entries": entries,
        "count": len(entries),
    }


def check() -> int:
    problems: list[str] = []
    names: dict[str, list[str]] = {}

    for path in all_skill_dirs():
        skill_file = path / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8", errors="replace")
        name = read_name(skill_file)
        rel = str(path.relative_to(ROOT))
        if not name:
            problems.append(f"missing-name: {rel}")
        else:
            names.setdefault(name, []).append(rel)
        if LEGACY_SKILL_ROOT.search(text):
            problems.append(f"legacy-agents-root-ref: {rel}")

    for name, locations in sorted(names.items()):
        if len(locations) > 1:
            active_locations = [loc for loc in locations if loc.startswith("skills/")]
            if len(active_locations) > 1:
                problems.append(f"duplicate-active-name: {name}: {', '.join(active_locations)}")

    if SKILLS.exists():
        for path in sorted(p for p in SKILLS.iterdir() if p.is_dir() and not any(p.iterdir())):
            problems.append(f"empty-active-dir: {path.relative_to(ROOT)}")

    if problems:
        print("skill hygiene failed")
        for problem in problems:
            print(problem)
        return 1

    print("skill hygiene ok")
    print(
        "active={active} system={system} review={review} gated={gated}".format(
            active=len(skill_dirs(SKILLS)),
            system=len(skill_dirs(SKILLS / ".system")),
            review=len(skill_dirs(REVIEW)),
            gated=len(skill_dirs(GATED / "security-offensive")),
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete-manifest", type=Path)
    parser.add_argument("--manifest-path", action="append", default=[])
    args = parser.parse_args()

    if args.delete_manifest:
        paths = [(ROOT / item).resolve() for item in args.manifest_path]
        data = build_manifest(paths)
        args.delete_manifest.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {args.delete_manifest}")
        print(f"entries={data['count']}")
        return 0

    return check()


if __name__ == "__main__":
    raise SystemExit(main())
