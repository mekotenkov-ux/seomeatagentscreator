---
name: repo-tool-librarian
description: Используйте, когда пользователь дает ссылки на репозитории, библиотеки, инструменты, статьи, SDK, SaaS или примеры, которые нужно сохранить в каталог идей для будущего создания агентов. По умолчанию только индексируйте и описывайте, не встраивайте в runtime, зависимости, tools, prompts или workflows без отдельного явного запроса.
---

# Repo Tool Librarian

Задача - сохранять полезные репозитории и инструменты как knowledge inventory для будущих агентских систем.

Это не integration skill. Каталог помогает потом находить готовые repo/tool ideas, но не добавляет их в текущего агента автоматически.

## Core Rule

Cataloging is not adoption.

A saved link is only a candidate. Do not install packages, add dependencies, copy code, change runtime instructions, create tools, enable connectors, or alter workflows unless the user explicitly asks to integrate a specific item into a specific project.

## When User Provides Links

For each link:

1. Identify the canonical source URL.
2. Inspect the primary source when network/access is available.
3. Record what the repo/tool is for in plain language.
4. Record which agent-building problems it may help with.
5. Record when to consider it and when not to use it.
6. Record license, maturity, maintenance signals, installation shape, security/privacy risks, and unknowns.
7. Assign catalog status.
8. Save the entry to the repo/tool library artifacts.

If the source cannot be inspected, create a `pending_inspection` entry instead of inventing facts.

## Status Pipeline

Use explicit status values:

- `raw_link` - user provided a link, not inspected yet.
- `cataloged` - basic description and source metadata saved.
- `evaluated` - license, risks, maturity, use cases, and limitations reviewed.
- `approved_candidate` - safe enough to consider in future projects.
- `selected_for_project` - explicitly chosen for a specific agent/project.
- `integrated` - actually added to runtime/tooling after explicit implementation request and validation.
- `rejected` - not useful, unsafe, incompatible, abandoned, or out of scope.

Only `selected_for_project` and `integrated` require a concrete project and user approval.

## Required Fields

Every catalog entry should capture:

- id;
- canonical URL;
- name;
- type: repo, library, CLI, SDK, SaaS, MCP server, agent framework, eval tool, reference, dataset, example;
- short description;
- why it may be useful;
- agent-building use cases;
- tags;
- language/runtime;
- license;
- maintenance signals;
- install/use shape;
- risks and permission needs;
- when to consider;
- when not to use;
- comparable alternatives;
- source evidence refs;
- inspection date;
- status;
- next review action.

## Use During Agent Creation

During `workflow-loop-me`, architecture, tool design, eval design, or packaging, consult the catalog only as an idea source.

If a catalog item looks relevant:

1. Propose it as an option with reason.
2. Explain risks, integration cost, and validation needed.
3. Ask before selecting it for the project.
4. Treat integration as a separate implementation task with tests and rollback plan.

## Forbidden Behavior

- Do not install or import a catalog item during indexing.
- Do not copy code into the public repo during indexing.
- Do not add catalog items to runtime dependencies during indexing.
- Do not present `cataloged` as `approved`.
- Do not use stars, README claims, or marketing copy as proof of quality.
- Do not scan private repos or paid docs without explicit access approval.
- Do not save secrets, tokens, private client data, or raw private logs in the catalog.

## Outputs

Recommended artifacts:

- `repo-tool-library.json` - machine-readable catalog.
- `repo-tool-cards/<item-id>.md` - human-readable note per item.
- `repo-tool-intake.md` - batch intake notes for links supplied in one turn.

## Done Condition

Indexing is done only when every provided link is either cataloged, pending inspection, rejected with reason, or blocked with a visible access/permission issue.