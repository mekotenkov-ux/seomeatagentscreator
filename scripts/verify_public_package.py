from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


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
    "agent-system/skills/workflow-loop-me/SKILL.md",
    "agent-system/skills/repo-tool-librarian/SKILL.md",
    "agent-system/skills/subagent-orchestrator/SKILL.md",
    "agent-system/references/README.md",
    "agent-system/references/skill-training-lab.md",
    "agent-system/references/package-boundary.md",
    "agent-system/references/repo-tool-library.md",
    "agent-system/catalog/README.md",
    "agent-system/catalog/repo-tool-library.json",
    "agent-system/references/birth-protocol.md",
    "agent-system/references/ide-runtime-adaptation.md",
    "agent-system/references/hook-system.md",
    "agent-system/references/subagent-orchestration.md",
    "agent-system/references/context-and-quality-gates.md",
    "agent-system/references/target-adapters.md",
    "agent-system/references/final-evidence-and-claim-guard.md",
    "agent-system/references/long-running-tool-lifecycle.md",
    "agent-system/references/universal-core-isolation.md",
    "agent-system/references/observability-and-living-adaptation.md",
    "agent-system/references/validation-harness.md",
    "agent-system/templates/agent-ir.template.json",
    "agent-system/templates/workflow-notes.template.md",
    "agent-system/templates/workflow-spec.template.md",
    "agent-system/templates/workflow-discovery-ledger.template.json",
    "agent-system/templates/repo-tool-library.template.json",
    "agent-system/templates/repo-tool-card.template.md",
    "agent-system/templates/repo-tool-intake.template.md",
    "agent-system/templates/agent-birth-contract.template.json",
    "agent-system/templates/runtime-profile.template.json",
    "agent-system/templates/birth-plan.template.json",
    "agent-system/templates/environment-readiness.template.json",
    "agent-system/templates/project-context.template.json",
    "agent-system/templates/birth-validation-gates.template.json",
    "agent-system/templates/tool-registry.template.json",
    "agent-system/templates/hook-registry.template.json",
    "agent-system/templates/hook-validation.template.yaml",
    "agent-system/templates/subagent-role-registry.template.json",
    "agent-system/templates/subagent-delegation-plan.template.json",
    "agent-system/templates/subagent-task-contract.template.json",
    "agent-system/templates/subagent-result.template.json",
    "agent-system/templates/subagent-run-ledger.template.jsonl",
    "agent-system/templates/subagent-eval-lab.template.yaml",
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
    "requirements-dev.txt",
    "scripts/build_agent_export.py",
    "scripts/validate_subagent_run.py",
    "scripts/validate_runtime_install.py",
    "scripts/check_core_isolation.py",
    "docs/index.html",
    "docs/quick-start.md",
    "docs/architecture.md",
    "docs/hooks.md",
    "docs/subagents.md",
    "docs/birth.md",
    "docs/workflow-discovery.md",
    "docs/repo-tool-library.md",
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

FORBIDDEN_SECRET_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".npmrc",
    ".pypirc",
    "id_rsa",
    "id_ed25519",
}

FORBIDDEN_SECRET_SUFFIXES = {
    ".key",
    ".p12",
    ".pem",
    ".pfx",
}

TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".html", ".py", ".txt", ".csv"}

FORBIDDEN_TEXT = [
    "C:" + "\\Users\\",
    "C:" + "/Users/",
    "BLACK" + "WHITE",
    "Copy" + "KillerDev",
]

MOJIBAKE_MARKERS = ["Рџ", "Рћ", "РЅ", "Р°", "Ð", "Ñ"]

SECRET_PATTERNS = {
    "private key header": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "OpenAI API key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    "AWS access key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
}


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


def parse_yaml(path: Path, rel: str) -> object:
    if yaml is None:
        fail("PyYAML is required for YAML verification; install requirements-dev.txt")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid YAML in {rel}: {exc}")


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
    for public_term in ["Skill Training Lab", "target conformance", "final evidence", "birth protocol", "workflow discovery", "repo/tool library", "hook system", "subagent orchestration"]:
        if public_term not in page:
            fail(f"docs/index.html must mention {public_term}")

    catalog = json.loads((ROOT / "agent-system" / "catalog" / "repo-tool-library.json").read_text(encoding="utf-8"))
    required_catalog_ids = {"withastro-flue", "paddlepaddle-paddleocr", "panniantong-agent-reach"}
    actual_catalog_ids = {item.get("id") for item in catalog.get("items", [])}
    missing_catalog_ids = required_catalog_ids - actual_catalog_ids
    if missing_catalog_ids:
        fail(f"repo/tool catalog missing ids: {sorted(missing_catalog_ids)}")
    for item in catalog.get("items", []):
        if item.get("status") == "integrated":
            fail(f"catalog item must not be integrated by default: {item.get('id')}")
        if item.get("selected_for_projects"):
            fail(f"catalog item must not be selected for a project by default: {item.get('id')}")


    independent_review = json.loads((ROOT / "agent-system" / "templates" / "independent-review-summary.template.json").read_text(encoding="utf-8"))
    if independent_review.get("independent_execution") is not False:
        fail("independent review template must default independent_execution to false")
    sample_review = independent_review.get("reviews", [{}])[0]
    if sample_review.get("independent") is not False:
        fail("independent review item must default independent to false")
    required_provenance = {"subagent_run_id", "parent_workflow_run_id", "runtime", "prompt_hash", "context_pack_ref", "context_hash", "trace_ref", "result_ref", "evidence_refs"}
    missing_provenance = required_provenance - set(sample_review)
    if missing_provenance:
        fail(f"independent review template missing provenance fields: {sorted(missing_provenance)}")

    delegation = json.loads((ROOT / "agent-system" / "templates" / "subagent-delegation-plan.template.json").read_text(encoding="utf-8"))
    if delegation.get("budgets", {}).get("max_depth") != 1:
        fail("subagent delegation template must default max_depth to 1")
    if delegation.get("write_isolation", {}).get("shared_mutable_checkout_forbidden") is not True:
        fail("subagent delegation template must forbid shared mutable checkout")

    task_contract = json.loads((ROOT / "agent-system" / "templates" / "subagent-task-contract.template.json").read_text(encoding="utf-8"))
    if task_contract.get("context", {}).get("full_artifact_load_requires_reason") is not True:
        fail("subagent task contract must require a reason for full artifact loads")
    if task_contract.get("failure_policy", {}).get("cancellation_propagates_to_descendants") is not True:
        fail("subagent task contract must propagate cancellation to descendants")

    role_registry = json.loads((ROOT / "agent-system" / "templates" / "subagent-role-registry.template.json").read_text(encoding="utf-8"))
    if role_registry.get("roles", [{}])[0].get("delegation", {}).get("max_depth") != 1:
        fail("subagent role registry must default max_depth to 1")

    subagent_eval_path = ROOT / "agent-system" / "templates" / "subagent-eval-lab.template.yaml"
    subagent_eval = parse_yaml(subagent_eval_path, "agent-system/templates/subagent-eval-lab.template.yaml")
    required_families = set(subagent_eval.get("required_case_families", []))
    covered_families = {case.get("family") for case in subagent_eval.get("cases", [])}
    missing_families = required_families - covered_families
    if missing_families:
        fail(f"subagent eval lab missing case families: {sorted(missing_families)}")

    ledger_path = ROOT / "agent-system" / "templates" / "subagent-run-ledger.template.jsonl"
    for line_number, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            try:
                json.loads(line)
            except Exception as exc:
                fail(f"invalid JSONL in subagent run ledger line {line_number}: {exc}")

    for path in ROOT.rglob("*"):
        rel_path = path.relative_to(ROOT)
        rel = rel_path.as_posix()
        parts = set(rel_path.parts)
        if parts & FORBIDDEN_PARTS:
            fail(f"forbidden path present: {rel}")
        if path.is_file() and path.name.lower() in FORBIDDEN_SECRET_FILENAMES:
            fail(f"forbidden secret-bearing filename present: {rel}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SECRET_SUFFIXES:
            fail(f"forbidden secret-bearing suffix present: {rel}")
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
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    fail(f"possible {label} in {rel}")
        if path.is_file() and path.suffix.lower() == ".json":
            parse_json(path, rel)
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml"}:
            parse_yaml(path, rel)
        if path.is_file() and path.suffix.lower() == ".py":
            parse_python(path, rel)

    print("PASS: public package verification succeeded")


if __name__ == "__main__":
    main()
