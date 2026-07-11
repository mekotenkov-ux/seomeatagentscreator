# Subagent Orchestration

## Главный принцип

Subagent - это изолированный исполнитель ограниченной задачи, а не автоматический усилитель качества. По умолчанию используйте одного агента. Делегируйте только когда разделение дает измеримую пользу: независимую параллельность, чистый контекст, отдельные permissions/tools, специализацию или независимую проверку.

Google Research в исследовании 180 конфигураций показал, что multi-agent системы улучшают хорошо распараллеливаемые задачи, но заметно ухудшают последовательные. Решение о делегировании должно зависеть от свойств задачи, а не от желания запустить больше агентов.

## Режимы оркестрации

| Режим | Когда применять | Кто владеет финальным результатом |
| --- | --- | --- |
| single_agent | задача последовательная, небольшая или требует общего плотного контекста | основной агент |
| agent_as_tool | узкая подзадача, результат нужен координатору | координатор |
| handoff | специалист должен стать активным владельцем следующей стадии или ответа | целевой специалист |
| sequential_chain | стадии зависят друг от друга и имеют разные роли | координатор, передающий проверенный артефакт |
| parallel_fanout | независимые read-heavy задачи или непересекающиеся write scopes | координатор/синтезатор |
| critic_loop | генератор и независимый evaluator работают по внешним критериям | внешний gate, не генератор |
| agent_team | участникам нужны shared task list и межагентные сообщения | team lead и внешний acceptance gate |
| batch_map | много однотипных строк/файлов с общей output schema | batch coordinator |

Agent team - самый дорогой и сложный режим. В Claude Code он экспериментальный. Не используйте team/mesh там, где достаточно hub-and-spoke или независимого fan-out.

## Решение о делегировании

Перед spawn оцените:

1. Decomposability: можно ли сформулировать независимые задачи с отдельным done condition?
2. Dependency density: сколько результатов одного worker нужны другому во время работы?
3. Tool density: сколько инструментов и side effects должен координировать каждый worker?
4. Context value: изоляция удалит шум или лишит worker критического контекста?
5. Write overlap: пересекаются ли файлы, записи, таблицы или внешние объекты?
6. Verification: есть ли способ проверить каждый результат и итоговый synthesis?
7. Economics: ожидаемый quality/latency gain выше coordination, token и review cost?

Не делегируйте, если следующая стадия немедленно зависит от результата, задача правит один и тот же участок, критерий нельзя проверить, subtask невозможно ограничить или single-agent baseline уже достаточен.

## Канонические артефакты

Каждая серьезная subagent-система должна иметь:

- subagent-role-registry.json: роли, tool/skill/model policy, permissions и runtime mappings;
- subagent-delegation-plan.json: топология, task graph, зависимости, ownership и бюджеты;
- один subagent-task-contract.json на worker или общую batch schema;
- один subagent-result.json на terminal run;
- append-only subagent-run-ledger.jsonl с parent/child correlation;
- subagent-eval-lab.yaml, сравнивающий single-agent и multi-agent варианты.

## Role registry

Роль должна быть узкой и отличимой от соседних ролей. Запишите should-use и should-not-use cases, capability class, model/reasoning policy, tool allowlist, skill preload, sandbox, network, secrets, approval inheritance, read/write scopes, allowed child roles, max depth, output schema и acceptance gate.

Наследование различается между runtimes. Adapter обязан явно записать, что наследуется от parent: instructions, model, tools, permissions, sandbox, memory, skills и conversation context.

## Delegation task contract

Task contract содержит task id, parent run id, role, rationale, один objective, measurable done condition, scope in/out, dependency ids, artifact refs, exact context pack, allowed/forbidden actions, permissions, write ownership, output schema, evidence, validation commands, budgets, timeout, cancellation, retry и cleanup semantics.

Не передавайте hidden desired verdict независимому reviewer. Не передавайте весь workspace, если compact projection отвечает на вопрос. Большие результаты сохраняйте как артефакты; parent получает ссылки и bounded summary.

## Lifecycle

Используйте состояния:

planned -> authorized -> queued -> running -> input_required | auth_required -> completed | partial | failed | rejected | timed_out | budget_exhausted | cancelled | unknown_outcome -> validated

Terminal task не переписывается задним числом. Повтор или refinement создает новый run/task attempt с ссылкой на исходный.

Parent обязан уметь ждать зависимости без простоя, направить follow-up или interrupt без выдачи permission, отменить worker и потомков, закрыть завершенные threads, сохранить partial result, повторить только transient/idempotent failure и заранее выбрать fail-fast, best-effort или quorum policy.

Background worker, который не может показать approval prompt, не получает молчаливое разрешение. Он возвращает auth_required или input_required, после чего parent выбирает foreground retry или запрашивает approval.

## Parallel write safety

Для write work:

- назначьте disjoint file/resource ownership;
- используйте отдельные git worktrees, clones, containers или sandboxes;
- не разрешайте нескольким workers менять один mutable checkout;
- назначьте одного merger/integrator;
- проверяйте итог после merge, а не только worker branches;
- используйте atomic claim/lease и expiry для shared task queue;
- внешние side effects оставляйте parent или approval-gated committer;
- worktree не считайте security boundary: process, credentials, temp/cache и permissions тоже изолируются.

## Synthesis и проверка

Parent проверяет result schema и status каждого task id, сверяет planned/completed/failed/cancelled counts, проверяет artifacts/evidence, показывает disagreements и coverage gaps, валидирует final merged artifact и закрывает workers. Worker narrative не является evidence.

Для consensus не считайте количество голосов истиной. Сохраняйте независимость контекста, проверяйте evidence и используйте adjudicator с явными критериями.

## Budgets и anti-fanout

По умолчанию depth = 1. Worker count определяется числом независимых задач. Coordinator не делегирует immediate blocking next step. Checks с одним evidence pack объединяются. Team mode и recursion требуют обоснования. Глобальный budget резервирует ресурсы для synthesis, verification и финального ответа. При достижении thread, token, cost, runtime или retry budget новые workers не создаются.

## Observability

Связывайте parent workflow, delegation plan, task, subagent run, tool calls, handoffs, checkpoints и result через стабильные ids. Измеряйте outcome rate, quality/coverage delta против baseline, total/critical-path latency, tokens, tool calls, cost, duplicate work, conflicts, retries, permission blocks, error amplification и context size.

Raw prompts, transcripts, secrets, private tool inputs/outputs и credentials не записываются по умолчанию.

## Subagent Eval Lab

Release gate проверяет positive parallel gain, sequential no-delegation, overlapping write isolation, malformed/partial result, missing permission, timeout/cancel/retry, unknown side-effect outcome, depth/thread/budget enforcement, batch completeness, reviewer independence, disagreement adjudication, count reconciliation, merge conflict, resume after interruption и single-agent vs multi-agent quality/cost/latency.

Multi-agent вариант не проходит gate только потому, что workers завершились. Он должен дать полезный delta или быть ограничен конкретными task classes.

## Target adaptation

Canonical contracts остаются платформенно-нейтральными. Adapter записывает native mechanisms и degradation:

- Codex: custom agents, built-in roles, thread/depth/runtime limits, sandbox inheritance, steering/cancel/close и batch fan-out;
- Claude Code: .claude/agents, foreground/background permissions, fresh vs fork context, worktree isolation и experimental agent teams;
- VS Code/Copilot: agent/runSubagent, custom agents, allowed-agent restrictions, handoffs, model policy и nesting;
- OpenAI Agents SDK: manager/agents-as-tools, handoffs, code orchestration, typed outputs, resumable state, guardrails и traces;
- runtimes без native subagents: sequential fresh-context runs или explicit unsupported status.

## Источники

- Codex subagents: https://developers.openai.com/codex/subagents/
- OpenAI Agents SDK orchestration: https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI Agents SDK tracing: https://openai.github.io/openai-agents-python/tracing/
- Claude Code subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code agent teams: https://code.claude.com/docs/en/agent-teams
- VS Code subagents: https://code.visualstudio.com/docs/agents/subagents
- Anthropic multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic parallel compiler experiment: https://www.anthropic.com/engineering/building-c-compiler
- Google Research, scaling agent systems: https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
- AutoGen behavior contracts: https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/core-concepts/application-stack.html