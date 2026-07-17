from __future__ import annotations

import unittest

from _support import RUNTIME_SCRIPTS
from agentjob_runtime.errors import RecordValidationError
from agentjob_runtime.fingerprinting.canonical import build_fingerprint, build_payload
from agentjob_runtime.goal.model import fingerprint_status


def parts(revision: str, **extra):
    return {
        "repository": {
            "provider": "git", "root": "/project", "worktree": "/project",
            "git_common_dir": "/project/.git", "branch": "main", "revision": revision,
            "status_porcelain": " M source.py\r\n", **extra,
        },
        "control": {"config_hash": "a" * 64, "task_id": "TASK-1"},
        "resolver": {"boundary": "existing_agent_job_ready", "reason_code": "job.ready"},
        "validation": {"required_validator_ids": ["focused"], "outcomes": ["pass"]},
        "checkpoint": {"provider": "git_status", "status": "pass", "revision": revision},
        "adapter_extensions": {},
    }


class FingerprintCycleTests(unittest.TestCase):
    def test_unchanged_repeated_and_longer_cycles(self) -> None:
        first = build_fingerprint([], **parts("A"))
        same = build_fingerprint([first.fingerprint], **parts("A"))
        second = build_fingerprint([first.fingerprint], **parts("B"))
        cycle = build_fingerprint([first.fingerprint, second.fingerprint], **parts("A"))
        third = build_fingerprint([first.fingerprint, second.fingerprint], **parts("C"))
        long_cycle = build_fingerprint(
            [first.fingerprint, second.fingerprint, third.fingerprint], **parts("B")
        )
        self.assertEqual(first.classification, "new")
        self.assertEqual(same.classification, "unchanged")
        self.assertEqual(second.classification, "new")
        self.assertEqual(cycle.classification, "repeated")
        self.assertEqual(long_cycle.classification, "repeated")

    def test_excluded_telemetry_does_not_change_generic_hash(self) -> None:
        clean = build_fingerprint([], **parts("A"))
        noisy = build_fingerprint(
            [], **parts("A", timestamp="2026-01-01T00:00:00Z", telemetry={"duration": 1})
        )
        self.assertEqual(clean.fingerprint, noisy.fingerprint)

    def test_adapter_cannot_insert_timestamp_or_telemetry(self) -> None:
        values = parts("A")
        values["adapter_extensions"] = {"domain": {"updated_at": "now"}}
        with self.assertRaises(RecordValidationError):
            build_payload(**values)

    def test_status_line_endings_are_canonicalized_only(self) -> None:
        windows = build_fingerprint([], **parts("A"))
        unix_parts = parts("A")
        unix_parts["repository"]["status_porcelain"] = " M source.py\n"
        unix = build_fingerprint([], **unix_parts)
        self.assertEqual(windows.fingerprint, unix.fingerprint)


if __name__ == "__main__":
    unittest.main()
