#!/usr/bin/env bash
set -Eeuo pipefail

REMOTE="origin"
BRANCH="main"
PROJECT_NAME="the-aether-flow-website"
BASE_URL="https://the-aether-flow-website.pages.dev"

usage() {
  cat <<'USAGE'
Usage: push_and_deploy.sh [options]

Push the current clean main commit, then deploy that pushed commit to
Cloudflare Pages by Wrangler Direct Upload.

Options:
  --remote NAME        Git remote to push. Default: origin
  --branch NAME        Branch to push and deploy. Default: main
  --project-name NAME  Cloudflare Pages project. Default: the-aether-flow-website
  --base-url URL       Production URL for smoke test.
                       Default: https://the-aether-flow-website.pages.dev
  -h, --help           Show this help text.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --remote)
      REMOTE="${2:?missing value for --remote}"
      shift 2
      ;;
    --branch)
      BRANCH="${2:?missing value for --branch}"
      shift 2
      ;;
    --project-name)
      PROJECT_NAME="${2:?missing value for --project-name}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:?missing value for --base-url}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
}

require_clean_worktree() {
  local status
  status="$(git status --porcelain)"
  if [[ -n "$status" ]]; then
    echo "ERROR: worktree must be clean before push and deploy." >&2
    git status --short --branch >&2
    exit 1
  fi
}

clean_generated_artifacts() {
  find .codex -type d -name __pycache__ -prune -exec rm -rf {} +
  find .codex -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
}

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

current_branch="$(git branch --show-current)"
if [[ "$current_branch" != "$BRANCH" ]]; then
  echo "ERROR: current branch is '$current_branch', expected '$BRANCH'." >&2
  exit 1
fi

require_clean_worktree

run make quality

clean_generated_artifacts
require_clean_worktree

run git fetch "$REMOTE" "$BRANCH"

read -r behind ahead < <(git rev-list --left-right --count "$REMOTE/$BRANCH...HEAD")
if [[ "$behind" != "0" ]]; then
  echo "ERROR: local $BRANCH is behind $REMOTE/$BRANCH by $behind commit(s)." >&2
  echo "Inspect and reconcile the branch before deployment." >&2
  exit 1
fi

if [[ "$ahead" != "0" ]]; then
  run git push "$REMOTE" "$BRANCH"
else
  echo "Local $BRANCH is already pushed to $REMOTE/$BRANCH."
fi

run git fetch "$REMOTE" "$BRANCH"

local_head="$(git rev-parse HEAD)"
remote_head="$(git rev-parse "$REMOTE/$BRANCH")"
if [[ "$local_head" != "$remote_head" ]]; then
  echo "ERROR: HEAD does not match $REMOTE/$BRANCH after push." >&2
  echo "HEAD: $local_head" >&2
  echo "$REMOTE/$BRANCH: $remote_head" >&2
  exit 1
fi

commit_message="$(git log -1 --pretty=%s)"

run npx --yes wrangler@latest pages deploy dist \
  --project-name "$PROJECT_NAME" \
  --branch "$BRANCH" \
  --commit-hash "$local_head" \
  --commit-message "$commit_message" \
  --commit-dirty=false

run python scripts/smoke_test_site.py \
  --base-url "$BASE_URL" \
  --timeout 20

run npx --yes wrangler@latest pages deployment list \
  --project-name "$PROJECT_NAME" \
  --environment production

echo "Push and deploy complete for $local_head."
