# Birth Protocol

Birth is a one-time import/install process. It must not become the installed agent's ongoing mission.

## Phase 1. Environment Adaptation

Run this before inspecting the user's project.

1. Detect active runtime: Codex, Claude Code, Cursor, OpenCode, local CLI, or another target.
2. Identify active native instruction files and skill mechanisms.
3. Ask before merging the common router into a native instruction file.
4. Ask before adapting skills, commands, or checkers into native runtime mechanisms.
5. Keep behavior equivalent to the Agent/Skill IR.
6. Remove or mark inactive adapters only after the active runtime is known and cleanup is approved or specified by the package.

Do not ask whether preserving adapters, connectors, or multi-platform export state is the installed agent's goal. Portability is an import concern.

## Phase 2. Project Adaptation

Start only after environment adaptation is complete, declined, or explicitly deferred.

1. Ask only for missing project blockers.
2. Inspect approved project sources.
3. Create project context and workspace folders.
4. Save local technical facts to memory, not package docs.
5. Stop after birth. Do not start the first domain task in the same turn unless the user explicitly starts it after setup.

## Post-Birth Cleanup

Depending on target package policy:

- delete pre-install `FILES.sha256` after successful verification;
- delete one-time birth file when no longer needed;
- remove inactive adapters or keep them only with a retained-adapter reason;
- do not silently merge native instruction files;
- do not delete canonical runtime skills, tools, commands, checkers, project context, workspace, or memory unless native embedding succeeded and the user approved the narrower layout.

Templates are not evidence. Preparation files copied during setup become evidence only after an approved run fills them with real observations.
