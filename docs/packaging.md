# Упаковка и публикация

## Runtime

Runtime содержит только то, что агент использует после установки:

- router;
- skills;
- commands/workflows;
- checker prompts, если нужны;
- schemas/templates/references;
- blank state/memory templates;
- install/birth instructions;
- manifest.

## Devkit

Devkit содержит:

- validation tests;
- fixtures;
- source materials;
- legacy drafts;
- audit reports;
- packaging scripts;
- validation runs.

## Public repo hygiene

Перед публикацией проверьте:

- нет `.env`;
- нет secrets;
- нет credentials;
- нет private client data;
- нет временных рабочих папок и debug-runs;
- нет browser profiles;
- нет zip-архивов предыдущих сборок;
- нет локальных абсолютных путей;
- нет доменных пакетов внутри универсального ядра.

## GitHub Pages

Этот репозиторий содержит статическую страницу `docs/index.html`. Для публикации в GitHub Pages выберите source `Deploy from a branch`, branch `main`, folder `/docs`.

## Export Builder Pattern

Используйте `agent-system/templates/export-manifest.template.json` и `scripts/build_agent_export.py` как базовый паттерн: explicit allowlist, clean staging, `FILES.sha256`, zip inspection, slash-only entries и install simulation из финального архива.

## Evidence Boundary

Пакет может быть locally ready, но external proof требует `final-evidence-contract.template.json`. Planned work, fixture, self-review, copied template и descope не повышают claim до external pass.
