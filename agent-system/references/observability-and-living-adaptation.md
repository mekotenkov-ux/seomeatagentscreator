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
