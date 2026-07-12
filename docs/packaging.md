---
---

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

## Как собрать runtime source tree

До запуска builder материализуйте `runtime/` как отдельное исходное дерево:

| Источник | Назначение в runtime |
| --- | --- |
| адаптированный router | `runtime/AGENTS.md` |
| заполненный Agent/Skill IR | `runtime/agent-ir.json` |
| заполненный `runtime-manifest.template.json` | `runtime/MANIFEST.json` |
| адаптированный `install-birth.template.md` | `runtime/INSTALL.md` |
| только реально используемые skills | `runtime/skills/` |
| только runtime-needed references/templates | `runtime/references/`, `runtime/templates/` |
| пустые локальные state/memory templates | `runtime/state/`, `runtime/memory/` |

`runtime/MANIFEST.json`, harness evidence и export manifest используют одну `system_release_id`. Не копируйте весь `agent-system/` в runtime автоматически: это development library, а не установленный агент.

Материализуйте `devkit/` отдельно: скопируйте туда project-specific tests, fixtures, audit/eval scripts, source materials и packaging evidence, которые нужны для разработки, но не читаются установленным агентом. Root `scripts/` этого repository являются инструментами-шаблонами; они не попадут в devkit zip, пока вы явно не добавите нужные scripts в свой `devkit/`.
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

Скопируйте `agent-system/templates/export-manifest.template.json` в корень development repo как `export-manifest.json` и используйте `scripts/build_agent_export.py`. Все пути manifest считаются от каталога manifest; placeholder `{repo_root}` указывает на этот же каталог. Builder запрещает совпадение или вложение source/staging, symlink/junction escape, secret-bearing files, devkit paths в runtime, unsafe/duplicate zip entries и расхождение staging с архивом. `FILES.sha256` является точным inventory, а не выборочным списком.

Запускайте из development repo:

```bash
python -B scripts/build_agent_export.py export-manifest.json --run-install-simulation
```

Команда install simulation задается массивом аргументов и должна вызывать `validate_runtime_install.py` с configured report placeholders, а не произвольную no-op команду. Builder передает только ограниченный набор process environment variables и timeout; временная extraction сама по себе не является security sandbox, поэтому запускайте builder только в одобренном isolated development project. Builder распаковывает финальный runtime zip во временную папку; `validate_runtime_install.py` отклоняет unlisted/stale files, `.git`, `scripts/`, devkit/test material, архивы, symlinks и checksum mismatch. Package/install reports содержат hash конкретного runtime zip, hash точного inventory, entry count и hash builder/validator; они относятся именно к этому `system_release_id` и только после этого могут входить в release evidence bundle.

## Evidence Boundary

Пакет может быть locally ready, но external proof требует `final-evidence-contract.template.json`. Planned work, fixture, self-review, copied template и descope не повышают claim до external pass.
