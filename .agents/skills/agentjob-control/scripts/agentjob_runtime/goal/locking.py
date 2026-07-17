"""Cross-platform exclusive lock abstraction with a lock-directory fallback."""

from __future__ import annotations

import json
import os
import secrets
import time
from pathlib import Path
from types import TracebackType
from typing import Literal

from agentjob_runtime.errors import StateConflict


try:  # pragma: no cover - platform-specific import.
    import fcntl as _fcntl
except ImportError:  # pragma: no cover - Windows.
    _fcntl = None

try:  # pragma: no cover - platform-specific import.
    import msvcrt as _msvcrt
except ImportError:  # pragma: no cover - POSIX.
    _msvcrt = None


LockBackend = Literal["auto", "posix", "windows", "directory"]


class CrossPlatformFileLock:
    """Non-stealing lock; timeout reports contention but never removes another holder."""

    def __init__(
        self,
        path: str | Path,
        *,
        backend: LockBackend = "auto",
        timeout_seconds: float = 5.0,
    ) -> None:
        self.path = Path(path).resolve(strict=False)
        self.backend = self._select_backend(backend)
        self.timeout_seconds = timeout_seconds
        self._descriptor: int | None = None
        self._directory: Path | None = None

    @staticmethod
    def _select_backend(requested: LockBackend) -> str:
        if requested == "auto":
            if _fcntl is not None:
                return "posix"
            if _msvcrt is not None:
                return "windows"
            return "directory"
        if requested == "posix" and _fcntl is None:
            raise StateConflict("POSIX locking is unavailable on this platform")
        if requested == "windows" and _msvcrt is None:
            raise StateConflict("Windows locking is unavailable on this platform")
        return requested

    def __enter__(self) -> "CrossPlatformFileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout_seconds
        if self.backend == "directory":
            self._directory = self.path.with_name(f"{self.path.name}.lockdir")
            while True:
                try:
                    self._directory.mkdir(mode=0o700)
                    owner = self._directory / "owner.json"
                    owner.write_text(
                        json.dumps(
                            {"pid": os.getpid(), "token": secrets.token_hex(16)}, sort_keys=True
                        )
                        + "\n",
                        encoding="utf-8",
                    )
                    return self
                except FileExistsError:
                    if time.monotonic() >= deadline:
                        raise StateConflict(
                            "lock acquisition timed out; existing lock was not stolen",
                            details={"lock_path": str(self._directory)},
                        )
                    time.sleep(0.01)
        self._descriptor = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        if self.backend == "windows" and os.fstat(self._descriptor).st_size == 0:
            os.write(self._descriptor, b"\0")
            os.fsync(self._descriptor)
        while True:
            try:
                if self.backend == "posix":
                    _fcntl.flock(self._descriptor, _fcntl.LOCK_EX | _fcntl.LOCK_NB)
                else:
                    os.lseek(self._descriptor, 0, os.SEEK_SET)
                    _msvcrt.locking(self._descriptor, _msvcrt.LK_NBLCK, 1)
                return self
            except (BlockingIOError, OSError):
                if time.monotonic() >= deadline:
                    os.close(self._descriptor)
                    self._descriptor = None
                    raise StateConflict(
                        "lock acquisition timed out; existing lock was not stolen",
                        details={"lock_path": str(self.path)},
                    )
                time.sleep(0.01)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.backend == "directory":
            if self._directory is not None:
                try:
                    (self._directory / "owner.json").unlink()
                    self._directory.rmdir()
                finally:
                    self._directory = None
            return
        if self._descriptor is None:
            return
        try:
            if self.backend == "posix":
                _fcntl.flock(self._descriptor, _fcntl.LOCK_UN)
            else:
                os.lseek(self._descriptor, 0, os.SEEK_SET)
                _msvcrt.locking(self._descriptor, _msvcrt.LK_UNLCK, 1)
        finally:
            os.close(self._descriptor)
            self._descriptor = None
