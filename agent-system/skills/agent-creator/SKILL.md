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
- versioned system identity and harness boundary for session, harness, sandbox, artifact store and credential broker;
- default-deny permission policy with approval binding, provenance-aware data flow and runtime enforcement;
- append-only run-event contract for effects, permissions, transfers, state revisions and budgets;
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
- eval-validity report with task inventory, feasibility witnesses, grader mapping, contamination checks and frozen holdout;
- Output Eval Lab with outcome, trajectory, boundary and stability graders, repeated trials and infrastructure calibration;
- Harness Assumption Registry and matched-budget Ablation Lab;
- workflow/negative fixtures;
- skill training lab and skill-candidate lifecycle;
- target conformance matrix;
- final evidence contract;
- release review;
- machine-readable release decision that reconciles required gates and derives allowed claims;
- evidence ledger and claim guard;
- package verification;
- install simulation from final zip;
- post-birth cleanup;
- runtime/devkit boundary.

Если какой-то слой отсутствует, запишите причину как limitation или blocker.

## Creation cycle

1. Intake and grill-me preflight.
2. Workflow discovery: world notes, candidate loops, selected workflow spec, blocking questions.
3. Repo/tool library check: catalog useful external links as candidates, not dependencies; before architecture, record a deliberate `obra-superpowers` decision for the meta-agent and ask the user only if its use is material.
4. Qualification and maturity mode.
5. Architecture before files.
6. Agent/Skill IR before adapters.
7. Freeze system identity and define session/harness/sandbox/artifact/credential boundaries.
8. Production foundation slice.
9. Tool contract plus default-deny permission policy, approval binding and provenance-aware data flow.
10. Append-only run-event and durable state contract.
11. Hook design pass: separate instructions from deterministic gates, fill registry, fail modes, native mappings and validation cases.
12. Subagent design pass through `../subagent-orchestrator/SKILL.md`: single-agent baseline first, then topology, roles, task graph, context, isolation, lifecycle, result schema and eval.
13. Loop contract, if the agent performs a repeatable process.
14. Trigger Lab.
15. Eval-validity pass: full task inventory, feasibility witness, grader mapping, leakage/contamination checks and frozen holdout.
16. Output Eval Lab: matched budgets/infrastructure, repeated trials, outcome/trajectory/boundary/stability graders and all-attempt reporting.
17. Harness Assumption Registry and Ablation Lab.
18. Stage quality gates and loop state.
19. Context provenance and subagent budgets; sufficiency gate only for evidence-heavy retrieval workflows after local eval.
20. Skill Training Lab: workflow ledger, subagent records, skill candidates, promotion gate.
21. Birth contract, first-run sequence, environment readiness, project context and post-birth cleanup.
22. Target conformance and adapter parity.
23. Draft final-evidence contract and claim boundary.
24. Trust, permissions, runtime probes, containment and recovery drills.
25. Memory disclosure, freshness and poisoning policy.
26. Human draft release review.
27. Package, install, birth gate and export validation on fresh extraction.
28. Independent validation of the final package.
29. Repair, regress, rerun benchmark-validity checks, rebuild and reinstall.
30. Hash the final evidence bundle and validate the machine-readable release decision.
31. Governed operations and proposal-only living adaptation with hidden holdout, canary and rollback.
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
