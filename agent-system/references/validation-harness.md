# Validation Harness

Validation belongs in the devkit, not inside runtime.

## Subagent validation

Public package verification checks template integrity and safe defaults. It is not proof of a live subagent run. For a filled run, execute `scripts/validate_subagent_run.py` to validate topology, roles, task/result/ledger reconciliation, provenance, effective permissions, process and credential isolation, budgets, lifecycle states, retries, cancellation, done invariants and final merged artifacts. Subagent Eval Lab must still provide measured delta against a single-agent baseline.

## Frontier harness release validation

Template integrity is not release evidence. For a filled production/library/governed release, execute `scripts/validate_harness_release.py` with harness boundary, permission policy, approval ledger, assumption registry, ablation lab, eval validity, Output Eval Lab, append-only run events, SHA-256 evidence bundle and machine release decision. The validator resolves real files, recomputes hashes, reconciles identities and counts, checks permission/effect lifecycle and requires all 13 gates including package, install and independent review. `warn`, `pending` and `not_applicable` cannot become a final production pass.

## Required Checks

- required runtime files exist;
- required devkit files exist;
- JSON/YAML/Markdown frontmatter parse;
- Python or script syntax checks are bytecode-free;
- tool registry schema passes;
- Agent/Skill IR schema passes;
- target conformance matrix exists for declared targets;
- Trigger Lab and Output Eval Lab exist;
- system-under-test identity pins model, harness, instructions, tools, permissions, runtime, dependencies and graders;
- harness boundary separates session, harness, sandbox, artifact store and credential broker;
- permission policy is default deny and approval bindings are runtime enforced;
- run-event coverage includes side effects, permissions, transfers and state deltas;
- eval validity reconciles every task and proves reference/feasibility, grader mapping and hidden holdout;
- repeated trials, A/A infrastructure noise and all-attempt reporting match deployment semantics;
- outcome, trajectory, boundary and stability graders are present;
- active harness assumptions have current matched-budget ablation evidence;
- machine release decision derives allowed claims from resolved gate evidence and recomputed SHA-256;
- final evidence contract and claim boundary exist;
- independent review summary is present or explicitly blocked;
- runtime/devkit boundary is clean;
- secret and local path scan passes;
- `__pycache__`, `.pyc`, caches, browser profiles, generated workspaces are absent from runtime;
- zip entries use `/` separators;
- required dot-directories are present;
- install simulation runs from a fresh extraction of the final zip and emits release-bound evidence;
- `FILES.sha256` is regenerated after cleanup and exactly matches every runtime file except itself.

## Negative Fixtures

Keep guard fixtures in devkit for:

- missing approval ledger;
- broken evidence refs;
- markdown-only review;
- placeholder reviewer fields;
- descope counted as external pass;
- direct skill expanding scope silently;
- no-network behavior claimed as live run;
- runtime containing tests/source materials/chat prompts;
- local absolute paths in manifests;
- correct answer after hidden boundary violation;
- broken or leaking eval task counted as model failure;
- infrastructure drift counted as model gain;
- best-of-N evidence used for single-attempt deployment;
- stale harness assumption after model/runtime change;
- credentials entering sandbox or project hooks before trust;
- self-update that can see holdout or modify graders/policy;
- public claim without machine release decision.

Fixtures prove the validator catches failures. They do not prove live external evidence.
