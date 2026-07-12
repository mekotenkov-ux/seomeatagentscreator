from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from content_safety import require_safe_file


DEFAULT_REQUIRED = [
    "AGENTS.md", "agent-ir.json", "MANIFEST.json", "INSTALL.md", "FILES.sha256"
]
FORBIDDEN_PARTS = {
    ".git", ".github", "__pycache__", "scripts", "devkit", "tests",
    "validation-tests", "source-materials", "test-scenarios", "eval-scripts",
    "chat-prompts", "ide-versions", "agent-workspace", "browser-profile",
    "chrome-profile", "node_modules",
}
FORBIDDEN_SUFFIXES = {
    ".pyc", ".pyo", ".sqlite", ".db", ".zip", ".7z", ".tar", ".gz",
}
HASH_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def sha256_file(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def junction(path: Path) -> bool:
    return hasattr(os.path, "isjunction") and os.path.isjunction(path)


def reject_reparse_components(root: Path, parts: tuple[str, ...], label: str) -> None:
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink() or junction(current):
            fail(f"{label} crosses a symlink or junction: {current}")


def confined_path(root: Path, raw: str, label: str) -> tuple[str, Path]:
    if "\\" in raw:
        fail(f"{label} must use forward slashes: {raw}")
    pure = PurePosixPath(raw)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        fail(f"{label} is not a confined relative path: {raw}")
    reject_reparse_components(root, pure.parts, label)
    normalized = pure.as_posix()
    path = root.joinpath(*pure.parts).resolve(strict=False)
    try:
        path.relative_to(root)
    except ValueError:
        fail(f"{label} escapes runtime root: {raw}")
    return normalized, path


def read_inventory(root: Path) -> dict[str, str]:
    inventory = root / "FILES.sha256"
    if not inventory.is_file():
        fail("FILES.sha256 is required for exact runtime validation")
    result: dict[str, str] = {}
    for line_no, line in enumerate(
        inventory.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            expected, raw = line.split("  ", 1)
        except ValueError:
            fail(f"invalid FILES.sha256 row {line_no}")
        if not HASH_RE.fullmatch(expected):
            fail(f"invalid checksum in FILES.sha256 row {line_no}")
        rel, path = confined_path(root, raw, f"inventory row {line_no}")
        if rel in result:
            fail(f"duplicate inventory path: {rel}")
        if not path.is_file():
            fail(f"inventory file missing: {rel}")
        if sha256_file(path) != expected.lower():
            fail(f"checksum mismatch: {rel}")
        result[rel] = expected.lower()
    if not result:
        fail("FILES.sha256 cannot be empty")
    return result


def zip_entry_count(path: Path) -> int:
    try:
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                fail("runtime zip failed CRC validation")
            return len(archive.infolist())
    except zipfile.BadZipFile:
        fail("--runtime-zip is not a valid zip archive")


def write_report(
    path: Path, release_id: str, root: Path, runtime_zip: Path,
    archive_ref: str, entry_count: int,
) -> None:
    inventory = root / "FILES.sha256"
    report = {
        "schema_version": 2,
        "evidence_id": f"install-{release_id}",
        "system_release_id": release_id,
        "gate_id": "install",
        "status": "pass",
        "verification_command": "validate_runtime_install.py",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "executor_provenance_ref": "local-runtime-validator",
        "runtime_archive_ref": archive_ref,
        "runtime_zip_name": runtime_zip.name,
        "runtime_zip_sha256": sha256_file(runtime_zip),
        "inventory_sha256": sha256_file(inventory),
        "entry_count": entry_count,
        "validator_sha256": sha256_file(Path(__file__).resolve()),
        "artifact_refs": [archive_ref],
        "validated_root_name": root.name,
        "blockers": [],
        "warnings": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a fresh runtime extraction against an exact checksum inventory."
    )
    parser.add_argument("root", nargs="?", default=".", help="Extracted runtime root")
    parser.add_argument(
        "--required", action="append", default=[], help="Required relative file path"
    )
    parser.add_argument("--system-release-id", default="")
    parser.add_argument("--runtime-zip", type=Path)
    parser.add_argument("--runtime-archive-ref", default="")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir() or root.is_symlink() or junction(root):
        fail(f"runtime root is not a safe directory: {root}")
    required_files = args.required or DEFAULT_REQUIRED
    for raw in required_files:
        _, path = confined_path(root, raw.replace("\\", "/"), "required path")
        if not path.is_file():
            fail(f"required file missing: {raw}")

    actual_files: set[str] = set()
    for path in root.rglob("*"):
        rel_path = path.relative_to(root)
        rel = rel_path.as_posix()
        if path.is_symlink() or junction(path):
            fail(f"runtime may not contain symlinks or junctions: {rel}")
        if set(rel_path.parts) & FORBIDDEN_PARTS:
            fail(f"forbidden runtime path: {rel}")
        if path.is_file():
            if path.suffix.lower() in FORBIDDEN_SUFFIXES:
                fail(f"forbidden runtime suffix: {rel}")
            try:
                require_safe_file(path, f"unsafe runtime file {rel}")
            except ValueError as exc:
                fail(str(exc))
            if rel != "FILES.sha256":
                actual_files.add(rel)

    inventory = read_inventory(root)
    if set(inventory) != actual_files:
        unlisted = sorted(actual_files - set(inventory))
        stale = sorted(set(inventory) - actual_files)
        fail(f"runtime inventory is not exact; unlisted={unlisted}, stale={stale}")
    if args.report:
        if not args.system_release_id:
            fail("--report requires --system-release-id")
        if not args.runtime_zip or not args.runtime_archive_ref:
            fail("--report requires --runtime-zip and --runtime-archive-ref")
        runtime_zip = args.runtime_zip.resolve()
        if not runtime_zip.is_file():
            fail("--runtime-zip does not exist")
        write_report(
            args.report.resolve(), args.system_release_id, root, runtime_zip,
            args.runtime_archive_ref, zip_entry_count(runtime_zip),
        )
    print("PASS: exact runtime install validation succeeded")


if __name__ == "__main__":
    main()
