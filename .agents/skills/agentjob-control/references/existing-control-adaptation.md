# Existing-Control Adaptation

An existing project control system may remain canonical when its adapter maps
the complete portable authority model without creating a second competing
store.

Required semantic mappings are:

| Existing concept | Portable authority |
| --- | --- |
| Work item | Task |
| Route selection | Director Decision |
| Execution contract | AgentJob |
| Bound operator role | ExecutionRole |
| Result evidence | Completion |
| Continuity evidence | Handoff |

The adapter must additionally prove immutable activated evidence,
supersession instead of in-place correction, at most one AgentJob per
continuation, explicit path and claim boundaries, and recovery evidence for
ambiguous or consumed execution.

Each conformance feature is reported as `native`, `emulated`, or
`unsupported`. Emulation is acceptable only when evidence proves equivalent
semantics. Missing evidence is blocking. Unsupported core authority cannot be
masked by prose, a generated index, or a cache.

The conformance report is inspect-only. It does not execute a job, repair
records, promote derivatives, or mutate the existing control system.
