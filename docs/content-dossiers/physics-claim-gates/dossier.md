# Claim Gates Content Dossier

Status: Task 9 physics dossier.
Human review status: pending maintainer review.

## Route and reader job

- Public route: `/project/physics/claim-gates/`
- Reader job: understand proposals, audits, stress tests, completions,
  handoffs, freeze labels, and human gates as scoped claim-control states.
- Primary audience: readers interpreting negative results and gates.
- Maintainer owner: website maintainer.
- Review status: implemented for mechanical audit; maintainer acceptance still
  required.

## Current page summary

The page already explains claim lifecycle and negative-result discipline. The
remediation adds a lifecycle diagram and safe/unsafe summary block.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `github-facing/claim-gates-explainer.md` | generated noncanonical reader surface | Claim lifecycle, negative-result discipline, safe/unsafe summary. |
| `research_control/README.md` | control guide | AgentJob and completion context. |
| `research_control/design/gr_derivation_burden_map.md` | control note | Freeze labels and burden map. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | registry | Allowed and forbidden claim patterns. |
| `registries/AGENT_ROLE_REGISTRY.csv` | registry | Human-gated Gate Chair role status. |

## Source-derived topic outline

1. Claim lifecycle.
2. Negative results as preserved evidence.
3. Scoped obstruction versus global no-go.
4. Gate Chair and human-gated decisions.
5. Safe and unsafe summary.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Human gate | Protected decision path for adoption or promotion. | Not automated by validators. |
| Scoped obstruction | Specific route failed under stated assumptions. | Not global no-go theorem. |
| Validator pass | Control check accepted bounded state. | Not physics proof. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Each lifecycle state authorizes narrower language.
- Negative results remain preserved evidence.
- Gate Chair and protected claims require explicit human-gated authority.

### Forbidden implications

- Do not claim validator PASS proves physics.
- Do not claim generated documentation can promote claims.
- Do not claim a frozen route proves global failure.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Claim-control route. |
| Plain summary | Yes | Gates narrow claims. |
| Mechanism steps | Yes | Classify state, read allowed claim, preserve negative value. |
| Term group | Yes | Human gate, scoped obstruction, validator pass. |
| Source basis | Optional | SourceNotice handles refs. |
| Boundary block | Yes | No Gate Chair shortcut, no global inflation. |
| Diagram | Yes | Static lifecycle diagram. |
| Equation walkthrough | No | No equation walkthrough required for this route. |
| Safe/unsafe summary | Yes | High overclaim-risk route. |
| Related internal routes | Yes | Existing links. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-claim-gates/diagrams/claim-gates-lifecycle.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-claim-gates-lifecycle.png` |
| Manifest id | `comprehension_physics_claim_gates_lifecycle` |
| Alt text | Diagram showing proposal, audit, stress test, completion, handoff, freeze, and human gate states with separate allowed claim scopes. |
| Caption | Static comprehension diagram: claim control preserves scoped evidence without turning it into global success or rejection. |
| Nearby prose requirement | State that gates narrow claim authority. |
| Review status | pending maintainer review |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: AEther Flow preserves proposals, audits, refutations, stress
tests, completions, handoffs, freeze labels, and human gates so each claim
stays scoped to its source evidence and authority boundary.

## Unsafe summary

Unsafe summary: A frozen route proves the whole theory false, validators prove
physics, generated documentation can promote claims, or Gate Chair approval
occurred without an explicit human-gated record.

## New-page audit

- Is a new public page proposed? No.
- Existing route that should be used instead: `/project/physics/claim-gates/`.
- Reason a new route is or is not justified: existing route owns claim-control
  explanation.

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

AEther-Flow Project. (2026). `github-facing/claim-gates-explainer.md`
[Generated noncanonical reader surface].
