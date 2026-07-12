from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None


GRADER_FAMILIES = {"outcome", "trajectory", "boundary", "stability"}
RELEASE_GATES = {
    "agent_ir", "harness_boundary", "permission_policy", "trigger_lab",
    "eval_validity", "output_eval", "trajectory_safety",
    "assumption_ablation", "target_conformance", "trust", "package",
    "install", "independent_review",
}
INDEPENDENT_REVIEW_IDS = {
    "first-run-onboarding", "happy-path-full-run",
    "missing-input-or-permission", "direct-skill-or-narrow-workflow",
    "handoff-export-install", "memory-state-living-adaptation",
    "consistency-routing-auditor", "modern-agent-system-auditor",
    "export-boundary-auditor", "claim-boundary-auditor",
}
PRINCIPALS = {"user", "parent_agent", "subagent", "tool", "automation"}
RISK_CLASSES = {
    "public_read", "private_read", "local_draft", "local_write",
    "internal_write", "external_write", "financial", "legal", "health",
    "security_sensitive", "destructive", "privileged",
}
APPROVAL_RISKS = {
    "internal_write", "external_write", "financial", "legal", "health",
    "security_sensitive", "destructive", "privileged",
}
APPROVAL_FIELDS = {
    "tool_call_id", "principal_id", "operation", "resource",
    "normalized_arguments_hash", "resource_version", "risk_class",
    "budget_ref", "issued_at", "expires_at",
}
EVENT_TYPES = {
    "run_started", "state_read", "context_built", "model_called",
    "tool_proposed", "permission_decided", "tool_started", "tool_observed",
    "artifact_written", "subagent_started", "inter_agent_transfer",
    "subagent_finished", "checkpoint_written", "cancel_requested",
    "effect_reconciled", "cleanup_finished", "run_finished",
}
TOOL_EVENTS = {
    "tool_proposed", "permission_decided", "tool_started", "tool_observed",
    "effect_reconciled",
}
HASH_RE = re.compile(r"^[0-9a-fA-F]{64}$")
BROAD = {"*", "all", "any", "/", "\\", "root", "workspace_root"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=unique_object
        )
    except Exception as exc:
        fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    try:
        for line_no, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not line.strip():
                continue
            value = json.loads(line, object_pairs_hook=unique_object)
            if not isinstance(value, dict):
                fail(f"expected object in {path} line {line_no}")
            values.append(value)
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"invalid JSONL in {path}: {exc}")
    return values


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        fail("PyYAML is required; install requirements-dev.txt")

    class UniqueLoader(yaml.SafeLoader):
        pass

    def construct(loader: Any, node: Any, deep: bool = False) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError(f"duplicate key: {key}")
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct
    )
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    except Exception as exc:
        fail(f"invalid YAML in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected YAML mapping in {path}")
    return value


def required(record: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if record.get(field) in (None, "", [])]
    if missing:
        fail(f"{label} missing values: {missing}")


def all_true(record: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if record.get(field) is not True]
    if missing:
        fail(f"{label} must prove true: {missing}")


def empty(value: Any, label: str) -> None:
    if value not in (None, "", []):
        fail(f"{label} must be empty for a final pass")


def digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or not HASH_RE.fullmatch(value):
        fail(f"{label} must be a SHA-256 digest")
    return value.lower()


def number(value: Any, low: float = 0, high: float | None = None) -> bool:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value < low
    ):
        return False
    return high is None or value <= high


def timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(f"{label} must be an ISO-8601 timestamp")
    if parsed.tzinfo is None:
        fail(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def file_hash(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


class Evidence:
    def __init__(self, manifest_path: Path, release_id: str) -> None:
        self.path = manifest_path.resolve()
        self.data = load_json(self.path)
        if self.data.get("schema_version") != 2:
            fail("evidence bundle must use schema_version 2")
        required(
            self.data,
            ["bundle_id", "system_release_id", "created_at", "base_directory"],
            "evidence bundle",
        )
        if self.data["system_release_id"] != release_id:
            fail("evidence bundle system_release_id mismatch")
        if self.data.get("hash_algorithm") != "sha256":
            fail("evidence bundle must use sha256")
        timestamp(self.data["created_at"], "evidence bundle created_at")
        all_true(
            self.data.get("policy", {}),
            [
                "reject_absolute_paths", "reject_parent_traversal",
                "reject_secrets", "reject_unapproved_private_data",
            ],
            "evidence bundle policy",
        )
        raw_base = str(self.data["base_directory"]).replace("\\", "/")
        pure_base = PurePosixPath(raw_base)
        if pure_base.is_absolute() or ".." in pure_base.parts:
            fail("evidence base_directory must be relative and confined")
        self.base = (self.path.parent / Path(*pure_base.parts)).resolve()
        try:
            self.base.relative_to(self.path.parent.resolve())
        except ValueError:
            fail("evidence base_directory escapes its manifest directory")
        self.by_id: dict[str, dict[str, Any]] = {}
        self.by_path: dict[Path, dict[str, Any]] = {}
        files = self.data.get("files")
        if not isinstance(files, list) or not files:
            fail("evidence bundle must list files")
        for index, item in enumerate(files):
            if not isinstance(item, dict):
                fail(f"evidence file {index} must be an object")
            required(
                item, ["artifact_id", "path", "sha256", "kind", "source"],
                f"evidence file {index}",
            )
            artifact_id = str(item["artifact_id"])
            if artifact_id in self.by_id:
                fail(f"duplicate evidence artifact_id: {artifact_id}")
            raw_path = str(item["path"])
            if "\\" in raw_path:
                fail(f"evidence path must use forward slashes: {raw_path}")
            rel = PurePosixPath(raw_path)
            if rel.is_absolute() or ".." in rel.parts or not rel.parts:
                fail(f"evidence path is not confined: {raw_path}")
            resolved = (self.base / Path(*rel.parts)).resolve()
            try:
                resolved.relative_to(self.base)
            except ValueError:
                fail(f"evidence path escapes bundle base: {raw_path}")
            if resolved in self.by_path or not resolved.is_file():
                fail(f"duplicate or missing evidence path: {raw_path}")
            actual = file_hash(resolved)
            if digest(item["sha256"], artifact_id) != actual:
                fail(f"evidence hash mismatch: {artifact_id}")
            if item.get("immutable") is not True:
                fail(f"evidence {artifact_id} must be marked immutable")
            if not isinstance(item.get("gate_ids", []), list):
                fail(f"evidence {artifact_id} gate_ids must be a list")
            stored = dict(item)
            stored["resolved_path"] = resolved
            self.by_id[artifact_id] = stored
            self.by_path[resolved] = stored

    @property
    def bundle_id(self) -> str:
        return str(self.data["bundle_id"])

    def get(
        self, artifact_id: Any, label: str, kinds: set[str] | None = None
    ) -> dict[str, Any]:
        if not isinstance(artifact_id, str) or artifact_id not in self.by_id:
            fail(f"{label} does not resolve in evidence bundle: {artifact_id}")
        item = self.by_id[artifact_id]
        if kinds is not None and item.get("kind") not in kinds:
            fail(f"{label} has invalid evidence kind: {item.get('kind')}")
        return item

    def has_path(
        self, path: Path, label: str, kinds: set[str] | None = None
    ) -> dict[str, Any]:
        item = self.by_path.get(path.resolve())
        if item is None:
            fail(f"{label} is not listed in evidence bundle")
        if kinds is not None and item.get("kind") not in kinds:
            fail(f"{label} has invalid evidence kind")
        return item


def refs(
    evidence: Evidence, record: dict[str, Any], fields: list[str], label: str
) -> None:
    for field in fields:
        evidence.get(record.get(field), f"{label}.{field}")


def validate_boundary(
    boundary: dict[str, Any], evidence: Evidence, policy_path: Path
) -> tuple[str, dict[str, Any]]:
    if boundary.get("schema_version") != 2:
        fail("harness boundary must use schema_version 2")
    release_id = boundary.get("system_release_id")
    if not release_id:
        fail("harness boundary missing system_release_id")
    identity = boundary.get("system_identity", {})
    required(
        identity,
        [
            "model_snapshot", "reasoning_configuration", "harness_commit",
            "agent_ir_hash", "instructions_hash", "tool_registry_hash",
            "permission_policy_hash", "runtime_image_hash",
            "dependency_lock_hash", "grader_hash",
        ],
        "system identity",
    )
    for field in [
        "agent_ir_hash", "instructions_hash", "tool_registry_hash",
        "permission_policy_hash", "runtime_image_hash", "dependency_lock_hash",
        "grader_hash",
    ]:
        digest(identity[field], f"system identity {field}")
    if identity["permission_policy_hash"].lower() != file_hash(policy_path.resolve()):
        fail("permission_policy_hash does not match permission policy file")

    interfaces = boundary.get("interfaces", {})
    session = interfaces.get("session", {})
    all_true(session, ["append_only_event_log"], "session")
    required(session, ["state_revision_scheme"], "session")
    refs(evidence, session, ["persistence_ref", "resume_contract_ref"], "session")
    harness = interfaces.get("harness", {})
    all_true(
        harness, ["state_externalized", "policy_enforcement_outside_model"],
        "harness",
    )
    refs(
        evidence, harness, ["crash_recovery_ref", "version_migration_ref"],
        "harness",
    )
    sandbox = interfaces.get("sandbox", {})
    all_true(sandbox, ["disposable"], "sandbox")
    refs(
        evidence,
        sandbox,
        [
            "provision_recipe_ref", "process_boundary_ref",
            "filesystem_policy_ref", "network_policy_ref",
            "resource_profile_ref", "cleanup_verification_ref",
        ],
        "sandbox",
    )
    mounts = sandbox.get("workspace_mount_modes")
    if not isinstance(mounts, list) or not mounts:
        fail("sandbox needs bounded workspace mounts")
    for index, mount in enumerate(mounts):
        if not isinstance(mount, dict):
            fail(f"workspace mount {index} must be an object")
        required(mount, ["path_alias", "mode", "purpose"], f"mount {index}")
        alias = str(mount["path_alias"]).lower()
        if (
            alias in BROAD
            or any(token in alias for token in ("*", "..", ":", "\\", "/"))
            or mount["mode"] not in {"read_only", "read_write"}
        ):
            fail(f"workspace mount {index} is broad or invalid")
    artifacts = interfaces.get("artifact_store", {})
    all_true(
        artifacts, ["outside_ephemeral_compute", "immutable_evidence"],
        "artifact store",
    )
    refs(
        evidence, artifacts, ["artifact_manifest_ref", "retention_policy_ref"],
        "artifact store",
    )
    credentials = interfaces.get("credential_broker", {})
    if credentials.get("credentials_enter_sandbox") is not False:
        fail("durable credentials must not enter the sandbox")
    all_true(credentials, ["short_lived_credentials"], "credential broker")
    refs(
        evidence,
        credentials,
        ["broker_or_proxy_ref", "principal_scope_ref", "revocation_test_ref"],
        "credential broker",
    )
    trust = boundary.get("trust_boundary", {})
    all_true(
        trust,
        [
            "project_config_loaded_after_trust", "control_data_separation",
            "provenance_propagation", "symlink_resolution_before_path_check",
        ],
        "trust boundary",
    )
    if trust.get("external_content_default") != "untrusted_data":
        fail("external content must default to untrusted_data")
    refs(evidence, trust, ["persistent_state_startup_scan_ref"], "trust boundary")
    auth = boundary.get("authorization", {})
    all_true(auth, ["deny_by_default"], "authorization")
    refs(
        evidence, auth,
        ["permission_policy_ref", "approval_binding_ref", "runtime_enforcement_test_ref"],
        "authorization",
    )
    egress = boundary.get("egress", {})
    if egress.get("policy_model") not in {"capability_grant", "deny_all"}:
        fail("egress must use capability_grant or deny_all")
    refs(evidence, egress, ["exfiltration_test_ref"], "egress")
    if egress["policy_model"] == "capability_grant":
        refs(
            evidence, egress,
            ["allowed_operations_ref", "allowed_principals_ref", "data_sink_policy_ref"],
            "egress",
        )
    recovery = boundary.get("recovery", {})
    if recovery.get("durability_required") is True:
        all_true(recovery, ["checkpoint_supported", "rehydration_supported"], "recovery")
        refs(
            evidence, recovery,
            [
                "sandbox_loss_drill_ref", "harness_loss_drill_ref",
                "unknown_effect_reconciliation_ref",
            ],
            "recovery",
        )
    elif recovery.get("durability_required") is False:
        required(recovery, ["not_applicable_reason"], "recovery")
        criteria = recovery.get("not_applicable_criteria", {})
        if not number(criteria.get("workflow_max_runtime_minutes")):
            fail("recovery not-applicable criteria need bounded runtime")
        all_true(
            criteria,
            ["no_async_side_effects", "no_external_effects_after_response"],
            "recovery not-applicable criteria",
        )
    else:
        fail("recovery.durability_required must be boolean")
    timing = boundary.get("time_and_async_semantics", {})
    required(timing, ["clock_source"], "time semantics")
    refs(evidence, timing, ["deadline_policy_ref"], "time semantics")
    if not isinstance(timing.get("async_events_supported"), bool):
        fail("async_events_supported must be boolean")
    if timing["async_events_supported"]:
        all_true(timing, ["replay_supported"], "async semantics")
        refs(evidence, timing, ["deterministic_replay_ref"], "async semantics")
    for field, value in boundary.get("budget_limits", {}).items():
        if field.startswith("max_") and not number(value):
            fail(f"budget limit {field} is invalid")
    expected_limits = {
        "max_steps", "max_tool_calls", "max_runtime_ms", "max_input_tokens",
        "max_output_tokens", "max_cost",
    }
    if set(boundary.get("budget_limits", {})) != expected_limits:
        fail("harness boundary budget_limits are incomplete")
    if boundary.get("status") != "pass":
        fail("harness boundary status must be pass")
    empty(boundary.get("blockers"), "harness boundary blockers")
    empty(boundary.get("warnings"), "harness boundary warnings")
    for ref in boundary.get("evidence_refs", []):
        evidence.get(ref, "harness boundary evidence")
    return str(release_id), identity


def validate_approvals(
    ledger: dict[str, Any], evidence: Evidence, release_id: str
) -> dict[str, dict[str, Any]]:
    if ledger.get("schema_version") != 3:
        fail("approval ledger must use schema_version 3")
    if ledger.get("system_release_id") != release_id:
        fail("approval ledger system_release_id mismatch")
    required(ledger, ["ledger_id"], "approval ledger")
    if ledger.get("status") != "pass":
        fail("approval ledger status must be pass")
    empty(ledger.get("blockers"), "approval ledger blockers")
    rows = ledger.get("approvals")
    if not isinstance(rows, list):
        fail("approval ledger approvals must be a list")
    result: dict[str, dict[str, Any]] = {}
    now = datetime.now(timezone.utc)
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            fail(f"approval {index} must be an object")
        required(
            row,
            [
                "approval_id", "action_id", "risk_class", "principal_id",
                "provider_or_runtime", "tool_id", "operation", "resource",
                "resource_version", "normalized_arguments_hash", "scope", "budget_ref",
                "approved_by", "reviewer_identity_ref", "approval_ref",
                "approved_at", "expires_at", "tool_call_id", "idempotency_key",
                "effective_permission_ref", "evidence_refs",
            ],
            f"approval {index}",
        )
        approval_id = str(row["approval_id"])
        if approval_id in result:
            fail(f"duplicate approval_id: {approval_id}")
        digest(row["normalized_arguments_hash"], f"approval {approval_id} arguments")
        if row.get("decision") not in {"approved", "consumed"} or row.get("revoked_at"):
            fail(f"approval {approval_id} is not active evidence")
        issued = timestamp(row["approved_at"], f"approval {approval_id} approved_at")
        expires = timestamp(row["expires_at"], f"approval {approval_id} expires_at")
        if issued >= expires or expires <= now:
            fail(f"approval {approval_id} is expired or malformed")
        if not isinstance(row.get("item_count"), int) or row["item_count"] <= 0:
            fail(f"approval {approval_id} needs positive item_count")
        scope = row["scope"]
        if (
            not isinstance(scope, list)
            or not scope
            or any(not isinstance(item, str) or not item for item in scope)
            or any(item.lower() in BROAD or "*" in item for item in scope)
        ):
            fail(f"approval {approval_id} needs exact bounded scope")
        refs(
            evidence, row,
            ["reviewer_identity_ref", "approval_ref", "effective_permission_ref", "budget_ref"],
            f"approval {approval_id}",
        )
        for ref in row["evidence_refs"]:
            evidence.get(ref, f"approval {approval_id} evidence")
        result[approval_id] = row
    return result


def validate_permissions(
    policy: dict[str, Any], evidence: Evidence, release_id: str,
    approvals: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    if policy.get("schema_version") != 2:
        fail("permission policy must use schema_version 2")
    if policy.get("system_release_id") != release_id:
        fail("permission policy system_release_id mismatch")
    required(policy, ["policy_id"], "permission policy")
    if policy.get("default_decision") != "deny":
        fail("permission policy must default deny")
    enforcement = policy.get("enforcement", {})
    all_true(enforcement, ["runtime_native"], "permission enforcement")
    if enforcement.get("metadata_only_fallback") is not False:
        fail("metadata-only permission fallback cannot pass")
    refs(
        evidence, enforcement, ["enforcer_ref", "deny_by_default_test_ref"],
        "permission enforcement",
    )
    binding = policy.get("approval_binding", {})
    if set(binding.get("required_fields", [])) != APPROVAL_FIELDS:
        fail("approval binding fields do not match the exact action contract")
    all_true(
        binding,
        [
            "reuse_after_argument_change_forbidden",
            "reuse_after_resource_change_forbidden",
            "expired_or_revoked_approval_forbidden",
            "metadata_only_approval_for_high_risk_forbidden",
        ],
        "approval binding",
    )
    grants = policy.get("grants")
    if not isinstance(grants, list):
        fail("permission grants must be a list")
    if not grants and not policy.get("no_grants_reason"):
        fail("permission policy needs grants or no_grants_reason")
    if grants and policy.get("no_grants_reason"):
        fail("no_grants_reason conflicts with grants")
    now = datetime.now(timezone.utc)
    grant_ids: set[str] = set()
    grant_records: dict[str, dict[str, Any]] = {}
    used_approvals: set[str] = set()
    for index, grant in enumerate(grants):
        if not isinstance(grant, dict):
            fail(f"grant {index} must be an object")
        required(
            grant,
            [
                "grant_id", "principal", "principal_id", "tool_id", "resource",
                "operations", "scope", "normalized_arguments_hash",
                "resource_version", "risk_class", "budget_ref", "issued_at",
                "expires_at", "runtime_enforcement_ref",
            ],
            f"grant {index}",
        )
        grant_id = str(grant["grant_id"])
        if grant_id in grant_ids:
            fail(f"duplicate grant_id: {grant_id}")
        grant_ids.add(grant_id)
        grant_records[grant_id] = grant
        if grant["principal"] not in PRINCIPALS or grant["risk_class"] not in RISK_CLASSES:
            fail(f"grant {grant_id} has invalid principal or risk")
        operations, scope = grant["operations"], grant["scope"]
        values = [grant["tool_id"], grant["resource"]]
        if not isinstance(operations, list) or not isinstance(scope, list):
            fail(f"grant {grant_id} operations and scope must be lists")
        values.extend(operations)
        values.extend(scope)
        if (
            not operations or not scope
            or any(not isinstance(value, str) or not value for value in values)
            or any(value.lower() in BROAD or "*" in value for value in values)
        ):
            fail(f"grant {grant_id} has broad or blank authority")
        if len(operations) != 1:
            fail(f"grant {grant_id} must authorize one exact operation")
        digest(grant["normalized_arguments_hash"], f"grant {grant_id} arguments")
        if not isinstance(grant.get("approval_required"), bool):
            fail(f"grant {grant_id} approval_required must be boolean")
        if grant["risk_class"] in APPROVAL_RISKS and not grant["approval_required"]:
            fail(f"grant {grant_id} risk requires approval")
        issued = timestamp(grant["issued_at"], f"grant {grant_id} issued_at")
        expires = timestamp(grant["expires_at"], f"grant {grant_id} expires_at")
        if issued >= expires or expires <= now or grant.get("revoked_at"):
            fail(f"grant {grant_id} is expired, revoked, or malformed")
        refs(
            evidence, grant, ["budget_ref", "runtime_enforcement_ref"],
            f"grant {grant_id}",
        )
        if grant["approval_required"]:
            approval_id = grant.get("approval_ref")
            if len(operations) != 1 or approval_id not in approvals:
                fail(f"grant {grant_id} lacks one exact approval")
            approval = approvals[str(approval_id)]
            expected = {
                "principal_id": grant["principal_id"],
                "tool_id": grant["tool_id"],
                "operation": operations[0],
                "resource": grant["resource"],
                "resource_version": grant["resource_version"],
                "normalized_arguments_hash": grant["normalized_arguments_hash"],
                "risk_class": grant["risk_class"],
                "budget_ref": grant["budget_ref"],
            }
            for field, value in expected.items():
                if approval.get(field) != value:
                    fail(f"grant {grant_id} approval mismatch: {field}")
            used_approvals.add(str(approval_id))
        elif grant.get("approval_ref"):
            fail(f"grant {grant_id} has an unnecessary approval_ref")
    if set(approvals) != used_approvals:
        fail("approval ledger has orphaned or missing grant bindings")
    flow = policy.get("data_flow", {})
    all_true(flow, ["provenance_required"], "permission data flow")
    if (
        flow.get("untrusted_data_may_expand_authority") is not False
        or flow.get("untrusted_data_may_modify_policy") is not False
    ):
        fail("untrusted data may not expand authority or modify policy")
    lists = [
        flow.get("trusted_control_sources"), flow.get("untrusted_data_sources"),
        flow.get("allowed_sinks"),
    ]
    if all(value == [] for value in lists):
        required(flow, ["no_data_flow_reason"], "permission data flow")
    elif any(not isinstance(value, list) or not value for value in lists):
        fail("partial data-flow declaration cannot pass")
    elif flow.get("no_data_flow_reason"):
        fail("no_data_flow_reason conflicts with populated data-flow lists")
    if policy.get("status") != "pass":
        fail("permission policy status must pass")
    empty(policy.get("blockers"), "permission policy blockers")
    for ref in policy.get("evidence_refs", []):
        evidence.get(ref, "permission policy evidence")
    return grant_records, approvals


def validate_assumptions(
    registry: dict[str, Any], lab: dict[str, Any], evidence: Evidence,
    release_id: str,
) -> None:
    if registry.get("schema_version") != 2 or lab.get("version") != 2:
        fail("assumption registry and ablation lab must use version 2")
    if (
        registry.get("system_release_id") != release_id
        or lab.get("system_release_id") != release_id
    ):
        fail("assumption system_release_id mismatch")
    required(registry, ["registry_id", "model_runtime_signature"], "assumptions")
    if lab.get("assumption_registry_ref") != registry["registry_id"]:
        fail("ablation assumption_registry_ref must equal registry_id")
    required(lab, ["lab_id", "system_identity_ref"], "ablation lab")
    evidence.get(lab["system_identity_ref"], "ablation system identity")
    assumptions = registry.get("assumptions")
    if not isinstance(assumptions, list):
        fail("assumptions must be a list")
    if not assumptions and not registry.get("no_active_assumptions_reason"):
        fail("assumption registry needs assumptions or an explicit empty reason")
    active: dict[str, dict[str, Any]] = {}
    affected: set[str] = set()
    now = datetime.now(timezone.utc)
    for index, item in enumerate(assumptions):
        if not isinstance(item, dict):
            fail(f"assumption {index} must be an object")
        required(
            item,
            ["assumption_id", "component", "claim", "compensates_for", "owner", "status"],
            f"assumption {index}",
        )
        assumption_id = str(item["assumption_id"])
        if assumption_id in active:
            fail(f"duplicate active assumption: {assumption_id}")
        if item["status"] == "ablation_due":
            fail(f"assumption {assumption_id} is due for ablation")
        if item["status"] != "active":
            continue
        required(
            item,
            [
                "introduced_at", "introduced_for_signature", "evidence_class",
                "evidence_refs", "review_due_at", "rollback_ref",
            ],
            f"assumption {assumption_id}",
        )
        if timestamp(item["review_due_at"], f"assumption {assumption_id} review") <= now:
            fail(f"assumption {assumption_id} review is overdue")
        for ref in item["evidence_refs"]:
            evidence.get(ref, f"assumption {assumption_id} evidence")
        evidence.get(item["rollback_ref"], f"assumption {assumption_id} rollback")
        changed = item["introduced_for_signature"] != registry["model_runtime_signature"]
        impact = item.get("impact_assessment", {})
        if changed and impact.get("affected_by_current_signature") is False:
            required(
                impact, ["not_affected_reason", "evidence_refs"],
                f"assumption {assumption_id} impact",
            )
            for ref in impact["evidence_refs"]:
                evidence.get(ref, f"assumption {assumption_id} impact evidence")
        elif changed and impact.get("affected_by_current_signature") is not True:
            fail(f"assumption {assumption_id} needs current-signature impact status")
        else:
            affected.add(assumption_id)
            required(item, ["ablation_case_id"], f"assumption {assumption_id}")
        active[assumption_id] = item
    if active and registry.get("no_active_assumptions_reason"):
        fail("no_active_assumptions_reason conflicts with active assumptions")
    cases = lab.get("cases")
    if not isinstance(cases, list):
        fail("ablation cases must be a list")
    covered: set[str] = set()
    case_ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(f"ablation case {index} must be an object")
        required(
            case,
            [
                "case_id", "assumption_id", "candidate_configuration_hash",
                "decision", "decision_reason", "evidence_refs",
            ],
            f"ablation case {index}",
        )
        case_id, assumption_id = str(case["case_id"]), str(case["assumption_id"])
        if case_id in case_ids or assumption_id not in active:
            fail(f"duplicate or orphaned ablation case: {case_id}")
        case_ids.add(case_id)
        if active[assumption_id].get("ablation_case_id") != case_id:
            fail(f"assumption {assumption_id} ablation_case_id mismatch")
        if not case.get("one_intervention_only") or not case.get("matched_budgets"):
            fail(f"ablation case {case_id} is not isolated and matched")
        if case.get("decision") not in {"remove", "retain", "replace"}:
            fail(f"ablation case {case_id} is unresolved")
        refs(
            evidence, case,
            [
                "capability_suite_ref", "regression_suite_ref",
                "safety_suite_ref", "holdout_result_ref",
            ],
            f"ablation case {case_id}",
        )
        for ref in case["evidence_refs"]:
            evidence.get(ref, f"ablation case {case_id} evidence")
        if case["decision"] == "retain":
            metrics = case.get("metrics", {})
            measured = (
                number(metrics.get("quality_delta"), -math.inf)
                and number(metrics.get("safety_delta"), -math.inf)
                and metrics["safety_delta"] >= 0
                and (metrics["quality_delta"] > 0 or metrics["safety_delta"] > 0)
            )
            if not case.get("deterministic_control_rationale") and not measured:
                fail(f"retained case {case_id} lacks rationale or measured lift")
        covered.add(assumption_id)
    if covered != affected:
        fail(f"ablation coverage mismatch: expected {sorted(affected)}")
    if affected:
        required(lab, ["frozen_holdout_ref"], "ablation lab")
        evidence.get(lab["frozen_holdout_ref"], "ablation frozen holdout")
    all_true(
        lab.get("release_rule", {}),
        [
            "all_active_assumptions_covered",
            "pending_or_blocked_cases_fail_release",
            "retain_requires_measured_lift_or_deterministic_control",
            "safety_non_inferiority_required",
            "final_holdout_hidden_from_optimizer",
        ],
        "ablation release rule",
    )
    if lab.get("result", {}).get("status") != "pass":
        fail("ablation lab result must pass")
    empty(lab.get("result", {}).get("blockers"), "ablation blockers")
    empty(lab.get("result", {}).get("warnings"), "ablation warnings")
    if registry.get("status") != "pass":
        fail("assumption registry status must pass")
    empty(registry.get("blockers"), "assumption blockers")
    empty(registry.get("warnings"), "assumption warnings")


def validate_eval(
    validity: dict[str, Any], output: dict[str, Any], evidence: Evidence,
    release_id: str,
) -> None:
    if validity.get("schema_version") != 2 or output.get("version") != 3:
        fail("eval validity must use schema 2 and Output Eval version 3")
    if (
        validity.get("system_release_id") != release_id
        or output.get("system_release_id") != release_id
    ):
        fail("eval system_release_id mismatch")
    required(
        validity,
        [
            "report_id", "eval_suite_id", "eval_suite_version",
            "dataset_commit_or_hash", "claim_under_test", "task_distribution_ref",
            "task_inventory_ref", "task_disposition_ref",
            "predeclared_exclusion_policy_ref",
        ],
        "eval validity",
    )
    refs(
        evidence, validity,
        [
            "task_distribution_ref", "task_inventory_ref", "task_disposition_ref",
            "predeclared_exclusion_policy_ref",
        ],
        "eval validity",
    )
    if validity.get("status") != "pass" or validity.get("claim_eligible") is not True:
        fail("eval validity must pass and be claim eligible")
    count = validity.get("source_task_count")
    if (
        not isinstance(count, int) or count <= 0
        or validity.get("disposition_count") != count
        or validity.get("counts_reconcile") is not True
    ):
        fail("eval task counts do not reconcile")
    holdout = validity.get("holdout", {})
    all_true(holdout, ["frozen_before_tuning", "hidden_from_optimizer"], "eval holdout")
    refs(
        evidence, holdout,
        ["split_ref", "network_policy_ref", "answer_key_access_test_ref"],
        "eval holdout",
    )
    quality = validity.get("task_quality", {})
    if quality.get("reference_solution_or_feasibility_witness_coverage") != 1.0:
        fail("eval feasibility/reference coverage must be 1.0")
    refs(
        evidence, quality,
        [
            "requirement_to_grader_map_ref", "hidden_test_coverage_ref",
            "mutation_test_ref", "ambiguity_review_ref",
            "contamination_probe_ref", "evaluation_awareness_probe_ref",
            "shortcut_and_leakage_probe_ref",
        ],
        "eval task quality",
    )
    if quality.get("known_severe_defects") != 0 or quality.get("known_warning_defects") != 0:
        fail("eval has unresolved known defects")
    grader_quality = validity.get("grader_quality", {})
    if grader_quality.get("llm_is_sole_safety_authority") is not False:
        fail("LLM judge cannot be sole safety authority")
    refs(
        evidence, grader_quality,
        [
            "deterministic_graders_ref", "model_judge_calibration_ref",
            "human_adjudication_ref", "confusion_matrix_ref",
            "inter_rater_agreement_ref",
        ],
        "grader quality",
    )
    review = validity.get("independent_review", {})
    all_true(review, ["blinded_to_system_identity"], "eval independent review")
    if not isinstance(review.get("sample_size"), int) or review["sample_size"] <= 0:
        fail("eval independent review needs positive sample_size")
    refs(
        evidence, review, ["reviewer_provenance_ref", "defect_rate_interval_ref"],
        "eval independent review",
    )
    refs(
        evidence, validity,
        ["raw_intention_to_test_result_ref", "adjudicated_result_ref"],
        "eval validity",
    )
    empty(validity.get("blockers"), "eval validity blockers")
    empty(validity.get("warnings"), "eval validity warnings")

    if output.get("eval_validity_ref") != validity["report_id"]:
        fail("Output Eval eval_validity_ref must equal report_id")
    if output.get("task_distribution_ref") != validity["task_distribution_ref"]:
        fail("Output Eval task distribution mismatch")
    evidence.get(output.get("system_identity_ref"), "Output Eval system identity")
    for side in ["baseline", "with_agent"]:
        row = output.get(side, {})
        required(
            row, ["description", "system_identity_ref", "artifact_ref", "budgets_ref"],
            f"Output Eval {side}",
        )
        refs(
            evidence, row, ["system_identity_ref", "artifact_ref", "budgets_ref"],
            f"Output Eval {side}",
        )
    comparison = output.get("comparison", {})
    all_true(
        comparison,
        [
            "one_intervention_only", "matched_budgets",
            "matched_infrastructure", "matched_task_distribution",
        ],
        "Output Eval comparison",
    )
    if not isinstance(comparison.get("improvement_claimed"), bool):
        fail("improvement_claimed must be boolean")
    trial = output.get("trial_protocol", {})
    if not isinstance(trial.get("stochastic"), bool):
        fail("stochastic must be boolean")
    trials = trial.get("trials_per_task")
    if not isinstance(trials, int) or trials <= 0:
        fail("trials_per_task must be positive")
    all_true(
        trial, ["clean_state_reset", "all_attempts_reported", "best_of_n_matches_deployment"],
        "trial protocol",
    )
    if trial["stochastic"] and trials < 3:
        fail("stochastic evaluation requires at least three trials")
    if not trial["stochastic"]:
        evidence.get(trial.get("determinism_evidence_ref"), "determinism evidence")
    infra = output.get("infrastructure", {})
    required(
        infra,
        [
            "container_or_environment_hash", "cpu_floor", "ram_floor",
            "cpu_kill_ceiling", "ram_kill_ceiling", "region_or_provider",
        ],
        "evaluation infrastructure",
    )
    refs(
        evidence, infra,
        [
            "profile_ref", "timeout_policy_ref", "network_policy_ref",
            "cache_policy_ref", "aa_noise_calibration_ref",
        ],
        "evaluation infrastructure",
    )
    if not isinstance(infra.get("concurrency"), int) or infra["concurrency"] <= 0:
        fail("evaluation concurrency must be positive")
    if infra.get("infrastructure_errors_reported_separately") is not True:
        fail("infrastructure errors must be reported separately")
    if set(output.get("required_grader_families", [])) != GRADER_FAMILIES:
        fail("Output Eval grader families are incomplete or duplicated")
    graders = output.get("graders", {})
    if not any(graders.get("outcome", {}).get(key) for key in [
        "deterministic_state_checks", "artifact_checks", "model_rubric_refs",
        "human_review_refs",
    ]):
        fail("outcome grader has no executable definition")
    trajectory = graders.get("trajectory", {})
    if not trajectory.get("required_events") or not isinstance(
        trajectory.get("verification_required"), bool
    ):
        fail("trajectory grader is incomplete")
    boundary = graders.get("boundary", {})
    if not any(boundary.get(key) for key in [
        "permission_checks", "data_flow_checks", "inter_agent_transfer_checks",
        "forbidden_actions",
    ]):
        fail("boundary grader has no executable definition")
    if boundary.get("correct_answer_after_hidden_violation_must_fail") is not True:
        fail("boundary grader must reject hidden violations")
    if not any(graders.get("stability", {}).get(key) for key in [
        "recovery_checks", "cancellation_checks", "idempotency_checks",
        "resource_limit_checks",
    ]):
        fail("stability grader has no executable definition")
    if graders.get("model_judge", {}).get("sole_safety_authority") is not False:
        fail("model judge cannot be sole safety authority")
    cases = output.get("cases")
    if not isinstance(cases, list) or len(cases) != count:
        fail("Output Eval case count must equal source_task_count")
    seen_cases: set[str] = set()
    seen_tasks: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(f"Output Eval case {index} must be an object")
        required(
            case, ["case_id", "task_id", "trial_result_refs", "evidence_refs"],
            f"Output Eval case {index}",
        )
        if case["case_id"] in seen_cases or case["task_id"] in seen_tasks:
            fail("Output Eval case_id and task_id must be unique")
        seen_cases.add(case["case_id"])
        seen_tasks.add(case["task_id"])
        if len(case["trial_result_refs"]) < trials:
            fail(f"Output Eval case {case['case_id']} lacks trial evidence")
        if len(case["trial_result_refs"]) != len(set(case["trial_result_refs"])):
            fail(f"Output Eval case {case['case_id']} reuses a trial evidence ref")
        for ref in [*case["trial_result_refs"], *case["evidence_refs"]]:
            evidence.get(ref, f"Output Eval case {case['case_id']} evidence")
        for family in GRADER_FAMILIES:
            if case.get(f"{family}_status") != "pass":
                fail(f"Output Eval case {case['case_id']} failed {family}")
        if case.get("infrastructure_failure") is not False:
            fail(f"Output Eval case {case['case_id']} has unresolved infra state")
    metrics = output.get("metrics", {})
    for field in [
        "pass_at_1", "pass_at_k", "pass_power_k_or_consistency",
        "critical_failure_probability", "outcome_quality", "trajectory_quality",
        "infrastructure_error_rate",
    ]:
        if not number(metrics.get(field), 0, 1):
            fail(f"Output Eval metric {field} must be in [0,1]")
    if (
        metrics["critical_failure_probability"] != 0
        or metrics["infrastructure_error_rate"] != 0
        or metrics.get("boundary_violation_count") != 0
    ):
        fail("Output Eval has safety, boundary, or infrastructure failures")
    for field in [
        "median_latency_ms", "p95_latency_ms", "average_tokens",
        "average_tool_calls", "average_cost",
    ]:
        if not number(metrics.get(field)):
            fail(f"Output Eval metric {field} is invalid")
    evidence.get(metrics.get("confidence_interval_ref"), "confidence interval")
    result = output.get("result", {})
    if result.get("status") != "pass" or result.get("critical_safety_violations") != 0:
        fail("Output Eval must pass with zero critical violations")
    empty(result.get("blockers"), "Output Eval blockers")
    empty(result.get("warnings"), "Output Eval warnings")
    if comparison["improvement_claimed"]:
        evidence.get(result.get("improvement_evidence_ref"), "improvement evidence")
        if result.get("non_improvement_limit_ref"):
            fail("improvement and non-improvement limit conflict")
    else:
        evidence.get(result.get("non_improvement_limit_ref"), "non-improvement limit")
        if result.get("improvement_evidence_ref"):
            fail("non-improvement run cannot claim improvement evidence")
    all_true(
        output.get("release_rule", {}),
        [
            "eval_validity_must_pass", "all_required_grader_families_covered",
            "p0_boundary_violation_blocks_release",
            "quality_cannot_compensate_safety",
            "stochastic_claim_requires_repeated_trials",
            "best_of_n_claim_requires_matching_deployment",
            "with_agent_must_improve_or_record_limit",
        ],
        "Output Eval release rule",
    )


def validate_events(
    events: list[dict[str, Any]], evidence: Evidence, release_id: str,
    identity: dict[str, Any], boundary: dict[str, Any],
    grants: dict[str, dict[str, Any]], approvals: dict[str, dict[str, Any]],
) -> None:
    if not events:
        fail("run-event ledger is empty")
    event_ids: set[str] = set()
    runs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, event in enumerate(events):
        if event.get("schema_version") != 2:
            fail(f"run event {index} must use schema_version 2")
        required(
            event,
            [
                "event_id", "event_type", "timestamp", "trace_id", "span_id",
                "workflow_run_id", "attempt_id", "intent_summary",
            ],
            f"run event {index}",
        )
        if event["event_id"] in event_ids or event["event_type"] not in EVENT_TYPES:
            fail(f"duplicate id or unknown event type: {event['event_id']}")
        event_ids.add(event["event_id"])
        if not isinstance(event.get("sequence"), int) or event["sequence"] < 0:
            fail(f"run event {event['event_id']} has invalid sequence")
        timestamp(event["timestamp"], f"run event {event['event_id']} timestamp")
        actor = event.get("actor", {})
        required(actor, ["type", "id", "principal_id"], "run event actor")
        system = event.get("system_identity", {})
        if system.get("system_release_id") != release_id:
            fail(f"run event {event['event_id']} release mismatch")
        for field in [
            "model_snapshot", "harness_commit", "instructions_hash",
            "tool_registry_hash", "permission_policy_hash",
        ]:
            if system.get(field) != identity.get(field):
                fail(f"run event {event['event_id']} identity mismatch: {field}")
        if event.get("sensitive_payload_omitted") is not True:
            fail(f"run event {event['event_id']} exposes sensitive payload")
        for field in [
            "step_delta", "tool_call_delta", "runtime_ms_delta",
            "input_tokens_delta", "output_tokens_delta", "cost_delta",
        ]:
            if not number(event.get("budgets", {}).get(field)):
                fail(f"run event {event['event_id']} has invalid {field}")
        for ref in [*event.get("provenance_refs", []), *event.get("artifact_refs", [])]:
            evidence.get(ref, f"run event {event['event_id']} evidence")
        runs[str(event["workflow_run_id"])].append(event)
    limits = boundary["budget_limits"]
    budget_map = {
        "step_delta": "max_steps", "tool_call_delta": "max_tool_calls",
        "runtime_ms_delta": "max_runtime_ms",
        "input_tokens_delta": "max_input_tokens",
        "output_tokens_delta": "max_output_tokens", "cost_delta": "max_cost",
    }
    for run_id, rows in runs.items():
        rows.sort(key=lambda row: row["sequence"])
        if rows[0]["event_type"] != "run_started" or rows[-1]["event_type"] != "run_finished":
            fail(f"run {run_id} lacks terminal lifecycle events")
        seq = [row["sequence"] for row in rows]
        if seq != list(range(seq[0], seq[0] + len(seq))):
            fail(f"run {run_id} sequence is not contiguous")
        times = [timestamp(row["timestamp"], f"run {run_id} time") for row in rows]
        if times != sorted(times):
            fail(f"run {run_id} timestamps are not monotonic")
        if len({row["trace_id"] for row in rows}) != 1 or len({row["attempt_id"] for row in rows}) != 1:
            fail(f"run {run_id} trace or attempt identity changed")
        for previous, current in zip(rows, rows[1:]):
            after = previous.get("state", {}).get("revision_after")
            before = current.get("state", {}).get("revision_before")
            if after and before and after != before:
                fail(f"run {run_id} state revision discontinuity")
        for delta, limit in budget_map.items():
            if sum(row["budgets"][delta] for row in rows) > limits[limit]:
                fail(f"run {run_id} exceeded {limit}")
        calls: dict[str, list[dict[str, Any]]] = defaultdict(list)
        cancel_at: list[int] = []
        cleanup_at: list[int] = []
        for position, row in enumerate(rows):
            if row["event_type"] == "cancel_requested":
                cancel_at.append(position)
            if row["event_type"] == "cleanup_finished":
                cleanup_at.append(position)
            if row["event_type"] in TOOL_EVENTS:
                tool = row.get("tool", {})
                required(
                    tool,
                    [
                        "tool_call_id", "tool_id", "principal_id", "operation", "resource",
                        "resource_version", "risk_class", "budget_ref",
                        "normalized_arguments_hash",
                    ],
                    f"run {run_id} {row['event_type']}",
                )
                digest(tool["normalized_arguments_hash"], "tool arguments")
                calls[str(tool["tool_call_id"])].append(row)
            if row["event_type"] == "inter_agent_transfer":
                permission = row.get("permission", {})
                if (
                    permission.get("decision") != "allow"
                    or permission.get("grant_or_approval_ref") not in set(grants) | set(approvals)
                    or not row.get("provenance_refs")
                    or not row.get("artifact_refs")
                ):
                    fail(f"run {run_id} has ungoverned inter-agent transfer")
        if cancel_at and not any(index > cancel_at[-1] for index in cleanup_at):
            fail(f"run {run_id} cancellation lacks cleanup")
        for call_id, call_rows in calls.items():
            types = [row["event_type"] for row in call_rows]
            if types[0] != "tool_proposed":
                fail(f"tool call {call_id} must begin with proposal")
            signatures = {
                tuple(row["tool"].get(field) for field in [
                    "tool_id", "principal_id", "operation", "resource", "resource_version",
                    "risk_class", "budget_ref", "normalized_arguments_hash",
                ])
                for row in call_rows
            }
            if len(signatures) != 1:
                fail(f"tool call {call_id} changed approval-bound fields")
            permissions = [row for row in call_rows if row["event_type"] == "permission_decided"]
            if not permissions:
                fail(f"tool call {call_id} lacks permission decision")
            decision = permissions[-1].get("permission", {})
            starts = [row for row in call_rows if row["event_type"] == "tool_started"]
            observations = [row for row in call_rows if row["event_type"] == "tool_observed"]
            if decision.get("decision") == "deny":
                if starts or observations:
                    fail(f"denied tool call {call_id} executed")
                continue
            if (
                decision.get("decision") != "allow"
                or decision.get("grant_or_approval_ref") not in set(grants) | set(approvals)
            ):
                fail(f"tool call {call_id} has unresolved authority")
            evidence.get(decision.get("enforcement_ref"), f"tool call {call_id} enforcement")
            authority_ref = str(decision["grant_or_approval_ref"])
            authority = grants.get(authority_ref) or approvals.get(authority_ref)
            if authority is None:
                fail(f"tool call {call_id} authority record is missing")
            tool = call_rows[0]["tool"]
            expected_authority = {
                "tool_id": authority.get("tool_id"),
                "principal_id": authority.get("principal_id"),
                "operation": authority.get("operations", [authority.get("operation")])[0],
                "resource": authority.get("resource"),
                "resource_version": authority.get("resource_version"),
                "risk_class": authority.get("risk_class"),
                "budget_ref": authority.get("budget_ref"),
                "normalized_arguments_hash": authority.get("normalized_arguments_hash"),
            }
            for field, expected in expected_authority.items():
                if tool.get(field) != expected:
                    fail(f"tool call {call_id} does not match authority: {field}")
            if len(starts) != 1 or len(observations) != 1:
                fail(f"tool call {call_id} needs one start and observation")
            if call_rows[0].get("effect", {}).get("status") != "proposed":
                fail(f"tool call {call_id} proposal must record proposed effect")
            if starts[0].get("effect", {}).get("status") != "started":
                fail(f"tool call {call_id} start must record started effect")
            if starts[0].get("budgets", {}).get("tool_call_delta", 0) < 1:
                fail(f"tool call {call_id} start must consume tool-call budget")
            positions = {id(row): call_rows.index(row) for row in call_rows}
            if not (
                positions[id(permissions[-1])] < positions[id(starts[0])]
                < positions[id(observations[0])]
            ):
                fail(f"tool call {call_id} lifecycle order is invalid")
            evidence.get(
                observations[0].get("tool", {}).get("observation_ref"),
                f"tool call {call_id} observation",
            )
            effect = observations[0].get("effect", {}).get("status")
            if effect == "unknown":
                reconciled = [
                    row for row in call_rows if row["event_type"] == "effect_reconciled"
                ]
                if not reconciled or reconciled[-1].get("effect", {}).get("status") not in {
                    "reconciled", "committed", "failed", "rolled_back",
                }:
                    fail(f"tool call {call_id} has unknown unreconciled effect")
            elif effect not in {"committed", "failed", "rolled_back"}:
                fail(f"tool call {call_id} has unresolved effect")


def validate_independent_review(
    report: dict[str, Any], evidence: Evidence, release_id: str,
    decided_at: datetime,
) -> None:
    if report.get("schema_version") != 3:
        fail("independent review must use schema_version 3")
    required(
        report,
        ["report_id", "system_release_id", "gate_id", "status", "completed_at"],
        "independent review",
    )
    if (
        report["system_release_id"] != release_id
        or report["gate_id"] != "independent_review"
        or report["status"] != "pass"
    ):
        fail("independent review does not prove this release gate")
    if report.get("independent_execution") is not True:
        fail("independent review must prove independent_execution")
    if report.get("self_review_only") is not False:
        fail("independent review cannot be self-review only")
    completed_at = timestamp(report["completed_at"], "independent review completed_at")
    if completed_at > decided_at:
        fail("independent review completed after release decision")
    if set(report.get("required_review_ids", [])) != INDEPENDENT_REVIEW_IDS:
        fail("independent review required_review_ids are incomplete")
    rows = report.get("reviews")
    if not isinstance(rows, list):
        fail("independent review reviews must be a list")
    reviews: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            fail(f"independent review row {index} must be an object")
        required(
            row,
            [
                "id", "kind", "reviewer_id", "status", "inspected_files",
                "work_trace", "subagent_run_id", "parent_workflow_run_id",
                "role_id", "runtime", "model", "prompt_hash",
                "context_pack_ref", "context_hash", "isolation_mode",
                "trace_ref", "result_ref", "evidence_refs",
            ],
            f"independent review row {index}",
        )
        review_id = str(row["id"])
        if review_id in reviews:
            fail(f"duplicate independent review id: {review_id}")
        if row.get("independent") is not True or row.get("status") != "pass":
            fail(f"independent review {review_id} is not an independent pass")
        if row["subagent_run_id"] == row["parent_workflow_run_id"]:
            fail(f"independent review {review_id} reuses the parent run id")
        digest(row["prompt_hash"], f"independent review {review_id} prompt_hash")
        digest(row["context_hash"], f"independent review {review_id} context_hash")
        refs(
            evidence, row, ["context_pack_ref", "trace_ref", "result_ref"],
            f"independent review {review_id}",
        )
        for ref in row["evidence_refs"]:
            evidence.get(ref, f"independent review {review_id} evidence")
        if not isinstance(row.get("tools"), list) or not isinstance(row.get("permissions"), list):
            fail(f"independent review {review_id} must record tools and permissions")
        reviews[review_id] = row
    if set(reviews) != INDEPENDENT_REVIEW_IDS:
        fail("independent review rows do not exactly match required_review_ids")
    if report.get("all_findings_dispositioned") is not True:
        fail("independent review findings are not fully dispositioned")
    for finding in report.get("findings", []):
        if finding.get("status") not in {
            "fixed", "rejected_with_reason", "known_limitation", "not_applicable"
        }:
            fail("independent review contains an unresolved finding")
        required(finding, ["id", "reason", "evidence_refs"], "independent finding")
        for ref in finding["evidence_refs"]:
            evidence.get(ref, "independent finding evidence")
    empty(report.get("blockers"), "independent review blockers")
    empty(report.get("warnings"), "independent review warnings")


def validate_release(
    decision: dict[str, Any], evidence: Evidence, release_id: str
) -> None:
    if decision.get("schema_version") != 2:
        fail("release decision must use schema_version 2")
    if decision.get("system_release_id") != release_id:
        fail("release decision system_release_id mismatch")
    required(
        decision, ["release_id", "maturity", "decided_by", "decided_at"],
        "release decision",
    )
    if decision["maturity"] not in {"production", "library", "governed"}:
        fail("release decision maturity is invalid")
    if decision.get("evidence_bundle_ref") != evidence.bundle_id:
        fail("release decision evidence_bundle_ref mismatch")
    decided_at = timestamp(decision["decided_at"], "release decided_at")
    gate_list = decision.get("required_gates")
    if (
        not isinstance(gate_list, list)
        or len(gate_list) != len(set(gate_list))
        or set(gate_list) != RELEASE_GATES
    ):
        fail("release decision must declare exactly all 13 mandatory gates")
    rows = decision.get("gate_results")
    if not isinstance(rows, list):
        fail("gate_results must be a list")
    results: dict[str, dict[str, Any]] = {}
    for row in rows:
        gate_id = row.get("gate_id") if isinstance(row, dict) else None
        if not gate_id or gate_id in results:
            fail("release decision has blank or duplicate gate_id")
        results[str(gate_id)] = row
    if set(results) != RELEASE_GATES:
        fail("gate_results must exactly match required_gates")
    archive_gate_reports: dict[str, dict[str, Any]] = {}
    for gate_id, row in results.items():
        if row.get("status") != "pass":
            fail(f"final gate {gate_id} must pass; warn/not_applicable cannot pass")
        required(
            row, ["evidence_ref", "evidence_hash", "verification_command"],
            f"release gate {gate_id}",
        )
        item = evidence.get(row["evidence_ref"], f"release gate {gate_id}")
        if gate_id not in item.get("gate_ids", []):
            fail(f"evidence does not declare gate {gate_id}")
        if digest(row["evidence_hash"], f"gate {gate_id} hash") != item["sha256"]:
            fail(f"gate {gate_id} evidence hash mismatch")
        expected_kind = {
            "package": "package_validation",
            "install": "install_validation",
            "independent_review": "independent_review",
        }.get(gate_id)
        if expected_kind and item["kind"] != expected_kind:
            fail(f"gate {gate_id} requires evidence kind {expected_kind}")
        report = load_json(item["resolved_path"])
        if gate_id == "independent_review":
            validate_independent_review(report, evidence, release_id, decided_at)
            continue
        required(report, ["executed_at"], f"gate {gate_id} report")
        if timestamp(report["executed_at"], f"gate {gate_id} executed_at") > decided_at:
            fail(f"gate {gate_id} executed after release decision")
        if gate_id in {"package", "install"}:
            required(
                report,
                [
                    "runtime_archive_ref", "runtime_zip_name",
                    "runtime_zip_sha256", "inventory_sha256", "entry_count",
                ],
                f"gate {gate_id} archive evidence",
            )
            archive = evidence.get(
                report["runtime_archive_ref"], f"gate {gate_id} runtime archive",
                {"runtime_archive"},
            )
            if digest(report["runtime_zip_sha256"], f"gate {gate_id} runtime zip") != archive["sha256"]:
                fail(f"gate {gate_id} runtime archive hash mismatch")
            digest(report["inventory_sha256"], f"gate {gate_id} inventory hash")
            if not isinstance(report["entry_count"], int) or report["entry_count"] <= 0:
                fail(f"gate {gate_id} entry_count must be positive")
            if report.get("artifact_refs") != [report["runtime_archive_ref"]]:
                fail(f"gate {gate_id} must reference exactly the runtime archive")
            proof_hash_field = "builder_sha256" if gate_id == "package" else "validator_sha256"
            digest(report.get(proof_hash_field), f"gate {gate_id} {proof_hash_field}")
            archive_gate_reports[gate_id] = report
        if (
            report.get("system_release_id") != release_id
            or report.get("gate_id") != gate_id
            or report.get("status") != "pass"
        ):
            fail(f"gate {gate_id} report does not prove this release")
        empty(report.get("blockers"), f"gate {gate_id} blockers")
        empty(report.get("warnings"), f"gate {gate_id} warnings")
        for ref in report.get("artifact_refs", []):
            evidence.get(ref, f"gate {gate_id} artifact")
    if set(archive_gate_reports) != {"package", "install"}:
        fail("package and install archive reports are both required")
    for field in [
        "runtime_archive_ref", "runtime_zip_name", "runtime_zip_sha256",
        "inventory_sha256", "entry_count",
    ]:
        if archive_gate_reports["package"].get(field) != archive_gate_reports["install"].get(field):
            fail(f"package/install report mismatch: {field}")
    reconciliation = decision.get("reconciliation", {})
    all_true(
        reconciliation,
        [
            "all_required_gates_present", "all_evidence_refs_resolve",
            "quality_cannot_compensate_safety",
        ],
        "release reconciliation",
    )
    empty(reconciliation.get("pending_or_blocking_gates"), "pending gates")
    empty(reconciliation.get("expired_waivers"), "expired waivers")
    if reconciliation.get("critical_safety_violations") != 0:
        fail("release must record zero critical safety violations")
    claims = decision.get("allowed_claims")
    supports = set(evidence.data.get("claim_boundary", {}).get("supports", []))
    if not isinstance(claims, list) or not claims:
        fail("release needs at least one bounded allowed claim")
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            fail(f"allowed claim {index} must be an object")
        required(claim, ["claim", "supported_by_gate_ids"], f"allowed claim {index}")
        support_gates = set(claim["supported_by_gate_ids"])
        if (
            claim["claim"] not in supports
            or not support_gates
            or not support_gates.issubset(RELEASE_GATES)
        ):
            fail(f"allowed claim {index} lacks reconciled support")
    if decision.get("decision") != "pass":
        fail("release decision must be pass")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a filled, evidence-backed frontier harness release."
    )
    parser.add_argument("--harness-boundary", type=Path, required=True)
    parser.add_argument("--permission-policy", type=Path, required=True)
    parser.add_argument("--assumption-registry", type=Path, required=True)
    parser.add_argument("--ablation-lab", type=Path, required=True)
    parser.add_argument("--eval-validity", type=Path, required=True)
    parser.add_argument("--output-eval", type=Path, required=True)
    parser.add_argument("--run-events", type=Path, required=True)
    parser.add_argument("--approval-ledger", type=Path, required=True)
    parser.add_argument("--evidence-bundle", type=Path, required=True)
    parser.add_argument("--release-decision", type=Path, required=True)
    args = parser.parse_args()

    boundary = load_json(args.harness_boundary)
    release_id = boundary.get("system_release_id")
    if not release_id:
        fail("harness boundary missing system_release_id")
    evidence = Evidence(args.evidence_bundle, str(release_id))
    for path, label, kinds in [
        (args.harness_boundary, "harness boundary", None),
        (args.permission_policy, "permission policy", None),
        (args.assumption_registry, "assumption registry", None),
        (args.ablation_lab, "ablation lab", None),
        (args.eval_validity, "eval validity", None),
        (args.output_eval, "Output Eval", None),
        (args.run_events, "run events", {"run_log"}),
        (args.approval_ledger, "approval ledger", {"approval"}),
        (args.release_decision, "release decision", None),
    ]:
        evidence.has_path(path, label, kinds)
    release_id, identity = validate_boundary(
        boundary, evidence, args.permission_policy
    )
    approvals = validate_approvals(
        load_json(args.approval_ledger), evidence, release_id
    )
    grants, approvals = validate_permissions(
        load_json(args.permission_policy), evidence, release_id, approvals
    )
    validate_assumptions(
        load_json(args.assumption_registry), load_yaml(args.ablation_lab),
        evidence, release_id,
    )
    validate_eval(
        load_json(args.eval_validity), load_yaml(args.output_eval), evidence,
        release_id,
    )
    validate_events(
        load_jsonl(args.run_events), evidence, release_id, identity, boundary,
        grants, approvals,
    )
    validate_release(load_json(args.release_decision), evidence, release_id)
    print(
        "PASS: frontier harness evidence is hashed, reconciled, and internally consistent"
    )


if __name__ == "__main__":
    main()
