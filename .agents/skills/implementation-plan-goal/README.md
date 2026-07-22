# implementation-plan-goal (deprecated)

<!-- BEGIN GENERATED INSTALLATION BANNER -->
> **Dependency-resolved workflow:** Select this skill with the installer; do not copy the folder without its required closure.
>
> **Installation class:** `user_workflow` / `dependency_resolved`<br>
> **User-selectable:** yes<br>
> **Direct copy allowed:** no<br>
> **Required dependencies:** `implementation-plan-relay`, `continue-implementing-plan-task`<br>
> **Recommended bundle:** none<br>
> **Recommended plugin:** none<br>
> **Mutable state required:** yes — `{project_root}/.local/sys4ai/implementation-plan-relay`; keep it outside installed skill/plugin trees and preserve it on uninstall<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill implementation-plan-goal --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

Compatibility launcher name. New accepted runs resolve to
`implementation-plan-relay` and `recursive_chain_v1`; no Goal or coordinator
is created. Legacy coordinator data remains available through explicit
read-only status/export and the documented compatibility policy.
