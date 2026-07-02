from __future__ import annotations

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
    "agent-system/templates/agent-ir.template.json",
    "agent-system/templates/tool-registry.template.json",
    "agent-system/templates/runtime-manifest.template.json",
    "agent-system/templates/release-review.template.md",
    "agent-system/templates/trigger-lab.template.yaml",
    "agent-system/templates/output-eval-lab.template.yaml",
    "agent-system/checklists/export-clean-checklist.md",
    "agent-system/checklists/production-readiness-checklist.md",
    "docs/index.html",
    "docs/quick-start.md",
    "docs/architecture.md",
    "docs/debugging.md",
    "docs/packaging.md",
]

FORBIDDEN_PARTS = {
    "__pycache__",
    "node_modules",
    "chrome-qfo-profile",
    "browser-profile",
    "agent-workspace",
    "validation-runs",
    "export-staging",
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

FORBIDDEN_TEXT = [
    "C:" + "\\Users\\",
    "BLACK" + "WHITE",
    "Copy" + "KillerDev",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def main() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"required file missing: {rel}")

    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("license") != "MIT":
        fail("manifest license must be MIT")

    page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    if "https://seomeat.ru/" not in page:
        fail("docs/index.html must link to https://seomeat.ru/")

    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        parts = set(path.relative_to(ROOT).parts)
        if parts & FORBIDDEN_PARTS:
            fail(f"forbidden path present: {rel}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"forbidden file suffix present: {rel}")
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".html", ".py"}:
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_TEXT:
                if pattern in text:
                    fail(f"forbidden local text {pattern!r} in {rel}")

    print("PASS: public package verification succeeded")


if __name__ == "__main__":
    main()
