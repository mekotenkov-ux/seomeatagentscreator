# References

Эти файлы описывают универсальные механики создания agent packages. Они не являются доменной методикой и не должны содержать клиентские данные, логи отладки или правила конкретного SEO/GEO/YouTube агента.

Используйте их как слой между коротким router и конкретными templates:

- `skill-training-lab.md` - как выращивать скиллы из реальных прогонов.
- `package-boundary.md` - как разделять runtime и devkit.
- `birth-protocol.md` - как устанавливать пакет и не превращать импорт в миссию агента.
- `context-and-quality-gates.md` - как строить compact context packs и stage gates.
- `target-adapters.md` - как проверять Codex, Claude, Cursor, OpenCode и другие adapters против одного IR.
- `final-evidence-and-claim-guard.md` - как отделять доказанные claims от planned work.
- `long-running-tool-lifecycle.md` - как проектировать возобновляемые долгие tool runs.
- `universal-core-isolation.md` - как не заносить доменные уроки и клиентские факты в универсальное ядро.
- `observability-and-living-adaptation.md` - как вести workflow/subagent/lesson/skill-candidate ledger.
- `validation-harness.md` - что должен проверять devkit перед упаковкой.
