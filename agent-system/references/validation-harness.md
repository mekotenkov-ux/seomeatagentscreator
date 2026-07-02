# Validation Harness

Validation belongs in the devkit, not inside runtime.

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
