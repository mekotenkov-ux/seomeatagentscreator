# Skill Training Lab

Skill training здесь означает не обучение модели, а проверяемую эволюцию скилла на реальных задачах.

## Цель

Не создавать постоянный skill после одного удачного чата. Сначала процедура становится `skill_candidate`, проходит реальные прогоны, получает evidence, boundaries и validation, и только потом повышается до runtime skill или workflow.

## Жизненный цикл

- `proposed` - один прогон подсказал повторяемый ход, но доказательств мало.
- `draft` - есть trigger, inputs, outputs, steps и boundaries, но нужен повторный прогон.
- `accepted` - пользователь или повторяемые evidence подтверждают, что это должен быть skill/workflow.
- `implemented` - skill/workflow добавлен в runtime и покрыт trigger/output/package checks.
- `rejected` - слишком узко, небезопасно, плохо доказано или заменено другим механизмом.

## Кандидат В Skill

Кандидат должен иметь:

- понятный trigger;
- should-trigger и should-not-trigger cases;
- repeatable procedure;
- expected inputs и outputs;
- evidence refs хотя бы из одного реального run;
- failure cases и boundaries;
- tool/permission needs;
- validation или review gate;
- owner и review cadence.

## Forward Testing

После существенной правки skill запускают на fresh context или через независимых subagents.

Правильная задача для проверяющего агента:

```text
Use <skill-name> at <path-to-skill> to solve <realistic task>.
```

Неправильно:

```text
Review this skill and pretend a user asks...
```

Проверяющий не должен видеть ожидаемый ответ, intended fix, hidden diagnosis или выводы автора. Он получает skill, задачу и разрешенные source artifacts.

## Promotion Gate

Перед переводом кандидата в `implemented` проверьте:

- fresh agent понимает trigger без истории текущего чата;
- Output Eval показывает улучшение или фиксирует limitation;
- Trigger Lab не крадет near-neighbor routes;
- tool needs имеют registry entries и permission gates;
- checker или reviewer может отвергнуть слабый результат;
- runtime/devkit boundary понятен;
- public claims не превышают evidence.

## Не Делать

- Не повышать процедуру в skill только потому, что она помогла один раз.
- Не хранить skill-candidate backlog в памяти чата.
- Не передавать subagent весь workspace без compact pack.
- Не считать подготовленный audit pack независимой проверкой.
- Не переносить доменную процедуру в универсальное ядро; переносите только форму workflow, gate или artifact contract.
