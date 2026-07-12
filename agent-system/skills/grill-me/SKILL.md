---
name: grill-me
description: Используйте перед созданием нового агента, скилла или крупного agent workflow, чтобы по одному вопросу за раз прояснить цель, пользователей, scope, автономию, риски, источники, платформы, экспорт, валидацию и done condition.
---

# Grill Me

Задача - не заполнить анкету, а убрать архитектурную неопределенность до начала разработки.

## Правила

- Задавайте один материальный вопрос за раз.
- Объясняйте, почему решение важно, если это не очевидно.
- Предлагайте рекомендуемый default.
- Если ответ можно узнать из репозитория, файлов или артефактов, сначала инспектируйте их.
- Не переходите к архитектуре, пока остается blocker по цели, scope, риску, данным, платформе, экспорту, валидации или done condition.

## Что нужно выяснить

1. Objective: какой результат агент должен производить.
2. Target users: кто будет им пользоваться.
3. Maturity mode: `production`, `library`, `governed` или явно временный `scaffold`.
4. Scope in/out: что агент делает и что не делает.
5. Autonomy level: answer-only, draft-only, approval-gated action, bounded autonomous action, long-running goal.
6. Risk level: read, local write, external write, paid API, destructive, regulated/high-stakes.
7. Allowed actions.
8. Forbidden actions.
9. Data sources.
10. Target platforms.
11. Export shape: runtime, devkit, zip, repo, native skill package.
12. Validation method.
13. Done condition.

## Выход preflight

Запишите решения в brief или IR. Если вопрос был не нужен, потому что ответ найден в файлах, укажите источник. До перехода к архитектуре просмотрите `../repo-tool-librarian/SKILL.md` и зафиксируйте оценку `obra/superpowers`: `not_relevant`, `consider`, `selected_by_user` или `declined_by_user`. Это опциональная методология для мета-агента, а не обязательная часть создаваемого агента. Спросите пользователя только если ее применение реально меняет процесс, добавляет plugin/dependency/hook, права или поставку. После этого перед архитектурой агента запустите `../workflow-loop-me/SKILL.md`, чтобы описать реальные loops/workflows, которые агент должен поддерживать.
