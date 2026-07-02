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
