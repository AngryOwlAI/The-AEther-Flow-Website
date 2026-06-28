#!/usr/bin/env python3
"""Validate the public-comprehension dossier and diagram contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REQUIRED_DOSSIER_HEADINGS = [
    "## Route and reader job",
    "## Current page summary",
    "## Upstream source basis",
    "## Source-derived topic outline",
    "## Glossary",
    "## Claim boundaries and forbidden implications",
    "## Required comprehension blocks",
    "## Diagram contract",
    "## Equation walkthrough contract",
    "## Safe summary",
    "## Unsafe summary",
    "## New-page audit",
    "## Human review checklist",
    "## References",
]

RUNTIME_MERMAID_PATTERNS = [
    re.compile(r"<script[^>]+src=[\"'][^\"']*mermaid", re.IGNORECASE),
    re.compile(r"from\s+[\"']mermaid[\"']"),
    re.compile(r"import\s+[^\n]+[\"']mermaid[\"']"),
    re.compile(r"mermaid\.initialize", re.IGNORECASE),
    re.compile(r"@mermaid-js/mermaid(?!-cli)", re.IGNORECASE),
]


@dataclass(frozen=True)
class RemediatedRoute:
    route_path: str
    dossier: Path
    local_page_source: Path
    diagram_source: Path
    diagram_public_path: str
    manifest_id: str
    high_risk: bool = True


ROUTES = [
    RemediatedRoute(
        route_path="/project/overview/",
        dossier=Path("docs/content-dossiers/project-overview/dossier.md"),
        local_page_source=Path("src/pages/project/overview.astro"),
        diagram_source=Path(
            "docs/content-dossiers/project-overview/diagrams/two-track-project-map.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/project-overview-two-track-map.png",
        manifest_id="comprehension_project_overview_two_track_map",
    ),
    RemediatedRoute(
        route_path="/project/ai-research-agent-system/parent-child-synthesis/",
        dossier=Path("docs/content-dossiers/parent-child-synthesis/dossier.md"),
        local_page_source=Path(
            "src/pages/project/ai-research-agent-system/parent-child-synthesis/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/parent-child-synthesis/diagrams/"
            "single-outer-agentjob-frame.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png",
        manifest_id="comprehension_parent_child_single_outer_agentjob",
    ),
    RemediatedRoute(
        route_path="/project/physics/",
        dossier=Path("docs/content-dossiers/physics-track/dossier.md"),
        local_page_source=Path("src/pages/project/physics/index.astro"),
        diagram_source=Path("docs/content-dossiers/physics-track/diagrams/status-layer-map.mmd"),
        diagram_public_path="/assets/diagrams/comprehension/physics-track-status-map.png",
        manifest_id="comprehension_physics_track_status_map",
    ),
    RemediatedRoute(
        route_path="/project/physics/ontology/",
        dossier=Path("docs/content-dossiers/physics-ontology/dossier.md"),
        local_page_source=Path("src/pages/project/physics/ontology/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-ontology/diagrams/ontology-boundary-map.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-ontology-boundary-map.png",
        manifest_id="comprehension_physics_ontology_boundary_map",
    ),
    RemediatedRoute(
        route_path="/project/physics/exact-gr-benchmark/",
        dossier=Path("docs/content-dossiers/physics-exact-gr-benchmark/dossier.md"),
        local_page_source=Path("src/pages/project/physics/exact-gr-benchmark/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-exact-gr-benchmark/diagrams/benchmark-boundary-ladder.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-benchmark-boundary-ladder.png",
        manifest_id="comprehension_physics_benchmark_boundary_ladder",
    ),
    RemediatedRoute(
        route_path="/project/physics/gr-derivation-roadmap/",
        dossier=Path("docs/content-dossiers/physics-gr-derivation-roadmap/dossier.md"),
        local_page_source=Path("src/pages/project/physics/gr-derivation-roadmap/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-gr-derivation-roadmap/diagrams/burden-ladder.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-roadmap-burden-ladder.png",
        manifest_id="comprehension_physics_roadmap_burden_ladder",
    ),
    RemediatedRoute(
        route_path="/project/physics/claim-gates/",
        dossier=Path("docs/content-dossiers/physics-claim-gates/dossier.md"),
        local_page_source=Path("src/pages/project/physics/claim-gates/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-claim-gates/diagrams/claim-gates-lifecycle.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-claim-gates-lifecycle.png",
        manifest_id="comprehension_physics_claim_gates_lifecycle",
    ),
    RemediatedRoute(
        route_path="/project/physics/source-extension-pipeline/",
        dossier=Path("docs/content-dossiers/physics-source-extension-pipeline/dossier.md"),
        local_page_source=Path("src/pages/project/physics/source-extension-pipeline/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-source-extension-pipeline/diagrams/"
            "source-extension-pipeline.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-source-extension-pipeline.png",
        manifest_id="comprehension_physics_source_extension_pipeline",
    ),
    RemediatedRoute(
        route_path="/project/physics/gate-chair-and-human-gates/",
        dossier=Path("docs/content-dossiers/physics-gate-chair-and-human-gates/dossier.md"),
        local_page_source=Path("src/pages/project/physics/gate-chair-and-human-gates/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-gate-chair-and-human-gates/diagrams/"
            "human-gate-authority.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-gate-chair-human-gates.png",
        manifest_id="comprehension_physics_gate_chair_human_gates",
    ),
    RemediatedRoute(
        route_path="/project/physics/current-state/",
        dossier=Path("docs/content-dossiers/physics-current-state/dossier.md"),
        local_page_source=Path("src/pages/project/physics/current-state/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-current-state/diagrams/snapshot-boundary.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-current-state-snapshot-boundary.png",
        manifest_id="comprehension_physics_current_state_snapshot_boundary",
    ),
    RemediatedRoute(
        route_path="/project/physics/distance-to-gr/",
        dossier=Path("docs/content-dossiers/physics-distance-to-gr/dossier.md"),
        local_page_source=Path("src/pages/project/physics/distance-to-gr/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-distance-to-gr/diagrams/"
            "distance-dashboard-boundary.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-distance-to-gr-dashboard.png",
        manifest_id="comprehension_physics_distance_to_gr_dashboard",
    ),
    RemediatedRoute(
        route_path="/project/physics/metric-response-ladder/",
        dossier=Path("docs/content-dossiers/physics-metric-response-ladder/dossier.md"),
        local_page_source=Path("src/pages/project/physics/metric-response-ladder/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-metric-response-ladder/diagrams/"
            "metric-response-ladder.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-metric-response-ladder.png",
        manifest_id="comprehension_physics_metric_response_ladder",
    ),
    RemediatedRoute(
        route_path="/project/physics/finite-toy-models/",
        dossier=Path("docs/content-dossiers/physics-finite-toy-models/dossier.md"),
        local_page_source=Path("src/pages/project/physics/finite-toy-models/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/physics-finite-toy-models/diagrams/"
            "finite-toy-freeze.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-finite-toy-models.png",
        manifest_id="comprehension_physics_finite_toy_models",
    ),
    RemediatedRoute(
        route_path="/project/physics/no-target-import-discipline/",
        dossier=Path("docs/content-dossiers/physics-no-target-import-discipline/dossier.md"),
        local_page_source=Path(
            "src/pages/project/physics/no-target-import-discipline/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/physics-no-target-import-discipline/diagrams/"
            "no-target-import-discipline.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/physics-no-target-import-discipline.png",
        manifest_id="comprehension_physics_no_target_import_discipline",
    ),
    RemediatedRoute(
        route_path="/project/physics/negative-results-and-frozen-routes/",
        dossier=Path("docs/content-dossiers/physics-negative-results-and-frozen-routes/dossier.md"),
        local_page_source=Path(
            "src/pages/project/physics/negative-results-and-frozen-routes/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/physics-negative-results-and-frozen-routes/diagrams/"
            "negative-results-freeze-flow.mmd"
        ),
        diagram_public_path=(
            "/assets/diagrams/comprehension/physics-negative-results-and-frozen-routes.png"
        ),
        manifest_id="comprehension_physics_negative_results_frozen_routes",
    ),
    RemediatedRoute(
        route_path="/project/ai-research-agent-system/",
        dossier=Path("docs/content-dossiers/ai-research-agent-system/dossier.md"),
        local_page_source=Path("src/pages/project/ai-research-agent-system/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/ai-research-agent-system/diagrams/"
            "task-authority-review-map.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/ai-system-task-authority-map.png",
        manifest_id="comprehension_ai_system_task_authority_map",
    ),
    RemediatedRoute(
        route_path="/project/ai-research-agent-system/workflow/",
        dossier=Path("docs/content-dossiers/ai-workflow/dossier.md"),
        local_page_source=Path("src/pages/project/ai-research-agent-system/workflow/index.astro"),
        diagram_source=Path("docs/content-dossiers/ai-workflow/diagrams/bounded-agentjob-chain.mmd"),
        diagram_public_path="/assets/diagrams/comprehension/ai-workflow-bounded-agentjob-chain.png",
        manifest_id="comprehension_ai_workflow_bounded_agentjob_chain",
    ),
    RemediatedRoute(
        route_path="/project/ai-research-agent-system/one-bounded-agentjob/",
        dossier=Path("docs/content-dossiers/ai-one-bounded-agentjob/dossier.md"),
        local_page_source=Path(
            "src/pages/project/ai-research-agent-system/one-bounded-agentjob/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/ai-one-bounded-agentjob/diagrams/"
            "one-agentjob-envelope.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/ai-one-bounded-agentjob-envelope.png",
        manifest_id="comprehension_ai_one_bounded_agentjob_envelope",
    ),
    RemediatedRoute(
        route_path="/project/ai-research-agent-system/roles-and-skills/",
        dossier=Path("docs/content-dossiers/ai-roles-and-skills/dossier.md"),
        local_page_source=Path(
            "src/pages/project/ai-research-agent-system/roles-and-skills/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/ai-roles-and-skills/diagrams/role-authority-stack.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/ai-roles-authority-stack.png",
        manifest_id="comprehension_ai_roles_authority_stack",
    ),
    RemediatedRoute(
        route_path="/project/ai-research-agent-system/role-authority-inspector/",
        dossier=Path("docs/content-dossiers/ai-role-authority-inspector/dossier.md"),
        local_page_source=Path(
            "src/pages/project/ai-research-agent-system/role-authority-inspector/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/ai-role-authority-inspector/diagrams/"
            "role-authority-inspection-stack.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/ai-role-authority-inspector-stack.png",
        manifest_id="comprehension_ai_role_authority_inspector_stack",
    ),
    RemediatedRoute(
        route_path="/project/ai-research-agent-system/memory-registries/",
        dossier=Path("docs/content-dossiers/ai-memory-registries/dossier.md"),
        local_page_source=Path(
            "src/pages/project/ai-research-agent-system/memory-registries/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/ai-memory-registries/diagrams/source-first-memory-layers.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/ai-memory-source-first-layers.png",
        manifest_id="comprehension_ai_memory_source_first_layers",
    ),
    RemediatedRoute(
        route_path="/project/operations/",
        dossier=Path("docs/content-dossiers/operations/dossier.md"),
        local_page_source=Path("src/pages/project/operations/index.astro"),
        diagram_source=Path("docs/content-dossiers/operations/diagrams/operations-control-spine.mmd"),
        diagram_public_path="/assets/diagrams/comprehension/operations-control-spine.png",
        manifest_id="comprehension_operations_control_spine",
    ),
    RemediatedRoute(
        route_path="/project/operations/director-agentjob-lifecycle/",
        dossier=Path("docs/content-dossiers/operations-director-agentjob-lifecycle/dossier.md"),
        local_page_source=Path("src/pages/project/operations/director-agentjob-lifecycle/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/operations-director-agentjob-lifecycle/diagrams/"
            "director-agentjob-record-chain.mmd"
        ),
        diagram_public_path=(
            "/assets/diagrams/comprehension/operations-director-agentjob-record-chain.png"
        ),
        manifest_id="comprehension_operations_director_agentjob_record_chain",
    ),
    RemediatedRoute(
        route_path="/project/operations/role-routing/",
        dossier=Path("docs/content-dossiers/operations-role-routing/dossier.md"),
        local_page_source=Path("src/pages/project/operations/role-routing/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/operations-role-routing/diagrams/role-routing-allowlist-stack.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/operations-role-routing-allowlist-stack.png",
        manifest_id="comprehension_operations_role_routing_allowlist_stack",
    ),
    RemediatedRoute(
        route_path="/project/operations/validator-operator-workflow/",
        dossier=Path("docs/content-dossiers/operations-validator-operator-workflow/dossier.md"),
        local_page_source=Path("src/pages/project/operations/validator-operator-workflow/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/operations-validator-operator-workflow/diagrams/"
            "validator-pass-boundary.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/operations-validator-pass-boundary.png",
        manifest_id="comprehension_operations_validator_pass_boundary",
    ),
    RemediatedRoute(
        route_path="/project/operations/publication-process/",
        dossier=Path("docs/content-dossiers/operations-publication-process/dossier.md"),
        local_page_source=Path("src/pages/project/operations/publication-process/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/operations-publication-process/diagrams/"
            "publication-source-review-flow.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/operations-publication-review-flow.png",
        manifest_id="comprehension_operations_publication_review_flow",
    ),
    RemediatedRoute(
        route_path="/project/operations/project-system-improvement/",
        dossier=Path("docs/content-dossiers/operations-project-system-improvement/dossier.md"),
        local_page_source=Path("src/pages/project/operations/project-system-improvement/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/operations-project-system-improvement/diagrams/"
            "project-system-improvement-loop.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/operations-project-system-improvement-loop.png",
        manifest_id="comprehension_operations_project_system_improvement_loop",
    ),
    RemediatedRoute(
        route_path="/project/operations/technical-requirements/",
        dossier=Path("docs/content-dossiers/operations-technical-requirements/dossier.md"),
        local_page_source=Path("src/pages/project/operations/technical-requirements/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/operations-technical-requirements/diagrams/"
            "technical-tool-authority-tiers.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/operations-technical-tool-tiers.png",
        manifest_id="comprehension_operations_technical_tool_tiers",
    ),
    RemediatedRoute(
        route_path="/project/source-authority/",
        dossier=Path("docs/content-dossiers/source-authority/dossier.md"),
        local_page_source=Path("src/pages/project/source-authority/index.astro"),
        diagram_source=Path("docs/content-dossiers/source-authority/diagrams/source-authority-ladder.mmd"),
        diagram_public_path="/assets/diagrams/comprehension/source-authority-ladder.png",
        manifest_id="comprehension_source_authority_ladder",
    ),
    RemediatedRoute(
        route_path="/project/source-authority/claim-boundary-explorer/",
        dossier=Path("docs/content-dossiers/source-authority-claim-boundary-explorer/dossier.md"),
        local_page_source=Path(
            "src/pages/project/source-authority/claim-boundary-explorer/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/source-authority-claim-boundary-explorer/diagrams/"
            "claim-boundary-explorer.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/source-authority-claim-boundary-explorer.png",
        manifest_id="comprehension_source_authority_claim_boundary_explorer",
    ),
    RemediatedRoute(
        route_path="/project/source-authority/publication-and-provenance-system/",
        dossier=Path("docs/content-dossiers/source-authority-publication-and-provenance-system/dossier.md"),
        local_page_source=Path(
            "src/pages/project/source-authority/publication-and-provenance-system/index.astro"
        ),
        diagram_source=Path(
            "docs/content-dossiers/source-authority-publication-and-provenance-system/"
            "diagrams/publication-provenance-system.mmd"
        ),
        diagram_public_path=(
            "/assets/diagrams/comprehension/"
            "source-authority-publication-provenance-system.png"
        ),
        manifest_id="comprehension_source_authority_publication_provenance_system",
    ),
    RemediatedRoute(
        route_path="/resources/guided-starts/general-public/",
        dossier=Path("docs/content-dossiers/guided-start-general-public/dossier.md"),
        local_page_source=Path("src/pages/resources/guided-starts/general-public/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/guided-start-general-public/diagrams/"
            "general-public-guided-start.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/general-public-guided-start.png",
        manifest_id="comprehension_general_public_guided_start",
    ),
    RemediatedRoute(
        route_path="/resources/guided-starts/",
        dossier=Path("docs/content-dossiers/guided-start-specialists/dossier.md"),
        local_page_source=Path("src/pages/resources/guided-starts/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/guided-start-specialists/diagrams/"
            "specialist-guided-starts.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/specialist-guided-starts.png",
        manifest_id="comprehension_specialist_guided_starts",
    ),
    RemediatedRoute(
        route_path="/resources/reviewer-packet/",
        dossier=Path("docs/content-dossiers/reviewer-packet/dossier.md"),
        local_page_source=Path("src/pages/resources/reviewer-packet/index.astro"),
        diagram_source=Path(
            "docs/content-dossiers/reviewer-packet/diagrams/reviewer-inspection-order.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/reviewer-inspection-order.png",
        manifest_id="comprehension_reviewer_inspection_order",
    ),
    RemediatedRoute(
        route_path="/resources/",
        dossier=Path("docs/content-dossiers/resources-index/dossier.md"),
        local_page_source=Path("src/pages/resources/index.astro"),
        diagram_source=Path("docs/content-dossiers/resources-index/diagrams/resource-manifest-chain.mmd"),
        diagram_public_path="/assets/diagrams/comprehension/resources-manifest-chain.png",
        manifest_id="comprehension_resources_manifest_chain",
    ),
    RemediatedRoute(
        route_path="/resources/documents/",
        dossier=Path("docs/content-dossiers/resources-documents/dossier.md"),
        local_page_source=Path("src/pages/resources/documents.astro"),
        diagram_source=Path(
            "docs/content-dossiers/resources-documents/diagrams/tex-pdf-derivative-chain.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/resources-tex-pdf-derivative-chain.png",
        manifest_id="comprehension_resources_tex_pdf_derivative_chain",
    ),
    RemediatedRoute(
        route_path="/resources/diagrams/",
        dossier=Path("docs/content-dossiers/resources-diagrams/dossier.md"),
        local_page_source=Path("src/pages/resources/diagrams.astro"),
        diagram_source=Path(
            "docs/content-dossiers/resources-diagrams/diagrams/diagram-publication-boundary.mmd"
        ),
        diagram_public_path="/assets/diagrams/comprehension/resources-diagram-publication-boundary.png",
        manifest_id="comprehension_resources_diagram_publication_boundary",
    ),
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return data


def public_path_to_file(public_dir: Path, site_path: str) -> Path:
    if not site_path.startswith("/"):
        raise ValueError(f"{site_path}: public path must start with '/'")
    relative = Path(site_path.removeprefix("/"))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{site_path}: public path must stay inside public/")
    return public_dir / relative


def manifest_ids(source_manifest: dict[str, Any]) -> set[str]:
    return {
        item["id"]
        for item in source_manifest.get("items", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def manifest_paths(asset_manifest: dict[str, Any]) -> set[str]:
    return {
        item["path"]
        for item in asset_manifest.get("items", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }


def validate_dossier(route: RemediatedRoute, repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / route.dossier
    if not path.is_file():
        return [f"{route.route_path}: missing dossier {route.dossier}"]

    text = path.read_text(encoding="utf-8")
    for heading in REQUIRED_DOSSIER_HEADINGS:
        if heading not in text:
            errors.append(f"{route.dossier}: missing required heading {heading!r}")

    required_terms = [
        str(route.diagram_source),
        route.diagram_public_path,
        route.manifest_id,
        "Alt text",
        "Caption",
        "Human review status:",
    ]
    for term in required_terms:
        if term not in text:
            errors.append(f"{route.dossier}: missing required diagram/review metadata {term!r}")

    if route.high_risk:
        for marker in ["Safe summary:", "Unsafe summary:"]:
            if marker not in text:
                errors.append(f"{route.dossier}: high-risk route missing {marker!r}")

    if "No equation walkthrough required" not in text and "symbol" not in text.lower():
        errors.append(
            f"{route.dossier}: equation contract must explicitly state no walkthrough "
            "is required or define walkthrough data"
        )

    return errors


def validate_diagram(route: RemediatedRoute, repo_root: Path, public_dir: Path) -> list[str]:
    errors: list[str] = []
    source = repo_root / route.diagram_source
    if not source.is_file():
        errors.append(f"{route.route_path}: missing Mermaid source {route.diagram_source}")
    elif not source.read_text(encoding="utf-8").strip():
        errors.append(f"{route.diagram_source}: Mermaid source is empty")

    try:
        output = public_path_to_file(public_dir, route.diagram_public_path)
    except ValueError as exc:
        return errors + [f"{route.route_path}: {exc}"]
    if not output.is_file():
        errors.append(f"{route.route_path}: missing generated diagram {route.diagram_public_path}")
    elif output.stat().st_size <= 0:
        errors.append(f"{route.diagram_public_path}: generated diagram is empty")
    return errors


def validate_runtime_mermaid(repo_root: Path) -> list[str]:
    errors: list[str] = []
    checked_roots = [repo_root / "src", repo_root / "public"]
    for root in checked_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_dir():
                continue
            if path.suffix.lower() not in {".astro", ".ts", ".js", ".mjs", ".mdx", ".html"}:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in RUNTIME_MERMAID_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{path.relative_to(repo_root)}: public Mermaid runtime marker")
    return errors


def validate_route_wiring(route: RemediatedRoute, repo_root: Path) -> list[str]:
    errors: list[str] = []
    page = repo_root / route.local_page_source
    if not page.is_file():
        return [f"{route.route_path}: missing page source {route.local_page_source}"]

    lib_sources = [
        path.relative_to(repo_root)
        for path in sorted((repo_root / "src/lib").glob("*.ts"))
        if path.is_file()
    ]
    searchable_files = [
        route.local_page_source,
        Path("src/components/ComprehensionBlocks.astro"),
        *lib_sources,
    ]
    combined = "\n".join(
        (repo_root / path).read_text(encoding="utf-8")
        for path in searchable_files
        if (repo_root / path).is_file()
    )
    for marker in [route.diagram_public_path, "Safe summary", "Unsafe summary"]:
        if marker not in combined:
            errors.append(f"{route.route_path}: page/comprehension model missing {marker!r}")
    return errors


def validate_manifests(
    route: RemediatedRoute,
    source_manifest: dict[str, Any],
    asset_manifest: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    ids = manifest_ids(source_manifest)
    paths = manifest_paths(asset_manifest)
    if route.manifest_id not in ids:
        errors.append(f"{route.route_path}: source_manifest missing {route.manifest_id}")
    if route.diagram_public_path not in paths:
        errors.append(f"{route.route_path}: asset_manifest missing {route.diagram_public_path}")
    return errors


def validate_human_review(repo_root: Path) -> list[str]:
    errors: list[str] = []
    quality_dir = repo_root / "docs/quality"
    if not quality_dir.is_dir():
        return ["docs/quality: missing quality directory"]

    quality_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(quality_dir.glob("*.md"))
        if path.is_file()
    )
    if "Human review status" not in quality_text:
        errors.append("docs/quality: missing human review status note")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--public-dir", type=Path, default=Path("public"))
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=Path("public/files/manifests/source_manifest.json"),
    )
    parser.add_argument(
        "--asset-manifest",
        type=Path,
        default=Path("public/files/manifests/asset_manifest.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    public_dir = args.public_dir if args.public_dir.is_absolute() else repo_root / args.public_dir
    source_manifest_path = (
        args.source_manifest
        if args.source_manifest.is_absolute()
        else repo_root / args.source_manifest
    )
    asset_manifest_path = (
        args.asset_manifest
        if args.asset_manifest.is_absolute()
        else repo_root / args.asset_manifest
    )

    source_manifest = load_json(source_manifest_path)
    asset_manifest = load_json(asset_manifest_path)

    errors: list[str] = []
    for route in ROUTES:
        errors.extend(validate_dossier(route, repo_root))
        errors.extend(validate_diagram(route, repo_root, public_dir))
        errors.extend(validate_route_wiring(route, repo_root))
        errors.extend(validate_manifests(route, source_manifest, asset_manifest))

    errors.extend(validate_runtime_mermaid(repo_root))
    errors.extend(validate_human_review(repo_root))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Public comprehension validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
