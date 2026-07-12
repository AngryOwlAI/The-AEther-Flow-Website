from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOME_PAGE = REPO_ROOT / "src/pages/index.astro"
PHYSICS_PAGE = REPO_ROOT / "src/pages/physics/index.astro"
ROUTE_MAP = REPO_ROOT / "public/files/manifests/page_route_map.json"

EXPECTED_STATE_ORDER = [
    "interpretive",
    "adopted-effective",
    "complete-effective",
    "open-foundational",
    "governed-method",
]


def load_public_statements() -> list[dict[str, object]]:
    script = r"""
import { createServer } from "vite";

const server = await createServer({
  root: process.cwd(),
  server: { middlewareMode: true },
  appType: "custom",
  logLevel: "silent",
});

try {
  const module = await server.ssrLoadModule("/src/lib/publicClaimLadder.ts");
  process.stdout.write(JSON.stringify(module.resolvedPublicClaimLadder));
} finally {
  await server.close();
}
"""
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def route_record(route_path: str) -> dict[str, object]:
    route_map = json.loads(ROUTE_MAP.read_text(encoding="utf-8"))
    return next(route for route in route_map["routes"] if route["route_path"] == route_path)


def test_routes_consume_only_accepted_surface_statements() -> None:
    for path, surface in ((HOME_PAGE, "home"), (PHYSICS_PAGE, "physics")):
        source = path.read_text(encoding="utf-8")
        assert "resolvedPublicClaimLadder" in source
        assert 'statement.disposition === "accepted"' in source
        assert f'statement.surfaces.includes("{surface}")' in source
        assert ".exactWording" in source
        assert ".allowedQualification" in source

    statements = load_public_statements()
    for surface in ("home", "physics"):
        surface_statements = [
            item["statement"]
            for item in statements
            if surface in item["statement"]["surfaces"]
        ]
        assert len(surface_statements) == 6
        assert all(statement["disposition"] == "accepted" for statement in surface_statements)
        assert all(statement["allowedQualification"] for statement in surface_statements)


def test_routes_encode_the_authorized_positive_content_order() -> None:
    for path, prefix in ((HOME_PAGE, "home"), (PHYSICS_PAGE, "physics")):
        source = path.read_text(encoding="utf-8")
        sequence_start = source.index(f"const {prefix}PositioningSteps")
        sequence_end = source.index("] as const;", sequence_start)
        sequence = source[sequence_start:sequence_end]

        positions = [sequence.index(f'get("{state}")') for state in EXPECTED_STATE_ORDER]
        assert positions == sorted(positions)
        assert 'get("not-claimed")' in sequence

        rendered_sequence = source.index(f"{{{prefix}PositioningSteps.map")
        evidence = source.index("<SourceAuthoritySection", rendered_sequence)
        route_navigation = source.index("<ComprehensionBlocks", evidence)
        assert rendered_sequence < evidence < route_navigation


def test_route_metadata_is_source_safe_and_route_local() -> None:
    home = HOME_PAGE.read_text(encoding="utf-8")
    physics = PHYSICS_PAGE.read_text(encoding="utf-8")

    assert 'title="The Æther Flow Project | Exact Closure and Open Foundations"' in home
    assert 'title="Physics Research | Exact Closure and Open Foundations"' in physics
    assert "description={`${homeCurrentResult.exactWording} ${homeOpenFoundation.exactWording}`}" in home
    assert "description={`${physicsCurrentResult.exactWording} ${physicsOpenFoundation.exactWording}`}" in physics


def test_route_bundles_and_authority_classifications_remain_fixed() -> None:
    expected_sources = [
        "ontology/tex/aether_flow_exact_closure_sequence_overview.tex",
        "ontology/tex/aether_flow_exact_closure_note.tex",
        "ontology/tex/aether_flow_exact_closure_flagship_article.tex",
    ]
    for route_path in ("/", "/physics/"):
        route = route_record(route_path)
        assert route["adaptation_type"] == "curated_synthesis"
        assert route["upstream_authority_status"] == "generated_noncanonical"
        assert route["website_publication_status"] == "published"
        for source_path in expected_sources:
            assert source_path in route["upstream_source_paths"]


def test_route_copy_omits_reviewed_forbidden_overreads() -> None:
    source = HOME_PAGE.read_text(encoding="utf-8") + PHYSICS_PAGE.read_text(encoding="utf-8")
    forbidden = {
        overread.casefold()
        for item in load_public_statements()
        for overread in item["statement"]["forbiddenOverreads"]
    }
    assert all(overread not in source.casefold() for overread in forbidden)
