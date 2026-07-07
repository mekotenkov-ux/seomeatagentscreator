# Repo/Tool Card: withastro/flue

## Identity

- ID: withastro-flue
- Canonical URL: https://github.com/withastro/flue
- Type: agent_framework
- Status: cataloged
- Inspection date: 2026-07-07

## What It Is

TypeScript framework for building autonomous agents and AI workflows with a programmable harness, tools, skills, sandboxes, sessions, deployment targets, and observability hooks.

## Why It May Be Useful

- Useful as a reference architecture for agent harness design: how to combine instructions, typed tools, reusable skills, sandboxed execution, durable sessions, deployment surfaces, subagents, MCP, and observability.

## Agent-Building Use Cases

- Study harness/runtime boundaries for production agents.
- Borrow ideas for typed tool packaging, skills, sandboxes, subagents, and deployment targets.
- Compare with our runtime/devkit, birth, target-conformance, and long-running tool lifecycle layers.

## When To Consider

- When designing a TypeScript agent runtime or harness.
- When comparing patterns for skills, tools, subagents, sandboxes, sessions, channels, MCP, and observability.
- When building deployable agents that need explicit runtime composition.

## When Not To Use

- When the task only needs a prompt/skill package for an existing IDE agent.
- When target runtime is not TypeScript/Node and no harness migration is desired.
- When there is no approval to add framework dependencies or hosted runtime surface.

## Implementation Shape

- Runtime/language: TypeScript, Node.js, Cloudflare Workers, GitHub Actions, GitLab CI/CD, Daytona, Render
- Install/use pattern: Monorepo with @flue/runtime, @flue/cli, @flue/sdk, @flue/opentelemetry, and @flue/postgres packages; candidate for study before any dependency selection.
- Requires permissions: network, package_install, model_provider_keys, sandbox_or_container_execution, external_service_connectors

## License And Maintenance

- License: Apache-2.0
- Maintainer: withastro
- Recent activity: active-looking repository; GitHub page showed 1,053 commits and public issues
- Adoption signal: GitHub page showed 7.1k stars and 410 forks during inspection

## Risks And Unknowns

- Harness integration changes runtime architecture and should be treated as a separate project.
- Sandbox, HTTP exposure, model keys, and connected tools require explicit permission and threat review.
- Do not copy workflow prose or package structure into our runtime without target conformance and validation.

## Alternatives

- LangGraph
- Mastra
- Temporal/Workflows plus LLM tools
- custom lightweight harness

## Evidence Refs

- https://github.com/withastro/flue - README describes Flue as an agent harness framework with tools, skills, sandbox, sessions, deployment targets, MCP, and observability; inspected 2026-07-07.

## Integration Gate

This item is not integrated until a specific project selects it and passes license, security, runtime, validation, and rollback checks.
