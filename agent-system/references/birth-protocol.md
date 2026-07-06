# Birth Protocol

Birth is a one-time import, first-run, and host-adaptation process. It must not become the installed agent's ongoing mission.

The installed agent must first learn where it lives, then learn the user's project. Environment adaptation comes before project adaptation.

## Sources Behind This Protocol

This protocol combines the universal birth-rules reference package with public runtime patterns:

- AGENTS.md is a predictable agent instruction file used across many coding agents: https://agents.md/
- OpenAI Codex documents `AGENTS.md`, permissions, skills, subagents, hooks, and sandbox profiles as separate control surfaces: https://developers.openai.com/codex/guides/agents-md
- Claude Code separates user, project, local, and managed scopes, and uses `CLAUDE.md`, `.claude/`, settings, subagents, hooks, MCP, and permission rules: https://code.claude.com/docs/en/settings
- GitHub Copilot and VS Code use repository instructions, `AGENTS.md`, `CLAUDE.md`, prompt files, skills, custom agents, MCP, hooks, and monorepo discovery rules: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions and https://code.visualstudio.com/docs/agent-customization/overview

Treat external docs as target behavior references, not as permission to copy every platform feature into every adapter.

## Birth Goals

A serious first-run flow produces machine-readable artifacts:

- `runtime-profile.json` - runtime, workspace, entrypoints, confidence, state paths, and cleanup permission;
- `birth-plan.json` - keep, move, ask, skip, blocked, merge, and conversion actions;
- `environment-readiness.json` - required runtimes, commands, write paths, env templates, connectors, and permission blockers;
- `project-context.json` - normalized project facts, sources, assumptions, missing evidence, and next valid actions;
- `target-conformance.json` - adapter parity, degraded behavior, permission mapping, install scope, native support, and cleanup behavior.

## Non-Negotiable Rules

1. The top router starts with the installed agent's real job, not package portability.
2. Parent-folder builder instructions are maintainer context, not the installed agent's mission.
3. Platform adapters are thin layers over one semantic contract or Agent/Skill IR.
4. Do not copy full workflow prose into every adapter.
5. Do not silently merge, rewrite, move, or delete native instruction files.
6. Do not inspect project source, ask domain questions, or start work before runtime, workspace, state paths, permission model, and cleanup policy are resolved or explicitly deferred.
7. If several native markers conflict, ask one clarifying question and skip cleanup until resolved.
8. Protected files stay protected: license, mission contract, router, skills, tools, references, templates, schemas, state, memory, package code, and required notices.
9. Ask one material project-context question at a time.
10. If the user supplied a source and approved acquisition exists, acquire/import it or record a blocked acquisition skip before asking for manual paste.
11. Every setup/tool action writes a bounded structured observation.
12. Every public claim points to an artifact, gate, or limitation.

## Birth Sequence

### Phase 0. Import Boundary

Confirm whether the files are in installed runtime, source devkit, export staging, runtime zip output, or an uncertain location. Detect workspace root, package root, writable state/artifact directories, and whether destructive cleanup is forbidden. Write `runtime-profile.json` with `is_source_runtime`, confidence, blocked reasons, and next valid actions.

### Phase 1. Runtime Detection

Detect the active runtime or IDE from explicit flags, active entrypoints, runtime folders, process metadata, environment metadata, or a user answer.

Useful markers include `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `GEMINI.md`, `opencode.json`, `.claude/`, `.cursor/`, `.github/`, `.gemini/`, and CLI config.

If signals conflict and no explicit runtime was supplied, ask one clarifying question and do not clean up adapters.

### Phase 2. Active Adapter Decision

Keep the canonical router, semantic contract, active native entrypoint, shared skills, tools, references, templates, schemas, state, memory, license, and package code. Mark inactive entrypoints only after runtime confidence is high. Write `birth-plan.json`.

### Phase 3. Native Layout Adaptation

Allowed actions: move inactive adapters to a local inactive-adapters folder, write an active-runtime note, ask before merging common router content into a native file, and ask before converting skills, commands, checker prompts, hooks, or MCP definitions into native mechanisms.

Denied actions: deleting protected files, editing user source code for cleanup, silently rewriting native instruction files, or turning import-time portability into the installed agent's mission.

### Phase 4. Environment Readiness

Verify required language runtimes, CLI entrypoints, writable state/artifact folders, env templates without secrets, optional connectors by presence only, network/paid/private/external/destructive permission gates, and first-run command allowlists. Write `environment-readiness.json` or a setup report.

### Phase 5. Project Context Intake

Start only after environment adaptation is complete, declined, or explicitly deferred. Ask one material question at a time: primary target, owner/brand/project, goal, audience, region/language/platform/stack, source documents or repos, constraints, allowed/forbidden actions, acquisition approvals, and expected output format.

If evidence is missing and acquisition is not approved, continue only with explicit assumptions, lower-assurance label, missing-evidence list, and a next action to improve confidence. Write `project-context.json`.

### Phase 6. First Workflow Selection

Offer one concrete next action that belongs to the installed agent's mission. A bare greeting or `start` leads to mission-specific intake, not package maintenance, unless this agent's product job is agent creation.

### Phase 7. Birth Gate

Birth passes only when runtime profile, birth plan, environment readiness, and project context exist or explicit blockers are recorded; active adapter is known or ambiguity is explicit; protected files remain in place; the next action is mission-specific; and no devkit, validation junk, local path, secret, or inactive-adapter confusion entered runtime.

## Notice And Attribution Rules

If the package has a required notice, define exact timing in the birth contract: first greeting only, completed workflow only, final delivery only, or never for clarification/status messages. Do not let notice policy drift into every message unless that is explicitly intended and tested.

## Post-Birth Cleanup

Depending on package policy: delete or archive pre-install inventories only after verification, move inactive adapters only after active runtime is known, keep protected files, record cleanup in `birth-plan.json`, and never hide cleanup from the user.

Templates are not evidence. Preparation files become evidence only after an approved run fills them with real observations.