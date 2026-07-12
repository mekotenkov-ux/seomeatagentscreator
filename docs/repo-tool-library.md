---
---

# Подборка репозиториев и инструментов

Этот слой нужен для того, чтобы сохранять полезные ссылки на репозитории, библиотеки, SDK, MCP servers, eval tools, SaaS и примеры для будущих агентских систем.

Главное правило: **каталог не равен интеграции**.

Если пользователь дал ссылку, ее нужно описать и положить в каталог. Не нужно сразу добавлять зависимость, переписывать runtime, создавать tool, менять prompt или включать это в текущего агента.

## Что записывать

Для каждой ссылки фиксируйте:

- canonical URL;
- название;
- тип: repo, library, CLI, SDK, SaaS, MCP server, eval tool, dataset, reference, example;
- простое описание;
- зачем может пригодиться при создании агентов;
- для каких workflow или tools подходит;
- когда использовать;
- когда не использовать;
- license;
- maintenance signals;
- risks and permission needs;
- статус;
- дату инспекции;
- ссылки на evidence.

## Статусы

- `raw_link` - ссылка сохранена, но не изучена.
- `cataloged` - есть базовое описание.
- `evaluated` - проверены license, maturity, risks, use cases.
- `approved_candidate` - можно рассматривать в будущих проектах.
- `selected_for_project` - пользователь явно выбрал для конкретной задачи.
- `integrated` - реально встроено после отдельной реализации и проверки.
- `rejected` - не подходит.

## Где хранить

Живая подборка хранится в:

```text
agent-system/catalog/repo-tool-library.json
agent-system/catalog/repo-tool-cards/
```

Используйте шаблоны:

```text
agent-system/templates/repo-tool-library.template.json
agent-system/templates/repo-tool-card.template.md
agent-system/templates/repo-tool-intake.template.md
```

## Когда доставать из каталога

Каталог полезен во время workflow discovery, проектирования IR, tool registry, eval/checker слоя, package/export слоя и при поиске готовых идей под конкретную задачу.

Но даже если item выглядит подходящим, сначала предложите его как вариант, объясните риски и стоимость интеграции, получите approval, затем делайте отдельную implementation задачу с проверками.