#!/usr/bin/env python3
"""Render dossier Mermaid diagrams into committed static PNG assets."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


MERMAID_CLI_PACKAGE = "@mermaid-js/mermaid-cli@11.15.0"


@dataclass(frozen=True)
class DiagramTarget:
    source: Path
    output: Path


DIAGRAMS = [
    DiagramTarget(
        source=Path("docs/content-dossiers/project-overview/diagrams/two-track-project-map.mmd"),
        output=Path("public/assets/diagrams/comprehension/project-overview-two-track-map.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/parent-child-synthesis/diagrams/"
            "single-outer-agentjob-frame.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/physics-track/diagrams/status-layer-map.mmd"),
        output=Path("public/assets/diagrams/comprehension/physics-track-status-map.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/physics-ontology/diagrams/ontology-boundary-map.mmd"),
        output=Path("public/assets/diagrams/comprehension/physics-ontology-boundary-map.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/physics-exact-gr-benchmark/diagrams/"
            "benchmark-boundary-ladder.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/physics-benchmark-boundary-ladder.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/physics-gr-derivation-roadmap/diagrams/burden-ladder.mmd"),
        output=Path("public/assets/diagrams/comprehension/physics-roadmap-burden-ladder.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/physics-claim-gates/diagrams/claim-gates-lifecycle.mmd"),
        output=Path("public/assets/diagrams/comprehension/physics-claim-gates-lifecycle.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/physics-current-state/diagrams/snapshot-boundary.mmd"),
        output=Path(
            "public/assets/diagrams/comprehension/physics-current-state-snapshot-boundary.png"
        ),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/ai-research-agent-system/diagrams/"
            "task-authority-review-map.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/ai-system-task-authority-map.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/ai-workflow/diagrams/bounded-agentjob-chain.mmd"),
        output=Path("public/assets/diagrams/comprehension/ai-workflow-bounded-agentjob-chain.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/ai-roles-and-skills/diagrams/role-authority-stack.mmd"),
        output=Path("public/assets/diagrams/comprehension/ai-roles-authority-stack.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/ai-memory-registries/diagrams/source-first-memory-layers.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/ai-memory-source-first-layers.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/operations/diagrams/operations-control-spine.mmd"),
        output=Path("public/assets/diagrams/comprehension/operations-control-spine.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/operations-director-agentjob-lifecycle/diagrams/"
            "director-agentjob-record-chain.mmd"
        ),
        output=Path(
            "public/assets/diagrams/comprehension/operations-director-agentjob-record-chain.png"
        ),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/operations-role-routing/diagrams/"
            "role-routing-allowlist-stack.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/operations-role-routing-allowlist-stack.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/operations-validator-operator-workflow/diagrams/"
            "validator-pass-boundary.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/operations-validator-pass-boundary.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/operations-publication-process/diagrams/"
            "publication-source-review-flow.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/operations-publication-review-flow.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/operations-project-system-improvement/diagrams/"
            "project-system-improvement-loop.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/operations-project-system-improvement-loop.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/operations-technical-requirements/diagrams/"
            "technical-tool-authority-tiers.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/operations-technical-tool-tiers.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/source-authority/diagrams/source-authority-ladder.mmd"),
        output=Path("public/assets/diagrams/comprehension/source-authority-ladder.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/resources-index/diagrams/resource-manifest-chain.mmd"),
        output=Path("public/assets/diagrams/comprehension/resources-manifest-chain.png"),
    ),
    DiagramTarget(
        source=Path("docs/content-dossiers/resources-documents/diagrams/tex-pdf-derivative-chain.mmd"),
        output=Path("public/assets/diagrams/comprehension/resources-tex-pdf-derivative-chain.png"),
    ),
    DiagramTarget(
        source=Path(
            "docs/content-dossiers/resources-diagrams/diagrams/diagram-publication-boundary.mmd"
        ),
        output=Path("public/assets/diagrams/comprehension/resources-diagram-publication-boundary.png"),
    ),
]


def render_diagram(target: DiagramTarget, *, repo_root: Path, package: str) -> None:
    source = repo_root / target.source
    output = repo_root / target.output
    if not source.is_file():
        raise FileNotFoundError(f"Missing Mermaid source: {target.source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    puppeteer_config = {
        "args": ["--no-sandbox", "--disable-setuid-sandbox"],
    }

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(puppeteer_config, handle)
        config_path = Path(handle.name)

    try:
        command = [
            "npx",
            "--yes",
            package,
            "-i",
            str(source),
            "-o",
            str(output),
            "-b",
            "#000000",
            "--scale",
            "2",
            "--puppeteerConfigFile",
            str(config_path),
        ]
        subprocess.run(command, cwd=repo_root, check=True)
    finally:
        config_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--package",
        default=os.environ.get("MERMAID_CLI_PACKAGE", MERMAID_CLI_PACKAGE),
        help="npm package spec passed to npx. Defaults to a pinned mermaid-cli package.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    for target in DIAGRAMS:
        render_diagram(target, repo_root=repo_root, package=args.package)
        print(f"Rendered {target.source} -> {target.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
