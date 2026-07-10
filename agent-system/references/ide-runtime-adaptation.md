# IDE And Runtime Adaptation

Use this reference when a package supports several agent surfaces such as Codex, Claude Code, Cursor, VS Code Copilot, GitHub Copilot, OpenCode, Gemini CLI, or a local CLI.

## Principle

The semantic contract is canonical. IDE files are adapters.

Adapter files should make the target runtime load the right contract, skills, tools, memory, permissions, and birth sequence. They should not become separate agent products.

## Common Runtime Surfaces

| Runtime or IDE | Common instruction surface | Native mechanisms to consider | Birth adaptation rule |
| --- | --- | --- | --- |
| Codex | `AGENTS.md` and nested `AGENTS.md` | skills, subagents, hooks, MCP, permissions, sandbox profiles | Keep `AGENTS.md` concise, route to shared contract/skills, verify active instruction chain when confused. |
| Claude Code | `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/` | settings scopes, permissions, subagents, hooks, MCP, local/user/project/managed config | Respect scope precedence; never treat local/user config as shareable package truth. |
| Cursor | `.cursor/rules/*.mdc`, `AGENTS.md` where supported, project rules | rules, MCP, memories, composer/agent modes | Keep rules thin; do not duplicate full workflows into every `.mdc`. |
| VS Code Copilot | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `AGENTS.md`, `CLAUDE.md`, prompt files, skills, custom agents | agent customizations, hooks, MCP, prompt files, skills, custom agents | Use repo-wide instructions for stable context, path-specific instructions only for scoped rules. |
| GitHub Copilot cloud agent | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `AGENTS.md` | cloud agent instructions, custom agents, skills, hooks, MCP, sandbox settings | Make build/test/validation commands obvious; do not hide permission or CI expectations. |
| OpenCode/Gemini/local CLI | runtime-specific config plus shared router | CLI args, config files, MCP, command allowlists | Keep a shared router and record degraded behavior where native skills/hooks are absent. |

## Adapter Checklist

Every adapter should include:

- installed agent identity and one-sentence mission;
- canonical router path;
- semantic contract or Agent/Skill IR path;
- first-run birth file path;
- active runtime value or how to detect it;
- setup/verification command if the runtime supports one;
- permission boundary and approval policy;
- environment-before-project rule;
- project-context intake rule;
- required notice timing, if any;
- protected-file cleanup refusal boundary;
- pointer to target conformance.

## Adapter Must Not Include

- full copied workflow prose;
- devkit validation instructions as normal user work;
- maintainer build steps unless the installed agent's job is package maintenance;
- package export as the installed agent mission;
- hidden rules;
- stale field names;
- domain rules from another package;
- local absolute paths;
- secrets or credential examples.

## Native Consolidation Questions

Ask before changing native files:

1. Should the common router be merged into the active native instruction file?
2. Should skills, commands, checker prompts, hooks, or MCP definitions be converted into native platform mechanisms?
3. Should inactive adapters be moved to a local inactive-adapters folder, or retained for portability?

If the user declines or the runtime has no native equivalent, keep the shared folder and point the active entrypoint to it.

## Target Conformance Evidence

For every platform, record active entrypoint, adapter file paths, semantic parity, unsupported features, degraded behavior, permission mapping, install scope, first-run setup command, native skill/command/hook/MCP support, cleanup behavior, verification status, and evidence refs.

For hooks, keep canonical event families in the shared hook registry and map them to native events in the adapter. Verify tool names, field casing, matcher behavior, exit/decision semantics, timeout behavior, execution shell, and whether the hook can actually block. Read `hook-system.md` before claiming parity.

Presence of an adapter file is not proof of support.