#!/usr/bin/env python3
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

CODEX = Path(os.environ.get("CODEX_DIR", str(Path.home() / ".codex"))).expanduser()
SKILLS = CODEX / "skills"
REVIEW = CODEX / "skills.review"
VENDOR = CODEX / "vendor"

SOURCES = [
    {
        "name": "antigravity-awesome-skills",
        "repo": "https://github.com/sickn33/antigravity-awesome-skills.git",
        "root": VENDOR / "antigravity-awesome-skills" / "skills",
    },
    {
        "name": "Anthropic-Cybersecurity-Skills",
        "repo": "https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git",
        "root": VENDOR / "Anthropic-Cybersecurity-Skills" / "skills",
    },
]

SENSITIVE_NAME = re.compile(
    r"(^|[._-])(env|secret|token|credential|credentials|private|id_rsa|key)([._-]|$)|"
    r"\.(pem|p12|pfx|key|crt|cert)$",
    re.I,
)

def slug(path: Path) -> str:
    return path.parent.name

def has_skill(path: Path) -> bool:
    return path.is_file() and path.name == "SKILL.md"

def sha_tree(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_dir() or ".git" in p.parts:
            continue
        rel = p.relative_to(root).as_posix()
        h.update(rel.encode())
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return h.hexdigest()

def unsafe_files(root: Path):
    out = []
    for p in root.rglob("*"):
        if p.is_file() and SENSITIVE_NAME.search(p.name):
            out.append(p.relative_to(root).as_posix())
    return out

def copy_dir(src: Path, dst: Path):
    shutil.copytree(
        src,
        dst,
        symlinks=False,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store", "node_modules"),
    )

def main():
    SKILLS.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": [],
        "installed": [],
        "duplicates_identical": [],
        "conflicts_review": [],
        "skipped_sensitive_names": [],
        "errors": [],
    }

    for source in SOURCES:
        root = source["root"]
        entry = {k: str(v) for k, v in source.items()}
        entry["skill_count"] = 0
        if not root.exists():
            report["errors"].append(f"missing source root: {root}")
            report["sources"].append(entry)
            continue
        for skill_md in sorted(root.rglob("SKILL.md")):
            src_dir = skill_md.parent
            name = slug(skill_md)
            entry["skill_count"] += 1
            unsafe = unsafe_files(src_dir)
            if unsafe:
                report["skipped_sensitive_names"].append(
                    {"source": source["name"], "skill": name, "files": unsafe}
                )
                continue
            dst = SKILLS / name
            src_hash = sha_tree(src_dir)
            if not dst.exists():
                copy_dir(src_dir, dst)
                report["installed"].append(
                    {"source": source["name"], "skill": name, "hash": src_hash}
                )
                continue
            dst_hash = sha_tree(dst)
            if dst_hash == src_hash:
                report["duplicates_identical"].append(
                    {"source": source["name"], "skill": name, "hash": src_hash}
                )
                continue
            review_dst = REVIEW / source["name"] / name
            if review_dst.exists():
                suffix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
                review_dst = REVIEW / source["name"] / f"{name}.{suffix}"
            review_dst.parent.mkdir(parents=True, exist_ok=True)
            copy_dir(src_dir, review_dst)
            report["conflicts_review"].append(
                {
                    "source": source["name"],
                    "skill": name,
                    "existing_hash": dst_hash,
                    "candidate_hash": src_hash,
                    "review_path": str(review_dst),
                }
            )
        report["sources"].append(entry)

    out = CODEX / "skills-integration-report.json"
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "installed": len(report["installed"]),
        "duplicates_identical": len(report["duplicates_identical"]),
        "conflicts_review": len(report["conflicts_review"]),
        "skipped_sensitive_names": len(report["skipped_sensitive_names"]),
        "errors": report["errors"],
        "report": str(out),
    }, indent=2))

if __name__ == "__main__":
    main()
