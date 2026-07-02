---
name: agent-creator
description: Используйте для создания, аудита, отладки, упаковки и публикации production-grade агентских систем, скиллов и workflows с IR, router, tool registry, permission gates, checkers, evals, release review, runtime/devkit boundary и installable package.
---

# Agent Creator

Создавайте агентские пакеты как переносимые системы, а не как промпты, которые работают только в текущем чате.

## Core rule

Модель предлагает. Runtime, tools, tests, permissions, artifacts и reviewers доказывают.

Не доверяйте safety, tool execution, validation, memory hygiene и final acceptance только инструкции в промпте.

## Перед началом

1. Прочитайте `../grill-me/SKILL.md`.
2. Зафиксируйте objective, target users, maturity, scope, autonomy, risk, allowed/forbidden actions, data sources, target platforms, export shape, validation и done condition.
3. Для production/library/governed пакетов прочитайте `references/production-skill-os.md`.

## Обязательная форма серьезного agent package

- router / instruction entrypoint;
- Agent/Skill IR;
- platform adapters;
- focused skills или workflows;
- typed tool registry;
- permission matrix;
- memory and state model;
- workspace hygiene rules;
- checker/reviewer layer;
- context packaging policy;
- Trigger Lab;
- Output Eval Lab;
- release review;
- evidence ledger and claim guard;
- package verification;
- install simulation;
- runtime/devkit boundary.

Если какой-то слой отсутствует, запишите причину как limitation или blocker.

## Creation cycle

1. Intake and preflight.
2. Qualification and maturity mode.
3. Architecture before files.
4. Agent/Skill IR before adapters.
5. Production foundation slice.
6. Tool contract.
7. Loop contract, если агент выполняет повторяемый процесс.
8. Trigger Lab.
9. Output Eval Lab.
10. Context packaging and subagent budget.
11. Trust, permissions, runtime probes.
12. Memory and workspace policy.
13. Release review.
14. Independent validation.
15. Repair and regress.
16. Package, install, export validation.
17. Operations and living adaptation.

## Runtime package

Runtime включает только файлы, которые агент читает при нормальной работе:

- root router;
- skills;
- commands/workflows;
- checker prompts, если они нужны runtime;
- schemas/templates/references, которые реально используются;
- blank state/memory templates;
- install/birth instructions;
- manifest.

## Devkit

Devkit включает:

- validation tests;
- fixtures;
- source materials;
- legacy drafts;
- audit reports;
- packaging scripts;
- full validation runs.

Devkit не должен попадать в runtime.

## Отладочный паттерн

Для качественной отладки создайте отдельный sandbox-проект. Установите туда runtime, работайте с агентом из отдельного чата и сохраните полный trace. Агент-создатель должен чинить source package по логам, state files, checker reports и generated artifacts из sandbox.

## Done

Пакет готов только когда fresh-agent понимает:

- когда запускаться;
- что читать;
- какие действия разрешены;
- какие действия запрещены;
- какие артефакты создать;
- как валидировать результат;
- какие limitations остались;
- что именно входит в runtime, а что осталось в devkit.
