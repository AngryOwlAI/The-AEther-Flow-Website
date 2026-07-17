from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import HASH_A, RUNTIME_SCRIPTS, TS, valid_goal, valid_job, valid_role
from agentjob_runtime.adapters.codex_permissions import (
    CodexRuntimeCapabilities,
    compile_codex_permissions,
)
from agentjob_runtime.adapters.native_goal_codex import (
    CodexNativeGoalProvider,
    build_goal_mirror,
)
from agentjob_runtime.adapters.thread_auto import select_thread_provider
from agentjob_runtime.adapters.thread_codex_app_server import CodexAppServerThreadProvider
from agentjob_runtime.adapters.thread_manual import ManualThreadProvider
from agentjob_runtime.errors import BootstrapRequired, RecordValidationError
from agentjob_runtime.execution.compiler import compile_authority
from agentjob_runtime.goal.launcher import launch_goal
from agentjob_runtime.goal.sqlite_store import SQLiteGoalStore


class SurfaceTransport:
    def __init__(self):
        self.calls = []

    def request(self, operation, payload, *, timeout_seconds):
        self.calls.append((operation, payload))
        if operation == "capabilities":
            return {"available": True, "operations": ["thread.start", "thread.read"]}
        if operation == "thread.start":
            return {"status": "returned", "thread_id": "thread-desktop", "request_id": "REQ-1"}
        return {"status": "active", "thread_id": payload.get("thread_id"), "terminal": False}


class MirrorTransport:
    def __init__(self):
        self.value = None

    def set(self, thread_id, mirror):
        self.value = dict(mirror)
        return {"status": "set"}

    def get(self, thread_id):
        return self.value

    def clear(self, thread_id):
        self.value = None
        return {"status": "cleared"}


EXECUTION_CAPABILITIES = {
    "read_path_enforcement": True,
    "write_path_enforcement": True,
    "environment_enforcement": True,
    "command_enforcement": True,
    "network_control": True,
    "external_effect_enforcement": True,
    "shell_execution": True,
}


class CodexSurfaceContractTests(unittest.TestCase):
    def launch(self, root: Path, provider, *, goal_text="Complete the surface fixture."):
        store = SQLiteGoalStore(root / ".local/state/goal.db")
        binding = {
            "project_id": "surface-fixture",
            "root": str(root),
            "worktree": str(root),
            "branch": "main",
            "git_common_dir": None,
            "starting_revision": "A",
            "environment_mode": "local",
        }
        summary = launch_goal(
            store,
            goal_text=goal_text,
            completion_contract={
                "interpretation": "Complete when focused evidence passes.",
                "required_evidence": ["Focused evidence passes."],
                "user_confirmed_when_ambiguous": True,
            },
            guards={
                "max_continue_passes": 2,
                "deadline_at": "2099-01-01T00:00:00Z",
            },
            repository_binding=binding,
            repository_observation=dict(binding),
            initial_fingerprint=HASH_A,
            authorization={"fresh_recursive_threads_explicitly_requested": True},
            capabilities={
                "agentjob_control": True,
                "goal_state": True,
                "continuation_envelope": True,
                "repository_provider": True,
                "thread_provider": True,
            },
            provider=provider,
            predecessor_thread_id="thread-launcher",
            canonical_state={"fingerprint": HASH_A},
            progress_summary="Initialized.",
            remaining_work="Run one bounded generation.",
            timestamp=TS,
            launcher_token="l" * 48,
            handoff_token="h" * 48,
        )
        return store, summary

    def authority(self, root: Path):
        (root / "src").mkdir(exist_ok=True)
        (root / "tests").mkdir(exist_ok=True)
        (root / "src/example.py").write_text("value = 1\n", encoding="utf-8")
        job = valid_job()
        role = valid_role()
        return compile_authority(
            project_root=root,
            job=job,
            execution_role=role,
            activated_record_ids={job["job_id"], role["execution_role_id"]},
            runtime_capabilities=EXECUTION_CAPABILITIES,
        )

    def test_cli_surface_has_manual_safe_path_and_stops_at_successor_intent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            manual = ManualThreadProvider(root, current_thread_id="thread-launcher", timestamp=TS)
            provider = select_thread_provider(
                configured_provider="auto",
                strategy="fresh_summary",
                providers=[],
                manual_provider=manual,
            )
            store, summary = self.launch(root, provider)
            self.assertEqual(summary.status, "manual_handoff_pending")
            self.assertEqual(summary.state_phase, "successor_intent")
            self.assertEqual(summary.agentjobs_executed, 0)
            self.assertEqual(store.load_goal(summary.goal_id)["state"]["phase"], "successor_intent")
            self.assertTrue((root / summary.manual_handoff_path).is_file())

    def test_desktop_surface_uses_explicit_app_server_capability_and_persists_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            transport = SurfaceTransport()
            automatic = CodexAppServerThreadProvider(transport)
            provider = select_thread_provider(
                configured_provider="codex-app-server",
                strategy="fresh_summary",
                providers=[automatic],
            )
            store, summary = self.launch(root, provider)
            self.assertEqual(summary.state_phase, "successor_created")
            self.assertEqual(
                store.load_goal(summary.goal_id)["handoff"]["successor_thread_id"],
                "thread-desktop",
            )
            self.assertEqual(
                [operation for operation, _ in transport.calls].count("thread.start"), 1
            )

    def test_ide_permission_profile_uses_local_enforcement_for_optional_coarse_gap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            authority = self.authority(root)
            profile = CodexRuntimeCapabilities(
                surface="ide",
                working_directory=True,
                writable_roots=True,
                network_control=True,
                approval_policy=True,
                tool_allowlist=True,
                required_skill_mentions=True,
                command_budget=False,
                fine_grained_path_exclusions=False,
            )
            plan = compile_codex_permissions(authority, capabilities=profile)
            self.assertEqual(plan.status, "ready_with_local_enforcement")
            self.assertTrue(plan.requires_local_executor)
            self.assertTrue(plan.post_execution_path_validation_required)

    def test_mirror_enabled_and_disabled_never_change_canonical_record(self) -> None:
        record = valid_goal()
        before = dict(record["state"])
        mirror = build_goal_mirror(
            record,
            canonical_ref=".local/sys4ai/continuation/state.sqlite3",
            concise_summary="Surface relay.",
            timestamp=TS,
        )
        enabled = CodexNativeGoalProvider(MirrorTransport(), timestamp=TS)
        self.assertEqual(enabled.set_mirror("thread-1", mirror).status, "pass")
        disabled = CodexNativeGoalProvider(None, enabled=False, timestamp=TS)
        self.assertEqual(disabled.set_mirror("thread-1", mirror).status, "unavailable")
        self.assertEqual(record["state"], before)
        self.assertFalse(mirror["may_mark_complete"])

    def test_missing_provider_or_degraded_mandatory_capability_stops_safely(self) -> None:
        with self.assertRaises(BootstrapRequired):
            select_thread_provider(
                configured_provider="auto",
                strategy="fresh_summary",
                providers=[],
            )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            authority = self.authority(root)
            profile = CodexRuntimeCapabilities(
                surface="desktop",
                working_directory=True,
                writable_roots=True,
                network_control=False,
                approval_policy=True,
                tool_allowlist=True,
                required_skill_mentions=True,
                command_budget=True,
                fine_grained_path_exclusions=True,
            )
            with self.assertRaises(BootstrapRequired):
                compile_codex_permissions(authority, capabilities=profile)

    def test_secret_like_goal_never_reaches_thread_prompt_or_mirror(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            transport = SurfaceTransport()
            provider = CodexAppServerThreadProvider(transport)
            with self.assertRaises(RecordValidationError):
                self.launch(
                    root,
                    provider,
                    goal_text="Use api_key=super-secret-value-1234567890 to finish.",
                )
            self.assertEqual(
                [operation for operation, _ in transport.calls].count("thread.start"), 0
            )
        with self.assertRaises(RecordValidationError):
            build_goal_mirror(
                valid_goal(),
                canonical_ref="state.sqlite3",
                concise_summary="Use sk-secretvalue123456789 to finish.",
            )

    def test_documentation_uses_capabilities_not_private_mandatory_tool_names(self) -> None:
        root = Path(__file__).resolve().parents[3]
        paths = (
            root / "docs/skills/CODEX_CONTINUATION_INTEGRATION.md",
            root / "skills/continue-goal/examples/codex-manual-handoff.md",
            root / "skills/continue-goal/examples/codex-app-server.md",
        )
        payload = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertNotIn("codex_app__", payload)
        self.assertNotIn("functions.create_thread", payload)
        self.assertIn("Authority limitation", payload)
        self.assertIn("Evidence limitation", payload)


if __name__ == "__main__":
    unittest.main()
