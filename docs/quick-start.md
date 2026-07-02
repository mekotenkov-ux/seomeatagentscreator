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

## 4. Соберите первый vertical slice

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

## 5. Добавьте проверки

Минимум:

- `trigger-lab.template.yaml`;
- `output-eval-lab.template.yaml`;
- `tool-registry.template.json`;
- `release-review.template.md`;
- `production-readiness-checklist.md`;
- `export-clean-checklist.md`.

## 6. Разделите runtime и devkit

Runtime - только файлы нормальной работы агента.

Devkit - тесты, fixtures, validation scripts, source materials, audit reports и packaging scripts.

## 7. Отлаживайте через sandbox

Для качественной отладки создайте отдельный sandbox-проект, установите туда runtime и работайте из отдельного чата. Агент-создатель должен читать полный trace из sandbox и чинить исходный пакет.

## 8. Публикуйте только clean package

Перед публикацией проверьте:

- нет `.env`;
- нет приватных данных;
- нет debug-runs;
- нет `dev/work/`;
- нет доменных скиллов, если пакет универсальный;
- нет локальных абсолютных путей;
- нет скрытой зависимости от истории чата.
