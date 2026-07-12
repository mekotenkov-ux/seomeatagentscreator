from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from content_safety import require_safe_file


RUNTIME_FORBIDDEN = {
    ".git", ".github", "scripts", "devkit", "tests", "validation-tests",
    "source-materials", "test-scenarios", "eval-scripts", "chat-prompts",
    "ide-versions", "__pycache__", "node_modules",
}
SAFE_ENV_KEYS = {
    "PATH", "PATHEXT", "SYSTEMROOT", "COMSPEC", "WINDIR", "TEMP", "TMP",
    "LANG", "LC_ALL", "PYTHONIOENCODING",
}


@dataclass(frozen=True)
class PackageLayout:
    key: str
    source: Path
    staging: Path
    zip_path: Path
    package_report: Path | None
    install_report: Path | None


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def load_json(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot read {label} {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def junction(path: Path) -> bool:
    return hasattr(os.path, "isjunction") and os.path.isjunction(path)


def reject_reparse_components(base: Path, parts: tuple[str, ...], label: str) -> None:
    current = base
    for part in parts:
        current = current / part
        if current.is_symlink() or junction(current):
            fail(f"{label} crosses a symlink or junction: {current}")


def confined(base: Path, value: str, label: str) -> Path:
    raw = value.replace("\\", "/")
    pure = PurePosixPath(raw)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        fail(f"{label} must be a confined relative path")
    reject_reparse_components(base, pure.parts, label)
    lexical = base.joinpath(*pure.parts)
    resolved = lexical.resolve(strict=False)
    if not inside(resolved, base):
        fail(f"{label} escapes the manifest directory")
    return resolved


def overlaps(left: Path, right: Path) -> bool:
    return left == right or inside(left, right) or inside(right, left)


def load_layouts(base: Path, config: dict, manifest_path: Path) -> dict[str, PackageLayout]:
    layouts: dict[str, PackageLayout] = {}
    for key in ("runtime", "devkit"):
        section = config.get(key)
        if not isinstance(section, dict):
            fail(f"export manifest needs a {key} object")
        package_report = (
            confined(base, section["package_validation_report"], f"{key}.package_validation_report")
            if section.get("package_validation_report") else None
        )
        install_report = (
            confined(base, section["install_validation_report"], f"{key}.install_validation_report")
            if section.get("install_validation_report") else None
        )
        layouts[key] = PackageLayout(
            key=key,
            source=confined(base, section["source_root"], f"{key}.source_root"),
            staging=confined(base, section["staging_dir"], f"{key}.staging_dir"),
            zip_path=confined(base, section["zip_path"], f"{key}.zip_path"),
            package_report=package_report,
            install_report=install_report,
        )

    sources = [layout.source for layout in layouts.values()]
    staging_dirs = [layout.staging for layout in layouts.values()]
    outputs = [layout.zip_path for layout in layouts.values()]
    outputs.extend(
        path
        for layout in layouts.values()
        for path in (layout.package_report, layout.install_report)
        if path is not None
    )
    if len(outputs) != len(set(outputs)):
        fail("zip and report output paths must be globally unique")
    for source in sources:
        if source == base or source == manifest_path:
            fail("source_root may not equal the manifest directory or manifest")
    for left_index, left in enumerate(sources):
        for right in sources[left_index + 1 :]:
            if overlaps(left, right):
                fail("runtime and devkit source roots must be disjoint")
    for staging in staging_dirs:
        if staging == base or staging == manifest_path:
            fail("staging_dir may not equal the manifest directory or manifest")
        for source in sources:
            if overlaps(staging, source):
                fail("all source_root and staging_dir paths must be globally disjoint")
    for left_index, left in enumerate(staging_dirs):
        for right in staging_dirs[left_index + 1 :]:
            if overlaps(left, right):
                fail("runtime and devkit staging directories must be disjoint")
    for output in outputs:
        if output == manifest_path or output == base:
            fail("zip/report output collides with manifest or its directory")
        for source in sources:
            if inside(output, source):
                fail("zip/report output may not be inside a source_root")
        for staging in staging_dirs:
            if inside(output, staging) or output == staging:
                fail("zip/report output may not be inside a staging_dir")
    return layouts


def scan_source_tree(source: Path) -> None:
    if source.is_symlink() or junction(source):
        fail(f"source_root may not be a symlink or junction: {source}")
    for item in source.rglob("*"):
        if item.is_symlink() or junction(item):
            fail(f"source tree contains a symlink or junction: {item}")


def selected_files(
    source: Path, include: list[str], exclude_parts: set[str],
    exclude_suffixes: set[str],
) -> list[Path]:
    scan_source_tree(source)
    files: dict[str, Path] = {}
    for pattern in include:
        for candidate in source.glob(pattern):
            if not candidate.is_file():
                continue
            resolved = candidate.resolve()
            if not inside(resolved, source):
                fail(f"selected file escapes source_root: {candidate}")
            rel_path = candidate.relative_to(source)
            rel = rel_path.as_posix()
            if set(rel_path.parts) & (exclude_parts | {".git", "__pycache__"}):
                continue
            if candidate.suffix.lower() in exclude_suffixes:
                continue
            if fnmatch.fnmatch(rel, "*/__pycache__/*"):
                continue
            try:
                require_safe_file(candidate, f"unsafe export file {rel}")
            except ValueError as exc:
                fail(str(exc))
            files[rel] = candidate
    if not files:
        fail(f"manifest selected no files from {source}")
    return [files[key] for key in sorted(files)]


def recreate(path: Path) -> None:
    if path.is_symlink() or junction(path):
        fail(f"refusing to recreate a symlink or junction: {path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=False)


def copy_files(files: list[Path], source: Path, staging: Path) -> None:
    for item in files:
        target = staging / item.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)


def sha256_file(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def write_inventory(staging: Path) -> Path:
    inventory = staging / "FILES.sha256"
    rows = []
    for path in sorted(item for item in staging.rglob("*") if item.is_file()):
        if path == inventory:
            continue
        rows.append(f"{sha256_file(path)}  {path.relative_to(staging).as_posix()}")
    inventory.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return inventory


def build_zip(staging: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        if zip_path.is_dir() or zip_path.is_symlink() or junction(zip_path):
            fail(f"unsafe existing zip output: {zip_path}")
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(item for item in staging.rglob("*") if item.is_file()):
            archive.write(path, path.relative_to(staging).as_posix())


def inspect_zip(
    zip_path: Path, staging: Path, required_dot_dirs: list[str], runtime: bool
) -> dict[str, int]:
    expected = {
        path.relative_to(staging).as_posix()
        for path in staging.rglob("*")
        if path.is_file()
    }
    with zipfile.ZipFile(zip_path) as archive:
        infos = archive.infolist()
        if archive.testzip() is not None:
            fail(f"zip CRC test failed: {zip_path}")
    names = [info.filename for info in infos]
    if len(names) != len(set(names)):
        fail(f"zip contains duplicate entries: {zip_path}")
    for info in infos:
        name = info.filename
        pure = PurePosixPath(name)
        if (
            "\\" in name
            or pure.is_absolute()
            or ".." in pure.parts
            or re.match(r"^[A-Za-z]:", name)
        ):
            fail(f"unsafe zip entry name: {name}")
        mode = (info.external_attr >> 16) & 0o170000
        if info.is_dir():
            if mode not in {0, stat.S_IFDIR}:
                fail(f"unsafe zip directory type: {name}")
        elif mode not in {0, stat.S_IFREG}:
            fail(f"zip entry is not a regular file: {name}")
        if info.flag_bits & 0x1:
            fail(f"encrypted zip entry is forbidden: {name}")
        if runtime and set(pure.parts) & RUNTIME_FORBIDDEN:
            fail(f"runtime zip contains devkit path: {name}")
    if set(names) != expected:
        fail(f"zip entries do not exactly match staging: {zip_path}")
    for dot_dir in required_dot_dirs:
        normalized = dot_dir.strip("/\\") + "/"
        if not any(name.startswith(normalized) for name in names):
            fail(f"required dot directory missing from zip: {dot_dir}")
    return {"entry_count": len(infos)}


def write_package_report(
    path: Path, release_id: str, archive_ref: str, zip_path: Path,
    inventory: Path, entry_count: int,
) -> dict:
    report = {
        "schema_version": 2,
        "evidence_id": f"package-{release_id}",
        "system_release_id": release_id,
        "gate_id": "package",
        "status": "pass",
        "verification_command": "build_agent_export.py",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "executor_provenance_ref": "local-export-builder",
        "runtime_archive_ref": archive_ref,
        "runtime_zip_name": zip_path.name,
        "runtime_zip_sha256": sha256_file(zip_path),
        "inventory_sha256": sha256_file(inventory),
        "entry_count": entry_count,
        "builder_sha256": sha256_file(Path(__file__).resolve()),
        "artifact_refs": [archive_ref],
        "blockers": [],
        "warnings": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def build_package(
    config: dict, layout: PackageLayout, required_dot_dirs: list[str]
) -> tuple[Path, Path, Path, int]:
    section = config[layout.key]
    if not layout.source.is_dir():
        fail(f"{layout.key}.source_root does not exist: {layout.source}")
    files = selected_files(
        layout.source,
        section.get("include", ["**"]),
        set(section.get("exclude_parts", [])),
        {value.lower() for value in section.get("exclude_suffixes", [])},
    )
    recreate(layout.staging)
    copy_files(files, layout.source, layout.staging)
    if not config.get("generate_files_sha256"):
        fail("generate_files_sha256 must be true for release exports")
    inventory = write_inventory(layout.staging)
    build_zip(layout.staging, layout.zip_path)
    inspection = inspect_zip(
        layout.zip_path,
        layout.staging,
        required_dot_dirs if layout.key == "runtime" else [],
        runtime=layout.key == "runtime",
    )
    print(f"Built {layout.key}: {layout.zip_path} ({len(files)} source files)")
    return layout.staging, layout.zip_path, inventory, inspection["entry_count"]


def find_validator_path(base: Path, command: list[str]) -> Path:
    rendered = [part.replace("{repo_root}", str(base)) for part in command]
    candidates = [Path(part) for part in rendered if Path(part).name == "validate_runtime_install.py"]
    if len(candidates) != 1:
        fail("install command must invoke exactly one validate_runtime_install.py")
    path = candidates[0]
    if not path.is_absolute():
        path = base / path
    path = path.resolve()
    if not path.is_file():
        fail(f"install validator does not exist: {path}")
    return path


def safe_subprocess_env() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key.upper() in SAFE_ENV_KEYS}


def validate_install_report(
    report: dict, release_id: str, archive_ref: str, runtime_zip: Path,
    inventory: Path, entry_count: int, validator_path: Path,
) -> None:
    expected = {
        "system_release_id": release_id,
        "gate_id": "install",
        "status": "pass",
        "runtime_archive_ref": archive_ref,
        "runtime_zip_name": runtime_zip.name,
        "runtime_zip_sha256": sha256_file(runtime_zip),
        "inventory_sha256": sha256_file(inventory),
        "entry_count": entry_count,
        "validator_sha256": sha256_file(validator_path),
    }
    for field, value in expected.items():
        if report.get(field) != value:
            fail(f"install report mismatch: {field}")
    if report.get("artifact_refs") != [archive_ref]:
        fail("install report must reference exactly the runtime archive")
    if report.get("blockers") or report.get("warnings"):
        fail("install report contains blockers or warnings")


def run_install_simulation(
    base: Path, config: dict, layout: PackageLayout, runtime_zip: Path,
    inventory: Path, entry_count: int, release_id: str, archive_ref: str,
) -> None:
    command = config.get("install_simulation_command")
    if not isinstance(command, list) or not command or not all(
        isinstance(part, str) and part for part in command
    ):
        fail("install_simulation_command must be a non-empty argument list")
    required_placeholders = {
        "{root}", "{repo_root}", "{install_report}", "{runtime_zip}",
        "{runtime_archive_ref}", "{system_release_id}",
    }
    joined = "\n".join(command)
    missing = sorted(value for value in required_placeholders if value not in joined)
    if missing:
        fail(f"install command missing placeholders: {missing}")
    if layout.install_report is None:
        fail("runtime.install_validation_report is required")
    validator_path = find_validator_path(base, command)
    if layout.install_report.exists():
        if layout.install_report.is_dir() or layout.install_report.is_symlink() or junction(layout.install_report):
            fail("unsafe existing install report output")
        layout.install_report.unlink()
    timeout_seconds = config.get("install_simulation_timeout_seconds")
    if not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 3600:
        fail("install_simulation_timeout_seconds must be in [1, 3600]")
    with tempfile.TemporaryDirectory(prefix="agent-install-") as temp:
        extracted = Path(temp).resolve()
        with zipfile.ZipFile(runtime_zip) as archive:
            archive.extractall(extracted)
        replacements = {
            "{root}": str(extracted),
            "{repo_root}": str(base),
            "{install_report}": str(layout.install_report),
            "{runtime_zip}": str(runtime_zip),
            "{runtime_archive_ref}": archive_ref,
            "{system_release_id}": release_id,
        }
        rendered = command
        for marker, value in replacements.items():
            rendered = [part.replace(marker, value) for part in rendered]
        try:
            completed = subprocess.run(
                rendered,
                cwd=base,
                env=safe_subprocess_env(),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            fail("install simulation timed out")
        if completed.returncode != 0:
            output = (completed.stdout + completed.stderr)[-2000:]
            fail(f"install simulation failed with exit code {completed.returncode}: {output}")
    if not layout.install_report.is_file():
        fail("install validator did not create the configured report")
    report = load_json(layout.install_report, "install report")
    validate_install_report(
        report, release_id, archive_ref, runtime_zip, inventory, entry_count,
        validator_path,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build isolated runtime/devkit zips. All manifest paths are relative "
            "to the manifest directory."
        )
    )
    parser.add_argument("manifest", type=Path, help="Export manifest copied to the development-repo root")
    parser.add_argument(
        "--run-install-simulation", action="store_true",
        help="Validate a fresh extraction with the bundled runtime validator.",
    )
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    base = manifest_path.parent.resolve()
    config = load_json(manifest_path, "export manifest")
    if config.get("schema_version") != 2:
        fail("export manifest must use schema_version 2")
    release_id = config.get("system_release_id")
    if not release_id:
        fail("export manifest needs system_release_id")
    archive_ref = config.get("runtime", {}).get("runtime_archive_ref")
    if not isinstance(archive_ref, str) or not archive_ref:
        fail("runtime.runtime_archive_ref is required")
    layouts = load_layouts(base, config, manifest_path)
    required_dot_dirs = config.get("required_dot_directories", [])
    runtime_result = build_package(config, layouts["runtime"], required_dot_dirs)
    build_package(config, layouts["devkit"], required_dot_dirs)
    _, runtime_zip, inventory, entry_count = runtime_result
    runtime_layout = layouts["runtime"]
    if runtime_layout.package_report is None:
        fail("runtime.package_validation_report is required")
    write_package_report(
        runtime_layout.package_report, release_id, archive_ref, runtime_zip,
        inventory, entry_count,
    )
    if args.run_install_simulation:
        run_install_simulation(
            base, config, runtime_layout, runtime_zip, inventory, entry_count,
            release_id, archive_ref,
        )
    elif runtime_layout.install_report is not None:
        fail("install_validation_report requires --run-install-simulation")


if __name__ == "__main__":
    main()
