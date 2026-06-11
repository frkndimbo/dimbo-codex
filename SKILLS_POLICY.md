# Skill And Documentation Policy

## Core Rule
- For non-trivial work, inspect available saved skills and use the minimal relevant set.
- Non-trivial means touching >=2 files, using an external library/API, or producing output that will be committed or deployed. Single-file edits, config lookups, and inline Q&A are trivial.
- If the user explicitly names a skill, load and follow it for that turn.
- Announce selected skill names in the first working update.
- If no exact skill match exists, proceed with the closest relevant skill or no skill; do not invent unavailable skills.
- Do not bulk-load skill references; read only the entrypoint and directly needed files.

## Domain Routing
- AGENTS/agent docs: use `agents-md`.
- Git/PR/commit: use relevant commit or git workflow skills when available.
- React/Next/frontend/UI: use relevant React/frontend/UI/design skills.
- API design/build: use `api-design-principles`, `api-endpoint-builder`, or local equivalent.
- Testing/TDD/debugging: use testing, TDD, or phase-gated debugging skills when relevant.
- Deployment/DevOps: use deployment, Cloudflare, Docker, or infra skills matching the repo.
- Performance: use performance optimization/profiling skills.
- Research/paper writing: use scientific writing or plan-writing skills when relevant.
- Academic routing is scoped to IT/CS, ML/data, research methodology, citation, academic reasoning, and writing unless the user explicitly asks for another scientific domain.
- Marketing/SEO routing is active for positioning, content strategy, growth, analytics, funnels, conversion, technical SEO, schema, keyword research, indexing, internal linking, and AEO/GEO search visibility.
- When a task spans domains, load the skill for the domain that owns the primary risk; use a secondary skill only if it adds rules the primary does not cover.

## Cybersecurity
- For API security, auth weakness testing, OWASP checks, vulnerability validation, pentest, cloud/container/Kubernetes security, malware/forensics, or detection-rule testing, load the most specific active skill sourced from `Anthropic-Cybersecurity-Skills` first.
- Use cybersecurity skills only for authorized defensive work, approved testing, incident response, or controlled education.
- Offensive, exploit, pentest, and red-team skills are gated outside `$HOME/.codex/skills`; use them only after explicit authorization and scope confirmation.
- If no active Anthropic cybersecurity skill matches, use the most relevant other saved skill.

## Academic Search
- For paper, jurnal, artikel ilmiah, sitasi, citation, daftar pustaka, DOI, arXiv, PubMed, Semantic Scholar, literature review, publisher template, TIN/JATI, or academic submission, use `paper-search-mcp` before generic web search.
- If Zotero is mentioned, also cover Zotero import, metadata, BibTeX, and citation-library workflow.
- Do not use Context7 as the primary academic paper discovery source.

## Framework And Current Docs
- For libraries, frameworks, SDKs, APIs, CLIs, or cloud services, fetch current official docs before answering when behavior may be version-sensitive.
- Prefer local repo docs, official docs, Context7, MCP tools, and CLIs before generic web.
- Use generic web only when explicitly requested or current external verification is required.

## Skill Hygiene
- Keep `AGENTS.md` concise; do not list installed skill directories there.
- Canonical global active skill root is `$HOME/.codex/skills`.
- `$HOME/.agents/skills` is a legacy/non-active source only; do not create active `SKILL.md` files there, point symlinks there, or run installers that hardcode it.
- If a repo/tool hardcodes `$HOME/.agents/skills`, keep its checkout local/vendor-only, inspect the skill payload, and copy/adapt only compatible skills into `$HOME/.codex/skills`.
- Check `skills-integration-report.json` only when diagnosing active/skipped/duplicate/quarantined skills.
- Preserve local skills when upstream duplicates exist unless the user asks for a migration.
- Do not bulk reinstall or symlink new payloads into active roots. Permanent skill deletion is allowed only when the user explicitly requests hard-delete pruning, after a manifest with counts and hashes exists, and after explicit destructive confirmation.
- After skill changes, run `rtk proxy python scripts/check_skill_hygiene.py` from this repo when available.
- `graphify` remains the active code graph tool unless a new review clearly favors migration with rollback.
