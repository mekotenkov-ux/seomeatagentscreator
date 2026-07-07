---
name: workflow-loop-me
description: Используйте вместе с grill-me перед созданием агента, чтобы подробно расспросить пользователя о повторяемых рабочих процессах, найти loops, выбрать workflow-кандидаты и довести каждый workflow spec до состояния, когда реализующий агент не задаст дополнительных вопросов.
---

# Workflow Loop Me

Задача - не просто понять, какого агента хочет пользователь, а выяснить, какие повторяемые рабочие процессы реально стоит делегировать агенту.

Используйте после `grill-me` и до архитектуры агента.

Prior art: loop/workflow lens вдохновлен открытым MIT skill `loop-me` by Matt Pocock: https://github.com/mattpocock/skills/blob/main/skills/in-progress/loop-me/SKILL.md

## Главный принцип

Ищите loops: повторяемые паттерны в работе пользователя, команды, недели, дня, канала, inbox, issue flow, продажах, контенте, QA, исследованиях, отчетности или поддержке.

Workflow - это спецификация одного loop, которую можно реализовать как агентский процесс, обычный checklist, automation, tool run или гибрид. Не навязывайте AI, расписание, checkpoint или автономию, если интервью не доказало, что они нужны.

## Правила интервью

- Задавайте один материальный вопрос за раз.
- Для каждого вопроса давайте recommended default, если он уместен.
- Не превращайте разговор в длинную анкету.
- Сначала ищите существующие артефакты: docs, tickets, reports, scripts, spreadsheets, inbox labels, calendars, SOPs, dashboards, logs.
- Записывайте язык пользователя: как он сам называет каналы, события, роли, артефакты и проблемы.
- Не проектируйте агента, пока ключевой workflow не описан как реализуемая спецификация.

## Vocabulary

Используйте эти термины только когда они помогают уточнить процесс:

- Loop - повторяемая активность или ситуация.
- Workflow spec - документированная версия loop, пригодная для реализации.
- Trigger - событие или расписание, которое запускает run.
- Input - что приходит на вход: файл, issue, письмо, чат, URL, таблица, запрос, сигнал.
- Actor - кто участвует: пользователь, клиент, reviewer, agent, tool, external system.
- Tool/channel - где workflow живет: repo, CRM, docs, messenger, inbox, dashboard, IDE, CMS.
- State - что нужно помнить между runs.
- Artifact - что workflow создает или меняет.
- Checkpoint - где человек должен принять решение или проверить результат.
- Brief - короткая decision-ready выжимка для checkpoint, а не raw draft.
- Push right - отложить checkpoint как можно дальше, чтобы человек видел уже подготовленное решение.
- Done signal - внешний признак, что run завершен.
- Failure mode - как workflow ломается и что делать.

## Process

1. World notes.
   - Соберите карту мира пользователя: роли, проекты, каналы, повторяющиеся задачи, инструменты, боли, ручные проверки, частые исключения.
   - Если заметок мало, интервьюируйте пользователя о его реальной неделе/дне/каналах до выбора агента.
2. Loop inventory.
   - Предложите 3-7 candidate loops, включая те, которые пользователь мог не заметить.
   - Для каждого loop запишите trigger, frequency, pain, current manual steps, inputs, outputs, risk, automation fit.
3. Workflow selection.
   - Выберите один loop для первой реализации: частый, ценный, проверяемый, с понятными входами и done signal.
   - Отложите широкие или рискованные loops в backlog.
4. Workflow spec.
   - Опишите trigger, inputs, actors, tools, state, artifacts, steps, checkpoints, permissions, failure modes, validation, budgets, done signal.
   - Укажите, где checkpoint можно push right, а где approval обязателен.
5. Agent fit.
   - Решите, нужен ли агент, skill, automation, tool, checklist, dashboard, или комбинация.
   - Не создавайте агента там, где хватает простой процедуры или deterministic script.
6. Implementation readiness.
   - Workflow spec готов только когда fresh implementer agent может построить его без уточняющих вопросов.

## Repo/Tool Library Handoff

If the user mentions useful repositories or tools during workflow discovery, send those links through `../repo-tool-librarian/SKILL.md`. Do not integrate them into the workflow spec by default; record them as idea candidates and ask before selection.

## Outputs

Рекомендуемые файлы:

- `workflow-notes.md` - словарь мира пользователя и сырые наблюдения.
- `workflow-specs/<workflow-id>.md` - одна спецификация на один workflow.
- `workflow-discovery-ledger.json` - candidate loops, выбранный first workflow, descopes, blockers и next questions.

## Done Condition

Workflow discovery завершен только когда:

- есть список candidate loops;
- выбран первый workflow или записан blocker;
- у выбранного workflow есть trigger, inputs, actors, tools, state, artifacts, steps, checkpoints, permissions, failure modes, validation, done signal;
- known unknowns видимы;
- следующий шаг для agent architecture понятен;
- не осталось вопроса, без ответа на который implementer agent будет гадать.