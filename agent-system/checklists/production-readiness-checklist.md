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

## Repo And Tool Library

- [ ] External repo/tool links are cataloged, not integrated by default.
- [ ] Catalog status separates `cataloged`, `evaluated`, `approved_candidate`, `selected_for_project`, and `integrated`.
- [ ] No dependency, tool, connector, prompt, or workflow was added from the library without explicit project approval.
- [ ] License, security, maintenance, and runtime compatibility are checked before integration.

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

## Harness Boundary And Authority

- [ ] Полная system identity фиксирует model, harness, instructions, tools, permissions, runtime, dependencies и graders.
- [ ] Session log, harness, sandbox и artifact store имеют отдельные интерфейсы и failure domains.
- [ ] State переживает loss ephemeral compute; crash recovery или explicit not-applicable reason проверены.
- [ ] Permission policy default-deny и исполняется runtime, а не prompt.
- [ ] Approvals связаны с principal, exact action, normalized arguments, resource version, risk, budget и expiry.
- [ ] Credentials не входят в sandbox; scoped broker/proxy, revoke и cleanup проверены.
- [ ] External content, project config, tool results, subagent outputs и memory имеют provenance/trust labels.
- [ ] Project-local config/hooks не исполняются до trust decision; symlinks разрешаются до path check.
- [ ] Append-only run events покрывают все side-effecting calls, permission decisions, transfers и state deltas.
## Subagent Orchestration

- [ ] Single-agent baseline создан до multi-agent claim.
- [ ] Topology выбрана по decomposability, dependencies, tool density, context value и write overlap.
- [ ] Role registry определяет should/should-not use, tools, skills, model policy, permissions и output schema.
- [ ] Delegation plan содержит task graph, ownership, budgets, join и partial-failure policy.
- [ ] Каждый worker получает bounded task contract и compact context pack.
- [ ] Default depth = 1; fan-out, concurrency, tokens, cost, runtime и retries ограничены.
- [ ] Parallel writes используют disjoint scopes и worktrees/containers; shared mutable checkout запрещен.
- [ ] Background approval behavior и permission inheritance проверены на target runtime.
- [ ] Result schema, task count reconciliation, cancellation propagation и completed-worker cleanup проверены.
- [ ] Independent reviewer имеет provenance и не получает intended verdict.
- [ ] Subagent Eval Lab показывает полезный delta или ограничивает multi-agent конкретными task classes.

## Validation

- [ ] Trigger Lab есть.
- [ ] Output Eval Lab есть.
- [ ] Checker layer есть.
- [ ] Context packaging policy есть.
- [ ] Release review есть.
- [ ] Evidence ledger/claim guard есть.
- [ ] Package verification есть.
- [ ] Install simulation есть или blocker записан.

## Eval Validity And Harness Evolution

- [ ] Eval validity report имеет полный task inventory и reconciled dispositions.
- [ ] У задач есть reference solution/feasibility witness и requirement-to-grader map.
- [ ] Frozen holdout скрыт от optimizer; contamination, shortcuts, leakage и ambiguity проверены.
- [ ] Baseline и candidate используют matched budgets, infrastructure и task distribution.
- [ ] Stochastic workflows имеют repeated trials, clean resets, confidence intervals и all-attempt reporting.
- [ ] Outcome, trajectory, boundary и stability graders покрыты отдельно.
- [ ] Correct answer после hidden boundary violation всегда считается fail.
- [ ] Infrastructure errors и A/A noise отделены от model/task failures.
- [ ] LLM judge откалиброван и не является sole safety authority.
- [ ] Harness Assumption Registry заполнен; model/runtime/tool changes запускают ablation.
- [ ] Machine-readable release decision reconciles every required gate and derives allowed claims.
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
- [ ] Production traces используются только из approved redacted source path.
- [ ] Living adaptation остается proposal-only до targeted, regression, safety и hidden-holdout gates.
- [ ] Optimizer не может менять graders, permissions, logs, budgets, sandbox или final holdout.
- [ ] Canary, kill switch, rollback и human approval доказаны до durable update.
- [ ] Independent review summary machine-readable или blocker записан.
- [ ] Runtime install проверяется из финального zip.
- [ ] Birth flow отделяет environment adaptation от project adaptation.
- [ ] Birth gate проверяет runtime profile, birth plan, environment readiness, project context и mission-specific next action.
- [ ] Post-birth cleanup не удаляет canonical runtime assets без approval.
