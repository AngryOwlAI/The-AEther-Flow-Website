from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[1]
CORPUS_ROOT = SKILL_ROOT / "tests" / "fixtures" / "phase-02"
MATRIX_PATH = CORPUS_ROOT / "coverage-matrix.json"
PLANCTL = SKILL_ROOT / "scripts" / "planctl.py"
BUILDER = SKILL_ROOT / "scripts" / "build_phase02_fixture_corpus.py"
AGENTJOB_SCRIPTS = SKILL_ROOT.parent / "agentjob-control" / "scripts"
if str(AGENTJOB_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AGENTJOB_SCRIPTS))

from agentjob_runtime.records.canonical import content_sha256
from agentjob_runtime.security import contains_secret


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _diff_paths(prior: Any, current: Any, path: str = "$") -> list[str]:
    if isinstance(prior, dict) and isinstance(current, dict):
        result: list[str] = []
        for key in sorted(set(prior) | set(current)):
            child = f"{path}.{key}"
            if key not in prior or key not in current:
                result.append(child)
            else:
                result.extend(_diff_paths(prior[key], current[key], child))
        return result
    if isinstance(prior, list) and isinstance(current, list):
        if len(prior) != len(current):
            return [path]
        result = []
        for index, (left, right) in enumerate(zip(prior, current, strict=True)):
            result.extend(_diff_paths(left, right, f"{path}[{index}]"))
        return result
    return [] if prior == current else [path]


class Phase02FixtureCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = _load_json(MATRIX_PATH)
        cls.contract_semantics = _load_module(
            "phase02_contract_semantics",
            SKILL_ROOT / "scripts" / "contract_semantics.py",
        )
        cls.planctl = _load_module(
            "phase02_planctl",
            PLANCTL,
        )

    def run_planctl(self, *arguments: str) -> tuple[int, dict[str, Any]]:
        result = subprocess.run(
            [sys.executable, str(PLANCTL), *arguments, "--json"],
            check=False,
            capture_output=True,
            text=True,
            cwd=REPOSITORY_ROOT,
        )
        try:
            body = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            self.fail(
                f"planctl returned non-JSON output for {arguments}: "
                f"{error}; stdout={result.stdout!r}; stderr={result.stderr!r}"
            )
        return result.returncode, body

    def test_builder_check_is_read_only_and_all_hashes_match(self) -> None:
        paths = [
            CORPUS_ROOT / item["path"]
            for item in self.matrix["files"]
        ] + [MATRIX_PATH]
        before = {
            path.relative_to(CORPUS_ROOT).as_posix(): (
                path.read_bytes(),
                path.stat().st_mtime_ns,
            )
            for path in paths
        }
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check", "--json"],
            check=False,
            capture_output=True,
            text=True,
            cwd=REPOSITORY_ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        body = json.loads(result.stdout)
        self.assertEqual(body["status"], "valid")
        self.assertFalse(body["write_performed"])
        self.assertEqual(body["missing"], [])
        self.assertEqual(body["drifted"], [])
        self.assertEqual(body["extra"], [])

        after = {
            path.relative_to(CORPUS_ROOT).as_posix(): (
                path.read_bytes(),
                path.stat().st_mtime_ns,
            )
            for path in paths
        }
        self.assertEqual(after, before)

        entries = self.matrix["files"]
        self.assertEqual(
            [item["path"] for item in entries],
            sorted(item["path"] for item in entries),
        )
        for item in entries:
            with self.subTest(path=item["path"]):
                value = (CORPUS_ROOT / item["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(value).hexdigest(), item["sha256"])
                self.assertFalse(contains_secret(value.decode("utf-8")))
        self.assertEqual(
            self.matrix["corpus_sha256"],
            content_sha256(entries),
        )

    def test_coverage_matrix_matches_every_declared_enum(self) -> None:
        coverage = self.matrix["coverage"]
        state_schema = _load_json(
            SKILL_ROOT / "schemas" / "implementation-plan-state.schema.json"
        )
        receipt_schema = _load_json(
            SKILL_ROOT / "schemas" / "plan-task-receipt.schema.json"
        )
        provider_schema = _load_json(
            SKILL_ROOT / "schemas" / "provider-intent.schema.json"
        )
        supersession_schema = _load_json(
            SKILL_ROOT / "schemas" / "plan-task-supersession.schema.json"
        )
        amendment_schema = _load_json(
            SKILL_ROOT / "schemas" / "plan-amendment.schema.json"
        )
        normalization_schema = _load_json(
            SKILL_ROOT / "schemas" / "normalization-report.schema.json"
        )
        selection_schema = _load_json(
            SKILL_ROOT / "schemas" / "selection-proof.schema.json"
        )
        offline_control = _load_module(
            "phase02_offline_control",
            SKILL_ROOT / "scripts" / "offline_control.py",
        )

        expected = {
            "schema_versions": set(offline_control.SCHEMA_PROFILES),
            "source_classes": set(self.planctl.SOURCE_CLASSES),
            "plan_phases": set(
                state_schema["$defs"]["planPhase"]["enum"]
            ),
            "task_statuses": set(
                state_schema["$defs"]["taskLifecycle"]["properties"]["status"][
                    "enum"
                ]
            ),
            "receipt_dispositions": set(
                receipt_schema["$defs"]["disposition"]["enum"]
            ),
            "receipt_execution_outcomes": set(
                receipt_schema["$defs"]["executionEvidence"]["properties"][
                    "outcome"
                ]["enum"]
            ),
            "provider_outcomes": set(
                provider_schema["properties"]["status"]["enum"]
            ),
            "supersession_terminal_statuses": set(
                supersession_schema["$defs"]["originalTask"]["properties"][
                    "terminal_status"
                ]["enum"]
            ),
            "supersession_reason_codes": set(
                supersession_schema["properties"]["reason_code"]["enum"]
            ),
            "amendment_effects": set(
                amendment_schema["$defs"]["operation"]["properties"]["effect"][
                    "enum"
                ]
            ),
            "normalization_statuses": set(
                normalization_schema["properties"]["status"]["enum"]
            ),
            "selection_outcomes": set(
                selection_schema["properties"]["outcome"]["enum"]
            ),
        }
        self.assertEqual(set(coverage), set(expected))
        for dimension, values in expected.items():
            with self.subTest(dimension=dimension):
                self.assertEqual(set(coverage[dimension]), values)

        positive = self.matrix["positive_record_cases"]
        observed_dimensions = {
            key: {
                case["dimensions"][key]
                for case in positive
                if key in case["dimensions"]
            }
            for key in (
                "plan_phase",
                "receipt_disposition",
                "receipt_execution_outcome",
                "provider_outcome",
                "supersession_terminal_status",
                "supersession_reason_code",
                "amendment_effect",
                "normalization_status",
                "selection_outcome",
            )
        }
        expected_dimension_names = {
            "plan_phase": "plan_phases",
            "receipt_disposition": "receipt_dispositions",
            "receipt_execution_outcome": "receipt_execution_outcomes",
            "provider_outcome": "provider_outcomes",
            "supersession_terminal_status": "supersession_terminal_statuses",
            "supersession_reason_code": "supersession_reason_codes",
            "amendment_effect": "amendment_effects",
            "normalization_status": "normalization_statuses",
            "selection_outcome": "selection_outcomes",
        }
        for dimension, coverage_name in expected_dimension_names.items():
            with self.subTest(dimension=dimension):
                self.assertEqual(
                    observed_dimensions[dimension],
                    set(coverage[coverage_name]),
                )

        state_cases = [
            _load_json(CORPUS_ROOT / case["path"])
            for case in positive
            if case["record_profile"] == "implementation_plan_state"
        ]
        self.assertEqual(
            {
                task["status"]
                for state in state_cases
                for task in state["tasks"]
            },
            set(coverage["task_statuses"]),
        )
        self.assertEqual(
            {
                _load_json(CORPUS_ROOT / case["path"])["schema_version"]
                for case in positive
            },
            set(coverage["schema_versions"]),
        )

    def test_all_source_classes_route_deterministically(self) -> None:
        observed: set[str] = set()
        for case in self.matrix["source_cases"]:
            with self.subTest(case=case["case_id"]):
                paths = [
                    (CORPUS_ROOT / item)
                    .relative_to(REPOSITORY_ROOT)
                    .as_posix()
                    for item in case["paths"]
                ]
                code, body = self.run_planctl(
                    "classify",
                    *paths,
                    "--source-root",
                    ".",
                )
                self.assertEqual(code, 0)
                self.assertEqual(body["source_set_class"], case["source_class"])
                observed.add(case["source_class"])
        self.assertEqual(
            observed,
            set(self.matrix["coverage"]["source_classes"]),
        )

    def test_all_positive_records_validate_standalone(self) -> None:
        for case in self.matrix["positive_record_cases"]:
            with self.subTest(case=case["case_id"]):
                path = CORPUS_ROOT / case["path"]
                code, body = self.run_planctl(
                    "validate-record",
                    str(path),
                )
                self.assertEqual(code, 0, body)
                self.assertEqual(body["status"], "valid")
                self.assertEqual(
                    body["record_profile"],
                    case["record_profile"],
                )
                self.assertEqual(body["findings"], [])

    def test_schema_negatives_are_one_fault_per_file_and_fail_closed(self) -> None:
        for case in self.matrix["schema_negative_cases"]:
            with self.subTest(case=case["case_id"]):
                prior = _load_json(CORPUS_ROOT / case["base_path"])
                current = _load_json(CORPUS_ROOT / case["path"])
                self.assertEqual(
                    _diff_paths(prior, current),
                    [case["fault_path"]],
                )
                code, body = self.run_planctl(
                    "validate-record",
                    str(CORPUS_ROOT / case["path"]),
                )
                self.assertEqual(code, 1, body)
                self.assertEqual(body["status"], "invalid")
                observed = {
                    finding["code"] for finding in body["findings"]
                }
                self.assertTrue(
                    set(case["expected_reason_codes"]) <= observed,
                    (case["expected_reason_codes"], observed),
                )

    def test_semantic_negatives_are_one_fault_per_file_and_fail_closed(self) -> None:
        base_records = {
            record_key: _load_json(CORPUS_ROOT / path)
            for record_key, path in self.matrix["semantic_contract_set"].items()
        }
        self.assertEqual(
            self.contract_semantics.validate_contract_set(base_records),
            [],
        )
        for case in self.matrix["semantic_negative_cases"]:
            with self.subTest(case=case["case_id"]):
                prior = _load_json(CORPUS_ROOT / case["base_path"])
                current = _load_json(CORPUS_ROOT / case["path"])
                self.assertEqual(
                    _diff_paths(prior, current),
                    [case["fault_path"]],
                )
                records = json.loads(json.dumps(base_records))
                records[case["record_key"]] = current
                findings = set(
                    self.contract_semantics.validate_contract_set(records)
                )
                self.assertTrue(
                    set(case["expected_reason_codes"]) <= findings,
                    (case["expected_reason_codes"], findings),
                )

    def test_profile_semantic_negatives_are_one_fault_and_fail_closed(
        self,
    ) -> None:
        base_records = {
            record_key: _load_json(CORPUS_ROOT / path)
            for record_key, path in self.matrix[
                "profile_semantic_contract_set"
            ].items()
        }
        self.assertEqual(
            self.contract_semantics.validate_profile_contract_set(
                base_records
            ),
            [],
        )
        for case in self.matrix["profile_semantic_negative_cases"]:
            with self.subTest(case=case["case_id"]):
                prior = _load_json(CORPUS_ROOT / case["base_path"])
                current = _load_json(CORPUS_ROOT / case["path"])
                self.assertEqual(
                    _diff_paths(prior, current),
                    [case["fault_path"]],
                )
                records = json.loads(json.dumps(base_records))
                records[case["record_key"]] = current
                findings = set(
                    self.contract_semantics.validate_profile_contract_set(
                        records
                    )
                )
                self.assertTrue(
                    set(case["expected_reason_codes"]) <= findings,
                    (case["expected_reason_codes"], findings),
                )


if __name__ == "__main__":
    unittest.main()
