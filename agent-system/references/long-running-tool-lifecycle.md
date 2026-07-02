# Long-Running Tool Lifecycle

Use this for package audits, export builds, eval batches, crawls, provider calls, or any run that may outlive one model turn.

## Required Controls

- run id and stage id;
- per-item queue with `pending|started|success|error|skipped|cancelled`;
- heartbeat timestamp;
- progress summary file;
- append-only progress log;
- raw sidecar directory when raw evidence exists;
- resume policy;
- duplicate-run guard;
- soft cancel signal;
- status command;
- bounded observations.

## Stop Conditions

Stop when:

- objective gate passes;
- budget is exhausted;
- credentials or approval are missing;
- user changes scope;
- repeated blocker occurs;
- cancel signal is present;
- checker failure repeats beyond repair budget.

## Observations

Every run, skip, timeout, resume, or cancel produces a structured observation:

```json
{
  "status": "success|blocked|timeout|cancelled|error|skipped",
  "summary": "",
  "items": [],
  "evidence_refs": [],
  "next_valid_actions": []
}
```

Long-running tools must not rely on the agent remembering what happened.
