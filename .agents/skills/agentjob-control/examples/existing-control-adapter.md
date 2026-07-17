# Portable Example: Existing-Control Adapter

## Scenario

A project already stores work items, route approvals, bounded work packets,
operator roles, results, and handoffs in its own control database. The project
wants governed continuation without replacing that system.

## Conformance mapping

The adapter reports each portable feature as `native`, `emulated`, or
`unsupported`:

| Portable feature | Project mapping | Mode |
| --- | --- | --- |
| Task | Work item | native |
| Director Decision | Route approval | native |
| AgentJob | Bounded work packet | native |
| ExecutionRole | Packet-local operator binding | emulated |
| Activation | Transactional approval commit with exact hashes | native |
| Supersession | Append-only replacement link | native |
| Completion | Result record with path, command, validator, and claim evidence | native |
| Handoff | Next-route recommendation with no authority grant | emulated |
| At-most-once goal generation | No equivalent | unsupported |

Because a mandatory relay feature is unsupported, automatic goal relay is
blocked. The adapter may still support one bounded `continue` transaction if
all of that capability's required semantics pass conformance. It must not
report full governed-continuation support or emulate consumption with
conversation prose.

## Safe alternatives

- implement and test a project-owned at-most-once relay mapping;
- install the reference local relay backend while leaving the existing control
  records canonical, if project policy permits that split;
- use manual, nonrecursive one-job continuation only;
- stop and retain the capability blocker.

Authority status: the conformance report is inspect-only evidence. It does not
execute a job, repair the existing system, or make an unsupported feature
available.
