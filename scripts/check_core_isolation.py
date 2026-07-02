from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".html", ".py", ".txt", ".csv"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def load_literals(path: Path) -> list[str]:
    if not path.exists():
        fail(f"literal file missing: {path}")
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            values = data.get("forbidden_literals", [])
        else:
            values = data
    else:
        values = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    return [value for value in values if isinstance(value, str) and value.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan universal core files for forbidden client/domain literals.")
    parser.add_argument("root", help="Universal core root to scan")
    parser.add_argument("literals", help="JSON or text file with forbidden literals")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    literals = load_literals(Path(args.literals).resolve())
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(root).as_posix()
        for literal in literals:
            if literal in text:
                fail(f"forbidden literal {literal!r} in {rel}")
    print("PASS: universal core isolation check succeeded")


if __name__ == "__main__":
    main()
