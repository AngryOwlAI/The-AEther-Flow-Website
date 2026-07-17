# Portable Example: Bootstrap Required

## Scenario

An operator asks `continue` to modify a small project that has no
`.agents/control/config.yaml` and no compatible existing-control adapter.

## Read-only diagnosis

```bash
python3 <AGENTJOB_CONTROL_PATH>/scripts/agentjobctl.py \
  doctor --project-root <PROJECT_ROOT> --json
```

Expected result:

```json
{
  "status": "error",
  "code": "bootstrap.required",
  "details": {
    "execution_performed": false
  }
}
```

The CLI exits with code `3`. No source, control, or local-state path is
created. The requested project change is not attempted.

## Safe next action

Inspect the exact locked installation plan:

```bash
python3 scripts/skills/install_skill_bundle.py \
  --bundle governed-continuation \
  --target-project <PROJECT_ROOT> \
  --json
```

Installation and bootstrap require explicit approval. If the project already
has a control system, evaluate an adapter before installing a competing
canonical record tree.

Authority status: the diagnostic and installation plan are non-authoritative
evidence. They do not grant permission to bootstrap, overwrite project files,
or execute the original request.
