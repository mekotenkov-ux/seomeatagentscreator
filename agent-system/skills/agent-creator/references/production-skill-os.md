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
6. Subagent Orchestration And Eval: single-agent baseline, topology, roles, task/result contracts, permissions, isolation, lifecycle, synthesis, provenance and measured delta.
7. Runtime Matrix.
8. Birth And IDE Adaptation: runtime profile, birth plan, environment readiness, project context, first response rule, and native consolidation policy.
9. Tool and Permission Gates.
10. Trust Report.
11. Package and Install Simulation.
12. Review Studio.
13. Evidence Ledger and Claim Guard.
14. Operations Loop.

## Anti-overclaim rules

- Planned work is not evidence.
- Self-review is not independent audit.
- A boolean independent flag is not provenance of an independent run.
- More agents, completed workers, or internal agreement are not evidence of better results without a single-agent comparison.
- Recorded fixtures are not executed evidence.
- Pending human review is not approval.
- Metadata fallback is not native permission enforcement.
- Local install is not portability proof.
- Adapter file presence is not target conformance.
- Birth templates are not first-run evidence until filled by an actual install run.
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

## Source Isolation

Universal agent-creation files must not contain domain package rules, client facts, provider defaults, raw logs, screenshots, browser profiles, or local absolute paths. Durable domain lessons belong in scoped references and must be generalized before they enter the public core.
