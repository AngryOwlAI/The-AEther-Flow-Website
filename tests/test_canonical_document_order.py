from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_PAGE = REPO_ROOT / "src/pages/documents/research/index.astro"
DOCUMENT_ACTIONS = REPO_ROOT / "src/components/DocumentActions.astro"

EXPECTED_SEQUENCE = [
    (1, "aether_flow_exact_closure_sequence_overview", "Exact Closure Sequence Overview", "canonical_front_door"),
    (2, "aether_flow_exact_closure_note", "Exact Closure Note", "ordered_core"),
    (3, "aether_flow_foundations", "Foundations", "ordered_core"),
    (4, "aether_flow_dynamics", "Dynamics", "ordered_core"),
    (5, "aether_flow_consistency", "Consistency", "ordered_core"),
    (6, "aether_flow_relativistic_recovery", "Relativistic Recovery", "ordered_core"),
    (7, "aether_flow_geometry", "Flow Geometry", "ordered_core"),
    (8, "aether_flow_exact_closure_flagship_article", "Exact Closure Flagship Article", "release_synthesis"),
]


def load_sequence_module_evidence() -> dict[str, object]:
    script = r"""
import { createServer } from "vite";

const server = await createServer({
  root: process.cwd(),
  server: { middlewareMode: true },
  appType: "custom",
  logLevel: "silent",
});

try {
  const module = await server.ssrLoadModule("/src/lib/manifests.ts");
  const sequence = module.ontologyDocumentSequence;
  const slugs = sequence.map((entry) => entry.slug);
  const failures = {};
  const capture = (name, candidateSequence, candidateSlugs) => {
    try {
      module.validateOntologyDocumentSequence(candidateSequence, candidateSlugs);
    } catch (error) {
      failures[name] = error.message;
    }
  };

  capture("duplicateAvailable", sequence, [...slugs, slugs[0]]);
  capture("duplicateSequence", [...sequence, sequence[0]], slugs);
  capture("missing", sequence, slugs.slice(1));
  capture("unexpected", sequence, [...slugs, "unexpected_document"]);
  capture(
    "ordinal",
    sequence.map((entry, index) => index === 0 ? { ...entry, ordinal: 2 } : entry),
    slugs,
  );

  process.stdout.write(JSON.stringify({
    sequence,
    documentSlugs: module.ontologyDocuments.map((document) => document.slug),
    failures,
  }));
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


def test_canonical_document_sequence_labels_slugs_positions_and_roles() -> None:
    evidence = load_sequence_module_evidence()
    sequence = evidence["sequence"]
    actual = [
        (entry["ordinal"], entry["slug"], entry["title"], entry["role"])
        for entry in sequence
    ]

    assert actual == EXPECTED_SEQUENCE
    assert evidence["documentSlugs"] == [item[1] for item in EXPECTED_SEQUENCE]
    assert len({item[1] for item in EXPECTED_SEQUENCE}) == 8


def test_canonical_document_sequence_fails_closed() -> None:
    failures = load_sequence_module_evidence()["failures"]

    assert "duplicate available slugs" in failures["duplicateAvailable"]
    assert "duplicate sequence slugs" in failures["duplicateSequence"]
    assert "missing ontology documents" in failures["missing"]
    assert "unexpected ontology documents" in failures["unexpected"]
    assert "invalid sequence ordinals" in failures["ordinal"]


def test_documents_consumers_preserve_sequence_and_authority_roles() -> None:
    page_source = DOCUMENTS_PAGE.read_text(encoding="utf-8")
    actions_source = DOCUMENT_ACTIONS.read_text(encoding="utf-8")

    assert "ontologyDocumentSequence.map" in page_source
    assert "documents={researchArticles.map(({ document }) => document)}" in page_source
    assert "canonicalOntologyDocuments" in page_source
    assert "release-facing synthesis" in page_source
    assert "TeX files are the registered source-authority artifacts" in actions_source
    assert "generated human-readable derivatives" in actions_source
