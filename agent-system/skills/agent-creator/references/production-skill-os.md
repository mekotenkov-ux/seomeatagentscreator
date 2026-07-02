# Production Skill OS

Используйте этот контракт для production, library, governed, team-distributed и public agent packages.

## Maturity modes

- `production` - переиспользуемый агент или skill с IR, routing tests, output evals, package checks и review evidence.
- `library` - shared capability, которую будут подключать разные агенты или команды; нужны registry metadata, ownership, review cadence и drift checks.
- `governed` - high-trust, policy-sensitive, externally distributed или release-critical агент; нужны полные permission gates, waivers, install simulation, evidence ledger и operations loop.
- `scaffold` - только временный внутренний статус. Не публикуйте как финальный статус без явного предупреждения.

## Gate families

1. Intent Canvas.
2. Agent/Skill IR.
3. Trigger Lab.
4. Output Eval Lab.
5. Context Budget.
6. Runtime Matrix.
7. Tool and Permission Gates.
8. Trust Report.
9. Package and Install Simulation.
10. Review Studio.
11. Evidence Ledger and Claim Guard.
12. Operations Loop.

## Anti-overclaim rules

- Planned work is not evidence.
- Self-review is not independent audit.
- Recorded fixtures are not executed evidence.
- Pending human review is not approval.
- Metadata fallback is not native permission enforcement.
- Local install is not portability proof.
- Warning waiver is not blocker waiver.

## Release decision

Каждый gate получает один статус:

- `pass` - требуемые доказательства есть и проходят контракт;
- `warn` - можно продолжать, но риск видим и имеет action, waiver или limitation;
- `block` - нельзя заявлять production/library/governed/public ready, пока не исправлено или явно не descoped.

## Required public-package hygiene

Публичный пакет не должен содержать:

- secrets;
- `.env`;
- credentials;
- cookies;
- private client data;
- raw private logs;
- debug workspaces;
- browser profiles;
- generated temp files;
- local absolute paths;
- domain-specific agents, если пакет заявлен как универсальный.
