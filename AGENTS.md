# Seomeat Agents Creator

Этот репозиторий содержит универсальную систему создания агентских систем и скиллов.

## Назначение

Помогать проектировать, отлаживать, проверять, упаковывать и публиковать агентские системы так, чтобы они работали для fresh-agent без скрытого контекста текущего чата.

## Рабочий порядок

1. Прочитайте `agent-system/AGENTS.md`.
2. Для нового агента начните с `agent-system/skills/grill-me/SKILL.md`, затем проведите workflow discovery по `agent-system/skills/workflow-loop-me/SKILL.md`.
3. До написания адаптеров заполните workflow notes/spec/ledger и `agent-system/templates/agent-ir.template.json`.
4. До заявлений о готовности создайте versioned system identity, harness boundary, default-deny permission policy, approval ledger, append-only run events, Eval Validity, Trigger Lab, trajectory-aware Output Eval и Assumption Registry. Затем соберите package, проверьте fresh install и independent review; только после этого закройте SHA-256 evidence bundle и финальный machine release decision по всем 13 gates.
5. Если пользователь дает ссылки на репозитории или инструменты, индексируйте их через `agent-system/skills/repo-tool-librarian/SKILL.md`; не встраивайте их без отдельного явного запроса.
6. Держите репозиторий универсальным: публикуйте только повторяемую методику, шаблоны, инструкции и чеклисты.
7. Используйте `agent-system/references/frontier-harness-engineering.md`; research-only приемы остаются experiment/defer до локального matched-budget holdout.

## Язык

Основной язык проекта: русский. Английские имена файлов и полей используются только для переносимости между инструментами.

## Безопасность

Публиковать можно только универсальные материалы:

- инструкции;
- шаблоны;
- checklists;
- публичные docs;
- нейтральные примеры без данных реальных проектов.

Нельзя публиковать:

- `.env`, токены, cookies, реальные credentials;
- временные рабочие папки, debug-runs, browser profiles;
- конкретные доменные скиллы и агенты;
- непубличные источники, логи, отчеты, raw exports;
- локальные абсолютные пути;
- файлы, которые предполагают историю текущего чата.
