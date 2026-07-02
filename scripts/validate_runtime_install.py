from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


DEFAULT_REQUIRED = [
    "AGENTS.md",
    "MANIFEST.json",
]

FORBIDDEN_PARTS = {
    "__pycache__",
    "tests",
    "validation-tests",
    "source-materials",
    "test-scenarios",
    "eval-scripts",
    "chat-prompts",
    "ide-versions",
    "agent-workspace",
    "browser-profile",
    "chrome-profile",
    "node_modules",
}

FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".sqlite", ".db", ".zip", ".7z", ".tar", ".gz"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_files_sha256(root: Path) -> None:
    inventory = root / "FILES.sha256"
    if not inventory.exists():
        return
    for line_no, line in enumerate(inventory.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            expected, rel = line.split("  ", 1)
        except ValueError:
            fail(f"invalid FILES.sha256 row {line_no}")
        path = root / rel
        if not path.is_file():
            fail(f"inventory file missing: {rel}")
        actual = sha256_file(path)
        if actual.lower() != expected.lower():
            fail(f"checksum mismatch: {rel}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an installed runtime package shape.")
    parser.add_argument("root", nargs="?", default=".", help="Installed runtime root")
    parser.add_argument("--required", action="append", default=[], help="Required relative file path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    required = args.required or DEFAULT_REQUIRED
    for rel in required:
        if not (root / rel).is_file():
            fail(f"required file missing: {rel}")

    for path in root.rglob("*"):
        rel_path = path.relative_to(root)
        rel = rel_path.as_posix()
        if set(rel_path.parts) & FORBIDDEN_PARTS:
            fail(f"forbidden runtime path: {rel}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"forbidden runtime suffix: {rel}")

    verify_files_sha256(root)
    print("PASS: runtime install validation succeeded")


if __name__ == "__main__":
    main()
