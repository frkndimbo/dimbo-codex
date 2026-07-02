# Tokenomics Policy

One-line summary: maximize reasoning quality by routing expensive context and models only to spec, eval, and review stages.

## Model Routing
- Default: medium profile for search, edits, local tests, doc cleanup, and bounded refactors.
- Deep: `cx/gpt-5.5-xhigh` for Spec Design, Eval Design, security review, architecture review, MCP/config changes, and final Diff Review.
- Research: deep model only for synthesis; use tools/subagents for collection and filtering.
- Subagents: use for inventory, grep summaries, test-output reduction, and paper/source extraction; avoid open-ended delegation.

## Skill Profiles
- Use generated profile files: `minimal`, `build`, `research`, `linux`, `security`, `agent-dev`, `frontend`, `deep`.
- Launch example: `codex --profile research`.
- Regenerate local profile files with `rtk run "sh scripts/generate_skill_profiles.sh"`.
- Do not keep all 288 saved skills visible for routine work.

## Context Compression
- Every instruction doc starts with a one-line summary.
- Keep focused docs below 1,000 words.
- Use linked docs from `AGENTS.md` instead of embedding long procedures.
- Use `inbox/` for active state and bulky notes; load only active notes.

## MCP And Tool Output
- Keep JSON for protocol calls and machine validation.
- Use compact Markdown, TOON, or table summaries only for large homogeneous result sets after tool execution.
- If accuracy matters more than token count, prefer canonical JSON plus short summary.

## Waste Patterns To Cut
- Repeated tree scans after file targets are known.
- Repeated tool descriptions from irrelevant skills.
- Broad subagent chatter without acceptance criteria.
- Verification started only after implementation.
- Full log dumps instead of grouped failures.
