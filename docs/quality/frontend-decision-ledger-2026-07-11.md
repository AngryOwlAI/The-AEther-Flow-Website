# FE-G0-05 Frontend Decision Ledger

Date: 2026-07-11  
Packet: `FE-G0-05`  
Task: `WI-20260711-006`  
Job: `WJ-20260711-006-A`  
Repository baseline: `8813faa38639591fbc8c6f6045f0bc64d5cf4fb7`  
Adopted plan SHA-256:
`55a4190b47dc0a1fbe4d13c38ab24f6cd588c233c9770bce57ff31399c825be5`

## 1. Decision boundary

This ledger gives every open roadmap decision `D-01` through `D-30` an
explicit disposition, accountable owner, blocking effect, and downstream
packet. A `decided` disposition establishes planning direction only. It does
not authorize the downstream implementation packet or satisfy a named approval
gate. A `deferred` disposition is deliberate and fail-closed: its unblock
condition must be met before the listed work can proceed.

This packet changes no public route, copy, claim, frontend runtime, style,
component, asset, manifest, upstream source, remote Git state, or deployment
state. It grants no physics-review acceptance, accessibility-conformance claim,
or production-release approval.

## 2. Named owners

Current repository evidence identifies **Alexander Ricciardi** as the human
maintainer operating the website repository. Git configuration names Alexander
Ricciardi, and the repository README identifies Alex's collaborator identity as
the authenticated GitHub operator for the `AngryOwlAI` repository (The Æther
Flow Website, 2026a).

For this frontend program, the following accountable assignments apply until a
later checked-in owner-change receipt supersedes them:

| Responsibility | Named owner | Authority and limit |
| --- | --- | --- |
| Project and website owner | Alexander Ricciardi | May authorize bounded website packets and named website gates; may not create upstream scientific authority through this ledger |
| Accessibility owner | Alexander Ricciardi | Owns the WCAG target, matrix completion, defect disposition, exceptions, and retest evidence; may not claim conformance without the complete evaluation required by the accessibility policy |
| Release owner | Alexander Ricciardi | Accepts or rejects website release readiness after required evidence; push and deployment still require separate explicit authorization |
| Home, Physics, AI, and Resources route-family maintainer | Alexander Ricciardi | Accountable for bounded rollout and route-family review; physics wording still requires source grounding and the independent physics-review gate |
| Gallery curator | Alexander Ricciardi | Selects the representative gallery subset using checked-in selection criteria and source/asset boundaries |
| Privacy decision owner | Alexander Ricciardi | Must approve provider, consent, retention, access, deletion, and removal terms before any retention or analytics feature |
| Windows/NVDA coverage owner | Alexander Ricciardi | Must provide or authorize the required environment, name the actual tester in evidence, and close blocked cases before affected acceptance |
| Physics reviewer | Unassigned | Alexander Ricciardi owns appointment of a qualified named reviewer, but this ledger does not appoint him or grant physics-review acceptance |

The release owner and accessibility owner are named, but role identity does not
replace evidence. Major accessibility exceptions require both decisions even
when one person currently holds both roles; the receipt must record the two
responsibilities separately.

## 3. Windows and NVDA coverage decision

`ENV-07` from the accessibility policy is promoted from recommended to
**required**. The required primary combination is:

- A supported 64-bit Windows 11 environment.
- The current stable NVDA release installed when the test evidence is recorded.
- Current stable Firefox as the primary browser, plus a focused current-stable
  Chrome interoperability check for changed ARIA-rich controls.
- Keyboard navigation using browse and focus modes across landmarks, headings,
  links, current states, status messages, menus, disclosures, dialogs, tables,
  figures, and route orientation.

NV Access currently lists 64-bit Windows 10 and Windows 11 as supported,
recommends Windows 11 or Windows 10 22H2, and documents NVDA browse mode for
both Mozilla Firefox and Google Chrome (NV Access, 2026a). The current NVDA
download page identifies release `2026.1.1` on the date of this ledger, but the
test record must capture the installed release rather than treating this
version as evergreen (NV Access, 2026b).

Coverage is required for `FE-P1-03`, `FE-P1-06`, and any packet that introduces
or materially changes menus, disclosures, dialogs, tables, status messages, or
route-orientation controls. It is also required in the final `FE-P7-03`
accessibility audit. If the environment or tester is unavailable, the result is
`blocked` or `not_run`, never `passed`; the affected acceptance and final
release remain blocked. VoiceOver/Safari coverage remains independently
required and is not replaced by NVDA.

## 4. D-01 through D-30 dispositions

| ID | Status | Disposition | Accountable owner | Gate, unblock condition, and downstream packet |
| --- | --- | --- | --- | --- |
| D-01 | Deferred; hard blocker | Do not self-approve physics wording. Appoint a qualified named physics reviewer and use a checked-in receipt containing reviewer identity, commit, reviewed claim/source rows, outcome, conditions, and signature/date. | Alexander Ricciardi, appointment owner; physics reviewer unassigned | Blocks `AG-01`, `FE-P0-05`, `FE-P0-06`, `FE-P2-07`, and public claim publication until the reviewer and receipt exist. |
| D-02 | Decided | Initially use the existing `/resources/documents/` flagship entry. A dedicated reader route is allowed only after evidence shows a distinct reader job and less friction without duplicating the source document. | Alexander Ricciardi | Governs `FE-P6-02`; a new route also requires the relevant navigation, canonical, provenance, and source gates. |
| D-03 | Deferred; policy fixed | Use exactly one configured Astro site origin and derive canonicals, sitemap URLs, social URLs, and structured-data URLs from it. `astro.config.mjs` currently has no `site` value; the production origin value is intentionally deferred. No hard-coded duplicates are allowed. | Alexander Ricciardi | Blocks canonical publication and structured URL claims until the production origin is approved in `FE-P6-08`; `FE-P6-08` through `FE-P6-11` must share it. |
| D-04 | Deferred; hard blocker | Draft from the audit direction, but do not approve final Home wording until the claim ladder, source matrix, and D-01 physics receipt pass. | Alexander Ricciardi | Blocks final `FE-P0-06` copy acceptance; resolved through `FE-P0-05` and `AG-01`. |
| D-05 | Decided | Alexander Ricciardi is the accountable maintainer for Home, Physics, AI, and Resources until a checked-in reassignment names a replacement and effective date. | Alexander Ricciardi | Enables bounded family routing; does not waive per-packet review or physics authority. |
| D-06 | Deferred | Do not select a display font in G0. Compare two or three licensed, self-hostable geometric faces with glyph, weight, loading, layout-shift, byte-budget, and license evidence. | Alexander Ricciardi | Selection occurs in `FE-P3-01`; hosting requires `FE-P3-02` and `AG-06`. System fallbacks remain lawful until then. |
| D-07 | Deferred | IBM Plex Mono is the leading candidate, not an approved asset. Compare it with at least one approved equivalent using the same license, glyph, performance, and rendering evidence as D-06. | Alexander Ricciardi | Selection occurs in `FE-P3-01`; hosting requires `FE-P3-02` and `AG-06`. |
| D-08 | Decided | Use `1180px` as the canonical provisional wide-container token, subject to responsive and visual-regression evidence. Reading measure remains independently constrained. | Alexander Ricciardi | Implement only in `FE-P3-03` and `FE-P3-05` after shared-visual-system authorization. |
| D-09 | Decided | Every route has one primary archetype; secondary behavior must be explicitly declared in the route-archetype registry and may not duplicate the primary hierarchy. | Alexander Ricciardi | Enforced by `FE-P3-06` and `FE-P3-09`. |
| D-10 | Decided | Place one global motion-preference control in the shared header/utility surface and persist the site preference locally. | Alexander Ricciardi | Implement in `FE-P1-09`; shared visual and privacy-safe local-storage review still applies. |
| D-11 | Decided | The OS reduced-motion preference supplies the initial default. An explicit user choice overrides it until reset; reset returns control to the current OS preference. | Alexander Ricciardi | Implement and test in `FE-P1-09` across Full, Reduced, and Still. |
| D-12 | Decided | Narrative entrance runs at most once per page load. Do not add replay until user evidence demonstrates value and the control is accessible. | Alexander Ricciardi | Governs `FE-P2-04`; absence of replay is the default. |
| D-13 | Decided | Begin with an observer threshold near 35 percent visible and a documented root margin; tune only from lifecycle and short-viewport evidence. | Alexander Ricciardi | Implement in motion primitives and verify in `FE-P2-07` and `FE-P7-05`. |
| D-14 | Decided | Adopt the measured provisional budgets and no-regression ceilings in the dated FE-G0-03 performance baseline. They are internal gates, not public performance claims. | Alexander Ricciardi, release owner | Applies to prototype acceptance and `FE-P7-05`; exceptions require a scoped repair packet or release-owner receipt. |
| D-15 | Decided | Adopt WCAG 2.2 Level AA as the internal engineering and release target under the FE-G0-04 policy. Add required Windows/NVDA coverage as defined in Section 3 of this ledger. | Alexander Ricciardi, accessibility owner; Alexander Ricciardi, release owner | Applies to all frontend packets and `FE-P7-03`; this is not a current-conformance claim. |
| D-16 | Decided | Use one compact top-level disclosure/drawer with nested groups opened on demand, safe short-viewport scrolling, Escape close, trigger-focus return, and a no-JavaScript path. | Alexander Ricciardi | Implement in `FE-P1-03`; acceptance requires VoiceOver and Windows/NVDA evidence. |
| D-17 | Decided | Support and test a minimum width of 320 CSS pixels plus the approved short-landscape case; retain the complete FE-G0-04 viewport/zoom matrix. | Alexander Ricciardi, accessibility owner | Applies beginning with `FE-P1-02`; no unapproved narrower-browser guarantee is implied. |
| D-18 | Decided | Convert reviewed public vocabulary/definition tables to semantic card or definition patterns; preserve comparison/data tables with table semantics and an accessible overflow affordance. | Alexander Ricciardi | Inventory and ontology pilot occur in `FE-P1-06`; do not transform from automated classification alone. |
| D-19 | Decided | Use an accessible dialog for quick gallery inspection plus a stable asset link. Add a dedicated detail page only when distinct editorial/source-backed content warrants it. | Alexander Ricciardi | Governs gallery rebuild packets; dialog acceptance requires keyboard, VoiceOver, and NVDA evidence. |
| D-20 | Decided | Alexander Ricciardi is the gallery feature owner and selects the representative default subset using a checked-in rubric covering reader value, source status, accessibility, performance, and visual duplication. | Alexander Ricciardi, gallery curator | Blocks gallery hierarchy acceptance until the rubric and selected set are recorded. |
| D-21 | Decided | Keep Advanced content public and indexable unless review finds internal-only material. Remove it from primary navigation and present it as a subordinate Resources utility. | Alexander Ricciardi | Execute only through `AG-04` route/navigation review and the route registry. |
| D-22 | Decided | Preserve working legacy redirects and remove duplicate legacy source pages only after inbound-link, parser, canonical, sitemap, smoke, and redirect-matrix evidence passes. | Alexander Ricciardi | Execute only in `FE-P6-13` with `AG-05`; no route is retired by this ledger. |
| D-23 | Deferred | Do not implement update retention. A later proposal must name a provider and service owner and define consent, data fields, retention duration, access, deletion, incident, and shutdown behavior. | Alexander Ricciardi, privacy decision owner | `FE-P6-06` remains blocked unless `AG-08` passes; otherwise the no-retention state is final. |
| D-24 | Deferred | Do not add analytics. A later proposal must demonstrate a minimal decision-linked event model, privacy need, provider/configuration, consent basis, retention, access, deletion, and a no-tracking fallback. | Alexander Ricciardi, privacy decision owner | `FE-P6-12` remains blocked unless `AG-08` passes; zero analytics is the default. |
| D-25 | Deferred | Do not decide replacement versus supplement for the current video until the existing media, source-approved script, reader job, caption/transcript need, performance cost, and asset license are reviewed. | Alexander Ricciardi | Blocks `FE-P6-01` and `FE-P6-07` until `AG-01` and `AG-06` evidence exists. |
| D-26 | Decided | Publish a source-bounded read-only reviewer packet first. Add a GitHub issue/discussion submission path only after moderation, conduct, licensing, privacy, response-capacity, and repository-readiness evidence passes. | Alexander Ricciardi | Governs `FE-P6-04`; interactive submission requires `AG-09`. |
| D-27 | Decided | Encode motion durations/ranges as named tokens and validator warnings initially. Promote violations to failures only after visual QA establishes stable tolerances and exceptions. | Alexander Ricciardi | Implement through `FE-P1-09`, `FE-P3-03`, and the final P7 gate. |
| D-28 | Decided | Every new or migrated SVG must declare `informational` or `decorative`. Informational SVGs require the full accessible/animated contract; decorative SVGs require assistive-technology hiding and no misleading metadata. | Alexander Ricciardi, accessibility owner | Enforce in `FE-P1-08`; this ledger does not reclassify existing artwork. |
| D-29 | Decided | Treat brand files used by the public runtime as governed public assets: optimize variants, record license/source/purpose/dimensions/bytes/hashes, and add manifest entries when the active schema requires them. | Alexander Ricciardi | Implement in `FE-P2-01` only after `AG-06`, plus `AG-07` for authority-schema/status changes. |
| D-30 | Decided | Replace remote badges with stable local icons and plain text or links. Never forge a local image that implies live build, coverage, release, or repository status. | Alexander Ricciardi | Implement in the approved footer/brand packet; dynamic status requires a separately sourced and freshness-tested feature. |

## 5. Exit and downstream gates

All thirty decisions now have an explicit disposition and accountable owner.
The following items remain intentionally blocking:

1. `D-01`: no named physics reviewer or receipt; public claim work is blocked.
2. `D-03`: no approved production origin; canonical/structured URL publication
   is blocked.
3. `D-04`: final Home wording awaits claim and physics review.
4. `D-06` and `D-07`: no final font selection or license/asset approval.
5. `D-23` and `D-24`: retention and analytics remain off.
6. `D-25`: media replacement/supplement decision awaits source, editorial,
   accessibility, performance, and license evidence.
7. Windows/NVDA is now required; unavailable coverage blocks affected packet
   acceptance rather than creating a waiver.

The next catalog packet is `FE-P0-01`, a read-only authoritative-source pin and
drift-disposition packet. It requires separate authorization. This ledger does
not approve it, does not resolve current upstream drift, and does not grant any
physics promotion.

## References

NV Access. (2026a). *NVDA 2026.1 user guide*. Retrieved July 11, 2026, from
https://download.nvaccess.org/documentation/userGuide.html

NV Access. (2026b). *Download NVDA*. Retrieved July 11, 2026, from
https://www.nvaccess.org/download/

The Æther Flow Website. (2026a). *README* [Internal repository documentation].

The Æther Flow Website. (2026b). *Frontend accessibility target and evidence
policy* [Internal quality policy].

The Æther Flow Website. (2026c). *Frontend recommendations: Source-safe,
motion-rich, responsive, accessible, fast, and maintainable implementation
roadmap* [Internal implementation plan].
