# Seomeat Agents Creator

Универсальная система для проектирования, отладки, упаковки и публикации агентских систем и скиллов.

Этот репозиторий не является набором доменных агентов. В нем нет SEO/GEO/YouTube/research-пакетов, отладочных прогонов, приватных логов, `dev/work/`, экспортных архивов и конкретных клиентских материалов. Здесь лежит только повторяемый процесс создания агентов: как определить контракт, собрать скиллы, описать инструменты, проверить поведение, подготовить runtime/devkit и безопасно экспортировать пакет.

## Для кого

- Для разработчиков, которые делают агентов не как один большой промпт, а как проверяемую систему.
- Для команд, которым нужны воспроизводимые скиллы, checkers, tools, evals и installable runtime.
- Для авторов образовательных и прикладных AI-процессов, которым важно не смешивать универсальную методику с доменными пакетами.

## Связь с SEOMeat

Подход вырос из практики школы и прикладных проектов SEOMeat. Больше о школе и SEO-подходе: [seomeat.ru](https://seomeat.ru/).

## Главный принцип

Модель предлагает действия. Runtime, инструменты, проверки, разрешения, логи и артефакты доказывают, что действие допустимо и результат действительно готов.

Не полагайтесь на "модель сама аккуратно сделает". Для production-grade агента нужны:

- Agent/Skill IR;
- router и focused skills;
- typed tool registry;
- permission matrix;
- state/memory вне истории чата;
- context packaging;
- trigger lab;
- output eval lab;
- checker/reviewer layer;
- release review;
- runtime/devkit boundary;
- package verification;
- install simulation;
- public claim guard.

## Быстрый старт

1. Скопируйте `agent-system/` в новый репозиторий или проект, где будете проектировать агента.
2. Откройте `agent-system/AGENTS.md` как корневую инструкцию для агента-создателя.
3. Запустите preflight по `agent-system/skills/grill-me/SKILL.md`.
4. Заполните `agent-system/templates/agent-ir.template.json`.
5. Соберите первый vertical slice: router, один workflow, один skill, один tool path, один checker, один eval set.
6. Проверьте Trigger Lab и Output Eval Lab.
7. Разделите runtime и devkit.
8. Соберите clean staging и только после этого делайте zip/public repo.

Подробно: [docs/quick-start.md](docs/quick-start.md).

## Рекомендация по качественной отладке

Для качественной отладки рекомендуется создавать отдельный проект под конкретного агента, подключать туда создаваемого агента и из отдельного чата выполнять реальную работу. Тогда агент-создатель видит полный лог, наблюдает, где целевой агент путается, и может чинить систему по фактическому trace, а не по пересказу.

Практический паттерн:

1. `agent-dev/` - репозиторий, где вы проектируете agent package.
2. `agent-sandbox/` - отдельный проект, куда вы устанавливаете runtime как fresh user.
3. `debug-chat` - отдельный чат, который работает как целевой агент в sandbox.
4. `creator-chat` - чат агента-создателя, который читает артефакты, логи и checker reports из sandbox и чинит исходный пакет.

## Что не включать в публичный агентский пакет

- `.env`, ключи, токены, cookies, реальные credentials;
- `dev/work/`, временные отладочные папки, browser profiles;
- доменные агенты и конкретные клиентские материалы;
- regression fixtures внутри runtime;
- source prompts, legacy drafts, финальные отчеты переделок;
- zip-архивы предыдущих сборок;
- локальные абсолютные пути;
- скрытую зависимость от текущего чата.

## Структура

```text
agent-system/
  AGENTS.md
  skills/
    agent-creator/
      SKILL.md
      references/production-skill-os.md
    grill-me/
      SKILL.md
  templates/
    agent-ir.template.json
    tool-registry.template.json
    runtime-manifest.template.json
    release-review.template.md
    trigger-lab.template.yaml
    output-eval-lab.template.yaml
  checklists/
    export-clean-checklist.md
    production-readiness-checklist.md
docs/
  index.html
  quick-start.md
  architecture.md
  unpack-and-use.md
  debugging.md
  packaging.md
```

## Лицензия

MIT. См. [LICENSE](LICENSE).
