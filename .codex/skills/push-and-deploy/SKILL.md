---
name: push-and-deploy
description: Push accepted The AEther Flow Website changes to GitHub, then deploy the pushed commit to Cloudflare Pages by Wrangler Direct Upload.
disable-model-invocation: true
---

# Push And Deploy

## Purpose

Publish accepted The AEther Flow Website changes through the current safe
deployment path:

1. verify the local repository;
2. push the accepted `main` commit to GitHub;
3. deploy that pushed commit to Cloudflare Pages by Wrangler Direct Upload;
4. smoke-test the production URL.

This skill standardizes Codex-operated deployment. It does not create true
Cloudflare Pages Git integration. The current Cloudflare Pages project remains
a Direct Upload project until the Cloudflare Pages GitHub App issue is repaired
and the project is deliberately migrated or replaced.

## Use When

- The user asks to push and deploy this website.
- The user asks to publish accepted website changes to production.
- The user asks to run the website deployment packet after a commit.

Do not use this skill for upstream research-repo work, source-sync work,
Cloudflare project deletion/recreation, custom-domain changes, or Cloudflare
Git integration migration unless the user explicitly asks for that separate
infrastructure packet.

## Deployment Rule

Deploy after push, not merely after commit.

A commit is a local source snapshot. A push makes that commit available on the
GitHub remote and gives the deployment a remote, auditable source of truth. The
Cloudflare Direct Upload metadata must use the pushed commit hash.

## Preconditions

- Repository root:

  ```bash
  /Volumes/P-SSD/AngryOwl/The-AEther-Flow-Website
  ```

- Production branch: `main`.
- Git remote: `origin`.
- Cloudflare Pages project: `the-aether-flow-website`.
- Production URL: `https://the-aether-flow-website.pages.dev`.
- The user has accepted the code/content changes.
- The worktree is clean before deployment. If the user also asked to commit,
  finish the commit first, then restart this deployment preflight from a clean
  worktree.
- Wrangler must already be authenticated with Cloudflare Pages write access.

## Workflow

### 1. Inspect repository state

```bash
git status --short --branch
git branch --show-current
git rev-parse HEAD
```

Stop if the current branch is not `main`, unless the user explicitly requested
a preview-branch deploy. This skill defaults to production only.

Stop if the worktree has uncommitted, staged, or untracked files. Do not deploy
dirty local state.

### 2. Run the quality gate

```bash
make quality
```

Stop on any failure. Do not push or deploy a failing build.

After the quality gate, inspect the worktree again. Stop if validation,
formatting, or build output changed tracked or untracked files.

### 3. Push the accepted commit

```bash
git fetch origin main
git push origin main
git fetch origin main
```

Stop if local `main` is behind `origin/main`. The correct next action is to
inspect and reconcile the branch before deployment.

Verify that `HEAD` matches `origin/main` after push:

```bash
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

### 4. Deploy the pushed commit

```bash
npx --yes wrangler@latest pages deploy dist \
  --project-name the-aether-flow-website \
  --branch main \
  --commit-hash "$(git rev-parse HEAD)" \
  --commit-message "$(git log -1 --pretty=%s)" \
  --commit-dirty=false
```

Use `main` for production. Do not delete, recreate, or migrate the Cloudflare
Pages project as part of this skill.

### 5. Verify production

```bash
python scripts/smoke_test_site.py \
  --base-url https://the-aether-flow-website.pages.dev \
  --timeout 20

npx --yes wrangler@latest pages deployment list \
  --project-name the-aether-flow-website \
  --environment production
```

Confirm the deployment list shows the expected branch and source hash. The
project will still show `Git Provider: No`; that is expected for the current
Direct Upload project.

## Helper Script

For the standard production path, run:

```bash
bash .codex/skills/push-and-deploy/scripts/push_and_deploy.sh
```

The script enforces the clean-tree, quality, push, deploy, and smoke-test
sequence above.

## Failure Handling

- If Wrangler authentication is missing, stop and report the exact failing
  command. The logical next step is Wrangler login or a Cloudflare API token
  with Pages write access.
- If GitHub push fails, stop before deployment.
- If Cloudflare deploy fails, do not retry blindly. Inspect the Wrangler error,
  deployment list, and production smoke result.
- If the smoke test fails, report the failed route/status and treat it as a
  production defect packet.

## Final Response Contract

Report:

- pushed commit hash;
- deployment method: Cloudflare Pages Direct Upload;
- production URL;
- quality gate result;
- production smoke-test result;
- any remaining uncertainty or blocker.

If staging, committing, pushing, or creating a PR occurred, emit the appropriate
Codex app git directive in the final response.
