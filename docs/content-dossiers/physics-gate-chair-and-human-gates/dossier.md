# Gate Chair And Human-Gated Decisions Content Dossier

Status: PG-004 implementation dossier.
Human review status: technical validation passed; maintainer review recommended before release.

## Route and reader job

- Public route: `/project/physics/gate-chair-and-human-gates/`
- Reader job: understand why protected scientific promotion decisions require
  human-gated authority, and why validators, handoffs, role registration, and
  website pages cannot issue Gate Chair verdicts.
- Primary audience: general readers, technical readers, and maintainers
  interpreting high-risk claim status.
- Maintainer owner: website maintainer.
- Review status: technical validation passed; no deployment.
- Source-analysis path:
  `docs/system-analyses/gate-chair-and-human-gated-decisions.md`

## Current page summary

This is a new page. It should start with plain-language decision authority,
then explain the authority stack, Gate Chair role fields, validator limits,
current handoff boundary language, and safe/unsafe summaries. It must not
issue or imply a Gate Chair verdict.

## Upstream source basis

| Source path | Status | Use in page |
| --- | --- | --- |
| `research_control/program_state.yaml` | control state | Current latest handoff id and current no-promotion boundary summary. |
| `research_control/handoffs/handoff-0280.yaml` | control handoff | Current bounded handoff, next action, blocked claims, and validator receipts. |
| `research_control/handoffs/handoff-0280.md` | control handoff | Public-readable current handoff summary and claim-boundary language. |
| `registries/AGENT_ROLE_REGISTRY.csv` | registry | Gate Chair authority level, may/may-not fields, human-gate status, and default validators. |
| `.agents/roles/physics/gate-chair.v0.1.0.md` | role contract | Gate Chair mission and boundary requiring explicit tracked approval. |
| `registries/CLAIM_BOUNDARY_REGISTRY.csv` | registry | Repeated forbidden overreads, including validator as proof, role as proof, handoff as proof, approval as proof, and gate readiness as verdict. |
| `github-facing/claim-gates-explainer.md` | generated noncanonical reader surface | Public-safe human-gate and validator-limit language. |
| `github-facing/roles-and-skills-explainer.md` | generated noncanonical reader surface | Role-status and Gate Chair overread warnings. |
| `github-facing/role-routing-explainer.md` | generated noncanonical reader surface | Role template versus current job authority model. |
| `docs/system-analyses/gate-chair-and-human-gated-decisions.md` | website-maintained analysis | Maintainer analysis used to shape the public route. |

## Source-derived topic outline

1. Plain-language explanation of human-gated authority.
2. What the Gate Chair is: a defined scientific-gate role, paused without
   explicit tracked approval.
3. What validators, completions, handoffs, and registries can record.
4. What those surfaces cannot decide.
5. Current handoff example: selector-routed draft/control material ready only
   for a future narrow Gate Chair evidence-status/precondition review, with no
   adoption or downstream GR promotion.
6. Static gate-boundary diagram.
7. Safe and unsafe summaries.
8. Internal reader path and provenance.

## Glossary

| Term | Plain-language explanation | Boundary note |
| --- | --- | --- |
| Gate Chair | Human-gated scientific role for protected promotion, closure, or suspension decisions after required evidence exists. | Defined but paused without explicit tracked approval. |
| Human gate | Protected decision step for adoption, promotion, closure, or authority expansion. | Cannot be replaced by validator PASS or public prose. |
| Gate readiness | Evidence or routing context that may prepare a protected decision. | Not a Gate Chair verdict. |
| Validator PASS | Deterministic repository or task-record check passed. | Operational receipt evidence only, not physics proof. |
| Completion | Record of one bounded AgentJob output and validation evidence. | Does not prove a broader theorem. |
| Handoff | Record of next recommended action. | The next action is not already executed. |
| Claim boundary | Allowed and forbidden claim forms for a source or task. | Metadata is not proof of the scientific claim. |

## Claim boundaries and forbidden implications

### Claim boundaries

- Gate Chair authority requires explicit tracked approval before execution or
  promotion.
- Validators can enforce record shape and boundaries; they cannot prove
  physics or promote claims.
- Role registration helps inspect authority; it does not grant current
  transaction authority.
- Handoffs record next action and blocked claims; they do not execute the next
  action.
- Website pages can explain the model; they cannot become source authority.

### Forbidden implications

- Do not claim Gate Chair approval occurred unless a tracked approved Gate
  Chair record says so.
- Do not claim gate readiness is a Gate Chair verdict.
- Do not claim validator PASS is scientific proof.
- Do not claim a role row or claim-boundary row promotes a physics claim.
- Do not claim handoff status adopts source law, `MetricData(E)`, `g_eff`,
  matter coupling, Einstein equations, benchmark promotion, completed
  derivation, or downstream GR promotion.
- Do not publish local workflow details beyond public-safe control evidence.

## Required comprehension blocks

| Block | Required? | Notes |
| --- | --- | --- |
| Context | Yes | Explain why human gates exist. |
| Plain summary | Yes | Protected decisions require explicit tracked approval. |
| Mechanism steps | Yes | Draft/control, validators, completion, handoff, claim boundary, human gate. |
| Term group | Yes | Required status and authority vocabulary. |
| Source basis | Yes | SourceNotice and provenance section. |
| Boundary block | Yes | No verdict laundering. |
| Diagram | Yes | Static human-gate diagram. |
| Equation walkthrough | No | No equations displayed. |
| Safe/unsafe summary | Yes | High overclaim-risk route. |
| Related internal routes | Yes | Source extension, claim gates, current state, source authority. |

## Diagram contract

| Field | Value |
| --- | --- |
| Mermaid source | `docs/content-dossiers/physics-gate-chair-and-human-gates/diagrams/human-gate-authority.mmd` |
| Public PNG path | `/assets/diagrams/comprehension/physics-gate-chair-human-gates.png` |
| Manifest id | `comprehension_physics_gate_chair_human_gates` |
| Alt text | Diagram showing draft evidence, validators, completion, handoff, claim boundary, explicit human gate, Gate Chair output, and blocked overreads. |
| Caption | Static comprehension diagram: human-gated decisions require explicit tracked approval; readiness signals remain non-verdict evidence. |
| Nearby prose requirement | State that validators, handoffs, role rows, and website pages cannot issue Gate Chair verdicts. |
| Review status | technical validation passed |

## Equation walkthrough contract

No equation walkthrough required for this route.

## Safe summary

Safe summary: Gate Chair authority is a protected human-gated decision path.
Draft/control evidence, validators, completions, handoffs, and registries can
prepare or record context, but only explicit tracked approval can authorize a
Gate Chair execution or protected promotion.

## Unsafe summary

Unsafe summary: A validator passed, a selector routed toward a gate, a handoff
named a next action, or a role row exists; therefore a Gate Chair verdict has
occurred or downstream GR claims are promoted.

## New-page audit

- Is a new public page proposed? Yes.
- Existing route that should be used instead: none.
  `/project/physics/claim-gates/` explains the broader claim-control
  lifecycle, but PG-004 requires a focused page on Gate Chair and human-gated
  authority.
- Reason a new route is justified: high-risk physics pages need a precise
  internal citation target for why validators, readiness, and public prose do
  not decide protected claims.

## Human review checklist

- [x] Source paths were inspected directly.
- [x] The public explanation starts from reader context.
- [x] Claim boundaries are visible.
- [x] Source/provenance links are not the primary reader journey.
- [x] Diagrams have source, public image, alt text, caption, and nearby prose.
- [x] Equation references have walkthroughs where needed.
- [x] Safe and unsafe summaries are present for high-risk topics.
- [x] Mobile layout and desktop layout were reviewed.
- [x] Human review note is recorded under `docs/quality/`.

## References

The AEther Flow. (n.d.-a). `research_control/program_state.yaml` [Program state].

The AEther Flow. (n.d.-b). `research_control/handoffs/handoff-0280.yaml`
[Latest handoff YAML].

The AEther Flow. (n.d.-c). `research_control/handoffs/handoff-0280.md`
[Latest handoff summary].

The AEther Flow. (n.d.-d). `registries/AGENT_ROLE_REGISTRY.csv` [Agent role
registry].

The AEther Flow. (n.d.-e). `.agents/roles/physics/gate-chair.v0.1.0.md`
[Gate Chair role contract].

The AEther Flow. (n.d.-f). `registries/CLAIM_BOUNDARY_REGISTRY.csv`
[Claim-boundary registry].

The AEther Flow. (n.d.-g). `github-facing/claim-gates-explainer.md` [Generated
noncanonical reader surface].

The AEther Flow. (n.d.-h). `github-facing/roles-and-skills-explainer.md`
[Generated noncanonical reader surface].

The AEther Flow. (n.d.-i). `github-facing/role-routing-explainer.md`
[Generated noncanonical reader surface].

The AEther Flow Website. (n.d.). `docs/system-analyses/gate-chair-and-human-gated-decisions.md`
[Website-maintained system analysis].
