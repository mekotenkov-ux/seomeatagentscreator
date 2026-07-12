# Seomeat Agents Creator

Открытая русскоязычная методика для создания production-grade AI-агентов и скиллов: от первичного замысла и Agent/Skill IR до проверки, упаковки, публикации и сопровождения.

Система помогает проектировать агентов как инженерные продукты: с понятной задачей, границами ответственности, проверяемыми инструментами, оценками качества, release gates и переносимым runtime-пакетом.

## Для кого

- Для разработчиков, которые делают агентов не как один большой промпт, а как проверяемую систему.
- Для команд, которым нужны воспроизводимые скиллы, checkers, tools, evals и installable runtime.
- Для авторов образовательных и прикладных AI-процессов, которым нужна понятная методика упаковки своих знаний в agent workflows.

## Создано в школе "SEO Мясо"

Подход вырос из практики школы и прикладных проектов SEOMeat. Больше о школе и SEO-подходе: [seomeat.ru](https://seomeat.ru/).

## Главный принцип

Модель предлагает действия. Runtime, инструменты, проверки, разрешения, логи и артефакты доказывают, что действие допустимо и результат действительно готов.

Не полагайтесь на "модель сама аккуратно сделает". Для production-grade агента нужны:

- workflow discovery перед IR;
- repo/tool catalog для внешних ссылок и идей;
- Agent/Skill IR;
- versioned system identity;
- harness boundary: session, harness, sandbox, artifacts и credential broker;
- router и focused skills;
- typed tool registry;
- default-deny permission policy и approval binding;
- provenance-aware trusted-control/data-flow policy;
- append-only run-event contract;
- hook registry и lifecycle gates;
- subagent orchestration: topology, role registry, task graph, isolation, lifecycle и eval;
- state/memory вне истории чата;
- context packaging;
- trigger lab;
- eval-validity report до score;
- trajectory-aware output eval: outcome, trajectory, boundary и stability;
- repeated trials и infrastructure-noise calibration;
- Harness Assumption Registry и Ablation Lab;
- checker/reviewer layer;
- skill training lab и skill-candidate lifecycle;
- birth contract и first-run artifacts;
- target conformance matrix;
- final evidence contract;
- release review;
- machine-readable release decision;
- runtime/devkit boundary;
- package verification;
- install simulation;
- post-birth cleanup;
- public claim guard.

## Быстрый старт

1. Клонируйте весь репозиторий. Для встраивания в существующий проект минимально перенесите `agent-system/`, `scripts/` и `requirements-dev.txt`: без scripts доступны шаблоны, но недоступны исполняемые release gates.
2. Откройте `agent-system/AGENTS.md` как корневую инструкцию для агента-создателя.
3. Запустите preflight по `agent-system/skills/grill-me/SKILL.md`, затем workflow discovery по `agent-system/skills/workflow-loop-me/SKILL.md`.
4. Заполните workflow notes/spec/ledger и `agent-system/templates/agent-ir.template.json`.
6. Соберите первый vertical slice: router, один workflow, один skill, один tool path, один checker, один eval set.
5. Зафиксируйте system identity, harness boundary, permission policy и run-event contract.
7. Проведите hook design pass: автоматические gates, fail modes, privacy, native mappings и validation cases.
8. Проведите subagent design pass: необходимость делегирования, topology, роли, task graph, context, isolation, budgets и result contracts.
9. Проверьте Subagent Eval Lab против matched-budget single-agent baseline.
10. Проверьте валидность eval tasks, frozen holdout и infrastructure noise.
11. Запустите Trigger Lab и trajectory-aware Output Eval Lab с repeated trials.
12. Проведите ablation затронутых harness assumptions; для остальных запишите evidence-backed `not_affected`.
13. Разделите runtime и devkit.
14. Соберите clean staging, runtime zip и devkit zip; проверьте архив и установку в fresh sandbox.
15. Проведите независимые scenario-аудиты уже собранного пакета.
16. Только после package/install/audit evidence сформируйте финальный machine release decision и публикуйте.

Подробно: [быстрый старт](docs/quick-start.md), [как распаковывать](docs/unpack-and-use.md), [упаковка runtime/devkit](docs/packaging.md) и [frontier harness](docs/frontier-harness.md).

## Рекомендация по качественной отладке

Для качественной отладки рекомендуется создавать отдельный проект под конкретного агента, подключать туда создаваемого агента и из отдельного чата выполнять реальную работу. Тогда агент-создатель видит полный лог, наблюдает, где целевой агент путается, и может чинить систему по фактическому trace, а не по пересказу.

Практический паттерн:

1. `agent-dev/` - репозиторий, где вы проектируете agent package.
2. `agent-sandbox/` - отдельный проект, куда вы устанавливаете runtime как fresh user.
3. `debug-chat` - отдельный чат, который работает как целевой агент в sandbox.
4. `creator-chat` - чат агента-создателя, который читает артефакты, логи и checker reports из sandbox и чинит исходный пакет.

## Гигиена публичного пакета

Перед публикацией проверяйте, что пакет не содержит секреты, локальные пути, закрытые данные, временные рабочие артефакты и скрытую зависимость от истории текущего чата. Установите dev-зависимости через `python -m pip install -r requirements-dev.txt`, затем запустите `python -B scripts/verify_public_package.py`, `python -B scripts/test_harness_release_controls.py` и `python -B scripts/test_export_safety.py`. Заполненные subagent-run артефакты дополнительно проверяет `scripts/validate_subagent_run.py`. Заполненный набор frontier harness release evidence проверяет `scripts/validate_harness_release.py`; наличие шаблонов или самостоятельно выставленного `pass` доказательством не является.

## Структура

```text
agent-system/
  AGENTS.md
  skills/
    agent-creator/
      SKILL.md
      references/production-skill-os.md
    grill-me/
      SKILL.md
    workflow-loop-me/
      SKILL.md
    repo-tool-librarian/
      SKILL.md
    subagent-orchestrator/
      SKILL.md
  references/
    skill-training-lab.md
    package-boundary.md
    repo-tool-library.md
    birth-protocol.md
    ide-runtime-adaptation.md
    hook-system.md
    subagent-orchestration.md
    frontier-harness-engineering.md
    frontier-harness-research-2026-07.md
    context-and-quality-gates.md
    target-adapters.md
    final-evidence-and-claim-guard.md
    long-running-tool-lifecycle.md
    universal-core-isolation.md
    observability-and-living-adaptation.md
    validation-harness.md
  catalog/
    README.md
    repo-tool-library.json
    repo-tool-cards/
  templates/
    workflow-notes.template.md
    workflow-spec.template.md
    workflow-discovery-ledger.template.json
    repo-tool-library.template.json
    repo-tool-card.template.md
    repo-tool-intake.template.md
    agent-ir.template.json
    agent-birth-contract.template.json
    runtime-profile.template.json
    birth-plan.template.json
    environment-readiness.template.json
    project-context.template.json
    birth-validation-gates.template.json
    tool-registry.template.json
    hook-registry.template.json
    hook-validation.template.yaml
    subagent-role-registry.template.json
    subagent-delegation-plan.template.json
    subagent-task-contract.template.json
    subagent-result.template.json
    subagent-run-ledger.template.jsonl
    subagent-eval-lab.template.yaml
    runtime-manifest.template.json
    release-review.template.md
    trigger-lab.template.yaml
    output-eval-lab.template.yaml
    harness-boundary.template.json
    permission-policy.template.json
    run-event.template.json
    harness-assumption-registry.template.json
    harness-ablation-lab.template.yaml
    eval-validity-report.template.json
    release-decision.template.json
    release-gate-evidence.template.json
    evidence-bundle-manifest.template.json
    external-approval-ledger.template.json
    final-evidence-runbook.template.md
    validation-run-matrix.template.yaml
    target-conformance.template.json
    final-evidence-contract.template.json
    independent-review-summary.template.json
    stage-quality-gates.template.json
    state.template.md
    local-memory.template.md
    export-manifest.template.json
  checklists/
    export-clean-checklist.md
    production-readiness-checklist.md
scripts/
  verify_public_package.py
  validate_harness_release.py
  validate_subagent_run.py
  build_agent_export.py
  validate_runtime_install.py
  check_core_isolation.py
  test_harness_release_controls.py
  test_export_safety.py
requirements-dev.txt
docs/
  index.html
  quick-start.md
  architecture.md
  frontier-harness.md
  hooks.md
  subagents.md
  birth.md
  workflow-discovery.md
  repo-tool-library.md
  unpack-and-use.md
  debugging.md
  packaging.md
```

## Лицензия

MIT. См. [LICENSE](LICENSE).
