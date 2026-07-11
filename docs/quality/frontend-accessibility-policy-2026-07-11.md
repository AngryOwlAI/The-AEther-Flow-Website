# Frontend Accessibility Target and Evidence Policy

Date: 2026-07-11  
Packet: `FE-G0-04`  
Repository baseline: `40ca36aa588bdf925520831c43f3b8aa6a5b4735`  
Adopted plan SHA-256: `55a4190b47dc0a1fbe4d13c38ab24f6cd588c233c9770bce57ff31399c825be5`

## 1. Decision and boundary

The engineering and release target for the reader-facing website is **WCAG 2.2
Level AA**, applied to complete pages, responsive variants, and complete reader
processes. The World Wide Web Consortium recommends WCAG 2.2 as the current
target and defines Level AA as satisfying every Level A and Level AA success
criterion (World Wide Web Consortium [W3C], 2024).

This is an internal implementation target, not a statement that the current
website conforms. `FE-G0-04` performs no conformance audit and authorizes no
public accessibility or legal-compliance claim. A future claim requires a dated,
versioned evaluation of the claimed scope, technologies relied upon, complete
pages, complete processes, responsive variants, and the required browser and
assistive-technology evidence.

This policy does not create scientific, mathematical, governance, or source
authority. It changes no public route, frontend runtime, claim, asset, manifest,
upstream source, remote Git state, or deployment state.

## 2. Normative target and project safeguards

### 2.1 Normative target

Every released page and complete reader process in the declared scope must meet
all applicable WCAG 2.2 Level A and Level AA success criteria. Conformance is
evaluated on full pages; responsive variations are part of the page. No page
fragment, component, automated score, or representative sample alone establishes
site-wide conformance.

The target includes, but is not limited to:

- Semantic structure, text alternatives, captions, contrast, reflow, and text
  resizing.
- Complete keyboard operation, visible and unobscured focus, predictable
  behavior, and no keyboard traps.
- Correct accessible name, role, value, state, and status announcements.
- Pointer-target sizing or spacing that satisfies WCAG 2.2 criterion 2.5.8.
- Motion, flashing, and automatically moving content that satisfies applicable
  Level A and Level AA requirements.

### 2.2 Repository-specific safeguards

The following safeguards are release requirements even where they are more
specific than the Level AA minimum:

- Meaning must remain available in `Full`, `Reduced`, and `Still` motion modes.
- The operating-system reduced-motion preference must be respected before any
  explicit site override. `Still` must run no non-essential motion.
- Informational SVGs must have a stable accessible name, title, description,
  HTML caption, unique IDs, and a meaningful static state. Decorative SVGs must
  be hidden from assistive technology.
- Public navigation, menus, filters, disclosures, tables, dialogs, and route
  orientation must remain operable by keyboard and understandable with the
  required assistive-technology combination.
- Primary navigation and control targets should use the plan's approximately
  40--44 CSS-pixel target where layout permits. Any smaller target must still
  satisfy WCAG 2.2 criterion 2.5.8, including its defined exceptions.
- Data tables and figures may use intentional two-dimensional containers only
  when their meaning requires them. The surrounding page, instructions,
  captions, controls, and individual content must still reflow and remain
  operable.
- Accessibility semantics must be verified in the browser and assistive
  technology. ARIA is not accepted as evidence by inspection alone because it
  can override native semantics and support varies by browser/AT combination
  (W3C, 2026a).

## 3. Severity and release effect

Severity describes user impact. It does not change WCAG conformance: any
unresolved applicable Level A or Level AA failure prevents a claim that the
affected scope conforms, regardless of its assigned severity.

| Severity | Definition | Packet effect | Release effect |
| --- | --- | --- | --- |
| Blocker | Prevents a user in a required modality from reaching core content or completing a primary action; includes traps, inaccessible-only paths, or a non-interference failure | Stop the packet; repair and retest | Blocks release and any conformance claim |
| Critical | Causes major content loss, false state, dangerous motion/flashing, unusable primary navigation, or equivalent failure on a required browser/AT/zoom path | Repair before packet acceptance | Blocks release and any conformance claim |
| Major | Creates significant difficulty but a documented reasonable workaround exists; includes a substantial repository safeguard failure | Repair in the packet or obtain a named, dated exception with owner, rationale, expiry, and follow-up | Blocks a conformance claim; release requires explicit accessibility-owner and release-owner acceptance |
| Minor | Creates localized friction without loss of content, state, or function | May defer with owner, due date, and retest packet | May release only if the issue is not an A/AA failure; any A/AA failure still blocks a conformance claim |

Additional triage rules:

1. Choose the highest severity supported by reproducible user impact.
2. A tool label such as `serious` or `critical` is input to triage, not the
   final project severity.
3. Unknown impact, missing equipment, or an unexecuted required case is
   `blocked` or `not_run`, never `passed`.
4. Multiple individually minor defects may be raised when their combined effect
   makes a path substantially harder to use.
5. A browser or assistive-technology defect does not excuse the failure unless
   the implementation has an accessibility-supported alternative and the
   compatibility decision is documented.

## 4. Required browser, AT, viewport, zoom, and motion matrix

Versions must be captured at test time. `Current stable` means the stable
release installed when the evidence is recorded, not an evergreen assertion in
this policy.

### 4.1 Browser and input matrix

| ID | Environment | Input or AT | Required coverage | Release role |
| --- | --- | --- | --- | --- |
| ENV-01 | Current stable Chromium desktop | Keyboard-only and pointer | Landmarks, focus order/visibility, skip link, menus, disclosures, dialogs, tables, metadata, motion, and basic performance | Required |
| ENV-02 | Current stable Firefox desktop | Keyboard-only and pointer | Layout, SVG, focus, disclosure, dialog, sticky/viewport behavior, and motion | Required |
| ENV-03 | Current stable Safari on macOS | Keyboard-only and pointer | Fonts, native color scheme, SVG, focus, dialog, sticky/viewport behavior, and motion | Required |
| ENV-04 | Current stable Safari on macOS with VoiceOver | VoiceOver keyboard navigation | Landmarks, headings, links, current states, status messages, menus, dialogs, tables, figures, and route orientation | Required |
| ENV-05 | Current stable Chrome on Android | Touch and orientation changes on a physical or approved remote reference device | Menu, tables, figures, targets, portrait/landscape, zoom support, and short-height behavior | Required |
| ENV-06 | Automated Chromium and WebKit where available | Automated semantic and interaction checks | Regression support only | Required where configured; never substitutes for ENV-03 or ENV-04 |
| ENV-07 | Windows with NVDA and a supported browser | NVDA keyboard navigation | Additional screen-reader interoperability | Recommended coverage gap for disposition in `FE-G0-05`; not part of the minimum matrix until an environment and owner are approved |

W3C advises testing each relevant browser/AT combination rather than assuming an
ARIA pattern is interoperable (W3C, 2026a). The minimum matrix above implements
the adopted frontend plan; `FE-G0-05` must either approve ENV-07 or record an
explicit owner and deferral rationale.

### 4.2 Viewport and zoom matrix

| ID | Profile | Required case |
| --- | --- | --- |
| VP-01 | Small phone | 320 by 568 CSS pixels |
| VP-02 | Current phone | 390 by 844 CSS pixels |
| VP-03 | Phone landscape/short height | 844 by 390 CSS pixels or approved equivalent |
| VP-04 | Tablet portrait | 768 by 1024 CSS pixels |
| VP-05 | Tablet/compact desktop | 1024 by 768 CSS pixels |
| VP-06 | Standard desktop | 1440 by 900 CSS pixels |
| VP-07 | Wide desktop | 1920 by 1080 CSS pixels |
| ZM-01 | Browser zoom | 200 percent on representative desktop and changed routes |
| ZM-02 | Reflow | 400 percent from a 1280 CSS-pixel-wide starting viewport, equivalent to 320 CSS pixels |
| ZM-03 | Text enlargement | 200 percent text-only enlargement where the tested browser supports it |

At each required case, the page must have no content loss, overlap, clipped
focus, or unintended page-level horizontal scrolling. Intentional table and
figure containers may scroll in two dimensions only where the content requires
that layout, and must expose an accessible affordance. W3C identifies 320 CSS
pixels as the Level AA reflow width and its 400-percent equivalent from a 1280
CSS-pixel starting viewport (W3C, 2025a).

### 4.3 Motion matrix

Every changed animated surface must be checked in `Full`, `Reduced`, and
`Still`. Meaning, state, accessible name, and keyboard operation are required in
all modes. `Full` and `Reduced` must pause when offscreen or when the document is
hidden; `Still` must have no active motion. User preference persistence and the
operating-system default must be recorded.

Automatically moving content that meets WCAG's duration and parallel-content
conditions requires an accessible pause, stop, or hide mechanism. Interaction-
triggered non-essential motion must be removable under the repository safeguard,
which adopts the WCAG 2.2 Level AAA animation-from-interactions behavior as an
additional project requirement without claiming Level AAA conformance (W3C,
2025b, 2025c).

## 5. Route and process sampling rules

### 5.1 Representative shared-component routes

The minimum shared-component matrix is:

1. `/`
2. `/physics/`
3. `/physics/ontology/`
4. `/physics/claim-status/`
5. `/physics/open-burdens/`
6. `/ai-research-system/workflow/`
7. `/ai-research-system/roles-and-schemas/`
8. `/resources/guided-starts/general-public/`
9. `/resources/documents/`
10. `/resources/diagrams/`
11. `/resources/source-authority/`
12. `/resources/site-builder-guide/`
13. `/license/`

A shared shell, navigation, typography, layout, motion-controller, figure, table,
or dialog change tests every route above. A route-local change tests the changed
route, Home, and at least one representative shared consumer. A final release
evaluation must include every active route template, every shared component
state, every primary reader process, and a structured representative sample.

WCAG-EM provides the evaluation sequence used here: define scope, explore the
site, choose a representative sample, evaluate it, and report findings (W3C,
2026b). Sampling reduces repeated execution; it does not permit an untested page
or responsive state to be included in a conformance claim without defensible
coverage.

### 5.2 Complete processes

At minimum, final evidence must exercise these complete reader processes:

- Enter from Home and reach the flagship theory and current project status.
- Use primary and mobile navigation, including opening, closing, Escape, current
  state, and return focus.
- Follow the general-public guided start through its recommended next step.
- Find and inspect a diagram by category or search and return to the gallery.
- Navigate an advanced long page using its orientation aids.
- Inspect a public table or equivalent card treatment without losing context.
- Change motion mode and verify persistence and OS-default behavior.
- Open and close every dialog or disclosure pattern with keyboard and VoiceOver.

## 6. Evidence policy

### 6.1 Accepted evidence types

Each test result must use one or more of:

- Deterministic automated test or validator output with command and version.
- Manual keyboard, zoom, text-enlargement, touch, or motion test notes.
- Browser and assistive-technology test notes with exact versions and steps.
- Accessibility-tree or DOM inspection tied to an observed behavior.
- Screenshot or short recording when visual state is material.
- A reproducible defect and a dated retest result.
- Structured user-evaluation notes when separately approved and privacy-safe.

Automated tools can identify potential barriers but cannot evaluate every
accessibility requirement and may produce inaccurate results; human judgment is
required (W3C, 2024b). Therefore an automated clean result never substitutes for
keyboard, zoom, VoiceOver, touch, motion, or complete-process testing.

### 6.2 Required record fields

Every matrix result must record:

- Evidence ID, date/time, tester or responsible role, repository commit, and
  build identifier.
- Route or process, component/state, environment ID, OS/device, browser version,
  assistive-technology version, viewport, zoom/text scale, motion mode, and input
  modality.
- Preconditions, exact steps, expected behavior, observed behavior, and result:
  `passed`, `failed`, `not_applicable`, `blocked`, or `not_run`.
- Applicable WCAG criterion and repository safeguard, if any.
- Defect ID, severity, user impact, workaround, evidence path, owner, due date,
  exception/deferral receipt, and retest result where applicable.

### 6.3 Storage and retention

- Commit the dated QA report, approved structured result files, and durable
  defect/exception records under an allowlisted `docs/quality/` or packet path.
- Keep raw screenshots, recordings, browser profiles, and generated reports in
  `output/` or `/tmp` unless the active packet explicitly approves their public
  or tracked storage.
- Do not commit personal data, user names, voices, faces, health information, or
  assistive-technology user-study notes without explicit consent, retention,
  and removal rules.
- Record hashes for committed evidence when a later packet relies on it.
- Preserve failed and blocked results. Do not replace them with a later pass;
  append the retest and link the two records.

### 6.4 Claim language

Allowed internal language before final evaluation:

- `Targets WCAG 2.2 Level AA.`
- `Passed the named automated and manual checks at the recorded commit.`
- `No blocker or critical issue was found in the executed matrix.`

Prohibited without a completed claim record:

- `WCAG compliant`, `fully accessible`, `accessible to everyone`, or equivalent.
- A site-wide conclusion based only on representative routes or automation.
- A statement that VoiceOver, zoom, or motion support exists when the required
  environment was not run.

Any public conformance claim must include the date, WCAG version and URI,
conformance level, exact page scope, and technologies relied upon, as required
by WCAG 2.2. It must also list tested user agents and assistive technologies as
supporting information.

## 7. Packet and release gates

A frontend packet may close when:

1. Its required route/process matrix is complete.
2. No Blocker or Critical defect remains.
3. Every Major defect is repaired or has the required named exception.
4. Every deferred Minor has an owner, due date, and retest packet.
5. Any applicable A/AA failure is explicitly recorded as preventing a
   conformance claim.
6. Automated, keyboard, zoom, browser/AT, responsive, and motion evidence is
   included when relevant to the change.

A release may be accepted only when the full required matrix is complete, no
Blocker or Critical issue remains, every Major disposition is accepted, and all
commands and skipped checks are recorded. A public WCAG 2.2 Level AA claim has a
stricter condition: every applicable A and AA criterion must pass for the
claimed complete pages and processes, with no exception treated as conformance.

`FE-G0-04` establishes these rules but does not run the final matrix. The first
implementation consumers are the P1 accessibility packets. `FE-P7-03` and
`FE-P7-04` must execute the evidence-based accessibility and browser/motion
audits before release acceptance.

## 8. Known limits and next decision

- Current site conformance remains unestablished.
- No Windows/NVDA environment, accessibility owner, external evaluator, or user
  research panel is approved by this packet.
- Legal obligations cannot be inferred from this technical target; jurisdiction
  and legal review are outside scope.
- `FE-G0-05` must approve or defer ENV-07, name the accessibility and release
  owners, and resolve the remaining frontend decision ledger without changing
  this packet's source-authority boundary.

## References

World Wide Web Consortium. (2024a, December 12). *Web Content Accessibility
Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/

World Wide Web Consortium. (2024b). *Selecting web accessibility evaluation
tools*. https://www.w3.org/WAI/test-evaluate/tools/selecting/

World Wide Web Consortium. (2025a). *Understanding success criterion 1.4.10:
Reflow*. https://www.w3.org/WAI/WCAG21/Understanding/reflow

World Wide Web Consortium. (2025b). *Understanding success criterion 2.2.2:
Pause, stop, hide*. https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html

World Wide Web Consortium. (2025c, September 16). *Understanding success
criterion 2.3.3: Animation from interactions*.
https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions

World Wide Web Consortium. (2026a). *Read me first*.
https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/

World Wide Web Consortium. (2026b, February 5). *WCAG-EM overview: Website
accessibility conformance evaluation methodology*.
https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/
