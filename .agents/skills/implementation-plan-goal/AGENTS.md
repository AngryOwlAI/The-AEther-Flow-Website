# Deprecated Launcher Shim Rules

- Route new runs only to `implementation-plan-relay`.
- State the deprecation and no-Goal/no-coordinator boundary.
- Never mutate legacy records without the explicit legacy selector.
- Do not add runtime logic here; canonical implementation lives in the new
  launcher and shared plan-relay runtime.
