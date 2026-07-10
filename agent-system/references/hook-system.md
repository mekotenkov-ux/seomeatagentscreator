# Hook System

## Что такое hook

Hook - это код, который runtime автоматически вызывает в определенной точке жизненного цикла агента. Скилл дает модели процедуру и знания; hook обеспечивает детерминированную реакцию, даже если модель забыла инструкцию или решила действовать иначе.

Типовой поток:

```text
event -> matcher -> handler -> structured decision/observation -> runtime action
```

Примеры событий: начало сессии, отправка запроса, действие инструментом до выполнения, результат инструмента, ошибка, запуск/остановка subagent, compaction и попытка агента завершить работу.

## Когда нужен hook

Используйте hook, если правило должно выполняться автоматически и проверяемо:

- блокировать опасные команды, публикацию, секреты или изменение защищенных файлов до действия;
- требовать approval для рискованного tool call;
- проверять схему tool input и нормализовать безопасные параметры;
- запускать узкий formatter/linter/test после изменения;
- записывать bounded audit event без transcript и секретов;
- сохранять короткое state перед compaction;
- проверять объективный done condition перед Stop;
- инициализировать проверяемый runtime context в начале сессии.

Не используйте hook для длинной методики, доменных знаний, свободного рассуждения или скрытого промпта. Это работа skills, references и checkers. Не запускайте тяжелый полный test suite после каждого tool call.

## Канонические семейства событий

IR хранит платформенно-нейтральные семейства, а adapter сопоставляет их с native events:

| Семейство | Назначение | Типичная политика |
| --- | --- | --- |
| `session_start` | readiness, короткий context, state recovery | fail-open для подсказки, fail-closed только для обязательной readiness gate |
| `prompt_submit` | классификация риска и bounded context | обычно observe/inject; не логировать сырой prompt по умолчанию |
| `pre_action` | permission, policy, schema, protected paths | fail-closed для security и irreversible actions |
| `post_action` | formatter, narrow validation, audit observation | fail-open для telemetry; fail-closed только если результат нельзя принимать |
| `action_failure` | классификация ошибки и recovery hint | не скрывать исходную ошибку |
| `pre_compact` | сохранить objective, approvals, state и evidence refs | bounded state, без transcript dump |
| `subagent_start_stop` | budget, isolation, result contract | блокировать fan-out сверх бюджета |
| `stop` | hard done gate | ограниченный retry; защита от бесконечного цикла |
| `session_end` | cleanup и итоговый bounded report | cleanup должен быть идемпотентным |

Native support различается. Claude Code имеет богатую модель events/handlers и component-scoped hooks; VS Code hooks находятся в Preview и совместимы с частью Claude/Copilot формата; GitHub Copilot CLI/cloud используют свои event names и разные execution environments. Если runtime не поддерживает нужное событие, target conformance обязан записать degraded behavior. Инструкцию нельзя выдавать за hard enforcement.

## Hook contract

Для каждого hook запишите:

- стабильный `hook_id`, owner, purpose и event family;
- native event mapping для каждого target;
- matcher и точный scope;
- handler type, entrypoint и dependencies;
- input/output schema;
- возможные решения: observe, allow, deny, ask, modify, inject context, continue/stop;
- risk class, side effects и permission boundary;
- timeout, retry, concurrency и idempotency;
- fail mode: open, closed или escalate;
- privacy policy и запрещенные поля;
- evidence/audit destination;
- tests и rollback/disable procedure.

Hook output должен быть машинным и ограниченным. Не смешивайте JSON для runtime с диагностическим текстом в stdout. Не считывайте transcript, shell history, credentials или private logs без отдельного разрешения и redacted source contract.

## Минимальный набор для нового агента

Не добавляйте хуки ради количества. Начните с трех кандидатов и оставьте только доказанно нужные:

1. `pre_action_policy` - schema, protected paths, destructive/external action approval.
2. `post_action_validation` - узкая проверка только измененного артефакта.
3. `stop_done_gate` - внешний done signal, blockers, budgets и max continuation count.

Добавляйте `session_start` и `pre_compact` только если агенту действительно нужны environment readiness или durable state recovery.

## Процесс проектирования

1. После tool registry и permission matrix составьте список правил, которые нельзя оставлять на модельной дисциплине.
2. Для каждого правила выберите механизм: skill, typed tool validation, runtime permission, hook, checker или CI. Предпочитайте самый узкий механизм.
3. Заполните `hook-registry.template.json` без native paths.
4. Определите fail-open/fail-closed, timeout, budgets, privacy и loop guard.
5. Скомпилируйте native config после runtime detection и явного решения пользователя о native adaptation.
6. Запустите `hook-validation.template.yaml`: allow, deny, malformed input, timeout, handler failure, sensitive data, duplicate event и unsupported target.
7. Проверьте hook script как доверенный исполняемый код: агент не должен бесконтрольно переписывать script, который затем сам автоматически запустит.
8. Добавьте evidence в target conformance и release review. Наличие JSON-файла не доказывает enforcement.

## Главные риски

- Компрометация hook script равна компрометации policy gate.
- Fail-open превращает security hook в уведомление; fail-closed может остановить всю работу.
- Stop hook без счетчика продолжений создает бесконечный цикл.
- Несовместимые tool names, casing, matchers и input fields ломают переносимость.
- Async hook не может надежно блокировать уже начавшееся действие.
- Широкий post-action hook делает агента медленным и шумным.
- Логирование prompt/transcript создает утечку данных и не должно включаться по умолчанию.

## Источники

- Claude Code hooks guide: https://code.claude.com/docs/en/hooks-guide
- Claude Code hooks reference: https://code.claude.com/docs/en/hooks
- VS Code agent hooks: https://code.visualstudio.com/docs/agent-customization/hooks
- VS Code hooks reference: https://code.visualstudio.com/docs/agents/reference/hooks-reference
- GitHub Copilot hooks concepts: https://docs.github.com/en/copilot/concepts/agents/hooks
- GitHub Copilot hooks reference: https://docs.github.com/en/copilot/reference/hooks-reference