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
