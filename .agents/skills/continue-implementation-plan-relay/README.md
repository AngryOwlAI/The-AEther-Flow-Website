# continue-implementation-plan-relay

<!-- BEGIN GENERATED INSTALLATION BANNER -->
> **Internal component:** Do not install this folder as a root. Use its owning bundle or plugin.
>
> **Installation class:** `internal_component` / `internal_only`<br>
> **User-selectable:** no — not a user-selected install root<br>
> **Direct copy allowed:** no<br>
> **Required dependencies:** `agentjob-control`, `continue`<br>
> **Recommended bundle:** `implementation-plan-relay`<br>
> **Recommended plugin:** none<br>
> **Mutable state required:** yes — `{project_root}/.local/sys4ai/implementation-plan-relay`; keep it outside installed skill/plugin trees and preserve it on uninstall<br>
> **Install command:** `python3 scripts/skills/install_skills.py --skill continue-implementation-plan-relay --target-project <PROJECT_ROOT>`<br>
> **Canonical installation documentation:** [INSTALL.md](../../INSTALL.md)
<!-- END GENERATED INSTALLATION BANNER -->

Internal recursive frame for one plan-native generation. It owns the complete
claim -> consume -> one task call -> receipt -> decision -> zero/one successor
boundary and then stops. It has no coordinator return, wakeup, resume, or
generic Goal dependency.
