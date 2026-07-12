# Repo And Tool Library

Use this reference to maintain a reusable catalog of external repositories, tools, libraries, SDKs, MCP servers, SaaS products, eval tools, datasets, and examples.

## Principle

A catalog item is an idea source, not a dependency.

Saving a link must not change the current agent, runtime package, dependency list, tool registry, prompts, adapters, workflows, or docs that claim active support.

## Why This Exists

Agent builders repeatedly need the same kinds of building blocks:

- agent frameworks;
- MCP servers;
- eval and benchmark tools;
- browser or scraping tools;
- document parsers;
- observability tools;
- workflow automation examples;
- prompt/skill examples;
- packaging and release tools.

The library keeps those links searchable and described so a future agent-building task can reuse ideas without re-discovering everything from scratch.

## Status Pipeline

- `raw_link`: saved but not inspected.
- `cataloged`: basic metadata and description saved.
- `evaluated`: license, maturity, maintenance, risks, use cases, and limitations reviewed.
- `approved_candidate`: acceptable to consider in future projects.
- `selected_for_project`: explicitly chosen for a specific build.
- `integrated`: added to a runtime or toolchain after explicit implementation and validation.
- `rejected`: not useful, unsafe, incompatible, abandoned, or out of scope.

Default status after user sends a link is `raw_link` or `cataloged`, never `integrated`.

## Catalog Rules

- Prefer primary sources: repo README, docs, releases, license, package metadata.
- Record unknowns instead of guessing.
- Record inspection date; repo health changes over time.
- Separate what the project claims from what was verified.
- Keep private data and credentials out of the catalog.
- Do not store full raw docs when a short summary and source URL are enough.
- Do not catalog a private repo unless the user explicitly provides access and says it can be indexed.

## When To Consult The Library

Consult the library during:

- workflow discovery;
- Agent/Skill IR creation;
- tool registry design;
- eval/checker design;
- package/export design;
- troubleshooting a known implementation gap.

The catalog can suggest options, but selection and integration are separate approval-gated tasks.

## Mandatory Candidate Check Before Agent Creation

Before architecture starts, the meta-agent records a deliberate decision for `obra/superpowers` from the catalog: `not_relevant`, `consider`, `selected_by_user`, or `declined_by_user`. The purpose is to consider a reusable engineering methodology for the meta-agent itself, not to force it into every created agent.

Ask the user only when using it would materially change the workflow, install a plugin, add a dependency or hook, alter permissions or telemetry, or change the generated package. A catalog entry never authorizes installation, code copying, or runtime integration.
## Integration Gate

Before using a catalog item in a real agent package, require:

- concrete project need;
- explicit user selection or approval;
- license compatibility check;
- security/privacy risk review;
- dependency and maintenance check;
- target runtime compatibility check;
- validation plan;
- rollback or removal plan.

Do not let `approved_candidate` bypass these gates.