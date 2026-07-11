# Context And Quality Gates

## Context Packaging

Default to compact artifacts:

- CSV or TSV for flat inventories;
- JSON for small summaries and configs;
- JSONL for per-row evidence or findings;
- Markdown for human reports that point to stable ids.

Do not pass whole repositories, whole generated folders, raw provider dumps, full browser profiles, or huge nested JSON to checkers by default.

A full raw artifact is allowed only when a compact projection cannot answer the check and the run records `full_artifact_load_reason`.

## Stage Gate Contract

Every production stage needs:

- stage id and owner;
- input universe or reason it is unavailable;
- expected item count;
- processed item count;
- output artifact path;
- status: `pending|done|blocked|partial|descoped|not_applicable`;
- quality verdict: `pass|warn|fail|blocked|not_applicable`;
- skipped/blocked reason when applicable;
- evidence refs;
- next valid actions.

Stage execution is not stage success. A stage is done only when the relevant input universe has been processed or every missing item has a visible disposition.

## Checker Packs

Checker/subagent packs should contain:

- objective and scenario;
- exact files or compact artifacts to inspect;
- frozen criteria;
- tool observations and skip records;
- allowed and forbidden actions;
- expected report schema;
- claim boundary.

Do not include hidden desired verdicts, intended fixes, or broad workspace access.

## Subagent Context Contract

Every writer, explorer, specialist, and checker pack should also declare task id, role, allowed actions, tool allowlist, permission scope, trust labels, snapshot/hash refs, freshness, context budget, write ownership, expected result schema, and full-artifact load reason.

Fresh isolated context is the default. Forked context requires a recorded reason because it loses input isolation and may carry irrelevant or sensitive history. Large outputs stay in the artifact store; the parent receives stable refs and a bounded summary.

## Full-Coverage Rule

Preview limits are not read limits. `top 50`, excerpts, summaries, or sample rows may guide humans, but source-of-truth inventories and final reports must account for every input item when the task claims full coverage.
