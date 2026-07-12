from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DECISION_LEDGER = REPO_ROOT / "docs/quality/frontend-decision-ledger-2026-07-11.md"


def load_claim_contract_evidence() -> dict[str, object]:
    script = r"""
import { createServer } from "vite";

const server = await createServer({
  root: process.cwd(),
  server: { middlewareMode: true },
  appType: "custom",
  logLevel: "silent",
});

try {
  const data = await server.ssrLoadModule("/src/data/publicStatements.ts");
  const module = await server.ssrLoadModule("/src/lib/publicClaimLadder.ts");
  const failures = {};
  const capture = (name, ladder, statements, routes, review) => {
    try {
      module.validatePublicClaimContract(ladder, statements, routes, review);
    } catch (error) {
      failures[name] = error.message;
    }
  };
  const baseRoutes = [
    {
      route_path: "/",
      upstream_source_paths: [...new Set(data.publicStatements.flatMap((statement) => statement.sources.map((source) => source.path)))],
    },
    {
      route_path: "/physics/",
      upstream_source_paths: [...new Set(data.publicStatements.flatMap((statement) => statement.sources.map((source) => source.path)))],
    },
  ];

  capture("duplicate", [...module.publicClaimLadder, module.publicClaimLadder[0]], data.publicStatements, baseRoutes, data.publicClaimReview);
  capture("orphan", module.publicClaimLadder.map((item, index) => index === 0 ? { ...item, statementId: "missing" } : item), data.publicStatements, baseRoutes, data.publicClaimReview);
  capture("nonaccepted", module.publicClaimLadder, data.publicStatements.map((statement, index) => index === 0 ? { ...statement, disposition: "repair" } : statement), baseRoutes, data.publicClaimReview);
  capture("sourceCoverage", module.publicClaimLadder, data.publicStatements, baseRoutes.map((route, index) => index === 0 ? { ...route, upstream_source_paths: [] } : route), data.publicClaimReview);
  capture("reviewerSeparation", module.publicClaimLadder, data.publicStatements, baseRoutes, { ...data.publicClaimReview, reviewer: { ...data.publicClaimReview.reviewer, taskName: data.publicClaimReview.implementationTaskName } });
  capture("credentials", module.publicClaimLadder, data.publicStatements, baseRoutes, { ...data.publicClaimReview, reviewer: { ...data.publicClaimReview.reviewer, declaredCredentials: "PhD" } });
  capture("adoption", module.publicClaimLadder, data.publicStatements.map((statement) => statement.claimState === "adopted-effective" ? { ...statement, exactWording: "General relativity emerged from the substrate." } : statement), baseRoutes, data.publicClaimReview);

  process.stdout.write(JSON.stringify({
    ladder: module.publicClaimLadder,
    statements: data.publicStatements,
    review: data.publicClaimReview,
    unsafeResults: data.unsafePublicClaimExamples.map((example) => module.isUnsafePublicClaim(example)),
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


def test_six_claim_states_exist_exactly_once_with_accepted_statements() -> None:
    evidence = load_claim_contract_evidence()
    ladder = evidence["ladder"]
    statements = {statement["id"]: statement for statement in evidence["statements"]}

    assert [item["state"] for item in ladder] == [
        "complete-effective",
        "adopted-effective",
        "interpretive",
        "open-foundational",
        "not-claimed",
        "governed-method",
    ]
    assert len({item["id"] for item in ladder}) == 6
    assert all(statements[item["statementId"]]["disposition"] == "accepted" for item in ladder)


def test_contract_fails_closed_for_traceability_and_review_defects() -> None:
    failures = load_claim_contract_evidence()["failures"]

    assert "duplicate ladder IDs" in failures["duplicate"]
    assert "orphaned statement ID" in failures["orphan"]
    assert "nonaccepted runtime statement" in failures["nonaccepted"]
    assert "source absent from /" in failures["sourceCoverage"]
    assert "task identities must be distinct" in failures["reviewerSeparation"]
    assert "must not claim human, external, or credentialed status" in failures["credentials"]
    assert "must distinguish adoption from derivation" in failures["adoption"]


def test_unsafe_inference_fixtures_are_rejected() -> None:
    evidence = load_claim_contract_evidence()
    assert all(evidence["unsafeResults"])


def test_reviewer_is_process_separated_without_human_credentials() -> None:
    review = load_claim_contract_evidence()["review"]
    reviewer = review["reviewer"]

    assert review["implementationTaskName"] != reviewer["taskName"]
    assert reviewer["declaredCredentials"] == "none"
    assert reviewer["human"] is False
    assert reviewer["external"] is False
    assert review["accountableOwner"] == "Alexander Ricciardi"
    assert "not_scientific_validation" in review["gateSatisfied"]
    assert len(review["reviewedPayloadSha256"]) == 64
    assert review["websiteBaselineCommit"] == "a38d6855fcfe2cebf9f9ad517ffd65ef92a2d2f5"


def test_generated_review_matrix_and_receipt_are_current() -> None:
    result = subprocess.run(
        ["node", "scripts/generate_public_claim_review.mjs", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "evidence is current" in result.stdout


def test_decision_ledger_records_bounded_ai_reviewer_function() -> None:
    ledger = DECISION_LEDGER.read_text(encoding="utf-8")

    assert "D-01 | Decided; bounded AI technical-review mechanism" in ledger
    assert "claims no degrees or professional credentials" in ledger
    assert "not external peer review" in ledger
    assert "Alexander Ricciardi remains the accountable human acceptance owner" in ledger
