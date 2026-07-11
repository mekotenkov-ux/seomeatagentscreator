# Validation Harness

Validation belongs in the devkit, not inside runtime.

## Subagent validation

Public package verification checks template integrity and safe defaults. It is not proof of a live subagent run. For a filled run, execute `scripts/validate_subagent_run.py` to validate topology, roles, task/result/ledger reconciliation, provenance, effective permissions, process and credential isolation, budgets, lifecycle states, retries, cancellation, done invariants and final merged artifacts. Subagent Eval Lab must still provide measured delta against a single-agent baseline.

## Required Checks

- required runtime files exist;
- required devkit files exist;
- JSON/YAML/Markdown frontmatter parse;
- Python or script syntax checks are bytecode-free;
- tool registry schema passes;
- Agent/Skill IR schema passes;
- target conformance matrix exists for declared targets;
- Trigger Lab and Output Eval Lab exist;
- final evidence contract and claim boundary exist;
- independent review summary is present or explicitly blocked;
- runtime/devkit boundary is clean;
- secret and local path scan passes;
- `__pycache__`, `.pyc`, caches, browser profiles, generated workspaces are absent from runtime;
- zip entries use `/` separators;
- required dot-directories are present;
- install simulation runs from the final zip;
- `FILES.sha256` or file inventory is regenerated after cleanup when used.

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
- local absolute paths in manifests.

Fixtures prove the validator catches failures. They do not prove live external evidence.
