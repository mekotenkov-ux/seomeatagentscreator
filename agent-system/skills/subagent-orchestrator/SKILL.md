---
name: subagent-orchestrator
description: Используйте для решения, нужно ли делегирование, выбора single-agent/subagent/handoff/chain/fan-out/team/batch topology, создания role registry и task graph, выдачи bounded task contracts, управления context, permissions, budgets, isolation, lifecycle, synthesis и Subagent Eval Lab.
---

# Subagent Orchestrator

Subagents нужны для ограниченной независимой работы. Они не являются автоматическим усилителем качества.

## Перед запуском

1. Прочитайте `../../references/subagent-orchestration.md`.
2. Подтвердите authorization: прямой запрос пользователя, применимый workflow/skill contract или platform policy.
3. Оцените decomposability, dependencies, tool density, context value, write overlap, verification и economics.
4. Если single agent надежнее или дешевле, запишите `single_agent` и не делегируйте.

## Порядок работы

1. Выберите topology: `single_agent|agent_as_tool|handoff|sequential_chain|parallel_fanout|critic_loop|agent_team|batch_map`.
2. Заполните role registry и delegation plan.
3. Создайте один task contract на worker с disjoint ownership и expected result schema.
4. Передайте compact context pack. Fresh context - default; fork разрешен только когда benefit и privacy cost записаны.
5. Запускайте только независимые sidecar tasks параллельно. Immediate blocking work оставляйте parent.
6. Не используйте параллельные writes в одном mutable checkout. Выделите worktree/container или disjoint resource scope.
7. Следите за lifecycle, budgets, approvals, cancellation и completed thread cleanup.
8. Требуйте structured result и artifact/evidence refs. Partial/failed/timed-out task тоже обязан вернуть запись.
9. Parent проверяет counts, artifacts и disagreements, затем синтезирует. Worker narrative не является evidence.
10. Запустите Subagent Eval Lab и сравните с single-agent baseline.

## Ограничения

- Default max depth: 1.
- Не создавайте workers только потому, что доступен concurrency slot.
- Не давайте subagent больше permissions, чем parent и task требуют.
- Не разрешайте background worker обходить approval.
- Не передавайте reviewer intended fix или hidden desired verdict.
- Не логируйте raw transcript, secrets и credentials.
- Agent team/peer messaging требует отдельного обоснования и пометки experimental, если target так его классифицирует.

## Done

Оркестрация завершена, когда все planned task ids имеют terminal status, counts сходятся, accepted results прошли schema/evidence checks, write outputs объединены и проверены, blockers/limits видимы, workers закрыты, ledger обновлен, а multi-agent claim подтвержден eval delta.
