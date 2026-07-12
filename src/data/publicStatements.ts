export type PublicClaimState =
  | "complete-effective"
  | "adopted-effective"
  | "interpretive"
  | "open-foundational"
  | "not-claimed"
  | "governed-method";

export type PublicClaimSurface = "home" | "physics";

export type PublicStatementDisposition =
  | "accepted"
  | "repair"
  | "blocked"
  | "superseded";

export type PublicStatementSource = {
  path: string;
  sha256: string;
  commit: string;
  passage: string;
  registryId: string;
  registryStatus: readonly string[];
};

export type PublicStatement = {
  id: string;
  claimState: PublicClaimState;
  exactWording: string;
  allowedQualification: string;
  surfaces: readonly PublicClaimSurface[];
  sources: readonly PublicStatementSource[];
  forbiddenOverreads: readonly string[];
  reviewerId: string;
  reviewDate: string;
  disposition: PublicStatementDisposition;
};

export const publicClaimSourceCommit =
  "a8c0b3f4ada00d852d3bc2123ddd4d203f5428b0";

export const publicClaimReviewPrompt = `Review the FE-P0-05 public statement registry at statement granularity against the pinned upstream exact-closure TeX sources and registries. Apply a rigorous physics, mathematics, and philosophy rubric. Confirm exact wording, qualification, source passage, source hash, source commit, registry status, route-bundle coverage, forbidden overreads, and adoption-versus-derivation discipline. Fail any claim that implies completed substrate derivation, independent validation, non-GR observational novelty, ontology as evidence, validator PASS as proof, or AI crossing a scientific promotion gate. Record that the reviewer is an AI sub-agent with no human degrees, credentials, signature, external-peer-review status, proof authority, or independent-validation authority.`;

export const publicClaimReview = {
  reviewId: "PCR-FE-P0-05-20260712-A",
  reviewType: "ai_subagent_technical_review",
  reviewDate: "2026-07-12",
  websiteBaselineCommit: "a38d6855fcfe2cebf9f9ad517ffd65ef92a2d2f5",
  reviewedPayloadSha256: "32e812c4be316a48ceb1be295768e2f4a7a7184c4d65a2440d0a5483920cbdd7",
  upstreamCommit: publicClaimSourceCommit,
  implementationTaskName: "/root",
  reviewer: {
    id: "ai-reviewer-physics-reviewer-20260712",
    taskName: "/root/physics_reviewer",
    systemClass: "spawned_language_model_subagent",
    declaredCredentials: "none",
    human: false,
    external: false,
    independenceScope: "separate_task_context_and_review_prompt_only",
    signatureType: "machine_attribution_not_human_signature",
  },
  accountableOwner: "Alexander Ricciardi",
  ownerAcceptanceStatus:
    "review_mechanism_authorized_route_publication_requires_separate_packet",
  overallOutcome: "accepted_for_source_bounded_candidate_registry",
  gateSatisfied:
    "website_publication_governance_review_only_not_scientific_validation",
  limitations: [
    "The reviewer does not hold or claim human academic degrees or professional credentials.",
    "The review is not external peer review, a human signature, or independent empirical validation.",
    "The review does not grant proof authority, source authority, benchmark promotion, or completed-derivation status.",
    "A passing receipt does not authorize route-copy publication, Git push, deployment, or upstream mutation.",
  ],
} as const;

const overviewSource = (
  passage: string,
): PublicStatementSource => ({
  path: "ontology/tex/aether_flow_exact_closure_sequence_overview.tex",
  sha256: "356a5f65b0931914fdf9362ba544c2868bad7d33b828754b91c029bed96f86b1",
  commit: publicClaimSourceCommit,
  passage,
  registryId: "TEX-ONTOLOGY-AETHER-FLOW-EXACT-CLOSURE-SEQUENCE-OVERVIEW",
  registryStatus: [
    "canonical",
    "benchmark_claim",
    "canonical_ontology",
    "accepted",
    "validation_PASS",
  ],
});

const flagshipSource = (
  passage: string,
): PublicStatementSource => ({
  path: "ontology/tex/aether_flow_exact_closure_flagship_article.tex",
  sha256: "900c799cb0c3d8f790c836196c136b3cec6944e46d41b89e511b85123fd30e40",
  commit: publicClaimSourceCommit,
  passage,
  registryId: "TEX-ONTOLOGY-AETHER-FLOW-EXACT-CLOSURE-FLAGSHIP-ARTICLE",
  registryStatus: [
    "canonical",
    "benchmark_claim",
    "canonical_ontology",
    "accepted",
    "validation_PASS",
  ],
});

const commonSurfaces = ["home", "physics"] as const;
const reviewerId = publicClaimReview.reviewer.id;

export const publicStatements: readonly PublicStatement[] = [
  {
    id: "PCS-EFFECTIVE-CLOSURE-001",
    claimState: "complete-effective",
    exactWording:
      "At the effective level, the active exact-closure package is complete as an operational theory statement: its observable gravitational content is that of general relativity.",
    allowedQualification:
      "Complete refers only to the adopted effective theory for its stated matter sector, initial data, and boundary conditions; it does not mean that substrate microphysics has been derived or independently validated.",
    surfaces: commonSurfaces,
    sources: [overviewSource("lines 47-50, 118-124, 175-182, and 200")],
    forbiddenOverreads: [
      "completed substrate derivation",
      "unique microphysical origin",
      "independent empirical validation",
      "new predictive content beyond general relativity",
    ],
    reviewerId,
    reviewDate: "2026-07-12",
    disposition: "accepted",
  },
  {
    id: "PCS-ADOPTED-GR-001",
    claimState: "adopted-effective",
    exactWording:
      "The exact-closure package adopts Einsteinian metric dynamics with one operative metric and universal matter coupling; adoption means use of that effective dynamics without claiming derivation from substrate variables.",
    allowedQualification:
      "Adopted means used as the effective benchmark; it does not mean derived, recovered, or proved from the Æther / Æther-Flow substrate.",
    surfaces: commonSurfaces,
    sources: [overviewSource("lines 57-65 and 118-124")],
    forbiddenOverreads: [
      "adoption equals derivation",
      "Einstein equations recovered from Æther variables",
      "universal matter coupling derived from substrate dynamics",
      "the adopted equations are novel equations",
    ],
    reviewerId,
    reviewDate: "2026-07-12",
    disposition: "accepted",
  },
  {
    id: "PCS-INTERPRETIVE-ONTOLOGY-001",
    claimState: "interpretive",
    exactWording:
      "The Æther / Æther-Flow vocabulary supplies the package's proposed ontological and interpretive setting; it does not add a second observer-level field law or an established low-energy signal beyond general relativity.",
    allowedQualification:
      "The ontology is a proposed interpretation within the project, not an observed preferred-frame field or empirical evidence for new low-energy physics.",
    surfaces: commonSurfaces,
    sources: [overviewSource("lines 60-65, 158-166, and 189-200")],
    forbiddenOverreads: [
      "ontology is empirically established",
      "ontology constitutes evidence for new physics",
      "Æther-Flow is a measured preferred-frame field",
      "interpretive novelty is observational novelty",
    ],
    reviewerId,
    reviewDate: "2026-07-12",
    disposition: "accepted",
  },
  {
    id: "PCS-OPEN-DERIVATION-001",
    claimState: "open-foundational",
    exactWording:
      "A first-principles derivation of Einsteinian gravity from explicit Æther / Æther-Flow substrate variables remains open.",
    allowedQualification:
      "Open means not completed; a roadmap, candidate, validator result, or scoped obstruction does not cross the derivation gate.",
    surfaces: commonSurfaces,
    sources: [overviewSource("lines 118-124, 175-183, and 202-214")],
    forbiddenOverreads: [
      "the open burden is nearly solved",
      "a roadmap or candidate completes the derivation",
      "a scoped obstruction is a program-wide impossibility theorem",
      "more computation alone crosses the gate",
    ],
    reviewerId,
    reviewDate: "2026-07-12",
    disposition: "accepted",
  },
  {
    id: "PCS-NOT-CLAIMED-001",
    claimState: "not-claimed",
    exactWording:
      "The project does not claim a completed substrate derivation, a unique underlying substrate action, an independently verified low-energy sector beyond general relativity, or a new observer-level gravitational law.",
    allowedQualification:
      "A nonclaim prevents overstatement; it does not prove the opposite proposition or validate the ontology.",
    surfaces: commonSurfaces,
    sources: [overviewSource("lines 175-183")],
    forbiddenOverreads: [
      "nonclaim language proves the opposite",
      "absence of a non-GR sector validates the ontology",
      "a scoped no-go rejects every possible substrate model",
      "exact closure is an independently tested alternative to GR",
    ],
    reviewerId,
    reviewDate: "2026-07-12",
    disposition: "accepted",
  },
  {
    id: "PCS-GOVERNED-AI-METHOD-001",
    claimState: "governed-method",
    exactWording:
      "AI assistance may support drafting, mathematical exploration, branch screening, organization, and revision, but it does not convert speculative steps into established physics or remove the need for expert human review.",
    allowedQualification:
      "This is a methodological provenance statement, not external peer review, a human signature, proof authority, or independent scientific validation.",
    surfaces: commonSurfaces,
    sources: [flagshipSource("lines 245-249")],
    forbiddenOverreads: [
      "AI independently validates the physics",
      "a spawned reviewer becomes scientific authority",
      "validator PASS is proof",
      "review completion is derivation completion",
      "registry entries, generated artifacts, or website pages prove physics claims",
    ],
    reviewerId,
    reviewDate: "2026-07-12",
    disposition: "accepted",
  },
] as const;

export const unsafePublicClaimExamples = [
  "The project has derived GR from Æther-Flow.",
  "Exact closure proves the substrate ontology.",
  "The package is a validated alternative to GR.",
  "Canonical registry status proves the physics.",
  "All validators passed, therefore the derivation is correct.",
  "The AI reviewer independently confirmed the theory.",
  "The AI research system crossed the derivation gate.",
  "The package predicts an established non-GR signal.",
  "The exact-closure package is a complete theory.",
  "General relativity emerged from the Æther substrate.",
] as const;
