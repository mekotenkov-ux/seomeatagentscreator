# Final Evidence And Claim Guard

A package can be locally validated without being externally proven. Keep these claims separate.

## Evidence Statuses

- `local_pass` - local runtime/devkit/fixture/package checks pass.
- `external_pending` - proof requires approval, credentials, budget, live data, reviewers, or another external condition.
- `external_pass` - approved external run or independent review completed and produced bounded artifacts.
- `descoped` - user accepted that an evidence item is out of scope, with reason and date.
- `ready_with_descopes` - release may proceed with explicit limitations, but not as full external proof.

## Not Evidence

- planned work;
- self-review;
- pending human review;
- fixture existence;
- template file copied during setup;
- markdown report without machine-readable backing;
- metadata fallback for permissions;
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
