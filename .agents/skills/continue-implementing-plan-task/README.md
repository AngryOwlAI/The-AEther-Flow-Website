# continue-implementing-plan-task (deprecated)

<!-- BEGIN GENERATED INSTALLATION BANNER -->
> **Internal component:** Do not install this folder as a root. Use its owning bundle or plugin.
>
> **Installation class:** `internal_component` / `internal_only`<br>
> **User-selectable:** no — not a user-selected install root<br>
> **Direct copy allowed:** no<br>
> **Required dependencies:** `continue-implementation-plan-relay`<br>
> **Recommended bundle:** `implementation-plan-relay`<br>
> **Recommended plugin:** none<br>
> **Mutable state required:** yes — `{project_root}/.local/sys4ai/implementation-plan-relay`; keep it outside installed skill/plugin trees and preserve it on uninstall<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill continue-implementing-plan-task --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

Compatibility frame name. New calls route to
`continue-implementation-plan-relay`, which owns N-to-N+1 scheduling and stops
without any coordinator wake/resume path.
