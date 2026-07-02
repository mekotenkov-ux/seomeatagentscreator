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

- subagent run id;
- parent workflow run id;
- scenario or role;
- prompt summary;
- allowed context pack;
- status;
- result ref;
- findings;
- confusion points.

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
