from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - intentionally broad CLI guard
        fail(f"cannot read manifest {path}: {exc}")


def ensure_inside_base(path: Path, base: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(base)
    except ValueError:
        fail(f"{label} must stay inside manifest directory: {resolved}")
    return resolved


def should_exclude(rel: str, parts: tuple[str, ...], suffix: str, exclude_parts: set[str], exclude_suffixes: set[str]) -> bool:
    if set(parts) & exclude_parts:
        return True
    if suffix.lower() in exclude_suffixes:
        return True
    return False


def iter_manifest_files(source_root: Path, include: list[str], exclude_parts: set[str], exclude_suffixes: set[str]) -> list[Path]:
    files: dict[str, Path] = {}
    for pattern in include:
        matches = source_root.glob(pattern)
        for path in matches:
            if not path.is_file():
                continue
            rel_path = path.relative_to(source_root)
            rel = rel_path.as_posix()
            if should_exclude(rel, rel_path.parts, path.suffix, exclude_parts, exclude_suffixes):
                continue
            if fnmatch.fnmatch(rel, "*/__pycache__/*"):
                continue
            files[rel] = path
    return [files[key] for key in sorted(files)]


def recreate_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_files(files: list[Path], source_root: Path, staging_dir: Path) -> None:
    for source in files:
        rel = source.relative_to(source_root)
        target = staging_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_files_sha256(staging_dir: Path) -> None:
    rows = []
    for path in sorted(p for p in staging_dir.rglob("*") if p.is_file()):
        if path.name == "FILES.sha256":
            continue
        rel = path.relative_to(staging_dir).as_posix()
        rows.append(f"{sha256_file(path)}  {rel}")
    (staging_dir / "FILES.sha256").write_text("\n".join(rows) + "\n", encoding="utf-8")


def zip_dir(staging_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in staging_dir.rglob("*") if p.is_file()):
            archive.write(path, path.relative_to(staging_dir).as_posix())


def inspect_zip(zip_path: Path, required_dot_directories: list[str]) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    for name in names:
        if "\\" in name:
            fail(f"zip entry uses Windows separator: {name}")
    for dot_dir in required_dot_directories:
        normalized = dot_dir.strip("/").replace("\\", "/") + "/"
        if not any(name.startswith(normalized) for name in names):
            fail(f"required dot directory missing from zip: {dot_dir}")


def build_package(base: Path, config: dict, key: str, required_dot_directories: list[str]) -> None:
    section = config.get(key)
    if not section:
        return
    source_root = ensure_inside_base(base / section["source_root"], base, f"{key}.source_root")
    staging_dir = ensure_inside_base(base / section["staging_dir"], base, f"{key}.staging_dir")
    zip_path = ensure_inside_base(base / section["zip_path"], base, f"{key}.zip_path")
    include = section.get("include", ["**"])
    exclude_parts = set(section.get("exclude_parts", []))
    exclude_suffixes = set(section.get("exclude_suffixes", []))

    files = iter_manifest_files(source_root, include, exclude_parts, exclude_suffixes)
    recreate_dir(staging_dir)
    copy_files(files, source_root, staging_dir)
    if config.get("generate_files_sha256", False):
        write_files_sha256(staging_dir)
    zip_dir(staging_dir, zip_path)
    inspect_zip(zip_path, required_dot_directories if key == "runtime" else [])
    print(f"Built {key}: {zip_path} ({len(files)} source files)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build runtime/devkit agent export zips from an explicit manifest.")
    parser.add_argument("manifest", help="Path to export-manifest.json")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    base = manifest_path.parent
    config = load_manifest(manifest_path)
    required_dot_directories = config.get("required_dot_directories", [])
    build_package(base, config, "runtime", required_dot_directories)
    build_package(base, config, "devkit", required_dot_directories)


if __name__ == "__main__":
    main()
