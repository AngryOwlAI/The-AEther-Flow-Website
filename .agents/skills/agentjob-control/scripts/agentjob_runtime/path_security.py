"""Cross-platform project-relative path normalization and containment checks."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from agentjob_runtime.errors import SecurityError


WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:(?:/|$)")
WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}
GLOB_META = frozenset("*?[")


@dataclass(frozen=True)
class NormalizedRelativePath:
    """One deterministic path spelling and its explicit directory semantics."""

    relative: str
    base_relative: str
    directory_rule: bool


def _raise(label: str, value: object, reason_code: str, message: str) -> None:
    raise SecurityError(
        f"{label} {message}: {value}",
        details={"reason_code": reason_code, "path": str(value)},
    )


def normalize_relative_path(
    value: str | Path,
    *,
    label: str = "path",
    allow_directory_rule: bool = True,
    allow_project_root: bool = False,
) -> NormalizedRelativePath:
    """Normalize POSIX and Windows separators without accepting path aliases.

    Exact paths remain exact. Directory authority must be declared explicitly
    with a trailing slash or ``/**``. Other glob syntax is unsupported.
    """

    raw = str(value)
    if not raw or "\x00" in raw:
        _raise(label, value, "path.invalid", "is empty or contains NUL")
    if unicodedata.normalize("NFC", raw) != raw:
        _raise(label, value, "path.unicode_not_nfc", "is not NFC-normalized")
    if any(ord(character) < 32 for character in raw):
        _raise(label, value, "path.control_character", "contains a control character")

    portable = raw.replace("\\", "/")
    if portable.startswith("/") or portable.startswith("//") or WINDOWS_DRIVE.match(portable):
        _raise(label, value, "path.absolute_forbidden", "must be project-relative")

    directory_rule = False
    marker = ""
    if portable.endswith("/**"):
        if not allow_directory_rule:
            _raise(label, value, "path.glob_forbidden", "cannot be a directory rule")
        directory_rule = True
        marker = "/**"
        portable = portable[:-3]
    elif portable.endswith("/"):
        if not allow_directory_rule:
            _raise(label, value, "path.directory_rule_forbidden", "cannot end with a slash")
        directory_rule = True
        marker = "/"
        portable = portable[:-1]

    if any(character in portable for character in GLOB_META):
        _raise(label, value, "path.glob_unsupported", "uses unsupported glob syntax")
    if "//" in portable:
        _raise(label, value, "path.alias", "contains an empty path component")
    if portable == ".":
        if not allow_project_root or directory_rule:
            _raise(label, value, "path.project_root_forbidden", "cannot name the project root")
        return NormalizedRelativePath(".", ".", False)

    parts = portable.split("/")
    if not parts or any(part in {"", ".", ".."} for part in parts):
        reason = "path.traversal" if ".." in parts else "path.alias"
        _raise(label, value, reason, "contains a forbidden path component")
    for part in parts:
        if part.endswith((" ", ".")):
            _raise(label, value, "path.windows_alias", "has a Windows-trimmed component")
        if ":" in part:
            _raise(label, value, "path.windows_alias", "contains a Windows stream separator")
        stem = part.split(".", 1)[0].upper()
        if stem in WINDOWS_RESERVED:
            _raise(label, value, "path.windows_reserved", "contains a reserved Windows name")

    base = "/".join(parts)
    return NormalizedRelativePath(f"{base}{marker}", base, directory_rule)


def alias_key(value: NormalizedRelativePath) -> str:
    """Return a filesystem-independent key used to reject portable aliases."""

    return unicodedata.normalize("NFC", value.base_relative).casefold()


def resolve_project_relative(
    project_root: str | Path,
    value: str | Path,
    *,
    label: str = "path",
    allow_directory_rule: bool = True,
    allow_project_root: bool = False,
    reject_symlinks: bool = True,
) -> tuple[Path, NormalizedRelativePath]:
    """Resolve one normalized path and prove that it remains below the root."""

    root = Path(project_root).expanduser().resolve()
    normalized = normalize_relative_path(
        value,
        label=label,
        allow_directory_rule=allow_directory_rule,
        allow_project_root=allow_project_root,
    )
    supplied = Path(*normalized.base_relative.split("/")) if normalized.base_relative != "." else Path()
    if reject_symlinks:
        current = root
        for part in supplied.parts:
            current = current / part
            if current.exists() and current.is_symlink():
                _raise(label, value, "path.symlink", "traverses a symlink")
    candidate = (root / supplied).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise SecurityError(
            f"{label} resolves outside the project root: {value}",
            details={"reason_code": "path.traversal", "path": str(value)},
        ) from error
    return candidate, normalized
