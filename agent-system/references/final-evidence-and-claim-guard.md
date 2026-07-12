# Final Evidence And Claim Guard

A package can be locally validated without being externally proven. Keep these claims separate.

## Evidence Statuses

- `local_pass` - local runtime/devkit/fixture/package checks pass.
- `external_pending` - proof requires approval, credentials, budget, live data, reviewers, or another external condition.
- `external_pass` - approved external run or independent review completed and produced bounded artifacts.
- `descoped` - user accepted that an evidence item is out of scope, with reason and date; keep it outside `accepted_evidence`.
- `ready_with_descopes` - release may proceed with explicit limitations, but not as full external proof.

## Not Evidence

- planned work;
- self-review;
- pending human review;
- fixture existence;
- template file copied during setup;
- markdown report without machine-readable backing;
- metadata fallback for permissions;
- passing final output without a safe trajectory;
- score from an unvalidated or infrastructure-unstable benchmark;
- best-of-N result when deployment is single-attempt;
- self-optimized harness selected by its own sole judge;
- descope decision.

## Required Claim Boundary

Every release review should list:

- accepted evidence;
- pending evidence;
- lower-assurance assumptions;
- skipped tools or stages;
- blocked permissions or credentials;
- descoped items;
- forbidden claims until external pass.

Do not let final text overrule deterministic gate failures.

## Machine Release Decision

Сначала соберите финальные runtime/devkit archives, выполните install simulation на fresh extraction и независимые scenario-аудиты. Затем `evidence-bundle-manifest.template.json` связывает каждый artifact id с confined relative path, release id и пересчитанным SHA-256.

`release-decision.template.json` обязан перечислить ровно 13 production/library/governed gates. Строгий финальный validator принимает только `pass`: `warn`, `not_applicable`, `pending`, `block`, missing/duplicate gate, unresolved ref, hash mismatch, expired approval или critical boundary violation не входят в accepted evidence. Allowed claim должен ссылаться на прошедшие gate ids и присутствовать в claim boundary evidence bundle.

Quality and utility do not compensate for unauthorized access, disclosure, unapproved irreversible action or other predefined P0 safety violation. Human Markdown review is a presentation surface; the machine decision is the consistency gate.
