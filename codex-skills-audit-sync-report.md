# Codex Skills Audit & Sync Report

## Summary

* Added: 18 active Codex skills: `academic-research-suite`, `webwright`, `agent-sort`, `skillopt-skill-optimizer`, `image-to-code`, and 13 Science Superpowers methodology skills.
* Updated: 7 Taste skills from `Leonxlnx/taste-skill`: `design-taste-frontend`, `gpt-taste`, `redesign-existing-projects`, `full-output-enforcement`, `high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui`.
* Replaced: `deep-research` replaced by `academic-research-suite`; `claude-scientific-skills` replaced by Science Superpowers methodology skills.
* Merged: `full-output-enforcement` kept upstream content but narrowed trigger text to avoid global over-triggering.
* Kept: Existing top-level duplicates kept where nested copies were identical or less discoverable; existing plugin Superpowers cache kept.
* Disabled: 27 active skill folders moved to timestamped quarantine.
* Deleted: 0 permanent deletes.
* Skipped: raw Claude ARS layout, ECC full installer/hooks/config, Taste v1/imagegen/brandkit extras, Science global bootstrap, SkillOpt heavy runtime install, Webwright deps install.
* Manual Review Needed: Webwright runtime dependencies are not installed; ECC installer dry-run needs missing `ajv`; restart Codex to reload skill registry.

## Environment

* OS: Arch Linux `7.0.9-zen1-1-zen` x86_64.
* Shell: `/usr/bin/fish`.
* Codex home: `~/.codex` because `CODEX_HOME` was unset.
* Skill locations scanned: `~/.codex/skills`, `~/.agents/skills`, `~/.codex/plugins`, `~/.codex/.tmp/plugins`, project `AGENTS.md`.
* Python: `3.14.5`.
* Node: `v26.1.0`.
* Package managers: npm/npx `11.14.1`, Bun `1.3.10`; pnpm/yarn not found in path scan.
* Plugin/MCP support: `~/.codex/config.toml` has MCP servers `icm`, `context7`, `paper-search-mcp`; Superpowers plugin enabled; no Webwright plugin installed.

## Source Repositories

| Repo | Commit | Purpose | Install Mode | Notes |
| ---- | ------ | ------- | ------------ | ----- |
| `Imbad0202/academic-research-skills` | `f0bfc594c452` | Upstream ARS Claude package | SKIP | Read only; Codex package preferred |
| `Imbad0202/academic-research-skills-codex` | `900238ce1b04` | Codex-native ARS suite | ADD | Installed as single router skill |
| `Leonxlnx/taste-skill` | `3c7017d636c3` | Frontend/UI taste skills | SELECTIVE UPDATE | Only high-value skills installed |
| `microsoft/Webwright` | `734bc60ea736` | Browser automation skill | ADD MANUAL | No plugin duplicate; deps not installed |
| `affaan-m/ECC` | `64cd1ba248e7` | Engineering skill catalog | ADD NARROW | Only `agent-sort`; full installer skipped |
| `microsoft/SkillOpt` | `4f3a9bc055b2` | Skill optimization framework | WRAPPER ADD | Local Codex wrapper created |
| `K-Dense-AI/science-superpowers` | `b1385d351173` | Computational science methodology | SELECTIVE ADD | Bootstrap skipped; core methodology installed |

## Existing Skill Inventory

Full pre-change inventory is saved at `~/.codex-skill-backups/20260530-191205/inventory/existing-skills.tsv`.

| Skill | Path | Source | Domain | Status | Notes |
| ----- | ---- | ------ | ------ | ------ | ----- |
| `deep-research` | `~/.codex/skills/deep-research` | sanjay3290 AI skills | Research | Disabled | API-dependent overlap with ARS |
| `claude-scientific-skills` | `~/.codex/skills/claude-scientific-skills` | K-Dense Claude scientific skills | Science | Disabled | Broad placeholder; Science Superpowers is better |
| `scientific-writing` | `~/.codex/skills/scientific-writing` | K-Dense | Academic writing | Kept | Domain-specific writing helper, not methodology core |
| `citation-management` | `~/.codex/skills/citation-management` | K-Dense | Citations | Kept | Useful citation utility; ARS handles pipeline routing |
| `design-taste-frontend` | `~/.codex/skills/design-taste-frontend` | Taste Skill | Frontend design | Updated | Replaced with current upstream v2 |
| `full-output-enforcement` | `~/.codex/skills/full-output-enforcement` | Taste Skill | Output completeness | Merged | Trigger narrowed |
| `browser-automation` | `~/.codex/skills/browser-automation` | community | Browser automation | Kept | General patterns; Webwright handles script evidence workflow |
| `playwright-skill` | `~/.codex/skills/playwright-skill` | community | Browser testing | Kept | Existing manual Playwright skill; Webwright distinct |
| `skill-optimizer` | `~/.codex/skills/skill-optimizer` | hqhq1025 | Skill audit | Kept | Read-only diagnostics; SkillOpt wrapper handles optimization workflow |

## Candidate Skill Inventory

| Skill | Repo | Domain | Codex Compatible | Dependencies | Notes |
| ----- | ---- | ------ | ---------------- | ------------ | ----- |
| `academic-research-suite` | ARS Codex | Academic research | Yes | Optional bibliographic APIs | Installed |
| `academic-paper`, `deep-research`, `academic-pipeline` raw | ARS raw | Academic research | No direct | Claude layout | Skipped |
| `design-taste-frontend` | Taste | Frontend design | Yes | None | Updated |
| `gpt-taste` | Taste | Motion-heavy frontend | Yes | GSAP only if project uses it | Updated |
| `image-to-code` | Taste | Visual-to-code | Yes | Image tool optional | Added |
| `imagegen-frontend-web/mobile`, `brandkit` | Taste | Image generation | Partial | Image generation | Skipped to avoid routing noise |
| `webwright` | Webwright | Browser automation | Yes as skill | Python/Playwright not present | Installed, runtime deps not installed |
| `agent-sort` | ECC | ECC selection | Yes | None | Installed |
| ECC full installer | ECC | Global harness ops | Risky | Node deps, hooks, config merge | Skipped |
| `skillopt-skill-optimizer` | SkillOpt | Skill evaluation | Yes wrapper | None for wrapper | Added |
| Science methodology skills | Science Superpowers | Scientific method | Yes | None | 13 installed |
| `using-science-superpowers` | Science Superpowers | Global bootstrap | Too broad | None | Skipped |

## Duplicate & Overlap Audit

| Skill A | Skill B | Overlap Type | Winner | Action | Reason |
| ------- | ------- | ------------ | ------ | ------ | ------ |
| raw ARS skills | `academic-research-suite` | Same suite | `academic-research-suite` | ADD/SKIP raw | Codex-native router prevents multi-skill overtrigger |
| `deep-research` | `academic-research-suite` | Literature/deep research | `academic-research-suite` | DISABLE old | Codex-native ARS covers academic research better |
| `claude-scientific-skills` | Science Superpowers | Scientific method | Science Superpowers | DISABLE old | New skills are concrete and methodology-specific |
| `scientific-writing` | ARS | Manuscript writing overlap | Both | KEEP both | ARS routes pipeline; scientific-writing remains domain utility |
| Taste existing | Taste upstream | Same names | Taste upstream plus local trigger narrowing | UPDATE/MERGE | Current upstream clearer for frontend tasks |
| `browser-automation` | `webwright` | Browser automation | Both | KEEP/ADD | General patterns vs end-to-end script-and-evidence workflow |
| ECC verification/TDD/security | Existing local verification/review skills | Broad workflow overlap | Existing local/specific skills | SKIP | Full ECC would create routing noise |
| `skill-optimizer` | `skillopt-skill-optimizer` | Skill improvement | Both | KEEP/ADD | Existing is read-only diagnostics; wrapper is evidence-based optimization |
| Manual `using-superpowers` | Superpowers plugin cache | Same bootstrap | Plugin cache | DISABLE manual | Avoid duplicate broad conversation-start trigger |

## Keep / Replace / Merge / Delete Decisions

| Candidate | Existing Conflict | Decision | Reason | Backup Path |
| --------- | ----------------- | -------- | ------ | ----------- |
| `academic-research-suite` | none | ADD | Codex-native ARS adapter | `~/.codex-skill-backups/20260530-191205` |
| `design-taste-frontend` | existing same name | REPLACE | Upstream has clearer anti-slop workflow | `.../touched/design-taste-frontend` |
| `full-output-enforcement` | existing same name | MERGE | Upstream content plus narrower trigger | `.../touched/full-output-enforcement` |
| `image-to-code` | none | ADD | High-value Codex visual frontend workflow | `~/.codex-skill-backups/20260530-191205` |
| `webwright` | browser automation skills | ADD | Distinct evidence-script workflow | `~/.codex-skill-backups/20260530-191205` |
| ECC full install | global AGENTS/config/hooks | SKIP | Too broad and installer deps missing | n/a |
| `agent-sort` | none | ADD | Helps trim ECC instead of installing all | `~/.codex-skill-backups/20260530-191205` |
| SkillOpt framework | none | ADD wrapper | Upstream has no SKILL.md | `~/.codex-skill-backups/20260530-191205` |
| `using-science-superpowers` | global bootstrap behavior | SKIP | Trigger too broad | n/a |
| duplicate nested skills | top-level equivalent | DISABLE | Duplicate names break discovery clarity | `.../quarantine/*` |

## Best Skill Set Kept

| Domain | Skill Kept | Why This One |
| ------ | ---------- | ------------ |
| Academic research / literature | `academic-research-suite` | Single Codex router, strong workflow coverage |
| Scientific methodology | Science Superpowers selected skills | Best pre-registration/reproducibility/anomaly discipline |
| Frontend/UI taste | Taste selected set | Clear frontend-only triggers and actionable design guidance |
| Browser automation | `webwright` plus existing `browser-automation` | Webwright for evidence scripts; existing skill for general patterns |
| ECC / engineering discipline | `agent-sort` | Trims ECC safely rather than installing global bundle |
| Skill optimization | `skillopt-skill-optimizer` plus `skill-optimizer` | Optimization wrapper plus read-only diagnostics |

## Removed or Quarantined Skills

| Skill | Old Path | Action | Reason | Backup/Quarantine Path |
| ----- | -------- | ------ | ------ | ---------------------- |
| `deep-research` | `~/.codex/skills/deep-research` | DISABLE | ARS replacement; API dependency | `.../quarantine/deep-research` |
| `claude-scientific-skills` | `~/.codex/skills/claude-scientific-skills` | DISABLE | Broad placeholder | `.../quarantine/claude-scientific-skills` |
| `using-superpowers` | `~/.codex/skills/using-superpowers` | DISABLE | Broad manual duplicate; plugin kept | `.../quarantine/using-superpowers` |
| Nested game skills | `~/.codex/skills/game-development/*` | DISABLE | Duplicate names | `.../quarantine/game-development_*` |
| Nested security AWS skills | `~/.codex/skills/security/aws-*` | DISABLE | Duplicate names | `.../quarantine/security_aws-*` |
| Nested LibreOffice skills | `~/.codex/skills/libreoffice/*` | DISABLE | Duplicate names | `.../quarantine/libreoffice_*` |
| `skill-creator` manual copy | `~/.codex/skills/skill-creator` | DISABLE | Duplicate system skill | `.../quarantine/skill-creator` |
| `skill-installer` manual copy | `~/.codex/skills/skill-installer` | DISABLE | Duplicate system skill | `.../quarantine/skill-installer` |
| Other nested duplicates | `karpathy-guidelines/skills/*`, `app-builder/templates`, `skills/x402-*` | DISABLE | Duplicate names | `.../quarantine/*` |

## Files Changed

| File/Folder | Action | Backup Path |
| ----------- | ------ | ----------- |
| `~/.codex/skills/academic-research-suite` | Added | `~/.codex-skill-backups/20260530-191205` |
| `~/.codex/skills/webwright` | Added | same backup root |
| `~/.codex/skills/agent-sort` | Added | same backup root |
| `~/.codex/skills/skillopt-skill-optimizer` | Added | same backup root |
| `~/.codex/skills/image-to-code` | Added | same backup root |
| `~/.codex/skills/design-taste-frontend` and 6 related Taste skills | Updated | `.../touched/*` |
| `~/.codex/skills/*Science Superpowers selected*` | Added | same backup root |
| `~/.codex/AGENTS.md` | Appended routing block | `.../files/home/d0mb1/.codex/AGENTS.md` |
| `AGENTS.md` | Appended routing block | `.../files/home/d0mb1/dimbo-codex/AGENTS.md` |
| `~/.codex/skills` duplicate folders | Quarantined | `.../quarantine/*` |
| `codex-skills-audit-sync-report.md` | Added report | n/a |

## Compatibility Adjustments

* Codex-specific fixes: ARS installed through Codex adapter; SkillOpt wrapper created; Science bootstrap skipped; Webwright manual skill installed without plugin duplication.
* Claude-only items skipped: ARS raw layout, ARS Claude hooks, ECC full Claude/agent/hook install, Science `using-science-superpowers` bootstrap.
* Plugin/manual install conflicts resolved: manual `using-superpowers` quarantined while Superpowers plugin cache remains enabled.
* Description/routing refinements: `full-output-enforcement` narrowed; `framing-research-questions` narrowed to computational-science/data-analysis contexts.
* Dependencies installed: none.
* Dependencies intentionally not installed: Playwright browsers/runtime, ECC node deps including `ajv`, SkillOpt editable Python package and benchmark extras.

## Verification Results

* Skill discovery: selected skill files exist and Codex prompt debug shows new AGENTS routing. Codex debug prompt-input does not enumerate full skill registry, so static registry validation was used.
* Duplicate name check: PASS. `duplicate_names 0` in `~/.codex/skills`.
* Duplicate function check: PASS for targeted domains; broad duplicates quarantined, partial overlaps kept only where workflows differ.
* Broken reference check: PASS. `selected_broken_refs 0`.
* Smoke tests: PASS for ARS router, Science pre-registration/reproducibility, Taste, image-to-code, Webwright contract, ECC agent-sort, SkillOpt wrapper.
* Issues found: Python Playwright `False`; Node Playwright `False`; ECC installer planner cannot run without `ajv`; Codex restart needed to reload skill registry.

## Final Recommendation

* Production-ready skills: `academic-research-suite`, selected Science Superpowers skills, selected Taste skills, `agent-sort`, `skillopt-skill-optimizer`.
* Disabled but recoverable skills: 27 quarantined folders under `~/.codex-skill-backups/20260530-191205/quarantine/`.
* Skills to avoid: raw Claude ARS, ECC full installer/hooks, global bootstrap skills with conversation-wide triggers, duplicate nested skill copies.
* Optional future installs: Webwright Playwright runtime after explicit approval; SkillOpt Python package only when real eval datasets and API budget exist; extra Taste imagegen/brandkit only when image-generation workflow is requested.
* Manual restart needed: restart Codex to pick up new and quarantined skills cleanly.
