---
---

# Frontier Harness: что добавлено по исследованиям 2025-2026

Срез исследований: 11 июля 2026 года. Полная доказательная карта находится в [`agent-system/references/frontier-harness-research-2026-07.md`](../agent-system/references/frontier-harness-research-2026-07.md), рабочий контракт - в [`frontier-harness-engineering.md`](../agent-system/references/frontier-harness-engineering.md).

## Простыми словами

Система проверяет не только ответ агента, но и путь к нему: какие права использованы, что прочитано и изменено, были ли скрытые нарушения, сколько ресурсов потрачено и можно ли воспроизвести прогон.

В основной контур внедрены:

1. **Версия всей системы.** Model snapshot, instructions, tools, permissions, runtime, sandbox и graders получают одну `system_release_id`.
2. **Раздельные failure boundaries.** Session, harness, sandbox, artifact store и credential broker имеют отдельные контракты восстановления и доказательства.
3. **Runtime-enforced authority.** Default deny; approval привязан к principal, operation, resource version, normalized arguments, risk, budget и expiry.
4. **Append-only trajectory.** События фиксируют proposals, permission decisions, effects, inter-agent transfers, state revisions и budget deltas без экспорта raw chain-of-thought.
5. **Проверка самого экзамена.** До score проверяются task inventory, feasibility witnesses, ambiguity, leakage, grader coverage, frozen holdout и независимый defect review.
6. **Stochastic reliability.** Учитываются все попытки, repeated trials, confidence intervals и отдельно infrastructure failures.
7. **Некомпенсируемая безопасность.** Правильный ответ после запрещенного доступа, утечки или unauthorized transfer остается fail.
8. **Assumption Registry.** Каждый scaffold-компонент фиксирует, какую слабость компенсирует, стоимость, owner, review trigger и rollback.
9. **Evidence-backed release.** Финальный `pass` требует реальные файлы, пересчитанные SHA-256, согласованные ID и все 13 обязательных gates.

## Порядок работы

1. Заполните `harness-boundary.template.json`, `permission-policy.template.json` и `external-approval-ledger.template.json`.
2. Пишите реальные события по `run-event.template.json` в append-only JSONL.
3. Проверьте eval через `eval-validity-report.template.json`, затем запустите Output Eval.
4. Заполните Harness Assumption Registry; запускайте Ablation Lab для затронутых assumptions или сохраните доказанное `not_affected`.
5. Разделите runtime/devkit, соберите архивы и выполните install simulation на свежей распаковке.
6. Проведите независимые scenario-аудиты финального пакета.
7. Создайте отдельный gate-evidence report для каждого обязательного gate и добавьте все артефакты в `evidence-bundle-manifest`.
8. Только после этого заполните `release-decision` и запустите строгую проверку из корня development repo:

```bash
python -B scripts/validate_harness_release.py \
  --harness-boundary path/to/harness-boundary.json \
  --permission-policy path/to/permission-policy.json \
  --assumption-registry path/to/harness-assumption-registry.json \
  --ablation-lab path/to/harness-ablation-lab.yaml \
  --eval-validity path/to/eval-validity-report.json \
  --output-eval path/to/output-eval-lab.yaml \
  --run-events path/to/run-events.jsonl \
  --approval-ledger path/to/external-approval-ledger.json \
  --evidence-bundle path/to/evidence-bundle-manifest.json \
  --release-decision path/to/release-decision.json
```

На Windows передайте те же аргументы в PowerShell одной строкой или используйте обратный апостроф для переноса.

## Что проверяется экспериментом

- автоматический Harness Ablation после каждого upgrade;
- context-sufficiency gate для evidence-heavy retrieval workflows;
- automated harness search и active failure discovery;
- dynamic memory/playbook optimization;
- self-critique и self-preference как optimizer signal.

Эти приемы сначала проверяются против matched-budget baseline и hidden holdout. Они не разрешают unattended production self-modification, изменение graders/permissions или обучение на приватных raw traces без отдельного согласия.
