# Documents navigation migration completion

## Record scope

This record closes the evidence product for plan task `AFDOC-R007` in
`PLAN-AETHER-DOCUMENTS-NAV-RECOVERY-002`. It describes the accepted local
Documents migration state, the later repair and validation chain, and the
effects that remain withheld. It does not change a reader route, navigation,
manifest, public asset, scientific claim, or upstream source.

The canonical Documents migration is present in local website commit
`7292ff009e3dbab89deb307a405cc6bb863caaf1`. The recovery relay was bound to
website checkout revision `34260d53fae15003cb2bdff24de2216297ff52c3` on
`main`. This task records those existing bytes; it does not claim to have
created, staged, committed, or pushed either revision.

## Canonical reader routes

The final route map and page-provenance manifest contain 15 canonical
Documents pages:

- `/documents/`
- `/documents/anthology/`
- `/documents/research/`
- `/documents/governance/`
- `/documents/diagrams/`
- `/documents/derivatives/`
- `/documents/reading-paths/`
- `/documents/reading-paths/general-public/`
- `/documents/reviewer-packet/`
- `/documents/governance/source-authority/`
- `/documents/governance/registries/`
- `/documents/governance/publication-process/`
- `/documents/governance/retrieval-layers/`
- `/documents/governance/repository-map/`
- `/documents/governance/site-builder-guide/`

The top-level navigation object is now `Documents`, matched by the
`/documents/` prefix, with exactly this order:

1. Documentation Overview
2. Anthology Articles
3. Research Articles
4. Governance & Control
5. Diagram Gallery

The accepted headed-browser receipt verified those five destinations at
`1440x900` and `390x844`, including disclosure behavior, Tab/Enter/Escape
navigation, visible focus, zero measured horizontal overflow, and zero console
warnings or errors.

## Moved, consolidated, redirected, and retired routes

`public/_redirects` is the production redirect source. The 15 retired
Resources routes map directly to terminal Documents destinations:

| Retired route | Canonical destination | Disposition |
| --- | --- | --- |
| `/resources/` | `/documents/` | Resources front door retired |
| `/resources/library/` | `/documents/` | Library consolidated into Documentation Overview |
| `/resources/documents/` | `/documents/research/` | Ontology documents consolidated into Research Articles |
| `/resources/diagrams/` | `/documents/diagrams/` | Page moved |
| `/resources/source-authority/` | `/documents/governance/source-authority/` | Page moved under Governance |
| `/resources/registries/` | `/documents/governance/registries/` | Page moved under Governance |
| `/resources/generated-derivatives/` | `/documents/derivatives/` | Page moved and label shortened |
| `/resources/retrieval-layers/` | `/documents/governance/retrieval-layers/` | Page moved under Governance |
| `/resources/publication-process/` | `/documents/governance/publication-process/` | Page moved under Governance |
| `/resources/reading-paths/` | `/documents/reading-paths/` | Consolidated with Guided Starts |
| `/resources/repository-map/` | `/documents/governance/repository-map/` | Page moved under Governance |
| `/resources/site-builder-guide/` | `/documents/governance/site-builder-guide/` | Page moved under Governance |
| `/resources/guided-starts/` | `/documents/reading-paths/` | Consolidated into Reading Paths |
| `/resources/guided-starts/general-public/` | `/documents/reading-paths/general-public/` | General-public path moved |
| `/resources/reviewer-packet/` | `/documents/reviewer-packet/` | Page moved |

The migration commit relocated 11 existing page sources into the Documents
tree. It removed four obsolete source pages only after their canonical
destinations and direct redirects existed:

- `src/pages/resources/index.astro`
- `src/pages/resources/library/index.astro`
- `src/pages/resources/documents.astro`
- `src/pages/resources/reading-paths/index.astro`

It also added the four category/front-door sources for Documentation Overview,
Anthology Articles, Research Articles, and Governance & Control. Retired
Resources routes are absent from the route map and page provenance as
canonical pages.

Legacy aliases were repointed directly, without avoidable redirect chains:

| Alias | Final destination | Status |
| --- | --- | --- |
| `/documents` | `/documents/` | `301` |
| `/diagrams` | `/documents/diagrams/` | `301` |
| `/equations` | `/documents/research/` | `301` |
| `/research/equations/` | `/documents/research/` | `301` |
| `/research/math-sample/` | `/documents/research/` | `301` |
| `/downloads` | `/documents/` | `301` |
| `/project/operations/publication-process/` | `/documents/governance/publication-process/` | `301` |
| `/project/source-authority/publication-and-provenance-system/` | `/documents/governance/publication-process/` | `301` |
| `/project/source-authority/` | `/documents/governance/source-authority/` | `301` |
| `/research/map/` | `/documents/governance/publication-process/` | `301` |
| `/research` | `/documents/governance/publication-process/` | preserved accepted `302` exception |

The redirect receipt reports 15 Resources mappings, zero redirect chains,
zero reverse Documents-to-Resources redirects, and a built redirect copy that
matched `public/_redirects`.

## Importer, catalog, manifests, and provenance

The migration added an ownership-scoped, configuration-driven document
collection importer at `scripts/import_document_collection.py`. Its accepted
behavior is deterministic and fail-closed: it replaces only records owned by
the selected collection, preserves foreign importer records, binds copied
bytes and SHA-256 values to source references and logical-document roles, and
publishes nothing when ownership or source status is ambiguous.

The public document catalog contains eight approved logical research documents
and 16 manifestations. Each document pairs a registered TeX
`authoritative_source` with a PDF `readable_derivative`; the catalog does not
promote the derivative into source authority. Final catalog inspection found
that the source and asset manifests, ontology asset URLs, and asset identities
did not require churn.

The final route/provenance repair replaced the 15 retired Resources canonical
records with the 15 Documents records and validated all 34 canonical website
routes. Page provenance carries current local page hashes and preserves
route-local upstream source ordering, hashes, and pinned URLs. The manifest's
top-level reviewed source snapshot is
`c6aa66b9a7412f14c6573dd0467b82ea11310c20`; unchanged route-local source pins
remain distinct evidence and are not silently advanced.

## Curator source snapshot

Curator review and the post-repair aggregate are bound to immutable upstream
commit `c6aa66b9a7412f14c6573dd0467b82ea11310c20`, dated
`2026-07-21T08:05:50-06:00`. This is the reviewed snapshot. A later moving
upstream checkout is not substituted for it and is not evidence for this
completion record.

The accepted AFDOC-038 receipt records:

- 246 declared source dependencies;
- 58 review-required drift pairs;
- 58 exact, matched, non-expired acknowledgements;
- zero missing review-required acknowledgements;
- zero critical drift after the bounded current-state refresh;
- zero critical acknowledgements; and
- no curator diagnostics.

The two critical inputs were refreshed through the bounded
`/physics/claim-status/` snapshot and coupled route/provenance identity. No
public prose or scientific claim was strengthened, and the upstream source
repository was not changed.

## Control-runtime repairs

The post-migration repair chain remained fail-closed:

- AFDOC-R001A preserved exact validator argv while changing Director-decision
  evidence references to the relative website task authority record. This
  allowed absolute executables such as `/usr/bin/env` without treating command
  text as a path or widening command authority; 18 focused tests passed.
- AFDOC-R001B added an explicit full upstream commit selector through
  `AETHER_FLOW_SOURCE_COMMIT` or `--source-commit`. Missing, malformed, and
  non-commit pins fail closed, and pinned reads cannot fall back to a moving
  worktree; 17 focused tests and the pinned curator check passed.
- AFDOC-R004 recognized environment-wrapped or argument-bearing forms only
  when the unwrapped argv is an already known validator command. Unknown or
  malformed wrappers still fail, and an empty validator list is accepted only
  for canonical inactive/no-action state; 26 focused tests and structural
  implementation-control validation passed.
- AFDOC-R005 made terminal-plan repository identity historical receipt
  evidence while retaining current HEAD, binding, topology, lease, worker,
  packet, changed-path, staged-file, and unrelated-drift enforcement for every
  nonterminal plan. Durable exact recovery bindings were validated; 19 focused
  tests and `npm run validate:plan-goal` passed.

These repairs did not authorize active-control substitution, arbitrary command
execution, staged files, branch or worktree changes, or external effects.

## Validation evidence

The final evidence sequence includes:

- AFDOC-028: `npm run build` passed for 63 static pages before the bounded
  `/documents` redirect collision was repaired.
- AFDOC-035: the repaired build passed for 64 static pages; Cloudflare
  configuration and the desktop/compact headed-browser review passed.
- AFDOC-030: Cloudflare validation and the representative status/Location
  matrix passed, including 15 direct Resources redirects and the documented
  `/research` `302` exception.
- AFDOC-034 and AFDOC-036: required-route, manifest, provenance, and Cloudflare
  checks passed for the final 15 Documents and 34 total canonical routes.
- AFDOC-038: `npm run validate:curator`, `npm run validate:manifests`,
  `npm run validate:provenance`, `npm run validate:claims`, and
  `git diff --check` passed against the reviewed source snapshot.
- AFDOC-R004 and AFDOC-R005: the focused implementation-control and plan-goal
  repairs passed their tests and structural validators.

AFDOC-R006 then invoked the post-repair aggregate exactly once:

```text
/usr/bin/env AETHER_FLOW_SOURCE_COMMIT=c6aa66b9a7412f14c6573dd0467b82ea11310c20 npm run validate
```

The command exited `0`. Manifest, content, claim, internal-link, layout, SVG,
provenance, curator, Cloudflare, implementation-control, plan-goal, plan-goal
test, and Astro build stages all passed. The plan-goal suite reported 78
passing tests, and Astro built 64 static pages. The subsequent R006
`git diff --check` also passed.

The durable aggregate receipt is
`PTR-b33588398239f93ead44122d70d88f73`, with receipt SHA-256
`42514584323a156ee5abe9634e3e576846b569c909fb738ad02a9b9f3a29ef6c`.

### Checks intentionally not rerun in AFDOC-R007

AFDOC-R007 runs only its bound manual inspection of this record and
`git diff --check`. It does not rerun the aggregate, build, headed-browser
review, redirect matrix, curator generation/check, manifest/provenance/claim
suites, or focused control-runtime tests. Their results are cited from the
accepted receipts above. In particular, rerunning the aggregate would violate
the coordinator's exact-one-run recovery boundary.

No deployment, publication, remote smoke test, or upstream mutation check was
attempted because those effects are outside this task's authority.

## External-effect status

For AFDOC-R007 and the accepted post-repair validation chain:

| Effect | Status |
| --- | --- |
| Product write | Only this evidence file is authorized |
| Reader route or navigation change | Not performed |
| Manifest or public asset change | Not performed |
| Scientific claim or authority promotion | Not performed |
| Upstream source-project write | Forbidden and not performed |
| Branch or worktree creation | Not authorized and not performed |
| Git staging | Not authorized and not performed |
| New commit | Not authorized and not performed |
| Push or merge | Not authorized and not performed |
| Cloudflare deployment | Not authorized and not performed |
| Publication | Not authorized and not performed |

The existing local migration checkpoint is historical repository evidence, not
proof that AFDOC-R007 performed a release. This record also does not establish
that another plan task or the global plan goal is complete. The plan worker
must finalize AFDOC-R007 from the two bound validator results and return control
to the coordinator without reserving a successor.

## References

The Æther Flow Website. (2026, July 21). *Implement canonical Documents
navigation migration* [Git commit `7292ff009e3dbab89deb307a405cc6bb863caaf1`].

The Æther Flow Website. (2026, July 21). *AFDOC-030 redirect verification*
[Implementation-control completion record].
`implementation_control/tasks/WI-20260720-030/jobs/completions/WJC-20260720-030-A.yaml`.

The Æther Flow Website. (2026, July 21). *AFDOC-035 Documents route and headed
browser repair review* [Implementation-control completion record].
`implementation_control/tasks/WI-20260720-035/jobs/completions/WJC-20260720-035-A.yaml`.

The Æther Flow Website. (2026, July 21). *AFDOC-038 curator reconciliation*
[Implementation-control completion record].
`implementation_control/tasks/WI-20260721-038/jobs/completions/WJC-20260721-038-A.yaml`.

The Æther Flow Website. (2026, July 21). *AFDOC-R001A plan adapter repair*
[Implementation-control completion record].
`implementation_control/tasks/WI-20260721-043/jobs/completions/WJC-20260721-043-A.yaml`.

The Æther Flow Website. (2026, July 21). *AFDOC-R001B curator source-pin repair*
[Implementation-control completion record].
`implementation_control/tasks/WI-20260721-044/jobs/completions/WJC-20260721-044-A.yaml`.

The Æther Flow Website. (2026, July 21). *AFDOC-R004 implementation-control
validator repair* [Implementation-control completion record].
`implementation_control/tasks/WI-20260721-045/jobs/completions/WJC-20260721-045-A.yaml`.

The Æther Flow Website. (2026, July 22). *AFDOC-R005 plan-goal terminal-history
repair* [Implementation-control completion record].
`implementation_control/tasks/WI-20260721-046/jobs/completions/WJC-20260721-046-A.yaml`.

The Æther Flow Website. (2026, July 22). *AFDOC-R006 pinned post-repair aggregate
validation* [Implementation-control completion record].
`implementation_control/tasks/WI-20260721-047/jobs/completions/WJC-20260721-047-A.yaml`.
