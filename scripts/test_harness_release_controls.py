from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_harness_release.py"
GATES = [
    "agent_ir", "harness_boundary", "permission_policy", "trigger_lab",
    "eval_validity", "output_eval", "trajectory_safety",
    "assumption_ablation", "target_conformance", "trust", "package",
    "install", "independent_review",
]
REVIEW_IDS = [
    "first-run-onboarding", "happy-path-full-run",
    "missing-input-or-permission", "direct-skill-or-narrow-workflow",
    "handoff-export-install", "memory-state-living-adaptation",
    "consistency-routing-auditor", "modern-agent-system-auditor",
    "export-boundary-auditor", "claim-boundary-auditor",
]
HASH = "a" * 64


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, value: object) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def proof_refs() -> dict:
    return {"proof": "proof"}


def build_fixture(root: Path) -> dict[str, Path]:
    root.mkdir(parents=True, exist_ok=True)
    release_id = "release-test"
    proof = root / "proof.json"
    write_json(proof, {"status": "pass"})
    runtime_archive = root / "runtime.zip"
    with zipfile.ZipFile(runtime_archive, "w") as archive:
        archive.writestr("AGENTS.md", "# Runtime\n")
    trial_paths = []
    for index in range(1, 4):
        trial_path = root / f"trial-{index}.json"
        write_json(trial_path, {"trial_id": index, "status": "pass"})
        trial_paths.append(trial_path)
    policy = {
        "schema_version": 2,
        "policy_id": "policy-test",
        "system_release_id": release_id,
        "default_decision": "deny",
        "enforcement": {
            "runtime_native": True,
            "enforcer_ref": "proof",
            "metadata_only_fallback": False,
            "deny_by_default_test_ref": "proof",
        },
        "risk_dimensions": ["reversibility"],
        "no_grants_reason": "This fixture performs no tool calls.",
        "grants": [],
        "approval_binding": {
            "required_fields": [
                "tool_call_id", "principal_id", "operation", "resource",
                "normalized_arguments_hash", "resource_version", "risk_class",
                "budget_ref", "issued_at", "expires_at",
            ],
            "reuse_after_argument_change_forbidden": True,
            "reuse_after_resource_change_forbidden": True,
            "expired_or_revoked_approval_forbidden": True,
            "metadata_only_approval_for_high_risk_forbidden": True,
        },
        "data_flow": {
            "trusted_control_sources": [],
            "untrusted_data_sources": [],
            "allowed_sinks": [],
            "no_data_flow_reason": "No tool or external data flow in fixture.",
            "provenance_required": True,
            "untrusted_data_may_expand_authority": False,
            "untrusted_data_may_modify_policy": False,
        },
        "status": "pass",
        "evidence_refs": ["proof"],
        "blockers": [],
    }
    policy_path = root / "permission.json"
    write_json(policy_path, policy)
    boundary = {
        "schema_version": 2,
        "system_release_id": release_id,
        "system_identity": {
            "model_snapshot": "model-test",
            "reasoning_configuration": "fixed",
            "harness_commit": "commit-test",
            "agent_ir_hash": HASH,
            "instructions_hash": HASH,
            "tool_registry_hash": HASH,
            "permission_policy_hash": sha(policy_path),
            "runtime_image_hash": HASH,
            "dependency_lock_hash": HASH,
            "grader_hash": HASH,
        },
        "interfaces": {
            "session": {
                "append_only_event_log": True,
                "persistence_ref": "proof",
                "state_revision_scheme": "integer",
                "resume_contract_ref": "proof",
            },
            "harness": {
                "state_externalized": True,
                "policy_enforcement_outside_model": True,
                "crash_recovery_ref": "proof",
                "version_migration_ref": "proof",
            },
            "sandbox": {
                "disposable": True,
                "provision_recipe_ref": "proof",
                "process_boundary_ref": "proof",
                "filesystem_policy_ref": "proof",
                "network_policy_ref": "proof",
                "resource_profile_ref": "proof",
                "workspace_mount_modes": [
                    {"path_alias": "workspace", "mode": "read_write", "purpose": "fixture"}
                ],
                "cleanup_verification_ref": "proof",
            },
            "artifact_store": {
                "outside_ephemeral_compute": True,
                "immutable_evidence": True,
                "artifact_manifest_ref": "proof",
                "retention_policy_ref": "proof",
            },
            "credential_broker": {
                "credentials_enter_sandbox": False,
                "broker_or_proxy_ref": "proof",
                "principal_scope_ref": "proof",
                "short_lived_credentials": True,
                "revocation_test_ref": "proof",
            },
        },
        "trust_boundary": {
            "project_config_loaded_after_trust": True,
            "external_content_default": "untrusted_data",
            "control_data_separation": True,
            "provenance_propagation": True,
            "persistent_state_startup_scan_ref": "proof",
            "symlink_resolution_before_path_check": True,
        },
        "authorization": {
            "deny_by_default": True,
            "permission_policy_ref": "proof",
            "approval_binding_ref": "proof",
            "runtime_enforcement_test_ref": "proof",
        },
        "egress": {"policy_model": "deny_all", "exfiltration_test_ref": "proof"},
        "recovery": {
            "durability_required": False,
            "not_applicable_reason": "Bounded synchronous fixture.",
            "not_applicable_criteria": {
                "workflow_max_runtime_minutes": 1,
                "no_async_side_effects": True,
                "no_external_effects_after_response": True,
            },
        },
        "time_and_async_semantics": {
            "clock_source": "runtime",
            "deadline_policy_ref": "proof",
            "async_events_supported": False,
            "replay_supported": False,
            "deterministic_replay_ref": "",
        },
        "budget_limits": {
            "max_steps": 10,
            "max_tool_calls": 1,
            "max_runtime_ms": 1000,
            "max_input_tokens": 100,
            "max_output_tokens": 100,
            "max_cost": 1,
        },
        "status": "pass",
        "evidence_refs": ["proof"],
        "blockers": [],
        "warnings": [],
    }
    boundary_path = root / "boundary.json"
    write_json(boundary_path, boundary)
    ledger = {
        "schema_version": 3,
        "ledger_id": "ledger-test",
        "system_release_id": release_id,
        "approvals": [],
        "status": "pass",
        "blockers": [],
    }
    ledger_path = root / "approvals.json"
    write_json(ledger_path, ledger)
    registry = {
        "schema_version": 2,
        "registry_id": "registry-test",
        "system_release_id": release_id,
        "model_runtime_signature": "signature-test",
        "no_active_assumptions_reason": "No scaffold assumptions in fixture.",
        "assumptions": [],
        "status": "pass",
        "blockers": [],
        "warnings": [],
    }
    registry_path = root / "registry.json"
    write_json(registry_path, registry)
    ablation = {
        "version": 2,
        "lab_id": "ablation-test",
        "system_release_id": release_id,
        "system_identity_ref": "proof",
        "assumption_registry_ref": "registry-test",
        "trigger": "manual",
        "frozen_holdout_ref": "",
        "baseline": {},
        "cases": [],
        "release_rule": {
            "all_active_assumptions_covered": True,
            "pending_or_blocked_cases_fail_release": True,
            "retain_requires_measured_lift_or_deterministic_control": True,
            "safety_non_inferiority_required": True,
            "final_holdout_hidden_from_optimizer": True,
        },
        "result": {"status": "pass", "blockers": [], "warnings": []},
    }
    ablation_path = root / "ablation.yaml"
    write_yaml(ablation_path, ablation)
    validity = {
        "schema_version": 2,
        "report_id": "validity-test",
        "system_release_id": release_id,
        "eval_suite_id": "suite-test",
        "eval_suite_version": "1",
        "dataset_commit_or_hash": HASH,
        "claim_under_test": "bounded fixture claim",
        "task_distribution_ref": "proof",
        "task_inventory_ref": "proof",
        "task_disposition_ref": "proof",
        "source_task_count": 1,
        "disposition_count": 1,
        "counts_reconcile": True,
        "predeclared_exclusion_policy_ref": "proof",
        "holdout": {
            "split_ref": "proof",
            "frozen_before_tuning": True,
            "hidden_from_optimizer": True,
            "network_policy_ref": "proof",
            "answer_key_access_test_ref": "proof",
        },
        "task_quality": {
            "reference_solution_or_feasibility_witness_coverage": 1.0,
            "requirement_to_grader_map_ref": "proof",
            "hidden_test_coverage_ref": "proof",
            "mutation_test_ref": "proof",
            "ambiguity_review_ref": "proof",
            "contamination_probe_ref": "proof",
            "evaluation_awareness_probe_ref": "proof",
            "shortcut_and_leakage_probe_ref": "proof",
            "known_severe_defects": 0,
            "known_warning_defects": 0,
        },
        "grader_quality": {
            "deterministic_graders_ref": "proof",
            "model_judge_calibration_ref": "proof",
            "human_adjudication_ref": "proof",
            "confusion_matrix_ref": "proof",
            "inter_rater_agreement_ref": "proof",
            "llm_is_sole_safety_authority": False,
        },
        "independent_review": {
            "reviewer_provenance_ref": "proof",
            "blinded_to_system_identity": True,
            "sample_size": 1,
            "defect_rate_interval_ref": "proof",
        },
        "raw_intention_to_test_result_ref": "proof",
        "adjudicated_result_ref": "proof",
        "claim_eligible": True,
        "status": "pass",
        "blockers": [],
        "warnings": [],
    }
    validity_path = root / "validity.json"
    write_json(validity_path, validity)
    output = {
        "version": 3,
        "lab_id": "output-test",
        "system_release_id": release_id,
        "system_identity_ref": "proof",
        "eval_validity_ref": "validity-test",
        "suite_kind": "mixed",
        "task_distribution_ref": "proof",
        "dataset_split_hash": HASH,
        "baseline": {
            "description": "baseline",
            "system_identity_ref": "proof",
            "artifact_ref": "proof",
            "budgets_ref": "proof",
        },
        "with_agent": {
            "description": "candidate",
            "system_identity_ref": "proof",
            "artifact_ref": "proof",
            "budgets_ref": "proof",
        },
        "comparison": {
            "one_intervention_only": True,
            "matched_budgets": True,
            "matched_infrastructure": True,
            "matched_task_distribution": True,
            "improvement_claimed": False,
        },
        "trial_protocol": {
            "stochastic": True,
            "trials_per_task": 3,
            "clean_state_reset": True,
            "all_attempts_reported": True,
            "time_blocks": [],
            "deployment_attempt_policy": "single_attempt",
            "best_of_n_matches_deployment": True,
            "determinism_evidence_ref": "",
        },
        "infrastructure": {
            "profile_ref": "proof",
            "container_or_environment_hash": HASH,
            "cpu_floor": "1",
            "ram_floor": "1GB",
            "cpu_kill_ceiling": "2",
            "ram_kill_ceiling": "2GB",
            "timeout_policy_ref": "proof",
            "network_policy_ref": "proof",
            "cache_policy_ref": "proof",
            "concurrency": 1,
            "region_or_provider": "local",
            "aa_noise_calibration_ref": "proof",
            "infrastructure_errors_reported_separately": True,
        },
        "required_grader_families": ["outcome", "trajectory", "boundary", "stability"],
        "graders": {
            "outcome": {"deterministic_state_checks": ["state"]},
            "trajectory": {"required_events": ["run_started", "run_finished"], "verification_required": True},
            "boundary": {"permission_checks": ["deny-by-default"], "correct_answer_after_hidden_violation_must_fail": True},
            "stability": {"resource_limit_checks": ["budget"]},
            "model_judge": {"sole_safety_authority": False},
        },
        "metrics": {
            "pass_at_1": 1.0,
            "pass_at_k": 1.0,
            "pass_power_k_or_consistency": 1.0,
            "critical_failure_probability": 0.0,
            "confidence_interval_ref": "proof",
            "outcome_quality": 1.0,
            "trajectory_quality": 1.0,
            "boundary_violation_count": 0,
            "infrastructure_error_rate": 0.0,
            "median_latency_ms": 1,
            "p95_latency_ms": 1,
            "average_tokens": 1,
            "average_tool_calls": 0,
            "average_cost": 0,
        },
        "cases": [{
            "case_id": "case-1",
            "task_id": "task-1",
            "trial_result_refs": ["trial-1", "trial-2", "trial-3"],
            "outcome_status": "pass",
            "trajectory_status": "pass",
            "boundary_status": "pass",
            "stability_status": "pass",
            "infrastructure_failure": False,
            "evidence_refs": ["proof"],
        }],
        "result": {
            "status": "pass",
            "blockers": [],
            "warnings": [],
            "accepted_limitations": ["fixture does not claim improvement"],
            "critical_safety_violations": 0,
            "improvement_evidence_ref": "",
            "non_improvement_limit_ref": "proof",
        },
        "release_rule": {
            "eval_validity_must_pass": True,
            "all_required_grader_families_covered": True,
            "p0_boundary_violation_blocks_release": True,
            "quality_cannot_compensate_safety": True,
            "stochastic_claim_requires_repeated_trials": True,
            "best_of_n_claim_requires_matching_deployment": True,
            "with_agent_must_improve_or_record_limit": True,
        },
    }
    output_path = root / "output.yaml"
    write_yaml(output_path, output)
    identity = boundary["system_identity"]
    base_event = {
        "schema_version": 2,
        "timestamp": "2099-01-01T00:00:00Z",
        "trace_id": "trace-1",
        "span_id": "span-1",
        "parent_span_id": "",
        "workflow_run_id": "run-1",
        "attempt_id": "attempt-1",
        "actor": {"type": "runtime", "id": "runtime-1", "principal_id": "runtime-1"},
        "system_identity": {
            "system_release_id": release_id,
            "model_snapshot": identity["model_snapshot"],
            "harness_commit": identity["harness_commit"],
            "instructions_hash": identity["instructions_hash"],
            "tool_registry_hash": identity["tool_registry_hash"],
            "permission_policy_hash": identity["permission_policy_hash"],
        },
        "state": {"revision_before": "1", "revision_after": "1", "checkpoint_ref": ""},
        "intent_summary": "bounded fixture run",
        "tool": {},
        "permission": {},
        "effect": {"status": "none"},
        "budgets": {
            "step_delta": 0, "tool_call_delta": 0, "runtime_ms_delta": 1,
            "input_tokens_delta": 0, "output_tokens_delta": 0, "cost_delta": 0,
        },
        "provenance_refs": ["proof"],
        "artifact_refs": ["proof"],
        "sensitive_payload_omitted": True,
    }
    first = copy.deepcopy(base_event)
    first.update({"event_id": "event-1", "event_type": "run_started", "sequence": 0})
    second = copy.deepcopy(base_event)
    second.update({"event_id": "event-2", "event_type": "run_finished", "sequence": 1, "timestamp": "2099-01-01T00:00:01Z"})
    events_path = root / "events.jsonl"
    events_path.write_text(
        json.dumps(first) + "\n" + json.dumps(second) + "\n", encoding="utf-8"
    )
    gate_paths: dict[str, Path] = {}
    for gate in GATES:
        gate_path = root / f"gate-{gate}.json"
        write_json(gate_path, {
            "schema_version": 1,
            "evidence_id": f"gate-{gate}",
            "system_release_id": release_id,
            "gate_id": gate,
            "status": "pass",
            "verification_command": f"verify {gate}",
            "executed_at": "2099-01-01T00:00:00Z",
            "executor_provenance_ref": "proof",
            "artifact_refs": ["proof"],
            "blockers": [],
            "warnings": [],
        })
        gate_paths[gate] = gate_path
    for gate in ["package", "install"]:
        report = json.loads(gate_paths[gate].read_text(encoding="utf-8"))
        report.update({
            "runtime_archive_ref": "runtime-archive",
            "runtime_zip_name": "runtime.zip",
            "runtime_zip_sha256": sha(runtime_archive),
            "inventory_sha256": HASH,
            "entry_count": 1,
            "artifact_refs": ["runtime-archive"],
        })
        report["builder_sha256" if gate == "package" else "validator_sha256"] = HASH
        write_json(gate_paths[gate], report)
    independent_path = gate_paths["independent_review"]
    write_json(independent_path, {
        "schema_version": 3,
        "report_id": "independent-test",
        "system_release_id": release_id,
        "gate_id": "independent_review",
        "status": "pass",
        "completed_at": "2099-01-01T00:00:00Z",
        "independent_execution": True,
        "self_review_only": False,
        "required_review_ids": REVIEW_IDS,
        "reviews": [{
            "id": review_id,
            "kind": "scenario" if index < 6 else "clean-auditor",
            "reviewer_id": f"reviewer-{index}",
            "independent": True,
            "status": "pass",
            "inspected_files": ["runtime.zip"],
            "work_trace": ["inspect", "verify"],
            "confusion_points": [],
            "findings": [],
            "subagent_run_id": f"child-run-{index}",
            "parent_workflow_run_id": "parent-run",
            "role_id": f"role-{index}",
            "runtime": "fixture-runtime",
            "model": "fixture-model",
            "prompt_hash": HASH,
            "context_pack_ref": "proof",
            "context_hash": HASH,
            "tools": [],
            "permissions": [],
            "isolation_mode": "fresh-process",
            "trace_ref": "proof",
            "result_ref": "proof",
            "evidence_refs": ["proof"],
        } for index, review_id in enumerate(REVIEW_IDS)],
        "findings": [],
        "all_findings_dispositioned": True,
        "blockers": [],
        "warnings": [],
    })
    decision = {
        "schema_version": 2,
        "release_id": "decision-test",
        "maturity": "production",
        "system_release_id": release_id,
        "required_gates": GATES,
        "gate_results": [{
            "gate_id": gate,
            "status": "pass",
            "evidence_ref": f"gate-{gate}",
            "evidence_hash": sha(gate_paths[gate]),
            "source_fix_location": "",
            "verification_command": f"verify {gate}",
            "waiver_ref": "",
            "not_applicable_reason": "",
        } for gate in GATES],
        "reconciliation": {
            "all_required_gates_present": True,
            "all_evidence_refs_resolve": True,
            "pending_or_blocking_gates": [],
            "expired_waivers": [],
            "critical_safety_violations": 0,
            "quality_cannot_compensate_safety": True,
        },
        "allowed_claims": [{
            "claim": "bounded fixture claim",
            "supported_by_gate_ids": GATES,
        }],
        "forbidden_claims": [],
        "known_limits": ["fixture only"],
        "decision": "pass",
        "decided_by": "test-suite",
        "decided_at": "2099-01-01T00:00:00Z",
        "evidence_bundle_ref": "bundle-test",
    }
    decision_path = root / "decision.json"
    write_json(decision_path, decision)
    direct = {
        "boundary": boundary_path,
        "permission": policy_path,
        "registry": registry_path,
        "ablation": ablation_path,
        "validity": validity_path,
        "output": output_path,
        "events": events_path,
        "approvals": ledger_path,
        "decision": decision_path,
        "proof": proof,
        "runtime-archive": runtime_archive,
        "trial-1": trial_paths[0],
        "trial-2": trial_paths[1],
        "trial-3": trial_paths[2],
    }
    files = []
    for artifact_id, path in direct.items():
        kind = "run_log" if artifact_id == "events" else "approval" if artifact_id == "approvals" else "runtime_archive" if artifact_id == "runtime-archive" else "report"
        files.append({
            "artifact_id": artifact_id,
            "path": path.name,
            "sha256": sha(path),
            "kind": kind,
            "gate_ids": [],
            "row_count": None,
            "included_raw_body": False,
            "source": "test fixture",
            "immutable": True,
        })
    for gate, path in gate_paths.items():
        files.append({
            "artifact_id": f"gate-{gate}",
            "path": path.name,
            "sha256": sha(path),
            "kind": "package_validation" if gate == "package" else "install_validation" if gate == "install" else "independent_review" if gate == "independent_review" else "gate_evidence",
            "gate_ids": [gate],
            "row_count": None,
            "included_raw_body": False,
            "source": "test fixture",
            "immutable": True,
        })
    manifest_path = root / "evidence.json"
    write_json(manifest_path, {
        "schema_version": 2,
        "bundle_id": "bundle-test",
        "system_release_id": release_id,
        "created_at": "2099-01-01T00:00:00Z",
        "base_directory": ".",
        "hash_algorithm": "sha256",
        "claim_boundary": {"supports": ["bounded fixture claim"], "does_not_support": []},
        "files": files,
        "policy": {
            "reject_absolute_paths": True,
            "reject_parent_traversal": True,
            "reject_secrets": True,
            "reject_unapproved_private_data": True,
        },
    })
    direct["evidence"] = manifest_path
    return direct


def rehash_manifest(paths: dict[str, Path], changed: Path) -> None:
    manifest = json.loads(paths["evidence"].read_text(encoding="utf-8"))
    for item in manifest["files"]:
        if item["path"] == changed.name:
            item["sha256"] = sha(changed)
    write_json(paths["evidence"], manifest)


def command(paths: dict[str, Path]) -> list[str]:
    return [
        sys.executable, "-B", str(VALIDATOR),
        "--harness-boundary", str(paths["boundary"]),
        "--permission-policy", str(paths["permission"]),
        "--assumption-registry", str(paths["registry"]),
        "--ablation-lab", str(paths["ablation"]),
        "--eval-validity", str(paths["validity"]),
        "--output-eval", str(paths["output"]),
        "--run-events", str(paths["events"]),
        "--approval-ledger", str(paths["approvals"]),
        "--evidence-bundle", str(paths["evidence"]),
        "--release-decision", str(paths["decision"]),
    ]


class HarnessReleaseControlsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="harness-release-test-")
        self.paths = build_fixture(Path(self.temp.name))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(command(self.paths), capture_output=True, text=True)

    def mutate_json(self, key: str, edit) -> None:
        value = json.loads(self.paths[key].read_text(encoding="utf-8"))
        edit(value)
        write_json(self.paths[key], value)
        rehash_manifest(self.paths, self.paths[key])

    def mutate_yaml(self, key: str, edit) -> None:
        value = yaml.safe_load(self.paths[key].read_text(encoding="utf-8"))
        edit(value)
        write_yaml(self.paths[key], value)
        rehash_manifest(self.paths, self.paths[key])

    def add_tool_call(self, mismatch_resource: bool = False) -> None:
        policy = json.loads(self.paths["permission"].read_text(encoding="utf-8"))
        policy["no_grants_reason"] = ""
        policy["grants"] = [{
            "grant_id": "grant-1",
            "principal": "parent_agent",
            "principal_id": "agent-1",
            "tool_id": "read-source",
            "resource": "artifact:source-1",
            "operations": ["read"],
            "scope": ["artifact:source-1"],
            "conditions": [],
            "normalized_arguments_hash": HASH,
            "resource_version": "v1",
            "risk_class": "public_read",
            "budget_ref": "proof",
            "approval_required": False,
            "approval_ref": "",
            "issued_at": "2098-01-01T00:00:00Z",
            "expires_at": "2099-12-31T00:00:00Z",
            "revoked_at": "",
            "runtime_enforcement_ref": "proof",
        }]
        write_json(self.paths["permission"], policy)
        policy_hash = sha(self.paths["permission"])
        boundary = json.loads(self.paths["boundary"].read_text(encoding="utf-8"))
        boundary["system_identity"]["permission_policy_hash"] = policy_hash
        write_json(self.paths["boundary"], boundary)
        rows = [json.loads(line) for line in self.paths["events"].read_text(encoding="utf-8").splitlines()]
        start, finish = rows
        start["system_identity"]["permission_policy_hash"] = policy_hash
        finish["system_identity"]["permission_policy_hash"] = policy_hash
        tool = {
            "tool_call_id": "call-1",
            "tool_id": "read-source",
            "principal_id": "agent-1",
            "operation": "read",
            "resource": "artifact:other" if mismatch_resource else "artifact:source-1",
            "resource_version": "v1",
            "risk_class": "public_read",
            "budget_ref": "proof",
            "normalized_arguments_hash": HASH,
            "observation_ref": "proof",
        }
        events = [start]
        for offset, event_type, effect_status in [
            (1, "tool_proposed", "proposed"),
            (2, "permission_decided", "proposed"),
            (3, "tool_started", "started"),
            (4, "tool_observed", "committed"),
        ]:
            event = copy.deepcopy(start)
            event.update({
                "event_id": f"event-{offset + 1}",
                "event_type": event_type,
                "sequence": offset,
                "timestamp": f"2099-01-01T00:00:0{offset}Z",
                "tool": copy.deepcopy(tool),
                "effect": {"status": effect_status},
            })
            if event_type == "permission_decided":
                event["permission"] = {
                    "decision": "allow",
                    "grant_or_approval_ref": "grant-1",
                    "enforcement_ref": "proof",
                }
            if event_type == "tool_started":
                event["budgets"]["tool_call_delta"] = 1
            events.append(event)
        finish["event_id"] = "event-6"
        finish["sequence"] = 5
        finish["timestamp"] = "2099-01-01T00:00:05Z"
        events.append(finish)
        self.paths["events"].write_text(
            "\n".join(json.dumps(event) for event in events) + "\n",
            encoding="utf-8",
        )
        for changed in [self.paths["permission"], self.paths["boundary"], self.paths["events"]]:
            rehash_manifest(self.paths, changed)

    def assert_rejected(self, expected: str) -> None:
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(expected, result.stdout + result.stderr)

    def test_positive_fixture_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_exact_tool_authority_binding_passes(self) -> None:
        self.add_tool_call()
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_tool_authority_resource_mismatch_is_rejected(self) -> None:
        self.add_tool_call(mismatch_resource=True)
        self.assert_rejected("does not match authority: resource")

    def test_fake_independent_review_is_rejected(self) -> None:
        report_path = self.paths["evidence"].parent / "gate-independent_review.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["independent_execution"] = False
        write_json(report_path, report)
        decision = json.loads(self.paths["decision"].read_text(encoding="utf-8"))
        for gate in decision["gate_results"]:
            if gate["gate_id"] == "independent_review":
                gate["evidence_hash"] = sha(report_path)
        write_json(self.paths["decision"], decision)
        rehash_manifest(self.paths, report_path)
        rehash_manifest(self.paths, self.paths["decision"])
        self.assert_rejected("must prove independent_execution")

    def test_unresolved_blocker_is_rejected(self) -> None:
        self.mutate_json("validity", lambda value: value["blockers"].append("open"))
        self.assert_rejected("eval validity blockers")

    def test_invalid_gate_hash_is_rejected(self) -> None:
        self.mutate_json("decision", lambda value: value["gate_results"][0].update({"evidence_hash": "b" * 64}))
        self.assert_rejected("evidence hash mismatch")

    def test_reused_trial_evidence_is_rejected(self) -> None:
        self.mutate_yaml("output", lambda value: value["cases"][0].update({"trial_result_refs": ["trial-1", "trial-1", "trial-1"]}))
        self.assert_rejected("reuses a trial evidence ref")

    def test_null_stochastic_state_is_rejected(self) -> None:
        self.mutate_yaml("output", lambda value: value["trial_protocol"].update({"stochastic": None}))
        self.assert_rejected("stochastic must be boolean")

    def test_empty_trial_evidence_is_rejected(self) -> None:
        self.mutate_yaml("output", lambda value: value["cases"][0].update({"trial_result_refs": []}))
        self.assert_rejected("trial_result_refs")

    def test_not_applicable_gate_is_rejected(self) -> None:
        self.mutate_json("decision", lambda value: value["gate_results"][0].update({"status": "not_applicable"}))
        self.assert_rejected("must pass")

    def test_missing_gate_is_rejected(self) -> None:
        self.mutate_json("decision", lambda value: value["required_gates"].pop())
        self.assert_rejected("all 13 mandatory gates")

    def test_non_monotonic_run_sequence_is_rejected(self) -> None:
        rows = [json.loads(line) for line in self.paths["events"].read_text(encoding="utf-8").splitlines()]
        rows[1]["sequence"] = 0
        self.paths["events"].write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
        rehash_manifest(self.paths, self.paths["events"])
        self.assert_rejected("sequence is not contiguous")


if __name__ == "__main__":
    unittest.main()
