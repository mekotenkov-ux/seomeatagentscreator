---
name: agent-creator
description: Используйте для создания, аудита, отладки, упаковки и публикации production-grade агентских систем, скиллов и workflows с grill-me, workflow discovery, repo/tool catalog, IR, router, birth contract, IDE/runtime adapters, tool registry, permission gates, checkers, evals, release review, runtime/devkit boundary и installable package.
---

# Agent Creator

Создавайте агентские пакеты как переносимые системы, а не как промпты, которые работают только в текущем чате.

## Core rule

Модель предлагает. Runtime, tools, tests, permissions, artifacts и reviewers доказывают.

Не доверяйте safety, tool execution, validation, memory hygiene и final acceptance только инструкции в промпте.

## Перед началом

1. Прочитайте `../grill-me/SKILL.md`.
2. Зафиксируйте objective, target users, maturity, scope, autonomy, risk, allowed/forbidden actions, data sources, target platforms, export shape, validation и done condition.
3. Прочитайте `../workflow-loop-me/SKILL.md` и соберите workflow notes, candidate loops и выбранный workflow spec.
4. Если пользователь дал ссылки на репозитории или инструменты, прочитайте `../repo-tool-librarian/SKILL.md` и сохраните их как catalog candidates без интеграции.
5. Для production/library/governed пакетов прочитайте `references/production-skill-os.md`.

## Обязательная форма серьезного agent package

- router / instruction entrypoint;
- Agent/Skill IR;
- workflow discovery notes, workflow spec и discovery ledger;
- repo/tool library для идей и reusable building blocks, не для автоматической интеграции;
- platform adapters;
- birth contract, runtime profile, birth plan, environment readiness и project context templates;
- IDE/runtime adaptation policy;
- focused skills или workflows;
- typed tool registry;
- permission matrix;
- hook registry, lifecycle event mappings и hook validation для правил, требующих автоматического enforcement;
- subagent topology decision, role registry, delegation plan, task/result contracts, run ledger, isolation, lifecycle и Subagent Eval Lab;
- memory and state model;
- workspace hygiene rules;
- checker/reviewer layer;
- context packaging policy;
- Trigger Lab;
- Output Eval Lab;
- workflow/negative fixtures;
- skill training lab and skill-candidate lifecycle;
- target conformance matrix;
- final evidence contract;
- release review;
- evidence ledger and claim guard;
- package verification;
- install simulation from final zip;
- post-birth cleanup;
- runtime/devkit boundary.

Если какой-то слой отсутствует, запишите причину как limitation или blocker.

## Creation cycle

1. Intake and grill-me preflight.
2. Workflow discovery: world notes, candidate loops, selected workflow spec, blocking questions.
3. Repo/tool library check: catalog useful external links as candidates, not dependencies.
4. Qualification and maturity mode.
5. Architecture before files.
6. Agent/Skill IR before adapters.
7. Production foundation slice.
8. Tool contract.
9. Hook design pass: отделить instructions от deterministic gates, заполнить registry, fail modes, native mappings и validation cases.
10. Subagent design pass через `../subagent-orchestrator/SKILL.md`: сначала single-agent baseline, затем topology, roles, task graph, context, isolation, lifecycle, result schema и eval.
11. Loop contract, если агент выполняет повторяемый процесс.
12. Trigger Lab.
13. Output Eval Lab.
14. Stage quality gates and loop state.
15. Context packaging and subagent budget.
16. Skill Training Lab: workflow ledger, subagent records, skill candidates, promotion gate.
17. Birth contract, first-run sequence, environment readiness, project context, and post-birth cleanup.
18. Target conformance and adapter parity.
19. Final evidence contract and claim guard.
20. Trust, permissions, runtime probes.
21. Memory and workspace policy.
22. Release review.
23. Independent validation.
24. Repair and regress.
25. Package, install, birth gate, export validation.
26. Operations and living adaptation.

## Runtime package

Runtime включает только файлы, которые агент читает при нормальной работе:

- root router;
- skills;
- workflow-loop-me skill and workflow discovery templates;
- repo-tool-librarian skill and repo/tool catalog templates;
- commands/workflows;
- checker prompts, если они нужны runtime;
- schemas/templates/references, которые реально используются;
- blank state/memory templates;
- install/birth instructions;
- machine-readable first-run templates;
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
