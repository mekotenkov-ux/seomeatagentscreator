---
---

# Хуки в агентах и скиллах

Хук - это автоматический обработчик события в работе агента. Он срабатывает не потому, что модель вспомнила инструкцию, а потому, что runtime дошел до конкретной точки: начал сессию, собирается вызвать инструмент, получил результат, запускает subagent, сжимает контекст или пытается закончить задачу.

Скилл отвечает на вопрос «как выполнить работу». Хук отвечает на вопрос «что обязательно проверить или сделать в этой точке».

## Что можно вшить в агента

- Перед tool call: проверить схему, риск, защищенные пути и необходимость approval.
- После изменения файла: запустить formatter или узкую проверку измененного артефакта.
- Перед compaction: сохранить objective, approvals, blockers, state и evidence refs.
- Перед завершением: проверить тесты, обязательные артефакты и внешний done signal.
- При ошибке: записать bounded observation и разрешенные recovery actions.

## Как добавлять

1. Сначала опишите tool registry и permission matrix.
2. Выпишите правила, которые нельзя оставлять только в промпте.
3. Заполните `agent-system/templates/hook-registry.template.json`.
4. Выберите для каждого правила fail-open, fail-closed или escalation.
5. После определения IDE/runtime сопоставьте универсальное событие с native hook.
6. Проверьте allow/deny, timeout, ошибки, privacy, idempotency и Stop loop guard через `hook-validation.template.yaml`.
7. Только после execution evidence отмечайте native enforcement как подтвержденный.

Не включайте логирование сырых prompts, transcripts, shell history и секретов. Не давайте агенту свободно менять hook script, который тот же runtime затем автоматически исполняет.

Полный контракт: [Hook System](../agent-system/references/hook-system.md).