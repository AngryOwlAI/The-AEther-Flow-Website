import pageRouteMap from "../../public/files/manifests/page_route_map.json";
import {
  publicClaimReview,
  publicStatements,
  unsafePublicClaimExamples,
  type PublicClaimState,
  type PublicStatement,
} from "../data/publicStatements";

export type PublicClaimVisualSemantic =
  | "solid"
  | "dashed"
  | "field"
  | "stopped"
  | "loop";

export type PublicClaimLadderItem = {
  id: string;
  statementId: string;
  shortLabel: string;
  state: PublicClaimState;
  visualSemantic: PublicClaimVisualSemantic;
  iconName: string;
};

export const requiredPublicClaimStates: readonly PublicClaimState[] = [
  "complete-effective",
  "adopted-effective",
  "interpretive",
  "open-foundational",
  "not-claimed",
  "governed-method",
] as const;

export const publicClaimLadder: readonly PublicClaimLadderItem[] = [
  {
    id: "PCL-EFFECTIVE-CLOSURE",
    statementId: "PCS-EFFECTIVE-CLOSURE-001",
    shortLabel: "Exact effective closure",
    state: "complete-effective",
    visualSemantic: "solid",
    iconName: "check-circle",
  },
  {
    id: "PCL-ADOPTED-GR",
    statementId: "PCS-ADOPTED-GR-001",
    shortLabel: "Exactly GR by adoption",
    state: "adopted-effective",
    visualSemantic: "solid",
    iconName: "closed-shell",
  },
  {
    id: "PCL-INTERPRETIVE-ONTOLOGY",
    statementId: "PCS-INTERPRETIVE-ONTOLOGY-001",
    shortLabel: "Interpretive ontology",
    state: "interpretive",
    visualSemantic: "field",
    iconName: "layered-field",
  },
  {
    id: "PCL-OPEN-DERIVATION",
    statementId: "PCS-OPEN-DERIVATION-001",
    shortLabel: "Foundational derivation open",
    state: "open-foundational",
    visualSemantic: "dashed",
    iconName: "open-aperture",
  },
  {
    id: "PCL-NOT-CLAIMED",
    statementId: "PCS-NOT-CLAIMED-001",
    shortLabel: "Beyond-GR signal not claimed",
    state: "not-claimed",
    visualSemantic: "stopped",
    iconName: "stopped-path",
  },
  {
    id: "PCL-GOVERNED-METHOD",
    statementId: "PCS-GOVERNED-AI-METHOD-001",
    shortLabel: "AI-assisted, human-accountable method",
    state: "governed-method",
    visualSemantic: "loop",
    iconName: "validation-loop",
  },
] as const;

type RouteRecord = {
  route_path: string;
  upstream_source_paths: readonly string[];
  adaptation_type?: string;
  upstream_authority_status?: string;
};

const routeForSurface = {
  home: "/",
  physics: "/physics/",
} as const;

export const publicClaimRouteBundleSnapshot = pageRouteMap.routes
  .filter((route) => route.route_path === "/" || route.route_path === "/physics/")
  .map((route) => ({
    routePath: route.route_path,
    adaptationType: route.adaptation_type,
    upstreamAuthorityStatus: route.upstream_authority_status,
    upstreamSourcePaths: route.upstream_source_paths,
  }));

const duplicateValues = (values: readonly string[]) =>
  [...new Set(values.filter((value, index) => values.indexOf(value) !== index))];

export const unsafePublicClaimPatterns: readonly RegExp[] = [
  /has derived (?:general relativity|gr) from/i,
  /exact closure proves (?:the )?substrate ontology/i,
  /validated alternative to (?:general relativity|gr)/i,
  /registry status proves (?:the )?physics/i,
  /validators? passed.*derivation is correct/i,
  /ai reviewer independently (?:confirmed|validated)/i,
  /ai research system crossed the derivation gate/i,
  /predicts an established non-gr signal/i,
  /(?:is|provides) a complete theory[.!]?$/i,
  /(?:general relativity|gr) (?:was |has )?(?:derived|recovered|emerged) from the .*substrate/i,
] as const;

export const isUnsafePublicClaim = (wording: string) =>
  unsafePublicClaimPatterns.some((pattern) => pattern.test(wording));

export const validatePublicClaimContract = (
  ladder: readonly PublicClaimLadderItem[] = publicClaimLadder,
  statements: readonly PublicStatement[] = publicStatements,
  routes: readonly RouteRecord[] = pageRouteMap.routes,
  review = publicClaimReview,
) => {
  const errors: string[] = [];
  const ladderIds = ladder.map((item) => item.id);
  const statementIds = statements.map((statement) => statement.id);
  const duplicateLadderIds = duplicateValues(ladderIds);
  const duplicateStatementIds = duplicateValues(statementIds);
  const stateCounts = new Map<PublicClaimState, number>();
  const statementById = new Map(statements.map((statement) => [statement.id, statement]));

  if (duplicateLadderIds.length) {
    errors.push(`duplicate ladder IDs: ${duplicateLadderIds.join(", ")}`);
  }
  if (duplicateStatementIds.length) {
    errors.push(`duplicate statement IDs: ${duplicateStatementIds.join(", ")}`);
  }

  for (const item of ladder) {
    stateCounts.set(item.state, (stateCounts.get(item.state) ?? 0) + 1);
    const statement = statementById.get(item.statementId);
    if (!statement) {
      errors.push(`orphaned statement ID: ${item.statementId}`);
      continue;
    }
    if (statement.disposition !== "accepted") {
      errors.push(`nonaccepted runtime statement: ${statement.id}=${statement.disposition}`);
    }
    if (statement.claimState !== item.state) {
      errors.push(`state mismatch: ${item.id} references ${statement.claimState}`);
    }
    if (statement.reviewerId !== review.reviewer.id) {
      errors.push(`reviewer mismatch: ${statement.id}`);
    }

    for (const surface of statement.surfaces) {
      const routePath = routeForSurface[surface];
      const route = routes.find((candidate) => candidate.route_path === routePath);
      if (!route) {
        errors.push(`missing route bundle: ${routePath}`);
        continue;
      }
      for (const source of statement.sources) {
        if (!route.upstream_source_paths.includes(source.path)) {
          errors.push(`source absent from ${routePath}: ${statement.id} -> ${source.path}`);
        }
      }
    }
  }

  for (const state of requiredPublicClaimStates) {
    if ((stateCounts.get(state) ?? 0) !== 1) {
      errors.push(`required state must exist exactly once: ${state}`);
    }
  }

  if (ladder.length !== requiredPublicClaimStates.length) {
    errors.push(`claim ladder must contain exactly ${requiredPublicClaimStates.length} items`);
  }
  if (review.reviewer.taskName === review.implementationTaskName) {
    errors.push("implementation and reviewer task identities must be distinct");
  }
  if (
    review.reviewer.human ||
    review.reviewer.external ||
    review.reviewer.declaredCredentials !== "none"
  ) {
    errors.push("AI reviewer must not claim human, external, or credentialed status");
  }
  if (!review.accountableOwner) {
    errors.push("accountable human owner is required");
  }

  const adopted = statements.find((statement) => statement.claimState === "adopted-effective");
  if (
    !adopted?.exactWording.includes("adopts") ||
    !adopted.exactWording.includes("without claiming derivation")
  ) {
    errors.push("adopted-effective wording must distinguish adoption from derivation");
  }

  for (const example of unsafePublicClaimExamples) {
    if (!isUnsafePublicClaim(example)) {
      errors.push(`unsafe inference fixture was not rejected: ${example}`);
    }
  }

  if (errors.length) {
    throw new Error(`Public claim contract is invalid: ${errors.join("; ")}`);
  }
};

validatePublicClaimContract();

const statementById = new Map(publicStatements.map((statement) => [statement.id, statement]));

export const resolvedPublicClaimLadder = publicClaimLadder.map((item) => ({
  ...item,
  statement: statementById.get(item.statementId)!,
}));
