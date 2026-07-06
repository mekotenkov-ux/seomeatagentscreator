# Быстрый старт

## 1. Создайте рабочий репозиторий агента

Не разрабатывайте production-агента прямо в чате без файлов. Создайте отдельный репозиторий или папку:

```text
my-agent-dev/
  agent-system/
  package/
  devkit/
```

Скопируйте `agent-system/` из этого репозитория.

## 2. Запустите preflight

Откройте:

```text
agent-system/skills/grill-me/SKILL.md
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

## 3. Создайте IR

Скопируйте:

```text
agent-system/templates/agent-ir.template.json
```

Заполните его до создания платформенных файлов. IR - главный смысловой контракт, а не документация после факта.

## 4. Создайте birth contract

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

## 5. Соберите первый vertical slice

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

## 6. Добавьте проверки

Минимум:

- `trigger-lab.template.yaml`;
- `output-eval-lab.template.yaml`;
- `tool-registry.template.json`;
- `release-review.template.md`;
- `production-readiness-checklist.md`;
- `export-clean-checklist.md`;
- `stage-quality-gates.template.json`;
- `target-conformance.template.json`;
- `final-evidence-contract.template.json`;
- `independent-review-summary.template.json`.

## 7. Разделите runtime и devkit

Runtime - только файлы нормальной работы агента.

Devkit - тесты, fixtures, validation scripts, source materials, audit reports и packaging scripts.

## 8. Отлаживайте через sandbox

Для качественной отладки создайте отдельный sandbox-проект, установите туда runtime и работайте из отдельного чата. Агент-создатель должен читать полный trace из sandbox и чинить исходный пакет.

## 9. Публикуйте только clean package

Перед публикацией проверьте:

- нет `.env`;
- нет закрытых данных;
- нет временных рабочих папок и debug-runs;
- нет доменных скиллов, если пакет универсальный;
- нет локальных абсолютных путей;
- нет скрытой зависимости от истории чата.

## 10. Проверьте переносимость

Перед публикацией заполните target conformance matrix, birth protocol, birth validation gates, final evidence contract и runtime/devkit boundary. Если пакет поддерживает несколько платформ, adapters должны быть thin layers поверх одного IR, а не расходящимися копиями промптов.
