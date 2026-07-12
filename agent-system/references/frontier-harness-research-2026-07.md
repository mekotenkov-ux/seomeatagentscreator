# Frontier Research: агенты и harnesses, июль 2026

Дата среза: 2026-07-11. Все live vendor/research URLs проверены 2026-07-11; arXiv citations закреплены на `v1`, когда используются для claim-bearing preprint. Для изменяемых web pages дата доступа является частью snapshot policy.

Этот документ фиксирует не список трендов, а доказательную базу для изменений универсальной системы создания агентов. В выборку вошли первичные материалы OpenAI, Anthropic, Google Research/DeepMind, Microsoft Research, Meta FAIR/AI at Meta и ведущих академических лабораторий. Vendor engineering posts считаются производственными кейсами, а не независимой репликацией. Один arXiv preprint не становится production-default без локальной проверки.

## Единица анализа

Нельзя приписывать результат только модели. Проверяется версия всей системы:

`model snapshot + harness + instructions + tools + permissions + budgets + infrastructure + task distribution + graders`.

Если хотя бы один компонент меняется, это новый system-under-test.

## Классы решений

- `policy_default` - консервативный детерминированный control этого проекта без обещания performance gain; требует enforcement test и измерения overhead.
- `adopt` - сравнительный вывод, прошедший evidence rubric и применимый в явно указанном scope.
- `experiment` - перспективный прием с ограниченной переносимостью; нужен matched-budget baseline, hidden holdout, sandbox, лимиты и review date.
- `defer` - доказательств недостаточно или риск выше подтвержденной пользы.

Для сравнительных performance/capability claims используйте локальную evidence rubric. Оцените claim/contrast, task validity, repeated trials, reproducibility, generalization и operational value по шкале 0-4. Такой claim получает `adopt` только при 20-24 баллах, отсутствии hard stops и независимой или prospective проверке. Низкорисковые deterministic controls могут стать `policy_default` без обещания performance gain, но требуют enforcement tests и overhead measurement. Это локальная строгая политика проекта, а не заявленный консенсус отрасли.

Hard stops: final holdout использовался при tuning; попытки или знаменатели скрыты; условия имеют разные бюджеты или инфраструктуру; единственный judge - оптимизируемый агент; generated code может менять grader, permissions, logs, budgets или sandbox; производственный self-modification не имеет rollback и human approval.

### Decision register

| Feature | Decision | Basis | Comparative evidence score |
| --- | --- | --- | --- |
| Full system identity, explicit budgets/resources | `policy_default` | Reproducibility and claim-validity control with cross-lab support | N/A; no performance claim |
| Runtime authority, provenance and containment | `policy_default` | Deterministic risk control; utility cost must be measured | N/A; no performance claim |
| Outcome + trajectory + boundary + stability grading | `policy_default` | Safety/validity control supported by Microsoft, Anthropic and OpenAI | N/A; no performance claim |
| Eval-task validity and frozen holdout | `policy_default` | Measurement control supported by OpenAI and Anthropic | N/A; no performance claim |
| Session/harness/sandbox separation | `policy_default` for long-running or tool-executing systems | First-party production architecture convergence; target conformance required | N/A; no performance claim |
| Single-agent baseline | `policy_default` | Prevents unmeasured multi-agent claims | N/A; no performance claim |
| Each multi-agent topology for a task class | `experiment` until local matched-budget gain | Google shows task-dependent gains and regressions | Not scored; prospective local eval required |
| Assumption registry | `policy_default` | Governance control | N/A |
| Automatic ablation after every model/runtime change | `experiment` | One primary vendor experiment; run when the component is plausibly model-dependent | Not scored |
| Sufficient Context checker | `experiment` and optional | Bundled Google Agentic RAG result; component effect not isolated | Not scored |
| Trace-driven candidate improvements | `policy_default` as a governed process | OpenAI production case; optimizer technique remains experimental | N/A |
| Memory provenance, disclosure, freshness and poisoning checks | `policy_default` when durable memory exists | Privacy/security governance control | N/A; no performance claim |
| Automated harness search, active failure discovery, learned playbooks | `experiment` | Preprints or narrow benchmark evidence | Not scored |
| Unattended production self-modification | `defer` | No adequate safety/generalization evidence | Hard stop |

## Что показали источники

### 1. Harness является частью результата

OpenAI рекомендует раскрывать model, reasoning setting, tool access, harness, safeguards, turns, tokens, retries, wall time и cost и предлагает закрепить это в будущих стандартах. Anthropic показал, что только конфигурация ресурсов меняла Terminal-Bench на 6 процентных пунктов. В ARE/Gaia2 inference-duration ablation (`generation-time` против fixed-one-second `instant`) изменила Gaia2-Time pass@1 GPT-5 high с 0% до 34.4%, поэтому timing policy является частью tested system.

Решение: `policy_default`. Версионировать весь system-under-test, фиксировать CPU/RAM floor и kill ceiling, timeout, network, cache, concurrency, retries и infra failures отдельно от model failures.

Источники:

- [OpenAI: trustworthy third-party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/)
- [Anthropic: infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise)
- [Meta: ARE and Gaia2](https://ai.meta.com/research/publications/are-scaling-up-agent-environments-and-evaluations/)

### 2. Final answer не доказывает правильный процесс

Microsoft AgentLens обнаружил `Lucky Pass` у 10.7% проходящих OpenHands trajectories в своей 1,815-trajectory, 47-task evaluation subset: blind retries, regression cycles и отсутствие нормальной verification могли случайно дать зеленый итог. HarnessAudit показал, что корректный ответ может скрывать unauthorized resource access или inter-agent leakage.

Решение: `policy_default`. Разделить outcome, trajectory/process, boundary/safety и system-stability graders. Любое P0 boundary violation блокирует релиз и не компенсируется высоким средним качеством.

Источники:

- [Microsoft Research: AgentLens](https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/)
- [Microsoft Research: HarnessAudit](https://www.microsoft.com/en-us/research/publication/auditing-agent-harness-safety/)
- [Anthropic: demystifying agent evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### 3. Сначала надо проверить сам экзамен

OpenAI оценил примерно 30% public split SWE-Bench Pro как broken: overly strict tests, underspecified или misleading prompts, low coverage. Anthropic рекомендует reference solution и однозначную связь между заданием и тем, что проверяет grader.

Решение: `policy_default`. До любого release claim нужны task inventory, per-task validity disposition, reference solution или feasibility witness, requirement-to-grader map, contamination/shortcut checks, independent defect review и frozen hidden holdout.

Источники:

- [OpenAI: separating signal from noise](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
- [Anthropic: demystifying agent evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### 4. Session, harness и sandbox должны жить отдельно

Anthropic Managed Agents разделяет append-only session log, заменяемый harness и disposable sandbox. OpenAI Agents SDK внешне хранит state, поддерживает snapshot/rehydration и изолированные sandboxes. Это позволяет пережить падение compute без потери run и не держать credentials рядом с model-generated code.

Решение: `policy_default` для tool-executing и long-running systems. Сделать эти интерфейсы явным contract и проверять crash recovery, checkpoint/rehydration, artifact persistence, revoke и cleanup.

Источники:

- [Anthropic: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)
- [OpenAI: next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- [OpenAI: Codex App Server](https://openai.com/index/unlocking-the-codex-harness/)

### 5. Authority должна исполняться runtime, а не текстом prompt

OpenAI и Anthropic сходятся на bounded execution, scoped network, external durable credential storage и auditable approvals; конкретные low-risk allow rules различаются по продуктам. Этот проект выбирает default deny как консервативную policy, а не приписывает такой универсальный default источникам. Anthropic отдельно показал, что allowlisted domain надо считать capability grant: разрешенный домен все еще может быть каналом exfiltration. Project-local config и hooks нельзя исполнять до trust decision.

Решение: `policy_default`. Durable credentials по умолчанию не входят в untrusted execution sandbox; target-native scoped ephemeral delivery допускается только с отдельным enforcement evidence. Egress описывает не только destinations, но и разрешенные operations/principals; symlink разрешается до path validation; внешние данные не могут повышать authority или становиться trusted control.

Источники:

- [OpenAI: Running Codex safely](https://openai.com/index/running-codex-safely/)
- [Anthropic: How we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude)
- [Google DeepMind: CaMeL](https://arxiv.org/abs/2503.18813v1)
- [Microsoft Research: Fides](https://www.microsoft.com/en-us/research/publication/securing-ai-agents-with-information-flow-control/)

### 6. Каждый scaffold-компонент является временным предположением

В одном Anthropic experiment отдельные scaffolding assumptions перестали быть load-bearing после смены model generation; это не универсальный закон, а причина перепроверять затронутые assumptions. Надежный способ понять, что действительно помогает, - удалять по одному компоненту при matched budgets и сравнивать quality, safety, latency и cost.

Решение: `policy_default` для Assumption Registry; автоматический ablation trigger остается `experiment`. После model/runtime/tool или task-distribution change сначала определить, зависит ли предположение от изменившегося компонента, затем провести matched-budget removal test или записать обоснованный `not_affected`.

Источник: [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).

### 7. Multi-agent topology выбирается по свойствам задачи

Google проверил 180 configurations: centralized topology дала +80.9% на parallelizable Finance-Agent, а все multi-agent варианты потеряли 39-70% на sequential PlanCraft; independent systems усиливали ошибки до 17.2x. Anthropic получил сильный результат на breadth-first research, но с большим token overhead.

Решение: `policy_default` для single-agent baseline и `experiment` для каждой topology в каждом task class. Topology получает право на локальный release claim только при prospective matched-budget gain и non-inferior safety.

Источники:

- [Google Research: scaling agent systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)

### 8. Context должен иметь проверяемую достаточность

Google Agentic RAG добавляет Sufficient Context Agent, который сравнивает запрос, evidence и draft, называет конкретные gaps и продолжает retrieval только по ним. Google сообщил улучшение bundled multi-agent RAG system, но не изолировал причинный вклад этого checker и использовал LLM judge.

Решение: `experiment` как optional phase gate для evidence-heavy retrieval workflows. Checker должен вернуть covered requirements, missing evidence и bounded next query, а не только общий verdict.

Источник: [Google Research: Agentic RAG](https://research.google/blog/unlocking-dependable-responses-with-gemini-enterprise-agent-platforms-agentic-rag/).

### 9. Улучшение по traces допустимо только через governed loop

OpenAI Tax AI превращает expert-reviewed corrections в structured findings, targeted evals и bounded engineering tasks, затем запускает regression suites и human review. Google ReasoningBank и Microsoft RHO показывают потенциал опыта и retrospective optimization, но self-validation не является внешним доказательством.

Решение: `policy_default` для governed trace-to-candidate process; `experiment` для optimizer technique и automated harness search. Production traces используются только из явно разрешенного redacted path. Candidate patch не применяется автоматически и проходит targeted, regression, safety и untouched holdout gates.

Источники:

- [OpenAI: self-improving tax agents](https://openai.com/index/building-self-improving-tax-agents-with-codex/)
- [Google Research: ReasoningBank](https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/)
- [Microsoft Research: Retrospective Harness Optimization](https://www.microsoft.com/en-us/research/publication/retrospective-harness-optimization-improving-llm-agents-via-self-preference-over-trajectory-rollouts/)
- [Stanford IRIS / KRAFTON / MIT: Meta-Harness v1](https://arxiv.org/abs/2603.28052v1)

### 10. Memory требует disclosure, freshness и poisoning evals

Meta CIMemories показывает, что полезная память может нарушать contextual integrity; OpenAI подчеркивает staleness и reviewable memory; Anthropic предупреждает, что persistent state превращается в долговременный prompt-injection surface.

Решение: `policy_default` для systems с durable memory. Каждая durable memory entry получает source, scope, confidence, observed_at, review_after/expiry и disclosure policy. Startup должен проверять persistent instructions как untrusted-until-approved data.

Источники:

- [Meta FAIR: CIMemories code](https://github.com/facebookresearch/CIMemories)
- [Meta FAIR: CIMemories paper v1](https://arxiv.org/abs/2511.14937v1)
- [OpenAI: Dreaming and memory](https://openai.com/index/chatgpt-memory-dreaming/)
- [Anthropic: How we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude)

### 11. Agent-friendly environment важнее длинного prompt

OpenAI и Anthropic связывают надежную автономную работу с быстрыми deterministic tests, isolated workspaces, доступными агенту logs/metrics/traces и короткими objective feedback loops. Плохой verifier заставляет агента оптимизировать неправильную цель.

Решение: `policy_default` для tool-using и long-running workflows, где environment feedback определяет успех: задать objective gate, reset и observability projection. Fast/full split применяется только когда локальный eval подтверждает его пользу и стоимость.

Источники:

- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/)
- [Anthropic: Building a C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)

### 12. Active failure discovery и harness search пока остаются экспериментом

Google ProEval сообщает 8-65x меньше samples, чем competitive baselines, для оценки performance в пределах ±1% от ground truth на изученных benchmarks, одновременно находя более разнообразные failure cases при строгом budget. Stanford Meta-Harness и Microsoft RHO показывают автоматический поиск harness changes. Это сильные research signals, но пока недостаточное основание для unattended production mutation.

Решение: `experiment`. Optimizer не видит final holdout, не меняет grader/policy/sandbox, имеет hard budget, immutable provenance и rollback. `defer` для непрерывного self-modification production system.

Источники:

- [Google DeepMind: ProEval](https://deepmind.google/research/publications/238239/)
- [Stanford IRIS / KRAFTON / MIT: Meta-Harness v1](https://arxiv.org/abs/2603.28052v1)
- [Microsoft Research: RHO](https://www.microsoft.com/en-us/research/publication/retrospective-harness-optimization-improving-llm-agents-via-self-preference-over-trajectory-rollouts/)

## Итоговый приоритет

P0: authority/containment, trusted-control separation, full-trajectory audit, non-compensatory safety, valid eval tasks.

P1: stable runtime boundaries, repeated-trial reliability, infrastructure calibration, conditional ablation of affected assumptions and governed trace-to-eval adaptation. Optional context sufficiency remains an evidence-heavy retrieval experiment.

P2: active failure discovery, memory/playbook optimization и automated harness search только как sandboxed experiments.

Не внедрять как default: multi-agent everywhere, LLM judge как единственный release authority, best-of-N без такого же deployment protocol, raw production-log learning, dynamic unsandboxed tools, irreversible autonomy и unattended production self-modification.
