# Implementation Checklist

## Before Editing

- Identify the existing page, layout, component, and style conventions.
- Run the scanner and read the generated brief.
- Inspect source files directly before adding strong public claims.
- Confirm whether the upstream source root is available.
- Decide whether a new page needs source manifest entries or existing source
  references.

## During Implementation

- Use Astro and the existing static-site structure.
- Keep content reader-facing and source-boundary aware.
- Use real project language from reviewed evidence.
- Include claim status and source authority notices where required.
- Avoid new production dependencies.
- Preserve accessible headings, links, focus states, and mobile behavior.

## After Implementation

- Build the site.
- Run the project explainer frontend audit.
- Run existing validators and quality gates.
- Use Playwright CLI and Playwright Interactive QA on `127.0.0.1`.
- Store screenshots or browser artifacts under `output/playwright/`.
