# Agent Birth

This file is first-run bootstrap only. It must not become the installed agent's ongoing mission.

## Core Rule

Run environment adaptation before project adaptation. Do not inspect project sources, ask domain questions, or start work until runtime, workspace, state paths, permission model, and adapter cleanup policy are resolved or explicitly deferred.

## Phase 0. Import Boundary

1. Detect workspace root and package root.
2. Decide whether this is installed runtime, source devkit, export staging, or uncertain.
3. Refuse destructive cleanup when uncertain or when this appears to be the source package.
4. Write `runtime-profile.json`.

## Phase 1. Runtime Detection

1. Detect active runtime from explicit flag, native entrypoint, runtime folders, environment metadata, or user answer.
2. Check for markers such as `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.github/instructions/`, `.claude/`, `.cursor/`, `GEMINI.md`, `opencode.json`, or CLI config.
3. If signals conflict, ask one clarifying question and skip cleanup.
4. Update `runtime-profile.json`.

## Phase 2. Active Adapter Decision

1. Keep the canonical router and semantic contract.
2. Keep the active native entrypoint.
3. Keep shared skills, tools, references, templates, schemas, state, memory, license, and package code.
4. Decide which inactive adapters are retained, moved, or left untouched.
5. Write `birth-plan.json`.

## Phase 3. Native Layout Adaptation

Allowed only after runtime confidence is high or explicit:

1. Move inactive adapters to a local inactive-adapters folder if package policy allows it.
2. Ask before merging common router content into the active native file.
3. Ask before converting skills, commands, checker prompts, hooks, or MCP definitions into native mechanisms.
4. Keep shared folders when native embedding is unavailable or declined.

## Phase 4. Environment Readiness

1. Verify required runtime commands and local CLI entrypoints.
2. Verify writable state and artifact folders.
3. Check env templates without printing secret values.
4. Record optional connectors and missing permissions.
5. Write `environment-readiness.json` or equivalent setup report.

## Phase 5. Project Context Intake

Ask one material question at a time. Prefer this order:

1. primary project target;
2. owner, brand, product, or team name;
3. goal;
4. target users or audience;
5. region, language, platform, stack, or market;
6. source documents, URLs, repos, datasets, or connectors;
7. constraints, competitors, comparables, or exclusions;
8. allowed and forbidden actions;
9. acquisition approvals;
10. expected output format.

If evidence is missing and acquisition is not approved, continue only with lower-assurance assumptions and missing-evidence list.

Write `project-context.json`.

## Phase 6. First Workflow Selection

Offer one concrete next action that belongs to the installed agent's mission. Do not offer a broad package-maintenance menu unless this agent's mission is agent creation.

## Phase 7. Birth Gate

Birth passes only when:

- runtime profile exists;
- birth plan exists;
- active adapter is known or ambiguity is explicit;
- protected files remain in place;
- environment readiness is pass/warn/block with reasons;
- project context is saved or lower-assurance assumptions are recorded;
- next valid action is mission-specific;
- runtime contains no devkit or validation junk.

Stop after birth. Wait for the user's next explicit task unless the user explicitly starts the first workflow.