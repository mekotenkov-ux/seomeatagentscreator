# Отладка агентских систем

## Главная рекомендация

Для качественной отладки рекомендуется создавать отдельный проект под конкретного агента, подключать туда агента и из отдельного чата выполнять реальную работу.

Это нужно, чтобы агент-создатель видел:

- полный лог;
- state files;
- tool observations;
- generated artifacts;
- checker reports;
- места, где целевой агент запутался;
- что было неочевидно для fresh-agent.

## Рабочая схема

```text
creator-repo/
  package-source/
  devkit/

sandbox-project/
  installed-runtime/
  task-artifacts/
  checks/
  logs/
```

Один чат играет роль целевого агента в `sandbox-project`. Второй чат играет роль agent creator и чинит `creator-repo`.

## Что фиксировать

- Неясный trigger.
- Неполный context pack.
- Tool skip без видимого not-done.
- Checker принимает narrative вместо evidence.
- Runtime читает devkit-файлы.
- State file разрастается в лог.
- Пользователь должен объяснять то, что агент мог прочитать.

## Как превращать ошибки в улучшения

1. Подтвердите failure по артефактам.
2. Исправьте source of truth.
3. Добавьте regression check.
4. Пересоберите runtime.
5. Повторите sandbox run.

## Skill Training Lab

Повторяемые ошибки и удачные процедуры сначала записываются как skill candidates. Перед тем как сделать их runtime skill, прогоните fresh-context или subagent forward-testing: проверяющий получает skill, реалистичную задачу и compact artifacts, но не получает intended fix или ожидаемый ответ.

## Machine Records

Сохраняйте `workflow_runs`, `subagent_runs`, `tool_observations`, `stage-quality-gates` и `living-adaptation-decision`. Если решение не требует durable update, запишите `no_update_reason`, чтобы не превращать шум в методику.
