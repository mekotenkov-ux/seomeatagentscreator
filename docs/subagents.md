---
---

# Система работы с сабагентами

Сабагент - отдельный исполнитель одной ограниченной задачи. Он полезен, когда работу можно действительно разделить: несколько независимых исследований, разные направления ревью, обработка большого списка или непересекающиеся изменения в изолированных worktrees.

Больше агентов не означает лучший результат. Для последовательных задач координация часто ухудшает качество и увеличивает стоимость. Поэтому система сначала доказывает, что делегирование нужно, и только потом запускает workers.

## Что теперь проектируется

1. Выбор режима: один агент, bounded subagent, handoff, последовательная цепочка, parallel fan-out, generator/checker loop, agent team или batch map.
2. Реестр ролей: назначение, tools, skills, model policy, permissions, sandbox и ограничения.
3. Task graph: зависимости, critical path, ownership и budgets.
4. Task contract: objective, context pack, allowed actions, write scope, output schema и done condition.
5. Result contract: status, artifacts, evidence, tests, blockers, limitations и usage.
6. Lifecycle: input/auth required, retry, timeout, cancel, unknown outcome, partial result и cleanup.
7. Изоляция: read-only для исследований, отдельный worktree/container для параллельных writes.
8. Synthesis: parent сверяет counts и evidence, показывает disagreements и проверяет итоговый artifact.
9. Subagent Eval Lab: сравнение с single-agent baseline по качеству, coverage, времени, цене, конфликтам и дублированию.

Начните с [Subagent Orchestration](../agent-system/references/subagent-orchestration.md) и `agent-system/skills/subagent-orchestrator/SKILL.md`.

`verify_public_package.py` проверяет целостность и безопасные defaults шаблонов. Заполненный запуск проверяется отдельно:

```bash
python scripts/validate_subagent_run.py   --role-registry run/subagent-role-registry.json   --delegation-plan run/subagent-delegation-plan.json   --tasks-dir run/tasks   --results-dir run/results   --ledger run/subagent-run-ledger.jsonl
```
