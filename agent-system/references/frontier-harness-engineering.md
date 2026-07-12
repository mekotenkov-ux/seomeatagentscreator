# Frontier Harness Engineering

Этот reference превращает исследования до 2026-07-11 в консервативную engineering policy этого проекта. Он дополняет Agent/Skill IR, tool registry, hooks, subagent orchestration и release review. Это набор выбранных controls, а не утверждение, что каждая архитектурная деталь доказана универсальным performance experiment; evidence и ограничения перечислены в dated research map.

## 1. Зафиксируйте system-under-test

Сравнивайте не модели, а полные версии систем. Для каждого eval, incident и release храните:

- model snapshot и reasoning configuration;
- harness/runtime commit;
- hashes instructions, tool schemas, permission policy и graders;
- sandbox image, OS/dependency lock, CPU/RAM floor и kill ceiling;
- network, cache, timeout, concurrency и retry policy;
- task distribution, dataset version/split и holdout policy;
- budgets и фактический расход tokens, tools, runtime и cost.

Канонический артефакт: `harness-boundary.template.json`.

## 2. Разделите session, harness, sandbox и artifacts

Session - append-only event history. Harness - заменяемый loop и policy router. Sandbox - disposable execution environment. Artifact store - независимое место для результатов и evidence.

Обязательные свойства:

- state хранится вне ephemeral compute;
- sandbox можно уничтожить и восстановить по provision recipe;
- checkpoint/rehydration проверены реальным crash drill;
- durable credentials не попадают в untrusted execution filesystem или environment; target-native short-lived scoped delivery допускается только с отдельным enforcement evidence;
- tool/MCP calls предпочтительно получают short-lived scoped authority через target-native broker/proxy или эквивалентный runtime-enforced mechanism;
- completed, cancelled и unknown-outcome runs проходят reconciliation и cleanup.

## 3. Исполняйте authority вне модели

Prompt не является permission boundary. Используйте `permission-policy.template.json` и default deny.

Каждый grant связывает:

- principal: user, parent agent, subagent, tool или automation;
- operation;
- resource и точный scope;
- normalized arguments или artifact hash;
- side-effect/risk class;
- budget;
- issued_at, expires_at и revocation state;
- runtime enforcement evidence.

Approval на один action нельзя переиспользовать после изменения arguments, resource version, target, cost или authority scope.

## 4. Разделите trusted control и untrusted data

Внешние документы, web pages, tool results, MCP metadata, repo instructions до trust decision, subagent summaries и persistent memory по умолчанию являются data, а не instructions.

На каждом context item сохраняйте provenance, integrity, classification, purpose, retention и allowed sinks. Untrusted data не может:

- расширять permissions;
- менять policy, grader, budgets или sandbox;
- выбирать новый principal;
- создавать доверенную instruction без отдельного approval;
- направлять секреты в новый sink.

Project-local hooks/config загружаются только после trust decision. Symlinks и junctions разрешаются до path authorization.

## 5. Ведите append-only run events

`run-event.template.json` является общей шиной observability. Событие должно иметь trace/span/parent ids, монотонный sequence, actor/principal, system hashes, state revision, budget delta, permission decision, tool/effect status, provenance и artifact refs.

Raw chain-of-thought не требуется и не должен экспортироваться по умолчанию. Для audit обязательны наблюдаемые intent summary, actions, transfers, approvals, tool results и state deltas.

## 6. Проверяйте trajectory и outcome отдельно

Output Eval Lab содержит четыре независимых grader families:

1. `outcome` - фактическое состояние среды и deliverables;
2. `trajectory` - порядок exploration, implementation, verification, retries и stop;
3. `boundary` - permissions, data flow, inter-agent transfer и unsafe effects;
4. `stability` - infra errors, recovery, cancellation, idempotency и resource behavior.

LLM judge дополняет deterministic и human graders, но не является единственным authority для safety или irreversible actions. P0 violation блокирует release независимо от среднего quality score.

## 7. Сначала валидируйте eval

До использования benchmark score заполните `eval-validity-report.template.json`:

- полный task inventory и reconciled dispositions;
- reference solution или feasibility witness;
- requirement-to-grader map;
- hidden-test coverage и mutation check;
- ambiguity, contamination, shortcut и answer-leak checks;
- predeclared exclusions;
- independent defect review;
- frozen holdout, недоступный optimizer/agent creator.

Broken, underspecified или leaking tasks не удаляются молча после просмотра результатов. Публикуйте raw intention-to-test и adjudicated results отдельно.

## 8. Измеряйте stochastic reliability

Если deployment не является детерминированным, делайте repeated independent trials с clean reset. Report:

- `pass@1`;
- `pass@k` только когда deployment действительно допускает k attempts и имеет selector;
- consistency (`pass^k` или эквивалент) для customer-facing reliability;
- critical-failure probability;
- confidence intervals;
- latency, tokens, tool calls и cost;
- infra failures отдельно от task failures.

Best trace не является evidence для обычного single-attempt deployment.

## 9. Калибруйте infrastructure noise

Перед сравнительным claim проведите A/A runs в fresh environments. Если measured infrastructure spread сравним с claimed improvement, результат считается tie или experiment. Не подменяйте модельную ошибку OOM, flaky service, browser drift, rate limit или unavailable dependency.

## 10. Удаляйте устаревший scaffold

Каждый harness component фиксируется в `harness-assumption-registry.template.json`: какую слабость модели он компенсирует, evidence, overhead, owner, review trigger и ablation case.

После model/runtime/tool upgrade или смены task distribution отметьте, какие assumptions затронуты. Для model-dependent компонентов проведите `harness-ablation-lab.template.yaml`; для незатронутых запишите `not_affected` с evidence. Удаляйте по одному компоненту при matched budgets. Retain разрешен при deterministic-control rationale или измеримом quality/safety lift, который оправдывает cost/latency/complexity. Автоматический ablation после каждого upgrade остается экспериментальной policy.

## 11. Экспериментально проверяйте достаточность context в evidence-heavy retrieval workflows

Если локальный eval показывает пользу, перед synthesis evidence-heavy retrieval checker сверяет original requirements, available evidence и draft. Для других workflows этот gate не обязателен. Он возвращает:

- covered requirement ids;
- missing evidence и unresolved contradictions;
- точные bounded acquisition queries;
- `sufficient|insufficient|blocked`;
- stop reason и budget remaining.

Context-sufficiency gate не означает бесконечный retrieval: budgets и невозможности остаются видимыми.

## 12. Улучшайте harness только через governed loop

Production traces не становятся training data автоматически. Разрешен следующий loop:

1. Approved redacted source path.
2. Expert-reviewed findings, отделенные от expected workflow noise.
3. Diverse failure coreset и untouched holdout.
4. Candidate change в isolated branch/sandbox.
5. Targeted, regression, safety и holdout evals при matched budgets.
6. Independent review, human approval, canary, rollback.
7. Durable change или explicit rejection with evidence.

`living-adaptation-decision.template.json` по умолчанию запрещает automatic application. Optimizer не может менять graders, permissions, logs, budgets, sandbox или final holdout.

## 13. Release gate

Для production/library/governed claims `scripts/validate_harness_release.py` принимает:

- harness boundary и permission policy;
- external approval ledger;
- append-only run-event JSONL;
- assumption registry и conditional ablation lab;
- eval validity и Output Eval Lab;
- confined SHA-256 evidence bundle;
- machine-readable release decision.

Валидатор пересчитывает hashes, связывает system release ids, сверяет task/trial counts, tool permission/effect lifecycle, budgets и ровно 13 обязательных gates. Package, fresh-extraction install и independent review входят в финальный набор. `warn`, `pending`, `not_applicable`, unresolved refs и самостоятельно выставленные booleans не являются финальным `pass`.

Template integrity и regression fixtures проверяют `scripts/verify_public_package.py`, `scripts/test_harness_release_controls.py` и `scripts/test_export_safety.py`; они не заменяют filled-run evidence конкретного агента.

## Experimental Boundary

Experiment only: automated harness search, active failure discovery, dynamic memory/playbook optimization и self-critique/self-preference как optimizer signal.

Deferred by default: unsandboxed generated tools, raw-log learning without consent, continuously self-modifying production agents, best-of-N claims for single-attempt deployment, irreversible high-stakes autonomy и multi-agent topology без matched-budget baseline.
## Evidence Mapping

- System identity, eval validity, infrastructure recording and trajectory grading: sections 1-3 of `frontier-harness-research-2026-07.md`.
- Session/harness/sandbox separation and containment: sections 4-5.
- Assumption registry and conditional ablation: section 6; automatic trigger remains experimental.
- Task-dependent multi-agent topology: section 7.
- Optional context sufficiency experiment: section 8.
- Governed trace-to-improvement and memory policy: sections 9-10.
- Environment feedback for tool-using/long-running workflows: section 11.
- Automated harness search and active failure discovery: section 12, experiment only.
