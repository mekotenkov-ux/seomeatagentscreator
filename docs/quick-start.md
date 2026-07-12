---
---

# Быстрый старт

## 1. Создайте рабочий репозиторий агента

Не разрабатывайте production-агента прямо в чате без файлов. Создайте отдельный репозиторий или папку:

```text
my-agent-dev/
  agent-system/
  runtime/
  devkit/
```

Рекомендуемый вариант - клонировать весь репозиторий: так рядом остаются шаблоны, валидаторы и negative fixtures.

При встраивании в существующий проект минимальный development layout включает:

```text
agent-system/
scripts/
requirements-dev.txt
```

Один `agent-system/` можно переносить как методическую/runtime-часть, но из него нельзя запускать package, install и release validators.

## 2. Запустите preflight

Откройте оба preflight skill:

```text
agent-system/skills/grill-me/SKILL.md
agent-system/skills/workflow-loop-me/SKILL.md
```

Зафиксируйте:

- objective;
- target users;
- maturity mode;
- scope in/out;
- autonomy level;
- risks;
- allowed and forbidden actions;
- data sources;
- target platforms;
- export shape;
- validation method;
- done condition.

Затем через `workflow-loop-me` зафиксируйте candidate loops, выбранный workflow, trigger, inputs, actors, tools, state, artifacts, checkpoints, failure modes и done signal. Если пользователь дает ссылки на репозитории или инструменты, сохраните их через `repo-tool-librarian` как catalog candidates, не как зависимости. Используйте:

```text
agent-system/templates/workflow-notes.template.md
agent-system/templates/workflow-spec.template.md
agent-system/templates/workflow-discovery-ledger.template.json
```

## 3. Создайте IR

Скопируйте:

```text
agent-system/templates/agent-ir.template.json
```

Заполните его до создания платформенных файлов. IR - главный смысловой контракт, а не документация после факта.

## 4. Зафиксируйте harness boundary

До расширения vertical slice заполните:

```text
agent-system/templates/harness-boundary.template.json
agent-system/templates/permission-policy.template.json
agent-system/templates/run-event.template.json
agent-system/templates/harness-assumption-registry.template.json
```

System identity связывает model, instructions, tools, permissions, runtime и graders. Session, harness, sandbox, artifacts и credentials должны иметь отдельные failure boundaries. Permission policy работает по default deny, а external content остается untrusted data и не может расширять authority.

## 5. Создайте birth contract

Скопируйте и адаптируйте:

```text
agent-system/templates/agent-birth-contract.template.json
agent-system/templates/runtime-profile.template.json
agent-system/templates/birth-plan.template.json
agent-system/templates/environment-readiness.template.json
agent-system/templates/project-context.template.json
agent-system/templates/birth-validation-gates.template.json
```

Birth contract нужен до платформенных адаптеров. Он фиксирует, как агент при первом запуске определяет runtime, выбирает активный adapter, проверяет окружение, собирает project context и где останавливается до первой реальной задачи.

## 6. Соберите первый vertical slice

Сначала один полный путь:

- router;
- один workflow;
- один skill;
- один tool path или artifact path;
- один checker;
- один eval set;
- один release gate;
- package check.

Не расширяйте возможности, пока первый путь не проверен.

## 7. Добавьте проверки

Минимум:

- `trigger-lab.template.yaml`;
- `eval-validity-report.template.json`;
- `output-eval-lab.template.yaml`;
- `harness-ablation-lab.template.yaml`;
- `release-decision.template.json`;
- `release-gate-evidence.template.json`;
- `evidence-bundle-manifest.template.json`;
- `external-approval-ledger.template.json`;
- `final-evidence-runbook.template.md`;
- `validation-run-matrix.template.yaml`;
- `tool-registry.template.json`;
- `release-review.template.md`;
- `production-readiness-checklist.md`;
- `export-clean-checklist.md`;
- `stage-quality-gates.template.json`;
- `target-conformance.template.json`;
- `final-evidence-contract.template.json`;
- `independent-review-summary.template.json`;
- `subagent-role-registry.template.json`;
- `subagent-delegation-plan.template.json`;
- `subagent-task-contract.template.json`;
- `subagent-result.template.json`;
- `subagent-run-ledger.template.jsonl`;
- `subagent-eval-lab.template.yaml`.

Если workflow использует subagents, сначала докажите пользу против single-agent baseline. Параллельные write workers должны иметь disjoint ownership и отдельные worktrees/containers; result counts и evidence сверяются до synthesis.

До любого quality claim валидируйте сами eval tasks, frozen holdout и infrastructure. Output Eval проверяет outcome, trajectory, boundary и stability отдельно, использует repeated trials для stochastic agents и отклоняет правильный ответ после hidden unsafe action. После model/runtime/tool change отметьте impact: затронутые assumptions проходят ablation, остальные получают evidence-backed `not_affected`.

## 8. Разделите runtime и devkit

Runtime - только файлы нормальной работы агента.

Devkit - тесты, fixtures, validation scripts, source materials, audit reports и packaging scripts.

## 9. Отлаживайте через sandbox

Для качественной отладки создайте отдельный sandbox-проект, установите туда runtime и работайте из отдельного чата. Агент-создатель должен читать полный trace из sandbox и чинить исходный пакет.

## 10. Соберите и установите clean package

Перед публикацией проверьте:

- нет `.env` и секретов;
- нет закрытых данных;
- нет временных рабочих папок и debug-runs;
- нет доменных скиллов, если пакет универсальный;
- нет локальных абсолютных путей;
- нет скрытой зависимости от истории чата;
- runtime inventory точно совпадает с содержимым архива;
- runtime и devkit собраны в разные zip;
- runtime установлен и проверен из свежей распаковки.

Скопируйте `agent-system/templates/export-manifest.template.json` в корень development repo как `export-manifest.json`, настройте пути относительно этого корня и запустите:

```bash
python -B scripts/verify_public_package.py
python -B scripts/test_harness_release_controls.py
python -B scripts/test_export_safety.py
python -B scripts/build_agent_export.py export-manifest.json --run-install-simulation
```

## 11. Проверьте переносимость

Заполните target conformance matrix, birth protocol, birth validation gates, final evidence contract и runtime/devkit boundary. Если пакет поддерживает несколько платформ, adapters должны быть thin layers поверх одного IR, а не расходящимися копиями промптов.

## 12. Закройте финальный release decision

Сначала получите package, install и independent-review evidence уже для финальных архивов. Затем соберите evidence bundle с реальными SHA-256 и запустите `scripts/validate_harness_release.py`. Финальный `pass` допустим только при точном прохождении всех 13 обязательных gates; `warn`, `pending` и `not_applicable` остаются вне публичного production claim.
