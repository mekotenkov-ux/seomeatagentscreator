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
3. System Identity And Harness Boundary: versioned model/harness/instructions/tools/permissions/runtime/graders plus separate session, sandbox, artifacts and credential broker.
4. Authority And Information Flow: default deny, approval binding, runtime enforcement, provenance, trusted-control separation and allowed sinks.
5. Run Event And Durable State: append-only trace, state revisions, leases, budget usage, side-effect reconciliation, checkpoint/recovery when applicable.
6. Trigger Lab.
7. Eval Validity: task inventory, feasibility witnesses, requirement-to-grader map, contamination/shortcut checks, frozen holdout and independent defect review.
8. Output And Trajectory Eval: matched baseline, repeated trials, infrastructure calibration, outcome, trajectory, boundary and stability graders.
9. Harness Assumption Registry And Ablation Lab.
10. Context Budget And Provenance; use a sufficiency gate only for evidence-heavy retrieval workflows after local eval.
11. Subagent Orchestration And Eval: single-agent baseline, topology, roles, task/result contracts, permissions, isolation, lifecycle, synthesis, provenance and measured delta.
12. Runtime Matrix.
13. Birth And IDE Adaptation: runtime profile, birth plan, environment readiness, project context, first response rule and native consolidation policy.
14. Tool and Permission Gates.
15. Trust Report And Containment Drills.
16. Package and Install Simulation.
17. Review Studio.
18. Machine Release Decision, Evidence Ledger and Claim Guard.
19. Operations Loop with proposal-only adaptation, canary, kill switch and rollback.
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
- A final answer or passing patch does not prove a safe or coherent trajectory.
- A score from a broken, leaking, contaminated, saturated or infrastructure-unstable benchmark is not release evidence.
- Best-of-N evidence is not a single-attempt reliability claim unless deployment uses the same attempts and selector.
- A vendor case study or single preprint is an experiment, not a universal performance default.
- Self-validation, self-preference and automated harness search are not independent release authority.
- Quality cannot compensate for a critical permission, disclosure or boundary violation.

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
