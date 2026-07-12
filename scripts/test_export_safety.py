from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_agent_export.py"
INSTALL_VALIDATOR = ROOT / "scripts" / "validate_runtime_install.py"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def fixture(base: Path) -> Path:
    runtime = base / "runtime"
    devkit = base / "devkit"
    runtime.mkdir()
    devkit.mkdir()
    (runtime / "AGENTS.md").write_text("# Runtime\n", encoding="utf-8")
    write_json(runtime / "agent-ir.json", {"job": "fixture"})
    write_json(runtime / "MANIFEST.json", {"name": "runtime", "system_release_id": "release-fixture"})
    (runtime / "INSTALL.md").write_text("# Install\n", encoding="utf-8")
    (devkit / "README.md").write_text("# Devkit\n", encoding="utf-8")
    scripts = base / "scripts"
    scripts.mkdir()
    shutil.copy2(INSTALL_VALIDATOR, scripts / "validate_runtime_install.py")
    shutil.copy2(ROOT / "scripts" / "content_safety.py", scripts / "content_safety.py")
    manifest = {
        "schema_version": 2,
        "package": "fixture",
        "version": "1.0.0",
        "system_release_id": "release-fixture",
        "runtime": {
            "source_root": "runtime",
            "staging_dir": "dist/runtime-staging",
            "zip_path": "dist/runtime.zip",
            "package_validation_report": "dist/package-validation.json",
            "install_validation_report": "dist/install-validation.json",
            "runtime_archive_ref": "runtime-archive",
            "include": ["**"],
            "exclude_parts": [],
            "exclude_suffixes": [],
        },
        "devkit": {
            "source_root": "devkit",
            "staging_dir": "dist/devkit-staging",
            "zip_path": "dist/devkit.zip",
            "include": ["**"],
            "exclude_parts": [],
            "exclude_suffixes": [],
        },
        "required_dot_directories": [],
        "generate_files_sha256": True,
        "install_simulation_timeout_seconds": 30,
        "install_simulation_command": [
            sys.executable,
            "-B",
            "{repo_root}/scripts/validate_runtime_install.py",
            "{root}",
            "--system-release-id",
            "{system_release_id}",
            "--runtime-zip",
            "{runtime_zip}",
            "--runtime-archive-ref",
            "{runtime_archive_ref}",
            "--report",
            "{install_report}",
        ],
    }
    path = base / "export.json"
    write_json(path, manifest)
    return path


class ExportSafetyTest(unittest.TestCase):
    def run_builder(self, manifest: Path, install: bool = False) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, "-B", str(BUILDER), str(manifest)]
        if install:
            command.append("--run-install-simulation")
        return subprocess.run(command, capture_output=True, text=True)

    def test_build_and_extracted_install_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            result = self.run_builder(manifest, install=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((base / "dist/package-validation.json").is_file())
            self.assertTrue((base / "dist/install-validation.json").is_file())
            with zipfile.ZipFile(base / "dist/runtime.zip") as archive:
                names = archive.namelist()
                self.assertIn("FILES.sha256", names)
                self.assertNotIn("scripts/", names)

    def test_manifest_directory_cannot_be_staging(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            value = json.loads(manifest.read_text(encoding="utf-8"))
            value["runtime"]["staging_dir"] = "."
            write_json(manifest, value)
            result = self.run_builder(manifest, install=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("confined relative path", result.stdout + result.stderr)

    def test_runtime_inventory_rejects_unlisted_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            result = self.run_builder(manifest, install=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            staging = base / "dist/runtime-staging"
            (staging / "unlisted.txt").write_text("late file\n", encoding="utf-8")
            check = subprocess.run(
                [sys.executable, "-B", str(INSTALL_VALIDATOR), str(staging)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(check.returncode, 0)
            self.assertIn("inventory is not exact", check.stdout + check.stderr)

    def test_runtime_rejects_devkit_path(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            result = self.run_builder(manifest, install=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            staging = base / "dist/runtime-staging"
            scripts = staging / "scripts"
            scripts.mkdir()
            (scripts / "validator.py").write_text("pass\n", encoding="utf-8")
            check = subprocess.run(
                [sys.executable, "-B", str(INSTALL_VALIDATOR), str(staging)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(check.returncode, 0)
            self.assertIn("forbidden runtime path", check.stdout + check.stderr)

    def test_secret_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            (base / "runtime/.env").write_text("TOKEN=placeholder\n", encoding="utf-8")
            result = self.run_builder(manifest, install=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("secret-bearing file", result.stdout + result.stderr)

    def test_cross_package_overlap_is_rejected_before_delete(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            marker = base / "runtime/marker.txt"
            marker.write_text("keep\n", encoding="utf-8")
            value = json.loads(manifest.read_text(encoding="utf-8"))
            value["devkit"]["staging_dir"] = "runtime"
            write_json(manifest, value)
            result = self.run_builder(manifest, install=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("globally disjoint", result.stdout + result.stderr)
            self.assertTrue(marker.is_file())

    def test_report_zip_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            value = json.loads(manifest.read_text(encoding="utf-8"))
            value["runtime"]["package_validation_report"] = value["runtime"]["zip_path"]
            write_json(manifest, value)
            result = self.run_builder(manifest, install=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("globally unique", result.stdout + result.stderr)

    def test_noop_install_command_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            value = json.loads(manifest.read_text(encoding="utf-8"))
            value["install_simulation_command"] = [sys.executable, "-c", "pass"]
            write_json(manifest, value)
            result = self.run_builder(manifest, install=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing placeholders", result.stdout + result.stderr)

    def test_local_path_and_slack_token_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            leaked_path = "C:" + "\\Users\\" + "Alice\\private.txt"
            leaked_token = "xoxb-" + ("A" * 30)
            (base / "runtime/notes.txt").write_text(
                leaked_path + "\n" + leaked_token + "\n", encoding="utf-8"
            )
            result = self.run_builder(manifest, install=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe export file", result.stdout + result.stderr)

    def test_zip_symlink_metadata_is_rejected(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            import build_agent_export as builder

            with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
                base = Path(temp)
                staging = base / "staging"
                staging.mkdir()
                (staging / "link.txt").write_text("regular\n", encoding="utf-8")
                archive_path = base / "malicious.zip"
                info = zipfile.ZipInfo("link.txt")
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                with zipfile.ZipFile(archive_path, "w") as archive:
                    archive.writestr(info, "../outside")
                with self.assertRaises(SystemExit):
                    builder.inspect_zip(archive_path, staging, [], runtime=True)
        finally:
            sys.path.remove(str(ROOT / "scripts"))

    def test_symlink_escape_is_rejected_when_supported(self) -> None:
        with tempfile.TemporaryDirectory(prefix="export-safety-") as temp:
            base = Path(temp)
            manifest = fixture(base)
            outside = base / "outside.txt"
            outside.write_text("outside\n", encoding="utf-8")
            link = base / "runtime/link.txt"
            try:
                os.symlink(outside, link)
            except OSError:
                self.skipTest("symlink creation is unavailable")
            result = self.run_builder(manifest, install=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink or junction", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
