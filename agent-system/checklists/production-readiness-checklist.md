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

## Claims

- [ ] Planned work не считается evidence.
- [ ] Self-review не считается independent audit.
- [ ] Metadata fallback не считается native enforcement.
- [ ] Pending review не считается approval.
- [ ] Warnings имеют action/waiver/limitation.
- [ ] Blockers не waived.
