"""Classify and enforce one-shot repository topology authority."""

from __future__ import annotations

import copy
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

from agentjob_runtime.errors import RecordValidationError, SecurityError, StateConflict
from agentjob_runtime.validation.schema import format_issues, validate_instance


PROTECTED_TOPOLOGY_ACTIONS = frozenset(
    {
        "repository-branch-create",
        "repository-worktree-create",
        "repository-binding-change",
    }
)


def _git_command_arguments(argv: Sequence[str]) -> tuple[str, ...]:
    values = tuple(str(item) for item in argv)
    if not values:
        return ()
    git_index = next(
        (
            index
            for index, value in enumerate(values)
            if Path(value).name.lower() in {"git", "git.exe"}
        ),
        None,
    )
    if git_index is None or git_index + 1 >= len(values):
        return ()
    args = list(values[git_index + 1 :])
    options_with_values = {
        "-C",
        "-c",
        "--exec-path",
        "--git-dir",
        "--namespace",
        "--super-prefix",
        "--work-tree",
    }
    while args and args[0].startswith("-"):
        option = args.pop(0)
        if option in options_with_values:
            if not args:
                return ()
            args.pop(0)
        elif any(
            option.startswith(f"{prefix}=")
            for prefix in options_with_values
            if prefix.startswith("--")
        ):
            continue
        else:
            return ()
    return tuple(args)


def classify_topology_command(argv: Sequence[str]) -> str | None:
    args = _git_command_arguments(argv)
    if not args:
        return None
    command = args[0]
    if command == "branch" and len(args) >= 2 and args[1] not in {
        "--show-current",
        "--list",
        "-l",
        "-a",
        "-r",
        "-d",
        "-D",
        "-m",
        "-M",
    }:
        return "repository-branch-create"
    if command == "switch" and any(
        item in {"-c", "-C", "--create"}
        or item.startswith("--create=")
        for item in args[1:]
    ):
        return "repository-branch-create"
    if command == "checkout" and any(item in {"-b", "-B"} for item in args[1:]):
        return "repository-branch-create"
    if command == "worktree" and len(args) >= 2 and args[1] == "add":
        return "repository-worktree-create"
    return None


def topology_command_target(argv: Sequence[str]) -> str | None:
    """Return the exact user-controlled name/path for a protected command."""

    args = _git_command_arguments(argv)
    if len(args) < 2:
        return None
    command = args[0]
    if command == "branch":
        return args[1] if not args[1].startswith("-") else None
    if command in {"switch", "checkout"}:
        flags = (
            {"-c", "-C", "--create"}
            if command == "switch"
            else {"-b", "-B"}
        )
        for index, item in enumerate(args[1:], start=1):
            if item.startswith("--create="):
                return item.split("=", 1)[1] or None
            if item in flags:
                if index + 1 >= len(args):
                    return None
                target = args[index + 1]
                return target if not target.startswith("-") else None
        return None
    if command == "worktree" and len(args) >= 3 and args[1] == "add":
        worktree_args = list(args[2:])
        option_boundary = (
            worktree_args.index("--")
            if "--" in worktree_args
            else len(worktree_args)
        )
        option_region = worktree_args[:option_boundary]
        if any(
            item in {"-b", "-B", "--orphan"}
            or item.startswith(("-b", "-B", "--orphan="))
            for item in option_region
        ):
            # A single worktree authorization cannot also authorize the
            # branch creation implicit in these forms.
            return None
        options_with_values = {"--reason"}
        index = 0
        while index < len(worktree_args):
            item = worktree_args[index]
            if item == "--":
                return (
                    worktree_args[index + 1]
                    if index + 1 < len(worktree_args)
                    else None
                )
            if item in options_with_values:
                index += 2
                continue
            if item.startswith("--reason="):
                index += 1
                continue
            if item.startswith("-"):
                index += 1
                continue
            return item
        return None
    return None


def validate_topology_authorization(
    value: Mapping[str, Any],
    *,
    action: str,
    command_id: str,
    starting_revision: str,
    requested_name_or_path: str | None = None,
    require_unconsumed: bool = True,
) -> dict[str, Any]:
    authorization = copy.deepcopy(dict(value))
    schema = (
        Path(__file__).resolve().parents[3]
        / "schemas"
        / "repository-topology-authorization.schema.json"
    )
    issues = validate_instance(authorization, schema)
    if issues:
        raise RecordValidationError(
            "repository topology authorization failed schema validation",
            details={"findings": format_issues(issues).splitlines()},
        )
    if (
        authorization["action"] != action
        or authorization["command_id"] != command_id
        or authorization["starting_revision"] != starting_revision
        or (
            requested_name_or_path is not None
            and authorization["requested_name_or_path"]
            != requested_name_or_path
        )
    ):
        raise SecurityError(
            "repository topology authorization does not match the exact operation"
        )
    if require_unconsumed and authorization["consumed"] is True:
        raise StateConflict("repository topology authorization was already consumed")
    return authorization


def consume_topology_authorization(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    if result.get("consumed") is True:
        raise StateConflict("repository topology authorization cannot be reused")
    result["consumed"] = True
    return result


def capture_git_topology(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root).expanduser().resolve()

    def run(*args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            raise RecordValidationError(
                "repository topology inspection failed",
                details={"arguments": list(args), "stderr": result.stderr.strip()},
            )
        return result.stdout.rstrip("\n")

    repository_root = Path(run("rev-parse", "--show-toplevel")).resolve()
    common = Path(run("rev-parse", "--git-common-dir"))
    if not common.is_absolute():
        common = (root / common).resolve()
    local_branches = sorted(
        item
        for item in run(
            "for-each-ref",
            "--format=%(refname)",
            "refs/heads",
        ).splitlines()
        if item
    )
    registered_worktrees: list[dict[str, Any]] = []
    current_worktree: dict[str, Any] = {}
    for field in run("worktree", "list", "--porcelain", "-z").split("\0"):
        if not field:
            if current_worktree:
                registered_worktrees.append(current_worktree)
                current_worktree = {}
            continue
        key, separator, value = field.partition(" ")
        if key == "worktree" and separator:
            current_worktree["path"] = str(
                Path(value).expanduser().resolve(strict=False)
            )
        elif key == "branch" and separator:
            current_worktree["branch"] = value
        elif key in {"bare", "detached"}:
            current_worktree[key] = True
    if current_worktree:
        registered_worktrees.append(current_worktree)
    registered_worktrees.sort(key=lambda item: str(item.get("path", "")))
    return {
        "root": str(repository_root),
        "worktree": str(repository_root),
        "git_common_dir": str(common),
        "branch": run("branch", "--show-current") or None,
        "revision": run("rev-parse", "HEAD"),
        "local_branches": local_branches,
        "registered_worktrees": [
            str(item["path"])
            for item in registered_worktrees
            if item.get("path")
        ],
        "worktree_bindings": registered_worktrees,
    }


def capture_git_topology_if_present(
    project_root: str | Path,
) -> dict[str, Any] | None:
    """Return Git topology, or ``None`` only when the root is not a worktree."""

    root = Path(project_root).expanduser().resolve()
    probe = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if probe.returncode != 0:
        return None
    return capture_git_topology(root)


def assert_topology_transition(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    authorized_actions: Sequence[str] = (),
) -> None:
    changes = {
        key
        for key in (
            "root",
            "worktree",
            "git_common_dir",
            "branch",
            "local_branches",
            "registered_worktrees",
            "worktree_bindings",
        )
        if before.get(key) != after.get(key)
    }
    if not changes:
        return
    allowed = set(authorized_actions)
    if "branch" in changes and "repository-branch-create" in allowed:
        changes.remove("branch")
    if (
        "local_branches" in changes
        and "repository-branch-create" in allowed
    ):
        changes.remove("local_branches")
    if (
        "worktree_bindings" in changes
        and "repository-branch-create" in allowed
    ):
        changes.remove("worktree_bindings")
    if (
        "registered_worktrees" in changes
        and "repository-worktree-create" in allowed
    ):
        changes.remove("registered_worktrees")
    if (
        "worktree_bindings" in changes
        and "repository-worktree-create" in allowed
    ):
        changes.remove("worktree_bindings")
    if (
        {"worktree", "git_common_dir", "root"} & changes
        and "repository-worktree-create" in allowed
    ):
        changes -= {"worktree", "git_common_dir", "root", "branch"}
    if changes:
        raise SecurityError(
            "repository topology changed without exact one-shot authority",
            details={
                "reason_code": "execution.unexpected_repository_topology_change",
                "changed_dimensions": sorted(changes),
            },
        )
