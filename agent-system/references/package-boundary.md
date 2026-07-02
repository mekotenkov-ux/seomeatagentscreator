# Runtime And Devkit Boundary

Agent package состоит из двух разных продуктов.

## Runtime

Runtime - это то, что целевой агент читает и использует при обычной работе после установки.

В runtime могут быть:

- router или native instruction entrypoint;
- Agent/Skill IR;
- skills, commands/workflows и checker prompts, которые реально нужны runtime;
- tool registry и runtime tool docs;
- runtime-needed schemas/templates/references;
- blank state/memory templates;
- install/birth docs;
- manifest и optional file inventory for import verification.

## Devkit

Devkit - это материалы разработки, аудита и проверки.

В devkit должны жить:

- validation scripts;
- test fixtures;
- source materials;
- legacy prompts;
- eval cases;
- full validation runs;
- independent audit reports;
- packaging scripts;
- handoff notes;
- release review evidence.

## Hard Rule

Runtime zip не должен содержать:

- `tests/`, `validation-tests/`, `test-scenarios/`;
- `source-materials/`, raw provider dumps, copied prompts;
- `agent-workspace/`, debug runs, browser profiles, screenshots;
- `handoff/`, final rework reports, `FINAL_REPORT.md`;
- `chat-prompts/`, `ide-versions/`, duplicate adapter copy folders;
- caches, `.pyc`, `__pycache__`, `.env`, credentials;
- local absolute paths;
- hidden dependency on this chat.

## Export Flow

1. Build runtime and full-devkit staging from explicit manifests.
2. Recreate staging from scratch.
3. Copy only allowlisted runtime files.
4. Generate `FILES.sha256` after final runtime cleanup when file inventory is used.
5. Create zip from explicit recursive file list.
6. Normalize zip entry names to `/`.
7. Inspect zip entries directly.
8. Run install simulation from the zip, not from the working tree.

Do not trust a clean-looking staging folder until the zip itself has been inspected.
