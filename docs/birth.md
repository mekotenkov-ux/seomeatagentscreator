# Рождение агента и первый запуск

Birth - это первый запуск установленного агента в новом проекте. Его задача не в том, чтобы сразу работать, а в том, чтобы безопасно понять среду, не сломать IDE-инструкции и собрать минимальный контекст проекта.

## Короткая схема

1. **Import boundary**: понять, это установленный runtime, devkit или staging.
2. **Runtime detection**: определить Codex, Claude Code, Cursor, VS Code Copilot, GitHub Copilot, OpenCode, Gemini CLI или локальный CLI.
3. **Active adapter decision**: выбрать активный entrypoint и не трогать остальные без уверенности.
4. **Native layout adaptation**: спросить перед merge/convert skills, commands, checkers, hooks или MCP.
5. **Environment readiness**: проверить команды, write paths, env templates, optional connectors и permission gates.
6. **Project context intake**: собрать контекст проекта одним вопросом за раз.
7. **First workflow selection**: предложить один следующий шаг по реальной миссии агента.
8. **Birth gate**: зафиксировать артефакты и остановиться до явного старта задачи.

## Артефакты

Используйте шаблоны:

```text
agent-system/templates/agent-birth-contract.template.json
agent-system/templates/runtime-profile.template.json
agent-system/templates/birth-plan.template.json
agent-system/templates/environment-readiness.template.json
agent-system/templates/project-context.template.json
agent-system/templates/birth-validation-gates.template.json
```

## Главное правило

Environment adaptation идет до project adaptation. Агент не должен читать исходники проекта, спрашивать бизнес-доменные детали или запускать работу, пока не понятны runtime, активная native instruction surface, workspace root, state paths, permissions и cleanup policy.

## IDE adaptation

Адаптеры должны быть тонкими. Для Codex это обычно `AGENTS.md`, для Claude Code - `CLAUDE.md` и `.claude/`, для Cursor - `.cursor/rules/`, для VS Code/GitHub Copilot - `.github/copilot-instructions.md`, `.github/instructions/`, `AGENTS.md`, prompt files, skills и custom agents. Эти файлы должны ссылаться на один контракт, а не копировать всю систему в разные версии.

## Что нельзя

- Нельзя превращать сохранение adapters/export state в миссию установленного агента.
- Нельзя молча объединять `AGENTS.md`, `CLAUDE.md`, Cursor rules или Copilot instructions.
- Нельзя удалять protected files: router, IR, skills, tools, references, templates, schemas, state, memory, license и package code.
- Нельзя считать наличие adapter file доказательством поддержки платформы.
- Нельзя начинать первую рабочую задачу в том же turn, если пользователь явно не попросил.