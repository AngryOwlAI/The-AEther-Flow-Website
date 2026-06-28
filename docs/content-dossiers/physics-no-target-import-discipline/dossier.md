# No-Target-Import Discipline Content Dossier

Status: draft dossier.

## Route and reader job

- Public route: `/project/physics/no-target-import-discipline/`
- Reader job: Understand why hidden target geometry, benchmark-success, and
  process-authority imports are blocked before source-side claims can be
  trusted.
- Primary audience: general public readers, physicists, mathematicians, and
  readers inspecting methodology.
- Maintainer owner: Documentation Curator / website maintainer.
- Review status: Human review status: pending maintainer review.

## Current page summary

The page explains no-target-import discipline as a fail-closed guardrail. It
distinguishes forbidden target-context imports from acceptable source-side
construction and states that criterion formalization is pending audit, not
completed physics proof.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `research_control/design/no_target_import_guard_map.md` | upstream control note | Guard categories and checklist behavior. |
| `research_control/tasks/RT-20260614-105/DDR-20260614-105.md` | upstream decision record | Guard map created as control surface, not physics claim. |
| `research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex` | upstream task artifact | Formal source-only factorization criterion. |
| `research_control/tasks/RT-20260614-128/jobs/completions/AJC-AJ-RT-20260614-128-001.yaml` | upstream completion | Criterion status and downstream blocked claims. |
| `research_control/tasks/RT-20260614-128/artifacts/parent_conflict_review_m_src_gsc_no_target_import_criterion.yaml` | upstream review artifact | Confirms criterion is not adoption. |
| `registries/RESEARCH_TASK_REGISTRY.csv` | upstream registry | Task closure wording for RT-105 and RT-128. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | upstream registry | Forbidden target-import and adoption overreads. |
| `github-facing/claim-gates-explainer.md` | generated noncanonical explainer | Public-safe lifecycle language. |
| `github-facing/gr-derivation-roadmap-explainer.md` | generated noncanonical explainer | Frontier caution and no-target-import context. |

## Source-derived topic outline

1. Why the guardrail exists: source derivation cannot borrow the target it is
   supposed to recover.
2. Forbidden import classes: topology, atlas, metric, proper time, detector
   semantics, benchmark success, and process authority.
3. Acceptable source-side construction: source supports, overlap predicates,
   transition tokens, certificates, and bottom guards.
4. Criterion model: `C_src(E; T)=F_src(E)` or proof-step factorization.
5. Fail-closed labels: `OB-MSRC-TARGET-IMPORT`,
   `OB-MSRC-PROCESS-AUTHORITY-LAUNDERING`, and
   `OB-MSRC-LOCAL-GLOBAL-GAP`.
6. Safe and unsafe summaries.
7. Internal reading path.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| no-target-import | A discipline requiring source-side arguments to avoid hidden target or process inputs. | Not proof of a candidate. |
| target context `T` | Diagnostic bundle of forbidden target and process data. | It is an audit handle, not an input to the proof. |
| source-only factorization | Every non-bottom proof step factors through source data. | Criterion remains pending audit. |
| process-authority laundering | Treating validators, registries, roles, handoffs, generated derivatives, file order, or commits as proof. | Always forbidden as mathematical evidence. |
| fail-closed | A forbidden import branch blocks or records an obstruction instead of silently continuing. | Does not prove global failure. |

## Claim boundaries and forbidden implications

### Claim boundaries

- The guard map is a reusable checklist and routing surface.
- The no-target-import criterion is theorem-shaped methodology.
- The criterion status is `criterion_formalized_pending_audit`.
- An audit pass is scoped to the checked text or data.

### Forbidden implications

- All future work is target-import-free.
- `M_src` has been adopted.
- `g_eff`, matter coupling, Einstein equations, benchmark promotion, or
  completed derivation has been produced.
- Exact-GR benchmark success can be used as source evidence.
- Validator, registry, role, handoff, generated derivative, local cache, file
  order, commit status, or recency is mathematical proof.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | yes | Explain why hidden target import would invalidate derivation. |
| Plain summary | yes | Guardrail, not proof. |
| Mechanism steps | yes | Target context, source-only factorization, audit, fail-closed branch. |
| Term group | yes | Glossary terms above. |
| Source basis | yes | Guard map, RT-105, RT-128, registries, explainers. |
| Boundary block | yes | Not all future work clean; not adoption or downstream promotion. |
| Diagram | yes | Static PNG generated from dossier Mermaid source. |
| Equation walkthrough | yes | Explain `C_src(E; T)=F_src(E)` in prose. |
| Safe/unsafe summary | yes | High-risk methodology overread prevention. |
| Related internal routes | yes | Source-extension, claim boundaries, Distance-to-GR, Gate Chair. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-no-target-import-discipline/diagrams/no-target-import-discipline.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-no-target-import-discipline.png` |
| Manifest id | `comprehension_physics_no_target_import_discipline` |
| Alt text | Diagram showing source data entering a source-only factorization check while target topology, target atlas, target metric, benchmark success, and process authority are blocked into fail-closed obstruction labels. |
| Caption | Static comprehension diagram: no-target-import discipline blocks target-context and process-authority imports without proving candidate adoption. |
| Nearby prose requirement | State that the diagram is a reader aid, not proof that all future work is target-import-free. |
| Review status | Human review status: pending maintainer review. |

## Equation walkthrough contract

Equation: `C_src(E; T)=F_src(E)`.

Symbol data:

| Symbol | Reader-facing meaning |
| --- | --- |
| `E` | Source object under discussion. |
| `T` | Diagnostic target context containing topology, atlas, metric, proper time, detector semantics, benchmark success, and process metadata. |
| `C_src(E; T)` | Candidate construction written with an explicit audit slot for forbidden target context. |
| `F_src(E)` | Source-only construction that does not depend on `T`. |

Plain-language reading:

- `E` is the source object under discussion.
- `T` is a diagnostic target context: topology, atlas, metric, proper time,
  detector semantics, benchmark success, and process metadata.
- `C_src(E; T)` is the candidate written with an explicit audit slot.
- `F_src(E)` is the source-only construction.
- The equality means the candidate must not change when target context changes.
  Where object equality is too strong, every non-bottom proof step must still
  factor through source data alone.

Boundary: the equation is a criterion, not proof that a later theorem satisfies
the criterion.

## Safe summary

Safe summary: No-target-import discipline blocks hidden target-context and
process-authority imports by requiring source-only factorization and
fail-closed handling. The current criterion is
`criterion_formalized_pending_audit`, not `M_src` adoption or downstream GR
promotion.

## Unsafe summary

Unsafe summary: Because the guardrail exists, all future target imports have
been eliminated, `M_src` is adopted, benchmark success counts as source
evidence, or validators and registries can prove physics.

## New-page audit

- Is a new public page proposed? Yes.
- New route: `/project/physics/no-target-import-discipline/`.
- Reason a new route is justified: PG-011 requires a dedicated methodology page
  for hidden target-import discipline, and existing pages mention the guardrail
  without a reader-facing explanation of import classes, factorization, and
  unsafe summaries.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [ ] Mobile layout and desktop layout were reviewed.
- [ ] Human review note is recorded under `docs/quality/`.

## References

- The AEther Flow. (2026a). `research_control/design/no_target_import_guard_map.md`.
- The AEther Flow. (2026b). `research_control/tasks/RT-20260614-105/DDR-20260614-105.md`.
- The AEther Flow. (2026c). `research_control/tasks/RT-20260614-128/artifacts/160_M_SRC_GSC_NO_TARGET_IMPORT_CRITERION.tex`.
- The AEther Flow. (2026d). `research_control/tasks/RT-20260614-128/jobs/completions/AJC-AJ-RT-20260614-128-001.yaml`.
- The AEther Flow. (2026e). `research_control/tasks/RT-20260614-128/artifacts/parent_conflict_review_m_src_gsc_no_target_import_criterion.yaml`.
- The AEther Flow. (2026f). `registries/RESEARCH_TASK_REGISTRY.csv`.
- The AEther Flow. (2026g). `registries/CLAIM_BOUNDARY_REGISTRY.csv`.
- The AEther Flow. (2026h). `github-facing/claim-gates-explainer.md`.
- The AEther Flow. (2026i). `github-facing/gr-derivation-roadmap-explainer.md`.
- The AEther Flow Website. (2026). `docs/system-analyses/no-target-import-discipline.md`.
