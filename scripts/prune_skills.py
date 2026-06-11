#!/usr/bin/env python3
"""Prune Codex skills by the user priority taxonomy.

Default mode is safe: classify + write manifest only. Destructive execution
requires --execute and --i-understand-hard-delete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


CODEX = Path("/home/d0mb1/.codex")
SKILLS = CODEX / "skills"
GATED = CODEX / "skills.gated" / "security-offensive"
REPORT = CODEX / "skill-prune-2026-06-03"

MANDATORY_KEEP = {
    "007",
    "academic-research-suite",
    "acceptance-orchestrator",
    "accessibility-compliance-accessibility-audit",
    "advanced-evaluation",
    "agent-evaluation",
    "agent-framework-azure-ai-py",
    "agent-manager-skill",
    "agent-memory-mcp",
    "agent-memory-systems",
    "agent-orchestration-improve-agent",
    "agent-tool-builder",
    "agentic-actions-auditor",
    "agents-md",
    "agents-v2-py",
    "agenttrace-session-audit",
    "ai-agent-development",
    "ai-agents-architect",
    "ai-engineer",
    "ai-engineering-toolkit",
    "ai-md",
    "ai-ml",
    "ai-native-cli",
    "ai-product",
    "ai-seo",
    "ai-wrapper-product",
    "analyze-project",
    "api-and-interface-design",
    "api-design-principles",
    "api-documentation",
    "api-documenter",
    "api-endpoint-builder",
    "api-patterns",
    "api-security-best-practices",
    "api-security-testing",
    "app-builder",
    "appdeploy",
    "architect-review",
    "architecture",
    "architecture-patterns",
    "astro",
    "audit-context-building",
    "audit-skills",
    "auth-implementation-patterns",
    "autonomous-agent-patterns",
    "autonomous-agents",
    "autoskill",
    "avoid-ai-writing",
    "aws-security-audit",
    "aws-serverless",
    "bash-pro",
    "bun-development",
    "citation-management",
    "cloudflare-workers-expert",
    "code-refactoring-tech-debt",
    "code-simplification",
    "codebase-cleanup-tech-debt",
    "context7-auto-research",
    "context7-mcp",
    "cpp-pro",
    "debugger",
    "debugging-and-error-recovery",
    "deployment-strategy",
    "design-taste-frontend",
    "devcontainer-setup",
    "docker",
    "frontend-design",
    "frontend-dev-guidelines",
    "frontend-ui-engineering",
    "git-pushing",
    "go-concurrency-patterns",
    "golang-pro",
    "google-sheets-automation",
    "grpc-golang",
    "hono",
    "javascript-pro",
    "javascript-testing-patterns",
    "javascript-typescript-typescript-scaffold",
    "linux-shell-scripting",
    "mcp-tool-developer",
    "modern-javascript-patterns",
    "nodejs-backend-patterns",
    "nodejs-best-practices",
    "openai-docs",
    "paper-lookup",
    "project-skill-audit",
    "python-development-python-scaffold",
    "python-pro",
    "react-nextjs-development",
    "rust-pro",
    "scientific-critical-thinking",
    "scientific-writing",
    "senior-frontend",
    "setting-up-reproducible-analysis",
    "skill-creator",
    "skill-installer",
    "skillopt-skill-optimizer",
    "system-design",
    "terraform",
    "testing-patterns",
    "typescript-expert",
    "typescript-pro",
    "web-performance-optimization",
    "webwright",
    "zig-pro",
}

KEEP_PATTERNS = [
    r"\bacademic\b", r"\bresearch\b", r"\bliterature\b", r"\bcitation\b",
    r"\bscientific-(writing|critical|brainstorming)\b", r"\bpeer-review\b",
    r"\bscholar\b", r"\breproducib", r"\bhypothesis\b", r"\bstatistics\b",
    r"\bdata-(science|analysis|engineering)\b", r"\bexploratory-data-analysis\b",
    r"\bpython\b", r"\bmachine-learning\b", r"\bdeep-learning\b", r"\bai-ml\b",
    r"\bpytorch\b", r"\btorch\b", r"\btensorflow\b", r"\bkeras\b",
    r"\bsklearn\b", r"\bscikit\b", r"\bnumpy\b", r"\bpandas\b", r"\bpolars\b",
    r"\bjupyter\b", r"\bnotebook\b", r"\btransformers\b", r"\bhugging-face\b",
    r"\bstable-baselines3\b", r"\breinforcement\b", r"\bcomputer-vision\b",
    r"\bfrontend\b", r"\bbackend\b", r"\bfullstack\b", r"\bfull-stack\b",
    r"\bapi\b", r"\bauth\b", r"\bdatabase\b", r"\bpostgres\b", r"\bsqlite\b",
    r"\bmysql\b", r"\bredis\b", r"\bsupabase\b", r"\bdrizzle\b", r"\bprisma\b",
    r"\breact\b", r"\bnextjs\b", r"\bnext-js\b", r"\bastro\b", r"\bsvelte\b",
    r"\bvue\b", r"\btailwind\b", r"\btypescript\b", r"\bjavascript\b",
    r"\bnodejs\b", r"\bnode-js\b", r"\bbun\b", r"\bdeno\b", r"\bhono\b",
    r"\bnestjs\b", r"\bexpress\b", r"\bcloudflare\b", r"\bworkers\b",
    r"\barchitecture\b", r"\barchitect\b", r"\bsystem-design\b",
    r"\bdevops\b", r"\bdeploy", r"\bproduction\b", r"\bdocker\b",
    r"\bkubernetes\b", r"\bk8s\b", r"\bterraform\b", r"\btesting\b",
    r"\btdd\b", r"\bobservability\b", r"\bmonitoring\b", r"\bperformance\b",
    r"\bscalability\b", r"\breliability\b", r"\bcode-review\b", r"\brefactor",
    r"\bclean-code\b", r"\btech-debt\b",
    r"\bsecurity\b", r"\baudit\b", r"\bhardening\b", r"\bforensics\b",
    r"\bincident-response\b", r"\bthreat\b", r"\bvulnerability\b", r"\bowasp\b",
    r"\bsast\b", r"\bdast\b", r"\bsbom\b", r"\bsupply-chain\b", r"\bsecrets\b",
    r"\biam\b", r"\bzero-trust\b", r"\bsiem\b", r"\bdetection\b", r"\blogs\b",
    r"\brust\b", r"\bzig\b", r"\bc\+\+\b", r"\bcpp\b", r"\bc-pro\b",
    r"\bclang\b", r"\bllvm\b", r"\bjava\b", r"\bspring\b", r"\bgolang\b",
    r"\bgo-", r"\bgrpc\b", r"\btemporal\b",
    r"\bagent\b", r"\bagents-md\b", r"\borchestrat", r"\bskill", r"\bprompt\b",
    r"\bcontext\b", r"\btoken\b", r"\bmemory\b", r"\bmcp\b", r"\bcodex\b",
    r"\bevaluation\b", r"\beval\b", r"\breasoning\b", r"\blogic\b",
    r"\blinux\b", r"\barch\b", r"\bbash\b", r"\bshell\b", r"\bposix\b",
    r"\bsystemd\b", r"\bnetworkmanager\b", r"\bkernel\b", r"\bunix\b",
    r"\bcli\b", r"\bterminal\b",
    r"\bmarketing\b", r"\bseo\b", r"\bcontent-strategy\b", r"\bcopywriting\b",
    r"\bbrand\b", r"\bgrowth\b", r"\bconversion\b", r"\blanding-page\b",
    r"\bfunnel\b", r"\banalytics\b", r"\bkeyword\b", r"\bstructured-data\b",
]

DELETE_PATTERNS = [
    r"\bodoo\b", r"\bshopify\b", r"\bsalesforce\b", r"\bhubspot\b",
    r"\bwordpress\b", r"^expo", r"^hig-", r"^n8n", r"\bdiscord\b",
    r"^azure-", r"^amazon-", r"^activecampaign", r"^amplitude", r"^apify",
    r"^m365-", r"^microsoft-", r"\boffice365\b", r"\bproofpoint\b", r"\bpalo-alto\b",
    r"\bokta\b", r"\bcrowdstrike\b", r"\bsplunk\b", r"\bsentinel\b", r"\belastic\b",
    r"\bdefectdojo\b", r"\bmisp\b", r"\bqualys\b", r"\bnessus\b", r"\brapid7\b",
    r"\bdelinea\b", r"\bcyberark\b", r"\bsailpoint\b", r"\bservicenow\b",
    r"\bairtable\b", r"\basana\b", r"\bslack\b", r"\bnotion\b",
    r"\btelegram\b", r"\bwhatsapp\b", r"\binstagram\b", r"\btiktok\b",
    r"\bx-twitter\b", r"\btwitter\b", r"\balexa\b",
    r"\bios\b", r"\bandroid\b", r"\bswiftui\b", r"\bswift\b", r"\bkotlin\b",
    r"\bunity\b", r"\bunreal\b", r"\bgodot\b", r"\bblender\b", r"\bfigma\b",
    r"\bppt\b", r"\bslides\b", r"\bexcel\b",
    r"\blegal\b", r"\bclinical\b", r"\bmedical\b", r"\bhealth\b", r"\bfitness\b",
    r"\bfinance\b", r"\bstock\b", r"\btrading\b", r"\bcrypto\b", r"\breal-estate\b",
    r"\bleiloeir", r"\bleilao",
    r"\bbioinformatics\b", r"\bgenomic", r"\bgenomics\b", r"\bmolecular\b",
    r"\bchem", r"\bbiology\b", r"\bcell\b", r"\bprotein\b", r"\brna\b", r"\bdna\b",
    r"\blabarchive\b", r"\bbenchling\b", r"\bprotocolsio\b",
    r"\bastronomy\b", r"\bastrophysics\b", r"\bgeospatial\b", r"\bgis\b",
    r"\bquantum\b", r"\bmaterials\b", r"\bmetabolomics\b",
]

GATED_PATTERNS = [
    r"^exploiting-", r"\bexploit", r"\battacks\b", r"\bbypass", r"\bforced-browsing\b",
    r"\bred-team\b", r"\bmetasploit\b",
    r"\bhashcat\b", r"\bprivilege-escalation\b", r"\bpost-exploitation\b",
    r"\bpenetration-testing\b", r"\bpentest\b", r"\bkerberoast", r"\bzerologon\b",
    r"\bbloodhound\b", r"\bsqlmap\b", r"\bphishing-simulation\b",
]

LEGACY_PATTERNS = [r"\.agents/skills", r"\$home/\.agents/skills"]

STRICT_KEEP_NAME_PATTERNS = [
    r"academic", r"citation", r"literature-review", r"paper", r"scientific-(writing|critical|brainstorming)",
    r"peer-review", r"scholar", r"proofreader", r"reproducible", r"hypothesis", r"research-grants",
    r"venue-templates", r"latex-paper", r"thesis", r"statistics", r"exploratory-data-analysis",
    r"python", r"pytorch", r"torch", r"tensorflow", r"keras", r"sklearn", r"scikit", r"numpy", r"pandas",
    r"polars", r"jupyter", r"notebook", r"transformers", r"hugging-face", r"stable-baselines3",
    r"reinforcement", r"computer-vision", r"data-science", r"machine-learning", r"deep-learning",
    r"matplotlib", r"seaborn", r"dask", r"modal", r"networkx", r"ai-ml", r"rag", r"llm",
    r"frontend", r"backend", r"fullstack", r"full-stack", r"api-(and-interface|design|documentation|documenter|endpoint|patterns|security)",
    r"auth", r"database", r"postgres", r"sqlite", r"mysql", r"redis", r"supabase", r"drizzle", r"prisma",
    r"react", r"nextjs", r"next-js", r"astro", r"svelte", r"vue", r"tailwind", r"typescript",
    r"javascript", r"nodejs", r"node-js", r"bun", r"deno", r"hono", r"nestjs", r"express", r"cloudflare",
    r"workers", r"web-performance", r"accessibility",
    r"architecture", r"architect", r"system-design", r"devops", r"deploy", r"production", r"docker",
    r"kubernetes", r"k8s", r"terraform", r"testing-patterns", r"tdd", r"observability", r"monitoring",
    r"performance", r"scalability", r"reliability", r"code-review", r"refactor", r"clean-code",
    r"tech-debt", r"debug", r"acceptance",
    r"security", r"audit", r"hardening", r"forensics", r"incident", r"threat", r"vulnerability",
    r"owasp", r"sast", r"dast", r"sbom", r"supply-chain", r"secrets", r"iam", r"zero-trust",
    r"siem", r"detection", r"logs", r"malware", r"container-security", r"tls", r"xss", r"csrf",
    r"rust", r"zig", r"cpp", r"c\+\+", r"c-pro", r"clang", r"llvm", r"java", r"spring", r"golang",
    r"go-concurrency", r"grpc-golang", r"temporal-golang",
    r"agents-md", r"agent-(evaluation|framework|manager|memory|orchestration|tool)", r"agentic-actions",
    r"agenttrace", r"ai-agent", r"ai-agents",
    r"skill-(audit|check|creator|developer|improver|installer|optimizer|router|scanner|sentinel|writer)",
    r"prompt", r"context7", r"token", r"memory", r"mcp-tool", r"codex", r"evaluation",
    r"reasoning", r"logic", r"orchestrator",
    r"linux", r"arch", r"bash", r"shell", r"posix", r"systemd", r"networkmanager", r"kernel", r"unix",
    r"seo", r"marketing", r"content-strategy", r"copywriting", r"brand", r"growth", r"conversion",
    r"landing-page", r"funnel", r"analytics", r"keyword", r"structured-data", r"ab-test",
]

STRICT_KEEP_DESC_PATTERNS = [
    r"machine learning", r"production-ready", r"full-stack", r"technical seo", r"content strategy",
    r"academic research", r"scientific manuscript", r"citation management", r"agent orchestration",
    r"token efficiency", r"linux system", r"cloudflare workers", r"api design", r"database schema",
]

GRANULAR_PREFIXES = (
    "analyzing-",
    "auditing-",
    "building-",
    "configuring-",
    "conducting-",
    "correlating-",
    "deploying-",
    "detecting-",
    "extracting-",
    "hardening-",
    "hunting-",
    "implementing-",
    "integrating-",
    "investigating-",
    "monitoring-",
    "performing-",
    "processing-",
    "remediating-",
    "securing-",
    "testing-",
)

CORE_GRANULAR_KEEP_PATTERNS = [
    r"api", r"auth", r"oauth", r"jwt", r"xss", r"csrf", r"sql-injection", r"web-application",
    r"docker", r"container", r"kubernetes", r"k8s", r"linux", r"cloudflare", r"tls", r"mtls",
    r"sast", r"dast", r"sbom", r"supply-chain", r"secrets", r"terraform", r"infrastructure-as-code",
    r"devsecops", r"github-advanced-security", r"code-scanning", r"semgrep", r"owasp",
    r"zero-trust", r"iam", r"rbac", r"runtime-security", r"incident-response", r"incident",
    r"network-traffic", r"web-server-logs", r"security-logs", r"prompt-injection", r"llm",
    r"malware", r"forensics", r"memory-dumps", r"vulnerability", r"waf", r"modsecurity",
    r"machine-learning", r"python", r"agent", r"mcp", r"detection-rule",
]


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has(patterns: list[str], text: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text)]


def has_name(patterns: list[str], name: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(r"(^|-)" + pattern + r"(-|$)", name)]


def strict_keep_hits(name: str, compact: str) -> list[str]:
    hits = has_name(STRICT_KEEP_NAME_PATTERNS, name)
    if hits:
        return hits
    return has(STRICT_KEEP_DESC_PATTERNS, compact)


def is_core_granular(name: str, compact: str) -> bool:
    if not name.startswith(GRANULAR_PREFIXES):
        return True
    return bool(has(CORE_GRANULAR_KEEP_PATTERNS, compact))


def classify(folder: Path) -> dict[str, object]:
    skill_md = folder / "SKILL.md"
    text = skill_md.read_text(errors="replace")
    meta = frontmatter(text)
    name = folder.name
    desc = meta.get("description", "")
    compact = " ".join(
        [name, meta.get("name", ""), desc, meta.get("category", ""), meta.get("tags", "")]
    ).lower()
    body_low = text.lower()

    legacy_hits = has(LEGACY_PATTERNS, body_low)
    if legacy_hits:
        return result(name, meta, "DELETE", "legacy .agents/skills reference", legacy_hits, skill_md)

    gated_hits = has(GATED_PATTERNS, compact)
    defensive_prefix = name.startswith(("detecting-", "analyzing-", "auditing-", "hardening-", "remediating-"))
    if gated_hits and not defensive_prefix:
        return result(name, meta, "GATED_SECURITY", "offensive security skill", gated_hits, skill_md)

    if name in MANDATORY_KEEP:
        return result(name, meta, "KEEP_ACTIVE", "mandatory priority skill", [], skill_md)

    delete_hits = has(DELETE_PATTERNS, compact)
    keep_hits = strict_keep_hits(name, compact)

    if keep_hits and not is_core_granular(name, compact):
        return result(name, meta, "DELETE", "granular workflow outside active core", keep_hits, skill_md)

    if delete_hits and not keep_hits:
        return result(name, meta, "DELETE", "outside priority domains", delete_hits, skill_md)

    if delete_hits and keep_hits:
        hard_excluded = re.search(r"\b(legal|medical|clinical|health|finance|stock|trading|crypto|real-estate)\b", compact)
        if not hard_excluded and re.search(r"\b(seo|marketing|content|growth|conversion|brand)\b", name):
            return result(name, meta, "KEEP_ACTIVE", "marketing/SEO priority", keep_hits, skill_md)
        if defensive_prefix and re.search(r"\b(security|forensics|audit|detect|hardening|threat)\b", compact):
            return result(name, meta, "KEEP_ACTIVE", "defensive security priority", keep_hits, skill_md)
        return result(name, meta, "DELETE", "priority match outweighed by excluded niche", delete_hits, skill_md)

    if keep_hits:
        return result(name, meta, "KEEP_ACTIVE", "matches priority taxonomy", keep_hits, skill_md)

    return result(name, meta, "DELETE", "no priority match", [], skill_md)


def result(name: str, meta: dict[str, str], action: str, reason: str, hits: list[str], skill_md: Path) -> dict[str, object]:
    return {
        "skill": name,
        "action": action,
        "reason": reason,
        "hits": hits,
        "path": str(skill_md.parent),
        "skill_md_sha256": sha256(skill_md),
        "description": meta.get("description", ""),
        "category": meta.get("category", ""),
        "risk": meta.get("risk", ""),
        "source": meta.get("source", ""),
    }


def build_manifest() -> dict[str, object]:
    entries = [classify(path) for path in sorted(SKILLS.iterdir()) if (path / "SKILL.md").exists()]
    counts = Counter(entry["action"] for entry in entries)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_root": str(SKILLS),
        "gated_security_root": str(GATED),
        "counts": dict(sorted(counts.items())),
        "entries": entries,
    }


def write_manifest(manifest: dict[str, object]) -> Path:
    REPORT.mkdir(parents=True, exist_ok=True)
    path = REPORT / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return path


def execute(manifest: dict[str, object]) -> None:
    GATED.mkdir(parents=True, exist_ok=True)
    for entry in manifest["entries"]:
        action = entry["action"]
        src = Path(entry["path"])
        if action == "GATED_SECURITY":
            dst = GATED / src.name
            if dst.exists():
                raise RuntimeError(f"gated destination already exists: {dst}")
            shutil.move(str(src), str(dst))
        elif action == "DELETE":
            shutil.rmtree(src)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--i-understand-hard-delete", action="store_true")
    args = parser.parse_args()

    manifest = build_manifest()
    path = write_manifest(manifest)
    print(json.dumps({"manifest": str(path), "counts": manifest["counts"]}, indent=2, sort_keys=True))

    if args.execute:
        if not args.i_understand_hard_delete:
            raise SystemExit("refusing destructive execution without --i-understand-hard-delete")
        execute(manifest)
        print("executed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
