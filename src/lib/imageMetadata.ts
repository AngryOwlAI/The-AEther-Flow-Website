export interface ImageDimensions {
  width: number;
  height: number;
  aspectRatio?: string;
}

const comprehensionImageDimensions: Record<string, ImageDimensions> = {
  "/assets/diagrams/comprehension/ai-memory-source-first-layers.png": { width: 1544, height: 1324 },
  "/assets/diagrams/comprehension/ai-one-bounded-agentjob-envelope.png": { width: 1368, height: 1596 },
  "/assets/diagrams/comprehension/ai-role-authority-inspector-stack.png": { width: 1326, height: 1640 },
  "/assets/diagrams/comprehension/ai-roles-authority-stack.png": { width: 1182, height: 1068 },
  "/assets/diagrams/comprehension/ai-system-task-authority-map.png": { width: 1568, height: 178 },
  "/assets/diagrams/comprehension/ai-workflow-bounded-agentjob-chain.png": { width: 1568, height: 230 },
  "/assets/diagrams/comprehension/general-public-guided-start.png": { width: 1568, height: 280 },
  "/assets/diagrams/comprehension/operations-control-spine.png": { width: 1568, height: 212 },
  "/assets/diagrams/comprehension/operations-director-agentjob-record-chain.png": { width: 1568, height: 164 },
  "/assets/diagrams/comprehension/operations-project-system-improvement-loop.png": { width: 1038, height: 2268 },
  "/assets/diagrams/comprehension/operations-publication-review-flow.png": { width: 1568, height: 220 },
  "/assets/diagrams/comprehension/operations-role-routing-allowlist-stack.png": { width: 1326, height: 1068 },
  "/assets/diagrams/comprehension/operations-technical-tool-tiers.png": { width: 1026, height: 1068 },
  "/assets/diagrams/comprehension/operations-validator-pass-boundary.png": { width: 868, height: 1898 },
  "/assets/diagrams/comprehension/parent-child-single-outer-agentjob.png": { width: 1568, height: 1020 },
  "/assets/diagrams/comprehension/physics-benchmark-boundary-ladder.png": { width: 1568, height: 278 },
  "/assets/diagrams/comprehension/physics-claim-gates-lifecycle.png": { width: 1568, height: 354 },
  "/assets/diagrams/comprehension/physics-current-state-snapshot-boundary.png": { width: 1568, height: 294 },
  "/assets/diagrams/comprehension/physics-distance-to-gr-dashboard.png": { width: 1568, height: 406 },
  "/assets/diagrams/comprehension/physics-finite-toy-models.png": { width: 1568, height: 158 },
  "/assets/diagrams/comprehension/physics-gate-chair-human-gates.png": { width: 1568, height: 464 },
  "/assets/diagrams/comprehension/physics-metric-response-ladder.png": { width: 1568, height: 172 },
  "/assets/diagrams/comprehension/physics-negative-results-and-frozen-routes.png": { width: 1568, height: 166 },
  "/assets/diagrams/comprehension/physics-no-target-import-discipline.png": { width: 1568, height: 304 },
  "/assets/diagrams/comprehension/physics-ontology-boundary-map.png": { width: 1568, height: 274 },
  "/assets/diagrams/comprehension/physics-roadmap-burden-ladder.png": { width: 1096, height: 1948 },
  "/assets/diagrams/comprehension/physics-source-extension-pipeline.png": { width: 1568, height: 224 },
  "/assets/diagrams/comprehension/physics-track-status-map.png": { width: 1568, height: 384 },
  "/assets/diagrams/comprehension/project-overview-two-track-map.png": { width: 1568, height: 558 },
  "/assets/diagrams/comprehension/resources-diagram-publication-boundary.png": { width: 1568, height: 298 },
  "/assets/diagrams/comprehension/resources-manifest-chain.png": { width: 1568, height: 472 },
  "/assets/diagrams/comprehension/resources-tex-pdf-derivative-chain.png": { width: 1568, height: 412 },
  "/assets/diagrams/comprehension/reviewer-inspection-order.png": { width: 1568, height: 348 },
  "/assets/diagrams/comprehension/source-authority-claim-boundary-explorer.png": { width: 1568, height: 472 },
  "/assets/diagrams/comprehension/source-authority-ladder.png": { width: 856, height: 1212 },
  "/assets/diagrams/comprehension/source-authority-publication-provenance-system.png": { width: 1568, height: 232 },
  "/assets/diagrams/comprehension/specialist-guided-starts.png": { width: 1568, height: 864 },
};

export const getImageDimensions = (
  src: string,
  provided: Partial<ImageDimensions> = {},
): Required<ImageDimensions> => {
  const registered = comprehensionImageDimensions[src];
  const dimensions = {
    width: provided.width ?? registered?.width,
    height: provided.height ?? registered?.height,
    aspectRatio: provided.aspectRatio ?? registered?.aspectRatio,
  };

  if (
    !Number.isInteger(dimensions.width) ||
    dimensions.width <= 0 ||
    !Number.isInteger(dimensions.height) ||
    dimensions.height <= 0
  ) {
    throw new Error(`Image dimensions are required for ${src}`);
  }

  return {
    width: dimensions.width,
    height: dimensions.height,
    aspectRatio: dimensions.aspectRatio ?? `${dimensions.width} / ${dimensions.height}`,
  };
};

export const withImageDimensions = <T extends { src: string }>(
  item: T,
): T & Required<ImageDimensions> => ({
  ...item,
  ...getImageDimensions(item.src),
});
