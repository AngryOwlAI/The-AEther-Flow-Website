# The AEther Flow Website

This repository is the website-development workspace for
`/Volumes/P-SSD/AngryOwl/The-AEther-Flow`.

The source research repository remains the authority for scientific claims,
research-control state, source documents, registries, validators, and generated
derivative rules. This website repository should present, organize, and publish
reader-facing material without silently changing the underlying research
claims.

## Purpose

- Build the public website for The AEther Flow research project.
- Keep website implementation separate from the source research-control repo.
- Preserve a clear boundary between public presentation and source authority.
- Track website code, assets, build configuration, and deployment notes here.

## Current Status

The repository now contains an Astro static-site scaffold with MDX, KaTeX,
manifest-backed downloads, Python/Bash validation tooling, Docker development
configuration, first reader-facing content pages, and Cloudflare Pages
configuration files.

Project-local Codex skills live in:

```text
.codex/skills/
```

The current local skills include `prototype` for throwaway design exploration
and `to-prd` for local PRD synthesis.

Build and validation entry points:

```bash
make install
make validate
make test
make lint
```

Cloudflare Pages settings are documented in:

```text
docs/deployment/cloudflare-pages.md
```

## Source Authority Boundary

Authoritative project state belongs in the source repository:

```text
/Volumes/P-SSD/AngryOwl/The-AEther-Flow
```

Website content should be derived from reviewed source material, publication
briefs, source specs, or other approved project surfaces. If a website page
needs to make or change a scientific, mathematical, governance, or research
workflow claim, update and validate the source repository first.

## Git Remote

This repository is connected to the AngryOwlAI GitHub repository using Alex's
Omegapy SSH identity:

```text
git@github-omegapy:AngryOwlAI/The-AEther-Flow-Website.git
```

This keeps the repository owned by `AngryOwlAI` while authenticating pushes
through Alex's GitHub collaborator account.
