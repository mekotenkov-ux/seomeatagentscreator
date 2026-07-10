# Архитектура агентской системы

## Слои

1. **Router** - короткий entrypoint: миссия, порядок запуска, границы, маршрутизация к skills/workflows.
2. **Workflow discovery** - карта реальных loops: trigger, inputs, actors, tools, state, artifacts, checkpoints, failure modes и done signal.
3. **Repo/tool library** - каталог внешних репозиториев и инструментов как источников идей, без автоматической интеграции.
4. **Agent/Skill IR** - платформенно-нейтральный смысловой контракт.
5. **Skills** - сфокусированные процедуры с frontmatter-trigger.
6. **Commands/workflows** - явные full-run процессы, если задача многошаговая.
7. **Tools** - детерминированные действия со схемами, permission gates и bounded observations.
8. **Hooks** - автоматические lifecycle gates вокруг session, tool use, compaction, subagents и Stop.
9. **Checkers** - независимые проверки результата и границ.
10. **Evals** - Trigger Lab и Output Eval Lab.
11. **State/memory** - короткие durable файлы вне истории чата.
12. **Release review** - единая поверхность blockers, warnings, actions, evidence и limitations.
13. **Birth protocol** - first-run процесс: runtime detection, active adapter decision, environment readiness, project context и birth gate.
14. **Runtime/devkit packages** - чистая упаковка для установки и разработки.

## Почему workflow discovery до IR

Пользователь часто описывает желаемого агента общими словами. До IR нужно найти реальные повторяемые loops, иначе агент будет спроектирован под фантазию, а не под работу. Workflow spec должен быть настолько ясным, чтобы fresh implementer agent мог построить процесс без уточнений.

## Почему IR до адаптеров

Если сначала писать `AGENTS.md`, `CLAUDE.md`, Cursor rules и другие адаптеры, они быстро начинают расходиться. IR держит один источник правды: job, trigger surface, workflow, risks, tools, evals и target platforms.

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

## Почему нужен claim guard

Agent package не готов, если готовность существует только в финальном тексте агента. Production claim требует внешних доказательств: evals, checker reports, package verification, install simulation, release review.

## Почему нужен birth protocol

Мультиплатформенность нужна до установки. После birth установленный агент должен заниматься своей задачей, а не сохранением adapters, connectors или экспортного состояния. Environment adaptation идет до project adaptation, native consolidation требует approval, а birth считается завершенным только после runtime profile, birth plan, environment readiness, project context и mission-specific next action.

## Почему нужен Skill Training Lab

Скиллы нельзя писать для текущего чата. Их нужно проверять на fresh agents, хранить skill-candidate lifecycle и повышать в runtime только после evidence, trigger/output checks и boundaries.
