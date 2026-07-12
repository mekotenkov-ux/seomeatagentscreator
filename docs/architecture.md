---
---

# Архитектура агентской системы

## Слои

1. **Router** - короткий entrypoint: миссия, порядок запуска, границы, маршрутизация к skills/workflows.
2. **Workflow discovery** - карта реальных loops: trigger, inputs, actors, tools, state, artifacts, checkpoints, failure modes и done signal.
3. **Repo/tool library** - каталог внешних репозиториев и инструментов как источников идей, без автоматической интеграции.
4. **Agent/Skill IR** - платформенно-нейтральный смысловой контракт.
5. **System identity** - версия model, harness, instructions, tools, permissions, runtime, dependencies и graders.
6. **Harness boundary** - отдельные session, harness, sandbox, artifact store и credential broker.
7. **Skills** - сфокусированные процедуры с frontmatter-trigger.
8. **Commands/workflows** - явные full-run процессы, если задача многошаговая.
9. **Tools and authority** - typed actions, default-deny permission policy, approval binding, provenance-aware data flow и bounded observations.
10. **Hooks** - автоматические lifecycle gates вокруг session, tool use, compaction, subagents и Stop.
11. **Run events/state** - append-only trajectory, revisions, leases, budgets, effects, recovery и reconciliation.
12. **Subagent orchestration** - выбор topology, роли, task graph, context, permissions, isolation, lifecycle, synthesis и eval против single-agent baseline.
13. **Checkers** - независимые проверки результата, trajectory и границ; context sufficiency добавляется только как локально подтвержденный evidence-heavy retrieval gate.
14. **Eval validity** - task inventory, feasibility witnesses, grader mapping, leakage/contamination checks и frozen holdout.
15. **Evals** - Trigger Lab и Output Eval Lab с outcome, trajectory, boundary, stability, repeated trials и infrastructure calibration.
16. **Harness evolution** - Assumption Registry, matched-budget Ablation Lab и governed proposal-only adaptation.
17. **State/memory** - durable state вне истории чата плюс memory provenance, scope, freshness, expiry и disclosure policy.
18. **Release review/decision** - human surface и machine reconciler для blockers, warnings, evidence и allowed claims.
19. **Birth protocol** - first-run процесс: runtime detection, active adapter decision, environment readiness, project context и birth gate.
20. **Runtime/devkit packages** - чистая упаковка для установки и разработки.
## Почему workflow discovery до IR

Пользователь часто описывает желаемого агента общими словами. До IR нужно найти реальные повторяемые loops, иначе агент будет спроектирован под фантазию, а не под работу. Workflow spec должен быть настолько ясным, чтобы fresh implementer agent мог построить процесс без уточнений.

## Почему IR до адаптеров

Если сначала писать `AGENTS.md`, `CLAUDE.md`, Cursor rules и другие адаптеры, они быстро начинают расходиться. IR держит один источник правды: job, trigger surface, workflow, risks, tools, evals и target platforms.

## Почему harness boundary обязательна

Harness - это не prompt. Session history должна переживать crash, harness должен заменяться без потери run, sandbox должен быть disposable, artifacts - независимыми от compute, а credentials - недоступными model-generated code. Authority проверяется runtime; внешний текст и tool output остаются data и не могут расширять permissions.
## Почему tools должны быть typed

Плохой первый инструмент выглядит так:

```text
execute_anything(command)
```

Хороший инструмент ограничен:

```text
read_source_artifact(artifact_id, projection)
propose_target_change(target_id, patch_artifact_id)
request_action_approval(action_id, evidence_refs)
```

Каждый результат инструмента должен быть structured observation:

```json
{
  "status": "success",
  "summary": "Short observation.",
  "items": [],
  "evidence_refs": [],
  "next_valid_actions": []
}
```

## Почему hooks - отдельный слой

Инструкция или skill могут попросить модель проверить риск, но не гарантируют, что проверка сработает. Hook вызывается runtime автоматически. Поэтому security, approvals, protected paths, state handoff перед compaction и hard Stop gate можно вынести из надежды на модель в исполняемый контракт. Hook не заменяет typed tools, sandbox и CI; он соединяет события agent loop с этими механизмами.

## Почему надо валидировать eval и trajectory

Passing result может быть случайным, benchmark - broken, а среда - нестабильной. Поэтому release evidence требует feasibility witness, requirement-to-grader map, hidden holdout, repeated trials, A/A infra calibration и четыре grader families: outcome, trajectory, boundary и stability. Правильный результат после hidden unsafe action остается fail.

## Почему harness надо упрощать

Каждый planner, critic, memory rule или retry loop является предположением о слабости текущей модели. После model/runtime/tool change запускайте ablation по одному компоненту при matched budgets. Не сохраняйте scaffold только потому, что он уже написан.
## Почему нужен claim guard

Agent package не готов, если готовность существует только в финальном тексте агента. Production claim требует внешних доказательств: evals, checker reports, package verification, install simulation, release review.

## Почему нужен birth protocol

Мультиплатформенность нужна до установки. После birth установленный агент должен заниматься своей задачей, а не сохранением adapters, connectors или экспортного состояния. Environment adaptation идет до project adaptation, native consolidation требует approval, а birth считается завершенным только после runtime profile, birth plan, environment readiness, project context и mission-specific next action.

## Почему нужен Skill Training Lab

Скиллы нельзя писать для текущего чата. Их нужно проверять на fresh agents, хранить skill-candidate lifecycle и повышать в runtime только после evidence, trigger/output checks и boundaries.
