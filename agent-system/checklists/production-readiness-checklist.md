# Production Readiness Checklist

## Core

- [ ] Objective понятен.
- [ ] Target users определены.
- [ ] Maturity mode выбран.
- [ ] Scope in/out/deferred записан.
- [ ] Autonomy level записан.
- [ ] Risk level записан.
- [ ] Allowed/forbidden actions записаны.
- [ ] Done condition внешний и проверяемый.

## Workflow Discovery

- [ ] `workflow-loop-me` run or blocker recorded.
- [ ] Candidate loops listed before architecture.
- [ ] First workflow selected or rejected with reason.
- [ ] Workflow spec has trigger, inputs, actors, tools, state, artifacts, checkpoints, failure modes, validation, budgets, and done signal.
- [ ] Implementer agent could build from the workflow spec without guessing, or blocking questions are explicit.

## Architecture

- [ ] Agent/Skill IR создан до адаптеров.
- [ ] Router короткий и не содержит все процедуры.
- [ ] Skills сфокусированы.
- [ ] Commands/workflows отделены от skills, если нужен явный full run.
- [ ] Tool registry есть.
- [ ] Permission matrix есть.
- [ ] State/memory вне истории чата.
- [ ] Workspace hygiene определен.

## Validation

- [ ] Trigger Lab есть.
- [ ] Output Eval Lab есть.
- [ ] Checker layer есть.
- [ ] Context packaging policy есть.
- [ ] Release review есть.
- [ ] Evidence ledger/claim guard есть.
- [ ] Package verification есть.
- [ ] Install simulation есть или blocker записан.

## Birth And IDE Adaptation

- [ ] Birth contract создан до адаптеров.
- [ ] `runtime-profile.json` шаблон определяет active runtime, confidence, entrypoints и cleanup_allowed.
- [ ] `birth-plan.json` шаблон описывает keep/move/ask/skip/blocked actions.
- [ ] `environment-readiness.json` шаблон проверяет runtime commands, writable paths, env templates, connectors и permission gates.
- [ ] `project-context.json` шаблон отделяет user inputs, normalized fields, sources, assumptions, missing evidence и next actions.
- [ ] Bare greeting ведет к mission-specific intake, а не к меню упаковки агента.
- [ ] Conflicting IDE/runtime markers блокируют cleanup до уточнения.
- [ ] Native consolidation asks before merge/convert.
- [ ] Target conformance включает first-run setup command, native support и inactive adapter cleanup.

## Claims

- [ ] Planned work не считается evidence.
- [ ] Self-review не считается independent audit.
- [ ] Metadata fallback не считается native enforcement.
- [ ] Pending review не считается approval.
- [ ] Warnings имеют action/waiver/limitation.
- [ ] Blockers не waived.

## Living And Packaging

- [ ] Skill candidates не считаются implemented skills без promotion gate.
- [ ] Independent review summary machine-readable или blocker записан.
- [ ] Runtime install проверяется из финального zip.
- [ ] Birth flow отделяет environment adaptation от project adaptation.
- [ ] Birth gate проверяет runtime profile, birth plan, environment readiness, project context и mission-specific next action.
- [ ] Post-birth cleanup не удаляет canonical runtime assets без approval.
