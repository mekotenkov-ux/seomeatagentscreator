from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "MANIFEST.json",
    "AGENTS.md",
    "agent-system/AGENTS.md",
    "agent-system/skills/agent-creator/SKILL.md",
    "agent-system/skills/agent-creator/references/production-skill-os.md",
    "agent-system/skills/grill-me/SKILL.md",
    "agent-system/references/README.md",
    "agent-system/references/skill-training-lab.md",
    "agent-system/references/package-boundary.md",
    "agent-system/references/birth-protocol.md",
    "agent-system/references/ide-runtime-adaptation.md",
    "agent-system/references/context-and-quality-gates.md",
    "agent-system/references/target-adapters.md",
    "agent-system/references/final-evidence-and-claim-guard.md",
    "agent-system/references/long-running-tool-lifecycle.md",
    "agent-system/references/universal-core-isolation.md",
    "agent-system/references/observability-and-living-adaptation.md",
    "agent-system/references/validation-harness.md",
    "agent-system/templates/agent-ir.template.json",
    "agent-system/templates/agent-birth-contract.template.json",
    "agent-system/templates/runtime-profile.template.json",
    "agent-system/templates/birth-plan.template.json",
    "agent-system/templates/environment-readiness.template.json",
    "agent-system/templates/project-context.template.json",
    "agent-system/templates/birth-validation-gates.template.json",
    "agent-system/templates/tool-registry.template.json",
    "agent-system/templates/runtime-manifest.template.json",
    "agent-system/templates/release-review.template.md",
    "agent-system/templates/trigger-lab.template.yaml",
    "agent-system/templates/output-eval-lab.template.yaml",
    "agent-system/templates/state.template.md",
    "agent-system/templates/local-memory.template.md",
    "agent-system/templates/skill-candidate-registry.template.csv",
    "agent-system/templates/living-adaptation-decision.template.json",
    "agent-system/templates/target-conformance.template.json",
    "agent-system/templates/final-evidence-contract.template.json",
    "agent-system/templates/final-evidence-runbook.template.md",
    "agent-system/templates/independent-review-summary.template.json",
    "agent-system/templates/external-approval-ledger.template.json",
    "agent-system/templates/stage-quality-gates.template.json",
    "agent-system/templates/evidence-ledger.template.json",
    "agent-system/templates/export-manifest.template.json",
    "agent-system/templates/install-birth.template.md",
    "agent-system/templates/checker-context-pack.template.json",
    "agent-system/templates/checker-report.template.json",
    "agent-system/templates/loop-state.template.json",
    "agent-system/templates/validation-run-matrix.template.yaml",
    "agent-system/templates/evidence-bundle-manifest.template.json",
    "agent-system/checklists/export-clean-checklist.md",
    "agent-system/checklists/production-readiness-checklist.md",
    "scripts/build_agent_export.py",
    "scripts/validate_runtime_install.py",
    "scripts/check_core_isolation.py",
    "docs/index.html",
    "docs/quick-start.md",
    "docs/architecture.md",
    "docs/birth.md",
    "docs/debugging.md",
    "docs/packaging.md",
]

FORBIDDEN_PARTS = {
    "__pycache__",
    "node_modules",
    "chrome-qfo-profile",
    "chrome-profile",
    "browser-profile",
    "agent-workspace",
    "validation-runs",
    "validation-tests",
    "test-scenarios",
    "source-materials",
    "eval-scripts",
    "export-staging",
    "chat-prompts",
    "ide-versions",
    "handoff",
    "_incoming",
    "для отладки",
}

FORBIDDEN_SUFFIXES = {
    ".zip",
    ".7z",
    ".tar",
    ".gz",
    ".sqlite",
    ".db",
    ".pyc",
    ".pyo",
}

TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".html", ".py", ".txt", ".csv"}

FORBIDDEN_TEXT = [
    "C:" + "\\Users\\",
    "C:" + "/Users/",
    "BLACK" + "WHITE",
    "Copy" + "KillerDev",
]

MOJIBAKE_MARKERS = ["Рџ", "Рћ", "РЅ", "Р°", "Ð", "Ñ"]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def parse_json(path: Path, rel: str) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {rel}: {exc}")


def parse_python(path: Path, rel: str) -> None:
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=rel)
    except SyntaxError as exc:
        fail(f"invalid Python syntax in {rel}: {exc}")


def main() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"required file missing: {rel}")

    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("license") != "MIT":
        fail("manifest license must be MIT")
    if manifest.get("language") != "ru":
        fail("manifest language must be ru")

    page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    if "https://seomeat.ru/" not in page:
        fail("docs/index.html must link to https://seomeat.ru/")
    for public_term in ["Skill Training Lab", "target conformance", "final evidence", "birth protocol"]:
        if public_term not in page:
            fail(f"docs/index.html must mention {public_term}")

    for path in ROOT.rglob("*"):
        rel_path = path.relative_to(ROOT)
        rel = rel_path.as_posix()
        parts = set(rel_path.parts)
        if parts & FORBIDDEN_PARTS:
            fail(f"forbidden path present: {rel}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"forbidden file suffix present: {rel}")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_TEXT:
                if pattern in text:
                    fail(f"forbidden local text {pattern!r} in {rel}")
            if rel.startswith(("README.md", "docs/", "agent-system/")):
                hits = [marker for marker in MOJIBAKE_MARKERS if marker in text]
                if hits:
                    fail(f"possible mojibake markers {hits} in {rel}")
        if path.is_file() and path.suffix.lower() == ".json":
            parse_json(path, rel)
        if path.is_file() and path.suffix.lower() == ".py":
            parse_python(path, rel)

    print("PASS: public package verification succeeded")


if __name__ == "__main__":
    main()
