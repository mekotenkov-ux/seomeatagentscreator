# Repo/Tool Card: obra/superpowers

## Identity

- ID: obra-superpowers
- Canonical URL: https://github.com/obra/superpowers
- Type: skill_library
- Status: cataloged
- Inspection date: 2026-07-12
- License: MIT

## What It Is

`obra/superpowers` is a cross-IDE methodology and composable skill library for coding agents. Its documented path goes from discovery and design approval to a detailed plan, isolated worktree, task execution, TDD, review, debugging, verification, and branch completion.

## Why It May Be Useful

The meta-agent may use it as an optional external process reference when it creates a software-producing agent or skill. It is useful when the resulting workflow needs stronger planning, test discipline, review checkpoints, or isolated parallel work.

It is not part of this repository's runtime and is not automatically installed, copied, or inherited by a created agent.

## Agent-Building Use Cases

- Compare its brainstorming and plan-approval sequence with the project's own `grill-me` and workflow discovery.
- Consider its worktree, subagent review, TDD, debugging, and verification patterns for a concrete software-agent project.
- Study how the project packages the same methodology across several coding-agent environments.

## When To Consider

- The user is creating a coding agent, engineering workflow, or development skill.
- The user needs explicit planning, TDD, review, debugging, or branch/worktree discipline.
- A meta-agent needs an optional process aid, rather than a dependency in the final generated runtime.

## When Not To Use

- The agent is not intended to produce software and the extra methodology would be overhead.
- The target IDE must not receive a third-party plugin, session hook, or instruction layer.
- The user has not selected it after seeing the process, permission, and privacy implications.

## Selection Rule For The Meta-Agent

Before architecture starts, the meta-agent must evaluate this catalog candidate and record one of: `not_relevant`, `consider`, `selected_by_user`, or `declined_by_user`.

It asks the user only when selection would materially change the workflow, add a plugin/dependency/hook, alter permissions or telemetry settings, or become part of the generated package. A `cataloged` item never becomes an installed component by implication.

## Risks And Unknowns

- The methodology is opinionated and may conflict with the user's established process.
- Platform-specific installation can add plugin instructions and session-start hooks.
- The repository documents an optional visual-companion telemetry feature; review the current version and opt-out controls before installation where relevant.
- Repository popularity is not proof of fit, security, or quality for a target project.

## Evidence Ref

- https://github.com/obra/superpowers - primary README and repository metadata inspected 2026-07-12.

## Integration Gate

Use is a separate project decision. Before installation or reuse, explain what changes, obtain explicit user selection, review license and privacy/telemetry implications, check target compatibility, and validate the result. Do not add it to a created agent by default.