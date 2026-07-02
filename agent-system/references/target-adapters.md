# Target Adapters

Target adapters are import/runtime compatibility layers. They are not separate sources of truth.

## Canonical Order

1. Agent/Skill IR defines the semantic contract.
2. Router and skills implement the contract.
3. Adapters map the same contract to target runtimes.
4. Target conformance records parity, degraded behavior, unsupported features, permission mapping, and install scope.

## Adapter Rules

- Keep adapters thin.
- Avoid copying full workflow bodies into every target file.
- Link or route to canonical skills/references when the target runtime can read them.
- Record unsupported native features explicitly.
- Treat metadata-only permissions as residual risk, not native enforcement.
- Ask before merging adapter text into existing native instruction files.

## Required Matrix Fields

For each target:

- `platform`;
- `adapter_paths`;
- `semantic_parity`;
- `unsupported_features`;
- `degraded_behavior`;
- `permission_mapping`;
- `install_scope`;
- `native_consolidation_policy`;
- `verification_status`;
- `evidence_refs`.

Presence of an adapter file is not proof of parity.
