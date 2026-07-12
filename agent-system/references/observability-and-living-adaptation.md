# Observability And Living Adaptation

Agent creation improves when runs leave machine-readable traces.

## Minimal Ledgers

Use JSONL, CSV, SQLite, or another durable store for:

- workflow runs;
- subagent/checker runs;
- tool observations;
- skill candidates;
- method lessons;
- waivers and descopes;
- release evidence.

## Workflow Run Fields

- run id;
- user request;
- route decision: `self|subagents|hybrid`;
- risk level;
- started/finished timestamps;
- status;
- evidence refs;
- notes or blocker.

## Subagent Run Fields

- subagent run id, task id, parent workflow/agent id and delegation plan id;
- topology, role, context mode and context pack ref;
- tool, skill, permission and write-isolation envelope;
- prompt/context hashes without raw private content;
- lifecycle transitions, attempt/retry/cancellation lineage and error class;
- result/artifact/evidence/trace refs;
- runtime, tokens, tool calls, cost and budget remaining;
- findings, disagreements, blockers, confusion points and cleanup status.

## Living Adaptation Decision

At the end of meaningful work, decide whether to update:

- router;
- skill;
- command/workflow;
- checker;
- tool registry;
- validation;
- reference docs;
- local memory;
- no durable file.

Record `no_update_reason` when no change is warranted. Do not turn noise into method.
## Canonical Run Events

Use `run-event.template.json` as the append-only event envelope for parent runs, tools, hooks, subagents, checkers and recovery. Events carry trace/span/parent ids, monotonic sequence, actor/principal, system release and definition hashes, state revision, permission decision, effect status, budget deltas, provenance and artifact refs.

All side-effecting calls must be represented. Unknown outcomes remain `unknown` until reconciliation; a missing event is not a no-op. Raw chain-of-thought is neither required nor exported by default.

## Governed Trace-To-Improvement Loop

A production trace is evidence only after source approval, redaction and expert adjudication. Build a diverse failure coreset, retain success counterexamples and freeze an untouched holdout. Candidate changes run in isolation and cannot edit graders, permissions, logs, budgets, sandbox or final holdout.

Require targeted, regression, safety and holdout results, then independent review, human approval, canary, kill switch and rollback. `living-adaptation-decision.template.json` defaults `automatic_application_allowed` to false. Self-validation and self-preference remain experimental evidence, not release authority.
