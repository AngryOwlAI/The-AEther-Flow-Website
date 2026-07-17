#!/usr/bin/env python3
"""Validate the pinned governed-continuation installation and website binding.

This integrity gate is read-only. It does not initialize goal state, launch a
goal, create a Codex task, execute an implementation job, or contact the source
repository recorded in the lock.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_ROOT = Path(__file__).resolve().parent
VENDOR_SCRIPTS = REPO_ROOT / ".agents/skills/agentjob-control/scripts"
for import_root in (SCRIPT_ROOT, VENDOR_SCRIPTS):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from agentjob_runtime.validation.schema import validate_instance  # noqa: E402
from goal_relay_adapter import build_continue_result, capture_snapshot  # noqa: E402
from implementation_control.continue_implementation import load_yaml  # noqa: E402


SOURCE_COMMIT = "f2852d5273ed7297a0abd55c9aecfbf7f5e4507e"
SOURCE_LOCK_SHA256 = (
    "eb952272d720cd6fc4d58e63e9ddb593956a1f5a721a9d1e638c5a7546d4fcef"
)
EXAMPLE_FIXTURES_SHA256 = (
    "cde18fd13c92932ba4343927ceaa802564e8873d53dbbfa3511facb7092af460"
)
INTEGRATION_DOCUMENT_SHA256 = (
    "2393d3361796f8a143c74d500b8c3084518a30ca70845686610da0ae8307f8ab"
)
EXPECTED_SKILLS = {
    "agentjob-control": {
        "source_sha256": (
            "899f7433425b6ef4408546823f6ef231383873100e3644188eb6399e5b76fb74"
        ),
        "required_skills": [],
        "invokes_skills": [],
    },
    "continue": {
        "source_sha256": (
            "5795757bf0c83494d64c0e682a712a146166965f13d620f03175acbe1d46ff1e"
        ),
        "required_skills": ["agentjob-control"],
        "invokes_skills": [],
    },
    "continue-goal": {
        "source_sha256": (
            "ad87c1dcc5f7d9b024490299c7f0707d553f8cebeafea5cb9c42c4c42dc9d28d"
        ),
        "required_skills": [
            "agentjob-control",
            "continue-implementing-goal",
        ],
        "invokes_skills": ["continue-implementing-goal"],
    },
    "continue-implementing-goal": {
        "source_sha256": (
            "7e6c30e605bbbd3af398dd025a3e3db827ac73e269b5662b8e8a9ef041239d17"
        ),
        "required_skills": ["agentjob-control", "continue"],
        "invokes_skills": ["continue"],
    },
}
EXPECTED_INVOCATION_EDGES = {
    ("continue-goal", "continue-implementing-goal"),
    ("continue-implementing-goal", "continue"),
}
EXPECTED_SCRIPTS = {
    "continue:goal": (
        "PYTHONDONTWRITEBYTECODE=1 python3 "
        "scripts/implementation_control/continue_goal.py"
    ),
    "validate:goal-relay": (
        "PYTHONDONTWRITEBYTECODE=1 python3 "
        "scripts/implementation_control/validate_goal_relay.py"
    ),
    "test:goal-relay-runtime": (
        "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover "
        "-s .agents/skills/agentjob-control/tests -p 'test_*.py' -v"
    ),
    "test:goal-relay": (
        "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest "
        "tests/test_goal_relay_adapter.py tests/test_goal_relay_facade.py"
    ),
}
IGNORED_SOURCE_NAMES = {".DS_Store", "__pycache__"}


class IntegrityFailure(RuntimeError):
    """Raised when the installed relay differs from its governed contract."""


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_source_files(root: Path) -> Iterable[Path]:
    if not root.is_dir():
        raise IntegrityFailure(f"installed skill directory is missing: {root}")
    for current_root, directory_names, file_names in os.walk(
        root, followlinks=False
    ):
        directory_names[:] = sorted(
            name for name in directory_names if name not in IGNORED_SOURCE_NAMES
        )
        current = Path(current_root)
        for directory_name in directory_names:
            if (current / directory_name).is_symlink():
                raise IntegrityFailure(
                    f"installed skill contains a directory symlink: "
                    f"{current / directory_name}"
                )
        for file_name in sorted(file_names):
            if file_name in IGNORED_SOURCE_NAMES or file_name.endswith(".pyc"):
                continue
            path = current / file_name
            if path.is_symlink():
                raise IntegrityFailure(
                    f"installed skill contains a file symlink: {path}"
                )
            if path.is_file():
                yield path


def directory_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in iter_source_files(root):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IntegrityFailure(message)


def mapping_by_id(
    values: Any,
    *,
    id_key: str,
    label: str,
) -> dict[str, Mapping[str, Any]]:
    require(isinstance(values, list), f"{label} must be a list")
    result: dict[str, Mapping[str, Any]] = {}
    for item in values:
        require(isinstance(item, Mapping), f"{label} contains a non-object")
        identifier = item.get(id_key)
        require(isinstance(identifier, str), f"{label} entry has no {id_key}")
        require(identifier not in result, f"duplicate {label} ID: {identifier}")
        result[identifier] = item
    return result


def validate_lock_and_vendor() -> dict[str, str]:
    lock_path = REPO_ROOT / ".agents/skill_registry/SKILL_LOCK.yaml"
    registry_path = REPO_ROOT / ".agents/skill_registry/SKILL_REGISTRY.yaml"
    require(lock_path.is_file(), "tracked source lock is missing")
    require(
        file_sha256(lock_path) == SOURCE_LOCK_SHA256,
        "tracked source lock hash differs from the pinned bundle lock",
    )
    lock = load_yaml(lock_path)
    registry = load_yaml(registry_path)
    require(lock.get("bundle_id") == "governed-continuation", "wrong bundle ID")
    require(lock.get("bundle_version") == "0.1.0", "wrong bundle version")
    require(lock.get("bootstrap_requested") is False, "lock requests bootstrap")
    require(
        lock.get("target_runtime_root") == ".agents/skills",
        "lock targets an unexpected runtime root",
    )
    require(lock.get("external_tools") == [], "bundle declares external tools")

    locked = mapping_by_id(lock.get("skills"), id_key="skill_id", label="lock skills")
    installed = mapping_by_id(
        registry.get("skills"),
        id_key="skill_id",
        label="registry skills",
    )
    require(
        set(locked) == set(EXPECTED_SKILLS),
        "lock dependency closure is not the exact four-skill family",
    )
    require(
        set(installed) == set(EXPECTED_SKILLS),
        "target registry is not the exact four-skill family",
    )

    actual_hashes: dict[str, str] = {}
    for skill_id, expected in EXPECTED_SKILLS.items():
        locked_entry = locked[skill_id]
        registry_entry = installed[skill_id]
        require(
            locked_entry.get("source_sha256") == expected["source_sha256"],
            f"{skill_id} lock hash differs from the pinned source",
        )
        require(
            locked_entry.get("required_skills") == expected["required_skills"],
            f"{skill_id} required dependency edges differ",
        )
        require(
            locked_entry.get("invokes_skills") == expected["invokes_skills"],
            f"{skill_id} invocation edges differ",
        )
        require(
            registry_entry.get("source_lock_sha256") == SOURCE_LOCK_SHA256,
            f"{skill_id} registry source-lock hash differs",
        )
        require(
            registry_entry.get("source_sha256") == expected["source_sha256"],
            f"{skill_id} registry source hash differs",
        )
        require(
            registry_entry.get("installation_kind") == "template_materialization",
            f"{skill_id} installation kind is not exact materialization",
        )
        skill_root = REPO_ROOT / ".agents/skills" / skill_id
        actual_hash = directory_sha256(skill_root)
        require(
            actual_hash == expected["source_sha256"],
            f"{skill_id} installed directory hash differs from the lock",
        )
        actual_hashes[skill_id] = actual_hash

    mutable_caches = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / ".agents/skills").rglob("*")
        if path.name == "__pycache__" or path.suffix == ".pyc"
    )
    require(
        not mutable_caches,
        "mutable Python cache exists in an installed skill: "
        + ", ".join(mutable_caches),
    )

    edges = {
        (str(item.get("from")), str(item.get("to")))
        for item in lock.get("invocation_edges", [])
        if isinstance(item, Mapping)
    }
    require(
        edges == EXPECTED_INVOCATION_EDGES,
        "bundle invocation graph differs from the pinned closure",
    )
    return actual_hashes


def validate_configuration_and_front_doors() -> None:
    config_path = REPO_ROOT / ".agents/continuation/website-adapter.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    require(config.get("status") == "experimental", "adapter is not experimental")
    require(config.get("version") == "0.1.0", "adapter version differs")
    source = config.get("source", {})
    require(source.get("commit") == SOURCE_COMMIT, "source commit pin differs")
    require(
        source.get("source_lock_sha256") == SOURCE_LOCK_SHA256,
        "adapter source-lock hash differs",
    )
    test_resources = config.get("test_resources", {})
    require(
        test_resources.get("status") == "vendored_read_only"
        and test_resources.get("runtime_required") is False
        and test_resources.get("validation_required") is True,
        "vendored test-resource boundary differs",
    )
    require(
        test_resources.get("source_commit") == SOURCE_COMMIT,
        "test-resource source commit differs",
    )
    require(
        directory_sha256(
            REPO_ROOT / ".agents/examples/governed-continuation"
        )
        == EXAMPLE_FIXTURES_SHA256,
        "vendored continuation fixture hash differs",
    )
    require(
        file_sha256(
            REPO_ROOT
            / ".agents/docs/skills/CODEX_CONTINUATION_INTEGRATION.md"
        )
        == INTEGRATION_DOCUMENT_SHA256,
        "vendored continuation integration document hash differs",
    )
    authority = config.get("authority", {})
    require(
        authority.get("implementation_root") == "implementation_control"
        and authority.get("sole_implementation_authority") is True,
        "implementation_control is not declared as sole authority",
    )
    require(
        authority.get("portable_control_bootstrap") is False
        and authority.get("portable_control_root") is None,
        "adapter permits a competing portable control root",
    )
    runtime = config.get("runtime", {})
    require(
        runtime.get("state_root") == ".local/sys4ai/continuation",
        "mutable relay state is not bound to the ignored local root",
    )
    policy = config.get("policy", {})
    required_false = (
        "allow_push",
        "allow_deployment",
        "allow_source_refresh",
        "allow_public_claim_promotion",
        "allow_upstream_write",
        "launch_real_goal_during_validation",
        "infer_checkpoint_authority_from_goal",
    )
    for key in required_false:
        require(policy.get(key) is False, f"adapter policy must disable {key}")
    require(
        policy.get("maximum_agentjobs_per_generation") == 1,
        "generation AgentJob limit differs",
    )
    require(
        policy.get("maximum_successors_per_generation") == 1,
        "generation successor limit differs",
    )
    excluded = set(config.get("fingerprint", {}).get("excludes", []))
    require(
        ".local/sys4ai/continuation" in excluded,
        "relay state is not excluded from project fingerprints",
    )

    require(
        not (REPO_ROOT / ".agents/control").exists(),
        "competing .agents/control authority must not exist",
    )
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    require(".local/sys4ai/" in gitignore, "mutable Sys4AI state is not ignored")

    expected_policies = {
        "agentjob-control": ("hidden_by_default", "declared_skills_only"),
        "continue": ("explicit_or_declared_relay", "declared_skills_only"),
        "continue-goal": ("explicit_only", "forbidden"),
        "continue-implementing-goal": (
            "hidden_by_default",
            "token_bound_or_recovery",
        ),
    }
    for skill_id, (user_policy, internal_policy) in expected_policies.items():
        skill = REPO_ROOT / ".codex/skills" / skill_id / "SKILL.md"
        metadata = REPO_ROOT / ".codex/skills" / skill_id / "agents/openai.yaml"
        require(skill.is_file(), f"project-local {skill_id} front door is missing")
        require(metadata.is_file(), f"project-local {skill_id} metadata is missing")
        text = skill.read_text(encoding="utf-8")
        require(
            text.startswith("---\n") and f"name: {skill_id}\n" in text,
            f"project-local {skill_id} front matter is invalid",
        )
        values = load_yaml(metadata)
        metadata_policy = values.get("policy", {})
        require(
            metadata_policy.get("allow_implicit_invocation") is False,
            f"{skill_id} unexpectedly permits implicit invocation",
        )
        require(
            metadata_policy.get("user_invocation") == user_policy,
            f"{skill_id} user invocation policy differs",
        )
        require(
            metadata_policy.get("internal_invocation") == internal_policy,
            f"{skill_id} internal invocation policy differs",
        )


def validate_package_interface() -> None:
    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    scripts = package.get("scripts", {})
    for name, expected in EXPECTED_SCRIPTS.items():
        require(scripts.get(name) == expected, f"package script {name} differs")
    validate = str(scripts.get("validate", ""))
    implementation_index = validate.find("npm run validate:implementation-control")
    relay_index = validate.find("npm run validate:goal-relay")
    build_index = validate.find("npm run build")
    require(
        -1 < implementation_index < relay_index < build_index,
        "validate must run implementation-control, goal-relay, then build",
    )


def validate_portable_result() -> dict[str, Any]:
    snapshot = capture_snapshot(REPO_ROOT)
    result = build_continue_result(snapshot)
    schema_path = (
        REPO_ROOT
        / ".agents/skills/agentjob-control/schemas/continue-result.schema.json"
    )
    issues = validate_instance(result, schema_path)
    require(
        not issues,
        "website adapter emitted an invalid portable result: "
        + "; ".join(f"{issue.path} {issue.message}" for issue in issues),
    )
    return {
        "status": result["status"],
        "reason_code": result["reason_code"],
        "fingerprint": snapshot.fingerprint,
    }


def main() -> int:
    try:
        hashes = validate_lock_and_vendor()
        validate_configuration_and_front_doors()
        validate_package_interface()
        sample = validate_portable_result()
    except (
        IntegrityFailure,
        json.JSONDecodeError,
        OSError,
        ValueError,
    ) as error:
        print(f"Goal relay integrity: FAIL\n- {error}", file=sys.stderr)
        return 1
    print("Goal relay integrity: PASS")
    print("- bundle: governed-continuation 0.1.0 (experimental)")
    print(f"- source commit: {SOURCE_COMMIT}")
    print(f"- source lock: {SOURCE_LOCK_SHA256}")
    for skill_id, digest in hashes.items():
        print(f"- {skill_id}: {digest}")
    print(
        "- sample result: "
        f"{sample['status']} ({sample['reason_code']}); "
        f"fingerprint {sample['fingerprint']}"
    )
    print("- implementation authority: implementation_control/")
    print("- real goals and Codex tasks launched: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
