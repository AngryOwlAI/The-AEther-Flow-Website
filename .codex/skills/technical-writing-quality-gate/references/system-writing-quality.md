# Website Technical Writing Quality Reference

Use this checklist for substantial technical, scientific, system, governance,
operational, or public-facing prose.

## Intake

- What artifact is being written or reviewed?
- Who is the audience and what should they understand or do afterward?
- What is the publication surface?
- What working thesis or purpose governs the text?
- Which upstream and website sources are authoritative for each claim class?
- What must remain out of scope?

Return `block` when the missing answer would require invented facts, authority,
intent, or certainty.

## Concrete Content

Strong technical prose normally identifies:

- the system, theory element, document, process, or decision under discussion;
- its actors, users, maintainers, or accountable reviewers;
- relevant inputs, outputs, interfaces, records, and dependencies;
- the mechanism, workflow, control loop, or causal sequence;
- constraints, validity regimes, limits, failure modes, and open questions;
- evidence supporting each outcome or status statement.

## Builder Pass

- Put the concrete subject and defining claim early.
- Use specific nouns, active verbs, and named mechanisms.
- Explain causal or procedural sequence where it matters.
- Preserve exact project terminology and qualifications.
- Match detail and vocabulary to the audience.
- Make assumptions, uncertainty, exclusions, and limitations visible.
- Use APA 7 for cited documents and include exact local evidence paths when
  practical.

## Refuter Pass

- Can every material claim be traced to the appropriate authority level?
- Has inference been labeled rather than presented as source fact?
- Does any sentence strengthen `open`, `proposed`, `adopted`, or
  `effective-level` language into completion or proof?
- Does a validator, registry, review, AI output, generated artifact, or website
  page receive authority it does not possess?
- Does the prose imply independent validation, empirical support, security,
  reliability, performance, scale, or benefit without evidence?
- Does polished framing delay or obscure the concrete subject?
- Could the text reduce length or repetition without losing necessary
  qualifications?

## Gate Decision

Return `pass` when the prose is specific, source-grounded, audience-fit, and
proportional to evidence.

Return `repair` when available evidence supports direct fixes to vague wording,
inflated tone, weak sequence, unsupported benefit language, or missing concrete
mechanics.

Return `block` when missing evidence, authority, audience, intent, or review
status prevents responsible writing or evaluation.

## Warning Matcher Interpretation

Warning words are review prompts, not prohibited vocabulary. A term such as
`dynamic` can be technically precise in context. Read the sentence, determine
whether a mechanism or source supports it, and repair only the actual defect.

No matcher result proves factual correctness, source coverage, originality, or
human authorship.
