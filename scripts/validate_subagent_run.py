from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


TERMINAL_STATUSES = {
    "completed",
    "partial",
    "failed",
    "rejected",
    "timed_out",
    "budget_exhausted",
    "cancelled",
    "unknown_outcome",
}
WRITE_MODES = {"exact_paths", "worktree", "clone", "container", "external_resource"}
PROVENANCE_FIELDS = {
    "subagent_run_id",
    "parent_workflow_run_id",
    "reviewer_id",
    "runtime",
    "model",
    "prompt_hash",
    "context_pack_ref",
    "context_hash",
    "isolation_mode",
    "trace_ref",
    "result_ref",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path}")
    return value


def load_objects(directory: Path, label: str) -> dict[str, dict[str, Any]]:
    if not directory.is_dir():
        fail(f"{label} directory missing: {directory}")
    objects: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.json")):
        value = load_json(path)
        task_id = value.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            fail(f"{label} missing task_id: {path}")
        if task_id in objects:
            fail(f"duplicate {label} task_id: {task_id}")
        objects[task_id] = value
    return objects


def load_ledger(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except Exception as exc:
            fail(f"invalid ledger JSONL line {line_number}: {exc}")
        if not isinstance(entry, dict):
            fail(f"ledger line {line_number} is not an object")
        entries.append(entry)
    if not entries:
        fail("subagent run ledger is empty")
    return entries


def require_positive_budget(budgets: dict[str, Any], key: str, allow_zero: bool = False) -> None:
    value = budgets.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        fail(f"budget {key} must be a finite number")
    if value < 0 or (value == 0 and not allow_zero):
        fail(f"budget {key} must be {'non-negative' if allow_zero else 'positive'}")


def paths_overlap(left: str, right: str) -> bool:
    a = left.replace("\\", "/").strip("/")
    b = right.replace("\\", "/").strip("/")
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def validate_permissions(contract: dict[str, Any], task_id: str) -> None:
    envelope = contract.get("permission_envelope", {})
    required = {
        "parent_permission_snapshot_ref",
        "role_permission_ref",
        "task_permission_ref",
        "effective_policy",
    }
    missing = [key for key in required if not envelope.get(key)]
    if missing:
        fail(f"task {task_id} missing effective permission fields: {missing}")
    if envelope.get("effective_policy") != "intersection_no_privilege_amplification":
        fail(f"task {task_id} must use permission intersection without privilege amplification")


def validate_write_isolation(contracts: dict[str, dict[str, Any]], strategy: str) -> None:
    writable: list[tuple[str, dict[str, Any]]] = []
    for task_id, contract in contracts.items():
        ownership = contract.get("write_ownership", {})
        if ownership.get("mode") in WRITE_MODES:
            writable.append((task_id, ownership))

    if len(writable) > 1 and strategy not in {
        "disjoint_scopes", "worktrees", "clones", "containers", "sandbox", "serialized"
    }:
        fail("multiple write tasks require an explicit isolation strategy")

    for task_id, ownership in writable:
        process = ownership.get("process_isolation", {})
        required = {
            "process_boundary_ref",
            "environment_allowlist_ref",
            "temp_root",
            "cache_root",
            "credential_scope_ref",
            "cleanup_verification_ref",
        }
        missing = [key for key in required if not process.get(key)]
        if missing:
            fail(f"write task {task_id} missing process/credential isolation: {missing}")
        if ownership.get("mode") in {"worktree", "clone", "container"} and not ownership.get("isolation_ref"):
            fail(f"write task {task_id} missing isolation_ref")

    if strategy == "disjoint_scopes":
        for index, (left_id, left) in enumerate(writable):
            for right_id, right in writable[index + 1 :]:
                for left_scope in left.get("scopes", []):
                    for right_scope in right.get("scopes", []):
                        if paths_overlap(str(left_scope), str(right_scope)):
                            fail(f"overlapping write scopes: {left_id}:{left_scope} and {right_id}:{right_scope}")


def validate_independent_review(path: Path) -> None:
    summary = load_json(path)
    if summary.get("independent_execution") is not True:
        fail("independent review claim requires independent_execution=true in the filled run artifact")
    reviews = summary.get("reviews", [])
    ids = [item.get("id") for item in reviews]
    if len(ids) != len(set(ids)):
        fail("independent review ids must be unique")
    missing_ids = set(summary.get("required_review_ids", [])) - set(ids)
    if missing_ids:
        fail(f"independent review missing required ids: {sorted(missing_ids)}")
    for item in reviews:
        review_id = item.get("id", "<unknown>")
        if item.get("independent") is not True:
            fail(f"review {review_id} is not marked independent")
        missing = [key for key in PROVENANCE_FIELDS if not item.get(key)]
        if missing:
            fail(f"review {review_id} missing provenance: {sorted(missing)}")
        if not item.get("evidence_refs"):
            fail(f"review {review_id} has no evidence refs")


def validate_done_invariants(loop_state_path: Path | None, stage_gates_path: Path | None) -> None:
    if loop_state_path:
        state = load_json(loop_state_path)
        if state.get("status") == "done":
            if state.get("active_child_runs"):
                fail("loop cannot be done with active child runs")
            if state.get("merge_verdict") not in {"pass", "not_applicable"}:
                fail("loop cannot be done without a passing merge verdict")
            if state.get("child_reconciliation_status") != "pass":
                fail("loop cannot be done without child reconciliation pass")
    if stage_gates_path:
        gates = load_json(stage_gates_path)
        for stage in gates.get("stages", []):
            if stage.get("status") == "done" and stage.get("quality_verdict") not in {"pass", "warn"}:
                fail(f"stage {stage.get('stage')} is done with non-passing quality verdict")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a filled subagent orchestration run.")
    parser.add_argument("--role-registry", type=Path, required=True)
    parser.add_argument("--delegation-plan", type=Path, required=True)
    parser.add_argument("--tasks-dir", type=Path, required=True)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--independent-review", type=Path)
    parser.add_argument("--loop-state", type=Path)
    parser.add_argument("--stage-gates", type=Path)
    args = parser.parse_args()

    registry = load_json(args.role_registry)
    role_ids = [item.get("role_id") for item in registry.get("roles", [])]
    if not role_ids or any(not item for item in role_ids) or len(role_ids) != len(set(role_ids)):
        fail("role registry must contain unique non-empty role ids")

    plan = load_json(args.delegation_plan)
    topology = plan.get("topology")
    if not topology or "|" in str(topology):
        fail("delegation plan topology must be resolved")
    budgets = plan.get("budgets", {})
    for key in ["max_workers", "max_total_runtime_minutes", "max_total_tokens", "max_total_tool_calls"]:
        require_positive_budget(budgets, key)
    for key in ["max_total_cost", "max_retries", "reserved_synthesis_and_verification_budget"]:
        require_positive_budget(budgets, key, allow_zero=True)
    require_positive_budget(budgets, "max_depth", allow_zero=True)
    if budgets.get("max_depth", 0) > 1 and not plan.get("recursive_delegation_justification"):
        fail("delegation depth above one requires recursive_delegation_justification")

    tasks = plan.get("tasks", [])
    task_ids = [item.get("task_id") for item in tasks]
    if topology != "single_agent" and not task_ids:
        fail("multi-agent topology requires tasks")
    if any(not item for item in task_ids) or len(task_ids) != len(set(task_ids)):
        fail("delegation tasks must have unique non-empty ids")
    task_set = set(task_ids)
    for item in tasks:
        unknown = set(item.get("depends_on", [])) - task_set
        if unknown:
            fail(f"task {item.get('task_id')} has unknown dependencies: {sorted(unknown)}")
        if item.get("role_id") not in role_ids:
            fail(f"task {item.get('task_id')} uses unknown role {item.get('role_id')}")

    contracts = load_objects(args.tasks_dir, "task contract")
    results = load_objects(args.results_dir, "subagent result")
    if set(contracts) != task_set:
        fail(f"task contracts do not reconcile with plan: expected {sorted(task_set)}, got {sorted(contracts)}")
    if set(results) != task_set:
        fail(f"results do not reconcile with plan: expected {sorted(task_set)}, got {sorted(results)}")

    for task_id, contract in contracts.items():
        validate_permissions(contract, task_id)
    validate_write_isolation(contracts, plan.get("write_isolation", {}).get("strategy", ""))

    for task_id, result in results.items():
        if result.get("status") not in TERMINAL_STATUSES or result.get("terminal") is not True:
            fail(f"task {task_id} has no terminal result")
        if result.get("status") == "unknown_outcome" and not result.get("reconciliation_artifact_ref"):
            fail(f"task {task_id} unknown outcome requires reconciliation artifact")
        if result.get("validation_status") not in {"accepted", "rejected"}:
            fail(f"task {task_id} missing validation status")

    ledger = load_ledger(args.ledger)
    ledger_tasks = {item.get("task_id") for item in ledger if item.get("status") in TERMINAL_STATUSES}
    if ledger_tasks != task_set:
        fail(f"terminal ledger tasks do not reconcile: expected {sorted(task_set)}, got {sorted(ledger_tasks)}")
    for entry in ledger:
        required = {
            "subagent_run_id", "task_id", "runtime", "model", "prompt_hash", "context_hash",
            "effective_permission_ref", "trace_ref", "result_ref", "attempt_id"
        }
        missing = [key for key in required if not entry.get(key)]
        if missing:
            fail(f"ledger entry missing provenance: {sorted(missing)}")

    if args.independent_review:
        validate_independent_review(args.independent_review)
    validate_done_invariants(args.loop_state, args.stage_gates)
    print("PASS: filled subagent orchestration run is internally consistent")


if __name__ == "__main__":
    main()
