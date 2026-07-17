# Third-Party Notices

## Sys4AI Governed Continuation Bundle

The vendored `agentjob-control`, `continue`, `continue-goal`, and
`continue-implementing-goal` packages are imported from
`/Volumes/P-SSD/AngryOwl/skills-Sys4AI` at source commit
`f2852d5273ed7297a0abd55c9aecfbf7f5e4507e`. The exact imported bundle is
`governed-continuation` version `0.1.0`, retained with its source `draft`
status and explicit-invocation policy.

Copyright 2026 Alexander Samuel Ricciardi, AngryOwl. The source packages are
licensed under the Apache License, Version 2.0.

The website adaptation adds project-local Codex front doors, a facade and
adapter for the existing `implementation_control/` authority, tracked source
lock and configuration, ignored local runtime state, activation receipts,
integrity validation, and website-specific regression coverage. The exact
vendor copies under `.agents/skills/` are unmodified. No portable
`.agents/control/` system is bootstrapped.

Read-only neutral fixture projects and the Codex integration contract required
by the complete vendored unit suite are retained under `.agents/examples/` and
`.agents/docs/`. They are source-pinned validation resources, not runtime
authority or website content.

## Technical Writing Quality Gate Adaptation

The local `technical-writing-quality-gate` skill is adapted from the
Sys4AI-dev package at source commit
`ef93cc008f1d3d91129e86bb4ce48b1435c17f6d`.

Copyright 2026 Alexander Samuel Ricciardi, AngryOwl. The source package is
licensed under the Apache License, Version 2.0. The website adaptation changes
the runtime location, authority hierarchy, project guidance, example,
metadata, matcher reporting, and regression coverage. The website repository's
Apache-2.0 tooling terms apply to these modifications without changing the
source license or attribution.

## Matt Pocock Skill Adaptations

Portions of the local `prototype` and `to-prd` skills are adapted from:

- Matt Pocock's `prototype` skill:
  https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype
- Matt Pocock's `to-prd` skill:
  https://github.com/mattpocock/skills/tree/main/skills/engineering/to-prd

Source snapshot checked during integration:
`5d78bd0903420f97c791f834201e550c765699f8`.

## MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
